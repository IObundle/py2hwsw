# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "subblocks": [
            {
                "core": "iob_rom_sp",
                "instance_name": "iob_rom_sp_inst",
            },
        ],
    }

    return attributes_dict
