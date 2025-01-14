`timescale 1ns / 1ps

`include "iob_bsp.vh"
`include "iob_eth_conf.vh"
`include "iob_eth_csrs_def.vh"

/*
 Ethernet Core
*/

module iob_eth #(
    `include "iob_eth_params.vs"
) (
    `include "iob_eth_io.vs"
);

   `include "iob_eth_wires.vs"

   // configuration control and status register file.
   `include "iob_eth_subblocks.vs"

  wire internal_frame_word_wen_wr;
  wire internal_frame_word_ren_rd;
  wire internal_tx_bd_cnt_ren_rd;
  wire internal_rx_bd_cnt_ren_rd;
  wire internal_tx_word_cnt_ren_rd;
  wire internal_rx_word_cnt_ren_rd;
  wire internal_bd_wen_wr;
  wire internal_bd_ren_rd;

  assign internal_frame_word_wen_wr = frame_word_wen_wr & iob_ready_o;
  assign internal_frame_word_ren_rd = frame_word_ren_rd & iob_ready_o;
  assign internal_tx_bd_cnt_ren_rd = tx_bd_cnt_ren_rd & iob_ready_o;
  assign internal_rx_bd_cnt_ren_rd = rx_bd_cnt_ren_rd & iob_ready_o;
  assign internal_tx_word_cnt_ren_rd = tx_word_cnt_ren_rd & iob_ready_o;
  assign internal_rx_word_cnt_ren_rd = rx_word_cnt_ren_rd & iob_ready_o;
  assign internal_bd_wen_wr = bd_wen_wr & iob_ready_o;
  assign internal_bd_ren_rd = bd_ren_rd & iob_ready_o;

  // BD rvalid is iob_valid registered
  wire bd_rvalid_nxt;
  assign bd_rvalid_nxt = iob_valid_i & internal_bd_ren_rd;
  iob_reg #(
      .DATA_W (1),
      .RST_VAL(1'd0)
  ) iob_reg_BD_rvalid (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(bd_rvalid_nxt),
      .data_o(bd_rvalid_rd)
  );

  // Connect write outputs to read
  assign moder_rd = moder_wr;
  assign int_source_rd = int_source_wr;
  assign int_mask_rd = int_mask_wr;
  assign ipgt_rd = ipgt_wr;
  assign ipgr1_rd = ipgr1_wr;
  assign ipgr2_rd = ipgr2_wr;
  assign packetlen_rd = packetlen_wr;
  assign collconf_rd = collconf_wr;
  assign tx_bd_num_rd = tx_bd_num_wr;
  assign ctrlmoder_rd = ctrlmoder_wr;
  assign miimoder_rd = miimoder_wr;
  assign miicommand_rd = miicommand_wr;
  assign miiaddress_rd = miiaddress_wr;
  assign miitx_data_rd = miitx_data_wr;
  assign miirx_data_rd = miirx_data_wr;
  assign miistatus_rd = miistatus_wr;
  assign mac_addr0_rd = mac_addr0_wr;
  assign mac_addr1_rd = mac_addr1_wr;
  assign eth_hash0_adr_rd = eth_hash0_adr_wr;
  assign eth_hash1_adr_rd = eth_hash1_adr_wr;
  assign eth_txctrl_rd = eth_txctrl_wr;

  // ETH CLOCK DOMAIN

  wire                         iob_eth_tx_buffer_enA;
  wire [`IOB_ETH_BUFFER_W-1:0] iob_eth_tx_buffer_addrA;
  wire [                8-1:0] iob_eth_tx_buffer_dinA;
  wire [`IOB_ETH_BUFFER_W-1:0] iob_eth_tx_buffer_addrB;
  wire [                8-1:0] iob_eth_tx_buffer_doutB;

  wire                         iob_eth_rx_buffer_enA;
  wire [`IOB_ETH_BUFFER_W-1:0] iob_eth_rx_buffer_addrA;
  wire [                8-1:0] iob_eth_rx_buffer_dinA;
  wire                         iob_eth_rx_buffer_enB;
  wire [`IOB_ETH_BUFFER_W-1:0] iob_eth_rx_buffer_addrB;
  wire [                8-1:0] iob_eth_rx_buffer_doutB;


  assign MTxErr_o = 1'b0;  //TODO

  //
  //  PHY RESET
  //

  wire [21-1:0] phy_rst_cnt_o;
  iob_acc #(
      .DATA_W(21),
`ifndef SIMULATION
      .RST_VAL(21'h100000 | (PHY_RST_CNT - 1))
`else
      .RST_VAL(21'h1000FF)  // Shorter reset for simulation
`endif
  ) phy_rst_cnt_acc (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (1'b0),
      .en_i  (phy_rst_cnt_o[20]),
      .incr_i(-21'd1),
      .data_o(phy_rst_cnt_o)
  );
  wire phy_rst = phy_rst_cnt_o[20];
  assign phy_rstn_o = ~phy_rst;
  assign phy_rst_val_rd = phy_rst;

  //
  // SYNCHRONIZERS
  //

  // arst synchronizers
  wire rx_arst;
  iob_sync #(
      .DATA_W(1)
  ) rx_arst_sync (
      .clk_i(MRxClk_i),
      .arst_i(arst_i),
      .signal_i(phy_rst),
      .signal_o(rx_arst)
  );

  wire tx_arst;
  iob_sync #(
      .DATA_W(1)
  ) tx_arst_sync (
      .clk_i(MTxClk_i),
      .arst_i(arst_i),
      .signal_i(phy_rst),
      .signal_o(tx_arst)
  );

  // clk to MRxClk_i (f2s)
  wire rcv_ack;
  wire eth_rcv_ack;
  iob_sync #(
      .DATA_W(1)
  ) rcv_f2s_sync (
      .clk_i   (MRxClk_i),
      .arst_i   (rx_arst),
      .signal_i (rcv_ack),
      .signal_o (eth_rcv_ack)
  );

  // clk to MTxClk_i (f2s)
  wire eth_send;
  wire send;
  iob_sync #(
      .DATA_W(1)
  ) send_f2s_sync (
      .clk_i   (MTxClk_i),
      .arst_i   (tx_arst),
      .signal_i (send),
      .signal_o (eth_send)
  );

  wire eth_crc_en;
  wire crc_en;
  iob_sync #(
      .DATA_W(1)
  ) crc_en_f2s_sync (
      .clk_i   (MTxClk_i),
      .arst_i   (tx_arst),
      .signal_i (crc_en),
      .signal_o (eth_crc_en)
  );

  wire [11-1:0] eth_tx_nbytes;
  wire [11-1:0] tx_nbytes;
  iob_sync #(
      .DATA_W(11)
  ) tx_nbytes_f2s_sync (
      .clk_i   (MTxClk_i),
      .arst_i  (tx_arst),
      .signal_i(tx_nbytes),
      .signal_o(eth_tx_nbytes)
  );

  // MRxClk_i to clk (s2f)

  wire eth_crc_err;
  wire crc_err;
  iob_sync #(
      .DATA_W(1)
  ) crc_err_sync (
      .clk_i   (clk_i),
      .arst_i   (arst_i),
      .signal_i (eth_crc_err),
      .signal_o (crc_err)
  );

  wire [`IOB_ETH_BUFFER_W-1:0] rx_nbytes;
  iob_sync #(
      .DATA_W(`IOB_ETH_BUFFER_W)
  ) rx_nbytes_sync (
      .clk_i   (clk_i),
      .arst_i   (arst_i),
      .signal_i (iob_eth_rx_buffer_addrA),
      .signal_o (rx_nbytes)
  );

  wire eth_rx_data_rcvd;
  wire rx_data_rcvd;
  iob_sync #(
      .DATA_W(1)
  ) rx_data_rcvd_sync (
      .clk_i   (clk_i),
      .arst_i   (arst_i),
      .signal_i (eth_rx_data_rcvd),
      .signal_o (rx_data_rcvd)
  );

  // MTxClk_i to clk (s2f)

  wire eth_tx_ready;
  wire tx_ready;
  iob_sync #(
      .DATA_W(1)
  ) tx_ready_sync (
      .clk_i   (clk_i),
      .arst_i   (arst_i),
      .signal_i (eth_tx_ready),
      .signal_o (tx_ready)
  );

  //
  // TRANSMITTER
  //

  iob_eth_tx tx (
      .arst_i   (tx_arst),
      // Buffer interface
      .addr_o   (iob_eth_tx_buffer_addrB),
      .data_i   (iob_eth_tx_buffer_doutB),
      // DMA control interface
      .send_i   (eth_send),
      .ready_o  (eth_tx_ready),
      .nbytes_i (eth_tx_nbytes),
      .crc_en_i (eth_crc_en),
      // MII interface
      .tx_clk_i (MTxClk_i),
      .tx_en_o  (MTxEn_o),
      .tx_data_o(MTxD_o)
  );


  //
  // RECEIVER
  //

  iob_eth_rx rx (
      .arst_i     (rx_arst),
      // Buffer interface
      .wr_o       (iob_eth_rx_buffer_enA),
      .addr_o     (iob_eth_rx_buffer_addrA),
      .data_o     (iob_eth_rx_buffer_dinA),
      // DMA control interface
      .rcv_ack_i  (eth_rcv_ack),
      .data_rcvd_o(eth_rx_data_rcvd),
      .crc_err_o  (eth_crc_err),
      // MII interface
      .rx_clk_i   (MRxClk_i),
      .rx_data_i  (MRxD_i),
      .rx_dv_i    (MRxDv_i)
  );

  // BUFFER memories
  iob_ram_at2p #(
      .DATA_W(8),
      // Note: the tx buffer also includes PREAMBLE+SFD,
      // maybe we should increase this size to acount for
      // this.
      .ADDR_W(`IOB_ETH_BUFFER_W)
  ) tx_buffer (
      // Front-End (written by host)
      .w_clk_i (clk_i),
      .w_en_i  (iob_eth_tx_buffer_enA),
      .w_addr_i(iob_eth_tx_buffer_addrA),
      .w_data_i(iob_eth_tx_buffer_dinA),

      // Back-End (read by core)
      .r_clk_i (MTxClk_i),
      .r_en_i  (1'b1),
      .r_addr_i(iob_eth_tx_buffer_addrB),
      .r_data_o(iob_eth_tx_buffer_doutB)
  );

  iob_ram_at2p #(
      .DATA_W(8),
      .ADDR_W(`IOB_ETH_BUFFER_W)
  ) rx_buffer (
      // Front-End (written by core)
      .w_clk_i (MRxClk_i),
      .w_en_i  (iob_eth_rx_buffer_enA),
      .w_addr_i(iob_eth_rx_buffer_addrA),
      .w_data_i(iob_eth_rx_buffer_dinA),

      // Back-End (read by host)
      .r_clk_i (clk_i),
      .r_en_i  (iob_eth_rx_buffer_enB),
      .r_addr_i(iob_eth_rx_buffer_addrB),
      .r_data_o(iob_eth_rx_buffer_doutB)
  );

  // DMA buffer descriptor wires
  wire dma_bd_en;
  wire [7:0] dma_bd_addr;
  wire dma_bd_wen;
  wire [31:0] dma_bd_i;
  wire [31:0] dma_bd_o;
  // DMA interrupt wires
  wire rx_irq;
  wire tx_irq;
  assign inta_o = rx_irq | tx_irq;

  // Data transfer module (includes DMA)
  iob_eth_dma #(
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_DATA_W(AXI_DATA_W),
      .AXI_LEN_W (AXI_LEN_W),
      .AXI_ID_W  (AXI_ID_W),
      //.BURST_W   (BURST_W),
      .BUFFER_W  (`IOB_ETH_BUFFER_W),
      .BD_ADDR_W (BD_NUM_LOG2 + 1)
  ) dma_inst (
      // SW reg control interface
      .rx_en_i(moder_wr[0]),
      .tx_en_i(moder_wr[1]),
      // Note: ethmac datasheet specifies TX_BD_NUM should support 0x80 value
      .tx_bd_num_i(tx_bd_num_wr[BD_NUM_LOG2-1:0]),

      // Buffer descriptors
      .bd_en_o(dma_bd_en),
      .bd_addr_o(dma_bd_addr),
      .bd_wen_o(dma_bd_wen),
      .bd_i(dma_bd_i),
      .bd_o(dma_bd_o),

      // TX Front-End
      .eth_data_wr_wen_o(iob_eth_tx_buffer_enA),  // |ETH_DATA_WR_wstrb
      .eth_data_wr_addr_o(iob_eth_tx_buffer_addrA),
      .eth_data_wr_wdata_o(iob_eth_tx_buffer_dinA),
      .tx_ready_i(tx_ready),
      .crc_en_o(crc_en),
      .tx_nbytes_o(tx_nbytes),
      .send_o(send),

      // RX Back-End
      .eth_data_rd_ren_o(iob_eth_rx_buffer_enB),
      .eth_data_rd_addr_o(iob_eth_rx_buffer_addrB),
      .eth_data_rd_rdata_i(iob_eth_rx_buffer_doutB),
      .rx_data_rcvd_i(rx_data_rcvd),
      .crc_err_i(crc_err),
      .rx_nbytes_i(rx_nbytes),
      .rcv_ack_o(rcv_ack),

      // AXI master interface
      // Can't use generated include, because of `internal_axi_*addr_o` signals.
      //include "axi_m_m_portmap.vs"
      .axi_awid_o(axi_awid_o),  //Address write channel ID.
      .axi_awaddr_o(axi_awaddr_o),  //Address write channel address.
      .axi_awlen_o(axi_awlen_o),  //Address write channel burst length.
      .axi_awsize_o(axi_awsize_o), //Address write channel burst size. This signal indicates the size of each transfer in the burst.
      .axi_awburst_o(axi_awburst_o),  //Address write channel burst type.
      .axi_awlock_o(axi_awlock_o),  //Address write channel lock type.
      .axi_awcache_o(axi_awcache_o), //Address write channel memory type. Set to 0000 if master output; ignored if slave input.
      .axi_awprot_o(axi_awprot_o), //Address write channel protection type. Set to 000 if master output; ignored if slave input.
      .axi_awqos_o(axi_awqos_o),  //Address write channel quality of service.
      .axi_awvalid_o(axi_awvalid_o),  //Address write channel valid.
      .axi_awready_i(axi_awready_i),  //Address write channel ready.
      .axi_wdata_o(axi_wdata_o),  //Write channel data.
      .axi_wstrb_o(axi_wstrb_o),  //Write channel write strobe.
      .axi_wlast_o(axi_wlast_o),  //Write channel last word flag.
      .axi_wvalid_o(axi_wvalid_o),  //Write channel valid.
      .axi_wready_i(axi_wready_i),  //Write channel ready.
      .axi_bid_i(axi_bid_i),  //Write response channel ID.
      .axi_bresp_i(axi_bresp_i),  //Write response channel response.
      .axi_bvalid_i(axi_bvalid_i),  //Write response channel valid.
      .axi_bready_o(axi_bready_o),  //Write response channel ready.
      .axi_arid_o(axi_arid_o),  //Address read channel ID.
      .axi_araddr_o(axi_araddr_o),  //Address read channel address.
      .axi_arlen_o(axi_arlen_o),  //Address read channel burst length.
      .axi_arsize_o(axi_arsize_o), //Address read channel burst size. This signal indicates the size of each transfer in the burst.
      .axi_arburst_o(axi_arburst_o),  //Address read channel burst type.
      .axi_arlock_o(axi_arlock_o),  //Address read channel lock type.
      .axi_arcache_o(axi_arcache_o), //Address read channel memory type. Set to 0000 if master output; ignored if slave input.
      .axi_arprot_o(axi_arprot_o), //Address read channel protection type. Set to 000 if master output; ignored if slave input.
      .axi_arqos_o(axi_arqos_o),  //Address read channel quality of service.
      .axi_arvalid_o(axi_arvalid_o),  //Address read channel valid.
      .axi_arready_i(axi_arready_i),  //Address read channel ready.
      .axi_rid_i(axi_rid_i),  //Read channel ID.
      .axi_rdata_i(axi_rdata_i),  //Read channel data.
      .axi_rresp_i(axi_rresp_i),  //Read channel response.
      .axi_rlast_i(axi_rlast_i),  //Read channel last word.
      .axi_rvalid_i(axi_rvalid_i),  //Read channel valid.
      .axi_rready_o(axi_rready_o),  //Read channel ready.

      // No-DMA interface
      .tx_bd_cnt_o(tx_bd_cnt_rdata_rd),
      .tx_word_cnt_o(tx_word_cnt_rdata_rd),
      .tx_frame_word_wen_i(internal_frame_word_wen_wr),
      .tx_frame_word_wdata_i(frame_word_wdata_wr),
      .tx_frame_word_ready_o(frame_word_wready_wr),
      .rx_bd_cnt_o(rx_bd_cnt_rdata_rd),
      .rx_word_cnt_o(rx_word_cnt_rdata_rd),
      .rx_frame_word_ren_i(internal_frame_word_ren_rd),
      .rx_frame_word_rdata_o(frame_word_rdata_rd),
      .rx_frame_word_ready_o(frame_word_rready_rd),

      // Interrupts
      .tx_irq_o(tx_irq),
      .rx_irq_o(rx_irq),

      // General signals interface
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i)
  );

  // No-DMA interface signals
  assign frame_word_rvalid_rd = internal_frame_word_ren_rd;
  assign tx_bd_cnt_rvalid_rd = internal_tx_bd_cnt_ren_rd;
  assign tx_bd_cnt_rready_rd = 1'b1;
  assign rx_bd_cnt_rvalid_rd = internal_rx_bd_cnt_ren_rd;
  assign rx_bd_cnt_rready_rd = 1'b1;
  assign tx_word_cnt_rvalid_rd = internal_tx_word_cnt_ren_rd;
  assign tx_word_cnt_rready_rd = 1'b1;
  assign rx_word_cnt_rvalid_rd = internal_rx_word_cnt_ren_rd;
  assign rx_word_cnt_rready_rd = 1'b1;
  assign rx_nbytes_rdata_rd = rx_data_rcvd ? rx_nbytes : 0;
  assign rx_nbytes_rvalid_rd = ~rcv_ack;  // Wait for ack complete
  assign rx_nbytes_rready_rd = 1'b1;

  // wire [31:0] buffer_addr = (iob_addr_i - `IOB_ETH_BD_ADDR) >> 2; Might still be needed

  assign bd_wready_wr = 1'b1;
  assign bd_rready_rd = 1'b1;

  // Buffer descriptors memory
  iob_ram_tdp #(
      .DATA_W(32),
      .ADDR_W(BD_NUM_LOG2 + 1),
      .MEM_NO_READ_ON_WRITE(1)
  ) bd_ram (
      .clk_i(clk_i),

      // Port A - csrss
      .addrA_i(bd_waddr_wr[BD_NUM_LOG2:0]),
      .enA_i(internal_bd_wen_wr || internal_bd_ren_rd),
      .weA_i(internal_bd_wen_wr),
      .dA_i(iob_wdata_i),
      .dA_o(bd_rdata_rd),

      // Port B - DMA module
      .addrB_i(dma_bd_addr),
      .enB_i(dma_bd_en),
      .weB_i(dma_bd_wen),
      .dB_i(dma_bd_o),
      .dB_o(dma_bd_i)
  );

endmodule
