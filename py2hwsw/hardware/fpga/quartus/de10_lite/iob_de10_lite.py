# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

bsp = [
    {"name": "BAUD", "type": "M", "val": "115200"},
    {"name": "FREQ", "type": "M", "val": "50000000"},
    {"name": "INTEL", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_de10_lite",
        "generate_hw": True,
        "confs": [
            {
                "name": "bsp",
                "descr": "Board Support Package confs",
                "confs": bsp,
            },
        ],
    }

    return attributes_dict
