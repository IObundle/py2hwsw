# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "subblocks": [
            {
                "core_name": "iob_reg_r",
                "instance_name": "iob_reg_r_inst",
            },
        ],
    }

    return attributes_dict
