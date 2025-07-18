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
