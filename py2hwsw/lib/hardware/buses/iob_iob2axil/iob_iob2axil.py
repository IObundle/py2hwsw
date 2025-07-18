# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
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
                "val": "AXIL_ADDR_W",
                "min": "1",
                "max": "32",
            },
            {
                "name": "DATA_W",
                "descr": "",
                "type": "P",
                "val": "AXIL_DATA_W",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "wires": {"type": "iob_clk"},
            },
            {
                "name": "iob_s",
                "descr": "Subordinate IOb interface",
                "wires": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "axil_m",
                "descr": "Manager AXI Lite interface",
                "wires": {
                    "type": "axil",
                    "ADDR_W": "AXIL_ADDR_W",
                    "DATA_W": "AXIL_DATA_W",
                },
            },
        ],
    }

    return attributes_dict
