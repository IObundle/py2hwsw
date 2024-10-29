# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

bsp = [
    {"name": "BAUD", "type": "M", "val": "115200"},
    {"name": "FREQ", "type": "M", "val": "50000000"},
    {"name": "INTEL", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    attributes_dict = {
        "confs": bsp,
    }

    return attributes_dict
