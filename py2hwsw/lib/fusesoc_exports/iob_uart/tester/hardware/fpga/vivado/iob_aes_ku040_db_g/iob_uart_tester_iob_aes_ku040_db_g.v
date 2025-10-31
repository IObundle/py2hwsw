// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_iob_aes_ku040_db_g_conf.vh"

module iob_uart_tester_iob_aes_ku040_db_g #(
    parameter AXI_ID_W = `IOB_UART_TESTER_IOB_AES_KU040_DB_G_AXI_ID_W,  // Don't change this parameter value!
    parameter AXI_LEN_W = `IOB_UART_TESTER_IOB_AES_KU040_DB_G_AXI_LEN_W,  // Don't change this parameter value!
    parameter AXI_ADDR_W = `IOB_UART_TESTER_IOB_AES_KU040_DB_G_AXI_ADDR_W,  // Don't change this parameter value!
    parameter AXI_DATA_W = `IOB_UART_TESTER_IOB_AES_KU040_DB_G_AXI_DATA_W,  // Don't change this parameter value!
    parameter BAUD = `IOB_UART_TESTER_IOB_AES_KU040_DB_G_BAUD,  // Don't change this parameter value!
    parameter FREQ = `IOB_UART_TESTER_IOB_AES_KU040_DB_G_FREQ,  // Don't change this parameter value!
    parameter XILINX = `IOB_UART_TESTER_IOB_AES_KU040_DB_G_XILINX  // Don't change this parameter value!
) (
    // clk_rst_i: Clock and reset
    input c0_sys_clk_clk_p_i,
    input c0_sys_clk_clk_n_i,
    input areset_i,
    // rs232_io: Serial port
    output txd_o,
    input rxd_i
);

// Clock, clock enable and reset
    wire clk;
    wire cke;
    wire arst;
// iob-system uart interface
    wire rs232_rts;
    wire high;


    // General connections
    assign high = 1'b1;
    assign cke = 1'b1;


        // IOb-SoC instance
        iob_uart_tester_mwrap #(
        .AXI_ID_W(AXI_ID_W),
        .AXI_LEN_W(AXI_LEN_W),
        .AXI_ADDR_W(AXI_ADDR_W),
        .AXI_DATA_W(AXI_DATA_W)
    ) iob_memwrapper (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk),
        .cke_i(cke),
        .arst_i(arst),
        // rs232_m port: iob-system uart interface
        .rs232_rxd_i(rxd_i),
        .rs232_txd_o(txd_o),
        .rs232_rts_o(rs232_rts),
        .rs232_cts_i(high)
        );

            // PLL to generate system clock
        iob_xilinx_clock_wizard #(
        .OUTPUT_PER(10),
        .INPUT_PER(4)
    ) clk_250_to_100_MHz (
            // clk_rst_i port: clock and reset inputs
        .clk_p_i(c0_sys_clk_clk_p_i),
        .clk_n_i(c0_sys_clk_clk_n_i),
        .arst_i(areset_i),
        // clk_rst_o port: clock and reset outputs
        .clk_out1_o(clk),
        .rst_out1_o(arst)
        );

    
endmodule
