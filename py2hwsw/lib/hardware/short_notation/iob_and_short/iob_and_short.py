#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

core_dictionary = {
    "generate_hw": True,
    "confs": [
        """
            W -t P -v 21 -m 1 -M 32
            -d 'Ports width'
        """
    ],
    "ports": [
        """
            a_i -s a_i:W
            -d 'Input port a'

            b_i -s b_i:W
            -d 'Input port b'

            y_o -s y_o:W
            -d 'Output port y'
        """
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
