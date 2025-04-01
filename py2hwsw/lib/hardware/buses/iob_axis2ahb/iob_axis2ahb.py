# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "ADDR_WIDTH",
                "descr": "",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "DATA_WIDTH",
                "descr": "",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "STRB_WIDTH",
                "descr": "",
                "type": "P",
                "val": "(DATA_WIDTH / 8)",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_ID_WIDTH",
                "descr": "",
                "type": "P",
                "val": "8",
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
                "name": "axis_s",
                "descr": "AXIS IN interface",
                "signals": {
                    "type": "axis",
                    "prefix": "in_",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
            },
            {
                "name": "axis_m",
                "descr": "AXIS OUT interface",
                "signals": {
                    "type": "axis",
                    "prefix": "out_",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
            },
            {
                "name": "config_in_io",
                "descr": "AXI Stream input configuration interface",
                "signals": [
                    {
                        "name": "config_in_addr_i",
                        "width": "ADDR_WIDTH",
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
                "name": "config_out_io",
                "descr": "AXI Stream output configuration interface",
                "signals": [
                    {
                        "name": "config_out_addr_i",
                        "width": "ADDR_WIDTH",
                        "descr": "",
                    },
                    {
                        "name": "config_out_length_i",
                        "width": "ADDR_WIDTH",
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
                "name": "ahb_m",
                "descr": "Master AHB interface",
                "signals": {
                    "type": "ahb",
                    "prefix": "m_",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instantiate": False,
            },
        ],
        "superblocks": [
            {"core_name": "iob_axistream_in"},
            {"core_name": "iob_axistream_out"},
        ],
    }

    return attributes_dict
