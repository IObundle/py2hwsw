// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

`include "iob_axistream_in_csrs_def.vh"
`include "iob_axistream_in_conf.vh"
`include "iob_axistream_out_csrs_def.vh"
`include "iob_axistream_out_conf.vh"

`define IOB_GET_NBYTES(WIDTH) (WIDTH/8 + |(WIDTH%8))
`define IOB_WORD_ADDRESS(ADDR) ((ADDR>>2)<<2)

`define IOB_BYTE_OFFSET(ADDR) (ADDR%(32/8))

`define IOB_GET_WDATA(ADDR, DATA) (DATA<<(8*`IOB_BYTE_OFFSET(ADDR)))
`define IOB_GET_WSTRB(ADDR, WIDTH) (((1<<`IOB_GET_NBYTES(WIDTH))-1)<<`IOB_BYTE_OFFSET(ADDR))
`define IOB_GET_RDATA(ADDR, DATA, WIDTH) ((DATA>>(8*`IOB_BYTE_OFFSET(ADDR)))&((1<<WIDTH)-1))

`define IOB_RESET(CLK, RESET, PRE, DURATION, POST) RESET=0;\
   #PRE RESET=1; #DURATION RESET=0; #POST;\
   @(posedge CLK) #1;



module iob_axistream_in_tb;

   parameter clk_frequency = 100e6;  //100 MHz
   parameter clk_per = 1e9 / clk_frequency;

   localparam DATA_W = 32;
   localparam ADDR_W = 10;
   localparam AXIS_FIFO_ADDR_W = 10;
   localparam NWORDS = 256;

   //iterator
   integer i, fd;

   // CORE SIGNALS
   reg arst = 0;
   reg clk;
   reg cke = 1;

   iob_clock #(.CLK_PERIOD(10)) clk_inst (.clk_o(clk));

   reg [DATA_W-1:0] word;

   //iob interfaces (backend)
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

   // AXIS OUT -> AXIS IN connection
   wire [DATA_W-1:0] axis_tdata;
   wire axis_tvalid;
   wire axis_tready;
   wire axis_tlast;

   integer                             failed = 0;

   initial begin
`ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
`endif

      //apply async reset
      `IOB_RESET(clk, arst, 100, 1_000, 100);

      $display("Starting testbench");

      $display("Configure AXIStream IN");
      axis_in_iob_write(`IOB_AXISTREAM_IN_SOFT_RESET_ADDR, 0, `IOB_AXISTREAM_IN_SOFT_RESET_W);
      axis_in_iob_write(`IOB_AXISTREAM_IN_MODE_ADDR, 0, `IOB_AXISTREAM_IN_MODE_W);
      axis_in_iob_write(`IOB_AXISTREAM_IN_NWORDS_ADDR, NWORDS, `IOB_AXISTREAM_IN_NWORDS_W);
      axis_in_iob_write(`IOB_AXISTREAM_IN_ENABLE_ADDR, 1, `IOB_AXISTREAM_IN_ENABLE_W);

      $display("Configure AXIStream OUT");
      axis_out_iob_write(`IOB_AXISTREAM_OUT_SOFT_RESET_ADDR, 0, `IOB_AXISTREAM_OUT_SOFT_RESET_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_MODE_ADDR, 0, `IOB_AXISTREAM_OUT_MODE_W);
      axis_out_iob_write(`IOB_AXISTREAM_IN_NWORDS_ADDR, NWORDS, `IOB_AXISTREAM_IN_NWORDS_W);
      axis_out_iob_write(`IOB_AXISTREAM_OUT_ENABLE_ADDR, 1, `IOB_AXISTREAM_OUT_ENABLE_W);

      $display("Write data to AXIStream OUT");

      // write data loop
      for (i = 0; i < 256; i = i + 1) begin
         axis_out_iob_write(`IOB_AXISTREAM_OUT_DATA_ADDR, i, `IOB_AXISTREAM_OUT_DATA_W);
      end

      $display("Read data from AXIStream IN");

      // read data loop
      for (i = 0; i < 256; i = i + 1) begin
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

      $fclose(fd);
      $finish();

   end

   // test setup: AXIS stream out -> AXIS stream in
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
       .sys_tdata_o(),
       .sys_tvalid_o(),
       .sys_tready_i(1'b0),
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
       .sys_tdata_i({DATA_W{1'b0}}),
       .sys_tvalid_i(1'b0),
       .sys_tready_o(),
       // iob_csrs_cbus_s
       .iob_csrs_iob_valid_i(axis_out_iob_valid),
       .iob_csrs_iob_addr_i(axis_out_iob_addr[`IOB_AXISTREAM_IN_CSRS_ADDR_W-1:2]),
       .iob_csrs_iob_wdata_i(axis_out_iob_wdata),
       .iob_csrs_iob_wstrb_i(axis_out_iob_wstrb),
       .iob_csrs_iob_rvalid_o(axis_out_iob_rvalid),
       .iob_csrs_iob_rdata_o(axis_out_iob_rdata),
       .iob_csrs_iob_rready_i(axis_out_iob_rready),
       .iob_csrs_iob_ready_o(axis_out_iob_ready)
   );

// Write data to AXIS IN IOb Native slave
task axis_in_iob_write;
   input [`IOB_AXISTREAM_IN_CSRS_ADDR_W-1:0] addr;
   input [31:0] data;
   input [$clog2(32):0] width;

   begin
      @(posedge clk) #1 axis_in_iob_valid = 1;  //sync and assign
      axis_in_iob_addr  = `IOB_WORD_ADDRESS(addr);
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
      axis_in_iob_addr = `IOB_WORD_ADDRESS(addr);
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
      axis_out_iob_addr  = `IOB_WORD_ADDRESS(addr);
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
      axis_out_iob_addr = `IOB_WORD_ADDRESS(addr);
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

