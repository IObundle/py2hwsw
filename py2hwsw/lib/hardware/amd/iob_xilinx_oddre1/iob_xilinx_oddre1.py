# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": True,
        "ports": [
            {
                "name": "io_io",
                "descr": "ODDRE1 io",
                "signals": [
                    {"name": "q_o", "width": "1"},
                    {"name": "c_i", "width": "1"},
                    {"name": "d1_i", "width": "1"},
                    {"name": "d2_i", "width": "1"},
                    {"name": "sr_i", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    ODDRE1 ODDRE1_inst (
      .Q (q_o),
      .C (c_i),
      .D1(d1_i),
      .D2(d2_i),
      .SR(sr_i)
    );
""",
            },
        ],
    }

    return attributes_dict
