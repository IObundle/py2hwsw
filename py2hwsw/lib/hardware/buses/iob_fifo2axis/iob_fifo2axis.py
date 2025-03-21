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
                "descr": "Clock, clock enable, and reset",
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
