# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
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
        "wires": [
            {
                "name": "r_raddr_bin",
                "descr": "Read address in binary format",
                "signals": [
                    {
                        "name": "r_raddr_bin",
                        "width": "R_ADDR_W+1",
                        "descr": "Read address in binary format wire",
                    },
                ],
            },
            {
                "name": "w_raddr_bin",
                "descr": "Write address in binary format",
                "signals": [
                    {
                        "name": "w_raddr_bin",
                        "width": "R_ADDR_W+1",
                        "descr": "Write address in binary format wire",
                    },
                ],
            },
            {
                "name": "r_waddr_bin",
                "descr": "Read address in binary format",
                "signals": [
                    {
                        "name": "r_waddr_bin",
                        "width": "W_ADDR_W+1",
                        "descr": "Read address in binary format wire",
                    },
                ],
            },
            {
                "name": "w_waddr_bin",
                "descr": "Write address in binary format",
                "signals": [
                    {
                        "name": "w_waddr_bin",
                        "width": "W_ADDR_W+1",
                        "descr": "Write address in binary format wire",
                    },
                ],
            },
            {
                "name": "r_raddr_bin_n",
                "descr": "Read address in binary format wire (negative edge)",
                "signals": [
                    {
                        "name": "r_raddr_bin_n",
                        "width": "ADDR_W+1",
                        "descr": "Read address in binary format wire (negative edge) wire",
                    },
                ],
            },
            {
                "name": "r_waddr_bin_n",
                "descr": "Write address in binary format wire (negative edge)",
                "signals": [
                    {
                        "name": "r_waddr_bin_n",
                        "width": "ADDR_W+1",
                        "descr": "Read address in binary format wire (negative edge) wire",
                    },
                ],
            },
            {
                "name": "w_raddr_bin_n",
                "descr": "Write address in binary format wire (negative edge)",
                "signals": [
                    {
                        "name": "w_raddr_bin_n",
                        "width": "ADDR_W+1",
                        "descr": "Write address in binary format wire (negative edge) wire",
                    },
                ],
            },
            {
                "name": "w_waddr_bin_n",
                "descr": "Write address in binary format wire (negative edge)",
                "signals": [
                    {
                        "name": "w_waddr_bin_n",
                        "width": "ADDR_W+1",
                        "descr": "Write address in binary format wire (negative edge) wire",
                    },
                ],
            },
            {
                "name": "w_waddr_gray",
                "descr": "Write address in gray format",
                "signals": [
                    {
                        "name": "w_waddr_gray",
                        "width": "W_ADDR_W+1",
                        "descr": "Write address in gray format wire",
                    },
                ],
            },
            {
                "name": "r_waddr_gray",
                "descr": "Read address in gray format",
                "signals": [
                    {
                        "name": "r_waddr_gray",
                        "width": "W_ADDR_W+1",
                        "descr": "Read address in gray format wire",
                    },
                ],
            },
            {
                "name": "r_raddr_gray",
                "descr": "Read address in gray format",
                "signals": [
                    {
                        "name": "r_raddr_gray",
                        "width": "R_ADDR_W+1",
                        "descr": "Read address in gray format wire",
                    },
                ],
            },
            {
                "name": "w_raddr_gray",
                "descr": "Write address in gray format",
                "signals": [
                    {
                        "name": "w_raddr_gray",
                        "width": "R_ADDR_W+1",
                        "descr": "Write address in gray format wire",
                    },
                ],
            },
            {
                "name": "r_level_int",
                "descr": "Internal read level",
                "signals": [
                    {
                        "name": "r_level_int",
                        "width": "(ADDR_W+1)",
                        "descr": "Internal read level wire",
                    },
                ],
            },
            {
                "name": "w_level_int",
                "descr": "Internal write level",
                "signals": [
                    {
                        "name": "w_level_int",
                        "width": "(ADDR_W+1)",
                        "descr": "Internal write level wire",
                    },
                ],
            },
            {
                "name": "r_en_int",
                "descr": "Internal read enable",
                "signals": [
                    {
                        "name": "r_en_int",
                        "width": 1,
                        "descr": "Internal read enable wire",
                    },
                ],
            },
            {
                "name": "w_en_int",
                "descr": "Internal write enable",
                "signals": [
                    {
                        "name": "w_en_int",
                        "width": 1,
                        "descr": "Internal write enable wire",
                    },
                ],
            },
            {
                "name": "w_addr",
                "descr": "Write address wire",
                "signals": [
                    {
                        "name": "w_addr",
                        "width": "W_ADDR_W",
                        "descr": "Write address wire",
                    },
                ],
            },
            {
                "name": "r_addr",
                "descr": "Read address wire",
                "signals": [
                    {
                        "name": "r_addr",
                        "width": "R_ADDR_W",
                        "descr": "Read address wire",
                    },
                ],
            },
            {
                "name": "r_clk_rst_s",
                "descr": "Read clock and reset",
                "signals": [
                    {
                        "name": "r_clk_i",
                        "width": 1,
                        "descr": "Clock",
                    },
                    {
                        "name": "r_arst_i",
                        "width": 1,
                        "descr": "Asynchronous active-high reset",
                    },
                ],
            },
            {
                "name": "w_clk_rst_s",
                "descr": "Write clock and reset",
                "signals": [
                    {
                        "name": "w_clk_i",
                        "width": 1,
                        "descr": "Clock",
                    },
                    {
                        "name": "w_arst_i",
                        "width": 1,
                        "descr": "Asynchronous active-high reset",
                    },
                ],
            },
            {
                "name": "ext_mem_r_w",
                "descr": "External memory read/write",
                "signals": [
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
            {
                "name": "write_addr_en_data",
                "descr": "Write address, enable, and data",
                "signals": [
                    {
                        "name": "w_en_int",
                        "width": 1,
                        "descr": "Internal write enable wire",
                    },
                    {
                        "name": "w_addr",
                        "width": "W_ADDR_W",
                        "descr": "Write address wire",
                    },
                    {
                        "name": "w_data_i",
                        "width": "W_DATA_W",
                    },
                ],
            },
            {
                "name": "r_data_o",
                "descr": "Read data output",
                "signals": [
                    {
                        "name": "r_data_o",
                        "width": "R_DATA_W",
                    },
                ],
            },
            {
                "name": "read_addr_en_data",
                "descr": "Read address, enable, and data",
                "signals": [
                    {
                        "name": "r_en_int",
                        "width": 1,
                        "descr": "Internal read enable wire",
                    },
                    {
                        "name": "r_addr",
                        "width": "R_ADDR_W",
                        "descr": "Read address wire",
                    },
                    {
                        "name": "r_data_o",
                        "width": "R_DATA_W",
                    },
                ],
            },
            {
                "name": "read_clk_cke_arst_rst_en",
                "descr": "Read clock, clock enable, async reset, sync reset, and enable",
                "signals": [
                    {
                        "name": "r_clk_i",
                        "width": 1,
                        "descr": "Clock",
                    },
                    {
                        "name": "r_cke_i",
                        "width": 1,
                        "descr": "Clock enable",
                    },
                    {
                        "name": "r_arst_i",
                        "width": 1,
                        "descr": "Asynchronous active-high reset",
                    },
                    {
                        "name": "r_rst_i",
                        "width": 1,
                    },
                    {
                        "name": "r_en_int",
                        "width": 1,
                        "descr": "Internal read enable wire",
                    },
                ],
            },
            {
                "name": "write_clk_cke_arst_rst_en",
                "descr": "Write clock, clock enable, async reset, sync reset, and enable",
                "signals": [
                    {
                        "name": "w_clk_i",
                        "width": 1,
                        "descr": "Clock",
                    },
                    {
                        "name": "w_cke_i",
                        "width": 1,
                        "descr": "Clock enable",
                    },
                    {
                        "name": "w_arst_i",
                        "width": 1,
                        "descr": "Asynchronous active-high reset",
                    },
                    {
                        "name": "w_rst_i",
                        "width": 1,
                    },
                    {
                        "name": "w_en_int",
                        "width": 1,
                        "descr": "Internal write enable wire",
                    },
                ],
            },
            {
                "name": "read_clk_cke_arst_rst",
                "descr": "Read clock, clock enable, async reset, sync reset",
                "signals": [
                    {
                        "name": "r_clk_i",
                        "width": 1,
                        "descr": "Clock",
                    },
                    {
                        "name": "r_cke_i",
                        "width": 1,
                    },
                    {
                        "name": "r_arst_i",
                        "width": 1,
                        "descr": "Asynchronous active-high reset",
                    },
                    {
                        "name": "r_rst_i",
                        "width": 1,
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_gray_counter",
                "instance_name": "r_raddr_gray_counter",
                "parameters": {
                    "W": "(R_ADDR_W + 1)",
                },
                "connect": {
                    "clk_en_rst_s": "read_clk_cke_arst_rst_en",
                    "data_o": "r_raddr_gray",
                },
            },
            {
                "core_name": "iob_gray_counter",
                "instance_name": "w_waddr_gray_counter",
                "parameters": {
                    "W": "(W_ADDR_W + 1)",
                },
                "connect": {
                    "clk_en_rst_s": "write_clk_cke_arst_rst_en",
                    "data_o": "w_waddr_gray",
                },
            },
            {
                "core_name": "iob_gray2bin",
                "instance_name": "gray2bin_r_raddr",
                "parameters": {
                    "DATA_W": "(R_ADDR_W + 1)",
                },
                "connect": {
                    "gr_i": "r_raddr_gray",
                    "bin_o": "r_raddr_bin",
                },
            },
            {
                "core_name": "iob_gray2bin",
                "instance_name": "gray2bin_r_raddr_sync",
                "parameters": {
                    "DATA_W": "(W_ADDR_W + 1)",
                },
                "connect": {
                    "gr_i": "r_waddr_gray",
                    "bin_o": "r_waddr_bin",
                },
            },
            {
                "core_name": "iob_gray2bin",
                "instance_name": "gray2bin_w_waddr",
                "parameters": {
                    "DATA_W": "(W_ADDR_W + 1)",
                },
                "connect": {
                    "gr_i": "w_waddr_gray",
                    "bin_o": "w_waddr_bin",
                },
            },
            {
                "core_name": "iob_gray2bin",
                "instance_name": "gray2bin_w_raddr_sync",
                "parameters": {
                    "DATA_W": "(R_ADDR_W + 1)",
                },
                "connect": {
                    "gr_i": "w_raddr_gray",
                    "bin_o": "w_raddr_bin",
                },
            },
            {
                "core_name": "iob_sync",
                "instance_name": "w_waddr_gray_sync0",
                "parameters": {
                    "DATA_W": "(W_ADDR_W + 1)",
                    "RST_VAL": "{(W_ADDR_W + 1) {1'd0}}",
                },
                "connect": {
                    "clk_rst_s": "r_clk_rst_s",
                    "signal_i": "w_waddr_gray",
                    "signal_o": "r_waddr_gray",
                },
            },
            {
                "core_name": "iob_sync",
                "instance_name": "r_raddr_gray_sync0",
                "parameters": {
                    "DATA_W": "(R_ADDR_W + 1)",
                    "RST_VAL": "{(R_ADDR_W + 1) {1'd0}}",
                },
                "connect": {
                    "clk_rst_s": "w_clk_rst_s",
                    "signal_i": "r_raddr_gray",
                    "signal_o": "w_raddr_gray",
                },
            },
            {
                "core_name": "iob_asym_converter",
                "instance_name": "asym_converter",
                "parameters": {
                    "W_DATA_W": "W_DATA_W",
                    "R_DATA_W": "R_DATA_W",
                    "ADDR_W": "ADDR_W",
                    "BIG_ENDIAN": "BIG_ENDIAN",
                },
                "connect": {
                    "extmem_io": "ext_mem_r_w",
                    "clk_en_rst_s": "read_clk_cke_arst_rst",
                    "write_i": "write_addr_en_data",
                    "read_io": "read_addr_en_data",
                },
            },
            {
                "core_name": "iob_functions",
                "instantiate": False,
            },
            # For simulation
            {
                "core_name": "iob_ram_at2p",
                "instantiate": False,
            },
            {
                "core_name": "iob_clock",
                "instantiate": False,
            },
        ],
        "snippets": [
            {
                "verilog_code": r"""
                 `include "iob_functions.vs"
                 localparam ADDR_W_DIFF = $clog2(R);  //difference between read and write address widths
                 localparam [ADDR_W:0] FIFO_SIZE = {1'b1, {ADDR_W{1'b0}}};  //in bytes
                 localparam [ADDR_W-1:0] W_INCR = (W_DATA_W > R_DATA_W) ? 1'b1 << ADDR_W_DIFF : 1'b1;
                 localparam [ADDR_W-1:0] R_INCR = (R_DATA_W > W_DATA_W) ? 1'b1 << ADDR_W_DIFF : 1'b1;
                 generate
                    if (W_DATA_W > R_DATA_W) begin : g_write_wider_bin
                        assign w_waddr_bin_n = w_waddr_bin << ADDR_W_DIFF;
                        assign w_raddr_bin_n = w_raddr_bin;
                        assign r_raddr_bin_n = r_raddr_bin;
                        assign r_waddr_bin_n = r_waddr_bin << ADDR_W_DIFF;
                    end else if (R_DATA_W > W_DATA_W) begin : g_read_wider_bin
                        assign w_waddr_bin_n = w_waddr_bin;
                        assign w_raddr_bin_n = w_raddr_bin << ADDR_W_DIFF;
                        assign r_raddr_bin_n = r_raddr_bin << ADDR_W_DIFF;
                        assign r_waddr_bin_n = r_waddr_bin;
                    end else begin : g_write_equals_read_bin
                        assign w_raddr_bin_n = w_raddr_bin;
                        assign w_waddr_bin_n = w_waddr_bin;
                        assign r_waddr_bin_n = r_waddr_bin;
                        assign r_raddr_bin_n = r_raddr_bin;
                    end
                endgenerate
                assign r_level_int = r_waddr_bin_n - r_raddr_bin_n;
                assign r_level_o   = r_level_int[0+:(ADDR_W+1)];
                //READ DOMAIN EMPTY AND FULL FLAGS
                assign r_empty_o   = (r_level_int < {2'd0, R_INCR});
                assign r_full_o    = (r_level_int > (FIFO_SIZE - {2'd0, R_INCR}));
                assign w_level_int = w_waddr_bin_n - w_raddr_bin_n;
                assign w_level_o   = w_level_int[0+:(ADDR_W+1)];
                assign w_empty_o   = (w_level_int < {2'd0, W_INCR});
                assign w_full_o    = (w_level_int > (FIFO_SIZE - {2'd0, W_INCR}));
                assign r_en_int = (r_en_i & (~r_empty_o));
                assign w_en_int = (w_en_i & (~w_full_o));
                assign w_addr = w_waddr_bin[W_ADDR_W-1:0];
                assign r_addr          = r_raddr_bin[R_ADDR_W-1:0];
                assign ext_mem_w_clk_o = w_clk_i;
                assign ext_mem_r_clk_o = r_clk_i;
                """
            }
        ],
    }

    return attributes_dict
