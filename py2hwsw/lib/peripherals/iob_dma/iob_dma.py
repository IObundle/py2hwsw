# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    CSR_IF = py_params_dict["csr_if"] if "csr_if" in py_params_dict else "iob"
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            # Parameters
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "32",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "5",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            # External memory interface
            {
                "name": "AXI_ADDR_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "AXI address width",
            },
            {
                "name": "AXI_LEN_W",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "8",
                "descr": "AXI len width",
            },
            {
                "name": "AXI_DATA_W",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
                "descr": "AXI data width",
            },
            {
                "name": "AXI_ID_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "AXI ID width",
            },
            {
                "name": "WLEN_W",
                "type": "P",
                "val": "12",
                "min": "1",
                "max": "AXI_ADDR_W",
                "descr": "Write length width",
            },
            {
                "name": "RLEN_W",
                "type": "P",
                "val": "12",
                "min": "1",
                "max": "AXI_ADDR_W",
                "descr": "Read length width",
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
                "descr": "Synchronous reset interface",
                "signals": [
                    {"name": "rst_i", "width": 1},
                ],
            },
            # AXIS Interfaces - without last
            {
                "name": "dma_input_io",
                "descr": "",
                "signals": [
                    {"name": "axis_in_tdata_i", "width": "AXI_DATA_W"},
                    {"name": "axis_in_tvalid_i", "width": "1"},
                    {"name": "axis_in_tready_o", "width": "1"},
                ],
            },
            {
                "name": "dma_output_io",
                "descr": "",
                "signals": [
                    {"name": "axis_out_tdata_o", "width": "AXI_DATA_W"},
                    {"name": "axis_out_tvalid_o", "width": "1"},
                    {"name": "axis_out_tready_i", "width": "1"},
                ],
            },
            # AXI Interface
            {
                "name": "axi_m",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "descr": "AXI interface",
            },
        ],
        "buses": [
            {
                "name": "receive_enabled",
                "descr": "",
                "signals": [
                    {"name": "receive_enabled", "width": 1},
                ],
            },
            {
                "name": "axis_in",
                "descr": "",
                "signals": [
                    {"name": "axis_in_tdata_i", "width": "AXI_DATA_W"},
                    {"name": "receive_valid", "width": "1"},
                    {"name": "receive_ready", "width": "1"},
                ],
            },
            {
                "name": "w_length_clk_en",
                "descr": "",
                "signals": [
                    {"name": "clk_i"},
                    {"name": "cke_i"},
                    {"name": "arst_i"},
                    {"name": "w_length_wen_wr", "width": 1},
                ],
            },
            {
                "name": "w_length_wdata",
                "descr": "",
                "signals": [
                    {"name": "w_length_wdata_wr", "width": "WLEN_W"},
                ],
            },
            {
                "name": "w_length_wdata_reg",
                "descr": "",
                "signals": [
                    {"name": "w_length_wdata_reg", "width": "WLEN_W"},
                ],
            },
            # Counter buses
            {
                "name": "counter_en_rst",
                "descr": "Enable and Synchronous reset interface",
                "signals": [
                    {
                        "name": "counter_en",
                        "width": 1,
                        "descr": "Enable input",
                    },
                    {
                        "name": "w_length_wen_wr",
                    },
                ],
            },
            {
                "name": "axis_in_cnt",
                "descr": "",
                "signals": [
                    {"name": "axis_in_cnt", "width": "WLEN_W"},
                ],
            },
            # AXIS_S_AXI_M configuration buses
            {
                "name": "config_write",
                "descr": "Configure write (AXIS in)",
                "signals": [
                    {"name": "w_addr_wr", "width": "AXI_ADDR_W"},
                    {"name": "w_length_wdata_reg"},
                    {"name": "w_start_wen_wr", "width": 1},
                    {"name": "w_burstlen_wr", "width": "(AXI_LEN_W+1)"},
                    {"name": "w_buf_level_rd", "width": "WLEN_W"},
                    {"name": "w_busy_rd", "width": 1},
                ],
            },
            {
                "name": "config_read",
                "descr": "Configure read (AXIS out)",
                "signals": [
                    {"name": "r_addr_wr", "width": "AXI_ADDR_W"},
                    {"name": "r_length_wr", "width": "WLEN_W"},
                    {"name": "r_start_wen_wr", "width": 1},
                    {"name": "r_burstlen_wr", "width": "(AXI_LEN_W+1)"},
                    {"name": "r_buf_level_rd", "width": "WLEN_W"},
                    {"name": "r_busy_rd", "width": 1},
                ],
            },
            # External memories buses
            {
                "name": "write_ext_mem",
                "descr": "External memory write buses",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "ext_mem_write_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "read_ext_mem",
                "descr": "External memory read buses",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "ext_mem_read_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            # Reg buses
            {
                "name": "w_addr",
                "descr": "",
                "signals": [
                    {"name": "w_addr_wr"},
                ],
            },
            {
                "name": "w_length",
                "descr": "",
                "signals": [
                    {"name": "w_length_valid_wr", "width": 1},
                    {"name": "w_length_wdata_wr"},
                    {"name": "w_length_wstrb_wr", "width": "WLEN_W/8"},  # Unused
                    {"name": "w_length_ready_wr", "width": 1},
                ],
            },
            {
                "name": "w_busy",
                "descr": "",
                "signals": [
                    {"name": "w_busy_rd"},
                ],
            },
            {
                "name": "w_start",
                "descr": "",
                "signals": [
                    {"name": "w_start_valid_wr", "width": 1},
                    {"name": "w_start_wdata_wr", "width": 1},
                    {"name": "w_start_wstrb_wr", "width": 1},  # Unused
                    {"name": "w_start_ready_wr", "width": 1},
                ],
            },
            {
                "name": "w_burstlen",
                "descr": "",
                "signals": [
                    {"name": "w_burstlen_wr"},
                ],
            },
            {
                "name": "w_buf_level",
                "descr": "",
                "signals": [
                    {"name": "w_buf_level_rd"},
                ],
            },
            {
                "name": "r_addr",
                "descr": "",
                "signals": [
                    {"name": "r_addr_wr"},
                ],
            },
            {
                "name": "r_length",
                "descr": "",
                "signals": [
                    {"name": "r_length_wr"},
                ],
            },
            {
                "name": "r_busy",
                "descr": "",
                "signals": [
                    {"name": "r_busy_rd"},
                ],
            },
            {
                "name": "r_start",
                "descr": "",
                "signals": [
                    {"name": "r_start_valid_wr", "width": 1},
                    {"name": "r_start_wdata_wr", "width": 1},
                    {"name": "r_start_wstrb_wr", "width": 1},  # Unused
                    {"name": "r_start_ready_wr", "width": 1},
                ],
            },
            {
                "name": "r_burstlen",
                "descr": "",
                "signals": [
                    {"name": "r_burstlen_wr"},
                ],
            },
            {
                "name": "r_buf_level",
                "descr": "",
                "signals": [
                    {"name": "r_buf_level_rd"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "iob_csrs",
                "instance_description": "Control/Status Registers",
                "autoaddr": True,
                "rw_overlap": True,
                "parameters": {
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "WLEN_W": "WLEN_W",
                    "RLEN_W": "RLEN_W",
                },
                "csrs": [
                    {
                        "name": "dma_write",
                        "descr": "DMA write software accessible registers.",
                        "regs": [
                            {
                                "name": "w_addr",
                                "mode": "W",
                                "n_bits": "AXI_ADDR_W",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA write start address.",
                            },
                            {
                                "name": "w_length",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": "WLEN_W",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA write length in words.",
                            },
                            {
                                "name": "w_busy",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA write busy: high when the DMA controller is writing data.",
                            },
                            {
                                "name": "w_start",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA write start: writing any value to this register starts the DMA write operation.",
                            },
                            {
                                "name": "w_burstlen",
                                "mode": "W",
                                "n_bits": "(AXI_LEN_W+1)",
                                "rst_val": 16,
                                "log2n_items": 0,
                                "descr": "AXI burst length for DMA write operations.",
                            },
                            {
                                "name": "w_buf_level",
                                "mode": "R",
                                "n_bits": "WLEN_W",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Number of words left in the DMA write memory buffer to be transmitted.",
                            },
                        ],
                    },
                    {
                        "name": "dma_read",
                        "descr": "DMA read software accessible registers.",
                        "regs": [
                            {
                                "name": "r_addr",
                                "mode": "W",
                                "n_bits": "AXI_ADDR_W",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA read start address.",
                            },
                            {
                                "name": "r_length",
                                "mode": "W",
                                "n_bits": "RLEN_W",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA read length in words.",
                            },
                            {
                                "name": "r_start",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA read start: writing any value to this register starts the DMA read operation.",
                            },
                            {
                                "name": "r_busy",
                                "mode": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "DMA read busy: high when the DMA controller is reading data.",
                            },
                            {
                                "name": "r_burstlen",
                                "mode": "W",
                                "n_bits": "(AXI_LEN_W+1)",
                                "rst_val": 16,
                                "log2n_items": 0,
                                "descr": "AXI burst length for DMA read operations.",
                            },
                            {
                                "name": "r_buf_level",
                                "mode": "R",
                                "n_bits": "RLEN_W",
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Number of words left in the DMA read memory buffer to be received.",
                            },
                        ],
                    },
                ],
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # 'control_if_m' port connected automatically
                    # Register interfaces
                    "w_addr_o": "w_addr",
                    "w_length_io": "w_length",
                    "w_busy_i": "w_busy",
                    "w_start_io": "w_start",
                    "w_burstlen_o": "w_burstlen",
                    "w_buf_level_i": "w_buf_level",
                    "r_addr_o": "r_addr",
                    "r_length_o": "r_length",
                    "r_busy_i": "r_busy",
                    "r_start_io": "r_start",
                    "r_burstlen_o": "r_burstlen",
                    "r_buf_level_i": "r_buf_level",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "w_length",
                "instance_description": "Write length register",
                "parameters": {
                    "DATA_W": "WLEN_W",
                    "RST_VAL": "{WLEN_W{1'd0}}",
                },
                "port_params": {"clk_en_rst_s": "c_a_e"},
                "connect": {
                    "clk_en_rst_s": "w_length_clk_en",
                    "data_i": "w_length_wdata",
                    "data_o": "w_length_wdata_reg",
                },
            },
            {
                "core_name": "iob_counter",
                "instance_name": "counter_inst",
                "instance_description": "Count number of words read via AXI Stream in",
                "parameters": {
                    "DATA_W": "WLEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "en_rst_i": "counter_en_rst",
                    "data_o": "axis_in_cnt",
                },
            },
            {
                "core_name": "iob_axis_s_axi_m",
                "instance_name": "axis_s_axi_m_inst",
                "instance_description": "AXIS to AXI",
                "parameters": {
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                    "AXI_ID_W": "AXI_ID_W",
                    "WLEN_W": "WLEN_W",
                    "RLEN_W": "RLEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst_i",
                    "config_write_io": "config_write",
                    "config_read_io": "config_read",
                    "axis_in_io": "axis_in",
                    "axis_out_io": "dma_output_io",
                    "write_ext_mem_m": "write_ext_mem",
                    "read_ext_mem_m": "read_ext_mem",
                    "axi_m": "axi_m",
                },
            },
            {
                "core_name": "iob_ram_t2p",
                "instance_name": "write_fifo_memory",
                "instance_description": "Write FIFO RAM",
                "parameters": {
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "ram_t2p_s": "write_ext_mem",
                },
            },
            {
                "core_name": "iob_ram_t2p",
                "instance_name": "read_fifo_memory",
                "instance_description": "Read FIFO RAM",
                "parameters": {
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "ram_t2p_s": "read_ext_mem",
                },
            },
        ],
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_dma_sim",
                "dest_dir": "hardware/simulation/src",
                "csr_if": CSR_IF,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    assign counter_en = axis_in_tvalid_i & axis_in_tready_o & receive_enabled;
    assign receive_enabled = axis_in_cnt != w_length_wdata_reg;
    assign receive_valid = axis_in_tvalid_i & receive_enabled;
    assign axis_in_tready_o = receive_ready & receive_enabled;

    assign w_length_ready_wr = 1'b1;
    assign w_start_ready_wr = 1'b1;
    assign r_start_ready_wr = 1'b1;

    assign w_length_wen_wr = w_length_valid_wr & w_length_ready_wr;
    assign w_start_wen_wr = w_start_valid_wr & w_start_ready_wr;
    assign r_start_wen_wr = r_start_valid_wr & r_start_ready_wr;
""",
            },
        ],
    }

    return attributes_dict
