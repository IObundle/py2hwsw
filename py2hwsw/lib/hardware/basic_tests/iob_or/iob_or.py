#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


import py2hwsw_api as py2hwsw

# Short notation with API is WIP
# core_dictionary = {
#     "generate_hw": True,
#     "confs": [
#         {
#             "name": "W",
#             "type": "P",
#             "val": "21",
#             "min": "1",
#             "max": "32",
#             "descr": "IO width",
#         },
#     ],
#     "ports": [
#         """
#             a_i -s a_i:W
#             -d 'Input port'
#
#             b_i -s b_i:W
#             -d 'Input port'
#
#             y_o -s y_o:W
#             -d 'Output port'
#             """,
#     ],
#     "snippets": [{"verilog_code": "   assign y_o = a_i | b_i;"}],
# }

core_dictionary = {
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
            "name": "a_i",
            "descr": "Input port a",
            "signals": [
                {"name": "a_i", "width": "W"},
            ],
        },
        {
            "name": "b_i",
            "descr": "Input port b",
            "signals": [
                {"name": "b_i", "width": "W"},
            ],
        },
        {
            "name": "y_o",
            "descr": "Output port y",
            "signals": [
                {"name": "y_o", "width": "W"},
            ],
        },
    ],
    "snippets": [{"verilog_code": "   assign y_o = a_i | b_i;"}],
}


class iob_or(py2hwsw.iob_core):
    def __init__(self):
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_or_obj = iob_or()
    iob_or_obj.generate_build_dir()
