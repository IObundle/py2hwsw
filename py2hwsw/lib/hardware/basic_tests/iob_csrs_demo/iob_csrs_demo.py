# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": True,
        "confs": [
            {
                "name": "ADDR_W",
                "type": "P",
                "val": 7,  # Same as CSRS_ADDR_W
                "min": 0,
                "max": 32,
                "descr": "Address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": 32,
                "min": 0,
                "max": 32,
                "descr": "Data bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "cbus_s",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W - 2",
                    "DATA_W": "DATA_W",
                },
                "descr": "CPU native interface",
            },
        ],
        "wires": [
            # Register wires
            {
                "name": "single_write",
                "descr": "",
                "signals": [
                    {"name": "single_write_wr", "width": 1},
                ],
            },
            {
                "name": "single_read",
                "descr": "",
                "signals": [
                    {"name": "single_read_wr", "width": 1},
                ],
            },
            # Regifiles wires
            {
                "name": "regfile_write",
                "descr": "",
                "signals": [
                    {"name": "regfile_write_0_wr", "width": 8},
                    {"name": "regfile_write_1_wr", "width": 8},
                    {"name": "regfile_write_2_wr", "width": 8},
                    {"name": "regfile_write_3_wr", "width": 8},
                    {"name": "regfile_write_raddr_wr", "width": 2},
                    {"name": "regfile_write_rdata_wr", "width": 8},
                ],
            },
            {
                "name": "regfile_read",
                "descr": "",
                "signals": [
                    {"name": "regfile_read_raddr", "width": 2},
                    {"name": "regfile_read", "width": 8},
                ],
            },
            # FIFO write wires
            {
                "name": "fifo_write_rst",
                "descr": "",
                "signals": [
                    {"name": "fifo_write_rst", "width": 1},
                ],
            },
            {
                "name": "fifo_write_read",
                "descr": "",
                "signals": [
                    {"name": "fifo_write_w_en", "width": 1},
                    {"name": "fifo_write_w_data", "width": 8},
                    {"name": "fifo_write_w_empty", "width": 1},
                ],
            },
            {
                "name": "fifo_write_extmem",
                "descr": "",
                "signals": [
                    {
                        "name": "fifo_write_ext_mem_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "fifo_write_ext_mem_w_en_o",
                        "width": 4,
                        "descr": "Memory write enable",
                    },
                    {
                        "name": "fifo_write_ext_mem_w_addr_o",
                        "width": 2,
                        "descr": "Memory write address",
                    },
                    {
                        "name": "fifo_write_ext_mem_w_data_o",
                        "width": 32,
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": "fifo_write_ext_mem_r_en_o",
                        "width": 4,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "fifo_write_ext_mem_r_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "fifo_write_ext_mem_r_data_i",
                        "width": 32,
                        "descr": "Memory read data",
                    },
                ],
            },
            {
                "name": "fifo_write_current_level",
                "descr": "",
                "signals": [
                    {"name": "fifo_write_current_level", "width": 5},
                ],
            },
            # FIFO read wires
            {
                "name": "fifo_read_rst",
                "descr": "",
                "signals": [
                    {"name": "fifo_read_rst", "width": 1},
                ],
            },
            {
                "name": "fifo_read_write",
                "descr": "",
                "signals": [
                    {"name": "fifo_read_r_en", "width": 1},
                    {"name": "fifo_read_r_data", "width": 8},
                    {"name": "fifo_read_r_full", "width": 1},
                ],
            },
            {
                "name": "fifo_read_interrupt",
                "descr": "",
                "signals": [
                    {"name": "fifo_read_interrupt", "width": 1},
                ],
            },
            {
                "name": "fifo_read_extmem",
                "descr": "",
                "signals": [
                    {
                        "name": "fifo_read_ext_mem_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "fifo_read_ext_mem_w_en_o",
                        "width": 4,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "fifo_read_ext_mem_w_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "fifo_read_ext_mem_w_data_o",
                        "width": 32,
                        "descr": "Memory read data",
                    },
                    #  Read port
                    {
                        "name": "fifo_read_ext_mem_r_en_o",
                        "width": 4,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "fifo_read_ext_mem_r_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "fifo_read_ext_mem_r_data_i",
                        "width": 32,
                        "descr": "Memory read data",
                    },
                ],
            },
            {
                "name": "fifo_read_current_level",
                "descr": "",
                "signals": [
                    {"name": "fifo_read_current_level", "width": 5},
                ],
            },
            # Async write FIFO
            {
                "name": "async_fifo_write_read",
                "descr": "Read interface",
                "signals": [
                    {
                        "name": "async_fifo_write_r_clk_i",
                        "width": 1,
                        "descr": "Read clock",
                    },
                    {
                        "name": "async_fifo_write_r_cke_i",
                        "width": 1,
                        "descr": "Read clock enable",
                    },
                    {
                        "name": "async_fifo_write_r_arst_i",
                        "width": 1,
                        "descr": "Read async reset",
                    },
                    {
                        "name": "async_fifo_write_r_rst_i",
                        "width": 1,
                        "descr": "Read sync reset",
                    },
                    {
                        "name": "async_fifo_write_r_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": "async_fifo_write_r_data_o",
                        "width": 8,
                        "descr": "Read data",
                    },
                    {
                        "name": "async_fifo_write_r_full_o",
                        "width": 1,
                        "descr": "Read full signal",
                    },
                    {
                        "name": "async_fifo_write_r_empty_o",
                        "width": 1,
                        "descr": "Read empty signal",
                    },
                    {
                        "name": "async_fifo_write_r_level_o",
                        "width": 5,
                        "descr": "Read fifo level",
                    },
                ],
            },
            {
                "name": "async_fifo_write_extmem",
                "descr": "",
                "signals": [
                    {
                        "name": "async_fifo_write_ext_mem_w_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "async_fifo_write_ext_mem_w_en_o",
                        "width": 4,
                        "descr": "Memory write enable",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_w_addr_o",
                        "width": 2,
                        "descr": "Memory write address",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_w_data_o",
                        "width": 32,
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": "async_fifo_write_ext_mem_r_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "async_fifo_write_ext_mem_r_en_o",
                        "width": 4,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_r_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_r_data_i",
                        "width": 32,
                        "descr": "Memory read data",
                    },
                ],
            },
            # Async read FIFO
            {
                "name": "async_fifo_read_write",
                "descr": "Write interface",
                "signals": [
                    {
                        "name": "async_fifo_read_w_clk_i",
                        "width": 1,
                        "descr": "Read clock",
                    },
                    {
                        "name": "async_fifo_read_w_cke_i",
                        "width": 1,
                        "descr": "Read clock enable",
                    },
                    {
                        "name": "async_fifo_read_w_arst_i",
                        "width": 1,
                        "descr": "Read async reset",
                    },
                    {
                        "name": "async_fifo_read_w_rst_i",
                        "width": 1,
                        "descr": "Read sync reset",
                    },
                    {
                        "name": "async_fifo_read_w_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": "async_fifo_read_w_data_o",
                        "width": 8,
                        "descr": "Read data",
                    },
                    {
                        "name": "async_fifo_read_w_full_o",
                        "width": 1,
                        "descr": "Read full signal",
                    },
                    {
                        "name": "async_fifo_read_w_empty_o",
                        "width": 1,
                        "descr": "Read empty signal",
                    },
                    {
                        "name": "async_fifo_read_w_level_o",
                        "width": 5,
                        "descr": "Read fifo level",
                    },
                ],
            },
            {
                "name": "async_fifo_read_extmem",
                "descr": "",
                "signals": [
                    {
                        "name": "async_fifo_read_ext_mem_w_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "async_fifo_read_ext_mem_w_en_o",
                        "width": 4,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_w_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_w_data_o",
                        "width": 32,
                        "descr": "Memory read data",
                    },
                    #  Read port
                    {
                        "name": "async_fifo_read_ext_mem_r_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "async_fifo_read_ext_mem_r_en_o",
                        "width": 4,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_r_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_r_data_i",
                        "width": 32,
                        "descr": "Memory read data",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "csrs_inst",
                "instance_description": "Control/Status Registers",
                "csrs": [
                    {
                        "name": "demo_single_csrs",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "single_write",
                                "type": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Single write register",
                            },
                            {
                                "name": "single_read",
                                "type": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Single read register",
                            },
                        ],
                    },
                    #
                    # See commit 0fc91ac for info about regfiles
                    #
                    {
                        "name": "demo_regfiles",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "regfile_write",
                                "type": "W",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 2,
                                "autoreg": True,
                                "descr": "Write regfile with 4 registers",
                            },
                            {
                                "name": "regfile_read",
                                "type": "R",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 2,
                                "autoreg": True,
                                "descr": "Read regfile with wires for 4 registers (no generated registers)",
                            },
                        ],
                    },
                    #
                    # See commit 925e7ad for info about FIFOs
                    #
                    {
                        "name": "demo_fifo_write",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "fifo_write",
                                "type": "FIFO_W",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 4,
                                "autoreg": True,
                                "descr": "Write FIFO",
                            },
                        ],
                    },
                    {
                        "name": "demo_fifo_read",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "fifo_read",
                                "type": "FIFO_R",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 4,
                                "autoreg": True,
                                "descr": "Read FIFO",
                            },
                        ],
                    },
                    {
                        "name": "demo_afifo_write",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "async_fifo_write",
                                "type": "AFIFO_W",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 4,
                                "autoreg": True,
                                "descr": "Asynchronous write FIFO",
                            },
                        ],
                    },
                    {
                        "name": "demo_afifo_read",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "async_fifo_read",
                                "type": "AFIFO_R",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 4,
                                "autoreg": True,
                                "descr": "Asynchronous read FIFO",
                            },
                        ],
                    },
                ],
                "csr_if": "iob",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "control_if_s": "cbus_s",
                    #
                    # Register interfaces
                    #
                    # Single registers
                    "single_write_o": "single_write",
                    "single_read_i": "single_read",
                    # Regfile
                    "regfile_write_io": "regfile_write",
                    "regfile_read_io": "regfile_read",
                    # FIFO write
                    "fifo_write_rst_i": "fifo_write_rst",
                    "fifo_write_read_io": "fifo_write_read",
                    "fifo_write_extmem_io": "fifo_write_extmem",
                    "fifo_write_current_level_o": "fifo_write_current_level",
                    # FIFO read
                    "fifo_read_rst_i": "fifo_read_rst",
                    "fifo_read_write_io": "fifo_read_write",
                    "fifo_read_interrupt_o": "fifo_read_interrupt",
                    "fifo_read_extmem_io": "fifo_read_extmem",
                    "fifo_read_current_level_o": "fifo_read_current_level",
                    # Async FIFO write
                    "async_fifo_write_read_io": "async_fifo_write_read",
                    "async_fifo_write_extmem_io": "async_fifo_write_extmem",
                    # Async FIFO read
                    "async_fifo_read_write_io": "async_fifo_read_write",
                    "async_fifo_read_extmem_io": "async_fifo_read_extmem",
                },
            },
        ],
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "dest_dir": "hardware/simulation/src",
            },
        ],
    }

    return attributes_dict
