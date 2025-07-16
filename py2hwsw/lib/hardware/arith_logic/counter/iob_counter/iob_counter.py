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
                "min": "1",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "RST_VAL",
                "type": "P",
                "val": "{DATA_W{1'b0}}",
                "min": "0",
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
                "name": "counter_rst_i",
                "descr": "Counter reset input",
                "signals": [{"name": "counter_rst_i"}],
            },
            {
                "name": "counter_en_i",
                "descr": "Counter enable input",
                "signals": [{"name": "counter_en_i"}],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "signals": [{"name": "data_o", "width": "DATA_W"}],
            },
        ],
        "wires": [
            {
                "name": "data_int",
                "descr": "data_int wire",
                "signals": [
                    {"name": "data_int", "width": "DATA_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "reg0",
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "RST_VAL",
                },
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i:counter_en_i",
                            "rst_i:counter_rst_i",
                        ],
                    ),
                    "data_i": "data_int",
                    "data_o": "data_o",
                },
            },
        ],
        "comb": {
            "code": """
        data_int = data_o + 1'b1;
        """,
        },
    }

    return attributes_dict
