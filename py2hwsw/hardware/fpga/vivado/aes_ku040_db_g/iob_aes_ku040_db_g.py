# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

bsp = [
    {"name": "BAUD", "type": "M", "val": "115200"},
    {"name": "FREQ", "type": "M", "val": "100000000"},
    {"name": "DDR_DATA_W", "type": "M", "val": "32"},
    {"name": "DDR_ADDR_W", "type": "M", "val": "30"},
    {"name": "XILINX", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_aes_ku040_db_g",
        "confs": [
            {
                "name": "bsp",
                "descr": "Board Support Package confs",
                "confs": bsp,
            },
        ],
    }

    return attributes_dict
