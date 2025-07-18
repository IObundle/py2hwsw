# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "CLK_PERIOD",
                "type": "P",
                "val": "10",
                "min": "",
                "max": "",
                "descr": "Clock period",
            },
        ],
        "ports": [
            {
                "name": "clk_o",
                "descr": "Output clock",
                "wires": [
                    {"name": "clk_o", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   reg clk;
   assign clk_o = clk;
   initial clk = 0; always #(CLK_PERIOD/2) clk = ~clk;
        """,
            }
        ],
    }

    return attributes_dict
