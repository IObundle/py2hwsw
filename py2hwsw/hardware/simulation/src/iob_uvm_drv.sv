/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

class iob_driver extends uvm_driver #(iob_transaction);
   `uvm_component_utils(iob_driver)

   virtual iob_if vif; // Virtual interface for driving signals

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);

      void'(uvm_resource_db#(virtual iob_if)::read_by_name
	    (.scope("ifs"), .name("iob_if"), .val(vif)));
   endfunction

   virtual task run_phase(uvm_phase phase);
      // Wait for reset to complete
      @(posedge vif.arst_i);
      @(negedge vif.arst_i);
      @(posedge vif.clk_i);
      `uvm_info("IOB_DRIVER", "Reset sequence complete, starting transactions", UVM_MEDIUM);
      drive();
   endtask // run_phase

   virtual task drive();
      iob_transaction trans;

      vif.iob_valid_i <= 1'd0;
      vif.iob_addr_i <= 32'd0;
      vif.iob_wdata_i <= 32'd0;
      vif.iob_wstrb_i <= 4'd0;
      
      forever begin

         // Get the next transaction from the sequencer
         //`uvm_info("DRV", "Waiting next item...", UVM_MEDIUM);
         seq_item_port.get_next_item(trans);
         //`uvm_info("DRV", "Received item", UVM_MEDIUM);

         // Drive the transaction to the DUT
         //`uvm_info("DRV", "Driving transaction to DUT", UVM_MEDIUM);
         vif.iob_valid_i = 1; // Assert valid signal
         vif.iob_addr_i  = trans.addr; // Use macro for address alignment
         vif.iob_wdata_i = trans.wdata; // Use macro for data shifting
         vif.iob_wstrb_i = trans.wstrb; // Use macro for strobe generation
         `uvm_info("DRV", $sformatf("Driving transaction to DUT: addr=%08x, wdata=%08x, wstrb=%08x", vif.iob_addr_i, vif.iob_wdata_i, vif.iob_wstrb_i), UVM_MEDIUM);
         while (!vif.iob_ready_o) @(posedge vif.clk_i);

         vif.iob_valid_i = 0;

         // If it's a read transaction, wait for iob_rvalid_o
         if (trans.wstrb == 0) begin
            while (!vif.iob_rvalid_o) @(posedge vif.clk_i);
            trans.rdata = vif.iob_rdata_o; // Capture read data
         end

          @(posedge vif.clk_i);
         //`uvm_info("DR", "Transaction done", UVM_MEDIUM);
         
         // Signal that the transaction is complete
         //`uvm_info("DRV", "Before item_done", UVM_LOW)
         seq_item_port.item_done();
         //`uvm_info("DRV", "After item_done", UVM_LOW)
      end
   endtask
 
endclass

