# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "io_io",
                "descr": "",
                "wires": [
                    {"name": "clkin_i", "width": "1"},
                    {"name": "clkout_o", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    clk_buf_altclkctrl_0 clk_buf (
        .inclk (clkin_i),
        .outclk(clkout_o)
    );
""",
            },
        ],
    }

    return attributes_dict
