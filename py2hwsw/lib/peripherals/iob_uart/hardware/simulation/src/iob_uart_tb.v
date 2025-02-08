// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

`include "iob_uart_csrs_def.vh"
`include "iob_uart_conf.vh"

`define IOB_NBYTES (32/8)
`define IOB_GET_NBYTES(WIDTH) (WIDTH/8 + |(WIDTH%8))
`define IOB_NBYTES_W $clog2(`IOB_NBYTES)
`define IOB_WORD_ADDR(ADDR) ((ADDR>>`IOB_NBYTES_W)<<`IOB_NBYTES_W)

`define IOB_BYTE_OFFSET(ADDR) (ADDR%(32/8))

`define IOB_GET_WDATA(ADDR, DATA) (DATA<<(8*`IOB_BYTE_OFFSET(ADDR)))
`define IOB_GET_WSTRB(ADDR, WIDTH) (((1<<`IOB_GET_NBYTES(WIDTH))-1)<<`IOB_BYTE_OFFSET(ADDR))
`define IOB_GET_RDATA(ADDR, DATA, WIDTH) ((DATA>>(8*`IOB_BYTE_OFFSET(ADDR)))&((1<<WIDTH)-1))

`define IOB_RESET(CLK, RESET, PRE, DURATION, POST) RESET=~`IOB_UART_RST_POL;\
   #PRE RESET=`IOB_UART_RST_POL; #DURATION RESET=~`IOB_UART_RST_POL; #POST;\
   @(posedge CLK) #1;

module iob_uart_tb;

   parameter clk_frequency = 100e6;  //100 MHz
   parameter baud_rate = 1e6;  //high value to speed sim
   parameter clk_per = 1e9 / clk_frequency;

   //iterator
   integer i, fd;

   // CORE SIGNALS
   reg                        arst = ~`IOB_UART_RST_POL;
   reg                        clk;
   reg                        cke = 1;

   reg [7:0]                  word;
   
   //rs232 interface (frontend)
   wire                       rts2cts;
   wire                       tx2rx;

   //iob interface (backend)
   reg                        iob_valid_i;
   reg [31:0]                 iob_wdata_i;
   reg [`IOB_UART_CSRS_ADDR_W-3:0] iob_addr_i;
   reg [7:0]                       iob_wstrb_i;
   wire                            iob_rvalid_o;
   wire [31:0]                     iob_rdata_o;
   wire                            iob_ready_o;
   
   integer                         failed = 0;
   
   initial begin
`ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
`endif
      clk      = 1;

      //apply async reset
      `IOB_RESET(clk, arst, 100, 1_000, 100);

      $display("Starting testbench");

      iob_write(`IOB_UART_SOFTRESET_ADDR, 0, `IOB_UART_SOFTRESET_W);
      iob_write(`IOB_UART_TXEN_ADDR, 0, `IOB_UART_TXEN_W);
      iob_write(`IOB_UART_RXEN_ADDR, 0, `IOB_UART_RXEN_W);

      $display("Softreset done");

      iob_write(`IOB_UART_DIV_ADDR, clk_frequency / baud_rate, `IOB_UART_DIV_W);

      $display("Baudrate set");

      
      iob_read(`IOB_UART_RXREADY_ADDR, word, `IOB_UART_RXREADY_W);
      if (word != 0) begin
         $display("Error: RX ready initially");
         failed = failed + 1;
      end

      iob_read(`IOB_UART_TXREADY_ADDR, word, `IOB_UART_TXREADY_W);
      if (word != 0) begin
         $display("Error: TX ready initially");
         failed = failed + 1;
      end

      $display("Ready signals checked");

      //pulse soft reset
      iob_write(`IOB_UART_SOFTRESET_ADDR, 1, `IOB_UART_SOFTRESET_W);
      iob_write(`IOB_UART_SOFTRESET_ADDR, 0, `IOB_UART_SOFTRESET_W);


      //enable tx and rx
      iob_write(`IOB_UART_TXEN_ADDR, 1, `IOB_UART_TXEN_W);
      iob_write(`IOB_UART_RXEN_ADDR, 1, `IOB_UART_RXEN_W);


      $display("TX and RX enabled");

      
      // data send/receive loop
      for (i=0; i<256; i=i+1) begin

         //wait for tx ready
         word = 0;
         while (word != 1) begin
            iob_read(`IOB_UART_TXREADY_ADDR, word, `IOB_UART_TXREADY_W);
         end

         $display("TX ready");

         //send data
         iob_write(`IOB_UART_TXDATA_ADDR, i, `IOB_UART_TXDATA_W);

         //wait for rx ready
         word = 0;
         while (word != 1) begin
            iob_read(`IOB_UART_RXREADY_ADDR, word, `IOB_UART_RXREADY_W);
         end

         //read data
         iob_read(`IOB_UART_RXDATA_ADDR, word, `IOB_UART_RXDATA_W);

         //check data
         if (word != i) begin
            $display("Error: wrong data received");
            failed = failed + 1;
         end
         
      end

      $display("%c[1;34m", 27);
      $display("Test completed successfully.");
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

   //
   // CLOCK
   //

   //system clock
   always #(clk_per / 2) clk = ~clk;


   // Instantiate the Unit Under Test (UUT)
   iob_uart uut 
     (
      .clk_i          (clk),
      .arst_i         (arst),
      .cke_i          (cke),

      .rs232_rxd_i    (tx2rx),
      .rs232_txd_o    (tx2rx),
      .rs232_rts_o    (rts2cts),
      .rs232_cts_i    (rts2cts),

      .iob_uart_csrs_iob_valid_i (iob_valid_i),
      .iob_uart_csrs_iob_addr_i  (iob_addr_i),
      .iob_uart_csrs_iob_wdata_i (iob_wdata_i),
      .iob_uart_csrs_iob_wstrb_i (iob_wstrb_i),
      .iob_uart_csrs_iob_rvalid_o(iob_rvalid_o),
      .iob_uart_csrs_iob_rdata_o  (iob_rdata_o),
      .iob_uart_csrs_iob_ready_o  (iob_ready_o)
   );

// Write data to IOb Native slave
task iob_write;
   input [`IOB_UART_CSRS_ADDR_W-3:0] addr;
   input [31:0] data;
   input [$clog2(32):0] width;

   begin
      @(posedge clk) #1 iob_valid_i = 1;  //sync and assign
      iob_addr_i  = `IOB_WORD_ADDR(addr);
      iob_wdata_i = `IOB_GET_WDATA(addr, data);
      iob_wstrb_i = `IOB_GET_WSTRB(addr, width);

      #1 while (!iob_ready_o) #1;

      @(posedge clk) iob_valid_i = 0;
      iob_wstrb_i = 0;
   end
endtask

// Read data from IOb Native slave
task iob_read;
   input [`IOB_UART_CSRS_ADDR_W-3:0] addr;
   output [31:0] data;
   input [$clog2(32):0] width;

   begin
      @(posedge clk) #1 iob_valid_i = 1;
      iob_addr_i = `IOB_WORD_ADDR(addr);
      iob_wstrb_i = 0;

      #1 while (!iob_ready_o) #1;
      @(posedge clk) #1 iob_valid_i = 0;

      while (!iob_rvalid_o) #1;
      data = #1 `IOB_GET_RDATA(addr, iob_rdata_o, width);
   end
endtask

endmodule

