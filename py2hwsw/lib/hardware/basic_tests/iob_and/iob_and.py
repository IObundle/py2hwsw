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

    conf_obj = py2hwsw.create_conf_from_text(
        """
        W -t P -v 21 -m 1 -M 32
        -d 'IO width'
        """
    )

    conf_groups_obj = py2hwsw.create_conf_group_from_text(
        """
        'Default group'
        -d 'Default group of confs'
        -doc
        -doc_clearpage
        --confs
            "
            DATA_W -t P -v 32 -m NA -M NA
            -d 'Data bus width'

            FRACTIONAL_W -t P -v 0 -m NA -M NA
            -d 'Fractional part width'

            REAL_W -t P -v 'DATA_W - FRACTIONAL_W' -m NA -M NA
            -d 'Real part width'

            SIZE_W -t P -v '(REAL_W / 2) + FRACTIONAL_W' -m NA -M NA
            -d 'Size width'

            END_COUNT -t D -v '(DATA_W + FRACTIONAL_W) >> 1' -m NA -M NA
            -d 'End count'

            COUNT_W -t D -v $clog2(END_COUNT) -m NA -M NA
            -d 'Count width'
            "
        """
    )
    print(conf_groups_obj.get_name())
    print(conf_groups_obj.get_descr())
    print(conf_groups_obj.get_doc_only())
    print(conf_groups_obj.get_doc_clearpage())
    for conf in conf_groups_obj.get_confs():
        print(">>> Conf name: ", conf.get_name())
        print(">>> Conf kind: ", conf.get_kind())
        print(">>> Conf value: ", conf.get_value())
        print(">>> Conf min: ", conf.get_min_value())
        print(">>> Conf max: ", conf.get_max_value())
        print(">>> Conf description: ", conf.get_descr())

    print("\n\n")
    signal_obj = py2hwsw.create_signal_from_text("en -w 1 -d 'Enable signal' -v")
    print("signal_obj: ", signal_obj.get_name(), end=" ")
    print("width: ", signal_obj.get_width(), end=" ")
    print("isvar: ", signal_obj.get_isvar(), end=" ")
    print("descr: ", signal_obj.get_descr())

    print("\n\n")
    wire_obj = py2hwsw.create_wire_from_text(
        """
            aoi_outs -s aab:W -s cad:W -s oab:1
            -d 'AOI outputs'
        """
    )
    print("wire_obj: ", wire_obj.get_name(), end=" ")
    print("width: ", wire_obj.get_interface())
    for signal in wire_obj.get_signals():
        print("\tsignal: ", signal.get_name(), "width:", signal.get_width())
    print("descr: ", wire_obj.get_descr())

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

    core_obj = py2hwsw.create_core_from_dict(core_dictionary)
    print(">>> Generate_hw of core_obj: ", core_obj.get_generate_hw())
    print(">>> Ports of core_obj: ", [i.get_name() for i in core_obj.get_ports()])

    # conf_obj.test_method()

    iob_and_obj = iob_and()
    print(">>> Generate_hw of iob_and_obj: ", iob_and_obj.get_generate_hw())
    print(">>> Ports of iob_and_obj: ", [i.get_name() for i in iob_and_obj.get_ports()])

    iob_and_obj.generate_build_dir()
