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


class iob_and(py2hwsw.iob_core):
    def __init__(self):
        print("[DEBUG]: iob_and constructor called.")
        super().__init__(core_dictionary)


if __name__ == "__main__": 

    iob_and_obj = iob_and()
    iob_and_obj.get_generate_hw();
    iob_and_obj.generate_build_dir()

    #OF COURSE THIS IS NOT THE RIGHT WAY TO DO IT! TO BE DELETED
    # GLOBAL WIRES ARE NOT EXPOSED . USERS DO NOT NEED TO KNOW ABOUT THEM
    # get_ports is useful
    #[i.get_global_wire().get_name() for i in iob_and_obj.get_ports()],
    
