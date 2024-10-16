# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
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
                "descr": "Master address bus width",
            },
            {
                "name": "S_COUNT",
                "type": "P",
                "val": "4",
                "min": "NA",
                "max": "NA",
                "descr": "Number of slave interfaces",
            },
            {
                "name": "M_COUNT",
                "type": "P",
                "val": "4",
                "min": "NA",
                "max": "NA",
                "descr": "Number of master interfaces",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Clock",
                "signals": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset",
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "s_axi_s",
                "interface": {
                    "type": "axi",
                    "subtype": "slave",
                    "prefix": "s_",
                    "mult": "S_COUNT",
                    "ID_W": "ID_WIDTH",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                    "LEN_W": "8",
                    "LOCK_W": 1,
                },
                "descr": "AXI slave interface",
                "signals": [
                    {"name": "s_axi_awuser_i", "width": "S_COUNT"},
                    {"name": "s_axi_wuser_i", "width": "S_COUNT"},
                    {"name": "s_axi_aruser_i", "width": "S_COUNT"},
                ],
            },
            {
                "name": "m_axi_m",
                "interface": {
                    "type": "axi",
                    "subtype": "master",
                    "prefix": "m_",
                    "mult": "M_COUNT",
                    "ID_W": "ID_WIDTH",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                    "LEN_W": "8",
                    "LOCK_W": 1,
                },
                "descr": "AXI master interface",
                "signals": [
                    {"name": "m_axi_buser_i", "width": "M_COUNT"},
                    {"name": "m_axi_ruser_i", "width": "M_COUNT"},
                ],
            },
        ],
        "blocks": [
            {
                "core_name": "iob_arbiter",
                "instance_name": "arbiter_inst",
            },
        ],
    }

    return attributes_dict
