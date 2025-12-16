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
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "INCR_W",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Increment value width",
            },
            {
                "name": "RST_VAL",
                "type": "P",
                "val": "{DATA_W{1'b0}}",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "clock, clock enable and reset",
            },
            {
                "name": "en_rst_i",
                "descr": "Enable and Synchronous reset interface",
                "signals": [
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
                "signals": [
                    {
                        "name": "ld_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "ld_val_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "ld_val_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "incr_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "incr_i",
                        "width": "INCR_W",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "data_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "data_nxt",
                "descr": "Sum result",
                "signals": [
                    {
                        "name": "data_nxt",
                        "width": "DATA_W+1",
                    },
                ],
            },
            {
                "name": "data_int",
                "descr": "data_int wire",
                "signals": [
                    {"name": "data_int", "width": "DATA_W+1"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "reg0",
                "parameters": {
                    "DATA_W": "DATA_W+1",
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
                    "data_i": "data_nxt",
                    "data_o": "data_int",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            assign data_nxt = ld_i ? ld_val_i : data_o + incr_i;
            assign data_o = data_int[DATA_W-1:0];
            """,
            },
        ],
    }

    return attributes_dict
