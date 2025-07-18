# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "ADDR_WIDTH",
                "descr": "Width of address bus in bits",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "DATA_WIDTH",
                "descr": "Width of input (subordinate/manager) AXIS/AHB interface data bus in bits",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "STRB_WIDTH",
                "descr": "Width of input (subordinate/manager) AXIS/AHB interface wstrb (width of data bus in words)",
                "type": "P",
                "val": "(DATA_WIDTH / 8)",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_ID_WIDTH",
                "descr": "Width of AXI ID wire",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "axis_s",
                "descr": "AXIS IN interface",
                "wires": {
                    "type": "axis",
                    "prefix": "in_",
                    "params": "tlast",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
            },
            {
                "name": "axis_m",
                "descr": "AXIS OUT interface",
                "wires": {
                    "type": "axis",
                    "params": "tlast",
                    "prefix": "out_",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
            },
            {
                "name": "config_in_io",
                "descr": "AXI Stream input configuration interface",
                "wires": [
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
                "wires": [
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
                "name": "general_o",
                "descr": "Generic interface",
                "wires": [
                    {
                        "name": "busy_o",
                        "width": 1,
                        "descr": "Module busy: (0) waiting for configuration; (1) during operation.",
                    },
                ],
            },
            {
                "name": "ahb_m",
                "descr": "Manager AHB interface",
                "wires": {
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
            {"core_name": "iob_ahb_ram"},
        ],
    }

    return attributes_dict
