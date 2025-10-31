// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_tester_iob_vexriscv_conf.vh"

module iob_uart_tester_iob_vexriscv #(
    parameter AXI_ID_W = `IOB_UART_TESTER_IOB_VEXRISCV_AXI_ID_W,
    parameter AXI_ADDR_W = `IOB_UART_TESTER_IOB_VEXRISCV_AXI_ADDR_W,
    parameter AXI_DATA_W = `IOB_UART_TESTER_IOB_VEXRISCV_AXI_DATA_W,
    parameter AXI_LEN_W = `IOB_UART_TESTER_IOB_VEXRISCV_AXI_LEN_W
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // rst_i: Synchronous reset
    input rst_i,
    // i_bus_m: iob-picorv32 instruction bus
    output [AXI_ADDR_W-1:0] ibus_axi_araddr_o,
    output ibus_axi_arvalid_o,
    input ibus_axi_arready_i,
    input [AXI_DATA_W-1:0] ibus_axi_rdata_i,
    input [2-1:0] ibus_axi_rresp_i,
    input ibus_axi_rvalid_i,
    output ibus_axi_rready_o,
    output [AXI_ID_W-1:0] ibus_axi_arid_o,
    output [AXI_LEN_W-1:0] ibus_axi_arlen_o,
    output [3-1:0] ibus_axi_arsize_o,
    output [2-1:0] ibus_axi_arburst_o,
    output ibus_axi_arlock_o,
    output [4-1:0] ibus_axi_arcache_o,
    output [4-1:0] ibus_axi_arqos_o,
    input [AXI_ID_W-1:0] ibus_axi_rid_i,
    input ibus_axi_rlast_i,
    output [AXI_ADDR_W-1:0] ibus_axi_awaddr_o,
    output ibus_axi_awvalid_o,
    input ibus_axi_awready_i,
    output [AXI_DATA_W-1:0] ibus_axi_wdata_o,
    output [AXI_DATA_W/8-1:0] ibus_axi_wstrb_o,
    output ibus_axi_wvalid_o,
    input ibus_axi_wready_i,
    input [2-1:0] ibus_axi_bresp_i,
    input ibus_axi_bvalid_i,
    output ibus_axi_bready_o,
    output [AXI_ID_W-1:0] ibus_axi_awid_o,
    output [AXI_LEN_W-1:0] ibus_axi_awlen_o,
    output [3-1:0] ibus_axi_awsize_o,
    output [2-1:0] ibus_axi_awburst_o,
    output ibus_axi_awlock_o,
    output [4-1:0] ibus_axi_awcache_o,
    output [4-1:0] ibus_axi_awqos_o,
    output ibus_axi_wlast_o,
    input [AXI_ID_W-1:0] ibus_axi_bid_i,
    // d_bus_m: iob-picorv32 data bus
    output [AXI_ADDR_W-1:0] dbus_axi_araddr_o,
    output dbus_axi_arvalid_o,
    input dbus_axi_arready_i,
    input [AXI_DATA_W-1:0] dbus_axi_rdata_i,
    input [2-1:0] dbus_axi_rresp_i,
    input dbus_axi_rvalid_i,
    output dbus_axi_rready_o,
    output [AXI_ID_W-1:0] dbus_axi_arid_o,
    output [AXI_LEN_W-1:0] dbus_axi_arlen_o,
    output [3-1:0] dbus_axi_arsize_o,
    output [2-1:0] dbus_axi_arburst_o,
    output dbus_axi_arlock_o,
    output [4-1:0] dbus_axi_arcache_o,
    output [4-1:0] dbus_axi_arqos_o,
    input [AXI_ID_W-1:0] dbus_axi_rid_i,
    input dbus_axi_rlast_i,
    output [AXI_ADDR_W-1:0] dbus_axi_awaddr_o,
    output dbus_axi_awvalid_o,
    input dbus_axi_awready_i,
    output [AXI_DATA_W-1:0] dbus_axi_wdata_o,
    output [AXI_DATA_W/8-1:0] dbus_axi_wstrb_o,
    output dbus_axi_wvalid_o,
    input dbus_axi_wready_i,
    input [2-1:0] dbus_axi_bresp_i,
    input dbus_axi_bvalid_i,
    output dbus_axi_bready_o,
    output [AXI_ID_W-1:0] dbus_axi_awid_o,
    output [AXI_LEN_W-1:0] dbus_axi_awlen_o,
    output [3-1:0] dbus_axi_awsize_o,
    output [2-1:0] dbus_axi_awburst_o,
    output dbus_axi_awlock_o,
    output [4-1:0] dbus_axi_awcache_o,
    output [4-1:0] dbus_axi_awqos_o,
    output dbus_axi_wlast_o,
    input [AXI_ID_W-1:0] dbus_axi_bid_i,
    // clint_cbus_s: CLINT CSRs bus
    input clint_iob_valid_i,
    input [16-1:0] clint_iob_addr_i,
    input [32-1:0] clint_iob_wdata_i,
    input [32/8-1:0] clint_iob_wstrb_i,
    output clint_iob_rvalid_o,
    output [32-1:0] clint_iob_rdata_o,
    output clint_iob_ready_o,
    // plic_cbus_s: PLIC CSRs bus
    input plic_iob_valid_i,
    input [22-1:0] plic_iob_addr_i,
    input [32-1:0] plic_iob_wdata_i,
    input [32/8-1:0] plic_iob_wstrb_i,
    output plic_iob_rvalid_o,
    output [32-1:0] plic_iob_rdata_o,
    output plic_iob_ready_o,
    // plic_interrupts_i: PLIC interrupts
    input [32-1:0] plic_interrupts_i
);

// cpu reset signal
    wire cpu_reset;
// ibus internal signals
    wire [4-1:0] ibus_axi_arregion_int;
// dbus internal signals
    wire [4-1:0] dbus_axi_awregion_int;
    wire [4-1:0] dbus_axi_arregion_int;
// CLINT CSRs bus
    wire [16-1:0] clint_axil_araddr;
    wire clint_axil_arvalid;
    wire clint_axil_arready;
    wire [AXI_DATA_W-1:0] clint_axil_rdata;
    wire [2-1:0] clint_axil_rresp;
    wire clint_axil_rvalid;
    wire clint_axil_rready;
    wire [16-1:0] clint_axil_awaddr;
    wire clint_axil_awvalid;
    wire clint_axil_awready;
    wire [AXI_DATA_W-1:0] clint_axil_wdata;
    wire [AXI_DATA_W/8-1:0] clint_axil_wstrb;
    wire clint_axil_wvalid;
    wire clint_axil_wready;
    wire [2-1:0] clint_axil_bresp;
    wire clint_axil_bvalid;
    wire clint_axil_bready;
// PLIC CSRs bus
    wire [22-1:0] plic_axil_araddr;
    wire plic_axil_arvalid;
    wire plic_axil_arready;
    wire [AXI_DATA_W-1:0] plic_axil_rdata;
    wire [2-1:0] plic_axil_rresp;
    wire plic_axil_rvalid;
    wire plic_axil_rready;
    wire [22-1:0] plic_axil_awaddr;
    wire plic_axil_awvalid;
    wire plic_axil_awready;
    wire [AXI_DATA_W-1:0] plic_axil_wdata;
    wire [AXI_DATA_W/8-1:0] plic_axil_wstrb;
    wire plic_axil_wvalid;
    wire plic_axil_wready;
    wire [2-1:0] plic_axil_bresp;
    wire plic_axil_bvalid;
    wire plic_axil_bready;


    wire [7:0] ibus_axi_arlen_int;
    wire [7:0] dbus_axi_arlen_int;
    wire [7:0] dbus_axi_awlen_int;


  // Instantiation of VexRiscv, Plic, and Clint
  VexRiscvAxi4LinuxPlicClint CPU (
      // CLINT
      .clint_awvalid(clint_axil_awvalid),
      .clint_awready(clint_axil_awready),
      .clint_awaddr(clint_axil_awaddr),
      .clint_awprot(3'd0),
      .clint_wvalid(clint_axil_wvalid),
      .clint_wready(clint_axil_wready),
      .clint_wdata(clint_axil_wdata),
      .clint_wstrb(clint_axil_wstrb),
      .clint_bvalid(clint_axil_bvalid),
      .clint_bready(clint_axil_bready),
      .clint_bresp(clint_axil_bresp),
      .clint_arvalid(clint_axil_arvalid),
      .clint_arready(clint_axil_arready),
      .clint_araddr(clint_axil_araddr),
      .clint_arprot(3'd0),
      .clint_rvalid(clint_axil_rvalid),
      .clint_rready(clint_axil_rready),
      .clint_rdata(clint_axil_rdata),
      .clint_rresp(clint_axil_rresp),
      // PLIC
      .plic_awvalid(plic_axil_awvalid),
      .plic_awready(plic_axil_awready),
      .plic_awaddr(plic_axil_awaddr),
      .plic_awprot(3'd0),
      .plic_wvalid(plic_axil_wvalid),
      .plic_wready(plic_axil_wready),
      .plic_wdata(plic_axil_wdata),
      .plic_wstrb(plic_axil_wstrb),
      .plic_bvalid(plic_axil_bvalid),
      .plic_bready(plic_axil_bready),
      .plic_bresp(plic_axil_bresp),
      .plic_arvalid(plic_axil_arvalid),
      .plic_arready(plic_axil_arready),
      .plic_araddr(plic_axil_araddr),
      .plic_arprot(3'd0),
      .plic_rvalid(plic_axil_rvalid),
      .plic_rready(plic_axil_rready),
      .plic_rdata(plic_axil_rdata),
      .plic_rresp(plic_axil_rresp),
      .plicInterrupts(plic_interrupts_i),

      // Configuration ports
      .externalResetVector(32'h40000000),
      .ioStartAddr(32'h80000000),
      .ioSize(32'h40000000),

      // Instruction Bus
      .iBusAxi_arvalid(ibus_axi_arvalid_o),
      .iBusAxi_arready(ibus_axi_arready_i),
      .iBusAxi_araddr(ibus_axi_araddr_o),
      .iBusAxi_arid(ibus_axi_arid_o),
      .iBusAxi_arregion(ibus_axi_arregion_int),
      .iBusAxi_arlen(ibus_axi_arlen_int),
      .iBusAxi_arsize(ibus_axi_arsize_o),
      .iBusAxi_arburst(ibus_axi_arburst_o),
      .iBusAxi_arlock(ibus_axi_arlock_o),
      .iBusAxi_arcache(ibus_axi_arcache_o),
      .iBusAxi_arqos(ibus_axi_arqos_o),
      .iBusAxi_arprot(),
      .iBusAxi_rvalid(ibus_axi_rvalid_i),
      .iBusAxi_rready(ibus_axi_rready_o),
      .iBusAxi_rdata(ibus_axi_rdata_i),
      .iBusAxi_rid(ibus_axi_rid_i),
      .iBusAxi_rresp(ibus_axi_rresp_i),
      .iBusAxi_rlast(ibus_axi_rlast_i),
      // Data Bus
      .dBusAxi_awvalid(dbus_axi_awvalid_o),
      .dBusAxi_awready(dbus_axi_awready_i),
      .dBusAxi_awaddr(dbus_axi_awaddr_o),
      .dBusAxi_awid(dbus_axi_awid_o),
      .dBusAxi_awregion(dbus_axi_awregion_int),
      .dBusAxi_awlen(dbus_axi_awlen_int),
      .dBusAxi_awsize(dbus_axi_awsize_o),
      .dBusAxi_awburst(dbus_axi_awburst_o),
      .dBusAxi_awlock(dbus_axi_awlock_o),
      .dBusAxi_awcache(dbus_axi_awcache_o),
      .dBusAxi_awqos(dbus_axi_awqos_o),
      .dBusAxi_awprot(),
      .dBusAxi_wvalid(dbus_axi_wvalid_o),
      .dBusAxi_wready(dbus_axi_wready_i),
      .dBusAxi_wdata(dbus_axi_wdata_o),
      .dBusAxi_wstrb(dbus_axi_wstrb_o),
      .dBusAxi_wlast(dbus_axi_wlast_o),
      .dBusAxi_bvalid(dbus_axi_bvalid_i),
      .dBusAxi_bready(dbus_axi_bready_o),
      .dBusAxi_bid(dbus_axi_bid_i),
      .dBusAxi_bresp(dbus_axi_bresp_i),
      .dBusAxi_arvalid(dbus_axi_arvalid_o),
      .dBusAxi_arready(dbus_axi_arready_i),
      .dBusAxi_araddr(dbus_axi_araddr_o),
      .dBusAxi_arid(dbus_axi_arid_o),
      .dBusAxi_arregion(dbus_axi_arregion_int),
      .dBusAxi_arlen(dbus_axi_arlen_int),
      .dBusAxi_arsize(dbus_axi_arsize_o),
      .dBusAxi_arburst(dbus_axi_arburst_o),
      .dBusAxi_arlock(dbus_axi_arlock_o),
      .dBusAxi_arcache(dbus_axi_arcache_o),
      .dBusAxi_arqos(dbus_axi_arqos_o),
      .dBusAxi_arprot(),
      .dBusAxi_rvalid(dbus_axi_rvalid_i),
      .dBusAxi_rready(dbus_axi_rready_o),
      .dBusAxi_rdata(dbus_axi_rdata_i),
      .dBusAxi_rid(dbus_axi_rid_i),
      .dBusAxi_rresp(dbus_axi_rresp_i),
      .dBusAxi_rlast(dbus_axi_rlast_i),
      // Clock and Reset
      .clk(clk_i),
      .reset(cpu_reset)
  );



   assign cpu_reset = rst_i | arst_i;

   assign ibus_axi_awvalid_o = 1'b0;
   assign ibus_axi_awaddr_o = {AXI_ADDR_W{1'b0}};
   assign ibus_axi_awid_o = 1'b0;
   assign ibus_axi_awlen_o = {AXI_LEN_W{1'b0}};
   assign ibus_axi_awsize_o = {3{1'b0}};
   assign ibus_axi_awburst_o = {2{1'b0}};
   assign ibus_axi_awlock_o = 1'b0;
   assign ibus_axi_awcache_o = {4{1'b0}};
   assign ibus_axi_awqos_o = {4{1'b0}};
   assign ibus_axi_wvalid_o = 1'b0;
   assign ibus_axi_wdata_o = {AXI_DATA_W{1'b0}};
   assign ibus_axi_wstrb_o = {AXI_DATA_W / 8{1'b0}};
   assign ibus_axi_wlast_o = 1'b0;
   assign ibus_axi_bready_o = 1'b0;

   generate
      if (AXI_LEN_W < 8) begin : gen_if_less_than_8
         assign ibus_axi_arlen_o = ibus_axi_arlen_int[AXI_LEN_W-1:0];
         assign dbus_axi_arlen_o = dbus_axi_arlen_int[AXI_LEN_W-1:0];
         assign dbus_axi_awlen_o = dbus_axi_awlen_int[AXI_LEN_W-1:0];
      end else begin : gen_if_equal_8
         assign ibus_axi_arlen_o = ibus_axi_arlen_int;
         assign dbus_axi_arlen_o = dbus_axi_arlen_int;
         assign dbus_axi_awlen_o = dbus_axi_awlen_int;
      end
   endgenerate


        // Convert IOb to AXI lite for CLINT
        iob_iob2axil #(
        .AXIL_ADDR_W(16),
        .AXIL_DATA_W(AXI_DATA_W)
    ) clint_iob2axil (
            // iob_s port: Subordinate IOb interface
        .iob_valid_i(clint_iob_valid_i),
        .iob_addr_i(clint_iob_addr_i),
        .iob_wdata_i(clint_iob_wdata_i),
        .iob_wstrb_i(clint_iob_wstrb_i),
        .iob_rvalid_o(clint_iob_rvalid_o),
        .iob_rdata_o(clint_iob_rdata_o),
        .iob_ready_o(clint_iob_ready_o),
        // axil_m port: Manager AXI Lite interface
        .axil_araddr_o(clint_axil_araddr),
        .axil_arvalid_o(clint_axil_arvalid),
        .axil_arready_i(clint_axil_arready),
        .axil_rdata_i(clint_axil_rdata),
        .axil_rresp_i(clint_axil_rresp),
        .axil_rvalid_i(clint_axil_rvalid),
        .axil_rready_o(clint_axil_rready),
        .axil_awaddr_o(clint_axil_awaddr),
        .axil_awvalid_o(clint_axil_awvalid),
        .axil_awready_i(clint_axil_awready),
        .axil_wdata_o(clint_axil_wdata),
        .axil_wstrb_o(clint_axil_wstrb),
        .axil_wvalid_o(clint_axil_wvalid),
        .axil_wready_i(clint_axil_wready),
        .axil_bresp_i(clint_axil_bresp),
        .axil_bvalid_i(clint_axil_bvalid),
        .axil_bready_o(clint_axil_bready),
        // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i)
        );

            // Convert IOb to AXI lite for PLIC
        iob_iob2axil #(
        .AXIL_ADDR_W(22),
        .AXIL_DATA_W(AXI_DATA_W)
    ) plic_iob2axil (
            // iob_s port: Subordinate IOb interface
        .iob_valid_i(plic_iob_valid_i),
        .iob_addr_i(plic_iob_addr_i),
        .iob_wdata_i(plic_iob_wdata_i),
        .iob_wstrb_i(plic_iob_wstrb_i),
        .iob_rvalid_o(plic_iob_rvalid_o),
        .iob_rdata_o(plic_iob_rdata_o),
        .iob_ready_o(plic_iob_ready_o),
        // axil_m port: Manager AXI Lite interface
        .axil_araddr_o(plic_axil_araddr),
        .axil_arvalid_o(plic_axil_arvalid),
        .axil_arready_i(plic_axil_arready),
        .axil_rdata_i(plic_axil_rdata),
        .axil_rresp_i(plic_axil_rresp),
        .axil_rvalid_i(plic_axil_rvalid),
        .axil_rready_o(plic_axil_rready),
        .axil_awaddr_o(plic_axil_awaddr),
        .axil_awvalid_o(plic_axil_awvalid),
        .axil_awready_i(plic_axil_awready),
        .axil_wdata_o(plic_axil_wdata),
        .axil_wstrb_o(plic_axil_wstrb),
        .axil_wvalid_o(plic_axil_wvalid),
        .axil_wready_i(plic_axil_wready),
        .axil_bresp_i(plic_axil_bresp),
        .axil_bvalid_i(plic_axil_bvalid),
        .axil_bready_o(plic_axil_bready),
        // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i)
        );

    
endmodule
