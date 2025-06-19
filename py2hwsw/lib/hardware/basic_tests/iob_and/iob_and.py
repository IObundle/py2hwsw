#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import py2hwsw_api as py2hwsw

core_dictionary = {
    "generate_hw": True,
    "confs": [
        {
            "name": "general",
            "descr": "General group of confs",
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
        },
    ],
    "ports": [
        {
            "name": "a_i",
            "descr": "Input port",
            "signals": [
                {"name": "a_i", "width": "W"},
            ],
        },
        {
            "name": "b_i",
            "descr": "Input port",
            "signals": [
                {"name": "b_i", "width": "W"},
            ],
        },
        {
            "name": "y_o",
            "descr": "Output port",
            "signals": [
                {"name": "y_o", "width": "W"},
            ],
        },
    ],
    "snippets": [{"verilog_code": "   assign y_o = a_i & b_i;"}],
}


class iob_and(py2hwsw.iob_core):
    def __init__(self):
        super().__init__(core_dictionary)


if __name__ == "__main__":
    print(py2hwsw.__dict__)
    # iob_and_obj = iob_and()
    # iob_and.generate_build_dir()
