# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
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
                "val": "16",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "STRB_WIDTH",
                "type": "D",
                "val": "(DATA_WIDTH / 8)",
                "min": "NA",
                "max": "NA",
                "descr": "Strobe bus width",
            },
            {
                "name": "ID_WIDTH",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "ID bus width",
            },
            {
                "name": "LEN_WIDTH",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "Len width",
            },
            {
                "name": "PIPELINE_OUTPUT",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
                "descr": "Extra pipeline register on output",
            },
            {
                "name": "FILE",
                "type": "P",
                "val": "none",
                "min": "NA",
                "max": "NA",
                "descr": "Name of the file to be used",
            },
            {
                "name": "FILE_SIZE",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "File size",
            },
            {
                "name": "HEX_DATA_W",
                "type": "P",
                "val": "DATA_WIDTH",
                "min": "NA",
                "max": "NA",
                "descr": "Width of hex data",
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
                "name": "axi_s",
                "signals": {
                    "type": "axi",
                    "ID_W": "ID_WIDTH",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                    "LEN_W": "LEN_WIDTH",
                },
                "descr": "AXI interface",
            },
            {
                "name": "external_mem_bus_m",
                "descr": "Port for connection to external 'iob_ram_t2p_be' memory",
                "signals": {
                    "type": "ram_t2p_be",
                    "prefix": "ext_mem_",
                    "ADDR_W": "ADDR_WIDTH - 2",
                    "DATA_W": "DATA_WIDTH",
                },
            },
        ],
    }

    return attributes_dict
