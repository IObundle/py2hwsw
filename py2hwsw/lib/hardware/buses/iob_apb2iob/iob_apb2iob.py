# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "APB_ADDR_W",
                "type": "P",
                "val": 21,
                "min": 1,
                "max": 32,
                "descr": "APB address bus width in bits",
            },
            {
                "name": "APB_DATA_W",
                "type": "P",
                "val": 21,
                "min": 1,
                "max": 32,
                "descr": "APB data bus width in bits",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "APB_ADDR_W",
                "min": 1,
                "max": 32,
                "descr": "IOb address bus width in bits",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "APB_DATA_W",
                "min": 1,
                "max": 32,
                "descr": "IOb data bus width in bits",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "apb_s",
                "wires": {
                    "type": "apb",
                    "ADDR_W": "APB_ADDR_W",
                    "DATA_W": "APB_DATA_W",
                },
                "descr": "APB interface",
            },
            {
                "name": "iob_m",
                "wires": {
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
