// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_mux_conf.vh"

module iob_mux #(
    parameter DATA_W = `IOB_MUX_DATA_W,
    parameter N = `IOB_MUX_N,
    parameter SEL_W = `IOB_MUX_SEL_W  // Don't change this parameter value!
) (
    // sel_i: Selector interface
    input [SEL_W-1:0] sel_i,
    // data_i: Input port
    input [N*DATA_W-1:0] data_i,
    // data_o: Output port
    output reg [DATA_W-1:0] data_o
);


        integer input_sel;
        always @* begin
            data_o = {DATA_W{1'b0}};
            for (input_sel = 0; input_sel < N; input_sel = input_sel + 1) begin : gen_mux
                if (input_sel[0+:SEL_W] == sel_i) begin
                     data_o = data_i[input_sel*DATA_W+:DATA_W];
                end
            end
        end
            


endmodule
