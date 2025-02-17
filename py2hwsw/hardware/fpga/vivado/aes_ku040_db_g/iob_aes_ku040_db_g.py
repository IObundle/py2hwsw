# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": py_params_dict["instantiator"]["name"] + "_aes_ku040_db_g",
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "F",
                "val": "4",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "F",
                "val": "8",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "F",
                "val": "30",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "F",
                "val": "32",
            },
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
