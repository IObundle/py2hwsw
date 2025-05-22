# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
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
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
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
                    {"name": "single_read_rd", "width": 1},
                ],
            },
            # Regarray wires
            {
                "name": "regarray_write",
                "descr": "",
                "signals": [
                    {"name": "regarray_read_addr_rd", "width": 3},
                    {"name": "regarray_read_data_rd", "width": 4},
                ],
            },
            {
                "name": "regarray_read",
                "descr": "",
                "signals": [
                    {"name": "regarray_write_en_wr", "width": 1},
                    {"name": "regarray_write_strb_wr", "width": 16 / 8},
                    {"name": "regarray_write_addr_wr", "width": 1},
                    {"name": "regarray_write_data_wr", "width": 16},
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
                    {"name": "fifo_write_w_data", "width": 4},
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
                        "width": 1,
                        "descr": "Memory write enable",
                    },
                    {
                        "name": "fifo_write_ext_mem_w_addr_o",
                        "width": 2,
                        "descr": "Memory write address",
                    },
                    {
                        "name": "fifo_write_ext_mem_w_data_o",
                        "width": 8,
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": "fifo_write_ext_mem_r_en_o",
                        "width": 1,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "fifo_write_ext_mem_r_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "fifo_write_ext_mem_r_data_i",
                        "width": 8,
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
                    {"name": "fifo_read_r_data", "width": 16},
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
                        "width": 2,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "fifo_read_ext_mem_w_addr_o",
                        "width": 1,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "fifo_read_ext_mem_w_data_o",
                        "width": 16,
                        "descr": "Memory read data",
                    },
                    #  Read port
                    {
                        "name": "fifo_read_ext_mem_r_en_o",
                        "width": 2,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "fifo_read_ext_mem_r_addr_o",
                        "width": 1,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "fifo_read_ext_mem_r_data_i",
                        "width": 16,
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
                        "width": 1,
                        "descr": "Memory write enable",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_w_addr_o",
                        "width": 2,
                        "descr": "Memory write address",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_w_data_o",
                        "width": 8,
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": "async_fifo_write_ext_mem_r_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "async_fifo_write_ext_mem_r_en_o",
                        "width": 1,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_r_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "async_fifo_write_ext_mem_r_data_i",
                        "width": 8,
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
                        "width": 1,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_w_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_w_data_o",
                        "width": 8,
                        "descr": "Memory read data",
                    },
                    #  Read port
                    {
                        "name": "async_fifo_read_ext_mem_r_clk_o",
                        "width": 1,
                    },
                    {
                        "name": "async_fifo_read_ext_mem_r_en_o",
                        "width": 1,
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_r_addr_o",
                        "width": 2,
                        "descr": "Memory read address",
                    },
                    {
                        "name": "async_fifo_read_ext_mem_r_data_i",
                        "width": 8,
                        "descr": "Memory read data",
                    },
                ],
            },
            # NOAUTO wires
            {
                "name": "noauto_write",
                "descr": "",
                "signals": [
                    {"name": "noauto_write_valid_wr", "width": 1},
                    {"name": "noauto_write_wdata_wr", "width": 1},
                    {"name": "noauto_write_wstrb_wr", "width": 1},
                    {"name": "noauto_write_ready_wr", "width": 1},
                ],
            },
            {
                "name": "noauto_read",
                "descr": "",
                "signals": [
                    {"name": "noauto_read_valid_rd", "width": 1},
                    {"name": "noauto_read_rdata_rd", "width": 1},
                    {"name": "noauto_read_rready_rd", "width": 1},
                    {"name": "noauto_read_ready_rd", "width": 1},
                    {"name": "noauto_read_rvalid_rd", "width": 1},
                ],
            },
            # Autoclear wires
            {
                "name": "autoclear_write",
                "descr": "",
                "signals": [
                    {"name": "autoclear_write_valid_wr", "width": 1},
                    {"name": "autoclear_write_wdata_wr", "width": 1},
                    {"name": "autoclear_write_wstrb_wr", "width": 1},
                    {"name": "autoclear_write_ready_wr", "width": 1},
                ],
            },
            {
                "name": "autoclear_read",
                "descr": "",
                "signals": [
                    {"name": "autoclear_read_valid_rd", "width": 1},
                    {"name": "autoclear_read_rdata_rd", "width": 1},
                    {"name": "autoclear_read_rready_rd", "width": 1},
                    {"name": "autoclear_read_ready_rd", "width": 1},
                    {"name": "autoclear_read_rvalid_rd", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "iob_csrs",
                "instance_description": "Control/Status Registers",
                "csrs": [
                    {
                        "name": "demo_single_csrs",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "single_write",
                                "descr": "Single write register",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                            },
                            {
                                "name": "single_read",
                                "descr": "Single read register",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                            },
                        ],
                    },
                    #
                    # See commit 0fc91ac for info about regarrays
                    #
                    {
                        "name": "demo_regarrays",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "regarray_write",
                                "descr": "Write regarray with 4 registers",
                                "mode": "W",
                                "n_bits": 8,  # register width
                                "rst_val": 0,
                                "log2n_items": 2,  # log number of items in the array
                                "asym": 2,  # Internal core interface twice the size as register width
                            },
                            {
                                "name": "regarray_read",
                                "descr": "Read regarray with wires for 4 registers (no generated registers)",
                                "mode": "R",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 2,  # log number of items in the array
                                "asym": -2,  # Internal core interface half the size as register width
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
                                "descr": "Write FIFO",
                                "type": "FIFO",
                                "mode": "W",
                                "n_bits": 8,  # fifo item width
                                "rst_val": 0,
                                "log2n_items": 4,  # log number of items in the fifo
                                "asym": -2,  # Internal core interface half the size as fifo item width
                            },
                        ],
                    },
                    {
                        "name": "demo_fifo_read",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "fifo_read",
                                "descr": "Read FIFO",
                                "type": "FIFO",
                                "mode": "R",
                                "n_bits": 8,  # fifo item width
                                "rst_val": 0,
                                "log2n_items": 4,  # log number of items in the fifo
                                "asym": 2,  # Internal core interface twice the size as fifo item width
                            },
                        ],
                    },
                    {
                        "name": "demo_afifo_write",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "async_fifo_write",
                                "descr": "Asynchronous write FIFO",
                                "type": "AFIFO",
                                "mode": "W",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 4,
                            },
                        ],
                    },
                    {
                        "name": "demo_afifo_read",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "async_fifo_read",
                                "descr": "Asynchronous read FIFO",
                                "type": "AFIFO",
                                "mode": "R",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 4,
                            },
                        ],
                    },
                    # No auto
                    {
                        "name": "demo_noauto_csrs",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "noauto_write",
                                "descr": "noauto write register",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                            },
                            {
                                "name": "noauto_read",
                                "descr": "noauto read register",
                                "type": "NOAUTO",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                            },
                        ],
                    },
                    # Auto clear (also noauto)
                    {
                        "name": "demo_autoclear_csrs",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "autoclear_write",
                                "descr": "autoclear write register",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "autoclear": True,
                            },
                            {
                                "name": "autoclear_read",
                                "descr": "autoclear read register",
                                "type": "NOAUTO",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "autoclear": True,
                            },
                        ],
                    },
                    # Other supported types: "ROM", "REGFILE", "RAM", "INTERRUPT"
                ],
                "csr_if": "iob",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # 'control_if_m' port connected automatically
                    #
                    # Register interfaces
                    #
                    # Single registers
                    "single_write_o": "single_write",
                    "single_read_i": "single_read",
                    # regarray
                    "regarray_write_read_io": "regarray_write",
                    "regarray_read_write_i": "regarray_read",
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
                    # No auto
                    "noauto_write_io": "noauto_write",
                    "noauto_read_io": "noauto_read",
                    # Auto clear
                    "autoclear_write_io": "autoclear_write",
                    "autoclear_read_io": "autoclear_read",
                },
            },
        ],
    }

    return attributes_dict
