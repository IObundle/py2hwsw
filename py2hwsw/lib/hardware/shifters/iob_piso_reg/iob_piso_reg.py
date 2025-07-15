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
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
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
                "name": "ld_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "ld_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "p_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "p_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "s_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "s_o",
                        "width": 1,
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "data_reg_int",
                "descr": "data_reg_int bus",
                "wires": [
                    {"name": "data_reg_int", "width": "DATA_W"},
                ],
            },
            {
                "name": "data_int",
                "descr": "data_int bus",
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
                    "RST_VAL": 0,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "data_int",
                    "data_o": "data_reg_int",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        assign data_int = ld_i ? p_i : data_reg_int << 1'b1;
        assign  s_o = data_reg_int[DATA_W-1];

            """,
            },
        ],
    }

    return attributes_dict
