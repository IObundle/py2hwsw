// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_pbus_split_conf.vh"

module iob_uart_tester_pbus_split (
    // clk_en_rst_s: Clock, clock enable and async reset
    input clk_i,
    input cke_i,
    input arst_i,
    // reset_i: Reset signal
    input rst_i,
    // s_s: Split subordinate interface
    input s_iob_valid_i,
    input [30-1:0] s_iob_addr_i,
    input [32-1:0] s_iob_wdata_i,
    input [32/8-1:0] s_iob_wstrb_i,
    output s_iob_rvalid_o,
    output [32-1:0] s_iob_rdata_o,
    output reg s_iob_ready_o,
    // m_0_m: Split manager interface
    output m0_iob_valid_o,
    output [28-1:0] m0_iob_addr_o,
    output [32-1:0] m0_iob_wdata_o,
    output [32/8-1:0] m0_iob_wstrb_o,
    input m0_iob_rvalid_i,
    input [32-1:0] m0_iob_rdata_i,
    input m0_iob_ready_i,
    // m_1_m: Split manager interface
    output m1_iob_valid_o,
    output [28-1:0] m1_iob_addr_o,
    output [32-1:0] m1_iob_wdata_o,
    output [32/8-1:0] m1_iob_wstrb_o,
    input m1_iob_rvalid_i,
    input [32-1:0] m1_iob_rdata_i,
    input m1_iob_ready_i,
    // m_2_m: Split manager interface
    output m2_iob_valid_o,
    output [28-1:0] m2_iob_addr_o,
    output [32-1:0] m2_iob_wdata_o,
    output [32/8-1:0] m2_iob_wstrb_o,
    input m2_iob_rvalid_i,
    input [32-1:0] m2_iob_rdata_i,
    input m2_iob_ready_i,
    // m_3_m: Split manager interface
    output m3_iob_valid_o,
    output [28-1:0] m3_iob_addr_o,
    output [32-1:0] m3_iob_wdata_o,
    output [32/8-1:0] m3_iob_wstrb_o,
    input m3_iob_rvalid_i,
    input [32-1:0] m3_iob_rdata_i,
    input m3_iob_ready_i
);

// Input of sel_reg
    reg [2-1:0] sel;
// Output of sel_reg
    wire [2-1:0] sel_reg;
// Input of valid demux
    reg s_iob_valid_int;
// Output of valid demux
    wire [4-1:0] demux_valid_output;
// Output of address demux
    wire [120-1:0] demux_addr_output;
// Output of wdata demux
    wire [128-1:0] demux_wdata_output;
// Output of wstrb demux
    wire [16-1:0] demux_wstrb_output;
// Input of rdata mux
    wire [128-1:0] mux_rdata_input;
// Input of rvalid mux
    wire [4-1:0] mux_rvalid_input;
// Input of ready mux
    wire [4-1:0] mux_ready_input;
// Output of ready mux
    wire s_iob_ready_int;
// FSM state
    wire [2-1:0] state;
    reg [2-1:0] state_nxt;


localparam WAIT_VALID = 2'd0;
localparam WAIT_READY = 2'd1;
localparam WAIT_RVALID = 2'd2;

always @* begin
    state_nxt = state;
   // Default assignments
   sel = sel_reg;

   // Disallow handshake signals from going through
   s_iob_valid_int = 1'b0;
   s_iob_ready_o = 1'b0;


    case (state)
        WAIT_VALID: begin
    // Wait for valid data
      // Allow handshake signals to go through
      s_iob_valid_int = s_iob_valid_i;
      s_iob_ready_o = s_iob_ready_int;
      // Allow selector to be changed
      sel = s_iob_addr_i[29-:2];
      if (s_iob_valid_i && ~s_iob_ready_o) begin
          // If not ready, wait for ready
         state_nxt = WAIT_READY;
      end else if (s_iob_valid_i && !s_iob_wstrb_i && ~s_iob_rvalid_o) begin
          // If read (and ready) and not rvalid, wait for rvalid
         state_nxt = WAIT_RVALID;
      end
end
WAIT_READY: begin
    // Wait for ready signal
      // Allow handshake signals to go through
      s_iob_valid_int = s_iob_valid_i;
      s_iob_ready_o = s_iob_ready_int;
      if (s_iob_ready_o && |s_iob_wstrb_i) begin
         // If write and ready, transaction complete
         state_nxt = WAIT_VALID;
      end else if (s_iob_ready_o && !s_iob_wstrb_i && s_iob_rvalid_o) begin
         // If read and ready and rvalid, transaction complete
         state_nxt = WAIT_VALID;
      end else if (s_iob_ready_o && !s_iob_wstrb_i) begin
         // If read and ready but not rvalid, wait for rvalid
         state_nxt = WAIT_RVALID;
      end
end
default: begin
    // Wait for read data
      if (s_iob_rvalid_o) begin
         state_nxt = WAIT_VALID;
      end
end
    endcase
end


    assign m0_iob_valid_o = demux_valid_output[0+:1];
    assign m0_iob_addr_o = demux_addr_output[0+:28];
    assign m0_iob_wdata_o = demux_wdata_output[0+:32];
    assign m0_iob_wstrb_o = demux_wstrb_output[0+:4];

    assign m1_iob_valid_o = demux_valid_output[1+:1];
    assign m1_iob_addr_o = demux_addr_output[30+:28];
    assign m1_iob_wdata_o = demux_wdata_output[32+:32];
    assign m1_iob_wstrb_o = demux_wstrb_output[4+:4];

    assign m2_iob_valid_o = demux_valid_output[2+:1];
    assign m2_iob_addr_o = demux_addr_output[60+:28];
    assign m2_iob_wdata_o = demux_wdata_output[64+:32];
    assign m2_iob_wstrb_o = demux_wstrb_output[8+:4];

    assign m3_iob_valid_o = demux_valid_output[3+:1];
    assign m3_iob_addr_o = demux_addr_output[90+:28];
    assign m3_iob_wdata_o = demux_wdata_output[96+:32];
    assign m3_iob_wstrb_o = demux_wstrb_output[12+:4];

    assign mux_rdata_input = {m3_iob_rdata_i, m2_iob_rdata_i, m1_iob_rdata_i, m0_iob_rdata_i};
    assign mux_rvalid_input = {m3_iob_rvalid_i, m2_iob_rvalid_i, m1_iob_rvalid_i, m0_iob_rvalid_i};
    assign mux_ready_input = {m3_iob_ready_i, m2_iob_ready_i, m1_iob_ready_i, m0_iob_ready_i};


        // Default description
        iob_reg_car #(
        .DATA_W(2),
        .RST_VAL(2'b0)
    ) sel_reg_r (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .rst_i(rst_i),
        // data_i port: Data input
        .data_i(sel),
        // data_o port: Data output
        .data_o(sel_reg)
        );

            // Default description
        iob_demux #(
        .DATA_W(1),
        .N(4)
    ) iob_demux_valid (
            // sel_i port: Selector interface
        .sel_i(sel),
        // data_i port: Input port
        .data_i(s_iob_valid_int),
        // data_o port: Output port
        .data_o(demux_valid_output)
        );

            // Default description
        iob_demux #(
        .DATA_W(30),
        .N(4)
    ) iob_demux_addr (
            // sel_i port: Selector interface
        .sel_i(sel),
        // data_i port: Input port
        .data_i(s_iob_addr_i),
        // data_o port: Output port
        .data_o(demux_addr_output)
        );

            // Default description
        iob_demux #(
        .DATA_W(32),
        .N(4)
    ) iob_demux_wdata (
            // sel_i port: Selector interface
        .sel_i(sel),
        // data_i port: Input port
        .data_i(s_iob_wdata_i),
        // data_o port: Output port
        .data_o(demux_wdata_output)
        );

            // Default description
        iob_demux #(
        .DATA_W(4),
        .N(4)
    ) iob_demux_wstrb (
            // sel_i port: Selector interface
        .sel_i(sel),
        // data_i port: Input port
        .data_i(s_iob_wstrb_i),
        // data_o port: Output port
        .data_o(demux_wstrb_output)
        );

            // Default description
        iob_mux #(
        .DATA_W(32),
        .N(4)
    ) iob_mux_rdata (
            // sel_i port: Selector interface
        .sel_i(sel_reg),
        // data_i port: Input port
        .data_i(mux_rdata_input),
        // data_o port: Output port
        .data_o(s_iob_rdata_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(4)
    ) iob_mux_rvalid (
            // sel_i port: Selector interface
        .sel_i(sel_reg),
        // data_i port: Input port
        .data_i(mux_rvalid_input),
        // data_o port: Output port
        .data_o(s_iob_rvalid_o)
        );

            // Default description
        iob_mux #(
        .DATA_W(1),
        .N(4)
    ) iob_mux_ready (
            // sel_i port: Selector interface
        .sel_i(sel),
        // data_i port: Input port
        .data_i(mux_ready_input),
        // data_o port: Output port
        .data_o(s_iob_ready_int)
        );

            // state register
        iob_reg_ca #(
        .DATA_W(2),
        .RST_VAL(0)
    ) state_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // data_i port: Data input
        .data_i(state_nxt),
        // data_o port: Data output
        .data_o(state)
        );

    
endmodule
