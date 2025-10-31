// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_or_conf.vh"

module iob_or #(
   parameter W = `IOB_OR_W
) (
   // a_i: Input port
   input  [W-1:0] a_i,
   // b_i: Input port
   input  [W-1:0] b_i,
   // y_o: Output port
   output [W-1:0] y_o
);

   assign y_o = a_i | b_i;


endmodule
