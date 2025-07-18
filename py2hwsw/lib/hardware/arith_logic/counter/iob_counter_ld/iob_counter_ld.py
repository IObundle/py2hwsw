# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "RST_VAL",
                "type": "P",
                "val": "{DATA_W{1'b0}}",
                "min": "0",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "en_rst_i",
                "descr": "Enable and Synchronous reset interface",
                "wires": [
                    {
                        "name": "en_i",
                        "width": 1,
                        "descr": "Enable input",
                    },
                    {
                        "name": "rst_i",
                        "width": 1,
                        "descr": "Synchronous reset input",
                    },
                ],
            },
            {
                "name": "ld_i",
                "descr": "Input port",
                "wires": [
                    {"name": "ld_i", "width": 1},
                ],
            },
            {
                "name": "ld_val_i",
                "descr": "Input port",
                "wires": [
                    {"name": "ld_val_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "wires": [
                    {"name": "data_o", "width": "DATA_W"},
                ],
            },
        ],
        "buses": [
            {
                "name": "data_int",
                "descr": "data bus",
                "wires": [
                    {"name": "data_int", "width": "DATA_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "reg0",
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "RST_VAL",
                },
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i:en_i",
                            "rst_i:rst_i",
                        ],
                    ),
                    "data_i": "data_int",
                    "data_o": "data_o",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        assign data_int = ld_i ? ld_val_i : data_o + 1'b1;
            """,
            },
        ],
    }

    return attributes_dict
