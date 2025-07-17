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
                "val": "21",
                "min": "NA",
                "max": "NA",
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
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset input",
                "signals": [{"name": "rst_i"}],
            },
            {
                "name": "w_en_i",
                "descr": "Write enable input",
                "signals": [{"name": "w_en_i"}],
            },
            {
                "name": "w_data_i",
                "descr": "Write data input",
                "signals": [{"name": "w_data_i", "width": "W_DATA_W"}],
            },
            {
                "name": "w_full_o",
                "descr": "Write full output",
                "signals": [{"name": "w_full_o"}],
            },
            {
                "name": "r_en_i",
                "descr": "Read enable input",
                "signals": [{"name": "r_en_i"}],
            },
            {
                "name": "r_data_o",
                "descr": "Read data output",
                "signals": [{"name": "r_data_o", "width": "R_DATA_W"}],
            },
            {
                "name": "r_empty_o",
                "descr": "Read empty output",
                "signals": [{"name": "r_empty_o"}],
            },
            {
                "name": "level_o",
                "descr": "FIFO interface",
                "signals": [
                    {
                        "name": "level_o",
                        "width": "ADDR_W+1",
                        "descr": "FIFO level",
                    },
                ],
            },
            {
                "name": "extmem_io",
                "descr": "External memory interface",
                "signals": [
                    {
                        "name": "ext_mem_clk_o",
                        "width": 1,
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
                "instance_name": "iob_reg_inst",
            },
            {
                "core_name": "iob_counter",
                "instance_name": "iob_counter_inst",
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
                "core_name": "iob_ram_t2p",
                "instance_name": "iob_ram_t2p_inst",
                "dest_dir": "hardware/simulation/src",
            },
        ],
    }

    return attributes_dict
