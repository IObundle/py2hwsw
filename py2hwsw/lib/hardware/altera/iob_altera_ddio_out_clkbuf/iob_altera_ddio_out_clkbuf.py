# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "ports": [
            {
                "name": "io_io",
                "descr": "",
                "signals": [
                    {"name": "aclr_i", "width": "1"},
                    {"name": "data_h_i", "width": "1"},
                    {"name": "data_l_i", "width": "1"},
                    {"name": "clk_i", "width": "1"},
                    {"name": "data_o", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    ddio_out_clkbuf ddio_out_clkbuf_inst (
        .aclr    (aclr_i),
        .datain_h(data_h_i),
        .datain_l(data_l_i),
        .outclock(clk_i),
        .dataout (data_o)
    );
""",
            },
        ],
    }

    return attributes_dict
