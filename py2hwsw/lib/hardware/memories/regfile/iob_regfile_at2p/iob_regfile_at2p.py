# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "subblocks": [
            {
                "core_name": "iob_sync",
                "instance_name": "iob_sync_inst",
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_e_inst",
                "port_params": {
                    "clk_en_rst_s": "cke_arst_en",
                },
            },
        ],
    }

    return attributes_dict
