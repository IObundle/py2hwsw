# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os
import copy

# Add csrs scripts folder to python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from reg_gen import generate_csr
from csr_classes import create_csr_group
from interrupts import find_and_update_interrupt_csrs
from fifos import find_and_update_fifo_csrs
from roms import find_and_update_rom_csrs
from memories import find_and_update_regarray_csrs
from memories import find_and_update_regfile_csrs
from memories import find_and_update_ram_csrs
from special_csrs import find_and_update_autoclear_csrs

# Static (shared) dictionary to store reg tables of generated csrs
# May be read by other python modules
static_reg_tables = {}


def setup(py_params_dict):
    """Standard Py2HWSW setup function"""
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        py_params_dict["csrs"] = [
            {
                "name": "reg_group",
                "descr": "Dummy reg group",
                "regs": [
                    {
                        "name": "dummy_reg",
                        "mode": "W",
                        "n_bits": 1,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Dummy register for demo",
                    },
                ],
            }
        ]
        py_params_dict["build_dir"] = "dummy_folder"
        py_params_dict["issuer"] = {
            "name": "iob",
            "confs": [],
        }
        py_params_dict["dest_dir"] = "dummy_dest"

    # by default use same version as issuer
    # use py2hwsw version as fallback
    default_version = py_params_dict["py2hwsw_version"]
    if "issuer" in py_params_dict:
        default_version = py_params_dict["issuer"].get("version", default_version)

    params = {
        # Use the same name as issuer + the suffix "_csrs"
        "name": py_params_dict["issuer"]["name"] + "_csrs",
        # Destination directory
        "dest_dir": py_params_dict["dest_dir"],
        # Version of the CSRs module (by default use issuer version, py2hwsw as fallback)
        "version": default_version,
        # Type of interface for CSR bus
        "csr_if": "iob",
        # List of Control Status Registers (CSRs)
        "csrs": [],
        # Select if register addresses should be auto-generated
        "autoaddr": True,
        # Allow overlap between Read and Write register addresses
        "rw_overlap": False,
        # Build directory for csrs (usually auto-passed py py2hwsw).
        "build_dir": "",
        # CSR Configuration to use
        "doc_conf": False,
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    assert params["csrs"], print("Error: Register list empty.")

    # Ensure build directory is given when py2hwsw is setting up this core
    if py_params_dict.get("py2hwsw_target", "") == "setup":
        assert params["build_dir"], print("Error: Register build dir empty.")

    # Generate verilog parameters for CSR interface
    csr_if_params = {}
    if params["csr_if"] == "axi":
        csr_if_params = {"AXI_ID_W": 1, "AXI_LEN_W": 8}

    # Copy issuer confs but skip ADDR_W and CSR params
    confs = [
        {
            "name": "ADDR_W",
            "type": "D",
            "val": "ND",  # ret automatically
            "min": "0",
            "max": "32",
            "descr": "Address bus width",
        },
    ]
    for conf in py_params_dict["issuer"].get("confs", []):
        if conf["name"] == "ADDR_W" or conf["name"] in csr_if_params:
            continue
        confs.append(conf)

    # Append DATA_W parameter if not already present
    if "DATA_W" not in [
        conf["name"] for conf in py_params_dict["issuer"].get("confs", [])
    ]:
        confs.append(
            {
                "name": "DATA_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "Data bus width",
            }
        )

    # Append parameters for csr interface
    interface_params = {}
    for param_name, param_value in csr_if_params.items():
        confs.append(
            {
                "name": param_name,
                "type": "P",
                "val": param_value,
                "min": "NA",
                "max": "NA",
                "descr": f"{param_name} CSR interface parameter",
            }
        )
        # Remove csr_if suffix from parameter name (remove "AXI_" prefix)
        name_without_suffix = param_name[len(params["csr_if"]) + 1 :]
        interface_params[name_without_suffix] = param_name

    attributes_dict = {
        "name": params["name"],
        "generate_hw": True,
        "dest_dir": params["dest_dir"],
        "version": params["version"],
        "confs": confs,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "control_if_s",
                "signals": {
                    "type": params["csr_if"],
                    # ADDR_W set automatically
                    "DATA_W": "DATA_W",
                    **interface_params,
                },
                "descr": "CSR control interface. Interface type defined by `csr_if` parameter.",
            },
        ],
        "wires": [
            {
                "name": "internal_iob",
                "descr": "Internal iob interface",
                "signals": {
                    "type": "iob",
                    "prefix": "internal_",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "state",
                "descr": "",
                "signals": [
                    {"name": "state", "width": 1},
                ],
            },
            {
                "name": "state_nxt",
                "descr": "",
                "signals": [
                    {"name": "state_nxt", "width": 1, "isvar": True, "isreg": True},
                ],
            },
            {
                "name": "write_en",
                "descr": "",
                "signals": [
                    {"name": "write_en", "width": 1},
                ],
            },
            {
                "name": "internal_iob_addr",
                "descr": "",
                "signals": [
                    {"name": "internal_iob_addr"},
                ],
            },
            {
                "name": "internal_iob_addr_stable",
                "descr": "",
                "signals": [
                    {"name": "internal_iob_addr_stable", "width": "ADDR_W"},
                ],
            },
            {
                "name": "internal_iob_addr_reg",
                "descr": "",
                "signals": [
                    {"name": "internal_iob_addr_reg", "width": "ADDR_W"},
                ],
            },
            {
                "name": "internal_iob_addr_reg_en",
                "descr": "",
                "signals": [
                    {"name": "internal_iob_addr_reg_en", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_functions",
                "instantiate": False,
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_inst",
                "instantiate": False,
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_e_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_e",
                },
                "instantiate": False,
            },
            {
                "core_name": "iob_ctls",
                "instance_name": "iob_ctls_inst",
                "instantiate": False,
            },
            {
                "core_name": "iob_reg",
                "instance_name": "internal_addr_reg",
                "instance_description": "store iob addr",
                "parameters": {
                    "DATA_W": "ADDR_W",
                    "RST_VAL": "{ADDR_W{1'b0}}",
                },
                "port_params": {
                    "clk_en_rst_s": "c_a_e",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i:internal_iob_addr_reg_en",
                        ],
                    ),
                    "data_i": "internal_iob_addr",
                    "data_o": "internal_iob_addr_reg",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "state_reg",
                "instance_description": "state register",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": "1'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "state_nxt",
                    "data_o": "state",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    // Include iob_functions for use in parameters
    `include "iob_functions.vs"
    `define IOB_NBYTES (DATA_W/8)
    `define IOB_NBYTES_W $clog2(`IOB_NBYTES)
    `define IOB_WORD_ADDR(ADDR) ((ADDR>>`IOB_NBYTES_W)<<`IOB_NBYTES_W)\n
    localparam WSTRB_W = DATA_W/8;

    //FSM states
    localparam WAIT_REQ = 1'd0;
    localparam WAIT_RVALID = 1'd1;


    assign internal_iob_addr_reg_en = (state == WAIT_REQ);
    assign internal_iob_addr_stable = (state == WAIT_RVALID) ? internal_iob_addr_reg : internal_iob_addr;

    assign write_en = |internal_iob_wstrb;

    //write address
    wire [($clog2(WSTRB_W)+1)-1:0] byte_offset;
    iob_ctls #(.W(WSTRB_W), .MODE(0), .SYMBOL(0)) bo_inst (.data_i(internal_iob_wstrb), .count_o(byte_offset));
"""
            }
        ],
    }

    params["csrs"] = create_group_for_ungrouped_csrs(params["csrs"])

    #
    # Layer 1 CSRs: Adds support for special CSRs. All of these will be converted into Layer 0 CSRs with extra logic.
    #
    find_and_update_interrupt_csrs(params["csrs"])  # "INTERUPT"
    find_and_update_fifo_csrs(params["csrs"], attributes_dict)  # "FIFO", "AFIFO"
    find_and_update_rom_csrs(params["csrs"], attributes_dict)  # "ROM"
    # "REG" with log2n_items > 0
    find_and_update_regarray_csrs(params["csrs"], attributes_dict)
    find_and_update_regfile_csrs(params["csrs"], attributes_dict)  # "REGFILE"
    find_and_update_ram_csrs(params["csrs"], attributes_dict)  # "RAM"
    # "NOAUTO" with autoclear = True
    find_and_update_autoclear_csrs(params["csrs"], attributes_dict)

    #
    # Layer 0 CSRs: From this point, params["csrs"] only contains basic Layer 0 CSRs: "REG", "NOAUTO"
    #

    # Convert csrs dictionaries to objects
    csrs_obj_list = []
    for group in params["csrs"]:
        csrs_obj_list.append(create_csr_group(**group))

    attributes_with_csrs = attributes_dict | {
        "csrs": csrs_obj_list,
        "csr_if": params["csr_if"],
        "rw_overlap": params["rw_overlap"],
        "autoaddr": params["autoaddr"],
        "build_dir": params["build_dir"],
        "doc_conf": params["doc_conf"],
    }

    # Generate snippets
    csr_gen_obj, reg_table = generate_csr(
        attributes_with_csrs,
        create_files=py_params_dict.get("py2hwsw_target", "") == "setup",
    )

    # Store reg_table in static dict
    global static_reg_tables
    static_reg_tables[params["name"]] = reg_table

    # Generate tex section for each doc_configuration and reg table
    if py_params_dict.get("py2hwsw_target", "") == "setup":
        # use regs copy to not modify original regs
        regs_copy = copy.deepcopy(attributes_with_csrs["csrs"])
        # Get doc_configuration_list
        doc_configs = _list_all_doc_configs(attributes_with_csrs["csrs"])
        doc_tables = {}
        # Generate doc_table for each doc_configuration
        for doc_conf in doc_configs:
            _reset_autoaddrs(attributes_with_csrs["autoaddr"], regs_copy)
            _, doc_table = csr_gen_obj.get_reg_table(
                regs_copy,
                attributes_with_csrs["rw_overlap"],
                attributes_with_csrs["autoaddr"],
                attributes_with_csrs["doc_conf"],
            )

            doc_tables[doc_conf] = doc_table

        csr_gen_obj.generate_regs_tex(
            doc_tables,
            attributes_with_csrs["build_dir"] + "/document/tsrc",
        )

    # Add ports and internal wires for registers
    auto_ports, auto_wires, auto_snippet = csr_gen_obj.gen_ports_wires(reg_table)
    attributes_dict["ports"] += auto_ports
    attributes_dict["wires"] += auto_wires
    attributes_dict["snippets"].append({"verilog_code": auto_snippet})

    # TODO: Append csr_if to config_build.mk ?
    # file2create.write(f"CSR_IF={python_module.csr_if}\n\n")

    # Set correct address width in ADDR_W (false-)parameter
    attributes_dict["confs"][0]["val"] = csr_gen_obj.core_addr_w
    # Set correct address width in control_if port
    attributes_dict["ports"][1]["signals"]["ADDR_W"] = max(1, csr_gen_obj.core_addr_w)

    return attributes_dict


def create_group_for_ungrouped_csrs(csrs):
    general_group = {
        "name": "general_operation",
        "descr": "General Registers.",
        "regs": [],
    }
    grouped_csrs = []
    for csr in csrs:
        # Check if csr is already a group
        if "regs" in csr:
            grouped_csrs.append(csr)
            continue

        # Append csr to general group
        general_group["regs"].append(csr)

    # Append general group if it has any registers
    if general_group["regs"]:
        grouped_csrs.append(general_group)

    return grouped_csrs


def _list_all_doc_configs(csrs):
    """Return list of all doc configurations"""
    doc_configs = []
    for csr_group in csrs:
        for reg in csr_group.regs:
            if reg.doc_conf_list:
                doc_configs += reg.doc_conf_list
    if not doc_configs:
        # empty case: no regs with specific doc_conf
        doc_configs = [""]
    else:
        # Remove duplicates
        doc_configs = list(set(doc_configs))
    return list(set(doc_configs))


def _reset_autoaddrs(autoaddr, csrs):
    """Reset autoaddr for regs"""
    if autoaddr and csrs:
        for csr_group in csrs:
            for r in csr_group.regs:
                r.addr = -1
