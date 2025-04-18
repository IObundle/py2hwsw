// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

module iob_axil2iob #(
   parameter AXIL_ADDR_W = 21,           // AXI Lite address bus width in bits
   parameter AXIL_DATA_W = 21,           // AXI Lite data bus width in bits
   parameter ADDR_W      = AXIL_ADDR_W,  // IOb address bus width in bits
   parameter DATA_W      = AXIL_DATA_W   // IOb data bus width in bits
) (
   `include "iob_axil2iob_io.vs"
);

   localparam WSTRB_W = DATA_W / 8;

   wire [ADDR_W-1:0] iob_addr;
   wire              iob_addr_en;

   // COMPUTE AXIL OUTPUTS

   // write address channel

   // write channel
   assign axil_wready_o  = iob_ready_i;

   // write response
   assign axil_bresp_o   = 2'b0;
   wire axil_bvalid_nxt;

   //bvalid 
   assign axil_bvalid_nxt = (iob_valid_o & (|iob_wstrb_o)) ? iob_ready_i : (axil_bvalid_o & ~axil_bready_i);

   // read address
   assign axil_arready_o = iob_ready_i;

   // read channel
   assign axil_rresp_o = 2'b0;

   //rvalid
   assign axil_rvalid_o = iob_rvalid_i;

   //rdata
   assign axil_rdata_o = iob_rdata_i;

   // COMPUTE IOb OUTPUTS

   assign iob_valid_o = axil_wvalid_i | axil_arvalid_i;
   assign iob_addr_o = axil_arvalid_i ? axil_araddr_i : axil_awvalid_i ? axil_awaddr_i : iob_addr;
   assign iob_wdata_o = axil_wdata_i;
   assign iob_wstrb_o = axil_wvalid_i ? axil_wstrb_i : {WSTRB_W{1'b0}};
   assign iob_rready_o = axil_rready_i;

   assign iob_addr_en = axil_arvalid_i | axil_awvalid_i;

   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(0)
   ) iob_reg_bvalid (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(axil_bvalid_nxt),
      .data_o(axil_bvalid_o)
   );

   iob_reg_cae #(
      .DATA_W (ADDR_W),
      .RST_VAL(0)
   ) iob_reg_addr (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (iob_addr_en),
      .data_i(iob_addr_o),
      .data_o(iob_addr)
   );

   // wstate: write state
   wire awready_en;
   wire axil_awready_nxt;

   // axil_awready == 0: waiting for bvalid and bready
   // axil_awready == 1: waiting for awvalid
   assign awready_en = axil_awready_o ? axil_awvalid_i : (axil_bvalid_o & axil_bready_i);
   assign axil_awready_nxt = ~axil_awready_o; // toggle state
   iob_reg_cae #(
      .DATA_W (1),
      .RST_VAL(1)
   ) iob_reg_awready (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (awready_en),
      .data_i(axil_awready_nxt),
      .data_o(axil_awready_o)
   );


endmodule
