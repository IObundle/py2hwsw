/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

class iob_agent extends uvm_agent;

   `uvm_component_utils(iob_agent)

   uvm_analysis_port#(iob_transaction) agent_ap;
   
   iob_sequencer iob_seqr;
   iob_driver iob_drvr;
   iob_monitor iob_mon;
   
   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction: new
   
   function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      
      agent_ap	= new(.name("agent_ap"), .parent(this));
      
      iob_seqr	= iob_sequencer::type_id::create(.name("iob_seqr"), .parent(this));
      iob_drvr	= iob_driver::type_id::create(.name("iob_drvr"), .parent(this));
      iob_mon	= iob_monitor::type_id::create(.name("iob_mon"), .parent(this));
   endfunction: build_phase
   
   function void connect_phase(uvm_phase phase);
      super.connect_phase(phase);
      iob_drvr.seq_item_port.connect(iob_seqr.seq_item_export);
      iob_mon.ap.connect(agent_ap);
   endfunction: connect_phase
   
endclass
