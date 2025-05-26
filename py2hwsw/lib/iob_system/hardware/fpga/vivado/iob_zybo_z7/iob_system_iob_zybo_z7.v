//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2024 Advanced Micro Devices, Inc. All Rights Reserved.
//--------------------------------------------------------------------------------
//Tool Version: Vivado v.2024.2 (lin64) Build 5239630 Fri Nov 08 22:34:34 MST 2024
//Date        : Mon May 19 22:40:48 2025
//Host        : pastel-de-nata running 64-bit Ubuntu 22.04.5 LTS
//Command     : generate_target design_1_wrapper.bd
//Design      : design_1_wrapper
//Purpose     : IP block netlist
//--------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

module iob_system_iob_zybo_z7 #(
    parameter AXI_ID_W = 4,  // AXI ID width
    parameter AXI_LEN_W = 8, // AXI length width
    parameter AXI_ADDR_W = 32, // AXI address width
    parameter AXI_DATA_W = 32  // AXI data width
                                )
   // IOb-SoC instance for Zybo Z7
   // This module instantiates the processing system and the IOb-SoC wrapper

   (DDR_addr,
    DDR_ba,
    DDR_cas_n,
    DDR_ck_n,
    DDR_ck_p,
    DDR_cke,
    DDR_cs_n,
    DDR_dm,
    DDR_dq,
    DDR_dqs_n,
    DDR_dqs_p,
    DDR_odt,
    DDR_ras_n,
    DDR_reset_n,
    DDR_we_n,
    FIXED_IO_ddr_vrn,
    FIXED_IO_ddr_vrp,
    FIXED_IO_mio,
    FIXED_IO_ps_clk,
    FIXED_IO_ps_porb,
    FIXED_IO_ps_srstb);
  inout [14:0]DDR_addr;
  inout [2:0]DDR_ba;
  inout DDR_cas_n;
  inout DDR_ck_n;
  inout DDR_ck_p;
  inout DDR_cke;
  inout DDR_cs_n;
  inout [3:0]DDR_dm;
  inout [31:0]DDR_dq;
  inout [3:0]DDR_dqs_n;
  inout [3:0]DDR_dqs_p;
  inout DDR_odt;
  inout DDR_ras_n;
  inout DDR_reset_n;
  inout DDR_we_n;
  inout FIXED_IO_ddr_vrn;
  inout FIXED_IO_ddr_vrp;
  inout [53:0]FIXED_IO_mio;
  inout FIXED_IO_ps_clk;
  inout FIXED_IO_ps_porb;
  inout FIXED_IO_ps_srstb;

  wire [14:0]DDR_addr;
  wire [2:0]DDR_ba;
  wire DDR_cas_n;
  wire DDR_ck_n;
  wire DDR_ck_p;
  wire DDR_cke;
  wire DDR_cs_n;
  wire [3:0]DDR_dm;
  wire [31:0]DDR_dq;
  wire [3:0]DDR_dqs_n;
  wire [3:0]DDR_dqs_p;
  wire DDR_odt;
  wire DDR_ras_n;
  wire DDR_reset_n;
  wire DDR_we_n;
  wire FIXED_IO_ddr_vrn;
  wire FIXED_IO_ddr_vrp;
  wire [53:0]FIXED_IO_mio;
  wire FIXED_IO_ps_clk;
  wire FIXED_IO_ps_porb;
  wire FIXED_IO_ps_srstb;

   wire clk;
   wire arst_n;
   wire cke= 1'b1;

   wire rxd;
   wire txd;
   
   processing_system7_0 processing_system7_0
     (
      .PS_CLK(FIXED_IO_ps_clk_io),
      .PS_PORB(FIXED_IO_ps_porb_io),
      .PS_SRSTB(FIXED_IO_ps_srstb_io),
                
      .FCLK_CLK0(clk),
      .FCLK_RESET0_N(arst_n),
      
      .UART1_RX(txd),
      .UART1_TX(rxd),

      .DDR_Addr(DDR_addr),
      .DDR_BankAddr(DDR_ba),
      .DDR_CAS_n(DDR_cas_n),
      .DDR_CKE(DDR_cke),
      .DDR_CS_n(DDR_cs_n),
      .DDR_Clk(DDR_ck_p),
      .DDR_Clk_n(DDR_ck_n),
      .DDR_DM(DDR_dm),
      .DDR_DQ(DDR_dq),
      .DDR_DQS(DDR_dqs_p),
      .DDR_DQS_n(DDR_dqs_n),
      .DDR_DRSTB(DDR_reset_n),
      .DDR_ODT(DDR_odt),
      .DDR_RAS_n(DDR_ras_n),
      .DDR_VRN(FIXED_IO_ddr_vrn),
      .DDR_VRP(FIXED_IO_ddr_vrp),
      .DDR_WEB(DDR_we_n)
      );

   // IOb-SoC instance
   iob_system_mwrap #(
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
        .rs232_rxd_i(rxd),
        .rs232_txd_o(txd),
        .rs232_rts_o(),
        .rs232_cts_i()
        );
        
endmodule
