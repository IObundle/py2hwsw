/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

`timescale 1ns/1ps
`include "iob_uvm_pkg.sv"

// Define the interface
interface iob_if;
   logic clk_i;
   logic cke_i;
   logic arst_i;
   logic iob_valid_i;
   logic [31:0] iob_wdata_i;
   logic [`IOB_CSRS_ADDR_W-1:0] iob_addr_i;
   logic [3:0]                  iob_wstrb_i;
   logic                        iob_rvalid_o;
   logic [31:0]                 iob_rdata_o;
   logic                        iob_ready_o;
endinterface: iob_if

module iob_uvm_tb;
   import uvm_pkg::*;
   import iob_uvm_pkg::*;
`include "uvm_macros.svh"

   reg clk;
   reg arst;

   //Interface declaration
   iob_if vif();

   //Connects the Interface to the DUT
   iob_uut uut (
      .clk_i(vif.clk_i),
      .cke_i(vif.cke_i),
      .arst_i(vif.arst_i),
      .iob_valid_i(vif.iob_valid_i),
      .iob_addr_i(vif.iob_addr_i),
      .iob_wdata_i(vif.iob_wdata_i),
      .iob_wstrb_i(vif.iob_wstrb_i),
      .iob_rvalid_o(vif.iob_rvalid_o),
      .iob_rdata_o(vif.iob_rdata_o),
      .iob_ready_o(vif.iob_ready_o)
   );

   initial begin
      //Registers the Interface in the configuration block so that other
      //blocks can use it
       uvm_resource_db#(virtual iob_if)::set
                        (.scope("ifs"), .name("iob_if"), .val(vif));

      //Executes the test
      run_test();
   end

   initial begin
   `ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
   `endif
   end

   //init clock, clock enable and reset
   initial begin 
      vif.clk_i = 1'b1;
      vif.arst_i = 0;
      vif.cke_i = 1;
      vif.iob_valid_i = 0;
      vif.iob_addr_i = 0;
      vif.iob_wdata_i = 0;
      vif.iob_wstrb_i = 0;
   end

   //toggle clock
   always #5 vif.clk_i = ~vif.clk_i;

   //do reset
   initial begin
      #10;
      vif.arst_i = 1;
      #10;
      vif.arst_i = 0;
   end

endmodule
