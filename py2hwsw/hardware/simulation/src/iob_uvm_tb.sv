`timescale 1ns/1ps
import uvm_pkg::*;
`include "iob_v_tb.vh"
`include "uvm_macros.svh"
//`include "dpi/uvm_dpi.svh"

`define R 0
`define W 1
`define F 2


// Define the transaction class
class iob_transaction extends uvm_sequence_item;
   rand bit [31:0] addr;
   rand bit [31:0] data;
   rand bit [3:0]  wstrb;
   rand bit        mode; // 0 for read, 1 for write

   `uvm_object_utils_begin(iob_transaction)
      `uvm_field_int(addr, UVM_ALL_ON)
      `uvm_field_int(data, UVM_ALL_ON)
      `uvm_field_int(wstrb, UVM_ALL_ON)
      `uvm_field_int(mode, UVM_ALL_ON)
   `uvm_object_utils_end

   function new(string name = "iob_transaction");
      super.new(name);
   endfunction
endclass

// Define the driver
class iob_driver extends uvm_driver #(iob_transaction);
   `uvm_component_utils(iob_driver)

   virtual iob_if vif;

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   virtual task run_phase(uvm_phase phase);
      forever begin
         seq_item_port.get_next_item(req);
         drive_transaction(req);
         seq_item_port.item_done();
      end
   endtask

   virtual task drive_transaction(iob_transaction trans);
      // Drive the transaction to the DUT
      vif.iob_valid_i = 1;
      vif.iob_addr_i  = trans.addr;
      vif.iob_wdata_i = trans.data;
      vif.iob_wstrb_i = trans.wstrb;
      @(posedge vif.clk);
      while (!vif.iob_ready_o) @(posedge vif.clk);
      vif.iob_valid_i = 0;
   endtask
endclass

// Define the monitor
class iob_monitor extends uvm_monitor;
   `uvm_component_utils(iob_monitor)

   virtual iob_if vif;
   uvm_analysis_port #(iob_transaction) ap;

   function new(string name, uvm_component parent);
      super.new(name, parent);
      ap = new("ap", this);
   endfunction

   virtual task run_phase(uvm_phase phase);
      forever begin
         iob_transaction trans;
         @(posedge vif.clk);
         if (vif.iob_rvalid_o) begin
            trans = iob_transaction::type_id::create("trans");
            trans.addr = vif.iob_addr_i;
            trans.data = vif.iob_rdata_o;
            ap.write(trans);
         end
      end
   endtask
endclass

// Define the agent
class iob_agent extends uvm_agent;
   `uvm_component_utils(iob_agent)

   iob_driver    driver;
   iob_monitor   monitor;
   uvm_sequencer #(iob_transaction) sequencer;

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      driver = iob_driver::type_id::create("driver", this);
      monitor = iob_monitor::type_id::create("monitor", this);
      sequencer = uvm_sequencer#(iob_transaction)::type_id::create("sequencer", this);
   endfunction

   virtual function void connect_phase(uvm_phase phase);
      driver.seq_item_port.connect(sequencer.seq_item_export);
   endfunction
endclass

// Define the scoreboard
class iob_scoreboard extends uvm_scoreboard;
   `uvm_component_utils(iob_scoreboard)

   uvm_analysis_imp #(iob_transaction, iob_scoreboard) ap;

   function new(string name, uvm_component parent);
      super.new(name, parent);
      ap = new("ap", this);
   endfunction

   virtual function void write(iob_transaction trans);
      // Compare expected and actual results
      // Implement your comparison logic here
   endfunction
endclass

// Define the environment
class iob_env extends uvm_env;
   `uvm_component_utils(iob_env)

   iob_agent    agent;
   iob_scoreboard scoreboard;

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      agent = iob_agent::type_id::create("agent", this);
      scoreboard = iob_scoreboard::type_id::create("scoreboard", this);
   endfunction

   virtual function void connect_phase(uvm_phase phase);
      agent.monitor.ap.connect(scoreboard.ap);
   endfunction
endclass

// Define the sequence with file I/O
class iob_sequence extends uvm_sequence #(iob_transaction);
   `uvm_object_utils(iob_sequence)

   // File handles
   integer c2v_read_fp;
   integer v2c_write_fp;

   // Variables for file I/O
   integer req = -100, ack = 0, mode = -100, address = -100, data = -100, data_w = -100;

   function new(string name = "iob_sequence");
      super.new(name);
   endfunction

   virtual task body();
      // Open the input file
      c2v_read_fp = $fopen("c2v.txt", "r");
      if (c2v_read_fp == 0) begin
         `uvm_fatal("FILE_ERR", "Failed to open c2v.txt")
      end

      // Open the output file
      v2c_write_fp = $fopen("v2c.txt", "w");
      if (v2c_write_fp == 0) begin
         `uvm_fatal("FILE_ERR", "Failed to open v2c.txt")
      end

      // Read and process commands from the input file
      while (!$feof(c2v_read_fp)) begin
         if ($fscanf(c2v_read_fp, "%08x %08x %08x %08x %08x\n", req, mode, address, data_w, data) == 5) begin
            `uvm_info("SEQ", $sformatf("Read from file: req=%08x mode=%08x address=%08x data_w=%08x data=%08x", req, mode, address, data_w, data), UVM_LOW)

            // Check if the request number matches the acknowledgment number
            if (req == ack) begin
               // Process the request
               if (mode == `F) begin // Finish request
                  `uvm_info("SEQ", "Finish request received", UVM_LOW)
                  $fclose(c2v_read_fp);
                  $fclose(v2c_write_fp);
                  return; // End the sequence
               end
               else if (mode == `R) begin // Read request
                  iob_transaction trans;
                  trans = iob_transaction::type_id::create("trans");
                  trans.addr = address;
                  trans.mode = 0; // Read mode
                  start_item(trans);
                  finish_item(trans);

                  // Write acknowledgment and data to the output file
                  $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w, trans.data);
                  `uvm_info("SEQ", $sformatf("Write to file: ack=%08x mode=%08x address=%08x data_w=%08x data=%08x", ack, mode, address, data_w, trans.data), UVM_LOW)
               end
               else if (mode == `W) begin // Write request
                  iob_transaction trans;
                  trans = iob_transaction::type_id::create("trans");
                  trans.addr = address;
                  trans.data = data;
                  trans.mode = 1; // Write mode
                  start_item(trans);
                  finish_item(trans);

                  // Write acknowledgment to the output file
                  $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w, data);
                  `uvm_info("SEQ", $sformatf("Write to file: ack=%08x mode=%08x address=%08x data_w=%08x data=%08x", ack, mode, address, data_w, data), UVM_LOW)
               end

               // Increment acknowledgment number
               ack = ack + 1;
            end
         end
      end

      // Close files
      $fclose(c2v_read_fp);
      $fclose(v2c_write_fp);
   endtask
endclass

// Define the test
class iob_test extends uvm_test;
   `uvm_component_utils(iob_test)

   iob_env env;

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      env = iob_env::type_id::create("env", this);
   endfunction

   virtual task run_phase(uvm_phase phase);
      iob_sequence seq;
      seq = iob_sequence::type_id::create("seq");
      seq.start(env.agent.sequencer);
   endtask
endclass

// Define the interface
interface iob_if(input logic clk);
   logic iob_valid_i;
   logic [31:0] iob_wdata_i;
   logic [31:0] iob_addr_i;
   logic [3:0]  iob_wstrb_i;
   logic        iob_rvalid_o;
   logic [31:0] iob_rdata_o;
   logic        iob_ready_o;
endinterface

// Top-level testbench
module iob_uvm_tb;
   import uvm_pkg::*;
   `include "uvm_macros.svh"

   // Clock and reset signals
   reg clk;
   reg arst;

   // Instantiate the interface
   iob_if iob_if(clk);

   // Instantiate the DUT and connect the interface
   iob_uut uut (
      .clk_i(clk),
      .arst_i(arst),
      .cke_i(1),
      .iob_valid_i(iob_if.iob_valid_i),
      .iob_addr_i(iob_if.iob_addr_i),
      .iob_wdata_i(iob_if.iob_wdata_i),
      .iob_wstrb_i(iob_if.iob_wstrb_i),
      .iob_rvalid_o(iob_if.iob_rvalid_o),
      .iob_rdata_o(iob_if.iob_rdata_o),
      .iob_ready_o(iob_if.iob_ready_o)
   );

   // Clock generation
   initial begin
      clk = 0;
      forever #5 clk = ~clk;
   end

   // Reset generation
   initial begin
      arst = 0;
      #10;
      arst = 1;
      #10;
      arst = 0;
   end

   // UVM test start
   initial begin
      uvm_config_db#(virtual iob_if)::set(null, "*", "vif", iob_if);
      run_test("iob_test");
   end
endmodule
