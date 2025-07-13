#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import py2hwsw_api as py2hwsw

core_dictionary = {
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
            "signals": {
                "type": "iob_clk",
            },
            "descr": "Clock, clock enable and reset",
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
            "name": "data_o",
            "descr": "Output port",
            "signals": [
                {"name": "data_o", "width": "DATA_W"},
            ],
        },
    ],
    "wires": [
        {
            "name": "data_int",
            "descr": "data_int wire",
            "signals": [
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
        assign data_int =  data_o + 1'b1;
            """,
        },
    ],
}


class iob_counter(py2hwsw.iob_core):
    def __init__(self):
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_counter_obj = iob_counter()
    iob_counter_obj.generate_build_dir()
