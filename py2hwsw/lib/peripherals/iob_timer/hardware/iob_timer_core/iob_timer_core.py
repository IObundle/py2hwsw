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
                "val": "32",
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
                "descr": "Clock and reset",
            },
            {
                "name": "reg_interface_io",
                "descr": "",
                "signals": [
                    {"name": "en_i", "width": "1"},
                    {"name": "rst_i", "width": "1"},
                    {"name": "rstrb_i", "width": "1"},
                    {"name": "time_o", "width": "64"},
                ],
            },
        ],
        "wires": [
            {
                "name": "rst_int",
                "descr": "Reset internal wire",
                "signals": [
                    {"name": "rst_i"},
                ],
            },
            {
                "name": "en_int",
                "descr": "Enable internal wire",
                "signals": [
                    {"name": "en_i"},
                ],
            },
            {
                "name": "rstrb_int",
                "descr": "Reset strobe internal wire",
                "signals": [
                    {"name": "rstrb_i"},
                ],
            },
            {
                "name": "time_int",
                "descr": "Time internal wire",
                "signals": [
                    {"name": "time_o"},
                ],
            },
            {
                "name": "time_counter",
                "descr": "Time counter wire",
                "signals": [
                    {"name": "time_counter", "width": "2*DATA_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "time_counter_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "parameters": {
                    "DATA_W": "2 * DATA_W",
                    "RST_VAL": "0",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i: rstrb_i",
                            "rst_i: rst_i",
                        ],
                    ),
                    "data_i": "time_counter",
                    "data_o": "time_int",
                },
            },
            {
                "core_name": "iob_counter",
                "instance_name": "time_counter_cnt",
                "parameters": {
                    "DATA_W": "2 * DATA_W",
                    "RST_VAL": "0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "counter_rst_i": "rst_int",
                    "counter_en_i": "en_int",
                    "data_o": "time_counter",
                },
            },
        ],
    }

    return attributes_dict
