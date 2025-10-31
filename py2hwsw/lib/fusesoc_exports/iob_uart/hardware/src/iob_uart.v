// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_conf.vh"

module iob_uart #(
   parameter DATA_W = `IOB_UART_DATA_W
) (
   // clk_en_rst_s: Clock, clock enable and reset
   input                 clk_i,
   input                 cke_i,
   input                 arst_i,
   // rs232_m: RS232 interface
   input                 rs232_rxd_i,
   output                rs232_txd_o,
   output                rs232_rts_o,
   input                 rs232_cts_i,
   // iob_csrs_cbus_s: Control and Status Registers interface (auto-generated)
   input                 iob_csrs_iob_valid_i,
   input  [       3-1:0] iob_csrs_iob_addr_i,
   input  [  DATA_W-1:0] iob_csrs_iob_wdata_i,
   input  [DATA_W/8-1:0] iob_csrs_iob_wstrb_i,
   output                iob_csrs_iob_rvalid_o,
   output [  DATA_W-1:0] iob_csrs_iob_rdata_o,
   output                iob_csrs_iob_ready_o
);

   wire          softreset_wr;
   wire [16-1:0] div_wr;
   wire          txdata_valid_wr;
   wire [ 8-1:0] txdata_wdata_wr;
   wire          txdata_wstrb_wr;
   wire          txdata_ready_wr;
   wire          txen_wr;
   wire          rxen_wr;
   wire          txready_rd;
   wire          rxready_rd;
   wire          rxdata_valid_rd;
   wire [ 8-1:0] rxdata_rdata_rd;
   wire          rxdata_ready_rd;
   wire          rxdata_rvalid_rd;
   wire          txdata_wen_wr;


   // txdata Manual logic
   assign txdata_ready_wr = (~softreset_wr);  // always ready, except on reset
   assign txdata_wen_wr   = txdata_valid_wr & txdata_wstrb_wr;

   // rxdata Manual logic
   assign rxdata_ready_rd = (~softreset_wr);  // always ready, except on reset



   // Control/Status Registers
   iob_uart_csrs iob_csrs (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i            (clk_i),
      .cke_i            (cke_i),
      .arst_i           (arst_i),
      // softreset_o port: softreset register interface
      .softreset_rdata_o(softreset_wr),
      // div_o port: div register interface
      .div_rdata_o      (div_wr),
      // txdata_io port: txdata register interface
      .txdata_valid_o   (txdata_valid_wr),
      .txdata_wdata_o   (txdata_wdata_wr),
      .txdata_wstrb_o   (txdata_wstrb_wr),
      .txdata_ready_i   (txdata_ready_wr),
      // txen_o port: txen register interface
      .txen_rdata_o     (txen_wr),
      // txready_i port: txready register interface
      .txready_wdata_i  (txready_rd),
      // rxen_o port: rxen register interface
      .rxen_rdata_o     (rxen_wr),
      // rxready_i port: rxready register interface
      .rxready_wdata_i  (rxready_rd),
      // rxdata_io port: rxdata register interface
      .rxdata_valid_o   (rxdata_valid_rd),
      .rxdata_rdata_i   (rxdata_rdata_rd),
      .rxdata_ready_i   (rxdata_ready_rd),
      .rxdata_rvalid_i  (rxdata_rvalid_rd),
      // control_if_s port: CSR control interface. Interface type defined by `csr_if` parameter.
      .iob_valid_i      (iob_csrs_iob_valid_i),
      .iob_addr_i       (iob_csrs_iob_addr_i),
      .iob_wdata_i      (iob_csrs_iob_wdata_i),
      .iob_wstrb_i      (iob_csrs_iob_wstrb_i),
      .iob_rvalid_o     (iob_csrs_iob_rvalid_o),
      .iob_rdata_o      (iob_csrs_iob_rdata_o),
      .iob_ready_o      (iob_csrs_iob_ready_o)
   );

   // Register for rxdata rvalid
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) iob_reg_rvalid (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(rxdata_valid_rd),
      // data_o port: Data output
      .data_o(rxdata_rvalid_rd)
   );

   // UART core driver
   iob_uart_core iob_uart_core_inst (
      // clk_en_rst_s port: Clock and reset
      .clk_i          (clk_i),
      .cke_i          (cke_i),
      .arst_i         (arst_i),
      .rst_soft_i     (softreset_wr),
      .tx_en_i        (txen_wr),
      .rx_en_i        (rxen_wr),
      .tx_ready_o     (txready_rd),
      .rx_ready_o     (rxready_rd),
      .tx_data_i      (txdata_wdata_wr),
      .rx_data_o      (rxdata_rdata_rd),
      .data_write_en_i(txdata_wen_wr),
      .data_read_en_i (rxdata_valid_rd),
      .bit_duration_i (div_wr),
      // rs232_m port: RS232 interface
      .rs232_rxd_i    (rs232_rxd_i),
      .rs232_txd_o    (rs232_txd_o),
      .rs232_rts_o    (rs232_rts_o),
      .rs232_cts_i    (rs232_cts_i)
   );


endmodule
