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
        ],
        "subblocks": [
            {
                "core_name": "iob_ctls",
                "instance_name": "iob_ctls_inst",
            },
        ],
    }

    return attributes_dict
