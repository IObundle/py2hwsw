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
                "val": "DATA_W",
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
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "clock, clock enable and reset",
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
                "name": "incr_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "incr_i",
                        "width": "INCR_W",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "data_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "data_nxt",
                "descr": "Sum result",
                "wires": [
                    {
                        "name": "data_nxt",
                        "width": "DATA_W+1",
                    },
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
            # FIXME: iob_reg_re no longer exists, but short notation does not seem to support python parameters (like "port_params")
            # """
            # iob_reg_re reg0 -p DATA_W:DATA_W RST_VAL:RST_VAL -c
            # clk_en_rst_s:clk_en_rst_s
            # en_rst_i:en_rst_i
            # data_i:data_int
            # data_o:data_o
            # -d 'Accomulator register with synchronous reset and enable'
            # """,
            # So, as an alternative, we dont use short notation and use the following:
            {
                "core_name": "iob_reg",
                "instance_name": "reg0",
                "instance_descr": "Accomulator register with synchronous reset and enable",
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
       assign data_nxt = data_o + incr_i;
       assign data_int = data_nxt[DATA_W-1:0];
            """,
            },
        ],
    }

    return attributes_dict
