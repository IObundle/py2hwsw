# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_cyclonev_gt_dk",
        "generate_hw": True,
        "confs": [
            {
                "name": "FREQ",
                "descr": "Typical clock frequency for this FPGA board",
                "type": "F",
                "val": "50000000",
            },
            {
                "name": "MEM_NO_READ_ON_WRITE",
                "descr": "Memory no read on write flag. Signals that this FPGA board does not support memories with simultaneous read and write.",
                "type": "F",
                "val": "1",
            },
            {
                "name": "INTEL",
                "descr": "Intel flag to signal that this board uses Intel tools",
                "type": "F",
                "val": "1",
            },
        ],
    }

    return attributes_dict
