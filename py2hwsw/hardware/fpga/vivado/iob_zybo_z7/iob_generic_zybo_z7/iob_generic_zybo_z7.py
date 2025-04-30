# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_iob_zybo_z7",
        "generate_hw": False,
        "confs": [
            {
                "name": "FREQ",
                "descr": "Typical clock frequency for this FPGA board",
                "type": "D",
                "val": "100000000",
            },
            {
                "name": "XILINX",
                "descr": "Xilinx flag to signal that this board uses Xilinx tools",
                "type": "D",
                "val": "1",
            },
        ],
    }

    return attributes_dict
