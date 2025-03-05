# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_syn",
        "generate_hw": True,
        "confs": [
            # empty for now
        ],
    }

    return attributes_dict
