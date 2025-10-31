// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_reg_cae_conf.vh"

module iob_reg_cae #(
   parameter DATA_W  = `IOB_REG_CAE_DATA_W,
   parameter RST_VAL = `IOB_REG_CAE_RST_VAL
) (
   // clk_en_rst_s: Clock, clock enable and reset
   input                   clk_i,
   input                   cke_i,
   input                   arst_i,
   input                   en_i,
   // data_i: Data input
   input      [DATA_W-1:0] data_i,
   // data_o: Data output
   output reg [DATA_W-1:0] data_o
);


   always @(posedge clk_i, posedge arst_i) begin
      if (arst_i) begin
         data_o <= RST_VAL;
      end else if (cke_i & en_i) begin
         data_o <= data_i;
      end
   end



endmodule
