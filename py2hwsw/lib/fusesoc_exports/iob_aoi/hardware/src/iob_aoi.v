// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_aoi_conf.vh"

module iob_aoi #(
   parameter W = `IOB_AOI_W
) (
   // a_i: Input port a
   input  [W-1:0] a_i,
   // b_i: Input port b
   input  [W-1:0] b_i,
   // c_i: Input port c
   input  [W-1:0] c_i,
   // d_i: Input port d
   input  [W-1:0] d_i,
   // y_o: Output port y
   output [W-1:0] y_o
);

   // and ab output
   wire [W-1:0] aab;
   // and cd output
   wire [W-1:0] cad;
   // or output
   wire         oab;

   // First and gate
   iob_and #(
      .W(W)
   ) iob_and_ab (
      // a_i port: Input port
      .a_i(a_i),
      // b_i port: Input port
      .b_i(b_i),
      // y_o port: Output port
      .y_o(aab)
   );

   // Second and gate
   iob_and #(
      .W(W)
   ) io_and_cd (
      // a_i port: Input port
      .a_i(c_i),
      // b_i port: Input port
      .b_i(d_i),
      // y_o port: Output port
      .y_o(cad)
   );

   // Or gate
   iob_or #(
      .W(W)
   ) iob_or_abcd (
      // a_i port: Input port
      .a_i(aab),
      // b_i port: Input port
      .b_i(cad),
      // y_o port: Output port
      .y_o(oab)
   );

   // Inverter
   iob_inv #(
      .W(W)
   ) iob_inv_out (
      // a_i port: Input port
      .a_i(oab),
      // y_o port: Output port
      .y_o(y_o)
   );


endmodule
