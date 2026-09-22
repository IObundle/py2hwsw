# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            # TODO: Remaining ports
        ],
        "subblocks": [
            {
                "core": "iob_reg",
                "instance_name": "iob_reg_inst",
            },
            {
                "core": "iob_counter",
                "instance_name": "iob_counter_inst",
            },
            # For simulation
            {
                "core": "iob_ram_t2p",
                "instance_name": "iob_ram_t2p_inst",
            },
        ],
    }

    return attributes_dict
