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
        print("iob_and constructor called.")
        super().__init__(core_dictionary)


if __name__ == "__main__":
    # conf_obj = py2hwsw.iob_conf(name="a")
    conf_group_obj = py2hwsw.create_conf_group_from_dict(
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
    )
    print(">>> Name of conf_group_obj: ", conf_group_obj.get_name())
    print(">>> Name of conf_obj: ", conf_group_obj.get_confs()[0].get_name())

    port_obj = py2hwsw.create_port_from_dict(
        {
            "name": "a_i",
            "descr": "Input port",
            "signals": [
                {"name": "a_i", "width": "W"},
            ],
        },
    )
    print(">>> Name of port_obj: ", port_obj.get_name())
    print(">>> Name of port signal: ", port_obj.get_signals()[0].get_name())

    snippet_obj = py2hwsw.create_snippet_from_dict(
        {"verilog_code": "   assign y_o = a_i & b_i;"}
    )
    print(">>> Verilog of snippet_obj: ", snippet_obj.get_verilog_code())

    # NOTE: Be careful that calling create_core_from_dict() will modify the dictionary given to it
    core_obj = py2hwsw.create_core_from_dict(core_dictionary)
    print(">>> Generate_hw of core_obj: ", core_obj.get_generate_hw())
    print(">>> Ports of core_obj: ", [i.get_name() for i in core_obj.get_ports()])

    # conf_obj.test_method()

    iob_and_obj = iob_and()
    print(">>> Generate_hw of iob_and_obj: ", iob_and_obj.get_generate_hw())
    print(">>> Ports of iob_and_obj: ", [i.get_name() for i in iob_and_obj.get_ports()])

    # iob_and.generate_build_dir()
