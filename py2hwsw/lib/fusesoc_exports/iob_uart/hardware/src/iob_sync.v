// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_sync_conf.vh"

module iob_sync #(
   parameter DATA_W  = `IOB_SYNC_DATA_W,
   parameter RST_VAL = `IOB_SYNC_RST_VAL
) (
   // clk_rst_s: Clock and reset
   input               clk_i,
   input               arst_i,
   // signal_i: Input port
   input  [DATA_W-1:0] signal_i,
   // signal_o: Output port
   output [DATA_W-1:0] signal_o
);

   // synchronizer wire
   wire [DATA_W-1:0] synchronizer;

   // Default description
   iob_reg_a #(
      .DATA_W (DATA_W),
      .RST_VAL(RST_VAL)
   ) reg1 (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(signal_i),
      // data_o port: Data output
      .data_o(synchronizer)
   );

   // Default description
   iob_reg_a #(
      .DATA_W (DATA_W),
      .RST_VAL(RST_VAL)
   ) reg2 (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(synchronizer),
      // data_o port: Data output
      .data_o(signal_o)
   );


endmodule
