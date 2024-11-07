# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset interface",
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                        "descr": "Synchronous reset input",
                    },
                ],
            },
            {
                "name": "config_in_io",
                "descr": "AXI Stream input configuration interface",
                "signals": [
                    {
                        "name": "config_in_addr_i",
                        "width": "AXI_ADDR_W",
                        "descr": "",
                    },
                    {
                        "name": "config_in_valid_i",
                        "width": 1,
                        "descr": "",
                    },
                    {
                        "name": "config_in_ready_o",
                        "width": 1,
                        "descr": "",
                    },
                ],
            },
            {
                "name": "axis_in_io",
                "descr": "AXI Stream input interface",
                "signals": [
                    {
                        "name": "axis_in_data_i",
                        "width": "AXI_DATA_W",
                        "descr": "",
                    },
                    {
                        "name": "axis_in_valid_i",
                        "width": 1,
                        "descr": "",
                    },
                    {
                        "name": "axis_in_ready_o",
                        "width": 1,
                        "descr": "",
                    },
                ],
            },
            {
                "name": "axi_write_m",
                "signals": {
                    "type": "axi_write",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
                "descr": "AXI write interface",
            },
            {
                "name": "extmem_io",
                "descr": "External memory interface",
                "signals": [
                    {
                        "name": "ext_mem_w_en_o",
                        "width": 1,
                        "descr": "Memory write enable",
                    },
                    {
                        "name": "ext_mem_w_addr_o",
                        "width": "BUFFER_W",
                        "descr": "Memory write address",
                    },
                    {
                        "name": "ext_mem_w_data_o",
                        "width": "AXI_DATA_W",
                        "descr": "Memory write data",
                    },
                    {
                        "name": "ext_mem_r_en_o",
                        "width": 1,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "ext_mem_r_addr_o",
                        "width": "BUFFER_W",
                        "descr": "Memory read address",
                    },
                    {
                        "name": "ext_mem_r_data_i",
                        "width": "AXI_DATA_W",
                        "descr": "Memory read data",
                    },
                ],
            },
        ],
        "blocks": [],
    }

    return attributes_dict
