// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uut_conf.vh"

module iob_uut #(
    parameter DATA_W = `IOB_UUT_DATA_W
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // uart_s: Testbench uart csrs interface
    input iob_valid_i,
    input [3-1:0] iob_addr_i,
    input [32-1:0] iob_wdata_i,
    input [32/8-1:0] iob_wstrb_i,
    output iob_rvalid_o,
    output [32-1:0] iob_rdata_o,
    output iob_ready_o
);

// Uart loopback wires
    wire rs232_rxd;
    wire rs232_txd;
    wire rs232_rts;
    wire rs232_cts;
// Testbench uart csrs bus
    wire internal_iob_valid;
    wire [3-1:0] internal_iob_addr;
    wire [32-1:0] internal_iob_wdata;
    wire [32/8-1:0] internal_iob_wstrb;
    wire internal_iob_rvalid;
    wire [32-1:0] internal_iob_rdata;
    wire internal_iob_ready;


   assign rs232_rxd = rs232_txd;
   assign rs232_cts = rs232_rts;


        // Unit Under Test (UUT) UART instance with 'iob' interface.
        iob_uart uart_inst (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // iob_csrs_cbus_s port: Control and Status Registers interface (auto-generated)
        .iob_csrs_iob_valid_i(internal_iob_valid),
        .iob_csrs_iob_addr_i(internal_iob_addr),
        .iob_csrs_iob_wdata_i(internal_iob_wdata),
        .iob_csrs_iob_wstrb_i(internal_iob_wstrb),
        .iob_csrs_iob_rvalid_o(internal_iob_rvalid),
        .iob_csrs_iob_rdata_o(internal_iob_rdata),
        .iob_csrs_iob_ready_o(internal_iob_ready),
        // rs232_m port: RS232 interface
        .rs232_rxd_i(rs232_rxd),
        .rs232_txd_o(rs232_txd),
        .rs232_rts_o(rs232_rts),
        .rs232_cts_i(rs232_cts)
        );

            // Convert IOb port from testbench into correct interface for UART CSRs bus
        iob_universal_converter_iob_iob #(
        .ADDR_W(3),
        .DATA_W(DATA_W)
    ) iob_universal_converter (
            // s_s port: Subordinate port
        .iob_valid_i(iob_valid_i),
        .iob_addr_i(iob_addr_i),
        .iob_wdata_i(iob_wdata_i),
        .iob_wstrb_i(iob_wstrb_i),
        .iob_rvalid_o(iob_rvalid_o),
        .iob_rdata_o(iob_rdata_o),
        .iob_ready_o(iob_ready_o),
        // m_m port: Manager port
        .iob_valid_o(internal_iob_valid),
        .iob_addr_o(internal_iob_addr),
        .iob_wdata_o(internal_iob_wdata),
        .iob_wstrb_o(internal_iob_wstrb),
        .iob_rvalid_i(internal_iob_rvalid),
        .iob_rdata_i(internal_iob_rdata),
        .iob_ready_i(internal_iob_ready)
        );

    
endmodule
