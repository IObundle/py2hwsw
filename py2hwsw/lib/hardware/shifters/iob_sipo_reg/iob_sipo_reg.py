# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    """Serial-in parallel-out register"""

    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "NA",
                "descr": "",
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
                "name": "sdata_i",
                "descr": "Input port",
                "signals": [
                    {"name": "sdata_i"},
                ],
            },
            {
                "name": "pdata_o",
                "descr": "Output port",
                "signals": [
                    {"name": "pdata_o", "width": "DATA_W"},
                ],
            },
        ],
        "comb": {
            "code": """
    pdata_o_nxt = {pdata_o[0+:(DATA_W-1)], sdata_i};
"""
        },
    }

    return attributes_dict
