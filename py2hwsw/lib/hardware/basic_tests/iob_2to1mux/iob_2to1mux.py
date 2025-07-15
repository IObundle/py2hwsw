# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "W",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
                "descr": "IO width",
            },
        ],
        "ports": [
            {
                "name": "data_i",
                "descr": "Input port",
                "wires": [
                    {"name": "a_i", "width": "W"},
                    {"name": "b_i", "width": "W"},
                    {"name": "sel_i", "width": "1"},
                ],
            },
            {
                "name": "y_o",
                "descr": "Output port",
                "wires": [
                    {"name": "y_o", "width": "W"},
                ],
            },
        ],
        "comb": {
            "code": """if (sel_i)
                    y_o = b_i;
                else
                    y_o = a_i;
                """,
        },
    }

    return attributes_dict
