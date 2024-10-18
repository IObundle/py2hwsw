// SPDX-FileCopyrightText: 2024 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_csrs_demo_csrs_def.vh"

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

   initial begin
`ifdef VCD
      $dumpfile("iob_csrs_demo.vcd");
      $dumpvars();
`endif

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
      .clk_i       (clk),
      .cke_i       (1'b1),
      .arst_i      (rst),
      // cbus_s port
      .iob_valid_i (iob_valid_i),
      .iob_addr_i  (iob_addr_i[`IOB_CSRS_DEMO_CSRS_ADDR_W-1:2]),
      .iob_wdata_i (iob_wdata_i),
      .iob_wstrb_i (iob_wstrb_i),
      .iob_rvalid_o(iob_rvalid_o),
      .iob_rdata_o (iob_rdata_o),
      .iob_ready_o (iob_ready_o)
   );

endmodule
