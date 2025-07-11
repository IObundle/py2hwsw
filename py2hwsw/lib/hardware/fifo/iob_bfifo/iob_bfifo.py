# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data width",
                "type": "P",
                "val": "21",
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
                "descr": "Clock, clock enable, async and sync reset",
            },
            {
                "name": "write_io",
                "descr": "Write interface",
                "signals": [
                    {
                        "name": "write_i",
                        "width": 1,
                        "descr": "Write",
                    },
                    {
                        "name": "wwidth_i",
                        "width": "$clog2(DATA_W)",
                        "descr": "Write width",
                    },
                    {
                        "name": "wdata_i",
                        "width": "DATA_W",
                        "descr": "Write data",
                    },
                    {
                        "name": "wlevel_o",
                        "width": "$clog2(2*DATA_W)",
                        "descr": "Write level",
                    },
                ],
            },
            {
                "name": "read_io",
                "descr": "Read interface",
                "signals": [
                    {
                        "name": "read_i",
                        "width": 1,
                        "descr": "Read",
                    },
                    {
                        "name": "rwidth_i",
                        "width": "$clog2(DATA_W)",
                        "descr": "Read width",
                    },
                    {
                        "name": "rdata_o",
                        "width": "DATA_W",
                        "descr": "Read data",
                    },
                    {
                        "name": "rlevel_o",
                        "width": "$clog2(2*DATA_W)",
                        "descr": "Read level",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "data",
                "descr": "data wire",
                "signals": [
                    {"name": "data", "width": "(2*DATA_W)", "descr": "Data Wire"},
                ],
            },
            {
                "name": "rdata",
                "descr": "Read data wire",
                "signals": [
                    {
                        "name": "rdata",
                        "width": "(2*DATA_W)",
                        "descr": "Read Data Wire",
                    },
                ],
            },
            {
                "name": "rptr",
                "descr": "Read pointer wire",
                "signals": [
                    {
                        "name": "rptr",
                        "width": "$clog2(2*DATA_W)",
                        "descr": "Read Pointer Wire",
                    },
                ],
            },
            {
                "name": "wptr",
                "descr": "Write pointer wire",
                "signals": [
                    {
                        "name": "wptr",
                        "width": "$clog2(2*DATA_W)",
                        "descr": "Write Pointer Wire",
                    },
                ],
            },
            {
                "name": "level",
                "descr": "FIFO level wire",
                "signals": [
                    {
                        "name": "level",
                        "width": "$clog2(2*DATA_W)+1",
                        "descr": "FIFO Level Wire",
                    },
                ],
            },
            {
                "name": "wmask",
                "descr": "Write mask wire",
                "signals": [
                    {
                        "name": "wmask",
                        "width": " (2*DATA_W)",
                        "descr": "Write mask wire",
                    }
                ],
            },
            {
                "name": "crwidth",
                "descr": "Read width  wire",
                "signals": [
                    {
                        "name": "crwidth",
                        "width": "$clog2(2*DATA_W)",
                        "descr": "Read width  wire",
                    },
                ],
            },
            {
                "name": "cwwidth",
                "descr": "Write width wire",
                "signals": [
                    {
                        "name": "cwwidth",
                        "width": "$clog2(2*DATA_W)",
                        "descr": "Write width  wire",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instantiate": False,
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
            },
            # For simulation
            {
                "core_name": "iob_functions",
                "instantiate": False,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
                `include "iob_functions.vs"
                reg  [      (2*DATA_W)-1:0] data_nxt;
                reg  [$clog2(2*DATA_W)-1:0] rptr_nxt;
                reg  [$clog2(2*DATA_W)-1:0] wptr_nxt;
                reg  [  $clog2(2*DATA_W):0] level_nxt;
                reg  [          DATA_W-1:0] wdata_int;
                reg  [      (2*DATA_W)-1:0] wdata;

                localparam BUFFER_SIZE = 2 * DATA_W;
                //assign outputs
                assign wlevel_o = (1'b1 << $clog2(BUFFER_SIZE)) - level;
                assign rlevel_o = level;

                assign crwidth = (~rwidth_i[$clog2(DATA_W)-1:0]) + {{$clog2(DATA_W) - 1{1'd0}}, 1'd1};
                assign cwwidth = (~wwidth_i[$clog2(DATA_W)-1:0]) + {{$clog2(DATA_W) - 1{1'd0}}, 1'd1};
                
                //zero trailing bits
                assign rdata_o = (rdata[(2*DATA_W)-1-:DATA_W] >> crwidth) << crwidth;
                
                //write mask shifted
                 assign wmask   = iob_cshift_right(BUFFER_SIZE, ({BUFFER_SIZE{1'b1}} >> wwidth_i), wptr);
                
                //read data shifted
                assign rdata   = iob_cshift_left(BUFFER_SIZE, data, rptr);
                
                
                always @* begin
                    //write data shifted
                    wdata_int = (wdata_i >> cwwidth) << cwwidth;
                    wdata     = iob_cshift_right(BUFFER_SIZE, {wdata_int, {DATA_W{1'b0}}}, wptr);
                    data_nxt  = data;
                    rptr_nxt  = rptr;
                    wptr_nxt  = wptr;
                    level_nxt = level;
                    if (read_i) begin  //read
                    rptr_nxt  = rptr + rwidth_i;
                    level_nxt = level - rwidth_i;
                    end else if (write_i) begin  //write
                    data_nxt  = (data & wmask) | wdata;
                    wptr_nxt  = wptr + wwidth_i;
                    level_nxt = level + wwidth_i;
                    end
                end

                //data register
                iob_reg_car #(
                    .DATA_W (BUFFER_SIZE),
                    .RST_VAL({BUFFER_SIZE{1'b0}})
                ) data_reg_inst (
                    .clk_i(clk_i),
                    .cke_i(cke_i),
                    .arst_i(arst_i),
                    .rst_i (rst_i),
                    .data_i(data_nxt),
                    .data_o(data)
                );

                //read pointer
                iob_reg_car #(
                    .DATA_W ($clog2(BUFFER_SIZE)),
                    .RST_VAL({$clog2(BUFFER_SIZE) {1'b0}})
                ) rptr_reg (
                    .clk_i(clk_i),
                    .cke_i(cke_i),
                    .arst_i(arst_i),
                    .rst_i (rst_i),
                    .data_i(rptr_nxt),
                    .data_o(rptr)
                );

                //write pointer
                iob_reg_car #(
                    .DATA_W ($clog2(BUFFER_SIZE)),
                    .RST_VAL({$clog2(BUFFER_SIZE) {1'b0}})
                ) wptr_reg (
                    .clk_i(clk_i),
                    .cke_i(cke_i),
                    .arst_i(arst_i),
                    .rst_i (rst_i),
                    .data_i(wptr_nxt),
                    .data_o(wptr)
                );

                //fifo level
                iob_reg_car #(
                    .DATA_W ($clog2(BUFFER_SIZE) + 1),
                    .RST_VAL({$clog2(BUFFER_SIZE) + 1{1'b0}})
                ) level_reg (
                    .clk_i(clk_i),
                    .cke_i(cke_i),
                    .arst_i(arst_i),
                    .rst_i (rst_i),
                    .data_i(level_nxt),
                    .data_o(level)
                );



                """
            }
        ],
    }

    return attributes_dict
