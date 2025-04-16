# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


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
            {
                "name": "axil_s",
                "signals": {
                    "type": "axil",
                    "ADDR_W": "AXIL_ADDR_W",
                    "DATA_W": "AXIL_DATA_W",
                },
                "descr": "AXIL interface",
            },
            {
                "name": "iob_m",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "CPU native interface",
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_e_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_e",
                },
            },
        ],
    }

    return attributes_dict
