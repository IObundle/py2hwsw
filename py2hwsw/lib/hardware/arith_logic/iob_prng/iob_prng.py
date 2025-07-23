# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
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
                    {"name": "ld_val_i", "width": "32"},
                ],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "wires": [
                    {"name": "data_o", "width": "32"},
                ],
            },
        ],
        "buses": [
            {
                "name": "data_int",
                "descr": "data bus",
                "wires": [
                    {"name": "data_int", "width": "32"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "reg0",
                "parameters": {
                    "DATA_W": "32",
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
                assign data_int = ld_i ? (ld_val_i != 0? ld_val_i: 32'd1) : count_nxt;
                wire feedback = count_o[31] ^ count_o[21] ^ count_o[1] ^ count_out[0];
                assign count_nxt = {data_o[30:0], feedback};
                """,
            },
        ],
    }

    return attributes_dict
