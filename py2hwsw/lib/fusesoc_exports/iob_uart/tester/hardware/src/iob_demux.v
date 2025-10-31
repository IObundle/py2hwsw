// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_demux_conf.vh"

module iob_demux #(
    parameter DATA_W = `IOB_DEMUX_DATA_W,
    parameter N = `IOB_DEMUX_N,
    parameter SEL_W = `IOB_DEMUX_SEL_W  // Don't change this parameter value!
) (
    // sel_i: Selector interface
    input [SEL_W-1:0] sel_i,
    // data_i: Input port
    input [DATA_W-1:0] data_i,
    // data_o: Output port
    output [N*DATA_W-1:0] data_o
);


   // Select the data to output
   genvar i;
   generate
      for (i = 0; i < N; i = i + 1) begin : gen_demux
         assign data_o[i*DATA_W+:DATA_W] = (sel_i==i[0+:SEL_W])? data_i : {DATA_W{1'b0}};
      end
   endgenerate

            


endmodule
