# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        # Note: This core currently has a manual verilog source! The generate_hw is true only because of the generated csrs subblock.
        "generate_hw": True,
        "board_list": ["iob_cyclonev_gt_dk", "iob_aes_ku040_db_g"],
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "32",
                "max": "32",
                "descr": "CPU data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                # "val": "`IOB_AXISTREAM_OUT_CSRS_ADDR_W",
                "val": "5",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "TDATA_W",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "DATA_W",
                "descr": "AXI stream data width",
            },
            {
                "name": "FIFO_ADDR_W",
                "type": "P",
                "val": "4",
                "min": "NA",
                "max": "16",
                "descr": "FIFO depth (log2)",
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
                "name": "interrupt_o",
                "descr": "Interrupt signal",
                "signals": [
                    {
                        "name": "interrupt_o",
                        "width": "1",
                        "descr": "FIFO threshold interrupt signal",
                    },
                ],
            },
            {
                "name": "axistream_io",
                "descr": "AXI Stream interface signals",
                "signals": [
                    {
                        "name": "axis_clk_i",
                        "width": "1",
                        "descr": "Clock.",
                    },
                    {
                        "name": "axis_cke_i",
                        "width": "1",
                        "descr": "Clock enable.",
                    },
                    {
                        "name": "axis_arst_i",
                        "width": "1",
                        "descr": "Aynchronous and active high reset.",
                    },
                    {
                        "name": "axis_tdata_o",
                        "width": "TDATA_W",
                        "descr": "Data.",
                    },
                    {
                        "name": "axis_tvalid_o",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "axis_tready_i",
                        "width": "1",
                        "descr": "Ready.",
                    },
                    {
                        "name": "axis_tlast_o",
                        "width": "1",
                        "descr": "Last word.",
                    },
                ],
            },
            {
                "name": "sys_axis_io",
                "descr": "System AXI Stream interface.",
                "signals": [
                    {
                        "name": "sys_tdata_i",
                        "width": "DATA_W",
                        "descr": "Data.",
                    },
                    {
                        "name": "sys_tvalid_i",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "sys_tready_o",
                        "width": "1",
                        "descr": "Ready.",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "soft_reset",
                "descr": "",
                "signals": [
                    {"name": "soft_reset_wr", "width": 1},
                ],
            },
            {
                "name": "enable",
                "descr": "",
                "signals": [
                    {"name": "enable_wr", "width": 1},
                ],
            },
            {
                "name": "data_wen_wr",
                "descr": "",
                "signals": [
                    {"name": "data_wen_wr", "width": 1},
                ],
            },
            {
                "name": "data",
                "descr": "",
                "signals": [
                    {"name": "data_valid_wr", "width": 1},
                    {"name": "data_wdata_wr", "width": 32},
                    {"name": "data_wstrb_wr", "width": 4},
                    {"name": "data_ready_wr", "width": 1},
                ],
            },
            {
                "name": "mode",
                "descr": "",
                "signals": [
                    {"name": "mode_wr", "width": 1},
                ],
            },
            {
                "name": "nwords",
                "descr": "",
                "signals": [
                    {"name": "nwords_wr", "width": "DATA_W"},
                ],
            },
            {
                "name": "fifo_full",
                "descr": "",
                "signals": [
                    {"name": "fifo_full_rd", "width": 1},
                ],
            },
            {
                "name": "fifo_empty",
                "descr": "",
                "signals": [
                    {"name": "fifo_empty_rd", "width": 1},
                ],
            },
            {
                "name": "fifo_threshold",
                "descr": "",
                "signals": [
                    {"name": "fifo_threshold_wr", "width": "FIFO_ADDR_W+1"},
                ],
            },
            {
                "name": "fifo_level",
                "descr": "",
                "signals": [
                    {"name": "fifo_level_rd", "width": "FIFO_ADDR_W+1"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "iob_csrs",
                "instance_description": "Control/Status Registers",
                "parameters": {
                    "FIFO_ADDR_W": "FIFO_ADDR_W",
                },
                "csrs": [
                    {
                        "name": "axistream",
                        "descr": "AXI Stream software accessible registers.",
                        "regs": [
                            {
                                "name": "soft_reset",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Soft reset.",
                            },
                            {
                                "name": "enable",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Enable peripheral.",
                            },
                            {
                                "name": "data",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": 32,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Data input.",
                            },
                            {
                                "name": "mode",
                                "mode": "W",
                                "n_bits": "1",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Sets the operation mode: (0) data is read using CSR; (1) data is read using system axistream interface.",
                            },
                            {
                                "name": "nwords",
                                "mode": "W",
                                "n_bits": "DATA_W",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Set the number of words (with TDATA_W bits) to be written to the FIFO.",
                            },
                        ],
                    },
                    {
                        "name": "fifo",
                        "descr": "FIFO related registers",
                        "regs": [
                            {
                                "name": "fifo_full",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Full (1), or non-full (0).",
                            },
                            {
                                "name": "fifo_empty",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Full (1), or non-full (0).",
                            },
                            {
                                "name": "fifo_threshold",
                                "mode": "W",
                                "n_bits": "FIFO_ADDR_W+1",
                                "rst_val": 8,
                                "log2n_items": 0,
                                "descr": "FIFO threshold level for interrupt signal",
                            },
                            {
                                "name": "fifo_level",
                                "mode": "R",
                                "n_bits": "FIFO_ADDR_W+1",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Current FIFO level",
                            },
                        ],
                    },
                ],
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # Register interfaces
                    "soft_reset_o": "soft_reset",
                    "enable_o": "enable",
                    "data_io": "data",
                    "mode_o": "mode",
                    "nwords_o": "nwords",
                    "fifo_full_i": "fifo_full",
                    "fifo_empty_i": "fifo_empty",
                    "fifo_threshold_o": "fifo_threshold",
                    "fifo_level_i": "fifo_level",
                },
            },
            # TODO: Connect remaining subblocks
            {
                "core_name": "iob_fifo_async",
                "instantiate": False,
            },
            {
                "core_name": "iob_sync",
                "instantiate": False,
            },
            {
                "core_name": "iob_reg",
                "instantiate": False,
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
            },
            {
                "core_name": "iob_ram_at2p",
                "instantiate": False,
            },
            {
                "core_name": "iob_counter",
                "instantiate": False,
            },
        ],
    }

    return attributes_dict
