// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps


`define CLK_PER 10

module iob_iob2axi_tb;

   parameter TEST_SZ = 1024;

   parameter ADDR_W = 24;
   parameter DATA_W = 32;

   parameter AXI_ADDR_W = ADDR_W;
   parameter AXI_DATA_W = DATA_W;

   // Clock
   reg clk = 1;
   always #(`CLK_PER / 2) clk = ~clk;

   // Reset
   reg                 rst = 0;

   //
   // DMA interface
   //

   // Control I/F
   reg                 run;
   reg                 direction;
   reg  [  ADDR_W-1:0] start_addr;
   wire                ready;
   wire                error;

   // Native subordinate I/F
   reg                 s_valid;
   reg  [  ADDR_W-1:0] s_addr;
   reg  [  DATA_W-1:0] s_wdata;
   reg  [DATA_W/8-1:0] s_wstrb;
   wire [  DATA_W-1:0] s_rdata;
   wire                s_ready;

   // AXI-4 full manager I/F
   `include "ddr_axi_wire.vs"

   // Iterators
   integer i, seq_ini;

   initial begin

`ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
`endif

      //
      // Init signals
      //
      run        = 0;
      start_addr = 0;
      direction  = 1;

      s_valid    = 0;
      s_addr     = 0;
      s_wdata    = 0;
      s_wstrb    = 0;

      //
      // Initialize memory
      //

      // Assert reset
      #100 rst = 1;

      // Deassert rst
      repeat (10) @(posedge clk) #1;
      rst = 0;

      // Wait an arbitray (10) number of cycles
      repeat (10) @(posedge clk) #1;

      //
      // Test starts here
      //

      // Write test

      direction  = 1;
      start_addr = 'h8000 - (10 * DATA_W / 8);

      run        = 1;
      @(posedge clk) #1;
      run     = 0;

      s_valid = 1;
      s_wstrb = 4'hf;

      // Number from which to start the incremental sequence to initialize the RAM
      seq_ini = 32;
      for (i = 0; i < TEST_SZ; i = i + 1) begin
         s_addr  = i;
         s_wdata = i + seq_ini;
         do @(posedge clk) #1; while (~s_ready);
      end
      s_valid = 0;

      repeat (20) @(posedge clk) #1;

      // Read test
      direction = 0;

      run       = 1;
      @(posedge clk) #1;
      run     = 0;

      s_valid = 1;
      s_wstrb = 4'h0;

      for (i = 0; i < TEST_SZ; i = i + 1) begin
         s_addr = i;
         do @(posedge clk) #1; while (~s_ready);

         if (s_rdata != i + seq_ini) begin
            $display("ERROR: Test failed! At position %d, data=%h and s_rdata=%h.", i, i + seq_ini,
                     s_rdata);
         end
      end
      s_valid = 0;

      while (~ready) @(posedge clk) #1;

      $display("INFO: Test completed successfully!");

      repeat (10) @(posedge clk) #1;

      $finish();
   end

   iob_iob2axi #(
      .ADDR_W(ADDR_W),
      .DATA_W(DATA_W)
   ) uut (
      .clk_i(clk),
      .rst_i(rst),

      //
      // Control I/F
      //
      .run_i      (run),
      .direction_i(direction),
      .addr_i     (start_addr),
      .ready_o    (ready),
      .error_o    (error),

      //
      // AXI-4 full manager I/F
      //
      `include "m_ddr_axi_portmap.vs"

      //
      // Native subordinate I/F
      //
      .s_valid_i(s_valid),
      .s_addr_i (s_addr),
      .s_wdata_i(s_wdata),
      .s_wstrb_i(s_wstrb),
      .s_rdata_o(s_rdata),
      .s_ready_o(s_ready)
   );


   // axi_ram_mem
   wire          ext_mem_clk;
   wire [32-1:0] ext_mem_r_data;
   wire          ext_mem_r_en;
   wire [32-1:0] ext_mem_r_addr;
   wire [32-1:0] ext_mem_w_data;
   wire [ 4-1:0] ext_mem_w_strb;
   wire [32-1:0] ext_mem_w_addr;

   iob_axi_ram #(
      .ID_WIDTH  (`AXI_ID_W),
      .DATA_WIDTH(AXI_DATA_W),
      .ADDR_WIDTH(AXI_ADDR_W)
   ) iob_axi_ram0 (
      .clk_i(clk),
      .rst_i(rst),

      //
      // AXI-4 full manager interface
      //

      // Address write
      .axi_awid_i   (ddr_axi_awid),
      .axi_awaddr_i (ddr_axi_awaddr),
      .axi_awlen_i  (ddr_axi_awlen),
      .axi_awsize_i (ddr_axi_awsize),
      .axi_awburst_i(ddr_axi_awburst),
      .axi_awlock_i (ddr_axi_awlock),
      .axi_awprot_i (ddr_axi_awprot),
      .axi_awqos_i  (ddr_axi_awqos),
      .axi_awcache_i(ddr_axi_awcache),
      .axi_awvalid_i(ddr_axi_awvalid),
      .axi_awready_o(ddr_axi_awready),

      // Write
      .axi_wvalid_i(ddr_axi_wvalid),
      .axi_wdata_i (ddr_axi_wdata),
      .axi_wstrb_i (ddr_axi_wstrb),
      .axi_wlast_i (ddr_axi_wlast),
      .axi_wready_o(ddr_axi_wready),

      // Write response
      .axi_bid_o   (ddr_axi_bid),
      .axi_bvalid_o(ddr_axi_bvalid),
      .axi_bresp_o (ddr_axi_bresp),
      .axi_bready_i(ddr_axi_bready),

      // Address read
      .axi_arid_i   (ddr_axi_arid),
      .axi_araddr_i (ddr_axi_araddr),
      .axi_arlen_i  (ddr_axi_arlen),
      .axi_arsize_i (ddr_axi_arsize),
      .axi_arburst_i(ddr_axi_arburst),
      .axi_arlock_i (ddr_axi_arlock),
      .axi_arcache_i(ddr_axi_arcache),
      .axi_arprot_i (ddr_axi_arprot),
      .axi_arqos_i  (ddr_axi_arqos),
      .axi_arvalid_i(ddr_axi_arvalid),
      .axi_arready_o(ddr_axi_arready),

      // Read
      .axi_rid_o   (ddr_axi_rid),
      .axi_rvalid_o(ddr_axi_rvalid),
      .axi_rdata_o (ddr_axi_rdata),
      .axi_rlast_o (ddr_axi_rlast),
      .axi_rresp_o (ddr_axi_rresp),
      .axi_rready_i(ddr_axi_rready),


      // external_mem_bus_m port
      .ext_mem_clk_o   (ext_mem_clk),
      .ext_mem_r_data_i(ext_mem_r_data),
      .ext_mem_r_en_o  (ext_mem_r_en),
      .ext_mem_r_addr_o(ext_mem_r_addr),
      .ext_mem_w_data_o(ext_mem_w_data),
      .ext_mem_w_strb_o(ext_mem_w_strb),
      .ext_mem_w_addr_o(ext_mem_w_addr)
   );

   // Memory for iob_axi_ram
   iob_ram_t2p_be #(
      .ADDR_W(ADDR_W - 2),
      .DATA_W(DATA_W)
   ) iob_ram_t2p_be_inst (
      // ram_t2p_be_s port
      .clk_i   (ext_mem_clk),
      .r_data_o(ext_mem_r_data),
      .r_en_i  (ext_mem_r_en),
      .r_addr_i(ext_mem_r_addr),
      .w_data_i(ext_mem_w_data),
      .w_strb_i(ext_mem_w_strb),
      .w_addr_i(ext_mem_w_addr)
   );

endmodule
