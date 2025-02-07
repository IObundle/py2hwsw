# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
            # TODO: Remaining ports
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_inst",
            },
            {
                "core_name": "iob_counter",
                "instance_name": "iob_counter_inst",
            },
            # For simulation
            {
                "core_name": "iob_ram_t2p",
                "instance_name": "iob_ram_t2p_inst",
            },
        ],
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "dest_dir": "hardware/simulation/src",
            },
        ],
    }

    return attributes_dict
