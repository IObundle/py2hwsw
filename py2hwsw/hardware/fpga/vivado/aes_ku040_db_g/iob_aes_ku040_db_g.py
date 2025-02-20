# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_aes_ku040_db_g",
        "generate_hw": True,
        "confs": [
            {
                "name": "DDR_ADDR_W",
                "descr": "Width of DDR memory address bus (byte addressed).",
                "type": "F",
                "val": "30",
            },
            {
                "name": "FREQ",
                "descr": "Typical clock frequency for this FPGA board",
                "type": "F",
                "val": "100000000",
            },
            {
                "name": "XILINX",
                "descr": "Xilinx flag to signal that this board uses Xilinx tools",
                "type": "F",
                "val": "1",
            },
        ],
    }

    return attributes_dict
