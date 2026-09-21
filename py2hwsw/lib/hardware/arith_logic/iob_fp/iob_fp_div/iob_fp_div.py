# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "subblocks": [
            {
                "core": "iob_fp_special",
                "instance_name": "iob_fp_special_inst",
            },
            {
                "core": "iob_div_subshift",
                "instance_name": "iob_div_subshift_inst",
            },
            {
                "core": "iob_fp_clz",
                "instance_name": "iob_fp_clz_inst",
            },
            {
                "core": "iob_fp_round",
                "instance_name": "iob_fp_round_inst",
            },
        ],
    }

    return attributes_dict
