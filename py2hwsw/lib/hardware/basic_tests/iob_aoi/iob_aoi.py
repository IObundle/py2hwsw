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
            "descr": "Data width",
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
            "name": "ab",
            "width": "W",
        },
        {
            "name": "cd",
            "width": "W",
        },
        {
            "name": "or_int",
            "width": "W",
        },
    ],
    "subblocks": [
        {
            "core": "iob_and",
            "name": "a_and_b",
            "description": "AND gate for inputs a and b",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "a_i",
                "b_i": "b_i",
                "y_o": "ab",
            },
        },
        {
            "core": "iob_and",
            "name": "c_and_d",
            "description": "AND gate for inputs c and d",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "c_i",
                "b_i": "d_i",
                "y_o": "cd",
            },
        },
        {
            "core": "iob_or",
            "name": "ab_or_cd",
            "description": "OR gate for inputs ab and cd",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "a_i": "ab",
                "b_i": "cd",
                "y_o": "or_int",
            },
        },
        {
            "core": "iob_inv",
            "name": "ao_inv",
            "description": "Inverter for the OR output",
            "parameters": {
                "W": "W",
            },
            "portmap_connections": {
                "x_i": "or_int",
                "y_o": "y_o",
            },
        },
    ],
}


class iob_aoi(iob_core):
    def __init__(self):
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_aoi_obj = iob_aoi()
    iob_aoi_obj.generate_build_dir()
