// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_reset_sync_conf.vh"

module iob_reset_sync (
    // clk_rst_s: clock and reset
    input clk_i,
    input arst_i,
    // arst_o: Output port
    output arst_o
);

// data_int wire
    wire [2-1:0] data_int;
// sync wire
    wire [2-1:0] sync;


    assign data_int = {sync[0], 1'b0};
    assign arst_o = sync[1];
            

        // Default description
        iob_reg_a #(
        .DATA_W(2),
        .RST_VAL(2'd3)
    ) reg1 (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .arst_i(arst_i),
        // data_i port: Data input
        .data_i(data_int),
        // data_o port: Data output
        .data_o(sync)
        );

    
endmodule
