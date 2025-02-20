# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "WDATA_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "8",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
        ],
        "wires": [
            # Register wires
            {
                "name": "reset",
                "descr": "",
                "signals": [
                    {"name": "reset_wr", "width": 1},
                ],
            },
            {
                "name": "enable",
                "descr": "",
                "signals": [
                    {"name": "enable_wr", "width": 1},
                ],
            },
            {
                "name": "sample",
                "descr": "",
                "signals": [
                    {"name": "sample_wr", "width": 1},
                ],
            },
            {
                "name": "data_low",
                "descr": "",
                "signals": [
                    {"name": "data_low_rd", "width": 32},
                ],
            },
            {
                "name": "data_high",
                "descr": "",
                "signals": [
                    {"name": "data_high_rd", "width": 32},
                ],
            },
            # Internal wires
            {
                "name": "time_now",
                "descr": "",
                "signals": [
                    {"name": "time_now", "width": 64},
                ],
            },
            # Timer core
            {
                "name": "iob_timer_core_reg_interface",
                "descr": "",
                "signals": [
                    {"name": "enable_wr"},
                    {"name": "reset_wr"},
                    {"name": "sample_wr"},
                    {"name": "time_now"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "iob_csrs",
                "instance_description": "Control/Status Registers",
                "csrs": [
                    {
                        "name": "reset",
                        "type": "W",
                        "n_bits": 1,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "Timer soft reset",
                    },
                    {
                        "name": "enable",
                        "type": "W",
                        "n_bits": 1,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "Timer enable",
                    },
                    {
                        "name": "sample",
                        "type": "W",
                        "n_bits": 1,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "Sample time counter value into a readable register",
                    },
                    {
                        "name": "data_low",
                        "type": "R",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "High part of the timer value, which has twice the width of the data word width",
                    },
                    {
                        "name": "data_high",
                        "type": "R",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "autoreg": True,
                        "descr": "Low part of the timer value, which has twice the width of the data word width",
                    },
                ],
                "csr_if": "iob",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # 'control_if_m' port connected automatically
                    # Register interfaces
                    "reset_o": "reset",
                    "enable_o": "enable",
                    "sample_o": "sample",
                    "data_low_i": "data_low",
                    "data_high_i": "data_high",
                },
            },
            {
                "core_name": "iob_timer_core",
                "instance_name": "iob_timer_core_inst",
                "instance_description": "Timer core driver",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reg_interface_io": "iob_timer_core_reg_interface",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    assign data_low_rd  = time_now[DATA_W-1:0];
    assign data_high_rd = time_now[2*DATA_W-1:DATA_W];
""",
            },
        ],
    }

    return attributes_dict
