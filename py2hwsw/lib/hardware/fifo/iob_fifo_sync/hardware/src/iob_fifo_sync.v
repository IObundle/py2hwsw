// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

`include "iob_fifo_sync_conf.vh"

module iob_fifo_sync #(
   `include "iob_fifo_sync_params.vs"
) (
   `include "iob_fifo_sync_io.vs"
);

   `include "iob_functions.vs"

   localparam ADDR_W_DIFF = $clog2(R);
   localparam [ADDR_W:0] FIFO_SIZE = {1'b1, {ADDR_W{1'b0}}};  //in bytes

   //effective write enable
   wire w_en_int;
   assign w_en_int = (w_en_i & (~w_full_o));

   //write address
   wire [W_ADDR_W-1:0] w_addr;
   iob_counter #(
      .DATA_W (W_ADDR_W),
      .RST_VAL({W_ADDR_W{1'd0}})
   ) w_addr_cnt0 (
      `include "iob_fifo_sync_iob_clk_s_s_portmap.vs"

      .counter_rst_i(rst_i),
      .counter_inc_i(w_en_int),
      .data_o       (w_addr)
   );

   //effective read enable
   wire r_en_int;
   assign r_en_int = (r_en_i & (~r_empty_o));

   //read address
   wire [R_ADDR_W-1:0] r_addr;
   iob_counter #(
      .DATA_W (R_ADDR_W),
      .RST_VAL({R_ADDR_W{1'd0}})
   ) r_addr_cnt0 (
      `include "iob_fifo_sync_iob_clk_s_s_portmap.vs"

      .counter_rst_i(rst_i),
      .counter_inc_i(r_en_int),
      .data_o       (r_addr)
   );

   //assign according to assymetry type
   localparam [ADDR_W-1:0] W_INCR = (W_DATA_W > R_DATA_W) ?
                  {{ADDR_W-1{1'd0}},{1'd1}} << ADDR_W_DIFF : {{ADDR_W-1{1'd0}},{1'd1}};
   localparam [ADDR_W-1:0] R_INCR = (R_DATA_W > W_DATA_W) ?
                  {{ADDR_W-1{1'd0}},{1'd1}} << ADDR_W_DIFF : {{ADDR_W-1{1'd0}},{1'd1}};

   //FIFO level
   reg  [ADDR_W:0] level_nxt;
   wire [ADDR_W:0] level_int;
   iob_reg_car #(
      .DATA_W (ADDR_W + 1),
      .RST_VAL({(ADDR_W + 1) {1'd0}})
   ) level_reg0 (
      `include "iob_fifo_sync_iob_clk_s_s_portmap.vs"

      .rst_i(rst_i),

      .data_i(level_nxt),
      .data_o(level_int)
   );

   reg [(ADDR_W+1)-1:0] level_incr;
   always @* begin
      level_incr = level_int + W_INCR;
      level_nxt  = level_int;
      if (w_en_int && (!r_en_int))  //write only
         level_nxt = level_incr;
      else if (w_en_int && r_en_int)  //write and read
         level_nxt = level_incr - R_INCR;
      else if (r_en_int)  //read only
         level_nxt = level_int - R_INCR;
   end

   assign level_o = level_int;

   //FIFO empty
   wire r_empty_nxt;
   assign r_empty_nxt = level_nxt < {1'b0, R_INCR};
   iob_reg_car #(
      .DATA_W (1),
      .RST_VAL(1'd1)
   ) r_empty_reg0 (
      `include "iob_fifo_sync_iob_clk_s_s_portmap.vs"
      .rst_i (rst_i),
      .data_i(r_empty_nxt),
      .data_o(r_empty_o)
   );

   //FIFO full
   wire w_full_nxt;
   assign w_full_nxt = level_nxt > (FIFO_SIZE - W_INCR);
   iob_reg_car #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) w_full_reg0 (
      `include "iob_fifo_sync_iob_clk_s_s_portmap.vs"
      .rst_i (rst_i),
      .data_i(w_full_nxt),
      .data_o(w_full_o)
   );

   assign ext_mem_clk_o = clk_i;

   iob_asym_converter #(
      .W_DATA_W(W_DATA_W),
      .R_DATA_W(R_DATA_W),
      .ADDR_W  (ADDR_W)
   ) asym_converter (
      .ext_mem_w_en_o  (ext_mem_w_en_o),
      .ext_mem_w_addr_o(ext_mem_w_addr_o),
      .ext_mem_w_data_o(ext_mem_w_data_o),
      .ext_mem_r_en_o  (ext_mem_r_en_o),
      .ext_mem_r_addr_o(ext_mem_r_addr_o),
      .ext_mem_r_data_i(ext_mem_r_data_i),
      `include "iob_fifo_sync_iob_clk_s_s_portmap.vs"
      .rst_i           (rst_i),
      .w_addr_i        (w_addr),
      .w_en_i          (w_en_int),
      .w_data_i        (w_data_i),
      .r_addr_i        (r_addr),
      .r_en_i          (r_en_int),
      .r_data_o        (r_data_o)
   );

endmodule
