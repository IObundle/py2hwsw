# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "rst_i",
                "descr": "",
                "signals": [
                    {"name": "rst_i", "width": 1},
                ],
            },
            {
                "name": "bit_i",
                "descr": "",
                "signals": [
                    {"name": "bit_i", "width": 1},
                ],
            },
            {
                "name": "detected_o",
                "descr": "",
                "signals": [
                    {"name": "detected_o", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg_r",
                "instance_name": "iob_reg_r_inst",
            },
        ],
    }

    return attributes_dict
