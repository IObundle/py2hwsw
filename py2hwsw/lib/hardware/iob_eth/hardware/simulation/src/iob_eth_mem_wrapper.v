`timescale 1ns / 1ps

`include "iob_utils.vh"
`include "iob_eth_defines.vh"

module iob_eth_mem_wrapper #(
    parameter integer ADDR_W = `IOB_ETH_CSRS_ADDR_W,
    parameter integer DATA_W = 32,
    parameter integer AXI_ID_W = 1,
    // Fit at least two frames in memory (2 * 2^9 words * 4 byte-word)
    // 12 is the minimum supported by axi_interconnect
    parameter integer AXI_ADDR_W = 12,
    parameter integer AXI_DATA_W = 32,
    parameter integer AXI_LEN_W = 8,
    parameter integer MEM_ADDR_OFFSET = `IOB_ETH_MEM_ADDR_OFFSET,
    parameter integer PHY_RST_CNT = `IOB_ETH_PHY_RST_CNT,
    parameter integer BD_NUM_LOG2 = `IOB_ETH_BD_NUM_LOG2,
    parameter integer BUFFER_W = `IOB_ETH_BUFFER_W
) (
    // Eth IOb csrs interface
    `include "iob_s_port.vs"

    // Testbench memory control
    input [AXI_ADDR_W-1:0] tb_addr,
    input tb_awvalid,
    output tb_awready,
    input tb_arvalid,
    output tb_arready,
    input [AXI_DATA_W-1:0] tb_wdata,
    input tb_wvalid,
    output tb_wready,
    output [AXI_DATA_W-1:0] tb_rdata,
    output tb_rvalid,
    input tb_rready,

    `include "clk_en_rst_s_port.vs"
);

  // ETH SIDE
  reg        mii_clk;
  wire [3:0] mii_data;
  wire       mii_en;

  // DMA wires
  `include "bus2_axi_wire.vs"

  // Wires to connect the interconnect with the memory
  `include "memory_axi_wire.vs"

  //ethernet clock: 4x slower than system clock
  reg [1:0] eth_cnt = 2'b0;

  always @(posedge clk_i) begin
    eth_cnt <= eth_cnt + 1'b1;
    mii_clk <= eth_cnt[1];
  end

  // UUT ethernet instance (MII signals connected to itself)
  iob_eth #(
      .AXI_ID_W  (AXI_ID_W),
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_DATA_W(AXI_DATA_W),
      .AXI_LEN_W (AXI_LEN_W)
  ) eth (
      .inta_o(),

      // PHY
      .MTxClk(mii_clk),
      .MTxD  (mii_data),
      .MTxEn (mii_en),
      .MTxErr(),
      .MRxClk(mii_clk),
      .MRxDv (mii_en),
      .MRxD  (mii_data),
      .MRxErr(1'b0),
      .MColl (1'b0),
      .MCrS  (1'b0),
      .MDC   (),
      .MDIO  (),

      .phy_rstn_o(),

      `include "iob_s_s_portmap.vs"

      // Connect DMA interface to interconnect (bus index 0)
      .axi_awid_o(axi_awid[0+:AXI_ID_W]),
      .axi_awaddr_o(axi_awaddr[0+:AXI_ADDR_W]),
      .axi_awlen_o(axi_awlen[0+:AXI_LEN_W]),
      .axi_awsize_o(axi_awsize[0+:3]),
      .axi_awburst_o(axi_awburst[0+:2]),
      .axi_awlock_o(axi_awlock[0+:2]),
      .axi_awcache_o(axi_awcache[0+:4]),
      .axi_awprot_o(axi_awprot[0+:3]),
      .axi_awqos_o(axi_awqos[0+:4]),
      .axi_awvalid_o(axi_awvalid[0+:1]),
      .axi_awready_i(axi_awready[0+:1]),
      .axi_wdata_o(axi_wdata[0+:AXI_DATA_W]),
      .axi_wstrb_o(axi_wstrb[0+:(AXI_DATA_W/8)]),
      .axi_wlast_o(axi_wlast[0+:1]),
      .axi_wvalid_o(axi_wvalid[0+:1]),
      .axi_wready_i(axi_wready[0+:1]),
      .axi_bid_i(axi_bid[0+:AXI_ID_W]),
      .axi_bresp_i(axi_bresp[0+:2]),
      .axi_bvalid_i(axi_bvalid[0+:1]),
      .axi_bready_o(axi_bready[0+:1]),
      .axi_arid_o(axi_arid[0+:AXI_ID_W]),
      .axi_araddr_o(axi_araddr[0+:AXI_ADDR_W]),
      .axi_arlen_o(axi_arlen[0+:AXI_LEN_W]),
      .axi_arsize_o(axi_arsize[0+:3]),
      .axi_arburst_o(axi_arburst[0+:2]),
      .axi_arlock_o(axi_arlock[0+:2]),
      .axi_arcache_o(axi_arcache[0+:4]),
      .axi_arprot_o(axi_arprot[0+:3]),
      .axi_arqos_o(axi_arqos[0+:4]),
      .axi_arvalid_o(axi_arvalid[0+:1]),
      .axi_arready_i(axi_arready[0+:1]),
      .axi_rid_i(axi_rid[0+:AXI_ID_W]),
      .axi_rdata_i(axi_rdata[0+:AXI_DATA_W]),
      .axi_rresp_i(axi_rresp[0+:2]),
      .axi_rlast_i(axi_rlast[0+:1]),
      .axi_rvalid_i(axi_rvalid[0+:1]),
      .axi_rready_o(axi_rready[0+:1]),

      .clk_i (clk_i),
      .arst_i(arst_i),
      .cke_i (cke_i)
  );

  //Axi interconnect
  axi_interconnect #(
      .ID_WIDTH    (AXI_ID_W),
      .DATA_WIDTH  (AXI_DATA_W),
      .ADDR_WIDTH  (AXI_ADDR_W),
      .M_ADDR_WIDTH(AXI_ADDR_W),
      .S_COUNT     (2),           // Eth core and testbench ctrl
      .M_COUNT     (1)
  ) system_axi_interconnect (
      .clk(clk_i),
      .rst(arst_i),

      // Need to use manually defined connections because awlock and arlock of interconnect is only on bit for each slave
      .s_axi_awid(axi_awid),  //Address write channel ID.
      .s_axi_awaddr(axi_awaddr),  //Address write channel address.
      .s_axi_awlen(axi_awlen),  //Address write channel burst length.
      .s_axi_awsize  (axi_awsize),  //Address write channel burst size. This signal indicates the size of each transfer in the burst.
      .s_axi_awburst(axi_awburst),  //Address write channel burst type.
      .s_axi_awlock({axi_awlock[2], axi_awlock[0]}),  //Address write channel lock type.
      .s_axi_awcache (axi_awcache), //Address write channel memory type. Transactions set with Normal, Non-cacheable, Modifiable, and Bufferable (0011).
      .s_axi_awprot  (axi_awprot),  //Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).
      .s_axi_awqos(axi_awqos),  //Address write channel quality of service.
      .s_axi_awvalid(axi_awvalid),  //Address write channel valid.
      .s_axi_awready(axi_awready),  //Address write channel ready.
      .s_axi_wdata(axi_wdata),  //Write channel data.
      .s_axi_wstrb(axi_wstrb),  //Write channel write strobe.
      .s_axi_wlast(axi_wlast),  //Write channel last word flag.
      .s_axi_wvalid(axi_wvalid),  //Write channel valid.
      .s_axi_wready(axi_wready),  //Write channel ready.
      .s_axi_bid(axi_bid),  //Write response channel ID.
      .s_axi_bresp(axi_bresp),  //Write response channel response.
      .s_axi_bvalid(axi_bvalid),  //Write response channel valid.
      .s_axi_bready(axi_bready),  //Write response channel ready.
      .s_axi_arid(axi_arid),  //Address read channel ID.
      .s_axi_araddr(axi_araddr),  //Address read channel address.
      .s_axi_arlen(axi_arlen),  //Address read channel burst length.
      .s_axi_arsize  (axi_arsize),  //Address read channel burst size. This signal indicates the size of each transfer in the burst.
      .s_axi_arburst(axi_arburst),  //Address read channel burst type.
      .s_axi_arlock({axi_arlock[2], axi_arlock[0]}),  //Address read channel lock type.
      .s_axi_arcache (axi_arcache), //Address read channel memory type. Transactions set with Normal, Non-cacheable, Modifiable, and Bufferable (0011).
      .s_axi_arprot  (axi_arprot),  //Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).
      .s_axi_arqos(axi_arqos),  //Address read channel quality of service.
      .s_axi_arvalid(axi_arvalid),  //Address read channel valid.
      .s_axi_arready(axi_arready),  //Address read channel ready.
      .s_axi_rid(axi_rid),  //Read channel ID.
      .s_axi_rdata(axi_rdata),  //Read channel data.
      .s_axi_rresp(axi_rresp),  //Read channel response.
      .s_axi_rlast(axi_rlast),  //Read channel last word.
      .s_axi_rvalid(axi_rvalid),  //Read channel valid.
      .s_axi_rready(axi_rready),  //Read channel ready.

      // Used manually defined connections because awlock and arlock of interconnect is only on bit.
      .m_axi_awid(memory_axi_awid[0+:AXI_ID_W]),  //Address write channel ID.
      .m_axi_awaddr(memory_axi_awaddr[0+:AXI_ADDR_W]),  //Address write channel address.
      .m_axi_awlen(memory_axi_awlen[0+:AXI_LEN_W]),  //Address write channel burst length.
      .m_axi_awsize  (memory_axi_awsize[0+:3]),              //Address write channel burst size. This signal indicates the size of each transfer in the burst.
      .m_axi_awburst(memory_axi_awburst[0+:2]),  //Address write channel burst type.
      .m_axi_awlock(memory_axi_awlock[0+:1]),  //Address write channel lock type.
      .m_axi_awcache (memory_axi_awcache[0+:4]),             //Address write channel memory type. Transactions set with Normal, Non-cacheable, Modifiable, and Bufferable (0011).
      .m_axi_awprot  (memory_axi_awprot[0+:3]),              //Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).
      .m_axi_awqos(memory_axi_awqos[0+:4]),  //Address write channel quality of service.
      .m_axi_awvalid(memory_axi_awvalid[0+:1]),  //Address write channel valid.
      .m_axi_awready(memory_axi_awready[0+:1]),  //Address write channel ready.
      .m_axi_wdata(memory_axi_wdata[0+:AXI_DATA_W]),  //Write channel data.
      .m_axi_wstrb(memory_axi_wstrb[0+:(AXI_DATA_W/8)]),  //Write channel write strobe.
      .m_axi_wlast(memory_axi_wlast[0+:1]),  //Write channel last word flag.
      .m_axi_wvalid(memory_axi_wvalid[0+:1]),  //Write channel valid.
      .m_axi_wready(memory_axi_wready[0+:1]),  //Write channel ready.
      .m_axi_bid(memory_axi_bid[0+:AXI_ID_W]),  //Write response channel ID.
      .m_axi_bresp(memory_axi_bresp[0+:2]),  //Write response channel response.
      .m_axi_bvalid(memory_axi_bvalid[0+:1]),  //Write response channel valid.
      .m_axi_bready(memory_axi_bready[0+:1]),  //Write response channel ready.
      .m_axi_arid(memory_axi_arid[0+:AXI_ID_W]),  //Address read channel ID.
      .m_axi_araddr(memory_axi_araddr[0+:AXI_ADDR_W]),  //Address read channel address.
      .m_axi_arlen(memory_axi_arlen[0+:AXI_LEN_W]),  //Address read channel burst length.
      .m_axi_arsize  (memory_axi_arsize[0+:3]),              //Address read channel burst size. This signal indicates the size of each transfer in the burst.
      .m_axi_arburst(memory_axi_arburst[0+:2]),  //Address read channel burst type.
      .m_axi_arlock(memory_axi_arlock[0+:1]),  //Address read channel lock type.
      .m_axi_arcache (memory_axi_arcache[0+:4]),             //Address read channel memory type. Transactions set with Normal, Non-cacheable, Modifiable, and Bufferable (0011).
      .m_axi_arprot  (memory_axi_arprot[0+:3]),              //Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).
      .m_axi_arqos(memory_axi_arqos[0+:4]),  //Address read channel quality of service.
      .m_axi_arvalid(memory_axi_arvalid[0+:1]),  //Address read channel valid.
      .m_axi_arready(memory_axi_arready[0+:1]),  //Address read channel ready.
      .m_axi_rid(memory_axi_rid[0+:AXI_ID_W]),  //Read channel ID.
      .m_axi_rdata(memory_axi_rdata[0+:AXI_DATA_W]),  //Read channel data.
      .m_axi_rresp(memory_axi_rresp[0+:2]),  //Read channel response.
      .m_axi_rlast(memory_axi_rlast[0+:1]),  //Read channel last word.
      .m_axi_rvalid(memory_axi_rvalid[0+:1]),  //Read channel valid.
      .m_axi_rready(memory_axi_rready[0+:1]),  //Read channel ready.

      //optional signals
      .s_axi_awuser  (2'b0),
      .s_axi_wuser   (2'b0),
      .s_axi_aruser  (2'b0),
      .s_axi_buser   (),
      .s_axi_ruser   (),
      .m_axi_awuser  (),
      .m_axi_wuser   (),
      .m_axi_aruser  (),
      .m_axi_buser   (1'b0),
      .m_axi_ruser   (1'b0),
      .m_axi_awregion(),
      .m_axi_arregion()
  );

  axi_ram #(
      .ID_WIDTH  (AXI_ID_W),
      .DATA_WIDTH(AXI_DATA_W),
      .ADDR_WIDTH(AXI_ADDR_W),
      .LEN_WIDTH (AXI_LEN_W)
  ) ddr_model_mem (
      .axi_awid_i(memory_axi_awid),  //Address write channel ID.
      .axi_awaddr_i(memory_axi_awaddr),  //Address write channel address.
      .axi_awlen_i(memory_axi_awlen),  //Address write channel burst length.
      .axi_awsize_i(memory_axi_awsize), //Address write channel burst size. This signal indicates the size of each transfer in the burst.
      .axi_awburst_i(memory_axi_awburst),  //Address write channel burst type.
      .axi_awlock_i(memory_axi_awlock),  //Address write channel lock type.
      .axi_awcache_i(memory_axi_awcache), //Address write channel memory type. Set to 0000 if master output; ignored if slave input.
      .axi_awprot_i(memory_axi_awprot), //Address write channel protection type. Set to 000 if master output; ignored if slave input.
      .axi_awqos_i(memory_axi_awqos),  //Address write channel quality of service.
      .axi_awvalid_i(memory_axi_awvalid),  //Address write channel valid.
      .axi_awready_o(memory_axi_awready),  //Address write channel ready.
      .axi_wdata_i(memory_axi_wdata),  //Write channel data.
      .axi_wstrb_i(memory_axi_wstrb),  //Write channel write strobe.
      .axi_wlast_i(memory_axi_wlast),  //Write channel last word flag.
      .axi_wvalid_i(memory_axi_wvalid),  //Write channel valid.
      .axi_wready_o(memory_axi_wready),  //Write channel ready.
      .axi_bid_o(memory_axi_bid),  //Write response channel ID.
      .axi_bresp_o(memory_axi_bresp),  //Write response channel response.
      .axi_bvalid_o(memory_axi_bvalid),  //Write response channel valid.
      .axi_bready_i(memory_axi_bready),  //Write response channel ready.
      .axi_arid_i(memory_axi_arid),  //Address read channel ID.
      .axi_araddr_i(memory_axi_araddr),  //Address read channel address.
      .axi_arlen_i(memory_axi_arlen),  //Address read channel burst length.
      .axi_arsize_i(memory_axi_arsize), //Address read channel burst size. This signal indicates the size of each transfer in the burst.
      .axi_arburst_i(memory_axi_arburst),  //Address read channel burst type.
      .axi_arlock_i(memory_axi_arlock),  //Address read channel lock type.
      .axi_arcache_i(memory_axi_arcache), //Address read channel memory type. Set to 0000 if master output; ignored if slave input.
      .axi_arprot_i(memory_axi_arprot), //Address read channel protection type. Set to 000 if master output; ignored if slave input.
      .axi_arqos_i(memory_axi_arqos),  //Address read channel quality of service.
      .axi_arvalid_i(memory_axi_arvalid),  //Address read channel valid.
      .axi_arready_o(memory_axi_arready),  //Address read channel ready.
      .axi_rid_o(memory_axi_rid),  //Read channel ID.
      .axi_rdata_o(memory_axi_rdata),  //Read channel data.
      .axi_rresp_o(memory_axi_rresp),  //Read channel response.
      .axi_rlast_o(memory_axi_rlast),  //Read channel last word.
      .axi_rvalid_o(memory_axi_rvalid),  //Read channel valid.
      .axi_rready_i(memory_axi_rready),  //Read channel ready.

      .clk_i(clk_i),
      .rst_i(arst_i)
  );

  // AXI bus[1] signals for testbench
  assign axi_awid[1*(AXI_ID_W)+:AXI_ID_W] = {AXI_ID_W{1'b0}};  //input
  assign axi_awaddr[1*(AXI_ADDR_W)+:AXI_ADDR_W] = tb_addr;  //input
  assign axi_awlen[1*(AXI_LEN_W)+:AXI_LEN_W] = {AXI_LEN_W{1'b0}};  //input
  assign axi_awsize[1*(3)+:3] = 3'b0;  //input
  assign axi_awburst[1*(2)+:2] = 2'b0;  //input
  assign axi_awlock[1*(2)+:2] = 2'b0;  //input
  assign axi_awcache[1*(4)+:4] = 4'b0;  //input
  assign axi_awprot[1*(3)+:3] = 3'b0;  //input
  assign axi_awqos[1*(4)+:4] = 4'b0;  //input
  assign axi_awvalid[1*(1)+:1] = tb_awvalid;  //input
  assign tb_awready = axi_awready[1*(1)+:1];  //output
  assign axi_wdata[1*(AXI_DATA_W)+:AXI_DATA_W] = tb_wdata;  //input
  assign axi_wstrb[1*((AXI_DATA_W/8))+:(AXI_DATA_W/8)] = {(AXI_DATA_W / 8) {1'b1}};  //input
  assign axi_wlast[1*(1)+:1] = 1'b1;  //input
  assign axi_wvalid[1*(1)+:1] = tb_wvalid;  //input
  assign tb_wready = axi_wready[1*(1)+:1];  //output
  //assign              axi_bid[1*(AXI_ID_W)+:AXI_ID_W];  //output
  //assign                            axi_bresp[1*(2)+:2];  //output
  //assign                            axi_bvalid[1*(1)+:1];  //output
  assign axi_bready[1*(1)+:1] = 1'b1;  //input
  assign axi_arid[1*(AXI_ID_W)+:AXI_ID_W] = {AXI_ID_W{1'b0}};  //input
  assign axi_araddr[1*(AXI_ADDR_W)+:AXI_ADDR_W] = tb_addr;  //input
  assign axi_arlen[1*(AXI_LEN_W)+:AXI_LEN_W] = {AXI_LEN_W{1'b0}};  //input
  assign axi_arsize[1*(3)+:3] = 3'b0;  //input
  assign axi_arburst[1*(2)+:2] = 2'b0;  //input
  assign axi_arlock[1*(2)+:2] = 2'b0;  //input
  assign axi_arcache[1*(4)+:4] = 4'b0;  //input
  assign axi_arprot[1*(3)+:3] = 3'b0;  //input
  assign axi_arqos[1*(4)+:4] = 4'b0;  //input
  assign axi_arvalid[1*(1)+:1] = tb_arvalid;  //input
  assign tb_arready = axi_arready[1*(1)+:1];  //output
  assign axi_rid[1*(AXI_ID_W)+:AXI_ID_W] = {AXI_ID_W{1'b0}};  //input
  assign tb_rdata = axi_rdata[1*(AXI_DATA_W)+:AXI_DATA_W];  //output
  //assign                            axi_rresp[1*(2)+:2];  //output
  //assign                            axi_rlast[1*(1)+:1];  //output
  assign tb_rvalid = axi_rvalid[1*(1)+:1];  //output
  assign axi_rready[1*(1)+:1] = tb_rready;  //input

endmodule
