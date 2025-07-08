# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["issuer"]["name"] + "_iob_de10_lite",
        "generate_hw": False,
        "confs": [
            {
                "name": "FREQ",
                "descr": "Typical clock frequency for this FPGA board",
                "type": "D",
                "val": "50000000",
            },
            {
                "name": "INTEL",
                "descr": "Intel flag to signal that this board uses Intel tools",
                "type": "D",
                "val": "1",
            },
        ],
    }

    return attributes_dict
