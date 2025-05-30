# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import copy
import os
import sys
from latex import write_table
from iob_base import find_obj_in_list, import_python_module
from iob_core import find_module_setup_dir


def setup(py_params_dict):
    """Memory wrapper core. Inteended to be used as a superblock of other cores.
    Required memories are automatically generated based on the ports of the instantiator (subblock).
    """
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        py_params_dict["mem_if_names"] = []
        py_params_dict["instantiator"] = {
            "original_name": "iob_core",
            "name": "iob",
            "confs": [],
            "ports": [],
        }

    # List of supported memory interfaces (usually taken from if_gen.py)
    mem_if_names = py_params_dict["mem_if_names"]
    attrs = py_params_dict["instantiator"]

    attributes_dict = {
        "name": f"{attrs['name']}_mwrap",
        "generate_hw": True,
        "confs": attrs["confs"],
    }

    mwrap_wires = []
    mwrap_ports = []
    memory_ports = []
    for port in attrs["ports"]:
        if isinstance(port["signals"], dict):
            if port["signals"]["type"] in mem_if_names:
                wire = copy.deepcopy(port)
                wire["name"] = wire["name"][:-2]
                mwrap_wires.append(wire)
                memory_ports.append(port)
            else:
                mwrap_ports.append(port)
        else:
            mwrap_ports.append(port)

    attributes_dict["ports"] = mwrap_ports

    attributes_dict["wires"] = mwrap_wires

    connect_dict = {
        p["name"]: w["name"]
        for p, w in zip(memory_ports + mwrap_ports, mwrap_wires + mwrap_ports)
    }

    attributes_dict["subblocks"] = [
        {
            "core_name": attrs["original_name"],
            "instance_name": f"{attrs['name']}_inst",
            "instance_description": "Wrapped module",
            "parameters": {
                i["name"]: i["name"] for i in attrs["confs"] if i["type"] in ["P", "D"]
            },
            "connect": connect_dict,
        }
    ]

    list_of_mems = []
    for wire in mwrap_wires:
        if wire["signals"].get("prefix", None):
            prefix_str = wire["signals"]["prefix"]
        else:
            prefix_str = wire["name"] + "_"

        signals_type = wire["signals"]["type"]

        # Instance name
        name = f"{prefix_str}mem"
        # Memory type
        type = f"iob_{signals_type}"
        # Data bus width
        data_w = wire["signals"].get("DATA_W", 32)
        # Address bus width
        word_addr_w = wire["signals"].get("ADDR_W", 32)
        # Memory init hexfile name
        hexfile_param = f"{prefix_str.upper()}HEXFILE"
        hexfile_obj = find_obj_in_list(attrs["confs"], hexfile_param)
        if hexfile_obj is None:
            hexfile = "none"
            hexfile_param = '"none"'
        else:
            hexfile = hexfile_obj["val"]

        # Add memory instance to list
        list_of_mems.append(
            {
                "name": name,
                "type": type,
                "addr_w": word_addr_w,
                "data_w": data_w,
                "hexfile": hexfile,
            }
        )

        # Extra Verilog parameters for this memory subblock
        extra_params = {}
        if "ram" in type:
            # check if memory module has MEM_NO_READ_ON_WRITE conf
            mem_dir, file_ext = find_module_setup_dir(type)
            import_python_module(os.path.join(mem_dir, f"{type}.py"))
            mem_module = sys.modules[type]
            mem_dict = mem_module.setup({})
            if "MEM_NO_READ_ON_WRITE" in mem_dict["confs"]:
                extra_params["MEM_NO_READ_ON_WRITE"] = mem_dict["MEM_NO_READ_ON_WRITE"]

        # Add memory instace to subblocks list
        attributes_dict["subblocks"].append(
            {
                "core_name": type,
                "instance_name": name,
                "parameters": {
                    "DATA_W": data_w,
                    "ADDR_W": word_addr_w,
                    "HEXFILE": hexfile_param,
                }
                | extra_params,
                "connect": {
                    f"{signals_type}_s": wire["name"],
                },
            }
        )

    if "superblocks" in attrs:
        attributes_dict["superblocks"] = attrs["superblocks"]

    # Add MEM_NO_READ_ON_WRITE to the attributes dictionary
    # if the user has not set it
    has_mem_no_read_on_write_in_attrs = False
    for conf in attrs["confs"]:
        if conf["name"] == "MEM_NO_READ_ON_WRITE":
            has_mem_no_read_on_write_in_attrs = True
            break
    if not has_mem_no_read_on_write_in_attrs:
        attributes_dict["confs"] += [
            {
                "name": "MEM_NO_READ_ON_WRITE",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "1",
                "descr": "No simultaneous read/write",
            },
        ]

    # Generate LaTeX table of memories
    # But don't create files for other targets (like clean)
    if py_params_dict.get("py2hwsw_target", "") == "setup":
        assert py_params_dict["build_dir"], "[iob_memwrapper]: Error: build_dir not set"
        generate_mems_tex(
            list_of_mems, os.path.join(py_params_dict["build_dir"], "document/tsrc")
        )

    return attributes_dict


#
# Document functions
#


# Generate mems.tex file with list TeX tables of mems
def generate_mems_tex(mems, out_dir):
    """Generate TeX for memories section
    :param mems: list of memories
    :param out_dir: output directory
    """
    os.makedirs(out_dir, exist_ok=True)
    mems_file = open(f"{out_dir}/mems.tex", "w")

    mems_file.write(
        """
    The memories of the core are described in the following table.
    The tables give information on the name, type, address and data width in bits, and initialization file name.
"""
    )

    mems_file.write(
        """
    \\begin{xltabular}{\\textwidth}{|l|c|c|c|X|}
      \\hline
      \\rowcolor{iob-green}
      {\\bf Name} & {\\bf Type} & {\\bf (Word-)Addr Width} & {\\bf Data Width} & {\\bf Init file} \\\\ \\hline
      \\input mems_tab
      \\caption{Table of memories of the core}
    \\end{xltabular}
    \\label{mems_tab:is}
"""
    )

    mems_file.write("\\clearpage")
    mems_file.close()

    # Generate mems table
    tex_table = []
    for mem in mems:
        tex_table.append(
            [
                mem["name"],
                mem["type"],
                str(mem["addr_w"]),
                str(mem["data_w"]),
                mem["hexfile"],
            ]
        )

    write_table(f"{out_dir}/mems", tex_table)
