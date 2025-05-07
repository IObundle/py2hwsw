# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "N",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "number of registers",
            },
            {
                "name": "W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "register width",
            },
            {
                "name": "WDATA_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "width of write data",
            },
            {
                "name": "WADDR_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "width of write address",
            },
            {
                "name": "RDATA_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "width of read data",
            },
            {
                "name": "RADDR_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "width of read address",
            },
            # cpu interface
            # the address on the cpu side must be a byte address
            {
                "name": "DATA_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "width of data",
            },
            {
                "name": "WSTRB_W",
                "type": "D",
                "val": "WDATA_W / 8",
                "min": "0",
                "max": "NA",
                "descr": "width of write strobe",
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
                "name": "write_i",
                "descr": "Write port",
                "signals": [
                    {"name": "w_en_i", "width": 1},
                    {"name": "w_strb_i", "width": "WSTRB_W"},
                    {"name": "w_addr_i", "width": "WADDR_W"},
                    {"name": "w_data_i", "width": "WDATA_W"},
                ],
            },
            {
                "name": "read_io",
                "descr": "read port",
                "signals": [
                    {"name": "r_addr_i", "width": "RADDR_W"},
                    {"name": "r_data_o", "width": "RDATA_W"},
                ],
            },
        ],
        "wires": [
            {
                "name": "internal_wires",
                "descr": "Wires for internal usage",
                "signals": [
                    {
                        "name": "regarray",
                        "width": "N*W",
                        "descr": "register file and register file write enable",
                    },
                    {"name": "wen", "width": "N"},
                    {"name": "waddr_incr", "width": "$clog2(DATA_W/8)+1"},
                    {"name": "waddr_int", "width": "WADDR_INT_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_ctls",
                # For now, this subblock is instantiated manually in the snippet
                "instantiate": False,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   //reconstruct write address from waddr_i and wstrb_i
   localparam WADDR_INT_W = (WADDR_W > ($clog2(
       DATA_W / 8
   ) + 1)) ? WADDR_W : ($clog2(
       DATA_W / 8
   ) + 1);
   assign waddr_int = w_addr_i + waddr_incr;

   iob_ctls #(
      .W     (DATA_W / 8),
      .MODE  (0),
      .SYMBOL(0)
   ) iob_ctls_txinst (
      .data_i (w_strb_i),
      .count_o(waddr_incr)
   );

   //write register file
   genvar row_sel;
   genvar col_sel;

   localparam LAST_I = (N / WSTRB_W) * WSTRB_W;
   localparam REM_I = (N - LAST_I) + 1;

   generate
      for (row_sel = 0; row_sel < N; row_sel = row_sel + WSTRB_W) begin : g_rows
         for (
             col_sel = 0; col_sel < ((row_sel == LAST_I) ? REM_I : WSTRB_W); col_sel = col_sel + 1
         ) begin : g_columns
            if ((row_sel + col_sel) < N) begin : g_if
               assign wen[row_sel+col_sel] = w_en_i & (waddr_int == (row_sel + col_sel)) & w_strb_i[col_sel];
               iob_reg_cae #(
                  .DATA_W (W),
                  .RST_VAL({W{1'b0}})
               ) iob_reg_inst (
                  `include "iob_regarray_2p_iob_clk_s_s_portmap.vs"
                  .en_i  (wen[row_sel+col_sel]),
                  .data_i(w_data_i[(col_sel*8)+:W]),
                  .data_o(regarray[(row_sel+col_sel)*W+:W])
               );
            end
         end
      end
   endgenerate

   //read register file
   generate
      if (RADDR_W > 0) begin : g_read
         assign r_data_o = regarray[RDATA_W*r_addr_i+:RDATA_W];
      end else begin : g_read
         assign r_data_o = regarray;
      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
