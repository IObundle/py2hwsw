`timescale 1ns / 1ps

`include "uart_defines.vh"

module iob_uart16550_sim_wrapper #(
   parameter MEM_ADDR_W = 32,
   parameter ADDR_W     = `UART_ADDR_WIDTH,
   parameter DATA_W     = 32
) (
   input  wire              clk,       // WISHBONE clock
   // WISHBONE slave
   input  wire              wb_rst_i,  // WISHBONE reset
   input  wire [ADDR_W-1:0] wb_adr_i,  // WISHBONE address input
   input  wire [      31:0] wb_dat_i,  // WISHBONE data input
   output wire [      31:0] wb_dat_o,  // WISHBONE data output
   input  wire              wb_we_i,   // WISHBONE write enable input
   input  wire              wb_stb_i,  // WISHBONE strobe input
   input  wire              wb_cyc_i,  // WISHBONE cycle input
   output wire              wb_ack_o,  // WISHBONE acknowledge output
   input  wire [       3:0] wb_sel_i,  // WISHBONE byte select input

   // Interrupt
   output wire int_o,      // Interrupt output
   // Tx
   output wire pad_stx_o,  // Transmit Byte
   // Rx
   input  wire pad_srx_i,  // Receive Byte

`ifdef UART_HAS_BAUDRATE_OUTPUT
   output wire baud1_o,
`endif

   // modem signals
   output wire rts_o,
   input  wire cts_i,
   output wire dtr_o,
   input  wire dsr_i,
   input  wire ri_i,
   input  wire dcd_i
);

   // Wires
   // // general
   wire                clk_i;
   wire                cke_i;
   wire                arst_i;
   wire                uartInterrupt;
   // // Master interface
   wire                m_valid;
   wire [  ADDR_W-1:0] m_address;
   wire [  DATA_W-1:0] m_wdata;
   wire [DATA_W/8-1:0] m_wstrb;
   wire                m_rvalid;
   wire [  DATA_W-1:0] m_rdata;
   wire                m_ready;

   // Logic
   assign clk_i  = clk;
   assign cke_i  = 1'b1;
   assign arst_i = wb_rst_i;
   assign int_o  = uartInterrupt;

   iob_wishbone2iob #(
      .ADDR_W(ADDR_W),
      .DATA_W(DATA_W)
   ) wishbone2iob (
      // General input/outputs
      .clk_i        (clk_i),
      .cke_i        (cke_i),
      .arst_i       (arst_i),
      // WishBone input/outputs
      .wb_addr_i    (wb_adr_i),
      .wb_select_i  (wb_sel_i),
      .wb_we_i      (wb_we_i),
      .wb_cyc_i     (wb_cyc_i),
      .wb_stb_i     (wb_stb_i),
      .wb_data_i    (wb_dat_i),
      .wb_ack_o     (wb_ack_o),
      .wb_data_o    (wb_dat_o),
      // IOb-bus input/outputs
      .iob_valid_o (m_valid),
      .iob_address_o(m_address),
      .iob_wdata_o  (m_wdata),
      .iob_wstrb_o  (m_wstrb),
      .iob_rvalid_i (m_rvalid),
      .iob_rdata_i  (m_rdata),
      .iob_ready_i  (m_ready)
   );

   iob_uart16550 #(
      .DATA_W(DATA_W),  //PARAM & 32 & 64 & CPU data width
      .ADDR_W(ADDR_W)   //CPU address section width
   ) uart16550 (
      //RS232 interface
      .txd_o(pad_stx_o),
      .rxd_i(pad_srx_i),
      .rts_o(rts_o),
      .cts_i(cts_i),

      //CPU interface
      .clk_i       (clk_i),
      .cke_i       (cke_i),
      .arst_i      (arst_i),
      .iob_valid_i(m_valid),
      .iob_addr_i  (m_address),
      .iob_wdata_i (m_wdata),
      .iob_wstrb_i (m_wstrb),
      .iob_rvalid_o(m_rvalid),
      .iob_rdata_o (m_rdata),
      .iob_ready_o (m_ready),

      .interrupt_o(uartInterrupt)
   );

endmodule
