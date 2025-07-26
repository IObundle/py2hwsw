#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

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
    def __init__(self, core_dict):
        super().__init__(core_dict)


if __name__ == "__main__":
    iob_and_obj = iob_and(core_dictionary)
    iob_and_obj.generate_build_dir()
