# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


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
                "core": "iob_reg",
                "instance_name": "iob_reg_re_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
            },
            {
                "core": "iob_demux",
                "instance_name": "iob_demux_inst",
            },
            {
                "core": "iob_mux",
                "instance_name": "iob_mux_inst",
            },
        ],
    }
    return attributes_dict
