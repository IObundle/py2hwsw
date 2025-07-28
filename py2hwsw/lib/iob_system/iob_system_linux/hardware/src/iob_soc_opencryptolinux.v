`timescale 1 ns / 1 ps

`include "bsp.vh"
`include "iob_soc_opencryptolinux_conf.vh"
`include "iob_utils.vh"

`include "iob_soc_opencryptolinux_periphs_swreg_def.vs"

module iob_soc_opencryptolinux #(
    `include "iob_soc_opencryptolinux_params.vs"
) (
    `include "iob_soc_opencryptolinux_io.vs"
);

  localparam integer Bbit = `IOB_SOC_OPENCRYPTOLINUX_B;
  localparam integer AddrMsb = `REQ_W - 2;

  localparam IBUS_AXI_ID_W = 1;
  localparam IBUS_AXI_LEN_W = 8;
  localparam IBUS_AXI_ADDR_W = 32;
  localparam IBUS_AXI_DATA_W = 32;
  localparam DBUS_AXI_ID_W = 1;
  localparam DBUS_AXI_LEN_W = 8;
  localparam DBUS_AXI_ADDR_W = 32;
  localparam DBUS_AXI_DATA_W = 32;
  localparam PERIPHERAL_AXI_ID_W = 1;
  localparam PERIPHERAL_AXI_LEN_W = 8;
  localparam PERIPHERAL_AXI_ADDR_W = 32;
  localparam PERIPHERAL_AXI_DATA_W = 32;
  localparam INTMEM_AXI_ID_W = 1;
  localparam INTMEM_AXI_LEN_W = 8;
  localparam INTMEM_AXI_ADDR_W = 32;
  localparam INTMEM_AXI_DATA_W = 32;

  localparam N_SLAVES = `IOB_SOC_OPENCRYPTOLINUX_N_SLAVES;  // peripherals (includes internal BOOT_CTR, PLIC and CLINT)


  `include "iob_soc_opencryptolinux_pwires.vs"


  wire peripheral_iob_valid;
  wire [ADDR_W-1:0] peripheral_iob_addr;
  wire [DATA_W-1:0] peripheral_iob_wdata;
  wire [DATA_W/8-1:0] peripheral_iob_wstrb;
  wire peripheral_iob_rvalid;
  wire [DATA_W-1:0] peripheral_iob_rdata;
  wire peripheral_iob_ready;

  //slaves bus (includes internal memory + periphrals)
  wire [(N_SLAVES)*`REQ_W-1:0] slaves_req;
  wire [(N_SLAVES)*`RESP_W-1:0] slaves_resp;

  //
  // SYSTEM RESET
  //

  wire boot;
  wire cpu_reset;

  // Axi instruction bus
  `include "iBus_axi_wire.vs"
  // Axi data bus
  `include "dBus_axi_wire.vs"
  // Internal memmory AXI bus
  `include "intmem_axi_wire.vs"
  // Periphrals AXI bus
  `include "peripheral_axi_wire.vs"

  wire [ADDR_W-1:0] extmem_axi_awaddr;
  wire [ADDR_W-1:0] extmem_axi_araddr;
  wire [7:0] extmem_axi_awlen;
  wire [7:0] extmem_axi_arlen;

  assign axi_awlock_o[1] = 1'b0;
  assign axi_arlock_o[1] = 1'b0;
  assign axi_awlen_o[AXI_LEN_W-1:0] = extmem_axi_awlen[AXI_LEN_W-1:0];
  assign axi_arlen_o[AXI_LEN_W-1:0] = extmem_axi_arlen[AXI_LEN_W-1:0];
  generate
    if (AXI_ID_W != 1) begin : g_fill_ID_signal
      assign axi_awid_o[AXI_ID_W-1:1] = {(AXI_ID_W - 1) {1'b0}};
      assign axi_arid_o[AXI_ID_W-1:1] = {(AXI_ID_W - 1) {1'b0}};
    end
  endgenerate
  assign axi_awaddr_o[AXI_ADDR_W-1:0] = extmem_axi_awaddr[MEM_ADDR_W-1:0] + MEM_ADDR_OFFSET;
  assign axi_araddr_o[AXI_ADDR_W-1:0] = extmem_axi_araddr[MEM_ADDR_W-1:0] + MEM_ADDR_OFFSET;

  assign peripheral_axi_bid = {PERIPHERAL_AXI_ID_W{1'b0}};
  assign peripheral_axi_rid = {PERIPHERAL_AXI_ID_W{1'b0}};
  assign peripheral_axi_rlast = 1'b1;

  assign cpu_trap_o = 1'b0;

  //
  //  CPU
  //
  iob_VexRiscv #(
      .ADDR_W    (ADDR_W),
      .DATA_W    (DATA_W),
      .USE_EXTMEM(1)
  ) cpu_0 (
      .clk_i         (clk_i),
      .cke_i         (cke_i),
      .arst_i        (arst_i),
      .cpu_reset_i   (cpu_reset),
      // PLIC and CLINT are the last peripherals
      .clint_req     (slaves_req[(N_SLAVES-2)*`REQ_W+:`REQ_W]),
      .clint_resp    (slaves_resp[(N_SLAVES-2)*`RESP_W+:`RESP_W]),
      .plic_req      (slaves_req[(N_SLAVES-1)*`REQ_W+:`REQ_W]),
      .plic_resp     (slaves_resp[(N_SLAVES-1)*`RESP_W+:`RESP_W]),
      .plicInterrupts({{30{1'b0}}, uart_interrupt_o, 1'b0}),
      // Axi instruction bus
      `include "iBus_axi_m_portmap.vs"
      // Axi data bus
      `include "dBus_axi_m_portmap.vs"
      .boot_i        (boot)
  );

  //
  // AXI interconnect {I, D} -> {peripheral, internal, external}
  //
  axi_interconnect #(
      .ID_WIDTH  (1),
      .DATA_WIDTH(DATA_W),
      .ADDR_WIDTH(ADDR_W),
      .M_ADDR_WIDTH({{32'd30}, {32'd30}, {32'd31}}),
      .S_COUNT   (2),
      .M_COUNT   (3)
  ) dBus_axi_interconnect (
      .clk(clk_i),
      .rst(arst_i),

      .s_axi_awid({iBus_axi_awid, dBus_axi_awid}),
      .s_axi_awaddr({iBus_axi_awaddr, dBus_axi_awaddr}),
      .s_axi_awlen({iBus_axi_awlen, dBus_axi_awlen}),
      .s_axi_awsize({iBus_axi_awsize, dBus_axi_awsize}),
      .s_axi_awburst({iBus_axi_awburst, dBus_axi_awburst}),
      .s_axi_awlock({iBus_axi_awlock[0], dBus_axi_awlock[0]}),
      .s_axi_awcache({iBus_axi_awcache, dBus_axi_awcache}),
      .s_axi_awprot({iBus_axi_awprot, dBus_axi_awprot}),
      .s_axi_awqos({iBus_axi_awqos, dBus_axi_awqos}),
      .s_axi_awvalid({iBus_axi_awvalid, dBus_axi_awvalid}),
      .s_axi_awready({iBus_axi_awready, dBus_axi_awready}),
      .s_axi_wdata({iBus_axi_wdata, dBus_axi_wdata}),
      .s_axi_wstrb({iBus_axi_wstrb, dBus_axi_wstrb}),
      .s_axi_wlast({iBus_axi_wlast, dBus_axi_wlast}),
      .s_axi_wvalid({iBus_axi_wvalid, dBus_axi_wvalid}),
      .s_axi_wready({iBus_axi_wready, dBus_axi_wready}),
      .s_axi_bid({iBus_axi_bid, dBus_axi_bid}),
      .s_axi_bresp({iBus_axi_bresp, dBus_axi_bresp}),
      .s_axi_bvalid({iBus_axi_bvalid, dBus_axi_bvalid}),
      .s_axi_bready({iBus_axi_bready, dBus_axi_bready}),
      .s_axi_arid({iBus_axi_arid, dBus_axi_arid}),
      .s_axi_araddr({iBus_axi_araddr, dBus_axi_araddr}),
      .s_axi_arlen({iBus_axi_arlen, dBus_axi_arlen}),
      .s_axi_arsize({iBus_axi_arsize, dBus_axi_arsize}),
      .s_axi_arburst({iBus_axi_arburst, dBus_axi_arburst}),
      .s_axi_arlock({iBus_axi_arlock[0], dBus_axi_arlock[0]}),
      .s_axi_arcache({iBus_axi_arcache, dBus_axi_arcache}),
      .s_axi_arprot({iBus_axi_arprot, dBus_axi_arprot}),
      .s_axi_arqos({iBus_axi_arqos, dBus_axi_arqos}),
      .s_axi_arvalid({iBus_axi_arvalid, dBus_axi_arvalid}),
      .s_axi_arready({iBus_axi_arready, dBus_axi_arready}),
      .s_axi_rid({iBus_axi_rid, dBus_axi_rid}),
      .s_axi_rdata({iBus_axi_rdata, dBus_axi_rdata}),
      .s_axi_rresp({iBus_axi_rresp, dBus_axi_rresp}),
      .s_axi_rlast({iBus_axi_rlast, dBus_axi_rlast}),
      .s_axi_rvalid({iBus_axi_rvalid, dBus_axi_rvalid}),
      .s_axi_rready({iBus_axi_rready, dBus_axi_rready}),

      .m_axi_awid({peripheral_axi_awid, intmem_axi_awid, axi_awid_o[0]}),
      .m_axi_awaddr({peripheral_axi_awaddr, intmem_axi_awaddr, extmem_axi_awaddr}),
      .m_axi_awlen({peripheral_axi_awlen, intmem_axi_awlen, extmem_axi_awlen}),
      .m_axi_awsize({peripheral_axi_awsize, intmem_axi_awsize, axi_awsize_o[3-1:0]}),
      .m_axi_awburst({peripheral_axi_awburst, intmem_axi_awburst, axi_awburst_o[2-1:0]}),
      .m_axi_awlock({peripheral_axi_awlock[0], intmem_axi_awlock[0], axi_awlock_o[0]}),
      .m_axi_awcache({peripheral_axi_awcache, intmem_axi_awcache, axi_awcache_o[4-1:0]}),
      .m_axi_awprot({peripheral_axi_awprot, intmem_axi_awprot, axi_awprot_o[3-1:0]}),
      .m_axi_awqos({peripheral_axi_awqos, intmem_axi_awqos, axi_awqos_o[4-1:0]}),
      .m_axi_awvalid({peripheral_axi_awvalid, intmem_axi_awvalid, axi_awvalid_o[0+:1]}),
      .m_axi_awready({peripheral_axi_awready, intmem_axi_awready, axi_awready_i[0+:1]}),
      .m_axi_wdata({peripheral_axi_wdata, intmem_axi_wdata, axi_wdata_o[AXI_DATA_W-1:0]}),
      .m_axi_wstrb({peripheral_axi_wstrb, intmem_axi_wstrb, axi_wstrb_o[(AXI_DATA_W/8)-1:0]}),
      .m_axi_wlast({peripheral_axi_wlast, intmem_axi_wlast, axi_wlast_o[0+:1]}),
      .m_axi_wvalid({peripheral_axi_wvalid, intmem_axi_wvalid, axi_wvalid_o[0+:1]}),
      .m_axi_wready({peripheral_axi_wready, intmem_axi_wready, axi_wready_i[0+:1]}),
      .m_axi_bid({peripheral_axi_bid, intmem_axi_bid, axi_bid_i[0]}),
      .m_axi_bresp({peripheral_axi_bresp, intmem_axi_bresp, axi_bresp_i[2-1:0]}),
      .m_axi_bvalid({peripheral_axi_bvalid, intmem_axi_bvalid, axi_bvalid_i[0+:1]}),
      .m_axi_bready({peripheral_axi_bready, intmem_axi_bready, axi_bready_o[0+:1]}),
      .m_axi_arid({peripheral_axi_arid, intmem_axi_arid, axi_arid_o[0]}),
      .m_axi_araddr({peripheral_axi_araddr, intmem_axi_araddr, extmem_axi_araddr}),
      .m_axi_arlen({peripheral_axi_arlen, intmem_axi_arlen, extmem_axi_arlen}),
      .m_axi_arsize({peripheral_axi_arsize, intmem_axi_arsize, axi_arsize_o[3-1:0]}),
      .m_axi_arburst({peripheral_axi_arburst, intmem_axi_arburst, axi_arburst_o[2-1:0]}),
      .m_axi_arlock({peripheral_axi_arlock[0], intmem_axi_arlock[0], axi_arlock_o[0]}),
      .m_axi_arcache({peripheral_axi_arcache, intmem_axi_arcache, axi_arcache_o[4-1:0]}),
      .m_axi_arprot({peripheral_axi_arprot, intmem_axi_arprot, axi_arprot_o[3-1:0]}),
      .m_axi_arqos({peripheral_axi_arqos, intmem_axi_arqos, axi_arqos_o[4-1:0]}),
      .m_axi_arvalid({peripheral_axi_arvalid, intmem_axi_arvalid, axi_arvalid_o[0+:1]}),
      .m_axi_arready({peripheral_axi_arready, intmem_axi_arready, axi_arready_i[0+:1]}),
      .m_axi_rid({peripheral_axi_rid, intmem_axi_rid, axi_rid_i[0]}),
      .m_axi_rdata({peripheral_axi_rdata, intmem_axi_rdata, axi_rdata_i[AXI_DATA_W-1:0]}),
      .m_axi_rresp({peripheral_axi_rresp, intmem_axi_rresp, axi_rresp_i[2-1:0]}),
      .m_axi_rlast({peripheral_axi_rlast, intmem_axi_rlast, axi_rlast_i[0+:1]}),
      .m_axi_rvalid({peripheral_axi_rvalid, intmem_axi_rvalid, axi_rvalid_i[0+:1]}),
      .m_axi_rready({peripheral_axi_rready, intmem_axi_rready, axi_rready_o[0+:1]}),

      //optional signals
      .s_axi_awuser(2'b00),
      .s_axi_wuser (2'b00),
      .s_axi_aruser(2'b00),
      .m_axi_buser (3'b000),
      .m_axi_ruser (3'b000)
  );


  //
  // INTERNAL SRAM MEMORY
  //
  axi_ram #(
      .DATA_WIDTH(DATA_W),
      .ADDR_WIDTH(BOOTROM_ADDR_W),
      .ID_WIDTH(INTMEM_AXI_ID_W),
`ifdef IOB_MEM_NO_READ_ON_WRITE
      .READ_ON_WRITE(0),
`else
      .READ_ON_WRITE(1),
`endif
      .PIPELINE_OUTPUT(2),
      .FILE("iob_soc_opencryptolinux_boot")
  ) boot_ram (
      .clk_i(clk_i),
      .rst_i(arst_i),

      .axi_awid_i(intmem_axi_awid),
      .axi_awaddr_i(intmem_axi_awaddr[BOOTROM_ADDR_W-1:0]),
      .axi_awlen_i(intmem_axi_awlen),
      .axi_awsize_i(intmem_axi_awsize),
      .axi_awburst_i(intmem_axi_awburst),
      .axi_awlock_i(intmem_axi_awlock),
      .axi_awcache_i(intmem_axi_awcache),
      .axi_awprot_i(intmem_axi_awprot),
      .axi_awqos_i(intmem_axi_awqos),
      .axi_awvalid_i(intmem_axi_awvalid),
      .axi_awready_o(intmem_axi_awready),
      .axi_wdata_i(intmem_axi_wdata),
      .axi_wstrb_i(intmem_axi_wstrb),
      .axi_wlast_i(intmem_axi_wlast),
      .axi_wvalid_i(intmem_axi_wvalid),
      .axi_wready_o(intmem_axi_wready),
      .axi_bid_o(intmem_axi_bid),
      .axi_bresp_o(intmem_axi_bresp),
      .axi_bvalid_o(intmem_axi_bvalid),
      .axi_bready_i(intmem_axi_bready),
      .axi_arid_i(intmem_axi_arid),
      .axi_araddr_i(intmem_axi_araddr[BOOTROM_ADDR_W-1:0]),
      .axi_arlen_i(intmem_axi_arlen),
      .axi_arsize_i(intmem_axi_arsize),
      .axi_arburst_i(intmem_axi_arburst),
      .axi_arlock_i(intmem_axi_arlock),
      .axi_arcache_i(intmem_axi_arcache),
      .axi_arprot_i(intmem_axi_arprot),
      .axi_arqos_i(intmem_axi_arqos),
      .axi_arvalid_i(intmem_axi_arvalid),
      .axi_arready_o(intmem_axi_arready),
      .axi_rid_o(intmem_axi_rid),
      .axi_rdata_o(intmem_axi_rdata),
      .axi_rresp_o(intmem_axi_rresp),
      .axi_rlast_o(intmem_axi_rlast),
      .axi_rvalid_o(intmem_axi_rvalid),
      .axi_rready_i(intmem_axi_rready)
  );

  //
  // Peripheral interface AXIL to IOb-bus
  //
  axil2iob #(
      .AXIL_ADDR_W(ADDR_W),
      .AXIL_DATA_W(DATA_W)
  ) peripheral_axil2iob (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      // AXI4 Lite slave interface
      .axil_awaddr_i(peripheral_axi_awaddr),
      .axil_awprot_i(peripheral_axi_awprot),
      .axil_awvalid_i(peripheral_axi_awvalid),
      .axil_awready_o(peripheral_axi_awready),
      .axil_wdata_i(peripheral_axi_wdata),
      .axil_wstrb_i(peripheral_axi_wstrb),
      .axil_wvalid_i(peripheral_axi_wvalid),
      .axil_wready_o(peripheral_axi_wready),
      .axil_bresp_o(peripheral_axi_bresp),
      .axil_bvalid_o(peripheral_axi_bvalid),
      .axil_bready_i(peripheral_axi_bready),
      .axil_araddr_i(peripheral_axi_araddr),
      .axil_arprot_i(peripheral_axi_arprot),
      .axil_arvalid_i(peripheral_axi_arvalid),
      .axil_arready_o(peripheral_axi_arready),
      .axil_rdata_o(peripheral_axi_rdata),
      .axil_rresp_o(peripheral_axi_rresp),
      .axil_rvalid_o(peripheral_axi_rvalid),
      .axil_rready_i(peripheral_axi_rready),
      // IOb-bus signals
      .iob_valid_o(peripheral_iob_valid),
      .iob_addr_o(peripheral_iob_addr),
      .iob_wdata_o(peripheral_iob_wdata),
      .iob_wstrb_o(peripheral_iob_wstrb),
      .iob_rvalid_i(peripheral_iob_rvalid),
      .iob_rdata_i(peripheral_iob_rdata),
      .iob_ready_i(peripheral_iob_ready)
  );

  iob_split #(
      .ADDR_W  (ADDR_W),
      .DATA_W  (DATA_W),
      .N_SLAVES(N_SLAVES),
      .P_SLAVES(AddrMsb - 4)
  ) pbus_split (
      .clk_i(clk_i),
      .arst_i(arst_i),
      // master interface
      .m_req_i({
        peripheral_iob_valid, peripheral_iob_addr, peripheral_iob_wdata, peripheral_iob_wstrb
      }),
      .m_resp_o({peripheral_iob_rdata, peripheral_iob_rvalid, peripheral_iob_ready}),
      // slaves interface
      .s_req_o(slaves_req),
      .s_resp_i(slaves_resp)
  );



  iob_soc_opencryptolinux_boot_ctr #(
      .DATA_W(UART0_DATA_W),
      .ADDR_W(UART0_ADDR_W)
  ) boot_ctr (
      .boot(boot),
      .cpu_reset(cpu_reset),
      .iob_valid_i(slaves_req[`VALID(0)]),
      .iob_addr_i(slaves_req[`ADDRESS(0, `IOB_UART16550_SWREG_ADDR_W)]),
      .iob_wdata_i(slaves_req[`WDATA(0)]),
      .iob_wstrb_i(slaves_req[`WSTRB(0)]),
      .iob_rvalid_o(slaves_resp[`RVALID(0)]),
      .iob_rdata_o(slaves_resp[`RDATA(0)]),
      .iob_ready_o(slaves_resp[`READY(0)]),
      .clk_i(clk_i),
      .arst_i(arst_i),
      .cke_i(cke_i)
  );

  `include "iob_soc_opencryptolinux_periphs_inst.vs"

endmodule
