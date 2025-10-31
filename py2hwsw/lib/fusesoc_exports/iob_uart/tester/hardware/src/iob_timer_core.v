// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_timer_core_conf.vh"

module iob_timer_core #(
    parameter DATA_W = `IOB_TIMER_CORE_DATA_W
) (
    // clk_en_rst_s: Clock and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // reg_interface_io: 
    input en_i,
    input rst_i,
    input rstrb_i,
    output [64-1:0] time_o
);

// Time counter wire
    wire [2*DATA_W-1:0] time_counter;

        // Default description
        iob_reg_care #(
        .DATA_W(2 * DATA_W),
        .RST_VAL(0)
    ) time_counter_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i( rst_i),
        .en_i( rstrb_i),
        // data_i port: Data input
        .data_i(time_counter),
        // data_o port: Data output
        .data_o(time_o)
        );

            // Default description
        iob_counter #(
        .DATA_W(2 * DATA_W),
        .RST_VAL(0)
    ) time_counter_cnt (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // counter_rst_i port: Counter reset input
        .counter_rst_i(rst_i),
        // counter_en_i port: Counter enable input
        .counter_en_i(en_i),
        // data_o port: Output port
        .data_o(time_counter)
        );

    
endmodule
