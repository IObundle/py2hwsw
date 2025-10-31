// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_axi_full_xbar_conf.vh"

module iob_uart_tester_axi_full_xbar #(
    parameter ID_W = `IOB_UART_TESTER_AXI_FULL_XBAR_ID_W,
    parameter LEN_W = `IOB_UART_TESTER_AXI_FULL_XBAR_LEN_W
) (
    // clk_en_rst_s: Clock, clock enable and async reset
    input clk_i,
    input cke_i,
    input arst_i,
    // rst_i: Synchronous reset
    input rst_i,
    // m0_axi_m: Manager 0 interface
    output [32-1:0] m0_axi_araddr_o,
    output m0_axi_arvalid_o,
    input m0_axi_arready_i,
    input [32-1:0] m0_axi_rdata_i,
    input [2-1:0] m0_axi_rresp_i,
    input m0_axi_rvalid_i,
    output m0_axi_rready_o,
    output [ID_W-1:0] m0_axi_arid_o,
    output [LEN_W-1:0] m0_axi_arlen_o,
    output [3-1:0] m0_axi_arsize_o,
    output [2-1:0] m0_axi_arburst_o,
    output m0_axi_arlock_o,
    output [4-1:0] m0_axi_arcache_o,
    output [4-1:0] m0_axi_arqos_o,
    input [ID_W-1:0] m0_axi_rid_i,
    input m0_axi_rlast_i,
    output [32-1:0] m0_axi_awaddr_o,
    output m0_axi_awvalid_o,
    input m0_axi_awready_i,
    output [32-1:0] m0_axi_wdata_o,
    output [32/8-1:0] m0_axi_wstrb_o,
    output m0_axi_wvalid_o,
    input m0_axi_wready_i,
    input [2-1:0] m0_axi_bresp_i,
    input m0_axi_bvalid_i,
    output m0_axi_bready_o,
    output [ID_W-1:0] m0_axi_awid_o,
    output [LEN_W-1:0] m0_axi_awlen_o,
    output [3-1:0] m0_axi_awsize_o,
    output [2-1:0] m0_axi_awburst_o,
    output m0_axi_awlock_o,
    output [4-1:0] m0_axi_awcache_o,
    output [4-1:0] m0_axi_awqos_o,
    output m0_axi_wlast_o,
    input [ID_W-1:0] m0_axi_bid_i,
    // m1_axi_m: Manager 1 interface
    output [32-1:0] m1_axi_araddr_o,
    output m1_axi_arvalid_o,
    input m1_axi_arready_i,
    input [32-1:0] m1_axi_rdata_i,
    input [2-1:0] m1_axi_rresp_i,
    input m1_axi_rvalid_i,
    output m1_axi_rready_o,
    output [ID_W-1:0] m1_axi_arid_o,
    output [LEN_W-1:0] m1_axi_arlen_o,
    output [3-1:0] m1_axi_arsize_o,
    output [2-1:0] m1_axi_arburst_o,
    output m1_axi_arlock_o,
    output [4-1:0] m1_axi_arcache_o,
    output [4-1:0] m1_axi_arqos_o,
    input [ID_W-1:0] m1_axi_rid_i,
    input m1_axi_rlast_i,
    output [32-1:0] m1_axi_awaddr_o,
    output m1_axi_awvalid_o,
    input m1_axi_awready_i,
    output [32-1:0] m1_axi_wdata_o,
    output [32/8-1:0] m1_axi_wstrb_o,
    output m1_axi_wvalid_o,
    input m1_axi_wready_i,
    input [2-1:0] m1_axi_bresp_i,
    input m1_axi_bvalid_i,
    output m1_axi_bready_o,
    output [ID_W-1:0] m1_axi_awid_o,
    output [LEN_W-1:0] m1_axi_awlen_o,
    output [3-1:0] m1_axi_awsize_o,
    output [2-1:0] m1_axi_awburst_o,
    output m1_axi_awlock_o,
    output [4-1:0] m1_axi_awcache_o,
    output [4-1:0] m1_axi_awqos_o,
    output m1_axi_wlast_o,
    input [ID_W-1:0] m1_axi_bid_i,
    // m2_axi_m: Manager 2 interface
    output [32-1:0] m2_axi_araddr_o,
    output m2_axi_arvalid_o,
    input m2_axi_arready_i,
    input [32-1:0] m2_axi_rdata_i,
    input [2-1:0] m2_axi_rresp_i,
    input m2_axi_rvalid_i,
    output m2_axi_rready_o,
    output [ID_W-1:0] m2_axi_arid_o,
    output [LEN_W-1:0] m2_axi_arlen_o,
    output [3-1:0] m2_axi_arsize_o,
    output [2-1:0] m2_axi_arburst_o,
    output m2_axi_arlock_o,
    output [4-1:0] m2_axi_arcache_o,
    output [4-1:0] m2_axi_arqos_o,
    input [ID_W-1:0] m2_axi_rid_i,
    input m2_axi_rlast_i,
    output [32-1:0] m2_axi_awaddr_o,
    output m2_axi_awvalid_o,
    input m2_axi_awready_i,
    output [32-1:0] m2_axi_wdata_o,
    output [32/8-1:0] m2_axi_wstrb_o,
    output m2_axi_wvalid_o,
    input m2_axi_wready_i,
    input [2-1:0] m2_axi_bresp_i,
    input m2_axi_bvalid_i,
    output m2_axi_bready_o,
    output [ID_W-1:0] m2_axi_awid_o,
    output [LEN_W-1:0] m2_axi_awlen_o,
    output [3-1:0] m2_axi_awsize_o,
    output [2-1:0] m2_axi_awburst_o,
    output m2_axi_awlock_o,
    output [4-1:0] m2_axi_awcache_o,
    output [4-1:0] m2_axi_awqos_o,
    output m2_axi_wlast_o,
    input [ID_W-1:0] m2_axi_bid_i,
    // s0_axi_s: Subordinate 0 interface
    input [32-1:0] s0_axi_araddr_i,
    input s0_axi_arvalid_i,
    output s0_axi_arready_o,
    output [32-1:0] s0_axi_rdata_o,
    output [2-1:0] s0_axi_rresp_o,
    output s0_axi_rvalid_o,
    input s0_axi_rready_i,
    input [ID_W-1:0] s0_axi_arid_i,
    input [LEN_W-1:0] s0_axi_arlen_i,
    input [3-1:0] s0_axi_arsize_i,
    input [2-1:0] s0_axi_arburst_i,
    input s0_axi_arlock_i,
    input [4-1:0] s0_axi_arcache_i,
    input [4-1:0] s0_axi_arqos_i,
    output [ID_W-1:0] s0_axi_rid_o,
    output s0_axi_rlast_o,
    input [32-1:0] s0_axi_awaddr_i,
    input s0_axi_awvalid_i,
    output s0_axi_awready_o,
    input [32-1:0] s0_axi_wdata_i,
    input [32/8-1:0] s0_axi_wstrb_i,
    input s0_axi_wvalid_i,
    output s0_axi_wready_o,
    output [2-1:0] s0_axi_bresp_o,
    output s0_axi_bvalid_o,
    input s0_axi_bready_i,
    input [ID_W-1:0] s0_axi_awid_i,
    input [LEN_W-1:0] s0_axi_awlen_i,
    input [3-1:0] s0_axi_awsize_i,
    input [2-1:0] s0_axi_awburst_i,
    input s0_axi_awlock_i,
    input [4-1:0] s0_axi_awcache_i,
    input [4-1:0] s0_axi_awqos_i,
    input s0_axi_wlast_i,
    output [ID_W-1:0] s0_axi_bid_o,
    // s1_axi_s: Subordinate 1 interface
    input [32-1:0] s1_axi_araddr_i,
    input s1_axi_arvalid_i,
    output s1_axi_arready_o,
    output [32-1:0] s1_axi_rdata_o,
    output [2-1:0] s1_axi_rresp_o,
    output s1_axi_rvalid_o,
    input s1_axi_rready_i,
    input [ID_W-1:0] s1_axi_arid_i,
    input [LEN_W-1:0] s1_axi_arlen_i,
    input [3-1:0] s1_axi_arsize_i,
    input [2-1:0] s1_axi_arburst_i,
    input s1_axi_arlock_i,
    input [4-1:0] s1_axi_arcache_i,
    input [4-1:0] s1_axi_arqos_i,
    output [ID_W-1:0] s1_axi_rid_o,
    output s1_axi_rlast_o,
    input [32-1:0] s1_axi_awaddr_i,
    input s1_axi_awvalid_i,
    output s1_axi_awready_o,
    input [32-1:0] s1_axi_wdata_i,
    input [32/8-1:0] s1_axi_wstrb_i,
    input s1_axi_wvalid_i,
    output s1_axi_wready_o,
    output [2-1:0] s1_axi_bresp_o,
    output s1_axi_bvalid_o,
    input s1_axi_bready_i,
    input [ID_W-1:0] s1_axi_awid_i,
    input [LEN_W-1:0] s1_axi_awlen_i,
    input [3-1:0] s1_axi_awsize_i,
    input [2-1:0] s1_axi_awburst_i,
    input s1_axi_awlock_i,
    input [4-1:0] s1_axi_awcache_i,
    input [4-1:0] s1_axi_awqos_i,
    input s1_axi_wlast_i,
    output [ID_W-1:0] s1_axi_bid_o
);

// Connect split of subordinate 0 to merge of manager 0
    wire [30-1:0] s0_m0_axi_araddr;
    wire s0_m0_axi_arvalid;
    wire s0_m0_axi_arready;
    wire [32-1:0] s0_m0_axi_rdata;
    wire [2-1:0] s0_m0_axi_rresp;
    wire s0_m0_axi_rvalid;
    wire s0_m0_axi_rready;
    wire [ID_W-1:0] s0_m0_axi_arid;
    wire [LEN_W-1:0] s0_m0_axi_arlen;
    wire [3-1:0] s0_m0_axi_arsize;
    wire [2-1:0] s0_m0_axi_arburst;
    wire s0_m0_axi_arlock;
    wire [4-1:0] s0_m0_axi_arcache;
    wire [4-1:0] s0_m0_axi_arqos;
    wire [ID_W-1:0] s0_m0_axi_rid;
    wire s0_m0_axi_rlast;
    wire [30-1:0] s0_m0_axi_awaddr;
    wire s0_m0_axi_awvalid;
    wire s0_m0_axi_awready;
    wire [32-1:0] s0_m0_axi_wdata;
    wire [32/8-1:0] s0_m0_axi_wstrb;
    wire s0_m0_axi_wvalid;
    wire s0_m0_axi_wready;
    wire [2-1:0] s0_m0_axi_bresp;
    wire s0_m0_axi_bvalid;
    wire s0_m0_axi_bready;
    wire [ID_W-1:0] s0_m0_axi_awid;
    wire [LEN_W-1:0] s0_m0_axi_awlen;
    wire [3-1:0] s0_m0_axi_awsize;
    wire [2-1:0] s0_m0_axi_awburst;
    wire s0_m0_axi_awlock;
    wire [4-1:0] s0_m0_axi_awcache;
    wire [4-1:0] s0_m0_axi_awqos;
    wire s0_m0_axi_wlast;
    wire [ID_W-1:0] s0_m0_axi_bid;
// Connect split of subordinate 0 to merge of manager 1
    wire [30-1:0] s0_m1_axi_araddr;
    wire s0_m1_axi_arvalid;
    wire s0_m1_axi_arready;
    wire [32-1:0] s0_m1_axi_rdata;
    wire [2-1:0] s0_m1_axi_rresp;
    wire s0_m1_axi_rvalid;
    wire s0_m1_axi_rready;
    wire [ID_W-1:0] s0_m1_axi_arid;
    wire [LEN_W-1:0] s0_m1_axi_arlen;
    wire [3-1:0] s0_m1_axi_arsize;
    wire [2-1:0] s0_m1_axi_arburst;
    wire s0_m1_axi_arlock;
    wire [4-1:0] s0_m1_axi_arcache;
    wire [4-1:0] s0_m1_axi_arqos;
    wire [ID_W-1:0] s0_m1_axi_rid;
    wire s0_m1_axi_rlast;
    wire [30-1:0] s0_m1_axi_awaddr;
    wire s0_m1_axi_awvalid;
    wire s0_m1_axi_awready;
    wire [32-1:0] s0_m1_axi_wdata;
    wire [32/8-1:0] s0_m1_axi_wstrb;
    wire s0_m1_axi_wvalid;
    wire s0_m1_axi_wready;
    wire [2-1:0] s0_m1_axi_bresp;
    wire s0_m1_axi_bvalid;
    wire s0_m1_axi_bready;
    wire [ID_W-1:0] s0_m1_axi_awid;
    wire [LEN_W-1:0] s0_m1_axi_awlen;
    wire [3-1:0] s0_m1_axi_awsize;
    wire [2-1:0] s0_m1_axi_awburst;
    wire s0_m1_axi_awlock;
    wire [4-1:0] s0_m1_axi_awcache;
    wire [4-1:0] s0_m1_axi_awqos;
    wire s0_m1_axi_wlast;
    wire [ID_W-1:0] s0_m1_axi_bid;
// Connect split of subordinate 0 to merge of manager 2
    wire [30-1:0] s0_m2_axi_araddr;
    wire s0_m2_axi_arvalid;
    wire s0_m2_axi_arready;
    wire [32-1:0] s0_m2_axi_rdata;
    wire [2-1:0] s0_m2_axi_rresp;
    wire s0_m2_axi_rvalid;
    wire s0_m2_axi_rready;
    wire [ID_W-1:0] s0_m2_axi_arid;
    wire [LEN_W-1:0] s0_m2_axi_arlen;
    wire [3-1:0] s0_m2_axi_arsize;
    wire [2-1:0] s0_m2_axi_arburst;
    wire s0_m2_axi_arlock;
    wire [4-1:0] s0_m2_axi_arcache;
    wire [4-1:0] s0_m2_axi_arqos;
    wire [ID_W-1:0] s0_m2_axi_rid;
    wire s0_m2_axi_rlast;
    wire [30-1:0] s0_m2_axi_awaddr;
    wire s0_m2_axi_awvalid;
    wire s0_m2_axi_awready;
    wire [32-1:0] s0_m2_axi_wdata;
    wire [32/8-1:0] s0_m2_axi_wstrb;
    wire s0_m2_axi_wvalid;
    wire s0_m2_axi_wready;
    wire [2-1:0] s0_m2_axi_bresp;
    wire s0_m2_axi_bvalid;
    wire s0_m2_axi_bready;
    wire [ID_W-1:0] s0_m2_axi_awid;
    wire [LEN_W-1:0] s0_m2_axi_awlen;
    wire [3-1:0] s0_m2_axi_awsize;
    wire [2-1:0] s0_m2_axi_awburst;
    wire s0_m2_axi_awlock;
    wire [4-1:0] s0_m2_axi_awcache;
    wire [4-1:0] s0_m2_axi_awqos;
    wire s0_m2_axi_wlast;
    wire [ID_W-1:0] s0_m2_axi_bid;
// Connect split of subordinate 1 to merge of manager 0
    wire [30-1:0] s1_m0_axi_araddr;
    wire s1_m0_axi_arvalid;
    wire s1_m0_axi_arready;
    wire [32-1:0] s1_m0_axi_rdata;
    wire [2-1:0] s1_m0_axi_rresp;
    wire s1_m0_axi_rvalid;
    wire s1_m0_axi_rready;
    wire [ID_W-1:0] s1_m0_axi_arid;
    wire [LEN_W-1:0] s1_m0_axi_arlen;
    wire [3-1:0] s1_m0_axi_arsize;
    wire [2-1:0] s1_m0_axi_arburst;
    wire s1_m0_axi_arlock;
    wire [4-1:0] s1_m0_axi_arcache;
    wire [4-1:0] s1_m0_axi_arqos;
    wire [ID_W-1:0] s1_m0_axi_rid;
    wire s1_m0_axi_rlast;
    wire [30-1:0] s1_m0_axi_awaddr;
    wire s1_m0_axi_awvalid;
    wire s1_m0_axi_awready;
    wire [32-1:0] s1_m0_axi_wdata;
    wire [32/8-1:0] s1_m0_axi_wstrb;
    wire s1_m0_axi_wvalid;
    wire s1_m0_axi_wready;
    wire [2-1:0] s1_m0_axi_bresp;
    wire s1_m0_axi_bvalid;
    wire s1_m0_axi_bready;
    wire [ID_W-1:0] s1_m0_axi_awid;
    wire [LEN_W-1:0] s1_m0_axi_awlen;
    wire [3-1:0] s1_m0_axi_awsize;
    wire [2-1:0] s1_m0_axi_awburst;
    wire s1_m0_axi_awlock;
    wire [4-1:0] s1_m0_axi_awcache;
    wire [4-1:0] s1_m0_axi_awqos;
    wire s1_m0_axi_wlast;
    wire [ID_W-1:0] s1_m0_axi_bid;
// Connect split of subordinate 1 to merge of manager 1
    wire [30-1:0] s1_m1_axi_araddr;
    wire s1_m1_axi_arvalid;
    wire s1_m1_axi_arready;
    wire [32-1:0] s1_m1_axi_rdata;
    wire [2-1:0] s1_m1_axi_rresp;
    wire s1_m1_axi_rvalid;
    wire s1_m1_axi_rready;
    wire [ID_W-1:0] s1_m1_axi_arid;
    wire [LEN_W-1:0] s1_m1_axi_arlen;
    wire [3-1:0] s1_m1_axi_arsize;
    wire [2-1:0] s1_m1_axi_arburst;
    wire s1_m1_axi_arlock;
    wire [4-1:0] s1_m1_axi_arcache;
    wire [4-1:0] s1_m1_axi_arqos;
    wire [ID_W-1:0] s1_m1_axi_rid;
    wire s1_m1_axi_rlast;
    wire [30-1:0] s1_m1_axi_awaddr;
    wire s1_m1_axi_awvalid;
    wire s1_m1_axi_awready;
    wire [32-1:0] s1_m1_axi_wdata;
    wire [32/8-1:0] s1_m1_axi_wstrb;
    wire s1_m1_axi_wvalid;
    wire s1_m1_axi_wready;
    wire [2-1:0] s1_m1_axi_bresp;
    wire s1_m1_axi_bvalid;
    wire s1_m1_axi_bready;
    wire [ID_W-1:0] s1_m1_axi_awid;
    wire [LEN_W-1:0] s1_m1_axi_awlen;
    wire [3-1:0] s1_m1_axi_awsize;
    wire [2-1:0] s1_m1_axi_awburst;
    wire s1_m1_axi_awlock;
    wire [4-1:0] s1_m1_axi_awcache;
    wire [4-1:0] s1_m1_axi_awqos;
    wire s1_m1_axi_wlast;
    wire [ID_W-1:0] s1_m1_axi_bid;
// Connect split of subordinate 1 to merge of manager 2
    wire [30-1:0] s1_m2_axi_araddr;
    wire s1_m2_axi_arvalid;
    wire s1_m2_axi_arready;
    wire [32-1:0] s1_m2_axi_rdata;
    wire [2-1:0] s1_m2_axi_rresp;
    wire s1_m2_axi_rvalid;
    wire s1_m2_axi_rready;
    wire [ID_W-1:0] s1_m2_axi_arid;
    wire [LEN_W-1:0] s1_m2_axi_arlen;
    wire [3-1:0] s1_m2_axi_arsize;
    wire [2-1:0] s1_m2_axi_arburst;
    wire s1_m2_axi_arlock;
    wire [4-1:0] s1_m2_axi_arcache;
    wire [4-1:0] s1_m2_axi_arqos;
    wire [ID_W-1:0] s1_m2_axi_rid;
    wire s1_m2_axi_rlast;
    wire [30-1:0] s1_m2_axi_awaddr;
    wire s1_m2_axi_awvalid;
    wire s1_m2_axi_awready;
    wire [32-1:0] s1_m2_axi_wdata;
    wire [32/8-1:0] s1_m2_axi_wstrb;
    wire s1_m2_axi_wvalid;
    wire s1_m2_axi_wready;
    wire [2-1:0] s1_m2_axi_bresp;
    wire s1_m2_axi_bvalid;
    wire s1_m2_axi_bready;
    wire [ID_W-1:0] s1_m2_axi_awid;
    wire [LEN_W-1:0] s1_m2_axi_awlen;
    wire [3-1:0] s1_m2_axi_awsize;
    wire [2-1:0] s1_m2_axi_awburst;
    wire s1_m2_axi_awlock;
    wire [4-1:0] s1_m2_axi_awcache;
    wire [4-1:0] s1_m2_axi_awqos;
    wire s1_m2_axi_wlast;
    wire [ID_W-1:0] s1_m2_axi_bid;
// Output of merge 0
    wire [31-1:0] merge_0_axi_araddr;
    wire merge_0_axi_arvalid;
    wire merge_0_axi_arready;
    wire [32-1:0] merge_0_axi_rdata;
    wire [2-1:0] merge_0_axi_rresp;
    wire merge_0_axi_rvalid;
    wire merge_0_axi_rready;
    wire [ID_W-1:0] merge_0_axi_arid;
    wire [LEN_W-1:0] merge_0_axi_arlen;
    wire [3-1:0] merge_0_axi_arsize;
    wire [2-1:0] merge_0_axi_arburst;
    wire merge_0_axi_arlock;
    wire [4-1:0] merge_0_axi_arcache;
    wire [4-1:0] merge_0_axi_arqos;
    wire [ID_W-1:0] merge_0_axi_rid;
    wire merge_0_axi_rlast;
    wire [31-1:0] merge_0_axi_awaddr;
    wire merge_0_axi_awvalid;
    wire merge_0_axi_awready;
    wire [32-1:0] merge_0_axi_wdata;
    wire [32/8-1:0] merge_0_axi_wstrb;
    wire merge_0_axi_wvalid;
    wire merge_0_axi_wready;
    wire [2-1:0] merge_0_axi_bresp;
    wire merge_0_axi_bvalid;
    wire merge_0_axi_bready;
    wire [ID_W-1:0] merge_0_axi_awid;
    wire [LEN_W-1:0] merge_0_axi_awlen;
    wire [3-1:0] merge_0_axi_awsize;
    wire [2-1:0] merge_0_axi_awburst;
    wire merge_0_axi_awlock;
    wire [4-1:0] merge_0_axi_awcache;
    wire [4-1:0] merge_0_axi_awqos;
    wire merge_0_axi_wlast;
    wire [ID_W-1:0] merge_0_axi_bid;
// Output of merge 1
    wire [31-1:0] merge_1_axi_araddr;
    wire merge_1_axi_arvalid;
    wire merge_1_axi_arready;
    wire [32-1:0] merge_1_axi_rdata;
    wire [2-1:0] merge_1_axi_rresp;
    wire merge_1_axi_rvalid;
    wire merge_1_axi_rready;
    wire [ID_W-1:0] merge_1_axi_arid;
    wire [LEN_W-1:0] merge_1_axi_arlen;
    wire [3-1:0] merge_1_axi_arsize;
    wire [2-1:0] merge_1_axi_arburst;
    wire merge_1_axi_arlock;
    wire [4-1:0] merge_1_axi_arcache;
    wire [4-1:0] merge_1_axi_arqos;
    wire [ID_W-1:0] merge_1_axi_rid;
    wire merge_1_axi_rlast;
    wire [31-1:0] merge_1_axi_awaddr;
    wire merge_1_axi_awvalid;
    wire merge_1_axi_awready;
    wire [32-1:0] merge_1_axi_wdata;
    wire [32/8-1:0] merge_1_axi_wstrb;
    wire merge_1_axi_wvalid;
    wire merge_1_axi_wready;
    wire [2-1:0] merge_1_axi_bresp;
    wire merge_1_axi_bvalid;
    wire merge_1_axi_bready;
    wire [ID_W-1:0] merge_1_axi_awid;
    wire [LEN_W-1:0] merge_1_axi_awlen;
    wire [3-1:0] merge_1_axi_awsize;
    wire [2-1:0] merge_1_axi_awburst;
    wire merge_1_axi_awlock;
    wire [4-1:0] merge_1_axi_awcache;
    wire [4-1:0] merge_1_axi_awqos;
    wire merge_1_axi_wlast;
    wire [ID_W-1:0] merge_1_axi_bid;
// Output of merge 2
    wire [31-1:0] merge_2_axi_araddr;
    wire merge_2_axi_arvalid;
    wire merge_2_axi_arready;
    wire [32-1:0] merge_2_axi_rdata;
    wire [2-1:0] merge_2_axi_rresp;
    wire merge_2_axi_rvalid;
    wire merge_2_axi_rready;
    wire [ID_W-1:0] merge_2_axi_arid;
    wire [LEN_W-1:0] merge_2_axi_arlen;
    wire [3-1:0] merge_2_axi_arsize;
    wire [2-1:0] merge_2_axi_arburst;
    wire merge_2_axi_arlock;
    wire [4-1:0] merge_2_axi_arcache;
    wire [4-1:0] merge_2_axi_arqos;
    wire [ID_W-1:0] merge_2_axi_rid;
    wire merge_2_axi_rlast;
    wire [31-1:0] merge_2_axi_awaddr;
    wire merge_2_axi_awvalid;
    wire merge_2_axi_awready;
    wire [32-1:0] merge_2_axi_wdata;
    wire [32/8-1:0] merge_2_axi_wstrb;
    wire merge_2_axi_wvalid;
    wire merge_2_axi_wready;
    wire [2-1:0] merge_2_axi_bresp;
    wire merge_2_axi_bvalid;
    wire merge_2_axi_bready;
    wire [ID_W-1:0] merge_2_axi_awid;
    wire [LEN_W-1:0] merge_2_axi_awlen;
    wire [3-1:0] merge_2_axi_awsize;
    wire [2-1:0] merge_2_axi_awburst;
    wire merge_2_axi_awlock;
    wire [4-1:0] merge_2_axi_awcache;
    wire [4-1:0] merge_2_axi_awqos;
    wire merge_2_axi_wlast;
    wire [ID_W-1:0] merge_2_axi_bid;

   assign m0_axi_awvalid_o = merge_0_axi_awvalid;
   assign merge_0_axi_awready = m0_axi_awready_i;
   assign m0_axi_wdata_o = merge_0_axi_wdata;
   assign m0_axi_wstrb_o = merge_0_axi_wstrb;
   assign m0_axi_wvalid_o = merge_0_axi_wvalid;
   assign merge_0_axi_wready = m0_axi_wready_i;
   assign merge_0_axi_bresp = m0_axi_bresp_i;
   assign merge_0_axi_bvalid = m0_axi_bvalid_i;
   assign m0_axi_bready_o = merge_0_axi_bready;
   assign m0_axi_awid_o = merge_0_axi_awid;
   assign m0_axi_awlen_o = merge_0_axi_awlen;
   assign m0_axi_awsize_o = merge_0_axi_awsize;
   assign m0_axi_awburst_o = merge_0_axi_awburst;
   assign m0_axi_awlock_o = merge_0_axi_awlock;
   assign m0_axi_awcache_o = merge_0_axi_awcache;
   assign m0_axi_awqos_o = merge_0_axi_awqos;
   assign m0_axi_wlast_o = merge_0_axi_wlast;
   assign merge_0_axi_bid = m0_axi_bid_i;
   assign m0_axi_arvalid_o = merge_0_axi_arvalid;
   assign merge_0_axi_arready = m0_axi_arready_i;
   assign merge_0_axi_rdata = m0_axi_rdata_i;
   assign merge_0_axi_rresp = m0_axi_rresp_i;
   assign merge_0_axi_rvalid = m0_axi_rvalid_i;
   assign m0_axi_rready_o = merge_0_axi_rready;
   assign m0_axi_arid_o = merge_0_axi_arid;
   assign m0_axi_arlen_o = merge_0_axi_arlen;
   assign m0_axi_arsize_o = merge_0_axi_arsize;
   assign m0_axi_arburst_o = merge_0_axi_arburst;
   assign m0_axi_arlock_o = merge_0_axi_arlock;
   assign m0_axi_arcache_o = merge_0_axi_arcache;
   assign m0_axi_arqos_o = merge_0_axi_arqos;
   assign merge_0_axi_rid = m0_axi_rid_i;
   assign merge_0_axi_rlast = m0_axi_rlast_i;
   assign m0_axi_awaddr_o = { {2{1'b0}}, merge_0_axi_awaddr[30-1:0]};
   assign m0_axi_araddr_o = { {2{1'b0}}, merge_0_axi_araddr[30-1:0]};
   assign m1_axi_awvalid_o = merge_1_axi_awvalid;
   assign merge_1_axi_awready = m1_axi_awready_i;
   assign m1_axi_wdata_o = merge_1_axi_wdata;
   assign m1_axi_wstrb_o = merge_1_axi_wstrb;
   assign m1_axi_wvalid_o = merge_1_axi_wvalid;
   assign merge_1_axi_wready = m1_axi_wready_i;
   assign merge_1_axi_bresp = m1_axi_bresp_i;
   assign merge_1_axi_bvalid = m1_axi_bvalid_i;
   assign m1_axi_bready_o = merge_1_axi_bready;
   assign m1_axi_awid_o = merge_1_axi_awid;
   assign m1_axi_awlen_o = merge_1_axi_awlen;
   assign m1_axi_awsize_o = merge_1_axi_awsize;
   assign m1_axi_awburst_o = merge_1_axi_awburst;
   assign m1_axi_awlock_o = merge_1_axi_awlock;
   assign m1_axi_awcache_o = merge_1_axi_awcache;
   assign m1_axi_awqos_o = merge_1_axi_awqos;
   assign m1_axi_wlast_o = merge_1_axi_wlast;
   assign merge_1_axi_bid = m1_axi_bid_i;
   assign m1_axi_arvalid_o = merge_1_axi_arvalid;
   assign merge_1_axi_arready = m1_axi_arready_i;
   assign merge_1_axi_rdata = m1_axi_rdata_i;
   assign merge_1_axi_rresp = m1_axi_rresp_i;
   assign merge_1_axi_rvalid = m1_axi_rvalid_i;
   assign m1_axi_rready_o = merge_1_axi_rready;
   assign m1_axi_arid_o = merge_1_axi_arid;
   assign m1_axi_arlen_o = merge_1_axi_arlen;
   assign m1_axi_arsize_o = merge_1_axi_arsize;
   assign m1_axi_arburst_o = merge_1_axi_arburst;
   assign m1_axi_arlock_o = merge_1_axi_arlock;
   assign m1_axi_arcache_o = merge_1_axi_arcache;
   assign m1_axi_arqos_o = merge_1_axi_arqos;
   assign merge_1_axi_rid = m1_axi_rid_i;
   assign merge_1_axi_rlast = m1_axi_rlast_i;
   assign m1_axi_awaddr_o = { {2{1'b0}}, merge_1_axi_awaddr[30-1:0]};
   assign m1_axi_araddr_o = { {2{1'b0}}, merge_1_axi_araddr[30-1:0]};
   assign m2_axi_awvalid_o = merge_2_axi_awvalid;
   assign merge_2_axi_awready = m2_axi_awready_i;
   assign m2_axi_wdata_o = merge_2_axi_wdata;
   assign m2_axi_wstrb_o = merge_2_axi_wstrb;
   assign m2_axi_wvalid_o = merge_2_axi_wvalid;
   assign merge_2_axi_wready = m2_axi_wready_i;
   assign merge_2_axi_bresp = m2_axi_bresp_i;
   assign merge_2_axi_bvalid = m2_axi_bvalid_i;
   assign m2_axi_bready_o = merge_2_axi_bready;
   assign m2_axi_awid_o = merge_2_axi_awid;
   assign m2_axi_awlen_o = merge_2_axi_awlen;
   assign m2_axi_awsize_o = merge_2_axi_awsize;
   assign m2_axi_awburst_o = merge_2_axi_awburst;
   assign m2_axi_awlock_o = merge_2_axi_awlock;
   assign m2_axi_awcache_o = merge_2_axi_awcache;
   assign m2_axi_awqos_o = merge_2_axi_awqos;
   assign m2_axi_wlast_o = merge_2_axi_wlast;
   assign merge_2_axi_bid = m2_axi_bid_i;
   assign m2_axi_arvalid_o = merge_2_axi_arvalid;
   assign merge_2_axi_arready = m2_axi_arready_i;
   assign merge_2_axi_rdata = m2_axi_rdata_i;
   assign merge_2_axi_rresp = m2_axi_rresp_i;
   assign merge_2_axi_rvalid = m2_axi_rvalid_i;
   assign m2_axi_rready_o = merge_2_axi_rready;
   assign m2_axi_arid_o = merge_2_axi_arid;
   assign m2_axi_arlen_o = merge_2_axi_arlen;
   assign m2_axi_arsize_o = merge_2_axi_arsize;
   assign m2_axi_arburst_o = merge_2_axi_arburst;
   assign m2_axi_arlock_o = merge_2_axi_arlock;
   assign m2_axi_arcache_o = merge_2_axi_arcache;
   assign m2_axi_arqos_o = merge_2_axi_arqos;
   assign merge_2_axi_rid = m2_axi_rid_i;
   assign merge_2_axi_rlast = m2_axi_rlast_i;
   assign m2_axi_awaddr_o = { {2{1'b0}}, merge_2_axi_awaddr[30-1:0]};
   assign m2_axi_araddr_o = { {2{1'b0}}, merge_2_axi_araddr[30-1:0]};


        // AXI split for subordinate 0
        iob_uart_tester_axi_full_xbar_split #(
        .ID_W(ID_W),
        .LEN_W(LEN_W)
    ) iob_axi_split_0 (
            // clk_en_rst_s port: Clock, clock enable and async reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // reset_i port: Reset signal
        .rst_i(rst_i),
        // s_s port: Split subordinate
        .s_axi_araddr_i(s0_axi_araddr_i),
        .s_axi_arvalid_i(s0_axi_arvalid_i),
        .s_axi_arready_o(s0_axi_arready_o),
        .s_axi_rdata_o(s0_axi_rdata_o),
        .s_axi_rresp_o(s0_axi_rresp_o),
        .s_axi_rvalid_o(s0_axi_rvalid_o),
        .s_axi_rready_i(s0_axi_rready_i),
        .s_axi_arid_i(s0_axi_arid_i),
        .s_axi_arlen_i(s0_axi_arlen_i),
        .s_axi_arsize_i(s0_axi_arsize_i),
        .s_axi_arburst_i(s0_axi_arburst_i),
        .s_axi_arlock_i(s0_axi_arlock_i),
        .s_axi_arcache_i(s0_axi_arcache_i),
        .s_axi_arqos_i(s0_axi_arqos_i),
        .s_axi_rid_o(s0_axi_rid_o),
        .s_axi_rlast_o(s0_axi_rlast_o),
        .s_axi_awaddr_i(s0_axi_awaddr_i),
        .s_axi_awvalid_i(s0_axi_awvalid_i),
        .s_axi_awready_o(s0_axi_awready_o),
        .s_axi_wdata_i(s0_axi_wdata_i),
        .s_axi_wstrb_i(s0_axi_wstrb_i),
        .s_axi_wvalid_i(s0_axi_wvalid_i),
        .s_axi_wready_o(s0_axi_wready_o),
        .s_axi_bresp_o(s0_axi_bresp_o),
        .s_axi_bvalid_o(s0_axi_bvalid_o),
        .s_axi_bready_i(s0_axi_bready_i),
        .s_axi_awid_i(s0_axi_awid_i),
        .s_axi_awlen_i(s0_axi_awlen_i),
        .s_axi_awsize_i(s0_axi_awsize_i),
        .s_axi_awburst_i(s0_axi_awburst_i),
        .s_axi_awlock_i(s0_axi_awlock_i),
        .s_axi_awcache_i(s0_axi_awcache_i),
        .s_axi_awqos_i(s0_axi_awqos_i),
        .s_axi_wlast_i(s0_axi_wlast_i),
        .s_axi_bid_o(s0_axi_bid_o),
        // m_0_m port: Split manager interface
        .m0_axi_araddr_o(s0_m0_axi_araddr),
        .m0_axi_arvalid_o(s0_m0_axi_arvalid),
        .m0_axi_arready_i(s0_m0_axi_arready),
        .m0_axi_rdata_i(s0_m0_axi_rdata),
        .m0_axi_rresp_i(s0_m0_axi_rresp),
        .m0_axi_rvalid_i(s0_m0_axi_rvalid),
        .m0_axi_rready_o(s0_m0_axi_rready),
        .m0_axi_arid_o(s0_m0_axi_arid),
        .m0_axi_arlen_o(s0_m0_axi_arlen),
        .m0_axi_arsize_o(s0_m0_axi_arsize),
        .m0_axi_arburst_o(s0_m0_axi_arburst),
        .m0_axi_arlock_o(s0_m0_axi_arlock),
        .m0_axi_arcache_o(s0_m0_axi_arcache),
        .m0_axi_arqos_o(s0_m0_axi_arqos),
        .m0_axi_rid_i(s0_m0_axi_rid),
        .m0_axi_rlast_i(s0_m0_axi_rlast),
        .m0_axi_awaddr_o(s0_m0_axi_awaddr),
        .m0_axi_awvalid_o(s0_m0_axi_awvalid),
        .m0_axi_awready_i(s0_m0_axi_awready),
        .m0_axi_wdata_o(s0_m0_axi_wdata),
        .m0_axi_wstrb_o(s0_m0_axi_wstrb),
        .m0_axi_wvalid_o(s0_m0_axi_wvalid),
        .m0_axi_wready_i(s0_m0_axi_wready),
        .m0_axi_bresp_i(s0_m0_axi_bresp),
        .m0_axi_bvalid_i(s0_m0_axi_bvalid),
        .m0_axi_bready_o(s0_m0_axi_bready),
        .m0_axi_awid_o(s0_m0_axi_awid),
        .m0_axi_awlen_o(s0_m0_axi_awlen),
        .m0_axi_awsize_o(s0_m0_axi_awsize),
        .m0_axi_awburst_o(s0_m0_axi_awburst),
        .m0_axi_awlock_o(s0_m0_axi_awlock),
        .m0_axi_awcache_o(s0_m0_axi_awcache),
        .m0_axi_awqos_o(s0_m0_axi_awqos),
        .m0_axi_wlast_o(s0_m0_axi_wlast),
        .m0_axi_bid_i(s0_m0_axi_bid),
        // m_1_m port: Split manager interface
        .m1_axi_araddr_o(s0_m1_axi_araddr),
        .m1_axi_arvalid_o(s0_m1_axi_arvalid),
        .m1_axi_arready_i(s0_m1_axi_arready),
        .m1_axi_rdata_i(s0_m1_axi_rdata),
        .m1_axi_rresp_i(s0_m1_axi_rresp),
        .m1_axi_rvalid_i(s0_m1_axi_rvalid),
        .m1_axi_rready_o(s0_m1_axi_rready),
        .m1_axi_arid_o(s0_m1_axi_arid),
        .m1_axi_arlen_o(s0_m1_axi_arlen),
        .m1_axi_arsize_o(s0_m1_axi_arsize),
        .m1_axi_arburst_o(s0_m1_axi_arburst),
        .m1_axi_arlock_o(s0_m1_axi_arlock),
        .m1_axi_arcache_o(s0_m1_axi_arcache),
        .m1_axi_arqos_o(s0_m1_axi_arqos),
        .m1_axi_rid_i(s0_m1_axi_rid),
        .m1_axi_rlast_i(s0_m1_axi_rlast),
        .m1_axi_awaddr_o(s0_m1_axi_awaddr),
        .m1_axi_awvalid_o(s0_m1_axi_awvalid),
        .m1_axi_awready_i(s0_m1_axi_awready),
        .m1_axi_wdata_o(s0_m1_axi_wdata),
        .m1_axi_wstrb_o(s0_m1_axi_wstrb),
        .m1_axi_wvalid_o(s0_m1_axi_wvalid),
        .m1_axi_wready_i(s0_m1_axi_wready),
        .m1_axi_bresp_i(s0_m1_axi_bresp),
        .m1_axi_bvalid_i(s0_m1_axi_bvalid),
        .m1_axi_bready_o(s0_m1_axi_bready),
        .m1_axi_awid_o(s0_m1_axi_awid),
        .m1_axi_awlen_o(s0_m1_axi_awlen),
        .m1_axi_awsize_o(s0_m1_axi_awsize),
        .m1_axi_awburst_o(s0_m1_axi_awburst),
        .m1_axi_awlock_o(s0_m1_axi_awlock),
        .m1_axi_awcache_o(s0_m1_axi_awcache),
        .m1_axi_awqos_o(s0_m1_axi_awqos),
        .m1_axi_wlast_o(s0_m1_axi_wlast),
        .m1_axi_bid_i(s0_m1_axi_bid),
        // m_2_m port: Split manager interface
        .m2_axi_araddr_o(s0_m2_axi_araddr),
        .m2_axi_arvalid_o(s0_m2_axi_arvalid),
        .m2_axi_arready_i(s0_m2_axi_arready),
        .m2_axi_rdata_i(s0_m2_axi_rdata),
        .m2_axi_rresp_i(s0_m2_axi_rresp),
        .m2_axi_rvalid_i(s0_m2_axi_rvalid),
        .m2_axi_rready_o(s0_m2_axi_rready),
        .m2_axi_arid_o(s0_m2_axi_arid),
        .m2_axi_arlen_o(s0_m2_axi_arlen),
        .m2_axi_arsize_o(s0_m2_axi_arsize),
        .m2_axi_arburst_o(s0_m2_axi_arburst),
        .m2_axi_arlock_o(s0_m2_axi_arlock),
        .m2_axi_arcache_o(s0_m2_axi_arcache),
        .m2_axi_arqos_o(s0_m2_axi_arqos),
        .m2_axi_rid_i(s0_m2_axi_rid),
        .m2_axi_rlast_i(s0_m2_axi_rlast),
        .m2_axi_awaddr_o(s0_m2_axi_awaddr),
        .m2_axi_awvalid_o(s0_m2_axi_awvalid),
        .m2_axi_awready_i(s0_m2_axi_awready),
        .m2_axi_wdata_o(s0_m2_axi_wdata),
        .m2_axi_wstrb_o(s0_m2_axi_wstrb),
        .m2_axi_wvalid_o(s0_m2_axi_wvalid),
        .m2_axi_wready_i(s0_m2_axi_wready),
        .m2_axi_bresp_i(s0_m2_axi_bresp),
        .m2_axi_bvalid_i(s0_m2_axi_bvalid),
        .m2_axi_bready_o(s0_m2_axi_bready),
        .m2_axi_awid_o(s0_m2_axi_awid),
        .m2_axi_awlen_o(s0_m2_axi_awlen),
        .m2_axi_awsize_o(s0_m2_axi_awsize),
        .m2_axi_awburst_o(s0_m2_axi_awburst),
        .m2_axi_awlock_o(s0_m2_axi_awlock),
        .m2_axi_awcache_o(s0_m2_axi_awcache),
        .m2_axi_awqos_o(s0_m2_axi_awqos),
        .m2_axi_wlast_o(s0_m2_axi_wlast),
        .m2_axi_bid_i(s0_m2_axi_bid)
        );

            // AXI split for subordinate 1
        iob_uart_tester_axi_full_xbar_split #(
        .ID_W(ID_W),
        .LEN_W(LEN_W)
    ) iob_axi_split_1 (
            // clk_en_rst_s port: Clock, clock enable and async reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // reset_i port: Reset signal
        .rst_i(rst_i),
        // s_s port: Split subordinate
        .s_axi_araddr_i(s1_axi_araddr_i),
        .s_axi_arvalid_i(s1_axi_arvalid_i),
        .s_axi_arready_o(s1_axi_arready_o),
        .s_axi_rdata_o(s1_axi_rdata_o),
        .s_axi_rresp_o(s1_axi_rresp_o),
        .s_axi_rvalid_o(s1_axi_rvalid_o),
        .s_axi_rready_i(s1_axi_rready_i),
        .s_axi_arid_i(s1_axi_arid_i),
        .s_axi_arlen_i(s1_axi_arlen_i),
        .s_axi_arsize_i(s1_axi_arsize_i),
        .s_axi_arburst_i(s1_axi_arburst_i),
        .s_axi_arlock_i(s1_axi_arlock_i),
        .s_axi_arcache_i(s1_axi_arcache_i),
        .s_axi_arqos_i(s1_axi_arqos_i),
        .s_axi_rid_o(s1_axi_rid_o),
        .s_axi_rlast_o(s1_axi_rlast_o),
        .s_axi_awaddr_i(s1_axi_awaddr_i),
        .s_axi_awvalid_i(s1_axi_awvalid_i),
        .s_axi_awready_o(s1_axi_awready_o),
        .s_axi_wdata_i(s1_axi_wdata_i),
        .s_axi_wstrb_i(s1_axi_wstrb_i),
        .s_axi_wvalid_i(s1_axi_wvalid_i),
        .s_axi_wready_o(s1_axi_wready_o),
        .s_axi_bresp_o(s1_axi_bresp_o),
        .s_axi_bvalid_o(s1_axi_bvalid_o),
        .s_axi_bready_i(s1_axi_bready_i),
        .s_axi_awid_i(s1_axi_awid_i),
        .s_axi_awlen_i(s1_axi_awlen_i),
        .s_axi_awsize_i(s1_axi_awsize_i),
        .s_axi_awburst_i(s1_axi_awburst_i),
        .s_axi_awlock_i(s1_axi_awlock_i),
        .s_axi_awcache_i(s1_axi_awcache_i),
        .s_axi_awqos_i(s1_axi_awqos_i),
        .s_axi_wlast_i(s1_axi_wlast_i),
        .s_axi_bid_o(s1_axi_bid_o),
        // m_0_m port: Split manager interface
        .m0_axi_araddr_o(s1_m0_axi_araddr),
        .m0_axi_arvalid_o(s1_m0_axi_arvalid),
        .m0_axi_arready_i(s1_m0_axi_arready),
        .m0_axi_rdata_i(s1_m0_axi_rdata),
        .m0_axi_rresp_i(s1_m0_axi_rresp),
        .m0_axi_rvalid_i(s1_m0_axi_rvalid),
        .m0_axi_rready_o(s1_m0_axi_rready),
        .m0_axi_arid_o(s1_m0_axi_arid),
        .m0_axi_arlen_o(s1_m0_axi_arlen),
        .m0_axi_arsize_o(s1_m0_axi_arsize),
        .m0_axi_arburst_o(s1_m0_axi_arburst),
        .m0_axi_arlock_o(s1_m0_axi_arlock),
        .m0_axi_arcache_o(s1_m0_axi_arcache),
        .m0_axi_arqos_o(s1_m0_axi_arqos),
        .m0_axi_rid_i(s1_m0_axi_rid),
        .m0_axi_rlast_i(s1_m0_axi_rlast),
        .m0_axi_awaddr_o(s1_m0_axi_awaddr),
        .m0_axi_awvalid_o(s1_m0_axi_awvalid),
        .m0_axi_awready_i(s1_m0_axi_awready),
        .m0_axi_wdata_o(s1_m0_axi_wdata),
        .m0_axi_wstrb_o(s1_m0_axi_wstrb),
        .m0_axi_wvalid_o(s1_m0_axi_wvalid),
        .m0_axi_wready_i(s1_m0_axi_wready),
        .m0_axi_bresp_i(s1_m0_axi_bresp),
        .m0_axi_bvalid_i(s1_m0_axi_bvalid),
        .m0_axi_bready_o(s1_m0_axi_bready),
        .m0_axi_awid_o(s1_m0_axi_awid),
        .m0_axi_awlen_o(s1_m0_axi_awlen),
        .m0_axi_awsize_o(s1_m0_axi_awsize),
        .m0_axi_awburst_o(s1_m0_axi_awburst),
        .m0_axi_awlock_o(s1_m0_axi_awlock),
        .m0_axi_awcache_o(s1_m0_axi_awcache),
        .m0_axi_awqos_o(s1_m0_axi_awqos),
        .m0_axi_wlast_o(s1_m0_axi_wlast),
        .m0_axi_bid_i(s1_m0_axi_bid),
        // m_1_m port: Split manager interface
        .m1_axi_araddr_o(s1_m1_axi_araddr),
        .m1_axi_arvalid_o(s1_m1_axi_arvalid),
        .m1_axi_arready_i(s1_m1_axi_arready),
        .m1_axi_rdata_i(s1_m1_axi_rdata),
        .m1_axi_rresp_i(s1_m1_axi_rresp),
        .m1_axi_rvalid_i(s1_m1_axi_rvalid),
        .m1_axi_rready_o(s1_m1_axi_rready),
        .m1_axi_arid_o(s1_m1_axi_arid),
        .m1_axi_arlen_o(s1_m1_axi_arlen),
        .m1_axi_arsize_o(s1_m1_axi_arsize),
        .m1_axi_arburst_o(s1_m1_axi_arburst),
        .m1_axi_arlock_o(s1_m1_axi_arlock),
        .m1_axi_arcache_o(s1_m1_axi_arcache),
        .m1_axi_arqos_o(s1_m1_axi_arqos),
        .m1_axi_rid_i(s1_m1_axi_rid),
        .m1_axi_rlast_i(s1_m1_axi_rlast),
        .m1_axi_awaddr_o(s1_m1_axi_awaddr),
        .m1_axi_awvalid_o(s1_m1_axi_awvalid),
        .m1_axi_awready_i(s1_m1_axi_awready),
        .m1_axi_wdata_o(s1_m1_axi_wdata),
        .m1_axi_wstrb_o(s1_m1_axi_wstrb),
        .m1_axi_wvalid_o(s1_m1_axi_wvalid),
        .m1_axi_wready_i(s1_m1_axi_wready),
        .m1_axi_bresp_i(s1_m1_axi_bresp),
        .m1_axi_bvalid_i(s1_m1_axi_bvalid),
        .m1_axi_bready_o(s1_m1_axi_bready),
        .m1_axi_awid_o(s1_m1_axi_awid),
        .m1_axi_awlen_o(s1_m1_axi_awlen),
        .m1_axi_awsize_o(s1_m1_axi_awsize),
        .m1_axi_awburst_o(s1_m1_axi_awburst),
        .m1_axi_awlock_o(s1_m1_axi_awlock),
        .m1_axi_awcache_o(s1_m1_axi_awcache),
        .m1_axi_awqos_o(s1_m1_axi_awqos),
        .m1_axi_wlast_o(s1_m1_axi_wlast),
        .m1_axi_bid_i(s1_m1_axi_bid),
        // m_2_m port: Split manager interface
        .m2_axi_araddr_o(s1_m2_axi_araddr),
        .m2_axi_arvalid_o(s1_m2_axi_arvalid),
        .m2_axi_arready_i(s1_m2_axi_arready),
        .m2_axi_rdata_i(s1_m2_axi_rdata),
        .m2_axi_rresp_i(s1_m2_axi_rresp),
        .m2_axi_rvalid_i(s1_m2_axi_rvalid),
        .m2_axi_rready_o(s1_m2_axi_rready),
        .m2_axi_arid_o(s1_m2_axi_arid),
        .m2_axi_arlen_o(s1_m2_axi_arlen),
        .m2_axi_arsize_o(s1_m2_axi_arsize),
        .m2_axi_arburst_o(s1_m2_axi_arburst),
        .m2_axi_arlock_o(s1_m2_axi_arlock),
        .m2_axi_arcache_o(s1_m2_axi_arcache),
        .m2_axi_arqos_o(s1_m2_axi_arqos),
        .m2_axi_rid_i(s1_m2_axi_rid),
        .m2_axi_rlast_i(s1_m2_axi_rlast),
        .m2_axi_awaddr_o(s1_m2_axi_awaddr),
        .m2_axi_awvalid_o(s1_m2_axi_awvalid),
        .m2_axi_awready_i(s1_m2_axi_awready),
        .m2_axi_wdata_o(s1_m2_axi_wdata),
        .m2_axi_wstrb_o(s1_m2_axi_wstrb),
        .m2_axi_wvalid_o(s1_m2_axi_wvalid),
        .m2_axi_wready_i(s1_m2_axi_wready),
        .m2_axi_bresp_i(s1_m2_axi_bresp),
        .m2_axi_bvalid_i(s1_m2_axi_bvalid),
        .m2_axi_bready_o(s1_m2_axi_bready),
        .m2_axi_awid_o(s1_m2_axi_awid),
        .m2_axi_awlen_o(s1_m2_axi_awlen),
        .m2_axi_awsize_o(s1_m2_axi_awsize),
        .m2_axi_awburst_o(s1_m2_axi_awburst),
        .m2_axi_awlock_o(s1_m2_axi_awlock),
        .m2_axi_awcache_o(s1_m2_axi_awcache),
        .m2_axi_awqos_o(s1_m2_axi_awqos),
        .m2_axi_wlast_o(s1_m2_axi_wlast),
        .m2_axi_bid_i(s1_m2_axi_bid)
        );

            // AXI merge for manager 0
        iob_uart_tester_axi_full_xbar_merge #(
        .ID_W(ID_W),
        .LEN_W(LEN_W)
    ) iob_axi_merge_0 (
            // clk_en_rst_s port: Clock, clock enable and async reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // reset_i port: Reset signal
        .rst_i(rst_i),
        // s_0_s port: Merge subordinate interfaces
        .s0_axi_araddr_i(s0_m0_axi_araddr),
        .s0_axi_arvalid_i(s0_m0_axi_arvalid),
        .s0_axi_arready_o(s0_m0_axi_arready),
        .s0_axi_rdata_o(s0_m0_axi_rdata),
        .s0_axi_rresp_o(s0_m0_axi_rresp),
        .s0_axi_rvalid_o(s0_m0_axi_rvalid),
        .s0_axi_rready_i(s0_m0_axi_rready),
        .s0_axi_arid_i(s0_m0_axi_arid),
        .s0_axi_arlen_i(s0_m0_axi_arlen),
        .s0_axi_arsize_i(s0_m0_axi_arsize),
        .s0_axi_arburst_i(s0_m0_axi_arburst),
        .s0_axi_arlock_i(s0_m0_axi_arlock),
        .s0_axi_arcache_i(s0_m0_axi_arcache),
        .s0_axi_arqos_i(s0_m0_axi_arqos),
        .s0_axi_rid_o(s0_m0_axi_rid),
        .s0_axi_rlast_o(s0_m0_axi_rlast),
        .s0_axi_awaddr_i(s0_m0_axi_awaddr),
        .s0_axi_awvalid_i(s0_m0_axi_awvalid),
        .s0_axi_awready_o(s0_m0_axi_awready),
        .s0_axi_wdata_i(s0_m0_axi_wdata),
        .s0_axi_wstrb_i(s0_m0_axi_wstrb),
        .s0_axi_wvalid_i(s0_m0_axi_wvalid),
        .s0_axi_wready_o(s0_m0_axi_wready),
        .s0_axi_bresp_o(s0_m0_axi_bresp),
        .s0_axi_bvalid_o(s0_m0_axi_bvalid),
        .s0_axi_bready_i(s0_m0_axi_bready),
        .s0_axi_awid_i(s0_m0_axi_awid),
        .s0_axi_awlen_i(s0_m0_axi_awlen),
        .s0_axi_awsize_i(s0_m0_axi_awsize),
        .s0_axi_awburst_i(s0_m0_axi_awburst),
        .s0_axi_awlock_i(s0_m0_axi_awlock),
        .s0_axi_awcache_i(s0_m0_axi_awcache),
        .s0_axi_awqos_i(s0_m0_axi_awqos),
        .s0_axi_wlast_i(s0_m0_axi_wlast),
        .s0_axi_bid_o(s0_m0_axi_bid),
        // s_1_s port: Merge subordinate interfaces
        .s1_axi_araddr_i(s1_m0_axi_araddr),
        .s1_axi_arvalid_i(s1_m0_axi_arvalid),
        .s1_axi_arready_o(s1_m0_axi_arready),
        .s1_axi_rdata_o(s1_m0_axi_rdata),
        .s1_axi_rresp_o(s1_m0_axi_rresp),
        .s1_axi_rvalid_o(s1_m0_axi_rvalid),
        .s1_axi_rready_i(s1_m0_axi_rready),
        .s1_axi_arid_i(s1_m0_axi_arid),
        .s1_axi_arlen_i(s1_m0_axi_arlen),
        .s1_axi_arsize_i(s1_m0_axi_arsize),
        .s1_axi_arburst_i(s1_m0_axi_arburst),
        .s1_axi_arlock_i(s1_m0_axi_arlock),
        .s1_axi_arcache_i(s1_m0_axi_arcache),
        .s1_axi_arqos_i(s1_m0_axi_arqos),
        .s1_axi_rid_o(s1_m0_axi_rid),
        .s1_axi_rlast_o(s1_m0_axi_rlast),
        .s1_axi_awaddr_i(s1_m0_axi_awaddr),
        .s1_axi_awvalid_i(s1_m0_axi_awvalid),
        .s1_axi_awready_o(s1_m0_axi_awready),
        .s1_axi_wdata_i(s1_m0_axi_wdata),
        .s1_axi_wstrb_i(s1_m0_axi_wstrb),
        .s1_axi_wvalid_i(s1_m0_axi_wvalid),
        .s1_axi_wready_o(s1_m0_axi_wready),
        .s1_axi_bresp_o(s1_m0_axi_bresp),
        .s1_axi_bvalid_o(s1_m0_axi_bvalid),
        .s1_axi_bready_i(s1_m0_axi_bready),
        .s1_axi_awid_i(s1_m0_axi_awid),
        .s1_axi_awlen_i(s1_m0_axi_awlen),
        .s1_axi_awsize_i(s1_m0_axi_awsize),
        .s1_axi_awburst_i(s1_m0_axi_awburst),
        .s1_axi_awlock_i(s1_m0_axi_awlock),
        .s1_axi_awcache_i(s1_m0_axi_awcache),
        .s1_axi_awqos_i(s1_m0_axi_awqos),
        .s1_axi_wlast_i(s1_m0_axi_wlast),
        .s1_axi_bid_o(s1_m0_axi_bid),
        // m_m port: Merge manager
        .m_axi_araddr_o(merge_0_axi_araddr),
        .m_axi_arvalid_o(merge_0_axi_arvalid),
        .m_axi_arready_i(merge_0_axi_arready),
        .m_axi_rdata_i(merge_0_axi_rdata),
        .m_axi_rresp_i(merge_0_axi_rresp),
        .m_axi_rvalid_i(merge_0_axi_rvalid),
        .m_axi_rready_o(merge_0_axi_rready),
        .m_axi_arid_o(merge_0_axi_arid),
        .m_axi_arlen_o(merge_0_axi_arlen),
        .m_axi_arsize_o(merge_0_axi_arsize),
        .m_axi_arburst_o(merge_0_axi_arburst),
        .m_axi_arlock_o(merge_0_axi_arlock),
        .m_axi_arcache_o(merge_0_axi_arcache),
        .m_axi_arqos_o(merge_0_axi_arqos),
        .m_axi_rid_i(merge_0_axi_rid),
        .m_axi_rlast_i(merge_0_axi_rlast),
        .m_axi_awaddr_o(merge_0_axi_awaddr),
        .m_axi_awvalid_o(merge_0_axi_awvalid),
        .m_axi_awready_i(merge_0_axi_awready),
        .m_axi_wdata_o(merge_0_axi_wdata),
        .m_axi_wstrb_o(merge_0_axi_wstrb),
        .m_axi_wvalid_o(merge_0_axi_wvalid),
        .m_axi_wready_i(merge_0_axi_wready),
        .m_axi_bresp_i(merge_0_axi_bresp),
        .m_axi_bvalid_i(merge_0_axi_bvalid),
        .m_axi_bready_o(merge_0_axi_bready),
        .m_axi_awid_o(merge_0_axi_awid),
        .m_axi_awlen_o(merge_0_axi_awlen),
        .m_axi_awsize_o(merge_0_axi_awsize),
        .m_axi_awburst_o(merge_0_axi_awburst),
        .m_axi_awlock_o(merge_0_axi_awlock),
        .m_axi_awcache_o(merge_0_axi_awcache),
        .m_axi_awqos_o(merge_0_axi_awqos),
        .m_axi_wlast_o(merge_0_axi_wlast),
        .m_axi_bid_i(merge_0_axi_bid)
        );

            // AXI merge for manager 1
        iob_uart_tester_axi_full_xbar_merge #(
        .ID_W(ID_W),
        .LEN_W(LEN_W)
    ) iob_axi_merge_1 (
            // clk_en_rst_s port: Clock, clock enable and async reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // reset_i port: Reset signal
        .rst_i(rst_i),
        // s_0_s port: Merge subordinate interfaces
        .s0_axi_araddr_i(s0_m1_axi_araddr),
        .s0_axi_arvalid_i(s0_m1_axi_arvalid),
        .s0_axi_arready_o(s0_m1_axi_arready),
        .s0_axi_rdata_o(s0_m1_axi_rdata),
        .s0_axi_rresp_o(s0_m1_axi_rresp),
        .s0_axi_rvalid_o(s0_m1_axi_rvalid),
        .s0_axi_rready_i(s0_m1_axi_rready),
        .s0_axi_arid_i(s0_m1_axi_arid),
        .s0_axi_arlen_i(s0_m1_axi_arlen),
        .s0_axi_arsize_i(s0_m1_axi_arsize),
        .s0_axi_arburst_i(s0_m1_axi_arburst),
        .s0_axi_arlock_i(s0_m1_axi_arlock),
        .s0_axi_arcache_i(s0_m1_axi_arcache),
        .s0_axi_arqos_i(s0_m1_axi_arqos),
        .s0_axi_rid_o(s0_m1_axi_rid),
        .s0_axi_rlast_o(s0_m1_axi_rlast),
        .s0_axi_awaddr_i(s0_m1_axi_awaddr),
        .s0_axi_awvalid_i(s0_m1_axi_awvalid),
        .s0_axi_awready_o(s0_m1_axi_awready),
        .s0_axi_wdata_i(s0_m1_axi_wdata),
        .s0_axi_wstrb_i(s0_m1_axi_wstrb),
        .s0_axi_wvalid_i(s0_m1_axi_wvalid),
        .s0_axi_wready_o(s0_m1_axi_wready),
        .s0_axi_bresp_o(s0_m1_axi_bresp),
        .s0_axi_bvalid_o(s0_m1_axi_bvalid),
        .s0_axi_bready_i(s0_m1_axi_bready),
        .s0_axi_awid_i(s0_m1_axi_awid),
        .s0_axi_awlen_i(s0_m1_axi_awlen),
        .s0_axi_awsize_i(s0_m1_axi_awsize),
        .s0_axi_awburst_i(s0_m1_axi_awburst),
        .s0_axi_awlock_i(s0_m1_axi_awlock),
        .s0_axi_awcache_i(s0_m1_axi_awcache),
        .s0_axi_awqos_i(s0_m1_axi_awqos),
        .s0_axi_wlast_i(s0_m1_axi_wlast),
        .s0_axi_bid_o(s0_m1_axi_bid),
        // s_1_s port: Merge subordinate interfaces
        .s1_axi_araddr_i(s1_m1_axi_araddr),
        .s1_axi_arvalid_i(s1_m1_axi_arvalid),
        .s1_axi_arready_o(s1_m1_axi_arready),
        .s1_axi_rdata_o(s1_m1_axi_rdata),
        .s1_axi_rresp_o(s1_m1_axi_rresp),
        .s1_axi_rvalid_o(s1_m1_axi_rvalid),
        .s1_axi_rready_i(s1_m1_axi_rready),
        .s1_axi_arid_i(s1_m1_axi_arid),
        .s1_axi_arlen_i(s1_m1_axi_arlen),
        .s1_axi_arsize_i(s1_m1_axi_arsize),
        .s1_axi_arburst_i(s1_m1_axi_arburst),
        .s1_axi_arlock_i(s1_m1_axi_arlock),
        .s1_axi_arcache_i(s1_m1_axi_arcache),
        .s1_axi_arqos_i(s1_m1_axi_arqos),
        .s1_axi_rid_o(s1_m1_axi_rid),
        .s1_axi_rlast_o(s1_m1_axi_rlast),
        .s1_axi_awaddr_i(s1_m1_axi_awaddr),
        .s1_axi_awvalid_i(s1_m1_axi_awvalid),
        .s1_axi_awready_o(s1_m1_axi_awready),
        .s1_axi_wdata_i(s1_m1_axi_wdata),
        .s1_axi_wstrb_i(s1_m1_axi_wstrb),
        .s1_axi_wvalid_i(s1_m1_axi_wvalid),
        .s1_axi_wready_o(s1_m1_axi_wready),
        .s1_axi_bresp_o(s1_m1_axi_bresp),
        .s1_axi_bvalid_o(s1_m1_axi_bvalid),
        .s1_axi_bready_i(s1_m1_axi_bready),
        .s1_axi_awid_i(s1_m1_axi_awid),
        .s1_axi_awlen_i(s1_m1_axi_awlen),
        .s1_axi_awsize_i(s1_m1_axi_awsize),
        .s1_axi_awburst_i(s1_m1_axi_awburst),
        .s1_axi_awlock_i(s1_m1_axi_awlock),
        .s1_axi_awcache_i(s1_m1_axi_awcache),
        .s1_axi_awqos_i(s1_m1_axi_awqos),
        .s1_axi_wlast_i(s1_m1_axi_wlast),
        .s1_axi_bid_o(s1_m1_axi_bid),
        // m_m port: Merge manager
        .m_axi_araddr_o(merge_1_axi_araddr),
        .m_axi_arvalid_o(merge_1_axi_arvalid),
        .m_axi_arready_i(merge_1_axi_arready),
        .m_axi_rdata_i(merge_1_axi_rdata),
        .m_axi_rresp_i(merge_1_axi_rresp),
        .m_axi_rvalid_i(merge_1_axi_rvalid),
        .m_axi_rready_o(merge_1_axi_rready),
        .m_axi_arid_o(merge_1_axi_arid),
        .m_axi_arlen_o(merge_1_axi_arlen),
        .m_axi_arsize_o(merge_1_axi_arsize),
        .m_axi_arburst_o(merge_1_axi_arburst),
        .m_axi_arlock_o(merge_1_axi_arlock),
        .m_axi_arcache_o(merge_1_axi_arcache),
        .m_axi_arqos_o(merge_1_axi_arqos),
        .m_axi_rid_i(merge_1_axi_rid),
        .m_axi_rlast_i(merge_1_axi_rlast),
        .m_axi_awaddr_o(merge_1_axi_awaddr),
        .m_axi_awvalid_o(merge_1_axi_awvalid),
        .m_axi_awready_i(merge_1_axi_awready),
        .m_axi_wdata_o(merge_1_axi_wdata),
        .m_axi_wstrb_o(merge_1_axi_wstrb),
        .m_axi_wvalid_o(merge_1_axi_wvalid),
        .m_axi_wready_i(merge_1_axi_wready),
        .m_axi_bresp_i(merge_1_axi_bresp),
        .m_axi_bvalid_i(merge_1_axi_bvalid),
        .m_axi_bready_o(merge_1_axi_bready),
        .m_axi_awid_o(merge_1_axi_awid),
        .m_axi_awlen_o(merge_1_axi_awlen),
        .m_axi_awsize_o(merge_1_axi_awsize),
        .m_axi_awburst_o(merge_1_axi_awburst),
        .m_axi_awlock_o(merge_1_axi_awlock),
        .m_axi_awcache_o(merge_1_axi_awcache),
        .m_axi_awqos_o(merge_1_axi_awqos),
        .m_axi_wlast_o(merge_1_axi_wlast),
        .m_axi_bid_i(merge_1_axi_bid)
        );

            // AXI merge for manager 2
        iob_uart_tester_axi_full_xbar_merge #(
        .ID_W(ID_W),
        .LEN_W(LEN_W)
    ) iob_axi_merge_2 (
            // clk_en_rst_s port: Clock, clock enable and async reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // reset_i port: Reset signal
        .rst_i(rst_i),
        // s_0_s port: Merge subordinate interfaces
        .s0_axi_araddr_i(s0_m2_axi_araddr),
        .s0_axi_arvalid_i(s0_m2_axi_arvalid),
        .s0_axi_arready_o(s0_m2_axi_arready),
        .s0_axi_rdata_o(s0_m2_axi_rdata),
        .s0_axi_rresp_o(s0_m2_axi_rresp),
        .s0_axi_rvalid_o(s0_m2_axi_rvalid),
        .s0_axi_rready_i(s0_m2_axi_rready),
        .s0_axi_arid_i(s0_m2_axi_arid),
        .s0_axi_arlen_i(s0_m2_axi_arlen),
        .s0_axi_arsize_i(s0_m2_axi_arsize),
        .s0_axi_arburst_i(s0_m2_axi_arburst),
        .s0_axi_arlock_i(s0_m2_axi_arlock),
        .s0_axi_arcache_i(s0_m2_axi_arcache),
        .s0_axi_arqos_i(s0_m2_axi_arqos),
        .s0_axi_rid_o(s0_m2_axi_rid),
        .s0_axi_rlast_o(s0_m2_axi_rlast),
        .s0_axi_awaddr_i(s0_m2_axi_awaddr),
        .s0_axi_awvalid_i(s0_m2_axi_awvalid),
        .s0_axi_awready_o(s0_m2_axi_awready),
        .s0_axi_wdata_i(s0_m2_axi_wdata),
        .s0_axi_wstrb_i(s0_m2_axi_wstrb),
        .s0_axi_wvalid_i(s0_m2_axi_wvalid),
        .s0_axi_wready_o(s0_m2_axi_wready),
        .s0_axi_bresp_o(s0_m2_axi_bresp),
        .s0_axi_bvalid_o(s0_m2_axi_bvalid),
        .s0_axi_bready_i(s0_m2_axi_bready),
        .s0_axi_awid_i(s0_m2_axi_awid),
        .s0_axi_awlen_i(s0_m2_axi_awlen),
        .s0_axi_awsize_i(s0_m2_axi_awsize),
        .s0_axi_awburst_i(s0_m2_axi_awburst),
        .s0_axi_awlock_i(s0_m2_axi_awlock),
        .s0_axi_awcache_i(s0_m2_axi_awcache),
        .s0_axi_awqos_i(s0_m2_axi_awqos),
        .s0_axi_wlast_i(s0_m2_axi_wlast),
        .s0_axi_bid_o(s0_m2_axi_bid),
        // s_1_s port: Merge subordinate interfaces
        .s1_axi_araddr_i(s1_m2_axi_araddr),
        .s1_axi_arvalid_i(s1_m2_axi_arvalid),
        .s1_axi_arready_o(s1_m2_axi_arready),
        .s1_axi_rdata_o(s1_m2_axi_rdata),
        .s1_axi_rresp_o(s1_m2_axi_rresp),
        .s1_axi_rvalid_o(s1_m2_axi_rvalid),
        .s1_axi_rready_i(s1_m2_axi_rready),
        .s1_axi_arid_i(s1_m2_axi_arid),
        .s1_axi_arlen_i(s1_m2_axi_arlen),
        .s1_axi_arsize_i(s1_m2_axi_arsize),
        .s1_axi_arburst_i(s1_m2_axi_arburst),
        .s1_axi_arlock_i(s1_m2_axi_arlock),
        .s1_axi_arcache_i(s1_m2_axi_arcache),
        .s1_axi_arqos_i(s1_m2_axi_arqos),
        .s1_axi_rid_o(s1_m2_axi_rid),
        .s1_axi_rlast_o(s1_m2_axi_rlast),
        .s1_axi_awaddr_i(s1_m2_axi_awaddr),
        .s1_axi_awvalid_i(s1_m2_axi_awvalid),
        .s1_axi_awready_o(s1_m2_axi_awready),
        .s1_axi_wdata_i(s1_m2_axi_wdata),
        .s1_axi_wstrb_i(s1_m2_axi_wstrb),
        .s1_axi_wvalid_i(s1_m2_axi_wvalid),
        .s1_axi_wready_o(s1_m2_axi_wready),
        .s1_axi_bresp_o(s1_m2_axi_bresp),
        .s1_axi_bvalid_o(s1_m2_axi_bvalid),
        .s1_axi_bready_i(s1_m2_axi_bready),
        .s1_axi_awid_i(s1_m2_axi_awid),
        .s1_axi_awlen_i(s1_m2_axi_awlen),
        .s1_axi_awsize_i(s1_m2_axi_awsize),
        .s1_axi_awburst_i(s1_m2_axi_awburst),
        .s1_axi_awlock_i(s1_m2_axi_awlock),
        .s1_axi_awcache_i(s1_m2_axi_awcache),
        .s1_axi_awqos_i(s1_m2_axi_awqos),
        .s1_axi_wlast_i(s1_m2_axi_wlast),
        .s1_axi_bid_o(s1_m2_axi_bid),
        // m_m port: Merge manager
        .m_axi_araddr_o(merge_2_axi_araddr),
        .m_axi_arvalid_o(merge_2_axi_arvalid),
        .m_axi_arready_i(merge_2_axi_arready),
        .m_axi_rdata_i(merge_2_axi_rdata),
        .m_axi_rresp_i(merge_2_axi_rresp),
        .m_axi_rvalid_i(merge_2_axi_rvalid),
        .m_axi_rready_o(merge_2_axi_rready),
        .m_axi_arid_o(merge_2_axi_arid),
        .m_axi_arlen_o(merge_2_axi_arlen),
        .m_axi_arsize_o(merge_2_axi_arsize),
        .m_axi_arburst_o(merge_2_axi_arburst),
        .m_axi_arlock_o(merge_2_axi_arlock),
        .m_axi_arcache_o(merge_2_axi_arcache),
        .m_axi_arqos_o(merge_2_axi_arqos),
        .m_axi_rid_i(merge_2_axi_rid),
        .m_axi_rlast_i(merge_2_axi_rlast),
        .m_axi_awaddr_o(merge_2_axi_awaddr),
        .m_axi_awvalid_o(merge_2_axi_awvalid),
        .m_axi_awready_i(merge_2_axi_awready),
        .m_axi_wdata_o(merge_2_axi_wdata),
        .m_axi_wstrb_o(merge_2_axi_wstrb),
        .m_axi_wvalid_o(merge_2_axi_wvalid),
        .m_axi_wready_i(merge_2_axi_wready),
        .m_axi_bresp_i(merge_2_axi_bresp),
        .m_axi_bvalid_i(merge_2_axi_bvalid),
        .m_axi_bready_o(merge_2_axi_bready),
        .m_axi_awid_o(merge_2_axi_awid),
        .m_axi_awlen_o(merge_2_axi_awlen),
        .m_axi_awsize_o(merge_2_axi_awsize),
        .m_axi_awburst_o(merge_2_axi_awburst),
        .m_axi_awlock_o(merge_2_axi_awlock),
        .m_axi_awcache_o(merge_2_axi_awcache),
        .m_axi_awqos_o(merge_2_axi_awqos),
        .m_axi_wlast_o(merge_2_axi_wlast),
        .m_axi_bid_i(merge_2_axi_bid)
        );

    
endmodule
