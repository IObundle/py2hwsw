# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    params = {
        # Type of interface for CSR bus
        "csr_if": "iob",
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    attributes_dict = {
        "name": "iob_uut",
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "P",
                "val": "32",
            },
        ],
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "iob_clk",
            },
        },
        {
            "name": "macc_s",
            "descr": "Testbench macc csrs interface",
            "signals": {
                "type": "iob",
                "ADDR_W": 4,
            },
        },
    ]
    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "macc_cbus",
            "descr": "Testbench macc csrs bus",
            "signals": {
                "type": params["csr_if"],
                "prefix": "internal_",
                "ADDR_W": 4,
            },
        },
    ]
    #
    # Blocks
    #
    converter_connect = {
        "s_s": "macc_s",
        "m_m": "macc_cbus",
    }
    if params["csr_if"] != "iob":
        converter_connect["clk_en_rst_s"] = "clk_en_rst_s"
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_macc",
            "instance_name": "macc_inst",
            "instance_description": f"Unit Under Test (UUT) MACC instance with '{params['csr_if']}' interface.",
            "csr_if": params["csr_if"],
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_csrs_cbus_s": "macc_cbus",
            },
        },
        {
            "core_name": "iob_universal_converter",
            "instance_name": "iob_universal_converter",
            "instance_description": "Convert IOb port from testbench into correct interface for MACC CSRs bus",
            "subordinate_if": "iob",
            "manager_if": params["csr_if"],
            "parameters": {
                "ADDR_W": 4,
                "DATA_W": "DATA_W",
            },
            "connect": converter_connect,
        },
    ]

    return attributes_dict
