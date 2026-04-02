# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["issuer"]["name"] + "_iob_smart_zynq_sl",
        "generate_hw": True,
        "confs": [
            {
                "name": "DDR_ADDR_W",
                "descr": "Smart Zynq SL has 512 MiB of DDR3 memory. 2**29 byte-addresses = 512 MiB.",
                "type": "D",
                "val": "29",
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
