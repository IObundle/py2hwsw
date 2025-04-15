# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "subblocks": [
            {
                "core_name": "iob_fp_dq",
                "instance_name": "iob_fp_dq_inst",
            },
        ],
    }

    return attributes_dict
