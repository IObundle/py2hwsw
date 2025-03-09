package iob_uvm_pkg;
//`include "uvm_macros.svh"
//import uvm_pkg::*;
`include "iob_v_tb.vh"
`include "iob_uvm_seq.sv"
`include "iob_uvm_mon.sv"
`include "iob_uvm_drv.sv"
`include "iob_uvm_agt.sv"
`include "iob_uvm_scb.sv"

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
      super.connect_phase(phase);
   endfunction

endclass

// Define the test
class iob_test extends uvm_test;
   `uvm_component_utils(iob_test)

   iob_env env;

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      env = iob_env::type_id::create(.name("env"), .parent(this));
   endfunction: build_phase
   
   task run_phase(uvm_phase phase);
      iob_sequence iob_seq;
      
      phase.raise_objection(.obj(this));
      iob_seq = iob_sequence::type_id::create(.name("seq"), .contxt(get_full_name()));
      assert(iob_seq.randomize());
      iob_seq.start(env.agent.iob_seqr);
      phase.drop_objection(.obj(this));
   endtask: run_phase
endclass

endpackage
