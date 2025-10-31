// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_axi_full_xbar_merge_conf.vh"

module iob_uart_tester_axi_full_xbar_merge #(
    parameter ID_W = `IOB_UART_TESTER_AXI_FULL_XBAR_MERGE_ID_W,
    parameter LEN_W = `IOB_UART_TESTER_AXI_FULL_XBAR_MERGE_LEN_W
) (
    // clk_en_rst_s: Clock, clock enable and async reset
    input clk_i,
    input cke_i,
    input arst_i,
    // reset_i: Reset signal
    input rst_i,
    // m_m: Merge manager
    output [31-1:0] m_axi_araddr_o,
    output m_axi_arvalid_o,
    input m_axi_arready_i,
    input [32-1:0] m_axi_rdata_i,
    input [2-1:0] m_axi_rresp_i,
    input m_axi_rvalid_i,
    output m_axi_rready_o,
    output [ID_W-1:0] m_axi_arid_o,
    output [LEN_W-1:0] m_axi_arlen_o,
    output [3-1:0] m_axi_arsize_o,
    output [2-1:0] m_axi_arburst_o,
    output m_axi_arlock_o,
    output [4-1:0] m_axi_arcache_o,
    output [4-1:0] m_axi_arqos_o,
    input [ID_W-1:0] m_axi_rid_i,
    input m_axi_rlast_i,
    output [31-1:0] m_axi_awaddr_o,
    output m_axi_awvalid_o,
    input m_axi_awready_i,
    output [32-1:0] m_axi_wdata_o,
    output [32/8-1:0] m_axi_wstrb_o,
    output m_axi_wvalid_o,
    input m_axi_wready_i,
    input [2-1:0] m_axi_bresp_i,
    input m_axi_bvalid_i,
    output m_axi_bready_o,
    output [ID_W-1:0] m_axi_awid_o,
    output [LEN_W-1:0] m_axi_awlen_o,
    output [3-1:0] m_axi_awsize_o,
    output [2-1:0] m_axi_awburst_o,
    output m_axi_awlock_o,
    output [4-1:0] m_axi_awcache_o,
    output [4-1:0] m_axi_awqos_o,
    output m_axi_wlast_o,
    input [ID_W-1:0] m_axi_bid_i,
    // s_0_s: Merge subordinate interfaces
    input [30-1:0] s0_axi_araddr_i,
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
    input [30-1:0] s0_axi_awaddr_i,
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
    // s_1_s: Merge subordinate interfaces
    input [30-1:0] s1_axi_araddr_i,
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
    input [30-1:0] s1_axi_awaddr_i,
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

// Enable and reset signal for busy_read_reg
    wire busy_read_reg_en;
    wire busy_read_reg_rst;
// Input of busy_read_reg
    wire busy_read_reg_i;
// Output of busy_read_reg
    wire busy_read_reg_o;
// Enable and reset signal for active_transaction_read_reg
    wire active_transaction_read_reg_en;
    wire active_transaction_read_reg_rst;
// Input of active_transaction_read_reg
    wire active_transaction_read_reg_i;
// Output of active_transaction_read_reg
    wire active_transaction_read_reg_o;
// Input of read_sel_reg
    wire read_sel;
// Output of read_sel_reg
    wire read_sel_reg;
// Enable and reset signal for busy_write_reg
    wire busy_write_reg_en;
    wire busy_write_reg_rst;
// Input of busy_write_reg
    wire busy_write_reg_i;
// Output of busy_write_reg
    wire busy_write_reg_o;
// Signals to allow address valid/ready
    wire wants_change_write_sel;
    wire allow_write_address;
// Enable and reset signal for active_write_transaction_acc
    wire active_write_transaction_acc_en;
// Input of active_write_transaction_acc
    wire [5-1:0] active_write_transaction_acc_input;
// Output of active_write_transaction_acc
    wire [5-1:0] active_write_transaction_count;
// Check for any active write transactions
    wire active_write_transaction;
// Start and end signals of active write transaction
    wire start_active_write_transaction;
    wire end_active_write_transaction;
// Check if active write accumulator is full
    wire full_active_write_transaction;
// Signal to allow data valid/ready
    wire allow_write_data;
// Enable and reset signal for pending_write_response_acc
    wire pending_write_response_acc_en;
// Input of pending_write_response_acc
    wire [5-1:0] pending_write_response_acc_input;
// Output of pending_write_response_acc
    wire [5-1:0] pending_write_response_count;
// Check for any active write transactions
    wire pending_write_response;
// Start and end signals of active write transaction
    wire start_pending_write_response;
    wire end_pending_write_response;
// Check if pending write accumulator is full
    wire full_pending_write_response;
// Input of write_sel_reg
    wire write_sel;
// Output of write_sel_reg
    wire write_sel_reg;
// Input of read priority encoder
    wire [2 * 1-1:0] mux_axi_arvalid;
// Output of read priority encoder
    wire [$clog2(2+1)-1:0] read_sel_prio_enc_o;
// Input of write priority encoder
    wire [2 * 1-1:0] mux_axi_awvalid;
// Output of write priority encoder
    wire [$clog2(2+1)-1:0] write_sel_prio_enc_o;
// Input of axi_awaddr demux
    wire [2 * 31-1:0] mux_axi_awaddr;
// Output of axi_awvalid demux
    wire mux_axi_awvalid_o;
// Input of axi_awready demux
    wire demux_axi_awready_i;
// Output of axi_awready demux
    wire [2 * 1-1:0] demux_axi_awready;
// Input of axi_wdata demux
    wire [2 * 32-1:0] mux_axi_wdata;
// Input of axi_wstrb demux
    wire [2 * 4-1:0] mux_axi_wstrb;
// Input of axi_wvalid demux
    wire [2 * 1-1:0] mux_axi_wvalid;
// Output of axi_wvalid demux
    wire mux_axi_wvalid_o;
// Input of axi_wready demux
    wire demux_axi_wready_i;
// Output of axi_wready demux
    wire [2 * 1-1:0] demux_axi_wready;
// Output of axi_bresp demux
    wire [2 * 2-1:0] demux_axi_bresp;
// Output of axi_bvalid demux
    wire [2 * 1-1:0] demux_axi_bvalid;
// Input of axi_bready demux
    wire [2 * 1-1:0] mux_axi_bready;
// Input of axi_awid demux
    wire [2 * ID_W-1:0] mux_axi_awid;
// Input of axi_awlen demux
    wire [2 * LEN_W-1:0] mux_axi_awlen;
// Input of axi_awsize demux
    wire [2 * 3-1:0] mux_axi_awsize;
// Input of axi_awburst demux
    wire [2 * 2-1:0] mux_axi_awburst;
// Input of axi_awlock demux
    wire [2 * 1-1:0] mux_axi_awlock;
// Input of axi_awcache demux
    wire [2 * 4-1:0] mux_axi_awcache;
// Input of axi_awqos demux
    wire [2 * 4-1:0] mux_axi_awqos;
// Input of axi_wlast demux
    wire [2 * 1-1:0] mux_axi_wlast;
// Output of axi_bid demux
    wire [2 * ID_W-1:0] demux_axi_bid;
// Input of axi_araddr demux
    wire [2 * 31-1:0] mux_axi_araddr;
// Output of axi_arvalid demux
    wire mux_axi_arvalid_o;
// Input of axi_arready demux
    wire demux_axi_arready_i;
// Output of axi_arready demux
    wire [2 * 1-1:0] demux_axi_arready;
// Output of axi_rdata demux
    wire [2 * 32-1:0] demux_axi_rdata;
// Output of axi_rresp demux
    wire [2 * 2-1:0] demux_axi_rresp;
// Output of axi_rvalid demux
    wire [2 * 1-1:0] demux_axi_rvalid;
// Input of axi_rready demux
    wire [2 * 1-1:0] mux_axi_rready;
// Input of axi_arid demux
    wire [2 * ID_W-1:0] mux_axi_arid;
// Input of axi_arlen demux
    wire [2 * LEN_W-1:0] mux_axi_arlen;
// Input of axi_arsize demux
    wire [2 * 3-1:0] mux_axi_arsize;
// Input of axi_arburst demux
    wire [2 * 2-1:0] mux_axi_arburst;
// Input of axi_arlock demux
    wire [2 * 1-1:0] mux_axi_arlock;
// Input of axi_arcache demux
    wire [2 * 4-1:0] mux_axi_arcache;
// Input of axi_arqos demux
    wire [2 * 4-1:0] mux_axi_arqos;
// Output of axi_rid demux
    wire [2 * ID_W-1:0] demux_axi_rid;
// Output of axi_rlast demux
    wire [2 * 1-1:0] demux_axi_rlast;


   //
   // Read
   //

   // Only switch managers when there is no current active transaction
   assign read_sel = busy_read_reg_o ? read_sel_reg : read_sel_prio_enc_o[1-1:0];

   assign busy_read_reg_en = m_axi_arvalid_o & !busy_read_reg_o;
   assign busy_read_reg_rst = (m_axi_rlast_i & m_axi_rvalid_i & m_axi_rready_o) | rst_i;
   assign busy_read_reg_i = 1'b1;

   // Block address valid/ready signals of current manager if there is still an active transaction
   assign m_axi_arvalid_o = ~active_transaction_read_reg_o & mux_axi_arvalid_o;
   assign demux_axi_arready_i = ~active_transaction_read_reg_o & m_axi_arready_i;

   assign active_transaction_read_reg_en = m_axi_arvalid_o & m_axi_arready_i;
   assign active_transaction_read_reg_rst = busy_read_reg_rst;
   assign active_transaction_read_reg_i = 1'b1;

   //
   // Write
   //

   // NOTE: Current logic does not allow wvalid to be asserted before awvalid!
   //       If the wvalid comes before, the data will go to the currently selected manager_interface, and that may not be the intended destination (real destination will be given later by awvalid)

   // Only switch managers when there is no current active transaction
   assign write_sel = (busy_write_reg_o | active_write_transaction) ? write_sel_reg : write_sel_prio_enc_o[1-1:0];

   assign busy_write_reg_en = m_axi_awvalid_o & !busy_write_reg_o;
   assign busy_write_reg_rst = end_pending_write_response;
   assign busy_write_reg_i = 1'b1;

   // Block address valid/ready signals of current manager if accumulator full or if another manager wants to write
   assign wants_change_write_sel = write_sel != write_sel_prio_enc_o;
   assign allow_write_address = ~(full_active_write_transaction | (active_write_transaction & wants_change_write_sel));
   assign m_axi_awvalid_o = allow_write_address & mux_axi_awvalid_o;
   assign demux_axi_awready_i = allow_write_address & m_axi_awready_i;

   assign start_active_write_transaction = m_axi_awvalid_o & m_axi_awready_i;
   assign end_active_write_transaction = end_pending_write_response;
   assign active_write_transaction = |active_write_transaction_count;
   assign full_active_write_transaction = &active_write_transaction_count;

   // iob_acc inputs
   assign active_write_transaction_acc_en = start_active_write_transaction ^ end_active_write_transaction;
   assign active_write_transaction_acc_input = start_active_write_transaction ? 5'd1 : -5'd1;

   // Block data valid/ready signals of current manager if accumulator full or if another manager wants to write
   assign allow_write_data = ~(full_pending_write_response | (pending_write_response & wants_change_write_sel));
   assign m_axi_wvalid_o = allow_write_data & mux_axi_wvalid_o;
   assign demux_axi_wready_i = allow_write_data & m_axi_wready_i;

   assign start_pending_write_response = m_axi_wlast_o & m_axi_wvalid_o & m_axi_wready_i;
   assign end_pending_write_response = m_axi_bvalid_i & m_axi_bready_o;
   assign pending_write_response = |pending_write_response_count;
   assign full_pending_write_response = &pending_write_response_count;

   // iob_acc inputs
   assign pending_write_response_acc_en = start_pending_write_response ^ end_pending_write_response;
   assign pending_write_response_acc_input = start_pending_write_response ? 5'd1 : -5'd1;

   assign mux_axi_awaddr = {{1'd1}, s1_axi_awaddr_i, {1'd0}, s0_axi_awaddr_i};
   assign mux_axi_awvalid = {s1_axi_awvalid_i, s0_axi_awvalid_i};

   assign s0_axi_awready_o = demux_axi_awready[0*1+:1];

   assign s1_axi_awready_o = demux_axi_awready[1*1+:1];
   assign mux_axi_wdata = {s1_axi_wdata_i, s0_axi_wdata_i};
   assign mux_axi_wstrb = {s1_axi_wstrb_i, s0_axi_wstrb_i};
   assign mux_axi_wvalid = {s1_axi_wvalid_i, s0_axi_wvalid_i};

   assign s0_axi_wready_o = demux_axi_wready[0*1+:1];

   assign s1_axi_wready_o = demux_axi_wready[1*1+:1];

   assign s0_axi_bresp_o = demux_axi_bresp[0*2+:2];

   assign s1_axi_bresp_o = demux_axi_bresp[1*2+:2];

   assign s0_axi_bvalid_o = demux_axi_bvalid[0*1+:1];

   assign s1_axi_bvalid_o = demux_axi_bvalid[1*1+:1];
   assign mux_axi_bready = {s1_axi_bready_i, s0_axi_bready_i};
   assign mux_axi_awid = {s1_axi_awid_i, s0_axi_awid_i};
   assign mux_axi_awlen = {s1_axi_awlen_i, s0_axi_awlen_i};
   assign mux_axi_awsize = {s1_axi_awsize_i, s0_axi_awsize_i};
   assign mux_axi_awburst = {s1_axi_awburst_i, s0_axi_awburst_i};
   assign mux_axi_awlock = {s1_axi_awlock_i, s0_axi_awlock_i};
   assign mux_axi_awcache = {s1_axi_awcache_i, s0_axi_awcache_i};
   assign mux_axi_awqos = {s1_axi_awqos_i, s0_axi_awqos_i};
   assign mux_axi_wlast = {s1_axi_wlast_i, s0_axi_wlast_i};

   assign s0_axi_bid_o = demux_axi_bid[0*ID_W+:ID_W];

   assign s1_axi_bid_o = demux_axi_bid[1*ID_W+:ID_W];
   assign mux_axi_araddr = {{1'd1}, s1_axi_araddr_i, {1'd0}, s0_axi_araddr_i};
   assign mux_axi_arvalid = {s1_axi_arvalid_i, s0_axi_arvalid_i};

   assign s0_axi_arready_o = demux_axi_arready[0*1+:1];

   assign s1_axi_arready_o = demux_axi_arready[1*1+:1];

   assign s0_axi_rdata_o = demux_axi_rdata[0*32+:32];

   assign s1_axi_rdata_o = demux_axi_rdata[1*32+:32];

   assign s0_axi_rresp_o = demux_axi_rresp[0*2+:2];

   assign s1_axi_rresp_o = demux_axi_rresp[1*2+:2];

   assign s0_axi_rvalid_o = demux_axi_rvalid[0*1+:1];

   assign s1_axi_rvalid_o = demux_axi_rvalid[1*1+:1];
   assign mux_axi_rready = {s1_axi_rready_i, s0_axi_rready_i};
   assign mux_axi_arid = {s1_axi_arid_i, s0_axi_arid_i};
   assign mux_axi_arlen = {s1_axi_arlen_i, s0_axi_arlen_i};
   assign mux_axi_arsize = {s1_axi_arsize_i, s0_axi_arsize_i};
   assign mux_axi_arburst = {s1_axi_arburst_i, s0_axi_arburst_i};
   assign mux_axi_arlock = {s1_axi_arlock_i, s0_axi_arlock_i};
   assign mux_axi_arcache = {s1_axi_arcache_i, s0_axi_arcache_i};
   assign mux_axi_arqos = {s1_axi_arqos_i, s0_axi_arqos_i};

   assign s0_axi_rid_o = demux_axi_rid[0*ID_W+:ID_W];

   assign s1_axi_rid_o = demux_axi_rid[1*ID_W+:ID_W];

   assign s0_axi_rlast_o = demux_axi_rlast[0*1+:1];

   assign s1_axi_rlast_o = demux_axi_rlast[1*1+:1];


        // Default description
        iob_reg_care #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) busy_read_reg_re (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(busy_read_reg_rst),
        .en_i(busy_read_reg_en),
        // data_i port: Data input
        .data_i(busy_read_reg_i),
        // data_o port: Data output
        .data_o(busy_read_reg_o)
        );

            // Default description
        iob_reg_care #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) active_transaction_read_reg_re (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(active_transaction_read_reg_rst),
        .en_i(active_transaction_read_reg_en),
        // data_i port: Data input
        .data_i(active_transaction_read_reg_i),
        // data_o port: Data output
        .data_o(active_transaction_read_reg_o)
        );

            // Default description
        iob_reg_car #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) read_sel_reg_r (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(rst_i),
        // data_i port: Data input
        .data_i(read_sel),
        // data_o port: Data output
        .data_o(read_sel_reg)
        );

            // Default description
        iob_prio_enc #(
        .W(2),
        .MODE("HIGH")
    ) read_sel_enc (
            // unencoded_i port: Input port
        .unencoded_i(mux_axi_arvalid),
        // encoded_o port: Output port
        .encoded_o(read_sel_prio_enc_o)
        );

            // Default description
        iob_reg_care #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) busy_write_reg_re (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(busy_write_reg_rst),
        .en_i(busy_write_reg_en),
        // data_i port: Data input
        .data_i(busy_write_reg_i),
        // data_o port: Data output
        .data_o(busy_write_reg_o)
        );

            // Default description
        iob_acc #(
        .DATA_W(5)
    ) active_write_transaction_acc (
            // clk_en_rst_s port: clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // en_rst_i port: Enable and Synchronous reset interface
        .en_i(active_write_transaction_acc_en),
        .rst_i(rst_i),
        // incr_i port: Input port
        .incr_i(active_write_transaction_acc_input),
        // data_o port: Output port
        .data_o(active_write_transaction_count)
        );

            // Default description
        iob_acc #(
        .DATA_W(5)
    ) pending_write_response_acc (
            // clk_en_rst_s port: clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // en_rst_i port: Enable and Synchronous reset interface
        .en_i(pending_write_response_acc_en),
        .rst_i(rst_i),
        // incr_i port: Input port
        .incr_i(pending_write_response_acc_input),
        // data_o port: Output port
        .data_o(pending_write_response_count)
        );

            // Default description
        iob_reg_car #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) write_sel_reg_r (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(rst_i),
        // data_i port: Data input
        .data_i(write_sel),
        // data_o port: Data output
        .data_o(write_sel_reg)
        );

            // Default description
        iob_prio_enc #(
        .W(2),
        .MODE("HIGH")
    ) write_sel_enc (
            // unencoded_i port: Input port
        .unencoded_i(mux_axi_awvalid),
        // encoded_o port: Output port
        .encoded_o(write_sel_prio_enc_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(31),
        .N(2)
    ) iob_mux_axi_awaddr (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awaddr),
        // data_o port: Output port
        .data_o(m_axi_awaddr_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_awvalid (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awvalid),
        // data_o port: Output port
        .data_o(mux_axi_awvalid_o)
        );

            // Default description
        iob_demux #(
        .DATA_W(1),
        .N(2)
    ) iob_demux_axi_awready (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(demux_axi_awready_i),
        // data_o port: Output port
        .data_o(demux_axi_awready)
        );

            // Default description
        iob_mux #(
        .DATA_W(32),
        .N(2)
    ) iob_mux_axi_wdata (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_wdata),
        // data_o port: Output port
        .data_o(m_axi_wdata_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(4),
        .N(2)
    ) iob_mux_axi_wstrb (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_wstrb),
        // data_o port: Output port
        .data_o(m_axi_wstrb_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_wvalid (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_wvalid),
        // data_o port: Output port
        .data_o(mux_axi_wvalid_o)
        );

            // Default description
        iob_demux #(
        .DATA_W(1),
        .N(2)
    ) iob_demux_axi_wready (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(demux_axi_wready_i),
        // data_o port: Output port
        .data_o(demux_axi_wready)
        );

            // Default description
        iob_demux #(
        .DATA_W(2),
        .N(2)
    ) iob_demux_axi_bresp (
            // sel_i port: Selector interface
        .sel_i(write_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_bresp_i),
        // data_o port: Output port
        .data_o(demux_axi_bresp)
        );

            // Default description
        iob_demux #(
        .DATA_W(1),
        .N(2)
    ) iob_demux_axi_bvalid (
            // sel_i port: Selector interface
        .sel_i(write_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_bvalid_i),
        // data_o port: Output port
        .data_o(demux_axi_bvalid)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_bready (
            // sel_i port: Selector interface
        .sel_i(write_sel_reg),
        // data_i port: Input port
        .data_i(mux_axi_bready),
        // data_o port: Output port
        .data_o(m_axi_bready_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(ID_W),
        .N(2)
    ) iob_mux_axi_awid (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awid),
        // data_o port: Output port
        .data_o(m_axi_awid_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(LEN_W),
        .N(2)
    ) iob_mux_axi_awlen (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awlen),
        // data_o port: Output port
        .data_o(m_axi_awlen_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(3),
        .N(2)
    ) iob_mux_axi_awsize (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awsize),
        // data_o port: Output port
        .data_o(m_axi_awsize_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(2),
        .N(2)
    ) iob_mux_axi_awburst (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awburst),
        // data_o port: Output port
        .data_o(m_axi_awburst_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_awlock (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awlock),
        // data_o port: Output port
        .data_o(m_axi_awlock_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(4),
        .N(2)
    ) iob_mux_axi_awcache (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awcache),
        // data_o port: Output port
        .data_o(m_axi_awcache_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(4),
        .N(2)
    ) iob_mux_axi_awqos (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_awqos),
        // data_o port: Output port
        .data_o(m_axi_awqos_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_wlast (
            // sel_i port: Selector interface
        .sel_i(write_sel),
        // data_i port: Input port
        .data_i(mux_axi_wlast),
        // data_o port: Output port
        .data_o(m_axi_wlast_o)
        );

            // Default description
        iob_demux #(
        .DATA_W(ID_W),
        .N(2)
    ) iob_demux_axi_bid (
            // sel_i port: Selector interface
        .sel_i(write_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_bid_i),
        // data_o port: Output port
        .data_o(demux_axi_bid)
        );

            // Default description
        iob_mux #(
        .DATA_W(31),
        .N(2)
    ) iob_mux_axi_araddr (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_araddr),
        // data_o port: Output port
        .data_o(m_axi_araddr_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_arvalid (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arvalid),
        // data_o port: Output port
        .data_o(mux_axi_arvalid_o)
        );

            // Default description
        iob_demux #(
        .DATA_W(1),
        .N(2)
    ) iob_demux_axi_arready (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(demux_axi_arready_i),
        // data_o port: Output port
        .data_o(demux_axi_arready)
        );

            // Default description
        iob_demux #(
        .DATA_W(32),
        .N(2)
    ) iob_demux_axi_rdata (
            // sel_i port: Selector interface
        .sel_i(read_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_rdata_i),
        // data_o port: Output port
        .data_o(demux_axi_rdata)
        );

            // Default description
        iob_demux #(
        .DATA_W(2),
        .N(2)
    ) iob_demux_axi_rresp (
            // sel_i port: Selector interface
        .sel_i(read_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_rresp_i),
        // data_o port: Output port
        .data_o(demux_axi_rresp)
        );

            // Default description
        iob_demux #(
        .DATA_W(1),
        .N(2)
    ) iob_demux_axi_rvalid (
            // sel_i port: Selector interface
        .sel_i(read_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_rvalid_i),
        // data_o port: Output port
        .data_o(demux_axi_rvalid)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_rready (
            // sel_i port: Selector interface
        .sel_i(read_sel_reg),
        // data_i port: Input port
        .data_i(mux_axi_rready),
        // data_o port: Output port
        .data_o(m_axi_rready_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(ID_W),
        .N(2)
    ) iob_mux_axi_arid (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arid),
        // data_o port: Output port
        .data_o(m_axi_arid_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(LEN_W),
        .N(2)
    ) iob_mux_axi_arlen (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arlen),
        // data_o port: Output port
        .data_o(m_axi_arlen_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(3),
        .N(2)
    ) iob_mux_axi_arsize (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arsize),
        // data_o port: Output port
        .data_o(m_axi_arsize_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(2),
        .N(2)
    ) iob_mux_axi_arburst (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arburst),
        // data_o port: Output port
        .data_o(m_axi_arburst_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(2)
    ) iob_mux_axi_arlock (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arlock),
        // data_o port: Output port
        .data_o(m_axi_arlock_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(4),
        .N(2)
    ) iob_mux_axi_arcache (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arcache),
        // data_o port: Output port
        .data_o(m_axi_arcache_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(4),
        .N(2)
    ) iob_mux_axi_arqos (
            // sel_i port: Selector interface
        .sel_i(read_sel),
        // data_i port: Input port
        .data_i(mux_axi_arqos),
        // data_o port: Output port
        .data_o(m_axi_arqos_o)
        );

            // Default description
        iob_demux #(
        .DATA_W(ID_W),
        .N(2)
    ) iob_demux_axi_rid (
            // sel_i port: Selector interface
        .sel_i(read_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_rid_i),
        // data_o port: Output port
        .data_o(demux_axi_rid)
        );

            // Default description
        iob_demux #(
        .DATA_W(1),
        .N(2)
    ) iob_demux_axi_rlast (
            // sel_i port: Selector interface
        .sel_i(read_sel_reg),
        // data_i port: Input port
        .data_i(m_axi_rlast_i),
        // data_o port: Output port
        .data_o(demux_axi_rlast)
        );

    
endmodule
