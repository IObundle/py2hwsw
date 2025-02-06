# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
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
                    "type": "clk_en_rst",
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
                "name": "incr_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "incr_i",
                        "width": "DATA_W",
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
                    {"name": "data_int", "width": "DATA_W"},
                ],
            },
        ],
        "subblocks": [
            """
            iob_reg_re reg0 -p DATA_W:DATA_W RST_VAL:RST_VAL -c
            clk_en_rst_s:clk_en_rst_s
            en_rst_i:en_rst_i
            data_i:data_int
            data_o:data_o
            -d 'Accomulator register with synchronous reset and enable'
            """
        ],
        "snippets": [
            {
                "verilog_code": """
       assign data_nxt = data_o + incr_i;
       assign data_int = data_nxt[DATA_W-1:0];
            """,
            },
        ],
    }

    return attributes_dict
