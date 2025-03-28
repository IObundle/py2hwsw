# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    # Confs List
    confs = [
        {
            "name": "ADDR_W",
            "descr": "",
            "type": "P",
            "val": "0",
            "min": "0",
            "max": "32",
        },
        {
            "name": "DATA_W",
            "descr": "",
            "type": "P",
            "val": "32",
            "min": "1",
            "max": "32",
        },
        # AXI parameters
        {
            "name": "AXI_ADDR_W",
            "descr": "AXI address bus width",
            "type": "F",
            "val": "ADDR_W",
            "min": "1",
            "max": "32",
        },
        {
            "name": "AXI_LEN_W",
            "descr": "AXI burst length width",
            "type": "P",
            "val": "4",
            "min": "1",
            "max": "4",
        },
        {
            "name": "AXI_DATA_W",
            "descr": "AXI data bus width",
            "type": "F",
            "val": "DATA_W",
            "min": "1",
            "max": "32",
        },
        {
            "name": "AXI_ID_W",
            "descr": "AXI ID bus width",
            "type": "P",
            "val": "0",
            "min": "0",
            "max": "32",
        },
    ]

    # Ports List
    ports = [
        {
            "name": "clk_en_rst_s",
            "signals": {
                "type": "iob_clk",
            },
            "descr": "Clock, clock enable and reset",
        },
        {
            "name": "iob_s",
            "descr": "Subordinate IOb interface",
            "signals": {
                "type": "iob",
                "ADDR_W": "ADDR_W",
                "DATA_W": "DATA_W",
            },
        },
        {
            "name": "axi_m",
            "descr": "Manager AXI interface",
            "signals": {
                "type": "axi",
                "prefix": "m_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
            },
        },
        {
            "name": "control_io",
            "descr": "Control interface",
            "signals": {
                {
                    "name": "length_i",
                    "width": "AXI_LEN_W",
                    "descr": "Burst length minus 1",
                },
                {
                    "name": "w_level_o",
                    "width": "AXI_LEN_W",
                    "descr": "Write FIFO level",
                },
                {
                    "name": "r_level_o",
                    "width": "AXI_LEN_W",
                    "descr": "Read FIFO level",
                },
            },
        },
        {
            "name": "write_fifo_ext_mem_m",
            "descr": "External memory interface for write fifo",
            "signals": {"type": "ram_t2p", "prefix": "write_fifo_"},
        },
        {
            "name": "read_fifo_ext_mem_m",
            "descr": "External memory interface for read fifo",
            "signals": {"type": "ram_t2p", "prefix": "read_fifo_"},
        },
    ]

    # Subblocks List
    subblocks = [
        {
            "core_name": "iob_iob2axi_write",
            "instance_name": "iob2axi_write",
            "instance_description": "IOB to AXI write",
            "parameters": {
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_DATA_W": "AXI_DATA_W",
                "AXI_ID_W": "AXI_ID_W",
            },
        },
        {
            "core_name": "iob_iob2axi_read",
            "instance_name": "iob2axi_read",
            "instance_description": "IOB to AXI read",
            "parameters": {
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_DATA_W": "AXI_DATA_W",
                "AXI_ID_W": "AXI_ID_W",
            },
        },
    ]

    attributes_dict = {
        "generate_hw": True,
        "confs": confs,
        "ports": ports,
        "subblocks": subblocks,
    }

    return attributes_dict
