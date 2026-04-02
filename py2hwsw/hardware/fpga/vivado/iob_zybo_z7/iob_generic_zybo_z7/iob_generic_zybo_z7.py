# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["issuer"]["name"] + "_iob_zybo_z7",
        "generate_hw": True,
        "confs": [
            {
                "name": "DDR_ADDR_W",
                "descr": "Zybo Z7 has 1 GiB of DDR3L memory. 2**30 byte-addresses = 1 GiB.",
                "type": "D",
                "val": "30",
            },
            {
                "name": "BAUD",
                "descr": "UART baud rate",
                "type": "D",
                "val": "115200",
            },
            {
                "name": "FREQ",
                "descr": "Typical clock frequency for this FPGA board",
                "type": "D",
                "val": "50000000",
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
