# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            # AXI parameters
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "4",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "operation_io",
                "descr": "Operation interface",
                "signals": [
                    {
                        "name": "start_addr_i",
                        "width": "AXI_ADDR_W",
                        "descr": "Burst start address",
                    },
                    {"name": "length_i", "width": "AXI_LEN_W", "descr": "Burst length"},
                    {
                        "name": "read_data_o",
                        "width": "AXI_DATA_W",
                        "descr": "Read data",
                    },
                    {
                        "name": "read_data_valid_o",
                        "width": 1,
                        "descr": "Read data valid",
                    },
                    {
                        "name": "read_data_ready_i",
                        "width": 1,
                        "descr": "Read data ready",
                    },
                    {"name": "read_ready_o", "width": 1, "descr": "Read ready"},
                    {"name": "level_o", "width": "AXI_LEN_W+1", "descr": "FIFO level"},
                ],
            },
            {
                "name": "axi_read_m",
                "descr": "AXI Read interface",
                "signals": {
                    "type": "axi_read",
                    "prefix": "m_",
                    "file_prefix": "iob_iob2axi_read_m_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
        ],
    }

    return attributes_dict
