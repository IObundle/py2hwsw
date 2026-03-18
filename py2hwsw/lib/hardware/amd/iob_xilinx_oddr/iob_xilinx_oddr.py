# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "io_io",
                "descr": "ODDR io",
                "signals": [
                    {"name": "clk_i", "width": "1"},
                    {"name": "d1_i", "width": "1"},
                    {"name": "d2_i", "width": "1"},
                    {"name": "q_o", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    ODDR #(
        .DDR_CLK_EDGE("SAME_EDGE"),
        .INIT(1'b0),
        .SRTYPE("SYNC")
    ) oddr_inst (
        .Q(q_o),
        .C(clk_i),
        .CE(1'b1),
        .D1(d1_i),
        .D2(d2_i),
        .R(1'b0),
        .S(1'b0)
    );
""",
            },
        ],
    }

    return attributes_dict
