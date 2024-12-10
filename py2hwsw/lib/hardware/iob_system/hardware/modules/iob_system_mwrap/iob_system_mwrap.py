# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import copy

import iob_system


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    iob_system_attr = iob_system.setup(params)

    attributes_dict = {
        "name": params["name"] + "_mwrap",
        "version": "0.1",
        "confs": [
            {
                "name": "BOOT_HEXFILE",
                "descr": "Bootloader file name",
                "type": "P",
                "val": f'"{params["name"]}_bootrom"',
                "min": "NA",
                "max": "NA",
            },
        ]
        + iob_system_attr["confs"],
    }

    # Declare memory wrapper ports and wires automatically based on iob-system ports.
    mwrap_wires = []
    mwrap_ports = []
    for port in iob_system_attr["ports"]:
        if port["name"] in ["rom_bus_io", "int_mem_axi_m"]:
            wire = copy.deepcopy(port)
            if type(wire["signals"]) is list:
                for sig in wire["signals"]:
                    if any(sig["name"].endswith(s) for s in ["_o", "_i", "_io"]):
                        sig["name"] = sig["name"][:-2]
                        if sig["name"].endswith("_"):
                            sig["name"] = sig["name"][:-1]
            mwrap_wires.append(wire)
        else:
            mwrap_ports.append(port)

    attributes_dict["ports"] = mwrap_ports

    attributes_dict["wires"] = mwrap_wires + [
        {
            "name": "clk",
            "descr": "Clock signal",
            "signals": [
                {"name": "clk_i"},
            ],
        },
        {
            "name": "rst",
            "descr": "Reset signal",
            "signals": [
                {"name": "arst_i"},
            ],
        },
    ]
    attributes_dict["subblocks"] = [
        # ROM
        {
            "core_name": "iob_rom_sp",
            "instance_name": "boot_rom",
            "instance_description": "Boot ROM",
            "parameters": {
                "ADDR_W": params["bootrom_addr_w"] - 2,
                "DATA_W": params["data_w"],
                "HEXFILE": '{BOOT_HEXFILE, ".hex"}',
            },
            "connect": {
                "clk_i": "clk",
                "rom_if_io": "rom_bus_io",
            },
        },
        # Internal memory
        {
            "core_name": "iob_axi_ram",
            "instance_name": "internal_memory",
            "instance_description": "Internal memory",
            "if_defined": "IOB_MEM_NO_READ_ON_WRITE",
            "parameters": {
                "ID_WIDTH": "AXI_ID_W",
                "ADDR_WIDTH": params["fw_addr_w"],
                "DATA_WIDTH": "AXI_DATA_W",
                "READ_ON_WRITE": 0,
            },
            "connect": {
                "clk_i": "clk",
                "rst_i": "rst",
                "axi_s": (
                    "int_mem_axi_m",
                    [
                        "{int_mem_axi_araddr, 2'b0}",
                        "{int_mem_axi_awaddr, 2'b0}",
                        "{1'b0, int_mem_axi_arlock}",
                        "{1'b0, int_mem_axi_awlock}",
                    ],
                ),
            },
        },
    ]
    if params["init_mem"]:
        attributes_dict["subblocks"][-1]["parameters"].update(
            {
                "FILE": f'"{params["name"]}_firmware"',
            }
        )

    # Copy iob_axi_ram block, but with READ_ON_WRITE=1
    attributes_dict["subblocks"].append(copy.deepcopy(attributes_dict["subblocks"][-1]))
    attributes_dict["subblocks"][-1].pop("if_defined")
    attributes_dict["subblocks"][-1]["if_not_defined"] = "IOB_MEM_NO_READ_ON_WRITE"
    attributes_dict["subblocks"][-1]["parameters"].update(
        {
            "READ_ON_WRITE": 1,
        }
    )

    attributes_dict["subblocks"].append(
        # IOb-System
        {
            "core_name": py_params_dict["instantiator"]["original_name"],
            "instance_name": py_params_dict["instantiator"]["original_name"],
            "instance_description": "IOb-SoC core",
            # "setup": False,  # FIXME: Remove this
            "parameters": {
                i["name"]: i["name"]
                for i in iob_system_attr["confs"]
                if i["type"] in ["P", "F"]
            },
            "connect": {i["name"]: i["name"] for i in iob_system_attr["ports"]},
            # **params,  # FIXME: Remove this
        }
    )

    return attributes_dict
