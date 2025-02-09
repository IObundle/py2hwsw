`timescale 1ns / 1ps
`include "iob_uart_conf.vh"

module iob_uart_sim #(
   parameter DATA_W = `IOB_UART_DATA_W
) (
   // clk_en_rst_s
   input                 clk_i,
   input                 cke_i,
   input                 arst_i,

   // iob_uart_csrs_cbus_s
   input                 iob_uart_csrs_iob_valid_i,
   input                 iob_uart_csrs_iob_addr_i,
   input  [  DATA_W-1:0] iob_uart_csrs_iob_wdata_i,
   input  [DATA_W/8-1:0] iob_uart_csrs_iob_wstrb_i,
   output                iob_uart_csrs_iob_rvalid_o,
   output [  DATA_W-1:0] iob_uart_csrs_iob_rdata_o,
   output                iob_uart_csrs_iob_ready_o
   // clk_rst_s
);

   wire                  tx2rx;
   wire                  rts2cts;
   
   // Instantiate the UART module with the rs232 loopback
   iob_uart uart_inst 
     (
      .clk_i          (clk_i),
      .arst_i         (arst_i),
      .cke_i          (cke_i),

      .rs232_rxd_i    (tx2rx),
      .rs232_txd_o    (tx2rx),
      .rs232_rts_o    (rts2cts),
      .rs232_cts_i    (rts2cts),

      .iob_uart_csrs_iob_valid_i (iob_uart_csrs_iob_valid_i),
      .iob_uart_csrs_iob_addr_i  (iob_uart_csrs_iob_addr_i),
      .iob_uart_csrs_iob_wdata_i (iob_uart_csrs_iob_wdata_i),
      .iob_uart_csrs_iob_wstrb_i (iob_uart_csrs_iob_wstrb_i),
      .iob_uart_csrs_iob_rvalid_o(iob_uart_csrs_iob_rvalid_o),
      .iob_uart_csrs_iob_rdata_o  (iob_uart_csrs_iob_rdata_o),
      .iob_uart_csrs_iob_ready_o  (iob_uart_csrs_iob_ready_o)
   );

   
endmodule
