#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

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
        {
            "name": "a_i",
            "descr": "Input port",
            "width": "W",
        },
        {
            "name": "y_o",
            "descr": "Output port",
            "width": "W",
        },
    ],
    "snippets": [{"verilog_code": "   assign y_o = ~a_i;"}],
}


class iob_inv(iob_core):
    def __init__(self, width=None):
        if width:
            core_dictionary["confs"][0]["value"] = str(width)
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_inv_obj = iob_inv(width=6)
    iob_inv_obj.generate_build_dir()
