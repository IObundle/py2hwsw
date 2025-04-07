// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

`include "iob_axistream_in_csrs_def.vh"
`include "iob_axistream_in_conf.vh"
`include "iob_axistream_out_csrs_def.vh"
`include "iob_axistream_out_conf.vh"


`define IOB_NBYTES (DATA_W/8)
`define IOB_GET_NBYTES(WIDTH) (WIDTH/8 + |(WIDTH%8))
`define IOB_NBYTES_W $clog2(`IOB_NBYTES)
`define IOB_WORD_ADDR(ADDR) ((ADDR>>`IOB_NBYTES_W)<<`IOB_NBYTES_W)

`define IOB_BYTE_OFFSET(ADDR) (ADDR%(32/8))

`define IOB_GET_WDATA(ADDR, DATA) (DATA<<(8*`IOB_BYTE_OFFSET(ADDR)))
`define IOB_GET_WSTRB(ADDR, WIDTH) (((1<<`IOB_GET_NBYTES(WIDTH))-1)<<`IOB_BYTE_OFFSET(ADDR))
`define IOB_GET_RDATA(ADDR, DATA, WIDTH) ((DATA>>(8*`IOB_BYTE_OFFSET(ADDR)))&((1<<WIDTH)-1))

`define IOB_RESET(CLK, RESET, PRE, DURATION, POST) RESET=0;\
   #PRE RESET=1; #DURATION RESET=0; #POST;\
   @(posedge CLK) #1;


module iob_axis2axi_tb;

   localparam PER = 10;
   localparam DATA_W = 32;
   localparam ADDR_W = 14;
   localparam AXI_LEN_W = 8;
   localparam RLEN_W = 12;
   localparam WLEN_W = 12;
   localparam AXIS_FIFO_ADDR_W = 10;
   localparam NWORDS = 256;
   localparam START_ADDR = 4000; // cross 4kB boundary

   // Change this parameters to add a delay, either to the AXI stream or to the AXI connection (0 is valid and will not add any delay)
   parameter DELAY_AXIS_IN = 3;
   parameter DELAY_AXIS_OUT = 3;
   parameter DELAY_AXI_READ = 5;
   parameter DELAY_AXI_WRITE = 5;

   integer fd;

   reg     clk;
   initial clk = 0;
   always #(PER / 2) clk = ~clk;

   reg cke;
   reg arst;
   reg rst;

   reg [DATA_W-1:0] word;
   integer failed = 0;
   integer i;

   // axi_ram_mem
   wire axi_ram_ext_mem_clk;
   wire [DATA_W-1:0] axi_ram_ext_mem_r_data;
   wire axi_ram_ext_mem_r_en;
   wire [(ADDR_W-2)-1:0] axi_ram_ext_mem_r_addr;
   wire [DATA_W-1:0] axi_ram_ext_mem_w_data;
   wire [(DATA_W/8)-1:0] axi_ram_ext_mem_w_strb;
   wire [(ADDR_W-2)-1:0] axi_ram_ext_mem_w_addr;

   // AXI-4 full master I/F
   wire ram_axi_awid;  //Address write channel ID
   wire [ADDR_W-1:0] ram_axi_awaddr;  //Address write channel address
   wire [8-1:0] ram_axi_awlen;  //Address write channel burst length
   wire [3-1:0] ram_axi_awsize
       ;  //Address write channel burst size. This signal indicates the size of each transfer in the burst
   wire [2-1:0] ram_axi_awburst;  //Address write channel burst type
   wire [2-1:0] ram_axi_awlock;  //Address write channel lock type
   wire [4-1:0] ram_axi_awcache
       ;  //Address write channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).
   wire [4-1:0] ram_axi_awqos;  //Address write channel quality of service
   wire ram_axi_awvalid;  //Address write channel valid
   wire ram_axi_awready;  //Address write channel ready
   wire ram_axi_wid;  //Write channel ID
   wire [DATA_W-1:0] ram_axi_wdata;  //Write channel data
   wire [(DATA_W/8)-1:0] ram_axi_wstrb;  //Write channel write strobe
   wire ram_axi_wvalid;  //Write channel write valid
   wire ram_axi_wready;  //Write channel write ready
   wire ram_axi_wlast;  //Write channel last word flag
   wire ram_axi_bid;  //Write response channel ID
   wire [2-1:0] ram_axi_bresp;  //Write response channel response
   wire ram_axi_bvalid;  //Write response channel valid
   wire ram_axi_bready;  //Write response channel ready
   wire ram_axi_arid;  //Address read channel ID
   wire [ADDR_W-1:0] ram_axi_araddr;  //Address read channel address
   wire [8-1:0] ram_axi_arlen;  //Address read channel burst length
   wire [3-1:0] ram_axi_arsize
       ;  //Address read channel burst size. This signal indicates the size of each transfer in the burst
   wire [2-1:0] ram_axi_arburst;  //Address read channel burst type
   wire [2-1:0] ram_axi_arlock;  //Address read channel lock type
   wire [4-1:0] ram_axi_arcache
       ;  //Address read channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).
   wire [4-1:0] ram_axi_arqos;  //Address read channel quality of service
   wire ram_axi_arvalid;  //Address read channel valid
   wire ram_axi_arready;  //Address read channel ready
   wire ram_axi_rid;  //Read channel ID
   wire [DATA_W-1:0] ram_axi_rdata;  //Read channel data
   wire [2-1:0] ram_axi_rresp;  //Read channel response
   wire ram_axi_rvalid;  //Read channel read valid
   wire ram_axi_rready;  //Read channel read ready
   wire ram_axi_rlast;  //Read channel last word

   // AXIS OUT -> AXIS IN connection
   wire [DATA_W-1:0] axis_tdata;
   wire axis_tvalid;
   wire axis_tready;
   wire axis_tlast;

   // AXIS2AXI -> AXIS OUT connection
   wire [DATA_W-1:0] axis2axi_axis_out_tdata;
   wire axis2axi_axis_out_tvalid;
   wire axis2axi_axis_out_tready;

   // AXIS IN -> AXIS2AXI connection
   wire [DATA_W-1:0] axis2axi_axis_in_tdata;
   wire axis2axi_axis_in_tvalid;
   wire axis2axi_axis_in_tready;

   // Config Write 
   reg [ADDR_W-1:0] w_addr;
   reg [WLEN_W-1:0] w_length;
   reg w_start_transfer;
   reg [(AXI_LEN_W+1)-1:0] w_max_len;
   wire [WLEN_W-1:0] w_remaining_data;
   wire w_busy;

   // Config Write 
   reg [ADDR_W-1:0] r_addr;
   reg [RLEN_W-1:0] r_length;
   reg r_start_transfer;
   reg [(AXI_LEN_W+1)-1:0] r_max_len;
   wire [RLEN_W-1:0] r_remaining_data;
   wire r_busy;

   // AXIS IN IOb
   reg axis_in_iob_valid;
   reg [DATA_W-1:0] axis_in_iob_wdata;
   reg [`IOB_AXISTREAM_IN_CSRS_ADDR_W-1:0] axis_in_iob_addr;
   reg [(DATA_W/8)-1:0] axis_in_iob_wstrb;
   wire axis_in_iob_rvalid;
   wire [DATA_W-1:0] axis_in_iob_rdata;
   reg axis_in_iob_rready;
   wire axis_in_iob_ready;

   // AXIS OUT IOb
   reg axis_out_iob_valid;
   reg [DATA_W-1:0] axis_out_iob_wdata;
   reg [`IOB_AXISTREAM_OUT_CSRS_ADDR_W-1:0] axis_out_iob_addr;
   reg [(DATA_W/8)-1:0] axis_out_iob_wstrb;
   wire axis_out_iob_rvalid;
   wire [DATA_W-1:0] axis_out_iob_rdata;
   reg axis_out_iob_rready;
   wire axis_out_iob_ready;

   initial begin
`ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
`endif

      //apply async reset
      `IOB_RESET(clk, arst, 23, 17, 13);

      cke          = 1;
      rst          = 1;
      // deassert soft reset
      @(posedge clk) #1 rst = 0;

      $display("AXIS2AXI TEST!");

      $display("Configure AXIStream IN");
      axis_in_iob_write(`IOB_AXISTREAM_IN_SOFT_RESET_ADDR, 1, `IOB_AXISTREAM_IN_SOFT_RESET_W);
      // wait for reset to propagate to axis domain
      @(posedge clk);
      @(posedge clk);
      axis_in_iob_write(`IOB_AXISTREAM_IN_SOFT_RESET_ADDR, 0, `IOB_AXISTREAM_IN_SOFT_RESET_W);
      axis_in_iob_write(`IOB_AXISTREAM_IN_MODE_ADDR, 1, `IOB_AXISTREAM_IN_MODE_W);
      axis_in_iob_write(`IOB_AXISTREAM_IN_ENABLE_ADDR, 1, `IOB_AXISTREAM_IN_ENABLE_W);

      $display("Configure AXIStream OUT");
      axis_out_iob_write(`IOB_AXISTREAM_OUT_SOFT_RESET_ADDR, 1, `IOB_AXISTREAM_OUT_SOFT_RESET_W);
      // wait for reset to propagate to axis domain
      @(posedge clk);
      @(posedge clk);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_SOFT_RESET_ADDR, 0, `IOB_AXISTREAM_OUT_SOFT_RESET_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_MODE_ADDR, 0, `IOB_AXISTREAM_OUT_MODE_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_NWORDS_ADDR, NWORDS, `IOB_AXISTREAM_OUT_NWORDS_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_ENABLE_ADDR, 1, `IOB_AXISTREAM_OUT_ENABLE_W);

      $display("Write data to AXIStream OUT -> AXIStream IN");

      // write data loop
      for (i = 0; i < NWORDS; i = i + 1) begin
         axis_out_iob_write(`IOB_AXISTREAM_OUT_DATA_ADDR, i, `IOB_AXISTREAM_OUT_DATA_W);
      end

      $display("Configure AXIS2AXI: write operation AXIStream IN -> AXIS2AXI -> AXI RAM");
      w_addr = START_ADDR;
      w_length = NWORDS;
      w_max_len = NWORDS;
      w_start_transfer = 1;
      @(posedge clk) #1 w_start_transfer = 0;

      // wait for write operation to complete
      while(w_busy) begin
         @(posedge clk);
      end

      $display("Reset and reconfigure AXIStream IN / OUT");
      axis_in_iob_write(`IOB_AXISTREAM_IN_SOFT_RESET_ADDR, 1, `IOB_AXISTREAM_IN_SOFT_RESET_W);
      // wait for reset to propagate to axis domain
      @(posedge clk);
      @(posedge clk);
      axis_in_iob_write(`IOB_AXISTREAM_IN_SOFT_RESET_ADDR, 0, `IOB_AXISTREAM_IN_SOFT_RESET_W);
      axis_in_iob_write(`IOB_AXISTREAM_IN_MODE_ADDR, 0, `IOB_AXISTREAM_IN_MODE_W);
      axis_in_iob_write(`IOB_AXISTREAM_IN_ENABLE_ADDR, 1, `IOB_AXISTREAM_IN_ENABLE_W);

      axis_out_iob_write(`IOB_AXISTREAM_OUT_SOFT_RESET_ADDR, 1, `IOB_AXISTREAM_OUT_SOFT_RESET_W);
      // wait for reset to propagate to axis domain
      @(posedge clk);
      @(posedge clk);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_SOFT_RESET_ADDR, 0, `IOB_AXISTREAM_OUT_SOFT_RESET_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_MODE_ADDR, 1, `IOB_AXISTREAM_OUT_MODE_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_NWORDS_ADDR, NWORDS, `IOB_AXISTREAM_OUT_NWORDS_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_ENABLE_ADDR, 1, `IOB_AXISTREAM_OUT_ENABLE_W);

      $display("Configure AXIS2AXI: read operation AXIStream OUT <- AXIS2AXI <- AXI RAM");
      r_addr = START_ADDR;
      r_length = NWORDS;
      r_max_len = NWORDS;
      r_start_transfer = 1;
      @(posedge clk) #1 r_start_transfer = 0;

      // wait for write operation to complete
      while(r_busy) begin
         @(posedge clk);
      end

      $display("Read data from AXIStream IN");
      // read data loop
      for (i = 0; i < NWORDS; i = i + 1) begin
         axis_in_iob_read(`IOB_AXISTREAM_IN_DATA_ADDR, word, `IOB_AXISTREAM_IN_DATA_W);

         //check data
         if (word != i) begin
            $display("Error: expected %d, got %d", i, word);
            failed = failed + 1;
         end
      end

      $display("%c[1;34m", 27);
      $display("%c[0m", 27);
      fd = $fopen("test.log", "w");

      if (failed == 0) begin
         $display("All tests passed");
         $fdisplay(fd, "Test passed!");
      end else begin
         $display("Failed tests: %d", failed);
         $fdisplay(fd, "Test failed!");
      end

      $finish();
   end

   // Insert delays between AXI like handshake interfaces
   wire m_rvalid, m_rready, s_rvalid, s_rready;
   axidelayRead #(
      .MAX_DELAY(DELAY_AXI_READ)
   ) delayRead (
      // Connect directly to the same named axi read wires in the manager interface
      .m_rvalid_o(m_rvalid),
      .m_rready_i(m_rready),

      // Connect directly to the same named axi read wires in the subordinate interface
      .s_rvalid_i(s_rvalid),
      .s_rready_o(s_rready),

      .clk_i(clk),
      .rst_i(rst)
   );

   wire m_wvalid, m_wready, s_wvalid, s_wready;
   axidelayWrite #(
      .MAX_DELAY(DELAY_AXI_WRITE)
   ) delayWrite (
      // Connect directly to the same named axi write wires in the manager interface
      .m_wvalid_i(m_wvalid),
      .m_wready_o(m_wready),

      // Connect directly to the same named axi write wires in the subordinate interface
      .s_wvalid_o(s_wvalid),
      .s_wready_i(s_wready),

      .clk_i(clk),
      .rst_i(rst)
   );

   wire delayed_axis_in_valid, delayed_axis_in_ready;
   wire axis_in_valid, axis_in_ready;
   axidelay #(
      .MAX_DELAY(DELAY_AXIS_IN)
   ) delayIn (
      // Manager interface. Connect to a subordinate interface
      .m_valid_o(delayed_axis_in_valid),
      .m_ready_i(delayed_axis_in_ready),

      // Subordinate interface. Connect to a manager interface
      .s_valid_i(axis_in_valid),
      .s_ready_o(axis_in_ready),

      .clk_i(clk),
      .rst_i(rst)
   );

   wire delayed_axis_out_valid, delayed_axis_out_ready;
   wire non_delayed_axis_out_valid, non_delayed_axis_out_ready;
   axidelay #(
      .MAX_DELAY(DELAY_AXIS_OUT)
   ) delayOut (
      // Manager interface. Connect to a subordinate interface
      .m_valid_o(delayed_axis_out_valid),
      .m_ready_i(delayed_axis_out_ready),

      // Subordinate interface. Connect to a manager interface
      .s_valid_i(non_delayed_axis_out_valid),
      .s_ready_o(non_delayed_axis_out_ready),

      .clk_i(clk),
      .rst_i(rst)
   );

   //instantiate axis2axi core
   iob_axis2axi_mwrap #(
        .AXI_ADDR_W(ADDR_W),
        .AXI_LEN_W(AXI_LEN_W),
        .AXI_DATA_W(DATA_W),
        .AXI_ID_W(1),
        .WLEN_W(WLEN_W),
        .RLEN_W(RLEN_W)
   ) axis2axi_mwrap0 (
        // clk_en_rst_s
        .clk_i(clk),
        .cke_i(cke),
        .arst_i(arst),
        // rst_i
        .rst_i(rst),
        // config_write_io
        .w_addr_i(w_addr),
        .w_length_i(w_length),
        .w_start_transfer_i(w_start_transfer),
        .w_max_len_i(w_max_len),
        .w_remaining_data_o(w_remaining_data),
        .w_busy_o(w_busy),
        // config_read_io
        .r_addr_i(r_addr),
        .r_length_i(r_length),
        .r_start_transfer_i(r_start_transfer),
        .r_max_len_i(r_max_len),
        .r_remaining_data_o(r_remaining_data),
        .r_busy_o(r_busy),
        // axis_in_io
        .axis_in_tdata_i(axis2axi_axis_in_tdata),
        .axis_in_tvalid_i(delayed_axis_in_valid),
        .axis_in_tready_o(delayed_axis_in_ready),
        // axis_out_io
        .axis_out_tdata_o(axis2axi_axis_out_tdata),
        .axis_out_tvalid_o(non_delayed_axis_out_valid),
        .axis_out_tready_i(non_delayed_axis_out_ready),
        // axi_m
        .axi_araddr_o(ram_axi_araddr),
        .axi_arvalid_o(ram_axi_arvalid),
        .axi_arready_i(ram_axi_arready),
        .axi_rdata_i(ram_axi_rdata),
        .axi_rresp_i(ram_axi_rresp),
        .axi_rvalid_i(m_rvalid),
        .axi_rready_o(m_rready),
        .axi_arid_o(ram_axi_arid),
        .axi_arlen_o(ram_axi_arlen),
        .axi_arsize_o(ram_axi_arsize),
        .axi_arburst_o(ram_axi_arburst),
        .axi_arlock_o(ram_axi_arlock),
        .axi_arcache_o(ram_axi_arcache),
        .axi_arqos_o(ram_axi_arqos),
        .axi_rid_i(ram_axi_rid),
        .axi_rlast_i(ram_axi_rlast),
        .axi_awaddr_o(ram_axi_awaddr),
        .axi_awvalid_o(ram_axi_awvalid),
        .axi_awready_i(ram_axi_awready),
        .axi_wdata_o(ram_axi_wdata),
        .axi_wstrb_o(ram_axi_wstrb),
        .axi_wvalid_o(m_wvalid),
        .axi_wready_i(m_wready),
        .axi_bresp_i(ram_axi_bresp),
        .axi_bvalid_i(ram_axi_bvalid),
        .axi_bready_o(ram_axi_bready),
        .axi_awid_o(ram_axi_awid),
        .axi_awlen_o(ram_axi_awlen),
        .axi_awsize_o(ram_axi_awsize),
        .axi_awburst_o(ram_axi_awburst),
        .axi_awlock_o(ram_axi_awlock),
        .axi_awcache_o(ram_axi_awcache),
        .axi_awqos_o(ram_axi_awqos),
        .axi_wlast_o(ram_axi_wlast),
        .axi_bid_i(ram_axi_bid)
   );

   iob_axistream_in #(
        .DATA_W(DATA_W),
        .ADDR_W(ADDR_W),
        .TDATA_W(DATA_W),
        .FIFO_ADDR_W(AXIS_FIFO_ADDR_W)
   ) axistream_in0 (
       // clk_en_rst_s
       .clk_i(clk),
       .cke_i(cke),
       .arst_i(arst),
       // interrupt_o
       .interrupt_o(),
       // axistream_io
       .axis_clk_i(clk),
       .axis_cke_i(cke),
       .axis_arst_i(arst),
       .axis_tdata_i(axis_tdata),
       .axis_tvalid_i(axis_tvalid),
       .axis_tready_o(axis_tready),
       .axis_tlast_i(axis_tlast),
       // sys_axis_io
       .sys_tdata_o(axis2axi_axis_in_tdata),
       .sys_tvalid_o(axis_in_valid),
       .sys_tready_i(axis_in_ready),
       // iob_csrs_cbus_s
       .iob_csrs_iob_valid_i(axis_in_iob_valid),
       .iob_csrs_iob_addr_i(axis_in_iob_addr[`IOB_AXISTREAM_IN_CSRS_ADDR_W-1:2]),
       .iob_csrs_iob_wdata_i(axis_in_iob_wdata),
       .iob_csrs_iob_wstrb_i(axis_in_iob_wstrb),
       .iob_csrs_iob_rvalid_o(axis_in_iob_rvalid),
       .iob_csrs_iob_rdata_o(axis_in_iob_rdata),
       .iob_csrs_iob_rready_i(axis_in_iob_rready),
       .iob_csrs_iob_ready_o(axis_in_iob_ready)
   );

   iob_axistream_out #(
        .DATA_W(DATA_W),
        .ADDR_W(ADDR_W),
        .TDATA_W(DATA_W),
        .FIFO_ADDR_W(AXIS_FIFO_ADDR_W)
   ) axistream_out0 (
       // clk_en_rst_s
       .clk_i(clk),
       .cke_i(cke),
       .arst_i(arst),
       // interrupt_o
       .interrupt_o(),
       // axistream_io
       .axis_clk_i(clk),
       .axis_cke_i(cke),
       .axis_arst_i(arst),
       .axis_tdata_o(axis_tdata),
       .axis_tvalid_o(axis_tvalid),
       .axis_tready_i(axis_tready),
       .axis_tlast_o(axis_tlast),
       // sys_axis_io
       .sys_tdata_i(axis2axi_axis_out_tdata),
       .sys_tvalid_i(delayed_axis_out_valid),
       .sys_tready_o(delayed_axis_out_ready),
       // iob_csrs_cbus_s
       .iob_csrs_iob_valid_i(axis_out_iob_valid),
       .iob_csrs_iob_addr_i(axis_out_iob_addr[`IOB_AXISTREAM_OUT_CSRS_ADDR_W-1:2]),
       .iob_csrs_iob_wdata_i(axis_out_iob_wdata),
       .iob_csrs_iob_wstrb_i(axis_out_iob_wstrb),
       .iob_csrs_iob_rvalid_o(axis_out_iob_rvalid),
       .iob_csrs_iob_rdata_o(axis_out_iob_rdata),
       .iob_csrs_iob_rready_i(axis_out_iob_rready),
       .iob_csrs_iob_ready_o(axis_out_iob_ready)
   );

   iob_axi_ram #(
        .DATA_WIDTH(DATA_W),
        .ADDR_WIDTH(ADDR_W),
        .ID_WIDTH(1)
   ) axi_ram0 (
        // clk_i
        .clk_i(clk),
        // rst_i
        .rst_i(rst),
        // axi_s
        .axi_araddr_i(ram_axi_araddr),
        .axi_arvalid_i(ram_axi_arvalid),
        .axi_arready_o(ram_axi_arready),
        .axi_rdata_o(ram_axi_rdata),
        .axi_rresp_o(ram_axi_rresp),
        .axi_rvalid_o(s_rvalid),
        .axi_rready_i(s_rready),
        .axi_arid_i(ram_axi_arid),
        .axi_arlen_i(ram_axi_arlen),
        .axi_arsize_i(ram_axi_arsize),
        .axi_arburst_i(ram_axi_arburst),
        .axi_arlock_i(ram_axi_arlock),
        .axi_arcache_i(ram_axi_arcache),
        .axi_arqos_i(ram_axi_arqos),
        .axi_rid_o(ram_axi_rid),
        .axi_rlast_o(ram_axi_rlast),
        .axi_awaddr_i(ram_axi_awaddr),
        .axi_awvalid_i(ram_axi_awvalid),
        .axi_awready_o(ram_axi_awready),
        .axi_wdata_i(ram_axi_wdata),
        .axi_wstrb_i(ram_axi_wstrb),
        .axi_wvalid_i(s_wvalid),
        .axi_wready_o(s_wready),
        .axi_bresp_o(ram_axi_bresp),
        .axi_bvalid_o(ram_axi_bvalid),
        .axi_bready_i(ram_axi_bready),
        .axi_awid_i(ram_axi_awid),
        .axi_awlen_i(ram_axi_awlen),
        .axi_awsize_i(ram_axi_awsize),
        .axi_awburst_i(ram_axi_awburst),
        .axi_awlock_i(ram_axi_awlock),
        .axi_awcache_i(ram_axi_awcache),
        .axi_awqos_i(ram_axi_awqos),
        .axi_wlast_i(ram_axi_wlast),
        .axi_bid_o(ram_axi_bid),
        // external_mem_bus_m port
        .ext_mem_clk_o   (axi_ram_ext_mem_clk),
        .ext_mem_r_data_i(axi_ram_ext_mem_r_data),
        .ext_mem_r_en_o  (axi_ram_ext_mem_r_en),
        .ext_mem_r_addr_o(axi_ram_ext_mem_r_addr),
        .ext_mem_w_data_o(axi_ram_ext_mem_w_data),
        .ext_mem_w_strb_o(axi_ram_ext_mem_w_strb),
        .ext_mem_w_addr_o(axi_ram_ext_mem_w_addr)
   );

   // Memory for iob_axi_ram
   iob_ram_t2p_be #(
      .ADDR_W(ADDR_W-2),
      .DATA_W(DATA_W)
   ) iob_ram_t2p_be_inst (
      // ram_t2p_be_s port
      .clk_i   (axi_ram_ext_mem_clk),
      .r_data_o(axi_ram_ext_mem_r_data),
      .r_en_i  (axi_ram_ext_mem_r_en),
      .r_addr_i(axi_ram_ext_mem_r_addr),
      .w_data_i(axi_ram_ext_mem_w_data),
      .w_strb_i(axi_ram_ext_mem_w_strb),
      .w_addr_i(axi_ram_ext_mem_w_addr)
   );

//
// Custom Tasks
//
// Write data to AXIS IN IOb Native slave
task axis_in_iob_write;
   input [`IOB_AXISTREAM_IN_CSRS_ADDR_W-1:0] addr;
   input [31:0] data;
   input [$clog2(32):0] width;

   begin
      @(posedge clk) #1 axis_in_iob_valid = 1;  //sync and assign
      axis_in_iob_addr  = `IOB_WORD_ADDR(addr);
      axis_in_iob_wdata = `IOB_GET_WDATA(addr, data);
      axis_in_iob_wstrb = `IOB_GET_WSTRB(addr, width);

      #1 while (!axis_in_iob_ready) #1;

      @(posedge clk) axis_in_iob_valid = 0;
      axis_in_iob_wstrb = 0;
   end
endtask

// Read data from AXIS IN IOb Native slave
task axis_in_iob_read;
   input [`IOB_AXISTREAM_IN_CSRS_ADDR_W-1:0] addr;
   output [31:0] data;
   input [$clog2(32):0] width;

   begin
      @(posedge clk) #1 axis_in_iob_valid = 1;
      axis_in_iob_addr = `IOB_WORD_ADDR(addr);
      axis_in_iob_wstrb = 0;

      #1 while (!axis_in_iob_ready) #1;
      @(posedge clk) #1 axis_in_iob_valid = 0;
      @(posedge clk) #1 axis_in_iob_rready = 1;

      while (!axis_in_iob_rvalid) #1;
      data = #1 `IOB_GET_RDATA(addr, axis_in_iob_rdata, width);
      @(posedge clk) #1 axis_in_iob_rready = 0;
   end
endtask

// Write data to AXIS OUT IOb Native slave
task axis_out_iob_write;
   input [`IOB_AXISTREAM_OUT_CSRS_ADDR_W-1:0] addr;
   input [31:0] data;
   input [$clog2(32):0] width;

   begin
      @(posedge clk) #1 axis_out_iob_valid = 1;  //sync and assign
      axis_out_iob_addr  = `IOB_WORD_ADDR(addr);
      axis_out_iob_wdata = `IOB_GET_WDATA(addr, data);
      axis_out_iob_wstrb = `IOB_GET_WSTRB(addr, width);

      #1 while (!axis_out_iob_ready) #1;

      @(posedge clk) axis_out_iob_valid = 0;
      axis_out_iob_wstrb = 0;
   end
endtask

// Read data from AXIS OUT IOb Native slave
task axis_out_iob_read;
   input [`IOB_AXISTREAM_OUT_CSRS_ADDR_W-1:0] addr;
   output [31:0] data;
   input [$clog2(32):0] width;

   begin
      @(posedge clk) #1 axis_out_iob_valid = 1;
      axis_out_iob_addr = `IOB_WORD_ADDR(addr);
      axis_out_iob_wstrb = 0;

      #1 while (!axis_out_iob_ready) #1;
      @(posedge clk) #1 axis_out_iob_valid = 0;
      @(posedge clk) #1 axis_out_iob_rready = 1;

      while (!axis_out_iob_rvalid) #1;
      data = #1 `IOB_GET_RDATA(addr, axis_out_iob_rdata, width);
      @(posedge clk) #1 axis_out_iob_rready = 0;
   end
endtask

endmodule
