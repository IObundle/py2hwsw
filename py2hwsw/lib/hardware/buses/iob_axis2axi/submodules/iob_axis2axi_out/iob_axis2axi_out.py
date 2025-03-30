# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
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
                "name": "config_out_io",
                "descr": "AXI Stream output configuration interface",
                "signals": [
                    {
                        "name": "config_out_addr_i",
                        "width": "AXI_ADDR_W",
                        "descr": "",
                    },
                    {
                        "name": "config_out_length_i",
                        "width": "AXI_ADDR_W",
                        "descr": "",
                    },
                    {
                        "name": "config_out_valid_i",
                        "width": 1,
                        "descr": "",
                    },
                    {
                        "name": "config_out_ready_o",
                        "width": 1,
                        "descr": "",
                    },
                ],
            },
            {
                "name": "axis_out_io",
                "descr": "AXI Stream output interface",
                "signals": [
                    {
                        "name": "axis_out_data_o",
                        "width": "AXI_DATA_W",
                        "descr": "",
                    },
                    {
                        "name": "axis_out_valid_o",
                        "width": 1,
                        "descr": "",
                    },
                    {
                        "name": "axis_out_ready_i",
                        "width": 1,
                        "descr": "",
                    },
                ],
            },
            {
                "name": "axi_read_m",
                "signals": {
                    "type": "axi_read",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
                "descr": "AXI read interface",
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "cke_arst_rst",
                },
            },
            {
                "core_name": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "cke_arst_rst_en",
                },
            },
        ],
    }

    return attributes_dict
