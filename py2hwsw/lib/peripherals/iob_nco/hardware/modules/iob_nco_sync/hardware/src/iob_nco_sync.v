// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_nco_sync_conf.vh"
`include "iob_nco_csrs.vh"

module iob_nco_sync #(
   `include "iob_nco_sync_params.vs"
) (
   `include "iob_nco_sync_io.vs"
);

   //synchronize CSR clock to in_clk_i clock
   iob_sync #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) soft_reset_sync (
      .clk_i   (in_clk_i),
      .arst_i  (in_arst_i),
      .signal_i(soft_reset_i),
      .signal_o(soft_reset_o)
   );

   iob_sync #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) enable_sync (
      .clk_i   (in_clk_i),
      .arst_i  (in_arst_i),
      .signal_i(enable_i),
      .signal_o(enable_o)
   );

   // async fifo memory wires
   wire                period_fifo_w_clk;
   wire [PERIOD_W-1:0] period_fifo_w_data;
   wire                period_fifo_w_addr;
   wire                period_fifo_w_en;
   wire                period_fifo_r_clk;
   wire [PERIOD_W-1:0] period_fifo_r_data;
   wire                period_fifo_r_addr;
   wire                period_fifo_r_en;
   wire                period_fifo_w_full;

   wire                period_fifo_ren;
   wire                period_fifo_empty;

   assign period_fifo_ren = ~period_fifo_empty;

   iob_fifo_async #(
      .W_DATA_W(PERIOD_W),
      .R_DATA_W(PERIOD_W),
      .ADDR_W  (1)
   ) period_fifo (
      //memory write port
      .ext_mem_w_clk_o (period_fifo_w_clk),
      .ext_mem_w_en_o  (period_fifo_w_en),
      .ext_mem_w_addr_o(period_fifo_w_addr),
      .ext_mem_w_data_o(period_fifo_w_data),
      //memory read port
      .ext_mem_r_clk_o (period_fifo_r_clk),
      .ext_mem_r_en_o  (period_fifo_r_en),
      .ext_mem_r_addr_o(period_fifo_r_addr),
      .ext_mem_r_data_i(period_fifo_r_data),

      //read port
      .r_clk_i  (in_clk_i),
      .r_cke_i  (in_cke_i),
      .r_arst_i (in_arst_i),
      .r_rst_i  (1'b0),
      .r_en_i   (period_fifo_ren),
      .r_data_o (period_wdata_o),
      .r_empty_o(period_fifo_empty),
      .r_full_o (),
      .r_level_o(),

      //write port
      .w_clk_i  (clk_i),
      .w_cke_i  (cke_i),
      .w_arst_i (arst_i),
      .w_rst_i  (soft_reset_i),
      .w_en_i   (period_wen_i),
      .w_data_i (period_wdata_i),
      .w_empty_o(),
      .w_full_o (),
      .w_level_o()
   );

   // audio in FIFO memory
   iob_regarray_at2p #(
      .ADDR_W(1),
      .DATA_W(PERIOD_W)
   ) audio_in_fifo_regs (
      .w_clk_i (period_fifo_w_clk),
      .w_cke_i (period_fifo_w_en),
      .w_arst_i(arst_i),
      .w_addr_i(period_fifo_w_addr),
      .w_data_i(period_fifo_w_data),
      .r_clk_i (period_fifo_r_clk),
      .r_cke_i (period_fifo_r_en),
      .r_arst_i(in_arst_i),
      .r_addr_i(period_fifo_r_addr),
      .r_data_o(period_fifo_r_data)
   );

   //fractional period value register
   iob_reg_car #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) period_wen_reg (
      .clk_i (in_clk_i),
      .cke_i (in_cke_i),
      .arst_i(in_arst_i),
      .rst_i (1'b0),
      .data_i(period_fifo_ren),
      .data_o(period_wen_o)
   );

endmodule
