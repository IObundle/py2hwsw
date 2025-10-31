// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_universal_converter_axi_iob_conf.vh"

module iob_universal_converter_axi_iob #(
    parameter ADDR_W = `IOB_UNIVERSAL_CONVERTER_AXI_IOB_ADDR_W,
    parameter DATA_W = `IOB_UNIVERSAL_CONVERTER_AXI_IOB_DATA_W,
    parameter AXI_ID_W = `IOB_UNIVERSAL_CONVERTER_AXI_IOB_AXI_ID_W,
    parameter AXI_LEN_W = `IOB_UNIVERSAL_CONVERTER_AXI_IOB_AXI_LEN_W
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // s_s: Subordinate port
    input [ADDR_W-1:0] axi_araddr_i,
    input axi_arvalid_i,
    output axi_arready_o,
    output [DATA_W-1:0] axi_rdata_o,
    output [2-1:0] axi_rresp_o,
    output axi_rvalid_o,
    input axi_rready_i,
    input [AXI_ID_W-1:0] axi_arid_i,
    input [AXI_LEN_W-1:0] axi_arlen_i,
    input [3-1:0] axi_arsize_i,
    input [2-1:0] axi_arburst_i,
    input [2-1:0] axi_arlock_i,
    input [4-1:0] axi_arcache_i,
    input [4-1:0] axi_arqos_i,
    output [AXI_ID_W-1:0] axi_rid_o,
    output axi_rlast_o,
    input [ADDR_W-1:0] axi_awaddr_i,
    input axi_awvalid_i,
    output axi_awready_o,
    input [DATA_W-1:0] axi_wdata_i,
    input [DATA_W/8-1:0] axi_wstrb_i,
    input axi_wvalid_i,
    output axi_wready_o,
    output [2-1:0] axi_bresp_o,
    output axi_bvalid_o,
    input axi_bready_i,
    input [AXI_ID_W-1:0] axi_awid_i,
    input [AXI_LEN_W-1:0] axi_awlen_i,
    input [3-1:0] axi_awsize_i,
    input [2-1:0] axi_awburst_i,
    input [2-1:0] axi_awlock_i,
    input [4-1:0] axi_awcache_i,
    input [4-1:0] axi_awqos_i,
    input axi_wlast_i,
    output [AXI_ID_W-1:0] axi_bid_o,
    // m_m: Manager port
    output iob_valid_o,
    output [ADDR_W-1:0] iob_addr_o,
    output [DATA_W-1:0] iob_wdata_o,
    output [DATA_W/8-1:0] iob_wstrb_o,
    input iob_rvalid_i,
    input [DATA_W-1:0] iob_rdata_i,
    input iob_ready_i
);

// Internal IOb wire
    wire iob_valid;
    wire [ADDR_W-1:0] iob_addr;
    wire [DATA_W-1:0] iob_wdata;
    wire [DATA_W/8-1:0] iob_wstrb;
    wire iob_rvalid;
    wire [DATA_W-1:0] iob_rdata;
    wire iob_ready;


   // Directly connect internal IOb wire to manager IOb port
   assign iob_valid_o = iob_valid;
   assign iob_addr_o = iob_addr;
   assign iob_wdata_o = iob_wdata;
   assign iob_wstrb_o = iob_wstrb;
   assign iob_rvalid = iob_rvalid_i;
   assign iob_rdata = iob_rdata_i;
   assign iob_ready = iob_ready_i;


        // Convert AXI from subordinate port into IOb interface for internal wire
        iob_axi2iob #(
        .ADDR_WIDTH(ADDR_W),
        .DATA_WIDTH(DATA_W),
        .AXI_ID_WIDTH(AXI_ID_W),
        .AXI_LEN_WIDTH(AXI_LEN_W)
    ) iob_axi2iob_coverter (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // axi_s port: Subordinate AXI interface
        .s_axi_araddr_i(axi_araddr_i),
        .s_axi_arvalid_i(axi_arvalid_i),
        .s_axi_arready_o(axi_arready_o),
        .s_axi_rdata_o(axi_rdata_o),
        .s_axi_rresp_o(axi_rresp_o),
        .s_axi_rvalid_o(axi_rvalid_o),
        .s_axi_rready_i(axi_rready_i),
        .s_axi_arid_i(axi_arid_i),
        .s_axi_arlen_i(axi_arlen_i),
        .s_axi_arsize_i(axi_arsize_i),
        .s_axi_arburst_i(axi_arburst_i),
        .s_axi_arlock_i(axi_arlock_i[0]),
        .s_axi_arcache_i(axi_arcache_i),
        .s_axi_arqos_i(axi_arqos_i),
        .s_axi_rid_o(axi_rid_o),
        .s_axi_rlast_o(axi_rlast_o),
        .s_axi_awaddr_i(axi_awaddr_i),
        .s_axi_awvalid_i(axi_awvalid_i),
        .s_axi_awready_o(axi_awready_o),
        .s_axi_wdata_i(axi_wdata_i),
        .s_axi_wstrb_i(axi_wstrb_i),
        .s_axi_wvalid_i(axi_wvalid_i),
        .s_axi_wready_o(axi_wready_o),
        .s_axi_bresp_o(axi_bresp_o),
        .s_axi_bvalid_o(axi_bvalid_o),
        .s_axi_bready_i(axi_bready_i),
        .s_axi_awid_i(axi_awid_i),
        .s_axi_awlen_i(axi_awlen_i),
        .s_axi_awsize_i(axi_awsize_i),
        .s_axi_awburst_i(axi_awburst_i),
        .s_axi_awlock_i(axi_awlock_i[0]),
        .s_axi_awcache_i(axi_awcache_i),
        .s_axi_awqos_i(axi_awqos_i),
        .s_axi_wlast_i(axi_wlast_i),
        .s_axi_bid_o(axi_bid_o),
        // iob_m port: Manager IOb interface
        .iob_valid_o(iob_valid),
        .iob_addr_o(iob_addr),
        .iob_wdata_o(iob_wdata),
        .iob_wstrb_o(iob_wstrb),
        .iob_rvalid_i(iob_rvalid),
        .iob_rdata_i(iob_rdata),
        .iob_ready_i(iob_ready)
        );

    
endmodule
