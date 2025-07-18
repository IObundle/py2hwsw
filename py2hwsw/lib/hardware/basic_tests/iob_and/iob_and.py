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
                    "kind": "P",
                    "value": "21",
                    "min_value": "1",
                    "max_value": "32",
                    "descr": "IO width",
                },
            ],
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
            "name": "b_i",
            "descr": "Input port",
            "wires": [
                {"name": "b_i", "width": "W"},
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
    "snippets": [{"verilog_code": "   assign y_o = a_i & b_i;"}],
}


class iob_and(py2hwsw.iob_core):
    def __init__(self):
        print("iob_and constructor called.")
        super().__init__(core_dictionary)


if __name__ == "__main__":
    # # conf_obj = py2hwsw.iob_conf(name="a")
    # conf_obj = py2hwsw.create_conf_from_dict(
    #     {
    #         "name": "W",
    #         "kind": "P",
    #         "value": "21",
    #         "min_value": "1",
    #         "max_value": "32",
    #         "descr": "IO width",
    #     }
    # )

    # conf_obj = py2hwsw.create_conf_from_text(
    #     """
    #     W -t P -v 21 -m 1 -M 32
    #     -d 'IO width'
    #     """
    # )

    # conf_obj = py2hwsw.create_conf_rom_text(
    #     """
    #     DATA_W -t P -v 32 -m NA -M NA
    #     -d 'Data bus width'
    #     """
    # )
    # print(">>> Conf name: ", conf_obj.get_name())
    # print(">>> Conf kind: ", conf_obj.get_kind())
    # print(">>> Conf value: ", conf_obj.get_value())
    # print(">>> Conf min: ", conf_obj.get_min_value())
    # print(">>> Conf max: ", conf_obj.get_max_value())
    # print(">>> Conf description: ", conf_obj.get_descr())

    # print("\n\n")
    # # wire_obj = py2hwsw.create_wire_from_text("en -w 1 -d 'Enable wire' -v")
    # # print("wire_obj: ", wire_obj.get_name(), end=" ")
    # # print("width: ", wire_obj.get_width(), end=" ")
    # # print("isvar: ", wire_obj.get_isvar(), end=" ")
    # # print("descr: ", wire_obj.get_descr())

    # # print("\n\n")
    # bus_obj = py2hwsw.create_bus_from_text(
    #     """
    #         aoi_outs -s aab:W -s cad:W -s oab:1
    #         -d 'AOI outputs'
    #     """
    # )
    # print("bus_obj: ", bus_obj.get_name(), end=" ")
    # print("width: ", bus_obj.get_interface())
    # for wire in bus_obj.get_wires():
    #     print("\twire: ", wire.get_name(), "width:", wire.get_width())
    # print("descr: ", bus_obj.get_descr())

    # exit(1)  # DEBUG
    # # iface_obj = py2hwsw.create_interface_from_text(
    # #     "axi -d manager -p cpu_ -m 1 -f ctrl_cpu_ -pm controller_"
    # # )
    # # iface_obj = py2hwsw.create_interface_from_text(
    # #     "rom_sp -d subordinate -p boot_ -w ADDR_W:8 -w DATA_W:32"
    # # )
    # # iface_obj = py2hwsw.create_interface_from_text(
    # #     "axis -p output_ -P 'has_tlast'"
    # # )

    # port_obj = py2hwsw.create_port_from_dict(
    #     {
    #         "name": "a_i",
    #         "descr": "Input port",
    #         "wires": [
    #             {"name": "a_i", "width": "W"},
    #         ],
    #     },
    # )
    # print(">>> Name of port_obj: ", port_obj.get_name())
    # print(">>> Name of port wire: ", port_obj.get_wires()[0].get_name())

    # port_obj = py2hwsw.create_port_from_text(
    #     "control -d 'control bus' -s start_i:1 -s done_o:1 -s cmd_i:CMD_W -doc"
    # )
    # print(">>> Name of port_obj: ", port_obj.get_name())
    # print(">>> port_obj doc_only: ", port_obj.get_doc_only())
    # print(">>> port_obj doc_clearpage: ", port_obj.get_doc_clearpage())
    # for s in port_obj.get_wires():
    #     print("\t>>> Wire name: ", s.get_name(), "width:", s.get_width())

    # snippet_obj = py2hwsw.create_snippet_from_dict(
    #     {"verilog_code": "   assign y_o = a_i & b_i;"}
    # )
    # print(">>> Verilog of snippet_obj: ", snippet_obj.get_verilog_code())

    # print("\n\nSnippet from text:")
    # snippet_obj = py2hwsw.create_snippet_from_text("   assign y_o = a_i & b_i;")
    # print(">>> Verilog of snippet_obj: ", snippet_obj.get_verilog_code())

    # comb_obj = py2hwsw.create_comb_from_text(
    #     """
    #         -c
    #         {{
    #             // Register data
    #             data_nxt = data;
    #         }}
    #         -clk_if c_a_r
    #         -clk_p data_
    #     """
    # )
    # print(">>> comb_obj: clk_if: ", comb_obj.get_clk_if(), end=" ")
    # print("|\t clk_prefix: ", comb_obj.get_clk_prefix())
    # print("code:")
    # print(comb_obj.get_code())
    # print("======\n\n")

    # fsm_obj = py2hwsw.create_fsm_from_text(
    #     """
    #         -t fsm
    #         -d 'a_o = 10;'
    #         -s
    #         {{
    #             A: a_o = 0;
    #             B: a_o = 1;
    #             a_o = 2;
    #             if(a_o == 0)
    #             begin
    #                 pcnt_nxt = A;
    #             end
    #             else
    #             begin
    #                 pcnt_nxt = B;
    #             end
    #          }}
    #     """
    # )
    # print(">>> fsm_obj: ", fsm_obj.get_kind())
    # print(">>> default assignments of fsm_obj:\n", fsm_obj.get_default_assignments())
    # print(">>> state descriptions of fsm_obj:\n", fsm_obj.get_state_descriptions())
    # print("======\n")

    # license_obj = py2hwsw.create_license_from_text("""MIT -y 2025 -a 'IObundle, Lda'""")
    # print(f">>> License name: {license_obj.get_name()}")
    # print(f"\tyear: {license_obj.get_year()}\n\tauthor: {license_obj.get_author()}")
    # print("======\n")

    # python_parameter_obj = py2hwsw.create_python_parameter_from_text(
    #     "my_param -v 42 -d 'My parameter description'"
    # )
    # print(f">>> python_parameter name: {python_parameter_obj.get_name()}")
    # print(
    #     f"\tvalue: {python_parameter_obj.get_val()}\n\tdescr: {python_parameter_obj.get_descr()}"
    # )
    # print("======\n")

    # py_param_group_obj = py2hwsw.create_python_parameter_group_from_text(
    #     """
    #             param_group -d 'Group of parameters' -doc_clearpage
    #             -P "param1 -v 42 -d 'Parameter 1 description'"
    #             -P "OUTPUT_W -v DATA_W -d 'Data width'"
    #      """
    # )
    # print(f">>> Python parameter group name: {py_param_group_obj.get_name()}")
    # print(f"\tdescr: {py_param_group_obj.get_descr()}")
    # for param in py_param_group_obj.get_python_parameters():
    #     print(f"\t>>> Parameter name: {param.get_name()}")
    #     print(f"\t\tvalue: {param.get_val()}\n\t\tdescr: {param.get_descr()}")
    # print("======\n")

    # core_obj = py2hwsw.create_core_from_dict(core_dictionary)
    # print(">>> Generate_hw of core_obj: ", core_obj.get_generate_hw())
    # print(">>> Ports of core_obj: ", [i.get_name() for i in core_obj.get_ports()])

    # conf_obj.test_method()

    iob_and_obj = iob_and()
    print(">>> Generate_hw of iob_and_obj: ", iob_and_obj.get_generate_hw())
    print(">>> Ports of iob_and_obj: ", [i.get_name() for i in iob_and_obj.get_ports()])

    iob_and_obj.generate_build_dir()
