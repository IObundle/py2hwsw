// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_rom_sp_conf.vh"

module iob_rom_sp #(
    parameter HEXFILE = `IOB_ROM_SP_HEXFILE,
    parameter ADDR_W = `IOB_ROM_SP_ADDR_W,
    parameter DATA_W = `IOB_ROM_SP_DATA_W,
    parameter MEM_INIT_FILE_INT = `IOB_ROM_SP_MEM_INIT_FILE_INT  // Don't change this parameter value!
) (
    // rom_sp_s: ROM interface
    input clk_i,
    input [ADDR_W-1:0] addr_i,
    input en_i,
    output [DATA_W-1:0] r_data_o
);


   localparam INIT_RAM = (MEM_INIT_FILE_INT != "none.hex") ? 1 : 0;
            // Declare the ROM
   reg [DATA_W-1:0] rom[(2**ADDR_W)-1:0];
   reg [DATA_W-1:0] r_data_int;

   // Initialize the ROM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh( MEM_INIT_FILE_INT, rom, 0, (2 ** ADDR_W) - 1);
       end
   endgenerate

   // Operate the ROM
   always @(posedge clk_i) if (en_i) 
   r_data_int <= rom[addr_i];

   assign r_data_o = r_data_int;
            


endmodule
