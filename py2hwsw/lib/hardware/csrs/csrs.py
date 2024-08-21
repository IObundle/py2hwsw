import sys
import os

# Add csrs scripts folder to python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

import reg_gen
from iob_csr import create_csr_group


def setup(py_params_dict):
    params = {
        "name": py_params_dict["instantiator"]["name"] + "_csrs",
        "version": "1.0",
        "csr_if": "iob",
        "csrs": [],
        "autoaddr": True,
        # Overlap Read and Write register addresses
        "rw_overlap": False,
        "build_dir": "",
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    assert params["csrs"], print("Error: Register list empty.")

    assert params["build_dir"], print("Error: Register build dir empty.")

    attributes_dict = {
        "original_name": "csrs",
        "name": params["name"],
        "version": params["version"],
        "generate_hw": False,
        "confs": [
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "ND",
                "min": "0",
                "max": "32",
                "descr": "Address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "0",
                "max": "32",
                "descr": "Data bus width.",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst",
                "interface": {
                    "type": "clk_en_rst",
                    "subtype": "slave",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "control_if",
                "interface": {
                    "type": params["csr_if"],
                    "subtype": "slave",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "CSR control interface. Interface type defined by `csr_if` parameter.",
            },
        ],
        "blocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_inst",
            },
            {
                "core_name": "iob_reg_e",
                "instance_name": "iob_reg_e_inst",
            },
        ],
    }

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
    }

    # Generate snippets
    csr_gen_obj, reg_table = reg_gen.generate_csr(attributes_with_csrs)

    # Generate docs
    csr_gen_obj.generate_regs_tex(
        attributes_with_csrs["csrs"],
        reg_table,
        attributes_with_csrs["build_dir"] + "/document/tsrc",
    )

    # Auto-add VERSION macro
    found_version_macro = False
    if attributes_with_csrs["confs"]:
        for macro in attributes_with_csrs["confs"]:
            if macro["name"] == "VERSION":
                found_version_macro = True
    if not found_version_macro:
        attributes_with_csrs["confs"].append(
            {
                "name": "VERSION",
                "type": "M",
                "val": "16'h"
                + reg_gen.version_str_to_digits(attributes_with_csrs["version"]),
                "min": "NA",
                "max": "NA",
                "descr": "Product version. This 16-bit macro uses nibbles to represent decimal numbers using their binary values. The two most significant nibbles represent the integral part of the version, and the two least significant nibbles represent the decimal part. For example V12.34 is represented by 0x1234.",
            }
        )

    # Add ports for registers
    attributes_dict["ports"] += csr_gen_obj.gen_ports(reg_table)

    # TODO: Append csr_if to config_build.mk ?
    # file2create.write(f"CSR_IF={python_module.csr_if}\n\n")

    # Set correct address width macro
    attributes_dict["confs"][0]["val"] = csr_gen_obj.core_addr_w

    return attributes_dict
