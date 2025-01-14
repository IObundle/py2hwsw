`timescale 1ns / 1ps

`include "uart_defines.vh"
`include "iob_uart16550_conf.vh"

module iob_uart16550 #(
   `include "iob_uart16550_params.vs"
) (
   `include "iob_uart16550_io.vs"
);

   wire [  `UART_ADDR_WIDTH-1:0] m_wb_adr;
   wire [`UART_DATA_WIDTH/8-1:0] m_wb_sel;
   wire                          m_wb_we;
   wire                          m_wb_cyc;
   wire                          m_wb_stb;
   wire [  `UART_DATA_WIDTH-1:0] m_wb_dat_req;
   wire                          m_wb_ack;
   wire [  `UART_DATA_WIDTH-1:0] m_wb_dat_resp;

   iob_iob2wishbone #(
      .ADDR_W    (`UART_ADDR_WIDTH),
      .DATA_W    (`UART_DATA_WIDTH),
      .READ_BYTES(1)
   ) iob2wishbone (
      // General input/outputs
      .clk_i       (clk_i),
      .cke_i       (cke_i),
      .arst_i      (arst_i),
      // IOb-bus input/outputs
      .iob_valid_i (iob_valid_i),
      .iob_addr_i  (iob_addr_i[`UART_ADDR_WIDTH-1:0]),
      .iob_wdata_i (iob_wdata_i),
      .iob_wstrb_i (iob_wstrb_i),
      .iob_rvalid_o(iob_rvalid_o),
      .iob_rdata_o (iob_rdata_o),
      .iob_ready_o (iob_ready_o),
      // WishBone input/outputs
      .wb_addr_o   (m_wb_adr),
      .wb_select_o (m_wb_sel),
      .wb_we_o     (m_wb_we),
      .wb_cyc_o    (m_wb_cyc),
      .wb_stb_o    (m_wb_stb),
      .wb_data_o   (m_wb_dat_req),
      .wb_ack_i    (m_wb_ack),
      .wb_data_i   (m_wb_dat_resp)
   );

   uart_top uart16550 (
      .wb_clk_i (clk_i),
      // WISHBONE interface
      .wb_rst_i (arst_i),
      .wb_adr_i (m_wb_adr),
      .wb_sel_i (m_wb_sel),
      .wb_we_i  (m_wb_we),
      .wb_cyc_i (m_wb_cyc),
      .wb_stb_i (m_wb_stb),
      .wb_dat_i (m_wb_dat_req),
      .wb_ack_o (m_wb_ack),
      .wb_dat_o (m_wb_dat_resp),
      .int_o    (interrupt_o),
`ifdef UART_HAS_BAUDRATE_OUTPUT
      .baud1_o  (),
`endif
      // UART signals
      .srx_pad_i(rs232_rxd_i),
      .stx_pad_o(rs232_txd_o),
      .rts_pad_o(rs232_rts_o),
      .cts_pad_i(rs232_cts_i),
      .dtr_pad_o(),
      .dsr_pad_i(1'b1),
      .ri_pad_i (1'b0),
      .dcd_pad_i(1'b0)
   );

endmodule
