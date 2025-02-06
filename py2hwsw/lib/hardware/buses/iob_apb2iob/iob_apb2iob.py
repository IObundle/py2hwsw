# SPDX-FileCopyrightText: 2025 IObundle
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
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "apb_s",
                "signals": {
                    "type": "apb",
                },
                "descr": "APB interface",
            },
            {
                "name": "iob_m",
                "signals": {
                    "type": "iob",
                },
                "descr": "CPU native interface",
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg_e",
                "instance_name": "iob_reg_e_inst",
            },
        ],
    }

    return attributes_dict
