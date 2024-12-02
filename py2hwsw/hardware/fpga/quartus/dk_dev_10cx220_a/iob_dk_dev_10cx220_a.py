# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

bsp = [
    {"name": "BAUD", "type": "M", "val": "115200"},
    {"name": "FREQ", "type": "M", "val": "50000000"},
    {"name": "IOB_MEM_NO_READ_ON_WRITE", "type": "M", "val": "1"},
    {"name": "DDR_DATA_W", "type": "M", "val": "32"},
    {"name": "DDR_ADDR_W", "type": "M", "val": "28"},
    {"name": "INTEL", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_dk_dev_10cx220_a",
        "confs": [
            {
                "name": "bsp",
                "descr": "Board Support Package confs",
                "confs": bsp,
            },
        ],
    }

    return attributes_dict
