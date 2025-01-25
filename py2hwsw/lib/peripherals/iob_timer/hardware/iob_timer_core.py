# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
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
        "subblocks": [
            {
                "core_name": "iob_reg_re",
                "instance_name": "iob_reg_re_inst",
            },
            {
                "core_name": "iob_counter",
                "instance_name": "iob_counter_inst",
            },
        ],
    }

    return attributes_dict
