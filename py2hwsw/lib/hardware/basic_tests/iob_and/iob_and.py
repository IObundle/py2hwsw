# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "confs": [
            {
                "name": "general",
                "descr": "General group of confs",
                "confs": [
                    {
                        "name": "W",
                        "type": "P",
                        "val": "21",
                        "min": "1",
                        "max": "32",
                        "descr": "IO width",
                    },
                ],
            },
        ],
        "ports": [
            {
                "name": "a_i",
                "descr": "Input port",
                "signals": [
                    {"name": "a_i", "width": "W"},
                ],
            },
            {
                "name": "b_i",
                "descr": "Input port",
                "signals": [
                    {"name": "b_i", "width": "W"},
                ],
            },
            {
                "name": "y_o",
                "descr": "Output port",
                "signals": [
                    {"name": "y_o", "width": "W"},
                ],
            },
        ],
        "blocks": [
            {
                "name": "simulation",
                "descr": "Blocks for simulation",
                "blocks": [
                    # Simulation wrapper
                    {
                        "core_name": "iob_sim",
                        "instance_name": "iob_sim",
                        "instantiate": False,
                        "dest_dir": "hardware/simulation/src",
                    },
                ],
            },
        ],
        "snippets": [{"verilog_code": "   assign y_o = a_i & b_i;"}],
    }

    return attributes_dict
