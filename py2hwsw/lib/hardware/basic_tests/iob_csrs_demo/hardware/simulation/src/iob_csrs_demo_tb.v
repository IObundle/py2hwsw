// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_csrs_demo_csrs_conf.vh"

`define IOB_RESET(CLK, RESET, PRE, DURATION, POST) RESET=0;\
   #PRE RESET=1; #DURATION RESET=0; #POST;\
   @(posedge CLK) #1;

module iob_csrs_demo_tb;

   localparam PER = 10;

   integer fd;

   reg     clk;
   initial clk = 0;
   always #(PER / 2) clk = ~clk;

   reg                                   rst;

   //Cbus wires
   reg                                   iob_valid_i;
   reg  [`IOB_CSRS_DEMO_CSRS_ADDR_W-1:0] iob_addr_i;
   reg  [                        32-1:0] iob_wdata_i;
   reg  [                           3:0] iob_wstrb_i;
   wire [                        32-1:0] iob_rdata_o;
   wire                                  iob_ready_o;
   wire                                  iob_rvalid_o;
   reg                                   iob_rready_i;

   initial begin
`ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
`endif

      rst          = 0;

      // Initialize inputs
      iob_valid_i  = 0;
      iob_addr_i   = 0;
      iob_wdata_i  = 0;
      iob_wstrb_i  = 0;
      iob_rready_i = 0;

      //apply async reset
      `IOB_RESET(clk, rst, 100, 1_000, 100);

      if (1) begin  // TODO: Check if passed
         $display("%c[1;34m", 27);
         $display("Test completed successfully.");
         $display("%c[0m", 27);
         fd = $fopen("test.log", "w");
         $fdisplay(fd, "Test passed!");
         $fclose(fd);

      end else begin
         $display("Test failed");
         fd = $fopen("test.log", "w");
         $fdisplay(fd, "Test failed");
         $fclose(fd);
      end

      $finish();
   end

   //instantiate iob_csrs_demo core
   iob_csrs_demo iob_csrs_demo0 (
      // clk_en_rst_s port
      .clk_i                (clk),
      .cke_i                (1'b1),
      .arst_i               (rst),
      // cbus_s port
      .iob_csrs_iob_valid_i (iob_valid_i),
      .iob_csrs_iob_addr_i  (iob_addr_i),
      .iob_csrs_iob_wdata_i (iob_wdata_i),
      .iob_csrs_iob_wstrb_i (iob_wstrb_i),
      .iob_csrs_iob_rvalid_o(iob_rvalid_o),
      .iob_csrs_iob_rdata_o (iob_rdata_o),
      .iob_csrs_iob_ready_o (iob_ready_o),
      .iob_csrs_iob_rready_i(iob_rready_i)
   );

endmodule
