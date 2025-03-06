`ifndef IOB_V_TB_UVM
`define IOB_V_TB_UVM

`include "uvm_macros.svh"
import uvm_pkg::*;

// Transaction Class
class iob_transaction extends uvm_sequence_item;
    rand bit iob_valid_i;
    rand bit [31:0] iob_wdata_i;
    rand bit [`IOB_CSRS_ADDR_W-1:0] iob_addr_i;
    rand bit [3:0] iob_wstrb_i;
    bit iob_rvalid_o;
    bit [31:0] iob_rdata_o;

    `uvm_object_utils(iob_transaction)
    
    function new(string name = "iob_transaction");
        super.new(name);
    endfunction
endclass

// Driver Class
class iob_driver extends uvm_driver #(iob_transaction);
    `uvm_component_utils(iob_driver)
    
    virtual iob_if vif;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if(!uvm_config_db#(virtual iob_if)::get(this, "", "vif", vif))
            `uvm_fatal(get_type_name(), "Virtual interface not set")
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            seq_item_port.get_next_item(req);
            vif.iob_valid_i = req.iob_valid_i;
            vif.iob_wdata_i = req.iob_wdata_i;
            vif.iob_addr_i  = req.iob_addr_i;
            vif.iob_wstrb_i = req.iob_wstrb_i;
            seq_item_port.item_done();
        end
    endtask
endclass

// Monitor Class
class iob_monitor extends uvm_monitor;
    `uvm_component_utils(iob_monitor)
    
    virtual iob_if vif;
    uvm_analysis_port #(iob_transaction) mon_ap;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if(!uvm_config_db#(virtual iob_if)::get(this, "", "vif", vif))
            `uvm_fatal(get_type_name(), "Virtual interface not set")
        mon_ap = new("mon_ap", this);
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            iob_transaction tr = new();
            tr.iob_rvalid_o = vif.iob_rvalid_o;
            tr.iob_rdata_o  = vif.iob_rdata_o;
            mon_ap.write(tr);
        end
    endtask
endclass

// Agent Class
class iob_agent extends uvm_agent;
    `uvm_component_utils(iob_agent)
    
    iob_driver drv;
    iob_monitor mon;
    uvm_sequencer #(iob_transaction) seqr;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        drv = iob_driver::type_id::create("drv", this);
        mon = iob_monitor::type_id::create("mon", this);
        seqr = uvm_sequencer#(iob_transaction)::type_id::create("seqr", this);
    endfunction
endclass

// Environment Class
class iob_env extends uvm_env;
    `uvm_component_utils(iob_env)
    
    iob_agent agt;
    
    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        agt = iob_agent::type_id::create("agt", this);
    endfunction
endclass

// Test Class
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
endclass

`endif
