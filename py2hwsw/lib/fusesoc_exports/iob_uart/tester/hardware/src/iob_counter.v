// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_counter_conf.vh"

module iob_counter #(
    parameter DATA_W = `IOB_COUNTER_DATA_W,
    parameter RST_VAL = `IOB_COUNTER_RST_VAL
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // counter_rst_i: Counter reset input
    input counter_rst_i,
    // counter_en_i: Counter enable input
    input counter_en_i,
    // data_o: Output port
    output [DATA_W-1:0] data_o
);

// data_int wire
    reg [DATA_W-1:0] data_int;

	always @ (*)
		begin
			
        data_int = data_o + 1'b1;
        
		end

        // Default description
        iob_reg_care #(
        .DATA_W(DATA_W),
        .RST_VAL(RST_VAL)
    ) reg0 (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(counter_rst_i),
        .en_i(counter_en_i),
        // data_i port: Data input
        .data_i(data_int),
        // data_o port: Data output
        .data_o(data_o)
        );

    
endmodule
