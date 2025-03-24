// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_uart_conf.vh"
`include "iob_uart_csrs_def.vh"

module iob_uart_sim #(
   parameter DATA_W = `IOB_UART_DATA_W
) (
   // clk_en_rst_s
   input clk_i,
   input cke_i,
   input arst_i,

   // iob_uart_csrs_cbus_s
   input                              iob_valid_i,
   input  [`IOB_UART_CSRS_ADDR_W-1:0] iob_addr_i,
   input  [               DATA_W-1:0] iob_wdata_i,
   input  [             DATA_W/8-1:0] iob_wstrb_i,
   output                             iob_rvalid_o,
   output [               DATA_W-1:0] iob_rdata_o,
   output                             iob_ready_o,
   input                              iob_rready_i
   // clk_rst_s
);

   wire tx2rx;
   wire rts2cts;

   `ifdef IOB_UART_CSR_IF_IOB
   // Instantiate the UART module with the rs232 loopback
   iob_uart uart_inst (
      .clk_i (clk_i),
      .arst_i(arst_i),
      .cke_i (cke_i),

      .rs232_rxd_i(tx2rx),
      .rs232_txd_o(tx2rx),
      .rs232_rts_o(rts2cts),
      .rs232_cts_i(rts2cts),

      .iob_csrs_iob_valid_i (iob_valid_i),
      .iob_csrs_iob_addr_i  (iob_addr_i[2]),
      .iob_csrs_iob_wdata_i (iob_wdata_i),
      .iob_csrs_iob_wstrb_i (iob_wstrb_i),
      .iob_csrs_iob_rvalid_o(iob_rvalid_o),
      .iob_csrs_iob_rdata_o (iob_rdata_o),
      .iob_csrs_iob_ready_o (iob_ready_o),
      .iob_csrs_iob_rready_i(iob_rready_i)
   );

   `elsif IOB_UART_CSR_IF_AXIL

   // iob_csrs_cbus_s
   wire [`IOB_UART_CSRS_ADDR_W-1:0] iob_csrs_axil_araddr;
   wire                             iob_csrs_axil_arvalid;
   wire                             iob_csrs_axil_arready;
   wire [               DATA_W-1:0] iob_csrs_axil_rdata;
   wire [                    2-1:0] iob_csrs_axil_rresp;
   wire                             iob_csrs_axil_rvalid;
   wire                             iob_csrs_axil_rready;
   wire [`IOB_UART_CSRS_ADDR_W-1:0] iob_csrs_axil_awaddr;
   wire                             iob_csrs_axil_awvalid;
   wire                             iob_csrs_axil_awready;
   wire [               DATA_W-1:0] iob_csrs_axil_wdata;
   wire [             DATA_W/8-1:0] iob_csrs_axil_wstrb;
   wire                             iob_csrs_axil_wvalid;
   wire                             iob_csrs_axil_wready;
   wire [                    2-1:0] iob_csrs_axil_bresp;
   wire                             iob_csrs_axil_bvalid;
   wire                             iob_csrs_axil_bready;

   iob_iob2axil #(
       .AXIL_ADDR_W(`IOB_UART_CSRS_ADDR_W),
       .AXIL_DATA_W(DATA_W),
       .ADDR_W(`IOB_UART_CSRS_ADDR_W),
       .DATA_W(DATA_W)
   ) iob2axil_inst (
   // clk_en_rst_s
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        
        .iob_valid_i(iob_valid_i),
        .iob_addr_i(iob_addr_i),
        .iob_wdata_i(iob_wdata_i),
        .iob_wstrb_i(iob_wstrb_i),
        .iob_rvalid_o(iob_rvalid_o),
        .iob_rdata_o(iob_rdata_o),
        .iob_ready_o(iob_ready_o),
        .iob_rready_i(iob_rready_i),
       
        .axil_araddr_o(iob_csrs_axil_araddr),
        .axil_arvalid_o(iob_csrs_axil_arvalid),
        .axil_arready_i(iob_csrs_axil_arready),
        .axil_rdata_i(iob_csrs_axil_rdata),
        .axil_rresp_i(iob_csrs_axil_rresp),
        .axil_rvalid_i(iob_csrs_axil_rvalid),
        .axil_rready_o(iob_csrs_axil_rready),
        .axil_awaddr_o(iob_csrs_axil_awaddr),
        .axil_awvalid_o(iob_csrs_axil_awvalid),
        .axil_awready_i(iob_csrs_axil_awready),
        .axil_wdata_o(iob_csrs_axil_wdata),
        .axil_wstrb_o(iob_csrs_axil_wstrb),
        .axil_wvalid_o(iob_csrs_axil_wvalid),
        .axil_wready_i(iob_csrs_axil_wready),
        .axil_bresp_i(iob_csrs_axil_bresp),
        .axil_bvalid_i(iob_csrs_axil_bvalid),
        .axil_bready_o(iob_csrs_axil_bready)
   );

   // Instantiate the UART module with the rs232 loopback
   iob_uart uart_inst (
      .clk_i (clk_i),
      .arst_i(arst_i),
      .cke_i (cke_i),

      .rs232_rxd_i(tx2rx),
      .rs232_txd_o(tx2rx),
      .rs232_rts_o(rts2cts),
      .rs232_cts_i(rts2cts),

      .iob_csrs_axil_araddr_i(iob_csrs_axil_araddr[2]),
      .iob_csrs_axil_arvalid_i(iob_csrs_axil_arvalid),
      .iob_csrs_axil_arready_o(iob_csrs_axil_arready),
      .iob_csrs_axil_rdata_o(iob_csrs_axil_rdata),
      .iob_csrs_axil_rresp_o(iob_csrs_axil_rresp),
      .iob_csrs_axil_rvalid_o(iob_csrs_axil_rvalid),
      .iob_csrs_axil_rready_i(iob_csrs_axil_rready),
      .iob_csrs_axil_awaddr_i(iob_csrs_axil_awaddr[2]),
      .iob_csrs_axil_awvalid_i(iob_csrs_axil_awvalid),
      .iob_csrs_axil_awready_o(iob_csrs_axil_awready),
      .iob_csrs_axil_wdata_i(iob_csrs_axil_wdata),
      .iob_csrs_axil_wstrb_i(iob_csrs_axil_wstrb),
      .iob_csrs_axil_wvalid_i(iob_csrs_axil_wvalid),
      .iob_csrs_axil_wready_o(iob_csrs_axil_wready),
      .iob_csrs_axil_bresp_o(iob_csrs_axil_bresp),
      .iob_csrs_axil_bvalid_o(iob_csrs_axil_bvalid),
      .iob_csrs_axil_bready_i(iob_csrs_axil_bready)
   );

   `elsif IOB_UART_CSR_IF_APB

   // TODO: instantiate iob2apb bridge

   // Instantiate the UART module with the rs232 loopback
   iob_uart uart_inst (
      .clk_i (clk_i),
      .arst_i(arst_i),
      .cke_i (cke_i),

      .rs232_rxd_i(tx2rx),
      .rs232_txd_o(tx2rx),
      .rs232_rts_o(rts2cts),
      .rs232_cts_i(rts2cts),

      .iob_csrs_iob_valid_i (iob_valid_i),
      .iob_csrs_iob_addr_i  (iob_addr_i[2]),
      .iob_csrs_iob_wdata_i (iob_wdata_i),
      .iob_csrs_iob_wstrb_i (iob_wstrb_i),
      .iob_csrs_iob_rvalid_o(iob_rvalid_o),
      .iob_csrs_iob_rdata_o (iob_rdata_o),
      .iob_csrs_iob_ready_o (iob_ready_o),
      .iob_csrs_iob_rready_i(iob_rready_i)
   );

   `endif


endmodule
