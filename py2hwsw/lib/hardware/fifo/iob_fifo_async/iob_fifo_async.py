# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "W_DATA_W",
                "descr": "Write data width",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "R_DATA_W",
                "descr": "Read data width",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "ADDR_W",
                "descr": "Higher ADDR_W (lower DATA_W)",
                "type": "P",
                "val": "3",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "BIG_ENDIAN",
                "descr": "Big-endian mode: 1 for big-endian, 0 for little-endian",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "1",
            },
            {
                "name": "MAXDATA_W",
                "descr": "Computed maximum data width",
                "type": "D",
                "val": "iob_max(W_DATA_W, R_DATA_W)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "MINDATA_W",
                "descr": "Computed minimum data width",
                "type": "D",
                "val": "iob_min(W_DATA_W, R_DATA_W)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "R",
                "descr": "Computed ratio between maximum and minimum data widths",
                "type": "D",
                "val": "MAXDATA_W / MINDATA_W",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "MINADDR_W",
                "descr": "Lower ADDR_W (higher DATA_W)",
                "type": "D",
                "val": "ADDR_W - $clog2(R)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "W_ADDR_W",
                "descr": "Computed write address width",
                "type": "D",
                "val": "(W_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "R_ADDR_W",
                "descr": "Computed read address width",
                "type": "D",
                "val": "(R_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
                "min": "NA",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "w_clk_en_rst_s",
                "descr": "Write clock, clock enable and async reset",
                "signals": {
                    "type": "iob_clk",
                    "prefix": "w_",
                },
            },
            {
                "name": "w_rst_i",
                "descr": "Write sync reset",
                "signals": [{"name": "w_rst_i"}],
            },
            {
                "name": "w_en_i",
                "descr": "Write enable",
                "signals": [{"name": "w_en_i"}],
            },
            {
                "name": "w_data_i",
                "descr": "Write data",
                "signals": [{"name": "w_data_i", "width": "W_DATA_W"}],
            },
            {
                "name": "w_full_o",
                "descr": "Write full signal",
                "signals": [{"name": "w_full_o"}],
            },
            {
                "name": "w_empty_o",
                "descr": "Write empty signal",
                "signals": [{"name": "w_empty_o"}],
            },
            {
                "name": "w_level_o",
                "descr": "Write FIFO level",
                "signals": [{"name": "w_level_o", "width": "ADDR_W+1"}],
            },
            {
                "name": "r_clk_en_rst_s",
                "descr": "Read clock, clock enable and async reset",
                "signals": {
                    "type": "iob_clk",
                    "prefix": "r_",
                },
            },
            {
                "name": "r_rst_i",
                "descr": "Read sync reset",
                "signals": [{"name": "r_rst_i"}],
            },
            {
                "name": "r_en_i",
                "descr": "Read enable",
                "signals": [{"name": "r_en_i"}],
            },
            {
                "name": "r_data_o",
                "descr": "Read data",
                "signals": [{"name": "r_data_o", "width": "R_DATA_W"}],
            },
            {
                "name": "r_full_o",
                "descr": "Read full signal",
                "signals": [{"name": "r_full_o"}],
            },
            {
                "name": "r_empty_o",
                "descr": "Read empty signal",
                "signals": [{"name": "r_empty_o"}],
            },
            {
                "name": "r_level_o",
                "descr": "Read fifo level",
                "signals": [{"name": "r_level_o", "width": "ADDR_W+1"}],
            },
            {
                "name": "extmem_io",
                "descr": "External memory interface",
                "signals": [
                    #  Write port
                    {
                        "name": "ext_mem_w_clk_o",
                        "width": 1,
                        "descr": "Memory clock",
                    },
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
                        "name": "ext_mem_r_clk_o",
                        "width": 1,
                        "descr": "Memory clock",
                    },
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
                "core_name": "iob_gray_counter",
                "instance_name": "iob_gray_counter_inst",
            },
            {
                "core_name": "iob_gray2bin",
                "instance_name": "iob_gray2bin_inst",
            },
            {
                "core_name": "iob_sync",
                "instance_name": "iob_sync_inst",
            },
            {
                "core_name": "iob_asym_converter",
                "instance_name": "iob_asym_converter_inst",
            },
            {
                "core_name": "iob_functions",
                "instance_name": "iob_functions_inst",
            },
            # For simulation
            {
                "core_name": "iob_ram_at2p",
                "instance_name": "iob_ram_at2p_inst",
                "dest_dir": "hardware/simulation/src",
            },
            {
                "core_name": "iob_clock",
                "instance_name": "iob_clock_inst",
                "dest_dir": "hardware/simulation/src",
            },
        ],
    }

    return attributes_dict
