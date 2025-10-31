// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_prio_enc_conf.vh"

module iob_prio_enc #(
   parameter W    = `IOB_PRIO_ENC_W,
   parameter MODE = `IOB_PRIO_ENC_MODE
) (
   // unencoded_i: Input port
   input      [          W-1:0] unencoded_i,
   // encoded_o: Output port
   output reg [$clog2(W+1)-1:0] encoded_o
);

   wire [W+1-1:0] unencoded_int;


   // MSB = 1 if unencoded_i = 0
   assign unencoded_int = {(~(|unencoded_i)), unencoded_i};

   integer pos;
   generate
      if (MODE == "LOW") begin : gen_low_prio
         always @* begin
            encoded_o = {$clog2(W + 1) {1'b0}};  //placeholder default value
            for (pos = W; pos != -1; pos = pos - 1) begin
               if (unencoded_int[pos]) begin
                  encoded_o = pos[$clog2(W+1)-1:0];
               end
            end
         end
      end else begin : gen_highest_prio  //MODE == "HIGH"
         always @* begin
            encoded_o = {$clog2(W + 1) {1'b0}};  //placeholder default value
            for (pos = {W{1'd0}}; pos < (W + 1); pos = pos + 1) begin
               if (unencoded_int[pos]) begin
                  encoded_o = pos[$clog2(W+1)-1:0];
               end
            end
         end
      end
   endgenerate



endmodule
