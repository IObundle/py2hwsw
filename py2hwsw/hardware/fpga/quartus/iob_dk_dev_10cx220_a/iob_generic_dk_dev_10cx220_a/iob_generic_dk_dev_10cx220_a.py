# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["issuer"]["name"] + "_iob_dk_dev_10cx220_a",
        "generate_hw": False,
        "confs": [
            {
                "name": "DDR_ADDR_W",
                "descr": "Width of DDR memory address bus (byte addressed).",
                "type": "D",
                "val": "32",
            },
            {
                "name": "FREQ",
                "descr": "Typical clock frequency for this FPGA board",
                "type": "D",
                "val": "50000000",
            },
            {
                "name": "MEM_NO_READ_ON_WRITE",
                "descr": "Memory no read on write flag. Signals that this FPGA board does not support memories with simultaneous read and write.",
                "type": "D",
                "val": "1",
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
