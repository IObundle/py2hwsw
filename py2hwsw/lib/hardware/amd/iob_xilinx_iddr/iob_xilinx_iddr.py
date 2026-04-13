# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "io_io",
                "descr": "IDDR io",
                "signals": [
                    {"name": "clk_i", "width": "1"},
                    {"name": "d_i", "width": "1"},
                    {"name": "q1_o", "width": "1"},
                    {"name": "q2_o", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    IDDR #(
        .DDR_CLK_EDGE("SAME_EDGE_PIPELINED"),
        .INIT_Q1(1'b0),
        .INIT_Q2(1'b0),
        .SRTYPE("SYNC")
    ) iddr_inst (
        .Q1(q1_o),
        .Q2(q2_o),
        .C(clk_i),
        .CE(1'b1),
        .D(d_i),
        .R(1'b0),
        .S(1'b0)
    );
""",
            },
        ],
    }

    return attributes_dict
