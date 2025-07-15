# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "in_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "in_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "en_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "en_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "out_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "out_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "in_out_io",
                "descr": "In/Output port",
                "wires": [
                    {
                        "name": "in_out_io",
                        "width": 1,
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            assign in_out_io = en_i ? in_i : 1'bz;
            assign out_o     = in_out_io;
         """,
            },
        ],
    }

    return attributes_dict
