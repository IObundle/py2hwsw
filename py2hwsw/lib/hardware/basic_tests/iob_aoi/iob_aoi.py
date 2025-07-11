#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import copy
import py2hwsw_api as py2hwsw

# Short notation with API is WIP
# core_dictionary = {
#     "generate_hw": True,
#     "confs": [
#         """
#             W -t P -v 1 -m 1 -M 32
#             -d 'Ports width'
#             """
#     ],
#     "ports": [
#         """
#             a_i -s a_i:W
#             -d 'Input port a'
#
#             b_i -s b_i:W
#             -d 'Input port b'
#
#             c_i -s c_i:W
#             -d 'Input port c'
#
#             d_i -s d_i:W
#             -d 'Input port d'
#
#             y_o -s y_o:W
#             -d 'Output port y'
#             """
#     ],
#     "wires": [
#         """
#             and_ab_out -s aab:W
#             -d 'and ab output'
#
#             and_cd_out -s cad:W
#             -d 'and cd output'
#
#             or_out -s oab:1
#             -d 'or output'
#             """,
#     ],
#     "subblocks": [
#         """
#             iob_and iob_and_ab -p W:W -c
#             a_i:a_i
#             b_i:b_i
#             y_o:and_ab_out
#             -d 'First and gate'
#
#             iob_and io_and_cd -p W:W -c
#             a_i:c_i
#             b_i:d_i
#             y_o:and_cd_out
#             -d 'Second and gate'
#
#             iob_or iob_or_abcd -p W:W -c
#             a_i:and_ab_out
#             b_i:and_cd_out
#             y_o:or_out
#             -d 'Or gate'
#
#             iob_inv iob_inv_out -p W:W -c
#             a_i:or_out
#             y_o:y_o
#             -d 'Inverter'
#             """,
#     ],
#     "superblocks": [
#         # Tester
#         {
#             "core_name": "iob_aoi_tester",
#             "instance_name": "iob_tester",
#             "dest_dir": "tester",
#         },
#     ],
# }

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
                    "val": "1",
                    "min": "1",
                    "max": "32",
                    "descr": "Ports width",
                },
            ],
        },
    ],
    "ports": [
        {
            "name": "a_i",
            "descr": "Input port a",
            "signals": [
                {"name": "a_i", "width": "W"},
            ],
        },
        {
            "name": "b_i",
            "descr": "Input port b",
            "signals": [
                {"name": "b_i", "width": "W"},
            ],
        },
        {
            "name": "c_i",
            "descr": "Input port c",
            "signals": [
                {"name": "c_i", "width": "W"},
            ],
        },
        {
            "name": "d_i",
            "descr": "Input port d",
            "signals": [
                {"name": "d_i", "width": "W"},
            ],
        },
        {
            "name": "y_o",
            "descr": "Output port y",
            "signals": [
                {"name": "y_o", "width": "W"},
            ],
        },
    ],
    "wires": [
        {
            "name": "and_ab_out",
            "descr": "and ab output",
            "signals": [
                {"name": "aab", "width": "W"},
            ],
        },
        {
            "name": "and_cd_out",
            "descr": "and cd output",
            "signals": [
                {"name": "cad", "width": "W"},
            ],
        },
        {
            "name": "or_out",
            "descr": "or output",
            "signals": [
                {"name": "oab", "width": "1"},
            ],
        },
    ],
    # TODO: Replace "portmap_connections" by "connect"
    "subblocks": [
        {
            "core": "iob_and",
            "descr": "First and gate",
            "instance_name": "iob_and_ab",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "a_i",
                "b_i": "b_i",
                "y_o": "and_ab_out",
            },
        },
        {
            "core": "iob_and",
            "descr": "Second and gate",
            "instance_name": "io_and_cd",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "c_i",
                "b_i": "d_i",
                "y_o": "and_cd_out",
            },
        },
        # {
        #     "core": "iob_or",
        #     "descr": "Or gate",
        #     "instance_name": "iob_or_abcd",
        #     "parameters": {
        #         "W": "W",
        #     },
        #     "portmap_connections": {
        #         "a_i": "and_ab_out",
        #         "b_i": "and_cd_out",
        #         "y_o": "or_out",
        #     },
        # },
        # {
        #     "core": "iob_inv",
        #     "descr": "Inverter",
        #     "instance_name": "iob_inv_out",
        #     "parameters": {
        #         "W": "W",
        #     },
        #     "portmap_connections": {
        #         "a_i": "or_out",
        #         "y_o": "y_o",
        #     },
        # },
    ],
    "superblocks": [
        # Tester
        # {
        #     "core": "iob_aoi_tester",
        #     "instance_name": "iob_tester",
        #     # "dest_dir": "tester",
        # },
    ],
}


class iob_aoi(py2hwsw.iob_core):
    def __init__(self):
        print("iob_aoi constructor called.")
        super().__init__(core_dictionary)


if __name__ == "__main__":
    # NOTE: Be careful that calling create_core_from_dict() will modify the dictionary given to it
    core_obj = py2hwsw.create_core_from_dict(copy.deepcopy(core_dictionary))
    print(">>> Generate_hw of core_obj: ", core_obj.get_generate_hw())
    print(">>> Ports of core_obj: ", [i.get_name() for i in core_obj.get_ports()])
    print(
        ">>> Subblocks of core_obj: ",
        [i.get_name() for i in core_obj.get_subblocks()],
    )
    print(
        ">>> Ports of iob_and subblock: ",
        core_obj.get_subblocks()[0].get_ports(),
    )

    # iob_aoi_obj = iob_aoi()
    # print(">>> Ports of iob_aoi: ", iob_aoi_obj.get_ports())
    # print(">>> Ports of iob_aoi: ", [i.get_name() for i in iob_aoi_obj.get_ports()])

    # iob_aoi.generate_build_dir()
