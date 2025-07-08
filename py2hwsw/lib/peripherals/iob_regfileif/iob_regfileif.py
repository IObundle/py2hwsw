# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import copy
import json


def setup(py_params_dict):
    params = {
        "internal_csr_if": "iob",
        "external_csr_if": "iob",
        # FIXME: Make ADDR_W automatic
        "internal_csr_if_widths": {"ADDR_W": 32, "DATA_W": 32},
        "external_csr_if_widths": {"ADDR_W": 32, "DATA_W": 32},
        "csrs": [],
        "autoaddr": True,
        "version": py_params_dict["py2hwsw_version"],
        "test": False,  # Enable this to use random registers
        "addr_w": 32,
        "data_w": 32,
        # Version of the CSRs module (by default use same version as py2hwsw)
        "version": py_params_dict["py2hwsw_version"],
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
                        "mode": "R",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Test register 1",
                    },
                    {
                        "name": "reg2",
                        "mode": "W",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Test register 1",
                    },
                    {
                        "name": "reg3",
                        "mode": "RW",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Test register 3",
                    },
                ],
            }
        ]

    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        params["csrs"] = [
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

    assert params["csrs"], "Error: Register list empty."

    ports = []
    reg_wires = []
    external_reg_connections = {}
    internal_reg_connections = {}
    snippets = ""

    for csr_group in params["csrs"]:
        for csr in csr_group["regs"]:
            if csr.get("type", "REG") == "REG":
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
                if csr["mode"] == "RW":
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
                if csr["mode"] == "W":
                    external_reg_connections[csr["name"] + "_o"] = csr["name"]
                    internal_reg_connections[csr["name"] + "_i"] = csr["name"]
                if csr["mode"] == "R":
                    external_reg_connections[csr["name"] + "_i"] = csr["name"]
                    internal_reg_connections[csr["name"] + "_o"] = csr["name"]
                elif csr["mode"] == "RW":
                    external_reg_connections[csr["name"] + "_io"] = csr["name"]
                    internal_reg_connections[csr["name"] + "_io"] = csr["name"] + "_inv"
            elif csr.get("type", "") == "NOAUTO":
                reg_wires += create_manual_reg_wires(csr)

                # Connect register interfaces
                external_reg_connections[csr["name"] + "_io"] = (
                    "external_" + csr["name"]
                )
                internal_reg_connections[csr["name"] + "_io"] = (
                    "internal_" + csr["name"]
                )

            if "output" in csr:
                if csr["output"]:
                    # Create ports for output
                    ports.append(
                        {
                            "name": csr["name"] + "_o",
                            "descr": "",
                            "signals": [
                                {"name": csr["name"] + "_o", "width": csr["n_bits"]},
                            ],
                        },
                    )

                    if csr["mode"] == "RW":
                        ports[-1]["signals"].append(
                            {"name": csr["name"] + "_2_o", "width": csr["n_bits"]},
                        )

                    # Assign wires to ports
                    if csr.get("type", "REG") == "REG":
                        snippets += f"assign {csr['name'] + '_o'} = {csr['name']};"
                        if csr["mode"] == "RW":
                            snippets += (
                                f"assign {csr['name'] + '_2_o'} = {csr['name'] + '_2'};"
                            )
                    elif csr.get("type", "") == "NOAUTO":
                        if csr["mode"] == "W":
                            snippets += f"assign {csr['name'] + '_o'} = {'internal_' + csr['name']+ '_wdata_o'};"
                        elif csr["mode"] == "R":
                            snippets += f"assign {csr['name'] + '_o'} = {'external_' + csr['name'] + '_wdata_o'};"
                        elif csr["mode"] == "RW":
                            snippets += f"""assign {csr['name'] + '_o'} = {'internal_' + csr['name']+ '_wdata_o'};
                            assign {csr['name'] + '_2_o'} = {'external_' + csr['name'] + '_wdata_o'};"""
                csr.pop("output")

    # Invert CSRS direction for internal CPU
    csrs_inverted = copy.deepcopy(params["csrs"])
    for csr_group in csrs_inverted:
        for csr in csr_group["regs"]:
            if csr["mode"] == "W":
                csr["mode"] = "R"
            elif csr["mode"] == "R":
                csr["mode"] = "W"
            # Do nothing for mode "RW"

    if "verilog-snippets" in py_params_dict:
        snippets = snippets + py_params_dict["verilog-snippets"]

    attributes_dict = {
        "name": "iob_regfileif",
        "generate_hw": True,
        "version": params["version"],
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
        "ports": ports
        + [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
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
                "instance_name": "iob_csrs_external",
                "instance_description": "Control/Status Registers for external CPU",
                "csrs": params["csrs"],
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # iob_csrs 'control_if_s' port is connected automatically by py2hwsw
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
                "instance_name": "iob_csrs",
                "instance_description": "Control/Status Registers for internal CPU (inverted registers)",
                "csrs": csrs_inverted,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # iob_csrs 'control_if_s' port is connected automatically by py2hwsw
                    **internal_reg_connections,
                },
                "csr_if": params["internal_csr_if"],
                # TODO: Support internal_csr_if_widths
                "version": py_params_dict["py2hwsw_version"],
                "autoaddr": params["autoaddr"],
            },
        ],
        "snippets": [
            {"verilog_code": snippets},
        ],
    }

    # print(json.dumps(attributes_dict, indent=4))  # DEBUG

    return attributes_dict


def create_manual_reg_wires(csr):
    """Creates wires for registers with NOAUTO"""
    internal_signals = []
    external_signals = []

    if csr["mode"] == "W":
        internal_signals = get_manual_signals(
            "internal_" + csr["name"], "W", csr["n_bits"]
        )
        external_signals = get_manual_signals(
            "external_" + csr["name"], "R", csr["n_bits"]
        )

    elif csr["mode"] == "R":
        internal_signals = get_manual_signals(
            "internal_" + csr["name"], "W", csr["n_bits"]
        )
        external_signals = get_manual_signals(
            "external_" + csr["name"], "R", csr["n_bits"]
        )

    elif csr["mode"] == "RW":
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


def get_manual_signals(name, mode, data_width):
    signals = []

    if "R" in mode:
        signals += [
            {"name": name + "_rdata_i", "width": data_width},
            {"name": name + "_rvalid_i", "width": 1},
            {"name": name + "_ren_o", "width": 1},
            {"name": name + "_ready_i", "width": 1},
        ]
    elif "W" in mode:
        signals += [
            {"name": name + "_wdata_o", "width": data_width},
            {"name": name + "_wen_o", "width": 1},
            {"name": name + "_wready_i", "width": 1},
        ]

    return signals
