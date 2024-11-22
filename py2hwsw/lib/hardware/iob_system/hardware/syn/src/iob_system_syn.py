# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

bsp = [
    # empty for now
]


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_syn",
        "confs": bsp,
    }

    return attributes_dict
