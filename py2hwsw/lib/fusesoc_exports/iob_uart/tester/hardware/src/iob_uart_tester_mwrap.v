// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_mwrap_conf.vh"

module iob_uart_tester_mwrap #(
    parameter AXI_ID_W = `IOB_UART_TESTER_MWRAP_AXI_ID_W,  // Don't change this parameter value!
    parameter AXI_ADDR_W = `IOB_UART_TESTER_MWRAP_AXI_ADDR_W,  // Don't change this parameter value!
    parameter AXI_DATA_W = `IOB_UART_TESTER_MWRAP_AXI_DATA_W,  // Don't change this parameter value!
    parameter AXI_LEN_W = `IOB_UART_TESTER_MWRAP_AXI_LEN_W,  // Don't change this parameter value!
    parameter BOOTROM_MEM_HEXFILE = `IOB_UART_TESTER_MWRAP_BOOTROM_MEM_HEXFILE,  // Don't change this parameter value!
    parameter INT_MEM_HEXFILE = `IOB_UART_TESTER_MWRAP_INT_MEM_HEXFILE,  // Don't change this parameter value!
    parameter MEM_NO_READ_ON_WRITE = `IOB_UART_TESTER_MWRAP_MEM_NO_READ_ON_WRITE
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // rs232_m: iob-system uart interface
    input rs232_rxd_i,
    output rs232_txd_o,
    output rs232_rts_o,
    input rs232_cts_i
);

// Ports for connection with boot ROM memory
    wire bootrom_mem_clk;
    wire [10-1:0] bootrom_mem_addr;
    wire bootrom_mem_en;
    wire [32-1:0] bootrom_mem_r_data;
// Port for connection to 'iob_ram_t2p_be' memory
    wire int_mem_clk;
    wire int_mem_r_en;
    wire [16-1:0] int_mem_r_addr;
    wire [32-1:0] int_mem_r_data;
    wire [32/8-1:0] int_mem_w_strb;
    wire [16-1:0] int_mem_w_addr;
    wire [32-1:0] int_mem_w_data;

        // Wrapped module
        iob_uart_tester #(
        .AXI_ID_W(AXI_ID_W),
        .AXI_ADDR_W(AXI_ADDR_W),
        .AXI_DATA_W(AXI_DATA_W),
        .AXI_LEN_W(AXI_LEN_W),
        .BOOTROM_MEM_HEXFILE(BOOTROM_MEM_HEXFILE),
        .INT_MEM_HEXFILE(INT_MEM_HEXFILE)
    ) iob_uart_tester_inst (
            // rom_bus_m port: Ports for connection with boot ROM memory
        .bootrom_mem_clk_o(bootrom_mem_clk),
        .bootrom_mem_addr_o(bootrom_mem_addr),
        .bootrom_mem_en_o(bootrom_mem_en),
        .bootrom_mem_r_data_i(bootrom_mem_r_data),
        // int_mem_bus_m port: Port for connection to 'iob_ram_t2p_be' memory
        .int_mem_clk_o(int_mem_clk),
        .int_mem_r_en_o(int_mem_r_en),
        .int_mem_r_addr_o(int_mem_r_addr),
        .int_mem_r_data_i(int_mem_r_data),
        .int_mem_w_strb_o(int_mem_w_strb),
        .int_mem_w_addr_o(int_mem_w_addr),
        .int_mem_w_data_o(int_mem_w_data),
        // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // rs232_m port: iob-system uart interface
        .rs232_rxd_i(rs232_rxd_i),
        .rs232_txd_o(rs232_txd_o),
        .rs232_rts_o(rs232_rts_o),
        .rs232_cts_i(rs232_cts_i)
        );

            // Default description
        iob_rom_sp #(
        .DATA_W(32),
        .ADDR_W(10),
        .HEXFILE(BOOTROM_MEM_HEXFILE)
    ) bootrom_mem_mem (
            // rom_sp_s port: ROM interface
        .clk_i(bootrom_mem_clk),
        .addr_i(bootrom_mem_addr),
        .en_i(bootrom_mem_en),
        .r_data_o(bootrom_mem_r_data)
        );

            // Default description
        iob_ram_t2p_be #(
        .DATA_W(32),
        .ADDR_W(16),
        .HEXFILE(INT_MEM_HEXFILE)
    ) int_mem_mem (
            // ram_t2p_be_s port: RAM interface
        .clk_i(int_mem_clk),
        .r_en_i(int_mem_r_en),
        .r_addr_i(int_mem_r_addr),
        .r_data_o(int_mem_r_data),
        .w_strb_i(int_mem_w_strb),
        .w_addr_i(int_mem_w_addr),
        .w_data_i(int_mem_w_data)
        );

    
endmodule
