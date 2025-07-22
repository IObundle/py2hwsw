#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# FIXME: API no longer exists
# import py2hwsw_api as py2hwsw
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
        {"name": "a_i", "width": "W"},
        {"name": "b_i", "width": "W"},
        {"name": "y_o", "width": "W"},
    ],
    "snippets": [{"verilog_code": "   assign y_o = a_i & b_i;"}],
}


class iob_and(iob_core):
    def __init__(self, width=None):
        if width:
            core_dictionary["confs"][0]["value"] = str(width)
        print("[DEBUG]: iob_and constructor called.")
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_and_obj = iob_and(width=8)
    iob_and_obj.generate_build_dir()
