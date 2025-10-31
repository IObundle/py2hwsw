// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_ram_t2p_be_conf.vh"

module iob_ram_t2p_be #(
    parameter HEXFILE = `IOB_RAM_T2P_BE_HEXFILE,
    parameter ADDR_W = `IOB_RAM_T2P_BE_ADDR_W,
    parameter DATA_W = `IOB_RAM_T2P_BE_DATA_W,
    parameter COL_W = `IOB_RAM_T2P_BE_COL_W,  // Don't change this parameter value!
    parameter NUM_COL = `IOB_RAM_T2P_BE_NUM_COL  // Don't change this parameter value!
) (
    // ram_t2p_be_s: RAM interface
    input clk_i,
    input r_en_i,
    input [ADDR_W-1:0] r_addr_i,
    output [DATA_W-1:0] r_data_o,
    input [DATA_W/8-1:0] w_strb_i,
    input [ADDR_W-1:0] w_addr_i,
    input [DATA_W-1:0] w_data_i
);



    genvar i;
    generate
        localparam file_suffix = {"7", "6", "5", "4", "3", "2", "1", "0"};
        for (i = 0; i < NUM_COL; i = i + 1) begin : ram_col
            localparam mem_init_file_int = (HEXFILE != "none") ?
                {HEXFILE, "_", file_suffix[8*(i+1)-1-:8], ".hex"} : "none";

            iob_ram_t2p #(
                .HEXFILE(mem_init_file_int),
                .ADDR_W (ADDR_W),
                .DATA_W (COL_W)
            ) ram (
                .clk_i(clk_i),
                .w_en_i  (w_strb_i[i]),
                .w_addr_i(w_addr_i),
                .w_data_i(w_data_i[i*COL_W+:COL_W]),
                .r_en_i  (r_en_i),
                .r_addr_i(r_addr_i),
                .r_data_o(r_data_o[i*COL_W+:COL_W])
            );
        end
    endgenerate



endmodule
