# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "Clock and reset",
            },
            {
                "name": "reg_interface_io",
                "descr": "",
                "wires": [
                    {"name": "en_i", "width": "1"},
                    {"name": "rst_i", "width": "1"},
                    {"name": "rstrb_i", "width": "1"},
                    {"name": "time_o", "width": "64"},
                ],
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
                "core_name": "iob_counter",
                "instance_name": "iob_counter_inst",
            },
        ],
    }

    return attributes_dict
