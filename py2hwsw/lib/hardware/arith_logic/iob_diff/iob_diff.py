# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data width",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "RST_VAL",
                "descr": "Reset value",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "data_i",
                "descr": "Data input",
                "signals": [
                    {
                        "name": "data_i",
                        "width": "DATA_W",
                        "descr": "Data input signal",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Data output",
                "signals": [
                    {
                        "name": "data_o",
                        "width": "DATA_W",
                        "descr": "Data output signal",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "data_i_reg",
                "descr": "Data input register wire",
                "signals": [
                    {
                        "name": "data_i_reg",
                        "width": "DATA_W",
                        "descr": "Registered data input signal",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_r_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "RST_VAL",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "data_i",
                    "data_o": "data_o",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": r"""
                assign data_o = data_i - data_i_reg;
                """
            }
        ],
    }

    return attributes_dict
