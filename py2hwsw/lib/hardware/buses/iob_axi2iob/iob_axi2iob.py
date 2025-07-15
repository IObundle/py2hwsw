# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "ADDR_WIDTH",
                "descr": "",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "DATA_WIDTH",
                "descr": "",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "STRB_WIDTH",
                "descr": "",
                "type": "P",
                "val": "(DATA_WIDTH / 8)",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_ID_WIDTH",
                "descr": "",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "32",
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
                "name": "axi_s",
                "descr": "Subordinate AXI interface",
                "wires": {
                    "type": "axi",
                    "prefix": "s_",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
            },
            {
                "name": "iob_m",
                "descr": "Manager IOb interface",
                "wires": {
                    "type": "iob",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
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
        ],
    }

    return attributes_dict
