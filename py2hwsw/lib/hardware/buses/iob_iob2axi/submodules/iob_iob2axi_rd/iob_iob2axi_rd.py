# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_i",
                "descr": "Clock",
                "signals": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset",
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "control_io",
                "descr": "Control interface",
                "signals": [
                    {"name": "run_i", "width": 1, "descr": ""},
                    {"name": "addr_i", "width": "ADDR_W", "descr": ""},
                    {"name": "length_i", "width": "AXI_LEN_W", "descr": ""},
                    {"name": "ready_o", "width": 1, "descr": ""},
                    {"name": "error_o", "width": 1, "descr": ""},
                ],
            },
            {
                "name": "axi_read_m",
                "descr": "AXI read interface",
                "signals": {
                    "type": "axi_read",
                    "prefix": "m_",
                    "file_prefix": "iob_iob2axi_rd_m_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "iob_m",
                "descr": "IOb interface",
                "signals": {
                    "type": "iob",
                    "prefix": "m_",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
    }

    return attributes_dict
