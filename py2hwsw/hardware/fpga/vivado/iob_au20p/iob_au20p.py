# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_au20p",
        "generate_hw": False,
        "confs": [
            {
                "name": "BAUD",
                "descr": "UART baud rate",
                "type": "F",
                "val": "115200",
            },
            {
                "name": "FREQ",
                "descr": "Clock frequency",
                "type": "F",
                "val": "100000000",
            },
            {
                "name": "XILINX",
                "descr": "xilinx flag",
                "type": "F",
                "val": "1",
            },
        ],
    }

    return attributes_dict
