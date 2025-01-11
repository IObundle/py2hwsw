# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": True,
        "confs": [
            {
                "name": "OUTPUT_PER",
                "type": "P",
                "val": "0",
                "min": "1",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "INPUT_PER",
                "type": "P",
                "val": "0",
                "min": "1",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_rst_i",
                "descr": "clock and reset inputs",
                "signals": [
                    {"name": "clk_p_i", "width": "1"},
                    {"name": "clk_n_i", "width": "1"},
                    {"name": "arst_i", "width": "1"},
                ],
            },
            {
                "name": "clk_rst_o",
                "descr": "clock and reset outputs",
                "signals": [
                    {"name": "clk_out1_o", "width": "1"},
                    {"name": "rst_out1_o", "width": "1"},
                ],
            },
        ],
        "wires": [
            {
                "name": "reset_sync_clk_rst",
                "descr": "Reset synchronizer inputs",
                "signals": [
                    {"name": "clk_out1_o"},
                    {"name": "arst_out", "width": "1"},
                ],
            },
            {
                "name": "reset_sync_rst_out",
                "descr": "Reset synchronizer output",
                "signals": [
                    {"name": "rst_out1_o"},
                ],
            },
        ],
    }
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_reset_sync",
            "instance_name": "rst_sync",
            "connect": {
                "clk_rst_s": "reset_sync_clk_rst",
                "arst_o": "reset_sync_rst_out",
            },
        },
    ]
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
    iob_clock_wizard #(
        .OUTPUT_PER(OUTPUT_PER),
        .INPUT_PER (INPUT_PER)
    ) clock_wizard_inst (
        .clk_in1_p(clk_p_i),
        .clk_in1_n(clk_n_i),
        .arst_i(arst_i),
        .clk_out1 (clk_out1_o),
        .arst_out1(arst_out)
    );
""",
        },
    ]

    return attributes_dict
