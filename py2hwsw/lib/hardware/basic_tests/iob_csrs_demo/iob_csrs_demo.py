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
            {
                "name": "REG_ITEMS_W",
                "type": "P",
                "val": 4,
                "min": 0,
                "max": 8,
                "descr": "Log2 Number of Items in Reg Array",
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
            {
                "name": "single_read_write",
                "descr": "",
                "signals": [
                    {"name": "single_read_write_wrrd_o", "width": 1},
                    {"name": "single_read_write_wrrd_i", "width": 1},
                    {"name": "single_read_write_wrrd_wstrb", "width": 1},
                ],
            },
            {
                "name": "multi_read_write",
                "descr": "",
                "signals": [
                    {"name": "multi_read_write_wrrd_o", "width": 23},
                    {"name": "multi_read_write_wrrd_i", "width": 23},
                    {"name": "multi_read_write_wrrd_wstrb", "width": 3},
                ],
            },
            # Regarray wires
            {
                "name": "regarray_write",
                "descr": "",
                "signals": [
                    {"name": "regarray_read_en_rd", "width": 1},
                    {"name": "regarray_read_addr_rd", "width": 3},
                    {"name": "regarray_read_data_rd", "width": 8},
                    {"name": "regarray_read_ready_rd", "width": 1},
                ],
            },
            {
                "name": "regarray_read",
                "descr": "",
                "signals": [
                    {"name": "regarray_write_en_wr", "width": 1},
                    {"name": "regarray_write_strb_wr", "width": int(32 / 8)},
                    {"name": "regarray_write_addr_wr", "width": 1},
                    {"name": "regarray_write_data_wr", "width": 32},
                    {"name": "regarray_write_ready_wr", "width": 1},
                ],
            },
            {
                "name": "regarray_rw_r",
                "descr": "",
                "signals": [
                    {"name": "regarray_read_write_en_rd", "width": 1},
                    {"name": "regarray_read_write_addr_rd", "width": 3},
                    {"name": "regarray_read_write_data_rd", "width": 16},
                    {"name": "regarray_read_write_ready_rd", "width": 1},
                ],
            },
            {
                "name": "regarray_rw_w",
                "descr": "",
                "signals": [
                    {"name": "regarray_read_write_en_wr", "width": 1},
                    {"name": "regarray_read_write_strb_wr", "width": int(16 / 8)},
                    {"name": "regarray_read_write_addr_wr", "width": 1},
                    {"name": "regarray_read_write_data_wr", "width": 16},
                    {"name": "regarray_read_write_ready_wr", "width": 1},
                ],
            },
            {
                "name": "regarray_param_rw_r",
                "descr": "",
                "signals": [
                    {"name": "regarray_read_write_param_en_rd", "width": 1},
                    {"name": "regarray_read_write_param_addr_rd", "width": 3},
                    {"name": "regarray_read_write_param_data_rd", "width": 16},
                    {"name": "regarray_read_write_param_ready_rd", "width": 1},
                ],
            },
            {
                "name": "regarray_param_rw_w",
                "descr": "",
                "signals": [
                    {"name": "regarray_read_write_param_en_wr", "width": 1},
                    {"name": "regarray_read_write_param_strb_wr", "width": int(16 / 8)},
                    {"name": "regarray_read_write_param_addr_wr", "width": 1},
                    {"name": "regarray_read_write_param_data_wr", "width": 16},
                    {"name": "regarray_read_write_param_ready_wr", "width": 1},
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
                "name": "async_fifo_write_r_clk_en_rst",
                "descr": "Read clock, clock enable and async reset",
                "signals": [
                    {"name": "async_fifo_write_r_clk_i"},
                    {"name": "async_fifo_write_r_cke_i"},
                    {"name": "async_fifo_write_r_arst_i"},
                ],
            },
            {
                "name": "async_fifo_write_r_rst_i",
                "descr": "Read sync reset",
                "signals": [
                    {"name": "async_fifo_write_r_rst_i"},
                ],
            },
            {
                "name": "async_fifo_write_r_en_i",
                "descr": "Read enable",
                "signals": [
                    {"name": "async_fifo_write_r_en_i"},
                ],
            },
            {
                "name": "async_fifo_write_r_data_o",
                "descr": "Read data",
                "signals": [
                    {"name": "async_fifo_write_r_data_o", "width": 8},
                ],
            },
            {
                "name": "async_fifo_write_r_full_o",
                "descr": "Read full signal",
                "signals": [
                    {"name": "async_fifo_write_r_full_o"},
                ],
            },
            {
                "name": "async_fifo_write_r_empty_o",
                "descr": "Read empty signal",
                "signals": [
                    {"name": "async_fifo_write_r_empty_o"},
                ],
            },
            {
                "name": "async_fifo_write_r_level_o",
                "descr": "Read fifo level",
                "signals": [
                    {"name": "async_fifo_write_r_level_o", "width": 5},
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
                "name": "async_fifo_read_r_clk_en_rst",
                "descr": "Read clock, clock enable and async reset",
                "signals": [
                    {"name": "async_fifo_read_w_clk_i"},
                    {"name": "async_fifo_read_w_cke_i"},
                    {"name": "async_fifo_read_w_arst_i"},
                ],
            },
            {
                "name": "async_fifo_read_w_rst_i",
                "descr": "Read sync reset",
                "signals": [
                    {"name": "async_fifo_read_w_rst_i"},
                ],
            },
            {
                "name": "async_fifo_read_w_en_i",
                "descr": "Read enable",
                "signals": [
                    {"name": "async_fifo_read_w_en_i"},
                ],
            },
            {
                "name": "async_fifo_read_w_data_i",
                "descr": "Read data",
                "signals": [
                    {"name": "async_fifo_read_w_data_i", "width": 8},
                ],
            },
            {
                "name": "async_fifo_read_w_full_o",
                "descr": "Read full signal",
                "signals": [
                    {"name": "async_fifo_read_w_full_o"},
                ],
            },
            {
                "name": "async_fifo_read_w_empty_o",
                "descr": "Read empty signal",
                "signals": [
                    {"name": "async_fifo_read_w_empty_o"},
                ],
            },
            {
                "name": "async_fifo_read_w_level_o",
                "descr": "Read fifo level",
                "signals": [
                    {"name": "async_fifo_read_w_level_o", "width": 5},
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
                    {"name": "noauto_read_ready_rd", "width": 1},
                    {"name": "noauto_read_rvalid_rd", "width": 1},
                ],
            },
            {
                "name": "noauto_read_write",
                "descr": "",
                "signals": [
                    {"name": "noauto_read_write_valid_wrrd", "width": 1},
                    {"name": "noauto_read_write_wdata_wrrd", "width": 1},
                    {"name": "noauto_read_write_wstrb_wrrd", "width": 1},
                    {"name": "noauto_read_write_ready_wrrd", "width": 1},
                    {"name": "noauto_read_write_rdata_wrrd", "width": 1},
                    {"name": "noauto_read_write_rvalid_wrrd", "width": 1},
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
                    {"name": "autoclear_read_ready_rd", "width": 1},
                    {"name": "autoclear_read_rvalid_rd", "width": 1},
                ],
            },
            # Interrupts wires
            {
                "name": "demo_interrupt_status",
                "descr": "",
                "signals": [
                    {"name": "demo_interrupt_status_rd", "width": 32},
                ],
            },
            {
                "name": "demo_interrupt_mask",
                "descr": "",
                "signals": [
                    {"name": "demo_interrupt_mask_wr", "width": 32},
                ],
            },
            {
                "name": "demo_interrupt_clear",
                "descr": "",
                "signals": [
                    {"name": "demo_interrupt_clear_wr", "width": 32},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "iob_csrs",
                "instance_description": "Control/Status Registers",
                "csrs": [
                    # Single registers
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
                                # "asym": 2,  # Currently single registers do not support asym.
                            },
                            {
                                "name": "single_read",
                                "descr": "Single read register",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                            },
                            {
                                "name": "single_read_write",
                                "descr": "Single read write register",
                                "mode": "RW",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                            },
                            {
                                "name": "multi_read_write",
                                "descr": "multi read write register",
                                "mode": "RW",
                                "n_bits": 23,
                                "rst_val": 0,
                                "log2n_items": 0,
                            },
                        ],
                    },
                    # Reg arrays
                    {
                        "name": "demo_regarrays",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "regarray_write",
                                "descr": "Write regarray with 4 registers",
                                "mode": "W",
                                "n_bits": 16,  # register width
                                "rst_val": 0,
                                "log2n_items": 2,  # log number of items in the array
                                "asym": 2,  # Internal core interface twice the size as register width
                            },
                            {
                                "name": "regarray_read",
                                "descr": "Read regarray with 4 registers",
                                "mode": "R",
                                "n_bits": 16,
                                "rst_val": 0,
                                "log2n_items": 2,  # log number of items in the array
                                "asym": -2,  # Internal core interface half the size as register width
                            },
                            {
                                "name": "regarray_read_write",
                                "descr": "Read-Write regarray with 4 registers",
                                "mode": "RW",
                                "n_bits": 16,
                                "rst_val": 0,
                                "log2n_items": 2,  # log number of items in the array
                            },
                            {
                                "name": "regarray_read_write_param",
                                "descr": "Read-Write regarray with 4 registers",
                                "mode": "RW",
                                "n_bits": 16,
                                "rst_val": 0,
                                "log2n_items": "REG_ITEMS_W",  # log number of items in the array
                            },
                        ],
                    },
                    # FIFO
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
                    # Currently, RW FIFOs are not supported.
                    # {
                    #     "name": "demo_fifo_read_write",
                    #     "descr": "demo software accessible registers.",
                    #     "regs": [
                    #         {
                    #             "name": "fifo_read_write",
                    #             "descr": "Read-Write FIFO",
                    #             "type": "FIFO",
                    #             "mode": "RW",
                    #             "n_bits": 8,  # fifo item width
                    #             "rst_val": 0,
                    #             "log2n_items": 4,  # log number of items in the fifo
                    #         },
                    #     ],
                    # },
                    # Asynchronous FIFO
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
                            {
                                "name": "noauto_read_write",
                                "descr": "noauto read-write register",
                                "type": "NOAUTO",
                                "mode": "RW",
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
                    # Interrupts
                    {
                        "name": "demo_interrupt_csrs",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "demo_interrupt",
                                "descr": "This CSR will be replaced by common interrupt CSRs: status, mask, and clear",
                                "type": "INTERRUPT",
                            },
                        ],
                    },
                    # Other supported types: "ROM", "REGFILE", "RAM"
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
                    "single_read_write_io": "single_read_write",
                    "multi_read_write_io": "multi_read_write",
                    # regarray
                    "regarray_write_read_io": "regarray_write",
                    "regarray_read_write_io": "regarray_read",
                    "regarray_read_write_read_io": "regarray_rw_r",
                    "regarray_read_write_write_io": "regarray_rw_w",
                    "regarray_read_write_param_read_io": "regarray_param_rw_r",
                    "regarray_read_write_param_write_io": "regarray_param_rw_w",
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
                    "async_fifo_write_r_clk_en_rst_s": "async_fifo_write_r_clk_en_rst",
                    "async_fifo_write_r_rst_i": "async_fifo_write_r_rst_i",
                    "async_fifo_write_r_en_i": "async_fifo_write_r_en_i",
                    "async_fifo_write_r_data_o": "async_fifo_write_r_data_o",
                    "async_fifo_write_r_full_o": "async_fifo_write_r_full_o",
                    "async_fifo_write_r_empty_o": "async_fifo_write_r_empty_o",
                    "async_fifo_write_r_level_o": "async_fifo_write_r_level_o",
                    "async_fifo_write_extmem_io": "async_fifo_write_extmem",
                    # Async FIFO read
                    "async_fifo_read_w_clk_en_rst_s": "async_fifo_read_w_clk_en_rst",
                    "async_fifo_read_w_rst_i": "async_fifo_read_w_rst_i",
                    "async_fifo_read_w_en_i": "async_fifo_read_w_en_i",
                    "async_fifo_read_w_data_i": "async_fifo_read_w_data_i",
                    "async_fifo_read_w_full_o": "async_fifo_read_w_full_o",
                    "async_fifo_read_w_empty_o": "async_fifo_read_w_empty_o",
                    "async_fifo_read_w_level_o": "async_fifo_read_w_level_o",
                    "async_fifo_read_extmem_io": "async_fifo_read_extmem",
                    # No auto
                    "noauto_write_io": "noauto_write",
                    "noauto_read_io": "noauto_read",
                    "noauto_read_write_io": "noauto_read_write",
                    # Auto clear
                    "autoclear_write_io": "autoclear_write",
                    "autoclear_read_io": "autoclear_read",
                    # Interrupts
                    "demo_interrupt_status_i": "demo_interrupt_status",
                    "demo_interrupt_mask_o": "demo_interrupt_mask",
                    "demo_interrupt_clear_o": "demo_interrupt_clear",
                },
            },
        ],
    }

    return attributes_dict
