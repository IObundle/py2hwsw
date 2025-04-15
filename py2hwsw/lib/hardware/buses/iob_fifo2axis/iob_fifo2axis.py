# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
            },
            {
                "name": "AXIS_LEN_W",
                "descr": "AXIS length bus width",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable, and reset",
            },
            {
                "name": "rst_i",
                "descr": "Reset signal",
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                        "descr": "Reset signal",
                    },
                ],
            },
            {
                "name": "en_i",
                "descr": "Enable signal",
                "signals": [
                    {
                        "name": "en_i",
                        "width": 1,
                        "descr": "Enable signal",
                    },
                ],
            },
            {
                "name": "len_i",
                "descr": "Length signal",
                "signals": [
                    {
                        "name": "len_i",
                        "width": "AXIS_LEN_W",
                        "descr": "Length signal",
                    },
                ],
            },
            {
                "name": "level_o",
                "descr": "Level signal",
                "signals": [
                    {
                        "name": "level_o",
                        "width": 2,
                        "descr": "Level signal",
                        "isvar": True,
                    },
                ],
            },
            {
                "name": "fifo_r_io",
                "descr": "FIFO read interface",
                "signals": [
                    {
                        "name": "fifo_read_o",
                        "width": 1,
                        "descr": "FIFO read signal",
                    },
                    {
                        "name": "fifo_rdata_i",
                        "width": "DATA_W",
                        "descr": "FIFO read data signal",
                    },
                    {
                        "name": "fifo_empty_i",
                        "width": 1,
                        "descr": "FIFO empty signal",
                    },
                ],
            },
            {
                "name": "axis_m",
                "descr": "AXIS master interface",
                "signals": {
                    "type": "axis",
                    "params": "tlast",
                    "DATA_W": "DATA_W",
                },
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
            {
                "core_name": "iob_modcnt",
                "instance_name": "iob_modcnt_inst",
            },
        ],
    }

    return attributes_dict
