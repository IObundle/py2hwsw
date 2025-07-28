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
            "value": "1",
            "min_value": "1",
            "max_value": "32",
            "descr": "Ports width",
        },
    ],
    "ports": [
        {
            "name": "a_i",
            "width": "W",
            "descr": "Input port a",
        },
        {
            "name": "b_i",
            "descr": "Input port b",
            "width": "W",
        },
        {
            "name": "c_i",
            "descr": "Input port c",
            "width": "W",
        },
        {
            "name": "d_i",
            "descr": "Input port d",
            "width": "W",
        },
        {
            "name": "y_o",
            "descr": "Output port y",
            "width": "W",
        },
    ],
    "wires": [
        {
            "name": "aab",
            "width": "W",
        },
        {
            "name": "cad",
            "width": "W",
        },
        {
            "name": "aob",
            "width": "W",
        },
    ],
    "subblocks": [
        {
            "core": "iob_and",
            "name": "iob_and_ab",
            "description": "First and gate",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "a_i",
                "b_i": "b_i",
                "y_o": "aab",
            },
        },
        {
            "core": "iob_and",
            "name": "io_and_cd",
            "description": "Second and gate",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "c_i",
                "b_i": "d_i",
                "y_o": "cad",
            },
        },
        {
            "core": "iob_or",
            "name": "iob_or_abcd",
            "description": "Or gate",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "aab",
                "b_i": "cad",
                "y_o": "aob",
            },
        },
        {
            "core": "iob_inv",
            "name": "iob_inv_out",
            "description": "Inverter",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "aob",
                "y_o": "y_o",
            },
        },
    ],
    "superblocks": [
        # Tester
        # {
        #     "core": "iob_aoi_tester",
        #     "name": "iob_tester",
        #     "dest_dir": "tester",
        # },
    ],
}


class iob_aoi(iob_core):
    def __init__(self, width=None):
        if width:
            core_dictionary["confs"][0]["value"] = str(width)
        print("iob_aoi constructor called.")
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_aoi_obj = iob_aoi(width=1)
    iob_aoi_obj.generate_build_dir()
