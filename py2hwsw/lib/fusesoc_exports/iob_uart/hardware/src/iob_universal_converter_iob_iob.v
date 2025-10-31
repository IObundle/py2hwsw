// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_universal_converter_iob_iob_conf.vh"

module iob_universal_converter_iob_iob #(
   parameter ADDR_W = `IOB_UNIVERSAL_CONVERTER_IOB_IOB_ADDR_W,
   parameter DATA_W = `IOB_UNIVERSAL_CONVERTER_IOB_IOB_DATA_W
) (
   // s_s: Subordinate port
   input                 iob_valid_i,
   input  [  ADDR_W-1:0] iob_addr_i,
   input  [  DATA_W-1:0] iob_wdata_i,
   input  [DATA_W/8-1:0] iob_wstrb_i,
   output                iob_rvalid_o,
   output [  DATA_W-1:0] iob_rdata_o,
   output                iob_ready_o,
   // m_m: Manager port
   output                iob_valid_o,
   output [  ADDR_W-1:0] iob_addr_o,
   output [  DATA_W-1:0] iob_wdata_o,
   output [DATA_W/8-1:0] iob_wstrb_o,
   input                 iob_rvalid_i,
   input  [  DATA_W-1:0] iob_rdata_i,
   input                 iob_ready_i
);

   // Internal IOb wire
   wire                iob_valid;
   wire [  ADDR_W-1:0] iob_addr;
   wire [  DATA_W-1:0] iob_wdata;
   wire [DATA_W/8-1:0] iob_wstrb;
   wire                iob_rvalid;
   wire [  DATA_W-1:0] iob_rdata;
   wire                iob_ready;


   // Directly connect subordinate IOb port to intetnal IOb wire
   assign iob_valid    = iob_valid_i;
   assign iob_addr     = iob_addr_i;
   assign iob_wdata    = iob_wdata_i;
   assign iob_wstrb    = iob_wstrb_i;
   assign iob_rvalid_o = iob_rvalid;
   assign iob_rdata_o  = iob_rdata;
   assign iob_ready_o  = iob_ready;

   // Directly connect internal IOb wire to manager IOb port
   assign iob_valid_o  = iob_valid;
   assign iob_addr_o   = iob_addr;
   assign iob_wdata_o  = iob_wdata;
   assign iob_wstrb_o  = iob_wstrb;
   assign iob_rvalid   = iob_rvalid_i;
   assign iob_rdata    = iob_rdata_i;
   assign iob_ready    = iob_ready_i;



endmodule
