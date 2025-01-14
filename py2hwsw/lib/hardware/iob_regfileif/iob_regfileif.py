# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import copy
import json


def setup(py_params_dict):
    params = {
        "version": "0.7",
        "internal_csr_if": "iob",
        "external_csr_if": "iob",
        # FIXME: Make ADDR_W automatic
        "internal_csr_if_widths": {"ADDR_W": 32, "DATA_W": 32},
        "external_csr_if_widths": {"ADDR_W": 32, "DATA_W": 32},
        "csrs": [],
        "autoaddr": True,
        "test": False,  # Enable this to use random registers
        "addr_w": 32,
        "data_w": 32,
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    # If we are in "test" mode, generate this core with random registers
    if params["test"]:
        params["csrs"] = [
            {
                "name": "reg_group",
                "descr": "Test register group",
                "regs": [
                    {
                        "name": "reg1",
                        "type": "R",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "Test register 1",
                    },
                    {
                        "name": "reg2",
                        "type": "W",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "Test register 1",
                    },
                    {
                        "name": "reg3",
                        "type": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "Test register 3",
                    },
                ],
            }
        ]

    assert params["csrs"], "Error: Register list empty."

    reg_wires = []
    external_reg_connections = {}
    internal_reg_connections = {}

    # Invert CSRS direction for internal CPU
    csrs_inverted = copy.deepcopy(params["csrs"])
    for csr_group in csrs_inverted:
        for csr in csr_group["regs"]:
            if csr["type"] == "W":
                csr["type"] = "R"
            elif csr["type"] == "R":
                csr["type"] = "W"
            # Do nothing for type "RW"

            if csr["autoreg"]:
                # Create wire for reg
                reg_wires.append(
                    {
                        "name": csr["name"],
                        "descr": "",
                        "signals": [
                            {"name": csr["name"], "width": csr["n_bits"]},
                        ],
                    },
                )
                if csr["type"] == "RW":
                    reg_wires[-1]["signals"].append(
                        {"name": csr["name"] + "_2", "width": csr["n_bits"]},
                    )
                    reg_wires.append(
                        {
                            "name": csr["name"] + "_inv",
                            "descr": "",
                            "signals": [
                                {"name": csr["name"] + "_2"},
                                {"name": csr["name"]},
                            ],
                        },
                    )

                # Connect register interfaces
                if csr["type"] == "R":
                    external_reg_connections[csr["name"] + "_o"] = csr["name"]
                    internal_reg_connections[csr["name"] + "_i"] = csr["name"]
                if csr["type"] == "W":
                    external_reg_connections[csr["name"] + "_i"] = csr["name"]
                    internal_reg_connections[csr["name"] + "_o"] = csr["name"]
                elif csr["type"] == "RW":
                    external_reg_connections[csr["name"] + "_io"] = csr["name"]
                    internal_reg_connections[csr["name"] + "_io"] = csr["name"] + "_inv"
            else:  # Autoreg false
                reg_wires += create_manual_reg_wires(csr)

                # Connect register interfaces
                external_reg_connections[csr["name"] + "_io"] = (
                    "external_" + csr["name"]
                )
                internal_reg_connections[csr["name"] + "_io"] = (
                    "internal_" + csr["name"]
                )

    attributes_dict = {
        "name": "iob_regfileif",
        "version": "0.1",
    }
    attributes_dict |= {
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": params["data_w"],
                "min": "NA",
                "max": "32",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": params["addr_w"],
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "cbus_s",
                "signals": {
                    "type": params["internal_csr_if"],
                    **params["internal_csr_if_widths"],
                },
                "descr": "Internal CPU native interface. Registers have their direction inverted from this CPU's perspective.",
            },
            {
                "name": "external_control_if_s",
                "signals": {
                    "type": params["external_csr_if"],
                    "prefix": "external_",
                    **params["external_csr_if_widths"],
                },
                "descr": "External CPU native interface.",
            },
        ],
        "wires": reg_wires
        + [
            {
                "name": "internal_iob2",
                "descr": "Internal iob interface",
                "signals": {
                    "type": "iob",
                    "prefix": "internal2_",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "csrs_external",
                "instance_description": "Control/Status Registers for external CPU",
                "csrs": params["csrs"],
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "control_if_s": "external_control_if_s",
                    **external_reg_connections,
                },
                "csr_if": params["external_csr_if"],
                # TODO: Support external_csr_if_widths
                "version": params["version"],
                "autoaddr": params["autoaddr"],
            },
            {
                "core_name": "iob_csrs",
                "name": attributes_dict["name"] + "_inverted_csrs",
                "instance_name": "csrs_internal_inverted",
                "instance_description": "Control/Status Registers for internal CPU (inverted registers)",
                "csrs": csrs_inverted,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "control_if_s": "cbus_s",
                    **internal_reg_connections,
                },
                "csr_if": params["internal_csr_if"],
                # TODO: Support internal_csr_if_widths
                "version": attributes_dict["version"],
                "autoaddr": params["autoaddr"],
            },
        ],
    }
    if "verilog-snippets" in py_params_dict:
        attributes_dict["snippets"] = [
            {"verilog_code": py_params_dict["verilog-snippets"]},
        ]

    # print(json.dumps(attributes_dict, indent=4))  # DEBUG

    return attributes_dict


def create_manual_reg_wires(csr):
    """Creates wires for registers with autoreg=false"""
    internal_signals = []
    external_signals = []

    if csr["type"] == "R":
        internal_signals = get_manual_signals(
            "internal_" + csr["name"], "W", csr["n_bits"]
        )
        external_signals = get_manual_signals(
            "external_" + csr["name"], "R", csr["n_bits"]
        )

    elif csr["type"] == "W":
        internal_signals = get_manual_signals(
            "internal_" + csr["name"], "W", csr["n_bits"]
        )
        external_signals = get_manual_signals(
            "external_" + csr["name"], "R", csr["n_bits"]
        )

    elif csr["type"] == "RW":
        internal_signals = get_manual_signals(
            "internal_" + csr["name"], "RW", csr["n_bits"]
        )
        external_signals = get_manual_signals(
            "external_" + csr["name"], "RW", csr["n_bits"]
        )

    reg_wires = []

    reg_wires.append(
        {"name": "internal_" + csr["name"], "descr": "", "signals": internal_signals}
    )

    reg_wires.append(
        {"name": "external_" + csr["name"], "descr": "", "signals": external_signals}
    )

    return reg_wires


def get_manual_signals(name, type, data_width):
    signals = []

    if "R" in type:
        signals += [
            {"name": name + "_rdata_i", "width": data_width},
            {"name": name + "_rvalid_i", "width": 1},
            {"name": name + "_ren_o", "width": 1},
            {"name": name + "_rready_i", "width": 1},
        ]
    elif "W" in type:
        signals += [
            {"name": name + "_wdata_o", "width": data_width},
            {"name": name + "_wen_o", "width": 1},
            {"name": name + "_wready_i", "width": 1},
        ]

    return signals
