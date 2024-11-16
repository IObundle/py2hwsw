# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
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
            """
            a_i -s a_i:W
            -d 'Input port'

            b_i -s b_i:W
            -d 'Input port'

            y_o -s y_o:W
            -d 'Output port'
            """,
        ],
        "snippets": [{"verilog_code": "   assign y_o = a_i | b_i;"}],
    }

    return attributes_dict
