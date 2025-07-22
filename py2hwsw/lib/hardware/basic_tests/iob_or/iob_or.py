#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
import sys

path_sufix = "../../../../scripts"
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), path_sufix)
    ),
)

from iob_core import iob_core

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
            "kind": "P",
            "value": "21",
            "min_value": "1",
            "max_value": "32",
            "descr": "IO width",
        },
    ],
    "ports": [
        {
            "name": "a_i",
            "descr": "Input port a",
            "width": "W",
        },
        {
            "name": "b_i",
            "descr": "Input port b",
            "width": "W",
        },
        {
            "name": "y_o",
            "descr": "Output port y",
            "width": "W",
        },
    ],
    "snippets": [{"verilog_code": "   assign y_o = a_i | b_i;"}],
}


class iob_or(iob_core):
    def __init__(self, width=None):
        if width:
            core_dictionary["confs"][0]["value"] = str(width)
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_or_obj = iob_or(width=3)
    iob_or_obj.generate_build_dir()
