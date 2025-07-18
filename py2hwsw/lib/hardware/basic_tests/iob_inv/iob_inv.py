#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import py2hwsw_api as py2hwsw

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
            "descr": "Input port",
            "wires": [
                {"name": "a_i", "width": "W"},
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
    "snippets": [{"verilog_code": "   assign y_o = ~a_i;"}],
}


class iob_inv(py2hwsw.iob_core):
    def __init__(self):
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_inv_obj = iob_inv()
    iob_inv_obj.generate_build_dir()
