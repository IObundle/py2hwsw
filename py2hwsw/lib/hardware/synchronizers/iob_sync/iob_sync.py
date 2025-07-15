# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "RST_VAL",
                "type": "P",
                "val": "{DATA_W{1'b0}}",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
        ],
        "ports": [
            {
                "name": "clk_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "a",
                },
                "descr": "Clock and reset",
            },
            {
                "name": "signal_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "signal_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "signal_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "signal_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "synchronizer",
                "descr": "synchronizer bus",
                "signals": [
                    {"name": "synchronizer", "width": "DATA_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "reg1",
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "RST_VAL",
                },
                "port_params": {
                    "clk_en_rst_s": "a",
                },
                "connect": {
                    "clk_en_rst_s": "clk_rst_s",
                    "data_i": "signal_i",
                    "data_o": "synchronizer",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "reg2",
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "RST_VAL",
                },
                "port_params": {
                    "clk_en_rst_s": "a",
                },
                "connect": {
                    "clk_en_rst_s": "clk_rst_s",
                    "data_i": "synchronizer",
                    "data_o": "signal_o",
                },
            },
        ],
    }

    return attributes_dict
