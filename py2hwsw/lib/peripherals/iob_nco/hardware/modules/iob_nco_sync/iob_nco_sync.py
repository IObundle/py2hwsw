# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "PERIOD_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "Period width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable, and reset",
            },
            {
                "name": "in_clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "prefix": "in_",
                },
                "descr": "Clock, clock enable, and reset for inputs",
            },
            # Inputs
            {
                "name": "soft_reset_i",
                "descr": "System soft reset",
                "signals": [
                    {
                        "name": "soft_reset_i",
                        "width": "1",
                        "descr": "System soft reset",
                    },
                ],
            },
            {
                "name": "enable_i",
                "descr": "System enable",
                "signals": [
                    {
                        "name": "enable_i",
                        "width": "1",
                        "descr": "System enable",
                    },
                ],
            },
            {
                "name": "period_wdata_i",
                "descr": "System period data",
                "signals": [
                    {
                        "name": "period_wdata_i",
                        "width": "PERIOD_W",
                        "descr": "System period data",
                    },
                ],
            },
            {
                "name": "period_wen_i",
                "descr": "System period write enable",
                "signals": [
                    {
                        "name": "period_wen_i",
                        "width": "1",
                        "descr": "System period write enable",
                    },
                ],
            },
            # Outputs
            {
                "name": "soft_reset_o",
                "descr": "Source clock domain soft reset",
                "signals": [
                    {
                        "name": "soft_reset_o",
                        "width": "1",
                        "descr": "Source clock domain soft reset",
                    },
                ],
            },
            {
                "name": "enable_o",
                "descr": "Source clock domain enable",
                "signals": [
                    {
                        "name": "enable_o",
                        "width": "1",
                        "descr": "Source clock domain enable",
                    },
                ],
            },
            {
                "name": "period_wdata_o",
                "descr": "Source clock domain period data",
                "signals": [
                    {
                        "name": "period_wdata_o",
                        "width": "PERIOD_W",
                        "descr": "Source clock domain period data",
                    },
                ],
            },
            {
                "name": "period_wen_o",
                "descr": "Source clock domain period write enable",
                "signals": [
                    {
                        "name": "period_wen_o",
                        "width": "1",
                        "descr": "Source clock domain period write enable",
                    },
                ],
            },
        ],
        "wires": [],
        "subblocks": [],
        "snippets": [],
    }

    return attributes_dict
