# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_LEN_W",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "8",
                "descr": "AXI burst length width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
                "descr": "AXI data bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {
                    "type": "iob_clk",
                },
            },
            {
                "name": "soft_reset_o",
                "descr": "Soft reset signal",
                "signals": [
                    {
                        "name": "soft_reset_o",
                    },
                ],
            },
            {
                "name": "burst_length_o",
                "descr": "Burst length signal",
                "signals": [
                    {
                        "name": "burst_length_o",
                        "width": "(AXI_LEN_W+1)",
                    },
                ],
            },
            {
                "name": "w_level_i",
                "descr": "Write level signal",
                "signals": [
                    {
                        "name": "w_level_i",
                        "width": "(AXI_LEN_W+1)",
                    },
                ],
            },
            {
                "name": "r_level_i",
                "descr": "Read level signal",
                "signals": [
                    {
                        "name": "r_level_i",
                        "width": "(AXI_LEN_W+1)",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "csrs",
                "instance_description": "Control/Status Registers",
                "parameters": {
                    "AXI_LEN_W": "AXI_LEN_W",
                },
                "csrs": [
                    {
                        "name": "Control",
                        "descr": "UUT Control software accessible registers.",
                        "regs": [
                            {
                                "name": "soft_reset",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Soft reset.",
                            },
                            {
                                "name": "burst_length",
                                "mode": "W",
                                "n_bits": "(AXI_LEN_W+1)",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Bursts Length.",
                            },
                            {
                                "name": "w_level",
                                "mode": "R",
                                "n_bits": "(AXI_LEN_W+1)",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Data output.",
                            },
                            {
                                "name": "r_level",
                                "mode": "R",
                                "n_bits": "(AXI_LEN_W+1)",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Data output.",
                            },
                        ],
                    },
                ],
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "soft_reset_o": "soft_reset_o",
                    "burst_length_o": "burst_length_o",
                    "w_level_i": "w_level_i",
                    "r_level_i": "r_level_i",
                },
            },
        ],
    }

    return attributes_dict
