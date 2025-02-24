# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": False,
        "confs": [
            {
                "name": "AXIL_ADDR_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXIL_DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
            {
                "name": "ADDR_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
            {
                "name": "DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {"type": "iob_clk"},
            },
            {
                "name": "iob_s",
                "descr": "Slave IOb interface",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "axil_m",
                "descr": "Master AXI Lite interface",
                "signals": {
                    "type": "axil",
                    "ADDR_W": "AXIL_ADDR_W",
                    "DATA_W": "AXIL_DATA_W",
                },
            },
        ],
    }

    return attributes_dict
