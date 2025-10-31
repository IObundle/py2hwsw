// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_ctls_conf.vh"

module iob_ctls #(
   parameter W      = `IOB_CTLS_W,
   parameter MODE   = `IOB_CTLS_MODE,
   parameter SYMBOL = `IOB_CTLS_SYMBOL
) (
   // data_i: Input data
   input  [          W-1:0] data_i,
   // count_o: Output counter
   output [$clog2(W+1)-1:0] count_o
);

   // Internal data
   wire [W-1:0] data_int1;
   // Reversed data
   wire [W-1:0] data_int2;


   // invert if searching zeros or not
   generate
      if (SYMBOL == 0) begin : g_zeros
         assign data_int1 = data_i;
      end else begin : g_ones
         assign data_int1 = ~data_i;
      end
   endgenerate
   // reverse if leading symbols or not
   generate
      if (MODE == 1) begin : g_reverse
         iob_reverse #(W) reverse0 (
            .data_i(data_int1),
            .data_o(data_int2)
         );
      end else begin : g_noreverse
         assign data_int2 = data_int1;
      end
   endgenerate



   // count trailing zeros
   iob_prio_enc #(
      .W   (W),
      .MODE("LOW")
   ) prio_encoder0 (
      // unencoded_i port: Input port
      .unencoded_i(data_int2),
      // encoded_o port: Output port
      .encoded_o  (count_o)
   );


endmodule
