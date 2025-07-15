# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "ID_WIDTH",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "ID bus width",
            },
            {
                "name": "DATA_WIDTH",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_WIDTH",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "M_ADDR_WIDTH",
                "type": "P",
                "val": "{M_COUNT{{M_REGIONS{32'd24}}}}",
                "min": "NA",
                "max": "NA",
                "descr": "Manager address bus width",
            },
            {
                "name": "S_COUNT",
                "type": "P",
                "val": "4",
                "min": "NA",
                "max": "NA",
                "descr": "Number of subordinate interfaces",
            },
            {
                "name": "M_COUNT",
                "type": "P",
                "val": "4",
                "min": "NA",
                "max": "NA",
                "descr": "Number of manager interfaces",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Clock",
                "wires": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset",
                "wires": [
                    {
                        "name": "rst_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "s_axi_s",
                "wires": {
                    "type": "axi",
                    "prefix": "s_",
                    "mult": "S_COUNT",
                    "ID_W": "ID_WIDTH",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                    "LEN_W": "8",
                    "LOCK_W": 1,
                },
                "descr": "AXI subordinate interface",
            },
            {
                "name": "m_axi_m",
                "wires": {
                    "type": "axi",
                    "prefix": "m_",
                    "mult": "M_COUNT",
                    "ID_W": "ID_WIDTH",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                    "LEN_W": "8",
                    "LOCK_W": 1,
                },
                "descr": "AXI manager interface",
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_arbiter",
                "instance_name": "arbiter_inst",
            },
        ],
    }

    return attributes_dict
