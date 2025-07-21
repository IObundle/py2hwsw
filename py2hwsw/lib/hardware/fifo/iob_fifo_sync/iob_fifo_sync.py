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
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable and reset",
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
        "wires": [
            {
                "name": "w_en_int",
                "descr": "Internal write enable wire",
                "signals": [
                    {
                        "name": "w_en_int",
                        "width": "1",
                        "descr": "Internal write enable signal",
                    },
                ],
            },
            {
                "name": "w_addr",
                "descr": "Internal write address wire",
                "signals": [
                    {
                        "name": "w_addr",
                        "width": "W_ADDR_W",
                        "descr": "Internal write address",
                    },
                ],
            },
            {
                "name": "r_en_int",
                "descr": "Internal read enable wire",
                "signals": [
                    {
                        "name": "r_en_int",
                        "width": "1",
                        "descr": "Internal read enable signal",
                    },
                ],
            },
            {
                "name": "r_addr",
                "descr": "Internal read address wire",
                "signals": [
                    {
                        "name": "r_addr",
                        "width": "R_ADDR_W",
                        "descr": "Internal read address",
                    },
                ],
            },
            {
                "name": "r_empty_nxt",
                "descr": "Next read empty signal",
                "signals": [
                    {
                        "name": "r_empty_nxt",
                        "width": "1",
                        "descr": "Next read empty signal",
                    },
                ],
            },
            {
                "name": "w_full_nxt",
                "descr": "Next write full signal",
                "signals": [
                    {
                        "name": "w_full_nxt",
                        "width": "1",
                        "descr": "Next write full signal",
                    },
                ],
            },
            {
                "name": "level",
                "descr": "Internal FIFO level wire",
                "signals": [
                    {
                        "name": "level",
                        "width": "ADDR_W+1",
                        "descr": "Internal FIFO level",
                    },
                ],
            },
            {
                "name": "level_incr",
                "descr": "Internal FIFO level wire",
                "signals": [
                    {
                        "name": "level_incr",
                        "width": "ADDR_W+1",
                        "descr": "Internal FIFO level",
                    },
                ],
            },
            {
                "name": "sync_rst",
                "descr": "Synchronous reset",
                "signals": [
                    {
                        "name": "rst_i",
                    },
                ],
            },
            {
                "name": "sync_ext_mem",
                "descr": "Synchronous external memory interface",
                "signals": [
                    {
                        "name": "ext_mem_w_en_o",
                        "width": "R",
                    },
                    {
                        "name": "ext_mem_w_addr_o",
                        "width": "MINADDR_W",
                    },
                    {
                        "name": "ext_mem_w_data_o",
                        "width": "MAXDATA_W",
                    },
                    {
                        "name": "ext_mem_r_en_o",
                        "width": "R",
                    },
                    {
                        "name": "ext_mem_r_addr_o",
                        "width": "MINADDR_W",
                    },
                    {
                        "name": "ext_mem_r_data_i",
                        "width": "MAXDATA_W",
                    },
                ],
            },
            {
                "name": "sync_write",
                "descr": "Synchronous write",
                "signals": [
                    {
                        "name": "w_en_int",
                        "width": "1",
                    },
                    {
                        "name": "w_addr",
                        "width": "W_ADDR_W",
                    },
                    {
                        "name": "w_data_i",
                        "width": "W_DATA_W",
                    },
                ],
            },
            {
                "name": "sync_read",
                "descr": "Synchronous read",
                "signals": [
                    {
                        "name": "r_en_int",
                        "width": "1",
                    },
                    {
                        "name": "r_addr",
                        "width": "R_ADDR_W",
                    },
                    {
                        "name": "r_data_o",
                        "width": "R_DATA_W",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "r_empty_reg0",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
                "parameters": {
                    "DATA_W": "1",
                    "RST_VAL": "{1'd1}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "r_empty_nxt",
                    "data_o": "r_empty_o",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "w_full_reg0",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
                "parameters": {
                    "DATA_W": "1",
                    "RST_VAL": "{1'd0}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "w_full_nxt",
                    "data_o": "w_full_o",
                },
            },
            {
                "core_name": "iob_counter",
                "instance_name": "w_addr_cnt0",
                "parameters": {
                    "DATA_W": "W_ADDR_W",
                    "RST_VAL": "{W_ADDR_W{1'd0}}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "counter_rst_i": "sync_rst",
                    "counter_en_i": "w_en_int",
                    "data_o": "w_addr",
                },
            },
            {
                "core_name": "iob_counter",
                "instance_name": "r_addr_cnt0",
                "parameters": {
                    "DATA_W": "R_ADDR_W",
                    "RST_VAL": "{R_ADDR_W{1'd0}}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "counter_rst_i": "sync_rst",
                    "counter_en_i": "r_en_int",
                    "data_o": "r_addr",
                },
            },
            {
                "core_name": "iob_asym_converter",
                "instance_name": "asym_converter",
                "parameters": {
                    "W_DATA_W": "W_DATA_W",
                    "R_DATA_W": "R_DATA_W",
                    "ADDR_W": "ADDR_W",
                },
                "connect": {
                    "extmem_io": "sync_ext_mem",
                    "clk_en_rst_s": "clk_en_rst_s",
                    "write_i": "sync_write",
                    "read_io": "sync_read",
                },
            },
            {
                "core_name": "iob_functions",
                "instantiate": False,
            },
            # For simulation
            {
                "core_name": "iob_ram_t2p",
                "instantiate": False,
            },
        ],
        "comb": {
            "code": """
                level_incr = level + W_INCR;
                level_nxt  = level;
                level_rst=rst_i;
                if (w_en_int && (!r_en_int))  //write only
                    level_nxt = level_incr;
                else if (w_en_int && r_en_int)  //write and read
                    level_nxt = level_incr - R_INCR;
                else if (r_en_int)  //read only
                    level_nxt = level - R_INCR;
            """,
        },
        "snippets": [
            {
                "verilog_code": r"""
                `include "iob_functions.vs"
                localparam ADDR_W_DIFF = $clog2(R);
                localparam [ADDR_W:0] FIFO_SIZE = {1'b1, {ADDR_W{1'b0}}};  //in bytes
                assign w_en_int = (w_en_i & (~w_full_o));
                assign r_en_int = (r_en_i & (~r_empty_o));
                //assign according to assymetry type
                localparam [ADDR_W-1:0] W_INCR = (W_DATA_W > R_DATA_W) ?
                  {{ADDR_W-1{1'd0}},{1'd1}} << ADDR_W_DIFF : {{ADDR_W-1{1'd0}},{1'd1}};
                localparam [ADDR_W-1:0] R_INCR = (R_DATA_W > W_DATA_W) ?
                  {{ADDR_W-1{1'd0}},{1'd1}} << ADDR_W_DIFF : {{ADDR_W-1{1'd0}},{1'd1}};
                assign level_o = level;
                assign r_empty_nxt = level_nxt < {1'b0, R_INCR};
                assign w_full_nxt = level_nxt > (FIFO_SIZE - W_INCR);
                assign ext_mem_clk_o = clk_i;


                """
            }
        ],
    }

    return attributes_dict
