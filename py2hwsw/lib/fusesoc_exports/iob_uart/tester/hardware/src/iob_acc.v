// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_acc_conf.vh"

module iob_acc #(
    parameter DATA_W = `IOB_ACC_DATA_W,
    parameter INCR_W = `IOB_ACC_INCR_W,
    parameter RST_VAL = `IOB_ACC_RST_VAL
) (
    // clk_en_rst_s: clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // en_rst_i: Enable and Synchronous reset interface
    input en_i,
    input rst_i,
    // incr_i: Input port
    input [INCR_W-1:0] incr_i,
    // data_o: Output port
    output [DATA_W-1:0] data_o
);

// Sum result
    wire [DATA_W+1-1:0] data_nxt;
// data_int wire
    wire [DATA_W-1:0] data_int;


       assign data_nxt = data_o + incr_i;
       assign data_int = data_nxt[DATA_W-1:0];
            

        // Default description
        iob_reg_care #(
        .DATA_W(DATA_W),
        .RST_VAL(RST_VAL)
    ) reg0 (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(rst_i),
        .en_i(en_i),
        // data_i port: Data input
        .data_i(data_int),
        // data_o port: Data output
        .data_o(data_o)
        );

    
endmodule
