// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1 ns / 1 ps
`include "iob_regarray_2p_conf.vh"

module iob_regarray_2p #(
   `include "iob_regarray_2p_params.vs"
) (
   `include "iob_regarray_2p_io.vs"

   //`include "iob_regarray_2p_iob_clk_s_port.vs"
   //input                                              w_en_i,
   //input  [((RADDR_W+WADDR_W)+(WSTRB_W+WDATA_W))-1:0] req_i,
   //output [                              RDATA_W-1:0] resp_o
);

   //register file and register file write enable
   wire [(N*W)-1 : 0] regarray;
   wire [      N-1:0] wen;

   //reconstruct write address from waddr_i and wstrb_i
   localparam WADDR_INT_W = (WADDR_W > ($clog2(
       DATA_W / 8
   ) + 1)) ? WADDR_W : ($clog2(
       DATA_W / 8
   ) + 1);
   wire [($clog2(DATA_W/8)+1)-1:0] waddr_incr;
   wire [         WADDR_INT_W-1:0] waddr_int;
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

endmodule
