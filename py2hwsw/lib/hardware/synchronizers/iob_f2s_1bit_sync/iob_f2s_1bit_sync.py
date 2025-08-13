# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "value_i",
                "descr": "Input value to be synchronized",
                "signals": [
                    {
                        "name": "value_i",
                        "width": "1",
                        "descr": "Input value signal",
                    },
                ],
            },
            {
                "name": "value_o",
                "descr": "Output value after synchronization",
                "signals": [
                    {
                        "name": "value_o",
                        "width": "1",
                        "descr": "Output value signal after synchronization",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "sync",
                "descr": "Internal synchronization wire",
                "signals": [
                    {
                        "name": "sync",
                        "width": "2",
                        "descr": "Internal synchronization wire for the input value",
                    },
                ],
            },
            {
                "name": "data",
                "descr": "Internal data wire",
                "signals": [
                    {
                        "name": "data",
                        "width": "2",
                        "descr": "Internal data wire for the synchronized value",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a",
                },
                "instance_name": "reg0",
                "parameters": {
                    "DATA_W": "2",
                    "RST_VAL": "1",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "arst_i:value_i",
                        ],
                    ),
                    "data_i": "data",
                    "data_o": "sync",
                },
            },
        ],
        "comb": {
            "code": """
                data = {sync[0], 1'b0};
                value_o = sync[1];
            """,
        },
    }

    return attributes_dict
