class iob_monitor extends uvm_monitor;

   `uvm_component_utils(iob_monitor)

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction

   uvm_analysis_port #(iob_transaction) ap;
   
   virtual iob_if vif;
   

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);

      void'(uvm_resource_db#(virtual iob_if)::read_by_name
	    (.scope("ifs"), .name("iob_if"), .val(vif)));
      ap = new(.name("ap"), .parent(this));
   endfunction

   virtual task run_phase(uvm_phase phase);

      iob_transaction trans;
      trans = iob_transaction::type_id::create
	      (.name("trans"), .contxt(get_full_name()));
       

      forever begin
         @(posedge vif.clk);
         if (vif.iob_rvalid_o) begin
            trans.rdata = vif.iob_rdata_o;
            ap.write(trans);
            `uvm_info("MON", $sformatf("Monitored transaction: addr=%08x data=%08x", trans.rdata), UVM_LOW)
         end
      end
   endtask
endclass
