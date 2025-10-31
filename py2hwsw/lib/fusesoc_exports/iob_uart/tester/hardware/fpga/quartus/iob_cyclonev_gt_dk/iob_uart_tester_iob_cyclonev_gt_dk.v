// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_iob_cyclonev_gt_dk_conf.vh"

module iob_uart_tester_iob_cyclonev_gt_dk #(
    parameter AXI_ID_W = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_AXI_ID_W,  // Don't change this parameter value!
    parameter AXI_LEN_W = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_AXI_LEN_W,  // Don't change this parameter value!
    parameter AXI_ADDR_W = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_AXI_ADDR_W,  // Don't change this parameter value!
    parameter AXI_DATA_W = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_AXI_DATA_W,  // Don't change this parameter value!
    parameter BAUD = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_BAUD,  // Don't change this parameter value!
    parameter FREQ = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_FREQ,  // Don't change this parameter value!
    parameter MEM_NO_READ_ON_WRITE = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_MEM_NO_READ_ON_WRITE,  // Don't change this parameter value!
    parameter INTEL = `IOB_UART_TESTER_IOB_CYCLONEV_GT_DK_INTEL  // Don't change this parameter value!
) (
    // clk_rst_i: Clock and reset
    input clk_i,
    input resetn_i,
    // rs232_io: Serial port
    output txd_o,
    input rxd_i
);

// Clock, clock enable and reset
    wire cke;
    wire arst;
// iob-system uart interface
    wire rs232_rts;
    wire high;
// Reset synchronizer inputs
    wire resetn_inv;


    // General connections
    assign high = 1'b1;
    assign cke = 1'b1;


    assign resetn_inv = ~resetn_i;


        // IOb-SoC memory wrapper
        iob_uart_tester_mwrap #(
        .AXI_ID_W(AXI_ID_W),
        .AXI_LEN_W(AXI_LEN_W),
        .AXI_ADDR_W(AXI_ADDR_W),
        .AXI_DATA_W(AXI_DATA_W),
        .MEM_NO_READ_ON_WRITE(MEM_NO_READ_ON_WRITE)
    ) iob_memwrapper (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke),
        .arst_i(arst),
        // rs232_m port: iob-system uart interface
        .rs232_rxd_i(rxd_i),
        .rs232_txd_o(txd_o),
        .rs232_rts_o(rs232_rts),
        .rs232_cts_i(high)
        );

            // Reset synchronizer
        iob_reset_sync rst_sync (
            // clk_rst_s port: clock and reset
        .clk_i(clk_i),
        .arst_i(resetn_inv),
        // arst_o port: Output port
        .arst_o(arst)
        );

    
endmodule
