# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "a",
                },
                "descr": "Clock and reset",
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_re_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
            },
            {
                "core_name": "iob_demux",
                "instance_name": "iob_demux_inst",
            },
            {
                "core_name": "iob_mux",
                "instance_name": "iob_mux_inst",
            },
        ],
    }
    return attributes_dict
