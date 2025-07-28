`timescale 1ns / 1ps
`include "bsp.vh"
`include "iob_soc_opencryptolinux_conf.vh"

module iob_soc_opencryptolinux_fpga_wrapper (
   //user clock
   input clk,
   input resetn,

   //uart
   output txd_o,
   input  rxd_i,

`ifdef IOB_SOC_OPENCRYPTOLINUX_USE_EXTMEM
   output [13:0] ddr3b_a,       //SSTL15  //Address
   output [ 2:0] ddr3b_ba,      //SSTL15  //Bank Address
   output        ddr3b_rasn,    //SSTL15  //Row Address Strobe
   output        ddr3b_casn,    //SSTL15  //Column Address Strobe
   output        ddr3b_wen,     //SSTL15  //Write Enable
   output [ 1:0] ddr3b_dm,      //SSTL15  //Data Write Mask
   inout  [15:0] ddr3b_dq,      //SSTL15  //Data Bus
   output        ddr3b_clk_n,   //SSTL15  //Diff Clock - Neg
   output        ddr3b_clk_p,   //SSTL15  //Diff Clock - Pos
   output        ddr3b_cke,     //SSTL15  //Clock Enable
   output        ddr3b_csn,     //SSTL15  //Chip Select
   inout  [ 1:0] ddr3b_dqs_n,   //SSTL15  //Diff Data Strobe - Neg
   inout  [ 1:0] ddr3b_dqs_p,   //SSTL15  //Diff Data Strobe - Pos
   output        ddr3b_odt,     //SSTL15  //On-Die Termination Enable
   output        ddr3b_resetn,  //SSTL15  //Reset
   input         rzqin,
`endif

`ifdef IOB_SOC_OPENCRYPTOLINUX_USE_ETHERNET
   output ENET_RESETN,
   input  ENET_RX_CLK,
   output ENET_GTX_CLK,
   input  ENET_RX_D0,
   input  ENET_RX_D1,
   input  ENET_RX_D2,
   input  ENET_RX_D3,
   input  ENET_RX_DV,
   //input  ENET_RX_ERR,
   output ENET_TX_D0,
   output ENET_TX_D1,
   output ENET_TX_D2,
   output ENET_TX_D3,
   output ENET_TX_EN,
   //output ENET_TX_ERR,
`endif
   output trap
);

   //axi4 parameters
   localparam AXI_ID_W = 1;
   localparam AXI_LEN_W = 4;
   localparam AXI_ADDR_W = `DDR_ADDR_W;
   localparam AXI_DATA_W = `DDR_DATA_W;

   wire         uart_txd_o;
   wire         uart_rxd_i;
   wire         uart_cts_i;
   wire         uart_rts_o;
   wire         ETH0_MTxClk;
   wire [4-1:0] ETH0_MTxD;
   wire         ETH0_MTxEn;
   wire         ETH0_MTxErr;
   wire         ETH0_MRxClk;
   wire         ETH0_MRxDv;
   wire [4-1:0] ETH0_MRxD;
   wire         ETH0_MRxErr;
   wire         ETH0_MColl;
   wire         ETH0_MCrS;
   wire         ETH0_MDC;
   wire         ETH0_MDIO;
   wire         ETH0_phy_rstn_o;
   wire         spi_SS;
   wire         spi_SCLK;
   wire         spi_MISO;
   wire         spi_MOSI;
   wire         spi_WP_N;
   wire         spi_HOLD_N;

   //DDR AXI interface signals
`ifdef IOB_SOC_OPENCRYPTOLINUX_USE_EXTMEM
   // Wires for the system and its peripherals
   wire [3*AXI_ID_W-1:0] axi_awid;  //Address write channel ID.
   wire [3*AXI_ADDR_W-1:0] axi_awaddr;  //Address write channel address.
   wire [3*AXI_LEN_W-1:0] axi_awlen;  //Address write channel burst length.
   wire [3*3-1:0] axi_awsize; //Address write channel burst size. This signal indicates the size of each transfer in the burst.
   wire [3*2-1:0] axi_awburst;  //Address write channel burst type.
   wire [3*2-1:0] axi_awlock;  //Address write channel lock type.
   wire [3*4-1:0] axi_awcache; //Address write channel memory type. Set to 0000 if master output; ignored if slave input.
   wire [3*3-1:0] axi_awprot; //Address write channel protection type. Set to 000 if master output; ignored if slave input.
   wire [3*4-1:0] axi_awqos;  //Address write channel quality of service.
   wire [3*1-1:0] axi_awvalid;  //Address write channel valid.
   wire [3*1-1:0] axi_awready;  //Address write channel ready.
   wire [3*AXI_DATA_W-1:0] axi_wdata;  //Write channel data.
   wire [3*(AXI_DATA_W/8)-1:0] axi_wstrb;  //Write channel write strobe.
   wire [3*1-1:0] axi_wlast;  //Write channel last word flag.
   wire [3*1-1:0] axi_wvalid;  //Write channel valid.
   wire [3*1-1:0] axi_wready;  //Write channel ready.
   wire [3*AXI_ID_W-1:0] axi_bid;  //Write response channel ID.
   wire [3*2-1:0] axi_bresp;  //Write response channel response.
   wire [3*1-1:0] axi_bvalid;  //Write response channel valid.
   wire [3*1-1:0] axi_bready;  //Write response channel ready.
   wire [3*AXI_ID_W-1:0] axi_arid;  //Address read channel ID.
   wire [3*AXI_ADDR_W-1:0] axi_araddr;  //Address read channel address.
   wire [3*AXI_LEN_W-1:0] axi_arlen;  //Address read channel burst length.
   wire [3*3-1:0] axi_arsize; //Address read channel burst size. This signal indicates the size of each transfer in the burst.
   wire [3*2-1:0] axi_arburst;  //Address read channel burst type.
   wire [3*2-1:0] axi_arlock;  //Address read channel lock type.
   wire [3*4-1:0] axi_arcache; //Address read channel memory type. Set to 0000 if master output; ignored if slave input.
   wire [3*3-1:0] axi_arprot; //Address read channel protection type. Set to 000 if master output; ignored if slave input.
   wire [3*4-1:0] axi_arqos;  //Address read channel quality of service.
   wire [3*1-1:0] axi_arvalid;  //Address read channel valid.
   wire [3*1-1:0] axi_arready;  //Address read channel ready.
   wire [3*AXI_ID_W-1:0] axi_rid;  //Read channel ID.
   wire [3*AXI_DATA_W-1:0] axi_rdata;  //Read channel data.
   wire [3*2-1:0] axi_rresp;  //Read channel response.
   wire [3*1-1:0] axi_rlast;  //Read channel last word.
   wire [3*1-1:0] axi_rvalid;  //Read channel valid.
   wire [3*1-1:0] axi_rready;  //Read channel ready.
   // Wires to connect the interconnect with the memory
   wire [AXI_ID_W-1:0] memory_axi_awid;  //Address write channel ID.
   wire [AXI_ADDR_W-1:0] memory_axi_awaddr;  //Address write channel address.
   wire [AXI_LEN_W-1:0] memory_axi_awlen;  //Address write channel burst length.
   wire [3-1:0] memory_axi_awsize; //Address write channel burst size. This signal indicates the size of each transfer in the burst.
   wire [2-1:0] memory_axi_awburst;  //Address write channel burst type.
   wire [2-1:0] memory_axi_awlock;  //Address write channel lock type.
   wire [4-1:0] memory_axi_awcache; //Address write channel memory type. Set to 0000 if master output; ignored if slave input.
   wire [3-1:0] memory_axi_awprot; //Address write channel protection type. Set to 000 if master output; ignored if slave input.
   wire [4-1:0] memory_axi_awqos;  //Address write channel quality of service.
   wire [1-1:0] memory_axi_awvalid;  //Address write channel valid.
   wire [1-1:0] memory_axi_awready;  //Address write channel ready.
   wire [AXI_DATA_W-1:0] memory_axi_wdata;  //Write channel data.
   wire [(AXI_DATA_W/8)-1:0] memory_axi_wstrb;  //Write channel write strobe.
   wire [1-1:0] memory_axi_wlast;  //Write channel last word flag.
   wire [1-1:0] memory_axi_wvalid;  //Write channel valid.
   wire [1-1:0] memory_axi_wready;  //Write channel ready.
   wire [AXI_ID_W-1:0] memory_axi_bid;  //Write response channel ID.
   wire [2-1:0] memory_axi_bresp;  //Write response channel response.
   wire [1-1:0] memory_axi_bvalid;  //Write response channel valid.
   wire [1-1:0] memory_axi_bready;  //Write response channel ready.
   wire [AXI_ID_W-1:0] memory_axi_arid;  //Address read channel ID.
   wire [AXI_ADDR_W-1:0] memory_axi_araddr;  //Address read channel address.
   wire [AXI_LEN_W-1:0] memory_axi_arlen;  //Address read channel burst length.
   wire [3-1:0] memory_axi_arsize; //Address read channel burst size. This signal indicates the size of each transfer in the burst.
   wire [2-1:0] memory_axi_arburst;  //Address read channel burst type.
   wire [2-1:0] memory_axi_arlock;  //Address read channel lock type.
   wire [4-1:0] memory_axi_arcache; //Address read channel memory type. Set to 0000 if master output; ignored if slave input.
   wire [3-1:0] memory_axi_arprot; //Address read channel protection type. Set to 000 if master output; ignored if slave input.
   wire [4-1:0] memory_axi_arqos;  //Address read channel quality of service.
   wire [1-1:0] memory_axi_arvalid;  //Address read channel valid.
   wire [1-1:0] memory_axi_arready;  //Address read channel ready.
   wire [AXI_ID_W-1:0] memory_axi_rid;  //Read channel ID.
   wire [AXI_DATA_W-1:0] memory_axi_rdata;  //Read channel data.
   wire [2-1:0] memory_axi_rresp;  //Read channel response.
   wire [1-1:0] memory_axi_rlast;  //Read channel last word.
   wire [1-1:0] memory_axi_rvalid;  //Read channel valid.
   wire [1-1:0] memory_axi_rready;  //Read channel ready.
`endif

   //-----------------------------------------------------------------
   // Clocking / Reset
   //-----------------------------------------------------------------

   wire arst;

   // 
   // Logic to contatenate data pins and ethernet clock
   //
`ifdef IOB_SOC_OPENCRYPTOLINUX_USE_ETHERNET
   //buffered eth clock
   wire ETH_Clk;

   //eth clock
   clk_buf_altclkctrl_0 txclk_buf (
      .inclk (ENET_RX_CLK),
      .outclk(ETH_Clk)
   );


   ddio_out_clkbuf ddio_out_clkbuf_inst (
      .aclr    (~ENET_RESETN),
      .datain_h(1'b0),
      .datain_l(1'b1),
      .outclock(ETH_Clk),
      .dataout (ENET_GTX_CLK)
   );

   //MII
   assign ETH0_MRxClk = ETH_Clk;
   assign ETH0_MRxD = {ENET_RX_D3, ENET_RX_D2, ENET_RX_D1, ENET_RX_D0};
   assign ETH0_MRxDv = ENET_RX_DV;
   //assign ETH0_MRxErr = ENET_RX_ERR;
   assign ETH0_MRxErr = 1'b0;

   assign ETH0_MTxClk = ETH_Clk;
   assign {ENET_TX_D3, ENET_TX_D2, ENET_TX_D1, ENET_TX_D0} = ETH0_MTxD;
   assign ENET_TX_EN = ETH0_MTxEn;
   //assign ENET_TX_ERR = ETH0_MTxErr;

   assign ENET_RESETN = ETH0_phy_rstn_o;

   assign ETH0_MColl = 1'b0;
   assign ETH0_MCrS = 1'b0;
`endif

   //
   // IOb-SoC (may include UUT)
   //
   iob_soc_opencryptolinux #(
      .AXI_ID_W  (AXI_ID_W),
      .AXI_LEN_W (AXI_LEN_W),
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_DATA_W(AXI_DATA_W)
   ) iob_soc_opencryptolinux (
      .uart_txd_o     (uart_txd_o),
      .uart_rxd_i     (uart_rxd_i),
      .uart_cts_i     (uart_cts_i),
      .uart_rts_o     (uart_rts_o),
      .ETH0_MTxClk    (ETH0_MTxClk),
      .ETH0_MTxD      (ETH0_MTxD),
      .ETH0_MTxEn     (ETH0_MTxEn),
      .ETH0_MTxErr    (ETH0_MTxErr),
      .ETH0_MRxClk    (ETH0_MRxClk),
      .ETH0_MRxDv     (ETH0_MRxDv),
      .ETH0_MRxD      (ETH0_MRxD),
      .ETH0_MRxErr    (ETH0_MRxErr),
      .ETH0_MColl     (ETH0_MColl),
      .ETH0_MCrS      (ETH0_MCrS),
      .ETH0_MDC       (ETH0_MDC),
      .ETH0_MDIO      (ETH0_MDIO),
      .ETH0_phy_rstn_o(ETH0_phy_rstn_o),
      .spi_SS         (spi_SS),
      .spi_SCLK       (spi_SCLK),
      .spi_MISO       (spi_MISO),
      .spi_MOSI       (spi_MOSI),
      .spi_WP_N       (spi_WP_N),
      .spi_HOLD_N     (spi_HOLD_N),

`ifdef IOB_SOC_OPENCRYPTOLINUX_USE_EXTMEM
      .axi_awid_o(axi_awid[0+:3*AXI_ID_W]),  //Address write channel ID.
      .axi_awaddr_o(axi_awaddr[0+:3*AXI_ADDR_W]),  //Address write channel address.
      .axi_awlen_o(axi_awlen[0+:3*AXI_LEN_W]),  //Address write channel burst length.
      .axi_awsize_o(axi_awsize[0+:3*3]), //Address write channel burst size. This signal indicates the size of each transfer in the burst.
      .axi_awburst_o(axi_awburst[0+:3*2]),  //Address write channel burst type.
      .axi_awlock_o(axi_awlock[0+:3*2]),  //Address write channel lock type.
      .axi_awcache_o(axi_awcache[0+:3*4]), //Address write channel memory type. Set to 0000 if master output; ignored if slave input.
      .axi_awprot_o(axi_awprot[0+:3*3]), //Address write channel protection type. Set to 000 if master output; ignored if slave input.
      .axi_awqos_o(axi_awqos[0+:3*4]),  //Address write channel quality of service.
      .axi_awvalid_o(axi_awvalid[0+:3*1]),  //Address write channel valid.
      .axi_awready_i(axi_awready[0+:3*1]),  //Address write channel ready.
      .axi_wdata_o(axi_wdata[0+:3*AXI_DATA_W]),  //Write channel data.
      .axi_wstrb_o(axi_wstrb[0+:3*(AXI_DATA_W/8)]),  //Write channel write strobe.
      .axi_wlast_o(axi_wlast[0+:3*1]),  //Write channel last word flag.
      .axi_wvalid_o(axi_wvalid[0+:3*1]),  //Write channel valid.
      .axi_wready_i(axi_wready[0+:3*1]),  //Write channel ready.
      .axi_bid_i(axi_bid[0+:3*AXI_ID_W]),  //Write response channel ID.
      .axi_bresp_i(axi_bresp[0+:3*2]),  //Write response channel response.
      .axi_bvalid_i(axi_bvalid[0+:3*1]),  //Write response channel valid.
      .axi_bready_o(axi_bready[0+:3*1]),  //Write response channel ready.
      .axi_arid_o(axi_arid[0+:3*AXI_ID_W]),  //Address read channel ID.
      .axi_araddr_o(axi_araddr[0+:3*AXI_ADDR_W]),  //Address read channel address.
      .axi_arlen_o(axi_arlen[0+:3*AXI_LEN_W]),  //Address read channel burst length.
      .axi_arsize_o(axi_arsize[0+:3*3]), //Address read channel burst size. This signal indicates the size of each transfer in the burst.
      .axi_arburst_o(axi_arburst[0+:3*2]),  //Address read channel burst type.
      .axi_arlock_o(axi_arlock[0+:3*2]),  //Address read channel lock type.
      .axi_arcache_o(axi_arcache[0+:3*4]), //Address read channel memory type. Set to 0000 if master output; ignored if slave input.
      .axi_arprot_o(axi_arprot[0+:3*3]), //Address read channel protection type. Set to 000 if master output; ignored if slave input.
      .axi_arqos_o(axi_arqos[0+:3*4]),  //Address read channel quality of service.
      .axi_arvalid_o(axi_arvalid[0+:3*1]),  //Address read channel valid.
      .axi_arready_i(axi_arready[0+:3*1]),  //Address read channel ready.
      .axi_rid_i(axi_rid[0+:3*AXI_ID_W]),  //Read channel ID.
      .axi_rdata_i(axi_rdata[0+:3*AXI_DATA_W]),  //Read channel data.
      .axi_rresp_i(axi_rresp[0+:3*2]),  //Read channel response.
      .axi_rlast_i(axi_rlast[0+:3*1]),  //Read channel last word.
      .axi_rvalid_i(axi_rvalid[0+:3*1]),  //Read channel valid.
      .axi_rready_o(axi_rready[0+:3*1]),  //Read channel ready.

`endif
      .clk_i (clk),
      .cke_i (1'b1),
      .arst_i(arst),
      .trap_o(trap)
   );

   //
   // UART
   //
   assign txd_o      = uart_txd_o;
   assign uart_rxd_i = rxd_i;
   assign uart_cts_i = 1'b1;
   // uart_rts_i unconnected


`ifdef IOB_SOC_OPENCRYPTOLINUX_USE_EXTMEM
   //user reset
   wire                                           locked;
   wire                                           init_done;

   //determine system reset
   wire rst_int = ~resetn | ~locked | ~init_done;
   //   wire          rst_int = ~resetn | ~locked;

   iob_reset_sync rst_sync (
      .clk_i (clk),
      .arst_i(rst_int),
      .arst_o(arst)
   );

   alt_ddr3 ddr3_ctrl (
      .clk_clk      (clk),
      .reset_reset_n(resetn),
      .oct_rzqin    (rzqin),

      .memory_mem_a      (ddr3b_a),
      .memory_mem_ba     (ddr3b_ba),
      .memory_mem_ck     (ddr3b_clk_p),
      .memory_mem_ck_n   (ddr3b_clk_n),
      .memory_mem_cke    (ddr3b_cke),
      .memory_mem_cs_n   (ddr3b_csn),
      .memory_mem_dm     (ddr3b_dm),
      .memory_mem_ras_n  (ddr3b_rasn),
      .memory_mem_cas_n  (ddr3b_casn),
      .memory_mem_we_n   (ddr3b_wen),
      .memory_mem_reset_n(ddr3b_resetn),
      .memory_mem_dq     (ddr3b_dq),
      .memory_mem_dqs    (ddr3b_dqs_p),
      .memory_mem_dqs_n  (ddr3b_dqs_n),
      .memory_mem_odt    (ddr3b_odt),


      //
      // External memory connection 0
      //

      //Write address
      .axi_bridge_0_s0_awid   (axi_awid[0*AXI_ID_W+:1]),
      .axi_bridge_0_s0_awaddr (axi_awaddr[0*AXI_ADDR_W+:AXI_ADDR_W]),
      .axi_bridge_0_s0_awlen  (axi_awlen[0*AXI_LEN_W+:AXI_LEN_W]),
      .axi_bridge_0_s0_awsize (axi_awsize[0*3+:3]),
      .axi_bridge_0_s0_awburst(axi_awburst[0*2+:2]),
      .axi_bridge_0_s0_awlock (axi_awlock[0*2+:1]),
      .axi_bridge_0_s0_awcache(axi_awcache[0*4+:4]),
      .axi_bridge_0_s0_awprot (axi_awprot[0*3+:3]),
      .axi_bridge_0_s0_awvalid(axi_awvalid[0*1+:1]),
      .axi_bridge_0_s0_awready(axi_awready[0*1+:1]),

      //Write data
      .axi_bridge_0_s0_wdata (axi_wdata[0*AXI_DATA_W+:AXI_DATA_W]),
      .axi_bridge_0_s0_wstrb (axi_wstrb[0*(AXI_DATA_W/8)+:(AXI_DATA_W/8)]),
      .axi_bridge_0_s0_wlast (axi_wlast[0*1+:1]),
      .axi_bridge_0_s0_wvalid(axi_wvalid[0*1+:1]),
      .axi_bridge_0_s0_wready(axi_wready[0*1+:1]),

      //Write response
      .axi_bridge_0_s0_bid   (axi_bid[0*AXI_ID_W+:1]),
      .axi_bridge_0_s0_bresp (axi_bresp[0*2+:2]),
      .axi_bridge_0_s0_bvalid(axi_bvalid[0*1+:1]),
      .axi_bridge_0_s0_bready(axi_bready[0*1+:1]),

      //Read address
      .axi_bridge_0_s0_arid   (axi_arid[0*AXI_ID_W+:1]),
      .axi_bridge_0_s0_araddr (axi_araddr[0*AXI_ADDR_W+:AXI_ADDR_W]),
      .axi_bridge_0_s0_arlen  (axi_arlen[0*AXI_LEN_W+:AXI_LEN_W]),
      .axi_bridge_0_s0_arsize (axi_arsize[0*3+:3]),
      .axi_bridge_0_s0_arburst(axi_arburst[0*2+:2]),
      .axi_bridge_0_s0_arlock (axi_arlock[0*2+:1]),
      .axi_bridge_0_s0_arcache(axi_arcache[0*4+:4]),
      .axi_bridge_0_s0_arprot (axi_arprot[0*3+:3]),
      .axi_bridge_0_s0_arvalid(axi_arvalid[0*1+:1]),
      .axi_bridge_0_s0_arready(axi_arready[0*1+:1]),

      //Read data
      .axi_bridge_0_s0_rid   (axi_rid[0*AXI_ID_W+:1]),
      .axi_bridge_0_s0_rdata (axi_rdata[0*AXI_DATA_W+:AXI_DATA_W]),
      .axi_bridge_0_s0_rresp (axi_rresp[0*2+:2]),
      .axi_bridge_0_s0_rlast (axi_rlast[0*1+:1]),
      .axi_bridge_0_s0_rvalid(axi_rvalid[0*1+:1]),
      .axi_bridge_0_s0_rready(axi_rready[0*1+:1]),


      //
      // External memory connection 1
      //

      //Write address
      .axi_bridge_1_s0_awid   (axi_awid[1*AXI_ID_W+:1]),
      .axi_bridge_1_s0_awaddr (axi_awaddr[1*AXI_ADDR_W+:AXI_ADDR_W]),
      .axi_bridge_1_s0_awlen  (axi_awlen[1*AXI_LEN_W+:AXI_LEN_W]),
      .axi_bridge_1_s0_awsize (axi_awsize[1*3+:3]),
      .axi_bridge_1_s0_awburst(axi_awburst[1*2+:2]),
      .axi_bridge_1_s0_awlock (axi_awlock[1*2+:1]),
      .axi_bridge_1_s0_awcache(axi_awcache[1*4+:4]),
      .axi_bridge_1_s0_awprot (axi_awprot[1*3+:3]),
      .axi_bridge_1_s0_awvalid(axi_awvalid[1*1+:1]),
      .axi_bridge_1_s0_awready(axi_awready[1*1+:1]),

      //Write data
      .axi_bridge_1_s0_wdata (axi_wdata[1*AXI_DATA_W+:AXI_DATA_W]),
      .axi_bridge_1_s0_wstrb (axi_wstrb[1*(AXI_DATA_W/8)+:(AXI_DATA_W/8)]),
      .axi_bridge_1_s0_wlast (axi_wlast[1*1+:1]),
      .axi_bridge_1_s0_wvalid(axi_wvalid[1*1+:1]),
      .axi_bridge_1_s0_wready(axi_wready[1*1+:1]),

      //Write response
      .axi_bridge_1_s0_bid   (axi_bid[1*AXI_ID_W+:1]),
      .axi_bridge_1_s0_bresp (axi_bresp[1*2+:2]),
      .axi_bridge_1_s0_bvalid(axi_bvalid[1*1+:1]),
      .axi_bridge_1_s0_bready(axi_bready[1*1+:1]),

      //Read address
      .axi_bridge_1_s0_arid   (axi_arid[1*AXI_ID_W+:1]),
      .axi_bridge_1_s0_araddr (axi_araddr[1*AXI_ADDR_W+:AXI_ADDR_W]),
      .axi_bridge_1_s0_arlen  (axi_arlen[1*AXI_LEN_W+:AXI_LEN_W]),
      .axi_bridge_1_s0_arsize (axi_arsize[1*3+:3]),
      .axi_bridge_1_s0_arburst(axi_arburst[1*2+:2]),
      .axi_bridge_1_s0_arlock (axi_arlock[1*2+:1]),
      .axi_bridge_1_s0_arcache(axi_arcache[1*4+:4]),
      .axi_bridge_1_s0_arprot (axi_arprot[1*3+:3]),
      .axi_bridge_1_s0_arvalid(axi_arvalid[1*1+:1]),
      .axi_bridge_1_s0_arready(axi_arready[1*1+:1]),

      //Read data
      .axi_bridge_1_s0_rid   (axi_rid[1*AXI_ID_W+:1]),
      .axi_bridge_1_s0_rdata (axi_rdata[1*AXI_DATA_W+:AXI_DATA_W]),
      .axi_bridge_1_s0_rresp (axi_rresp[1*2+:2]),
      .axi_bridge_1_s0_rlast (axi_rlast[1*1+:1]),
      .axi_bridge_1_s0_rvalid(axi_rvalid[1*1+:1]),
      .axi_bridge_1_s0_rready(axi_rready[1*1+:1]),


      //
      // External memory connection 2
      //

      //Write address
      .axi_bridge_2_s0_awid   (axi_awid[2*AXI_ID_W+:1]),
      .axi_bridge_2_s0_awaddr (axi_awaddr[2*AXI_ADDR_W+:AXI_ADDR_W]),
      .axi_bridge_2_s0_awlen  (axi_awlen[2*AXI_LEN_W+:AXI_LEN_W]),
      .axi_bridge_2_s0_awsize (axi_awsize[2*3+:3]),
      .axi_bridge_2_s0_awburst(axi_awburst[2*2+:2]),
      .axi_bridge_2_s0_awlock (axi_awlock[2*2+:1]),
      .axi_bridge_2_s0_awcache(axi_awcache[2*4+:4]),
      .axi_bridge_2_s0_awprot (axi_awprot[2*3+:3]),
      .axi_bridge_2_s0_awvalid(axi_awvalid[2*1+:1]),
      .axi_bridge_2_s0_awready(axi_awready[2*1+:1]),

      //Write data
      .axi_bridge_2_s0_wdata (axi_wdata[2*AXI_DATA_W+:AXI_DATA_W]),
      .axi_bridge_2_s0_wstrb (axi_wstrb[2*(AXI_DATA_W/8)+:(AXI_DATA_W/8)]),
      .axi_bridge_2_s0_wlast (axi_wlast[2*1+:1]),
      .axi_bridge_2_s0_wvalid(axi_wvalid[2*1+:1]),
      .axi_bridge_2_s0_wready(axi_wready[2*1+:1]),

      //Write response
      .axi_bridge_2_s0_bid   (axi_bid[2*AXI_ID_W+:1]),
      .axi_bridge_2_s0_bresp (axi_bresp[2*2+:2]),
      .axi_bridge_2_s0_bvalid(axi_bvalid[2*1+:1]),
      .axi_bridge_2_s0_bready(axi_bready[2*1+:1]),

      //Read address
      .axi_bridge_2_s0_arid   (axi_arid[2*AXI_ID_W+:1]),
      .axi_bridge_2_s0_araddr (axi_araddr[2*AXI_ADDR_W+:AXI_ADDR_W]),
      .axi_bridge_2_s0_arlen  (axi_arlen[2*AXI_LEN_W+:AXI_LEN_W]),
      .axi_bridge_2_s0_arsize (axi_arsize[2*3+:3]),
      .axi_bridge_2_s0_arburst(axi_arburst[2*2+:2]),
      .axi_bridge_2_s0_arlock (axi_arlock[2*2+:1]),
      .axi_bridge_2_s0_arcache(axi_arcache[2*4+:4]),
      .axi_bridge_2_s0_arprot (axi_arprot[2*3+:3]),
      .axi_bridge_2_s0_arvalid(axi_arvalid[2*1+:1]),
      .axi_bridge_2_s0_arready(axi_arready[2*1+:1]),

      //Read data
      .axi_bridge_2_s0_rid   (axi_rid[2*AXI_ID_W+:1]),
      .axi_bridge_2_s0_rdata (axi_rdata[2*AXI_DATA_W+:AXI_DATA_W]),
      .axi_bridge_2_s0_rresp (axi_rresp[2*2+:2]),
      .axi_bridge_2_s0_rlast (axi_rlast[2*1+:1]),
      .axi_bridge_2_s0_rvalid(axi_rvalid[2*1+:1]),
      .axi_bridge_2_s0_rready(axi_rready[2*1+:1]),


      .mem_if_ddr3_emif_0_pll_sharing_pll_mem_clk              (),
      .mem_if_ddr3_emif_0_pll_sharing_pll_write_clk            (),
      .mem_if_ddr3_emif_0_pll_sharing_pll_locked               (locked),
      .mem_if_ddr3_emif_0_pll_sharing_pll_write_clk_pre_phy_clk(),
      .mem_if_ddr3_emif_0_pll_sharing_pll_addr_cmd_clk         (),
      .mem_if_ddr3_emif_0_pll_sharing_pll_avl_clk              (),
      .mem_if_ddr3_emif_0_pll_sharing_pll_config_clk           (),
      .mem_if_ddr3_emif_0_pll_sharing_pll_mem_phy_clk          (),
      .mem_if_ddr3_emif_0_pll_sharing_afi_phy_clk              (),
      .mem_if_ddr3_emif_0_pll_sharing_pll_avl_phy_clk          (),
      .mem_if_ddr3_emif_0_status_local_init_done               (init_done),
      .mem_if_ddr3_emif_0_status_local_cal_success             (),
      .mem_if_ddr3_emif_0_status_local_cal_fail                ()
   );

`else
   iob_reset_sync rst_sync (
      .clk_i (clk),
      .arst_i(~resetn),
      .arst_o(arst)
   );
`endif

endmodule
