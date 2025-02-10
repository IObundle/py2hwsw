# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": True,
        "confs": [
            {
                "name": "POLARITY",
                "type": "P",
                "val": "1",
                "min": "0",
                "max": "1",
                "descr": "Reset polarity",
            },
            {
                "name": "T_BEFORE",
                "type": "P",
                "val": "10",
                "min": "0",
                "max": "",
                "descr": "Time in ms before reset is active",
            },
            {
                "name": "T_ACTIVE",
                "type": "P",
                "val": "10",
                "min": "0",
                "max": "1",
                "descr": "Time in ms reset is active",
            },
        ],
        "ports": [
            {
                "name": "arst_o",
                "descr": "Async reset output",
                "signals": [
                    {"name": "arst_o", "width": "1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   reg arst;
   assign arst_o = arst;
   initial arst = ~POLARITY; #(T_BEFORE) arst = POLARITY; #(T_ACTIVE) arst = ~POLARITY;
        """,
            }
        ],
    }

    return attributes_dict
