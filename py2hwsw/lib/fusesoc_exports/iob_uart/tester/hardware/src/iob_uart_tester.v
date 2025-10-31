// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_conf.vh"

module iob_uart_tester #(
    parameter AXI_ID_W = `IOB_UART_TESTER_AXI_ID_W,  // Don't change this parameter value!
    parameter AXI_ADDR_W = `IOB_UART_TESTER_AXI_ADDR_W,  // Don't change this parameter value!
    parameter AXI_DATA_W = `IOB_UART_TESTER_AXI_DATA_W,  // Don't change this parameter value!
    parameter AXI_LEN_W = `IOB_UART_TESTER_AXI_LEN_W,  // Don't change this parameter value!
    parameter BOOTROM_MEM_HEXFILE = `IOB_UART_TESTER_BOOTROM_MEM_HEXFILE,  // Don't change this parameter value!
    parameter INT_MEM_HEXFILE = `IOB_UART_TESTER_INT_MEM_HEXFILE  // Don't change this parameter value!
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // rom_bus_m: Ports for connection with boot ROM memory
    output bootrom_mem_clk_o,
    output [10-1:0] bootrom_mem_addr_o,
    output bootrom_mem_en_o,
    input [32-1:0] bootrom_mem_r_data_i,
    // int_mem_bus_m: Port for connection to 'iob_ram_t2p_be' memory
    output int_mem_clk_o,
    output int_mem_r_en_o,
    output [16-1:0] int_mem_r_addr_o,
    input [32-1:0] int_mem_r_data_i,
    output [32/8-1:0] int_mem_w_strb_o,
    output [16-1:0] int_mem_w_addr_o,
    output [32-1:0] int_mem_w_data_o,
    // rs232_m: iob-system uart interface
    input rs232_rxd_i,
    output rs232_txd_o,
    output rs232_rts_o,
    input rs232_cts_i
);

// System interrupts
    wire [32-1:0] interrupts;
// CPU instruction bus
    wire [32-1:0] cpu_i_axi_araddr;
    wire cpu_i_axi_arvalid;
    wire cpu_i_axi_arready;
    wire [32-1:0] cpu_i_axi_rdata;
    wire [2-1:0] cpu_i_axi_rresp;
    wire cpu_i_axi_rvalid;
    wire cpu_i_axi_rready;
    wire [AXI_ID_W-1:0] cpu_i_axi_arid;
    wire [AXI_LEN_W-1:0] cpu_i_axi_arlen;
    wire [3-1:0] cpu_i_axi_arsize;
    wire [2-1:0] cpu_i_axi_arburst;
    wire cpu_i_axi_arlock;
    wire [4-1:0] cpu_i_axi_arcache;
    wire [4-1:0] cpu_i_axi_arqos;
    wire [AXI_ID_W-1:0] cpu_i_axi_rid;
    wire cpu_i_axi_rlast;
    wire [32-1:0] cpu_i_axi_awaddr;
    wire cpu_i_axi_awvalid;
    wire cpu_i_axi_awready;
    wire [32-1:0] cpu_i_axi_wdata;
    wire [32/8-1:0] cpu_i_axi_wstrb;
    wire cpu_i_axi_wvalid;
    wire cpu_i_axi_wready;
    wire [2-1:0] cpu_i_axi_bresp;
    wire cpu_i_axi_bvalid;
    wire cpu_i_axi_bready;
    wire [AXI_ID_W-1:0] cpu_i_axi_awid;
    wire [AXI_LEN_W-1:0] cpu_i_axi_awlen;
    wire [3-1:0] cpu_i_axi_awsize;
    wire [2-1:0] cpu_i_axi_awburst;
    wire cpu_i_axi_awlock;
    wire [4-1:0] cpu_i_axi_awcache;
    wire [4-1:0] cpu_i_axi_awqos;
    wire cpu_i_axi_wlast;
    wire [AXI_ID_W-1:0] cpu_i_axi_bid;
// CPU data bus
    wire [32-1:0] cpu_d_axi_araddr;
    wire cpu_d_axi_arvalid;
    wire cpu_d_axi_arready;
    wire [32-1:0] cpu_d_axi_rdata;
    wire [2-1:0] cpu_d_axi_rresp;
    wire cpu_d_axi_rvalid;
    wire cpu_d_axi_rready;
    wire [AXI_ID_W-1:0] cpu_d_axi_arid;
    wire [AXI_LEN_W-1:0] cpu_d_axi_arlen;
    wire [3-1:0] cpu_d_axi_arsize;
    wire [2-1:0] cpu_d_axi_arburst;
    wire cpu_d_axi_arlock;
    wire [4-1:0] cpu_d_axi_arcache;
    wire [4-1:0] cpu_d_axi_arqos;
    wire [AXI_ID_W-1:0] cpu_d_axi_rid;
    wire cpu_d_axi_rlast;
    wire [32-1:0] cpu_d_axi_awaddr;
    wire cpu_d_axi_awvalid;
    wire cpu_d_axi_awready;
    wire [32-1:0] cpu_d_axi_wdata;
    wire [32/8-1:0] cpu_d_axi_wstrb;
    wire cpu_d_axi_wvalid;
    wire cpu_d_axi_wready;
    wire [2-1:0] cpu_d_axi_bresp;
    wire cpu_d_axi_bvalid;
    wire cpu_d_axi_bready;
    wire [AXI_ID_W-1:0] cpu_d_axi_awid;
    wire [AXI_LEN_W-1:0] cpu_d_axi_awlen;
    wire [3-1:0] cpu_d_axi_awsize;
    wire [2-1:0] cpu_d_axi_awburst;
    wire cpu_d_axi_awlock;
    wire [4-1:0] cpu_d_axi_awcache;
    wire [4-1:0] cpu_d_axi_awqos;
    wire cpu_d_axi_wlast;
    wire [AXI_ID_W-1:0] cpu_d_axi_bid;
// Wires to connect to unused output bits of interconnect
    wire [14-1:0] unused_m0_araddr_bits;
    wire [14-1:0] unused_m0_awaddr_bits;
    wire [32 - AXI_ADDR_W-1:0] unused_m1_araddr_bits;
    wire [32 - AXI_ADDR_W-1:0] unused_m1_awaddr_bits;
    wire [19-1:0] unused_m2_araddr_bits;
    wire [19-1:0] unused_m2_awaddr_bits;
    wire [2-1:0] unused_m3_araddr_bits;
    wire [2-1:0] unused_m3_awaddr_bits;
// AXI manager interface for internal memory
    wire [18-1:0] int_mem_axi_araddr;
    wire int_mem_axi_arvalid;
    wire int_mem_axi_arready;
    wire [AXI_DATA_W-1:0] int_mem_axi_rdata;
    wire [2-1:0] int_mem_axi_rresp;
    wire int_mem_axi_rvalid;
    wire int_mem_axi_rready;
    wire [AXI_ID_W-1:0] int_mem_axi_arid;
    wire [AXI_LEN_W-1:0] int_mem_axi_arlen;
    wire [3-1:0] int_mem_axi_arsize;
    wire [2-1:0] int_mem_axi_arburst;
    wire int_mem_axi_arlock;
    wire [4-1:0] int_mem_axi_arcache;
    wire [4-1:0] int_mem_axi_arqos;
    wire [AXI_ID_W-1:0] int_mem_axi_rid;
    wire int_mem_axi_rlast;
    wire [18-1:0] int_mem_axi_awaddr;
    wire int_mem_axi_awvalid;
    wire int_mem_axi_awready;
    wire [AXI_DATA_W-1:0] int_mem_axi_wdata;
    wire [AXI_DATA_W/8-1:0] int_mem_axi_wstrb;
    wire int_mem_axi_wvalid;
    wire int_mem_axi_wready;
    wire [2-1:0] int_mem_axi_bresp;
    wire int_mem_axi_bvalid;
    wire int_mem_axi_bready;
    wire [AXI_ID_W-1:0] int_mem_axi_awid;
    wire [AXI_LEN_W-1:0] int_mem_axi_awlen;
    wire [3-1:0] int_mem_axi_awsize;
    wire [2-1:0] int_mem_axi_awburst;
    wire int_mem_axi_awlock;
    wire [4-1:0] int_mem_axi_awcache;
    wire [4-1:0] int_mem_axi_awqos;
    wire int_mem_axi_wlast;
    wire [AXI_ID_W-1:0] int_mem_axi_bid;
// iob-system boot controller data interface
    wire [13-1:0] bootrom_axi_araddr;
    wire bootrom_axi_arvalid;
    wire bootrom_axi_arready;
    wire [AXI_DATA_W-1:0] bootrom_axi_rdata;
    wire [2-1:0] bootrom_axi_rresp;
    wire bootrom_axi_rvalid;
    wire bootrom_axi_rready;
    wire [AXI_ID_W-1:0] bootrom_axi_arid;
    wire [AXI_LEN_W-1:0] bootrom_axi_arlen;
    wire [3-1:0] bootrom_axi_arsize;
    wire [2-1:0] bootrom_axi_arburst;
    wire bootrom_axi_arlock;
    wire [4-1:0] bootrom_axi_arcache;
    wire [4-1:0] bootrom_axi_arqos;
    wire [AXI_ID_W-1:0] bootrom_axi_rid;
    wire bootrom_axi_rlast;
    wire [13-1:0] bootrom_axi_awaddr;
    wire bootrom_axi_awvalid;
    wire bootrom_axi_awready;
    wire [AXI_DATA_W-1:0] bootrom_axi_wdata;
    wire [AXI_DATA_W/8-1:0] bootrom_axi_wstrb;
    wire bootrom_axi_wvalid;
    wire bootrom_axi_wready;
    wire [2-1:0] bootrom_axi_bresp;
    wire bootrom_axi_bvalid;
    wire bootrom_axi_bready;
    wire [AXI_ID_W-1:0] bootrom_axi_awid;
    wire [AXI_LEN_W-1:0] bootrom_axi_awlen;
    wire [3-1:0] bootrom_axi_awsize;
    wire [2-1:0] bootrom_axi_awburst;
    wire bootrom_axi_awlock;
    wire [4-1:0] bootrom_axi_awcache;
    wire [4-1:0] bootrom_axi_awqos;
    wire bootrom_axi_wlast;
    wire [AXI_ID_W-1:0] bootrom_axi_bid;
// AXI bus for peripheral CSRs
    wire [30-1:0] periphs_axi_araddr;
    wire periphs_axi_arvalid;
    wire periphs_axi_arready;
    wire [AXI_DATA_W-1:0] periphs_axi_rdata;
    wire [2-1:0] periphs_axi_rresp;
    wire periphs_axi_rvalid;
    wire periphs_axi_rready;
    wire [AXI_ID_W-1:0] periphs_axi_arid;
    wire [AXI_LEN_W-1:0] periphs_axi_arlen;
    wire [3-1:0] periphs_axi_arsize;
    wire [2-1:0] periphs_axi_arburst;
    wire [2-1:0] periphs_axi_arlock;
    wire [4-1:0] periphs_axi_arcache;
    wire [4-1:0] periphs_axi_arqos;
    wire [AXI_ID_W-1:0] periphs_axi_rid;
    wire periphs_axi_rlast;
    wire [30-1:0] periphs_axi_awaddr;
    wire periphs_axi_awvalid;
    wire periphs_axi_awready;
    wire [AXI_DATA_W-1:0] periphs_axi_wdata;
    wire [AXI_DATA_W/8-1:0] periphs_axi_wstrb;
    wire periphs_axi_wvalid;
    wire periphs_axi_wready;
    wire [2-1:0] periphs_axi_bresp;
    wire periphs_axi_bvalid;
    wire periphs_axi_bready;
    wire [AXI_ID_W-1:0] periphs_axi_awid;
    wire [AXI_LEN_W-1:0] periphs_axi_awlen;
    wire [3-1:0] periphs_axi_awsize;
    wire [2-1:0] periphs_axi_awburst;
    wire [2-1:0] periphs_axi_awlock;
    wire [4-1:0] periphs_axi_awcache;
    wire [4-1:0] periphs_axi_awqos;
    wire periphs_axi_wlast;
    wire [AXI_ID_W-1:0] periphs_axi_bid;
// AXI-Lite bus for peripheral CSRs
    wire periphs_iob_valid;
    wire [30-1:0] periphs_iob_addr;
    wire [AXI_DATA_W-1:0] periphs_iob_wdata;
    wire [AXI_DATA_W/8-1:0] periphs_iob_wstrb;
    wire periphs_iob_rvalid;
    wire [AXI_DATA_W-1:0] periphs_iob_rdata;
    wire periphs_iob_ready;
// uart0 Control/Status Registers bus
    wire uart0_cbus_iob_valid;
    wire [28-1:0] uart0_cbus_iob_addr;
    wire [32-1:0] uart0_cbus_iob_wdata;
    wire [32/8-1:0] uart0_cbus_iob_wstrb;
    wire uart0_cbus_iob_rvalid;
    wire [32-1:0] uart0_cbus_iob_rdata;
    wire uart0_cbus_iob_ready;
// timer0 Control/Status Registers bus
    wire timer0_cbus_iob_valid;
    wire [28-1:0] timer0_cbus_iob_addr;
    wire [32-1:0] timer0_cbus_iob_wdata;
    wire [32/8-1:0] timer0_cbus_iob_wstrb;
    wire timer0_cbus_iob_rvalid;
    wire [32-1:0] timer0_cbus_iob_rdata;
    wire timer0_cbus_iob_ready;
// CLINT Control/Status Registers bus
    wire clint_cbus_iob_valid;
    wire [28-1:0] clint_cbus_iob_addr;
    wire [32-1:0] clint_cbus_iob_wdata;
    wire [32/8-1:0] clint_cbus_iob_wstrb;
    wire clint_cbus_iob_rvalid;
    wire [32-1:0] clint_cbus_iob_rdata;
    wire clint_cbus_iob_ready;
// PLIC Control/Status Registers bus
    wire plic_cbus_iob_valid;
    wire [28-1:0] plic_cbus_iob_addr;
    wire [32-1:0] plic_cbus_iob_wdata;
    wire [32/8-1:0] plic_cbus_iob_wstrb;
    wire plic_cbus_iob_rvalid;
    wire [32-1:0] plic_cbus_iob_rdata;
    wire plic_cbus_iob_ready;


   assign interrupts = {{31{1'b0}},  1'b0};


        // RISC-V CPU instance
        iob_uart_tester_iob_vexriscv #(
        .AXI_ID_W(1),
        .AXI_ADDR_W(32),
        .AXI_DATA_W(32),
        .AXI_LEN_W(AXI_LEN_W)
    ) cpu (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // rst_i port: Synchronous reset
        .rst_i(arst_i),
        // i_bus_m port: iob-picorv32 instruction bus
        .ibus_axi_araddr_o(cpu_i_axi_araddr),
        .ibus_axi_arvalid_o(cpu_i_axi_arvalid),
        .ibus_axi_arready_i(cpu_i_axi_arready),
        .ibus_axi_rdata_i(cpu_i_axi_rdata),
        .ibus_axi_rresp_i(cpu_i_axi_rresp),
        .ibus_axi_rvalid_i(cpu_i_axi_rvalid),
        .ibus_axi_rready_o(cpu_i_axi_rready),
        .ibus_axi_arid_o(cpu_i_axi_arid[0]),
        .ibus_axi_arlen_o(cpu_i_axi_arlen),
        .ibus_axi_arsize_o(cpu_i_axi_arsize),
        .ibus_axi_arburst_o(cpu_i_axi_arburst),
        .ibus_axi_arlock_o(cpu_i_axi_arlock),
        .ibus_axi_arcache_o(cpu_i_axi_arcache),
        .ibus_axi_arqos_o(cpu_i_axi_arqos),
        .ibus_axi_rid_i(cpu_i_axi_rid[0]),
        .ibus_axi_rlast_i(cpu_i_axi_rlast),
        .ibus_axi_awaddr_o(cpu_i_axi_awaddr),
        .ibus_axi_awvalid_o(cpu_i_axi_awvalid),
        .ibus_axi_awready_i(cpu_i_axi_awready),
        .ibus_axi_wdata_o(cpu_i_axi_wdata),
        .ibus_axi_wstrb_o(cpu_i_axi_wstrb),
        .ibus_axi_wvalid_o(cpu_i_axi_wvalid),
        .ibus_axi_wready_i(cpu_i_axi_wready),
        .ibus_axi_bresp_i(cpu_i_axi_bresp),
        .ibus_axi_bvalid_i(cpu_i_axi_bvalid),
        .ibus_axi_bready_o(cpu_i_axi_bready),
        .ibus_axi_awid_o(cpu_i_axi_awid[0]),
        .ibus_axi_awlen_o(cpu_i_axi_awlen),
        .ibus_axi_awsize_o(cpu_i_axi_awsize),
        .ibus_axi_awburst_o(cpu_i_axi_awburst),
        .ibus_axi_awlock_o(cpu_i_axi_awlock),
        .ibus_axi_awcache_o(cpu_i_axi_awcache),
        .ibus_axi_awqos_o(cpu_i_axi_awqos),
        .ibus_axi_wlast_o(cpu_i_axi_wlast),
        .ibus_axi_bid_i(cpu_i_axi_bid[0]),
        // d_bus_m port: iob-picorv32 data bus
        .dbus_axi_araddr_o(cpu_d_axi_araddr),
        .dbus_axi_arvalid_o(cpu_d_axi_arvalid),
        .dbus_axi_arready_i(cpu_d_axi_arready),
        .dbus_axi_rdata_i(cpu_d_axi_rdata),
        .dbus_axi_rresp_i(cpu_d_axi_rresp),
        .dbus_axi_rvalid_i(cpu_d_axi_rvalid),
        .dbus_axi_rready_o(cpu_d_axi_rready),
        .dbus_axi_arid_o(cpu_d_axi_arid[0]),
        .dbus_axi_arlen_o(cpu_d_axi_arlen),
        .dbus_axi_arsize_o(cpu_d_axi_arsize),
        .dbus_axi_arburst_o(cpu_d_axi_arburst),
        .dbus_axi_arlock_o(cpu_d_axi_arlock),
        .dbus_axi_arcache_o(cpu_d_axi_arcache),
        .dbus_axi_arqos_o(cpu_d_axi_arqos),
        .dbus_axi_rid_i(cpu_d_axi_rid[0]),
        .dbus_axi_rlast_i(cpu_d_axi_rlast),
        .dbus_axi_awaddr_o(cpu_d_axi_awaddr),
        .dbus_axi_awvalid_o(cpu_d_axi_awvalid),
        .dbus_axi_awready_i(cpu_d_axi_awready),
        .dbus_axi_wdata_o(cpu_d_axi_wdata),
        .dbus_axi_wstrb_o(cpu_d_axi_wstrb),
        .dbus_axi_wvalid_o(cpu_d_axi_wvalid),
        .dbus_axi_wready_i(cpu_d_axi_wready),
        .dbus_axi_bresp_i(cpu_d_axi_bresp),
        .dbus_axi_bvalid_i(cpu_d_axi_bvalid),
        .dbus_axi_bready_o(cpu_d_axi_bready),
        .dbus_axi_awid_o(cpu_d_axi_awid[0]),
        .dbus_axi_awlen_o(cpu_d_axi_awlen),
        .dbus_axi_awsize_o(cpu_d_axi_awsize),
        .dbus_axi_awburst_o(cpu_d_axi_awburst),
        .dbus_axi_awlock_o(cpu_d_axi_awlock),
        .dbus_axi_awcache_o(cpu_d_axi_awcache),
        .dbus_axi_awqos_o(cpu_d_axi_awqos),
        .dbus_axi_wlast_o(cpu_d_axi_wlast),
        .dbus_axi_bid_i(cpu_d_axi_bid[0]),
        // plic_interrupts_i port: PLIC interrupts
        .plic_interrupts_i(interrupts),
        // plic_cbus_s port: PLIC CSRs bus
        .plic_iob_valid_i(plic_cbus_iob_valid),
        .plic_iob_addr_i(plic_cbus_iob_addr[22-1:0]),
        .plic_iob_wdata_i(plic_cbus_iob_wdata),
        .plic_iob_wstrb_i(plic_cbus_iob_wstrb),
        .plic_iob_rvalid_o(plic_cbus_iob_rvalid),
        .plic_iob_rdata_o(plic_cbus_iob_rdata),
        .plic_iob_ready_o(plic_cbus_iob_ready),
        // clint_cbus_s port: CLINT CSRs bus
        .clint_iob_valid_i(clint_cbus_iob_valid),
        .clint_iob_addr_i(clint_cbus_iob_addr[16-1:0]),
        .clint_iob_wdata_i(clint_cbus_iob_wdata),
        .clint_iob_wstrb_i(clint_cbus_iob_wstrb),
        .clint_iob_rvalid_o(clint_cbus_iob_rvalid),
        .clint_iob_rdata_o(clint_cbus_iob_rdata),
        .clint_iob_ready_o(clint_cbus_iob_ready)
        );

            // AXI full xbar instance
        iob_uart_tester_axi_full_xbar #(
        .ID_W(AXI_ID_W),
        .LEN_W(AXI_LEN_W)
    ) iob_axi_full_xbar (
            // clk_en_rst_s port: Clock, clock enable and async reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // rst_i port: Synchronous reset
        .rst_i(arst_i),
        // s0_axi_s port: Subordinate 0 interface
        .s0_axi_araddr_i(cpu_i_axi_araddr),
        .s0_axi_arvalid_i(cpu_i_axi_arvalid),
        .s0_axi_arready_o(cpu_i_axi_arready),
        .s0_axi_rdata_o(cpu_i_axi_rdata),
        .s0_axi_rresp_o(cpu_i_axi_rresp),
        .s0_axi_rvalid_o(cpu_i_axi_rvalid),
        .s0_axi_rready_i(cpu_i_axi_rready),
        .s0_axi_arid_i(cpu_i_axi_arid),
        .s0_axi_arlen_i(cpu_i_axi_arlen),
        .s0_axi_arsize_i(cpu_i_axi_arsize),
        .s0_axi_arburst_i(cpu_i_axi_arburst),
        .s0_axi_arlock_i(cpu_i_axi_arlock),
        .s0_axi_arcache_i(cpu_i_axi_arcache),
        .s0_axi_arqos_i(cpu_i_axi_arqos),
        .s0_axi_rid_o(cpu_i_axi_rid),
        .s0_axi_rlast_o(cpu_i_axi_rlast),
        .s0_axi_awaddr_i(cpu_i_axi_awaddr),
        .s0_axi_awvalid_i(cpu_i_axi_awvalid),
        .s0_axi_awready_o(cpu_i_axi_awready),
        .s0_axi_wdata_i(cpu_i_axi_wdata),
        .s0_axi_wstrb_i(cpu_i_axi_wstrb),
        .s0_axi_wvalid_i(cpu_i_axi_wvalid),
        .s0_axi_wready_o(cpu_i_axi_wready),
        .s0_axi_bresp_o(cpu_i_axi_bresp),
        .s0_axi_bvalid_o(cpu_i_axi_bvalid),
        .s0_axi_bready_i(cpu_i_axi_bready),
        .s0_axi_awid_i(cpu_i_axi_awid),
        .s0_axi_awlen_i(cpu_i_axi_awlen),
        .s0_axi_awsize_i(cpu_i_axi_awsize),
        .s0_axi_awburst_i(cpu_i_axi_awburst),
        .s0_axi_awlock_i(cpu_i_axi_awlock),
        .s0_axi_awcache_i(cpu_i_axi_awcache),
        .s0_axi_awqos_i(cpu_i_axi_awqos),
        .s0_axi_wlast_i(cpu_i_axi_wlast),
        .s0_axi_bid_o(cpu_i_axi_bid),
        // s1_axi_s port: Subordinate 1 interface
        .s1_axi_araddr_i(cpu_d_axi_araddr),
        .s1_axi_arvalid_i(cpu_d_axi_arvalid),
        .s1_axi_arready_o(cpu_d_axi_arready),
        .s1_axi_rdata_o(cpu_d_axi_rdata),
        .s1_axi_rresp_o(cpu_d_axi_rresp),
        .s1_axi_rvalid_o(cpu_d_axi_rvalid),
        .s1_axi_rready_i(cpu_d_axi_rready),
        .s1_axi_arid_i(cpu_d_axi_arid),
        .s1_axi_arlen_i(cpu_d_axi_arlen),
        .s1_axi_arsize_i(cpu_d_axi_arsize),
        .s1_axi_arburst_i(cpu_d_axi_arburst),
        .s1_axi_arlock_i(cpu_d_axi_arlock),
        .s1_axi_arcache_i(cpu_d_axi_arcache),
        .s1_axi_arqos_i(cpu_d_axi_arqos),
        .s1_axi_rid_o(cpu_d_axi_rid),
        .s1_axi_rlast_o(cpu_d_axi_rlast),
        .s1_axi_awaddr_i(cpu_d_axi_awaddr),
        .s1_axi_awvalid_i(cpu_d_axi_awvalid),
        .s1_axi_awready_o(cpu_d_axi_awready),
        .s1_axi_wdata_i(cpu_d_axi_wdata),
        .s1_axi_wstrb_i(cpu_d_axi_wstrb),
        .s1_axi_wvalid_i(cpu_d_axi_wvalid),
        .s1_axi_wready_o(cpu_d_axi_wready),
        .s1_axi_bresp_o(cpu_d_axi_bresp),
        .s1_axi_bvalid_o(cpu_d_axi_bvalid),
        .s1_axi_bready_i(cpu_d_axi_bready),
        .s1_axi_awid_i(cpu_d_axi_awid),
        .s1_axi_awlen_i(cpu_d_axi_awlen),
        .s1_axi_awsize_i(cpu_d_axi_awsize),
        .s1_axi_awburst_i(cpu_d_axi_awburst),
        .s1_axi_awlock_i(cpu_d_axi_awlock),
        .s1_axi_awcache_i(cpu_d_axi_awcache),
        .s1_axi_awqos_i(cpu_d_axi_awqos),
        .s1_axi_wlast_i(cpu_d_axi_wlast),
        .s1_axi_bid_o(cpu_d_axi_bid),
        // m0_axi_m port: Manager 0 interface
        .m0_axi_araddr_o({unused_m0_araddr_bits, int_mem_axi_araddr}),
        .m0_axi_arvalid_o(int_mem_axi_arvalid),
        .m0_axi_arready_i(int_mem_axi_arready),
        .m0_axi_rdata_i(int_mem_axi_rdata),
        .m0_axi_rresp_i(int_mem_axi_rresp),
        .m0_axi_rvalid_i(int_mem_axi_rvalid),
        .m0_axi_rready_o(int_mem_axi_rready),
        .m0_axi_arid_o(int_mem_axi_arid),
        .m0_axi_arlen_o(int_mem_axi_arlen),
        .m0_axi_arsize_o(int_mem_axi_arsize),
        .m0_axi_arburst_o(int_mem_axi_arburst),
        .m0_axi_arlock_o(int_mem_axi_arlock),
        .m0_axi_arcache_o(int_mem_axi_arcache),
        .m0_axi_arqos_o(int_mem_axi_arqos),
        .m0_axi_rid_i(int_mem_axi_rid),
        .m0_axi_rlast_i(int_mem_axi_rlast),
        .m0_axi_awaddr_o({unused_m0_awaddr_bits, int_mem_axi_awaddr}),
        .m0_axi_awvalid_o(int_mem_axi_awvalid),
        .m0_axi_awready_i(int_mem_axi_awready),
        .m0_axi_wdata_o(int_mem_axi_wdata),
        .m0_axi_wstrb_o(int_mem_axi_wstrb),
        .m0_axi_wvalid_o(int_mem_axi_wvalid),
        .m0_axi_wready_i(int_mem_axi_wready),
        .m0_axi_bresp_i(int_mem_axi_bresp),
        .m0_axi_bvalid_i(int_mem_axi_bvalid),
        .m0_axi_bready_o(int_mem_axi_bready),
        .m0_axi_awid_o(int_mem_axi_awid),
        .m0_axi_awlen_o(int_mem_axi_awlen),
        .m0_axi_awsize_o(int_mem_axi_awsize),
        .m0_axi_awburst_o(int_mem_axi_awburst),
        .m0_axi_awlock_o(int_mem_axi_awlock),
        .m0_axi_awcache_o(int_mem_axi_awcache),
        .m0_axi_awqos_o(int_mem_axi_awqos),
        .m0_axi_wlast_o(int_mem_axi_wlast),
        .m0_axi_bid_i(int_mem_axi_bid),
        // m1_axi_m port: Manager 1 interface
        .m1_axi_araddr_o({unused_m2_araddr_bits, bootrom_axi_araddr}),
        .m1_axi_arvalid_o(bootrom_axi_arvalid),
        .m1_axi_arready_i(bootrom_axi_arready),
        .m1_axi_rdata_i(bootrom_axi_rdata),
        .m1_axi_rresp_i(bootrom_axi_rresp),
        .m1_axi_rvalid_i(bootrom_axi_rvalid),
        .m1_axi_rready_o(bootrom_axi_rready),
        .m1_axi_arid_o(bootrom_axi_arid),
        .m1_axi_arlen_o(bootrom_axi_arlen),
        .m1_axi_arsize_o(bootrom_axi_arsize),
        .m1_axi_arburst_o(bootrom_axi_arburst),
        .m1_axi_arlock_o(bootrom_axi_arlock),
        .m1_axi_arcache_o(bootrom_axi_arcache),
        .m1_axi_arqos_o(bootrom_axi_arqos),
        .m1_axi_rid_i(bootrom_axi_rid),
        .m1_axi_rlast_i(bootrom_axi_rlast),
        .m1_axi_awaddr_o({unused_m2_awaddr_bits, bootrom_axi_awaddr}),
        .m1_axi_awvalid_o(bootrom_axi_awvalid),
        .m1_axi_awready_i(bootrom_axi_awready),
        .m1_axi_wdata_o(bootrom_axi_wdata),
        .m1_axi_wstrb_o(bootrom_axi_wstrb),
        .m1_axi_wvalid_o(bootrom_axi_wvalid),
        .m1_axi_wready_i(bootrom_axi_wready),
        .m1_axi_bresp_i(bootrom_axi_bresp),
        .m1_axi_bvalid_i(bootrom_axi_bvalid),
        .m1_axi_bready_o(bootrom_axi_bready),
        .m1_axi_awid_o(bootrom_axi_awid),
        .m1_axi_awlen_o(bootrom_axi_awlen),
        .m1_axi_awsize_o(bootrom_axi_awsize),
        .m1_axi_awburst_o(bootrom_axi_awburst),
        .m1_axi_awlock_o(bootrom_axi_awlock),
        .m1_axi_awcache_o(bootrom_axi_awcache),
        .m1_axi_awqos_o(bootrom_axi_awqos),
        .m1_axi_wlast_o(bootrom_axi_wlast),
        .m1_axi_bid_i(bootrom_axi_bid),
        // m2_axi_m port: Manager 2 interface
        .m2_axi_araddr_o({unused_m3_araddr_bits, periphs_axi_araddr}),
        .m2_axi_arvalid_o(periphs_axi_arvalid),
        .m2_axi_arready_i(periphs_axi_arready),
        .m2_axi_rdata_i(periphs_axi_rdata),
        .m2_axi_rresp_i(periphs_axi_rresp),
        .m2_axi_rvalid_i(periphs_axi_rvalid),
        .m2_axi_rready_o(periphs_axi_rready),
        .m2_axi_arid_o(periphs_axi_arid),
        .m2_axi_arlen_o(periphs_axi_arlen),
        .m2_axi_arsize_o(periphs_axi_arsize),
        .m2_axi_arburst_o(periphs_axi_arburst),
        .m2_axi_arlock_o(periphs_axi_arlock[0]),
        .m2_axi_arcache_o(periphs_axi_arcache),
        .m2_axi_arqos_o(periphs_axi_arqos),
        .m2_axi_rid_i(periphs_axi_rid),
        .m2_axi_rlast_i(periphs_axi_rlast),
        .m2_axi_awaddr_o({unused_m3_awaddr_bits, periphs_axi_awaddr}),
        .m2_axi_awvalid_o(periphs_axi_awvalid),
        .m2_axi_awready_i(periphs_axi_awready),
        .m2_axi_wdata_o(periphs_axi_wdata),
        .m2_axi_wstrb_o(periphs_axi_wstrb),
        .m2_axi_wvalid_o(periphs_axi_wvalid),
        .m2_axi_wready_i(periphs_axi_wready),
        .m2_axi_bresp_i(periphs_axi_bresp),
        .m2_axi_bvalid_i(periphs_axi_bvalid),
        .m2_axi_bready_o(periphs_axi_bready),
        .m2_axi_awid_o(periphs_axi_awid),
        .m2_axi_awlen_o(periphs_axi_awlen),
        .m2_axi_awsize_o(periphs_axi_awsize),
        .m2_axi_awburst_o(periphs_axi_awburst),
        .m2_axi_awlock_o(periphs_axi_awlock[0]),
        .m2_axi_awcache_o(periphs_axi_awcache),
        .m2_axi_awqos_o(periphs_axi_awqos),
        .m2_axi_wlast_o(periphs_axi_wlast),
        .m2_axi_bid_i(periphs_axi_bid)
        );

            // Internal memory
        iob_axi_ram #(
        .ID_WIDTH(AXI_ID_W),
        .LEN_WIDTH(AXI_LEN_W),
        .ADDR_WIDTH(18),
        .DATA_WIDTH(AXI_DATA_W)
    ) internal_memory (
            // clk_i port: Clock
        .clk_i(clk_i),
        // rst_i port: Synchronous reset
        .rst_i(arst_i),
        // axi_s port: AXI interface
        .axi_araddr_i(int_mem_axi_araddr),
        .axi_arvalid_i(int_mem_axi_arvalid),
        .axi_arready_o(int_mem_axi_arready),
        .axi_rdata_o(int_mem_axi_rdata),
        .axi_rresp_o(int_mem_axi_rresp),
        .axi_rvalid_o(int_mem_axi_rvalid),
        .axi_rready_i(int_mem_axi_rready),
        .axi_arid_i(int_mem_axi_arid),
        .axi_arlen_i(int_mem_axi_arlen),
        .axi_arsize_i(int_mem_axi_arsize),
        .axi_arburst_i(int_mem_axi_arburst),
        .axi_arlock_i({1'b0, int_mem_axi_arlock}),
        .axi_arcache_i(int_mem_axi_arcache),
        .axi_arqos_i(int_mem_axi_arqos),
        .axi_rid_o(int_mem_axi_rid),
        .axi_rlast_o(int_mem_axi_rlast),
        .axi_awaddr_i(int_mem_axi_awaddr),
        .axi_awvalid_i(int_mem_axi_awvalid),
        .axi_awready_o(int_mem_axi_awready),
        .axi_wdata_i(int_mem_axi_wdata),
        .axi_wstrb_i(int_mem_axi_wstrb),
        .axi_wvalid_i(int_mem_axi_wvalid),
        .axi_wready_o(int_mem_axi_wready),
        .axi_bresp_o(int_mem_axi_bresp),
        .axi_bvalid_o(int_mem_axi_bvalid),
        .axi_bready_i(int_mem_axi_bready),
        .axi_awid_i(int_mem_axi_awid),
        .axi_awlen_i(int_mem_axi_awlen),
        .axi_awsize_i(int_mem_axi_awsize),
        .axi_awburst_i(int_mem_axi_awburst),
        .axi_awlock_i({1'b0, int_mem_axi_awlock}),
        .axi_awcache_i(int_mem_axi_awcache),
        .axi_awqos_i(int_mem_axi_awqos),
        .axi_wlast_i(int_mem_axi_wlast),
        .axi_bid_o(int_mem_axi_bid),
        // external_mem_bus_m port: Port for connection to external 'iob_ram_t2p_be' memory
        .ext_mem_clk_o(int_mem_clk_o),
        .ext_mem_r_en_o(int_mem_r_en_o),
        .ext_mem_r_addr_o(int_mem_r_addr_o),
        .ext_mem_r_data_i(int_mem_r_data_i),
        .ext_mem_w_strb_o(int_mem_w_strb_o),
        .ext_mem_w_addr_o(int_mem_w_addr_o),
        .ext_mem_w_data_o(int_mem_w_data_o)
        );

            // Boot ROM peripheral
        iob_bootrom #(
        .AXI_ID_W(AXI_ID_W),
        .AXI_LEN_W(AXI_LEN_W)
    ) bootrom (
            // clk_en_rst_s port: Clock and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // iob_csrs_cbus_s port: Control and Status Registers interface (auto-generated)
        .iob_csrs_axi_araddr_i(bootrom_axi_araddr),
        .iob_csrs_axi_arvalid_i(bootrom_axi_arvalid),
        .iob_csrs_axi_arready_o(bootrom_axi_arready),
        .iob_csrs_axi_rdata_o(bootrom_axi_rdata),
        .iob_csrs_axi_rresp_o(bootrom_axi_rresp),
        .iob_csrs_axi_rvalid_o(bootrom_axi_rvalid),
        .iob_csrs_axi_rready_i(bootrom_axi_rready),
        .iob_csrs_axi_arid_i(bootrom_axi_arid),
        .iob_csrs_axi_arlen_i(bootrom_axi_arlen),
        .iob_csrs_axi_arsize_i(bootrom_axi_arsize),
        .iob_csrs_axi_arburst_i(bootrom_axi_arburst),
        .iob_csrs_axi_arlock_i({1'b0, bootrom_axi_arlock}),
        .iob_csrs_axi_arcache_i(bootrom_axi_arcache),
        .iob_csrs_axi_arqos_i(bootrom_axi_arqos),
        .iob_csrs_axi_rid_o(bootrom_axi_rid),
        .iob_csrs_axi_rlast_o(bootrom_axi_rlast),
        .iob_csrs_axi_awaddr_i(bootrom_axi_awaddr),
        .iob_csrs_axi_awvalid_i(bootrom_axi_awvalid),
        .iob_csrs_axi_awready_o(bootrom_axi_awready),
        .iob_csrs_axi_wdata_i(bootrom_axi_wdata),
        .iob_csrs_axi_wstrb_i(bootrom_axi_wstrb),
        .iob_csrs_axi_wvalid_i(bootrom_axi_wvalid),
        .iob_csrs_axi_wready_o(bootrom_axi_wready),
        .iob_csrs_axi_bresp_o(bootrom_axi_bresp),
        .iob_csrs_axi_bvalid_o(bootrom_axi_bvalid),
        .iob_csrs_axi_bready_i(bootrom_axi_bready),
        .iob_csrs_axi_awid_i(bootrom_axi_awid),
        .iob_csrs_axi_awlen_i(bootrom_axi_awlen),
        .iob_csrs_axi_awsize_i(bootrom_axi_awsize),
        .iob_csrs_axi_awburst_i(bootrom_axi_awburst),
        .iob_csrs_axi_awlock_i({1'b0, bootrom_axi_awlock}),
        .iob_csrs_axi_awcache_i(bootrom_axi_awcache),
        .iob_csrs_axi_awqos_i(bootrom_axi_awqos),
        .iob_csrs_axi_wlast_i(bootrom_axi_wlast),
        .iob_csrs_axi_bid_o(bootrom_axi_bid),
        // rom_bus_m port: External rom ROM signals.
        .rom_clk_o(bootrom_mem_clk_o),
        .rom_addr_o(bootrom_mem_addr_o),
        .rom_en_o(bootrom_mem_en_o),
        .rom_r_data_i(bootrom_mem_r_data_i)
        );

            // Convert AXI to AXI lite for CLINT
        iob_axi2iob #(
        .AXI_ID_WIDTH(AXI_ID_W),
        .AXI_LEN_WIDTH(AXI_LEN_W),
        .ADDR_WIDTH(30),
        .DATA_WIDTH(AXI_DATA_W)
    ) periphs_axi2iob (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // axi_s port: Subordinate AXI interface
        .s_axi_araddr_i(periphs_axi_araddr),
        .s_axi_arvalid_i(periphs_axi_arvalid),
        .s_axi_arready_o(periphs_axi_arready),
        .s_axi_rdata_o(periphs_axi_rdata),
        .s_axi_rresp_o(periphs_axi_rresp),
        .s_axi_rvalid_o(periphs_axi_rvalid),
        .s_axi_rready_i(periphs_axi_rready),
        .s_axi_arid_i(periphs_axi_arid),
        .s_axi_arlen_i(periphs_axi_arlen),
        .s_axi_arsize_i(periphs_axi_arsize),
        .s_axi_arburst_i(periphs_axi_arburst),
        .s_axi_arlock_i(periphs_axi_arlock[0]),
        .s_axi_arcache_i(periphs_axi_arcache),
        .s_axi_arqos_i(periphs_axi_arqos),
        .s_axi_rid_o(periphs_axi_rid),
        .s_axi_rlast_o(periphs_axi_rlast),
        .s_axi_awaddr_i(periphs_axi_awaddr),
        .s_axi_awvalid_i(periphs_axi_awvalid),
        .s_axi_awready_o(periphs_axi_awready),
        .s_axi_wdata_i(periphs_axi_wdata),
        .s_axi_wstrb_i(periphs_axi_wstrb),
        .s_axi_wvalid_i(periphs_axi_wvalid),
        .s_axi_wready_o(periphs_axi_wready),
        .s_axi_bresp_o(periphs_axi_bresp),
        .s_axi_bvalid_o(periphs_axi_bvalid),
        .s_axi_bready_i(periphs_axi_bready),
        .s_axi_awid_i(periphs_axi_awid),
        .s_axi_awlen_i(periphs_axi_awlen),
        .s_axi_awsize_i(periphs_axi_awsize),
        .s_axi_awburst_i(periphs_axi_awburst),
        .s_axi_awlock_i(periphs_axi_awlock[0]),
        .s_axi_awcache_i(periphs_axi_awcache),
        .s_axi_awqos_i(periphs_axi_awqos),
        .s_axi_wlast_i(periphs_axi_wlast),
        .s_axi_bid_o(periphs_axi_bid),
        // iob_m port: Manager IOb interface
        .iob_valid_o(periphs_iob_valid),
        .iob_addr_o(periphs_iob_addr),
        .iob_wdata_o(periphs_iob_wdata),
        .iob_wstrb_o(periphs_iob_wstrb),
        .iob_rvalid_i(periphs_iob_rvalid),
        .iob_rdata_i(periphs_iob_rdata),
        .iob_ready_i(periphs_iob_ready)
        );

            // Split between peripherals
        iob_uart_tester_pbus_split iob_pbus_split (
            // clk_en_rst_s port: Clock, clock enable and async reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // reset_i port: Reset signal
        .rst_i(arst_i),
        // s_s port: Split subordinate interface
        .s_iob_valid_i(periphs_iob_valid),
        .s_iob_addr_i(periphs_iob_addr),
        .s_iob_wdata_i(periphs_iob_wdata),
        .s_iob_wstrb_i(periphs_iob_wstrb),
        .s_iob_rvalid_o(periphs_iob_rvalid),
        .s_iob_rdata_o(periphs_iob_rdata),
        .s_iob_ready_o(periphs_iob_ready),
        // m_0_m port: Split manager interface
        .m0_iob_valid_o(uart0_cbus_iob_valid),
        .m0_iob_addr_o(uart0_cbus_iob_addr),
        .m0_iob_wdata_o(uart0_cbus_iob_wdata),
        .m0_iob_wstrb_o(uart0_cbus_iob_wstrb),
        .m0_iob_rvalid_i(uart0_cbus_iob_rvalid),
        .m0_iob_rdata_i(uart0_cbus_iob_rdata),
        .m0_iob_ready_i(uart0_cbus_iob_ready),
        // m_1_m port: Split manager interface
        .m1_iob_valid_o(timer0_cbus_iob_valid),
        .m1_iob_addr_o(timer0_cbus_iob_addr),
        .m1_iob_wdata_o(timer0_cbus_iob_wdata),
        .m1_iob_wstrb_o(timer0_cbus_iob_wstrb),
        .m1_iob_rvalid_i(timer0_cbus_iob_rvalid),
        .m1_iob_rdata_i(timer0_cbus_iob_rdata),
        .m1_iob_ready_i(timer0_cbus_iob_ready),
        // m_2_m port: Split manager interface
        .m2_iob_valid_o(clint_cbus_iob_valid),
        .m2_iob_addr_o(clint_cbus_iob_addr),
        .m2_iob_wdata_o(clint_cbus_iob_wdata),
        .m2_iob_wstrb_o(clint_cbus_iob_wstrb),
        .m2_iob_rvalid_i(clint_cbus_iob_rvalid),
        .m2_iob_rdata_i(clint_cbus_iob_rdata),
        .m2_iob_ready_i(clint_cbus_iob_ready),
        // m_3_m port: Split manager interface
        .m3_iob_valid_o(plic_cbus_iob_valid),
        .m3_iob_addr_o(plic_cbus_iob_addr),
        .m3_iob_wdata_o(plic_cbus_iob_wdata),
        .m3_iob_wstrb_o(plic_cbus_iob_wstrb),
        .m3_iob_rvalid_i(plic_cbus_iob_rvalid),
        .m3_iob_rdata_i(plic_cbus_iob_rdata),
        .m3_iob_ready_i(plic_cbus_iob_ready)
        );

            // UART peripheral
        iob_uart UART0 (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // rs232_m port: RS232 interface
        .rs232_rxd_i(rs232_rxd_i),
        .rs232_txd_o(rs232_txd_o),
        .rs232_rts_o(rs232_rts_o),
        .rs232_cts_i(rs232_cts_i),
        // iob_csrs_cbus_s port: Control and Status Registers interface (auto-generated)
        .iob_csrs_iob_valid_i(uart0_cbus_iob_valid),
        .iob_csrs_iob_addr_i(uart0_cbus_iob_addr[3-1:0]),
        .iob_csrs_iob_wdata_i(uart0_cbus_iob_wdata),
        .iob_csrs_iob_wstrb_i(uart0_cbus_iob_wstrb),
        .iob_csrs_iob_rvalid_o(uart0_cbus_iob_rvalid),
        .iob_csrs_iob_rdata_o(uart0_cbus_iob_rdata),
        .iob_csrs_iob_ready_o(uart0_cbus_iob_ready)
        );

            // Timer peripheral
        iob_timer TIMER0 (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // iob_csrs_cbus_s port: Control and Status Registers interface (auto-generated)
        .iob_csrs_iob_valid_i(timer0_cbus_iob_valid),
        .iob_csrs_iob_addr_i(timer0_cbus_iob_addr[4-1:0]),
        .iob_csrs_iob_wdata_i(timer0_cbus_iob_wdata),
        .iob_csrs_iob_wstrb_i(timer0_cbus_iob_wstrb),
        .iob_csrs_iob_rvalid_o(timer0_cbus_iob_rvalid),
        .iob_csrs_iob_rdata_o(timer0_cbus_iob_rdata),
        .iob_csrs_iob_ready_o(timer0_cbus_iob_ready)
        );

    
endmodule
