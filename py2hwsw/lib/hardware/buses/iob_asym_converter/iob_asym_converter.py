# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {"name": "W_DATA_W", "type": "P", "val": 21, "min": 1, "max": "NA"},
            {"name": "R_DATA_W", "type": "P", "val": 21, "min": 1, "max": "NA"},
            {
                "name": "ADDR_W",
                "type": "P",
                "val": 3,
                "min": 1,
                "max": "NA",
                "descr": "higher ADDR_W lower DATA_W",
            },
            {
                "name": "BIG_ENDIAN",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 1,
                "descr": "0: little endian, 1: big endian",
            },
            # determine W_ADDR_W and R_ADDR_W
            {"name": "MAXDATA_W", "type": "D", "val": "iob_max(W_DATA_W, R_DATA_W)"},
            {"name": "MINDATA_W", "type": "D", "val": "iob_min(W_DATA_W, R_DATA_W)"},
            {"name": "R", "type": "D", "val": "MAXDATA_W / MINDATA_W"},
            {
                "name": "MINADDR_W",
                "type": "D",
                "val": "ADDR_W - $clog2(R)",
                "descr": "lower ADDR_W (higher DATA_W)",
            },
            {
                "name": "W_ADDR_W",
                "type": "D",
                "val": "(W_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
            },
            {
                "name": "R_ADDR_W",
                "type": "D",
                "val": "(R_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
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
                "name": "rst_i",
                "descr": "Synchronous reset interface",
                "wires": [
                    {
                        "name": "rst_i",
                        "width": 1,
                        "descr": "Synchronous reset input",
                    },
                ],
            },
            {
                "name": "write_i",
                "descr": "Write interface",
                "wires": [
                    {
                        "name": "w_en_i",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": "w_addr_i",
                        "width": "W_ADDR_W",
                        "descr": "Write address",
                    },
                    {
                        "name": "w_data_i",
                        "width": "W_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
            {
                "name": "read_io",
                "descr": "Read interface",
                "wires": [
                    {
                        "name": "r_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": "r_addr_i",
                        "width": "R_ADDR_W",
                        "descr": "Read address",
                    },
                    {
                        "name": "r_data_o",
                        "width": "R_DATA_W",
                        "descr": "Read data",
                    },
                ],
            },
            {
                "name": "extmem_io",
                "descr": "External memory interface",
                "wires": [
                    #  Write port
                    {
                        "name": "ext_mem_w_en_o",
                        "width": "R",
                        "descr": "Memory write enable",
                    },
                    {
                        "name": "ext_mem_w_addr_o",
                        "width": "MINADDR_W",
                        "descr": "Memory write address",
                    },
                    {
                        "name": "ext_mem_w_data_o",
                        "width": "MAXDATA_W",
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": "ext_mem_r_en_o",
                        "width": "R",
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "ext_mem_r_addr_o",
                        "width": "MINADDR_W",
                        "descr": "Memory read address",
                    },
                    {
                        "name": "ext_mem_r_data_i",
                        "width": "MAXDATA_W",
                        "descr": "Memory read data",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_r_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_re_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
            },
            {
                "core_name": "iob_functions",
                "instance_name": "iob_functions_inst",
            },
        ],
    }

    return attributes_dict
