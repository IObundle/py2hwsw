# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "io_io",
                "descr": "IBUFG io",
                "wires": [
                    {"name": "i_i", "width": "1"},
                    {"name": "o_o", "width": "1"},
                ],
            },
        ],
        "buses": [
            {
                "name": "clk_buf",
                "descr": "",
                "wires": [
                    {"name": "clk_buf", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    IBUF ibuf_inst (
      .I(i_i),
      .O(clk_buf)
    );

    BUFG bufg_inst (
    .I(clk_buf),
    .O(o_o)
    );

""",
            },
        ],
    }

    return attributes_dict
