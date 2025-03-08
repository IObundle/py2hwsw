`timescale 1ns/1ps

`include "uvm_macros.svh"
import uvm_pkg::*;

`define R 0
`define W 1
`define F 2

`define IOB_GET_NBYTES(WIDTH) (WIDTH/8 + |(WIDTH%8))
`define IOB_WORD_ADDRESS(ADDR) ((ADDR>>2)<<2)

`define IOB_BYTE_OFFSET(ADDR) (ADDR%(32/8))

`define IOB_GET_WDATA(ADDR, DATA) (DATA<<(8*`IOB_BYTE_OFFSET(ADDR)))
`define IOB_GET_WSTRB(ADDR, WIDTH) (((1<<`IOB_GET_NBYTES(WIDTH))-1)<<`IOB_BYTE_OFFSET(ADDR))
`define IOB_GET_RDATA(ADDR, DATA, WIDTH) ((DATA>>(8*`IOB_BYTE_OFFSET(ADDR)))&((1<<WIDTH)-1))


// Define the transaction class
class iob_transaction extends uvm_sequence_item;
   rand bit [31:0] addr;
   rand bit [31:0] data;
   rand bit [3:0]  wstrb;

   `uvm_object_utils_begin(iob_transaction)
      `uvm_field_int(addr, UVM_ALL_ON)
      `uvm_field_int(data, UVM_ALL_ON)
      `uvm_field_int(wstrb, UVM_ALL_ON)
   `uvm_object_utils_end

   function new(string name = "iob_transaction");
      super.new(name);
   endfunction
endclass

// Define the driver
class iob_driver extends uvm_driver #(iob_transaction);
   `uvm_component_utils(iob_driver)

   virtual iob_if vif; // Virtual interface for driving signals

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      // Retrieve the virtual interface from the uvm_config_db
      if (!uvm_config_db#(virtual iob_if)::get(this, "", "vif", vif)) begin
         `uvm_fatal("CFG_ERR", "Virtual interface not found for iob_driver")
      end
   endfunction

   virtual task run_phase(uvm_phase phase);
      forever begin
         iob_transaction trans;

         // Get the next transaction from the sequencer
         seq_item_port.get_next_item(trans);

         // Drive the transaction to the DUT
         drive_transaction(trans);

         // Signal that the transaction is complete
         seq_item_port.item_done();
      end
   endtask

   virtual task drive_transaction(iob_transaction trans);
      // Drive the transaction to the DUT
      vif.iob_valid_i = 1; // Assert valid signal
      vif.iob_addr_i  = trans.addr; // Use macro for address alignment
      vif.iob_wdata_i = trans.data; // Use macro for data shifting
      vif.iob_wstrb_i = trans.wstrb; // Use macro for strobe generation

      // Wait for the DUT to assert iob_ready_o
      @(posedge vif.clk);
      while (!vif.iob_ready_o) @(posedge vif.clk);

      // Deassert valid signal
      vif.iob_valid_i = 0;

      // If it's a read transaction, wait for iob_rvalid_o
      if (trans.wstrb == 0) begin
         while (!vif.iob_rvalid_o) @(posedge vif.clk);
         trans.data = vif.iob_rdata_o; // Capture read data
      end

      `uvm_info("DRV", $sformatf("Driven transaction: addr=%08x data=%08x mode=%0d", trans.addr, trans.data, trans.wstrb), UVM_LOW)
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

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if (!uvm_config_db#(virtual iob_if)::get(this, "", "vif", vif)) begin
         `uvm_fatal("CFG_ERR", "Virtual interface not found for iob_monitor")
      end
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
            `uvm_info("MON", $sformatf("Monitored transaction: addr=%08x data=%08x", trans.addr, trans.data), UVM_LOW)
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
      `uvm_info("SCB", $sformatf("Received transaction: addr=%08x data=%08x", trans.addr, trans.data), UVM_LOW)
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

   integer c2v_read_fp;
   integer v2c_write_fp;
   integer req = -100, ack = 0, mode = -100, address = -100, data = -100, data_w = -100;

   function new(string name = "iob_sequence");
      super.new(name);
   endfunction

   virtual task body();
      if (c2v_read_fp == 0) begin
         `uvm_fatal("FILE_ERR", "Failed to open c2v.txt")
      end

      if (v2c_write_fp == 0) begin
         `uvm_fatal("FILE_ERR", "Failed to open v2c.txt")
      end

      while (1) begin
         c2v_read_fp = $fopen("c2v.txt", "rb");
         if (c2v_read_fp != 0) begin
            if ($fscanf(c2v_read_fp, "%08x %08x %08x %08x %08x\n", req, mode, address, data_w, data)) begin
               `uvm_info("SEQ", $sformatf("Read from file: req=%08x mode=%08x address=%08x data_w=%08x data=%08x", req, mode, address, data_w, data), UVM_LOW)
               if (req == ack) begin
                  v2c_write_fp = $fopen("v2c.txt", "wb");
                  if (v2c_write_fp != 0) begin
                     $display("mode=%0d address=%08x data_w=%08x", mode, address, data_w);
                     if (mode == `F) begin // Finish request
                        `uvm_info("SEQ", "Finish request received", UVM_LOW)
                        $fclose(c2v_read_fp);
                        $fclose(v2c_write_fp);
                        return;
                     end
                     else if (mode == `R) begin // Read request
                        iob_transaction trans;
                        trans = iob_transaction::type_id::create("trans");
                        if (trans == null) `uvm_fatal("SEQ", "Transaction creation failed!")
                        trans.addr =  `IOB_WORD_ADDRESS(address);
                        trans.wstrb = 0;
                        start_item(trans);
                        finish_item(trans);
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w, trans.data);
                        `uvm_info("SEQ", $sformatf("Write to file: ack=%08x mode=%08x address=%08x data_w=%08x data=%08x", ack, mode, address, data_w, trans.data), UVM_LOW)
                     end
                     else if (mode == `W) begin // Write request
                        iob_transaction trans;
                        trans = iob_transaction::type_id::create("trans");
                        trans.addr =  `IOB_WORD_ADDRESS(address);
                        trans.data = `IOB_GET_WDATA(address, data);
                        trans.wstrb = `IOB_GET_WSTRB(address, data_w);
                        start_item(trans);
                        finish_item(trans); #1;
                        
                        `uvm_info("SEQ", "finish item", UVM_LOW)
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w, `IOB_GET_RDATA(address, data, data_w));
                        `uvm_info("SEQ", $sformatf("Write to file: ack=%08x mode=%08x address=%08x data_w=%08x data=%08x", ack, mode, address, data_w, data), UVM_LOW)
                     end
                     $fclose(v2c_write_fp);
                  end // if (v2c_write_fp != 0)
                  $display("Write to file failed");
                  ack = ack + 1;
               end
            end
            $fclose(c2v_read_fp);
            `uvm_info("SEQ", "Read from file failed", UVM_LOW)
         end 
      end
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

   reg clk;
   reg arst;

   iob_if iob_if(clk);

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

   initial begin
   `ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
   `endif
   end

   initial begin
      clk = 0;
      forever #5 clk = ~clk;
   end

   initial begin
      arst = 0;
      #10;
      arst = 1;
      #10;
      arst = 0;
   end

   initial begin
      uvm_config_db#(virtual iob_if)::set(null, "*", "vif", iob_if);
      `uvm_info("TB", "Starting UVM Test", UVM_LOW)
      run_test("iob_test");
      $display("run_test FINISHED");
      `uvm_info("TB", "UVM Test Completed", UVM_LOW)
   end
endmodule
