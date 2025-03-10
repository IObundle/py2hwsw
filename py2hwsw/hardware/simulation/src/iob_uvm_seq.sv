/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

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
   bit [`IOB_CSRS_ADDR_W-1:0] valid;
   bit [`IOB_CSRS_ADDR_W-1:0] addr;
   bit [31:0]                 wdata;
   bit [3:0]                  wstrb;
   bit [31:0]                 rdata;
   bit                        rvalid;
   bit                        ready;

   function new(string name = "iob_transaction");
      super.new(name);
   endfunction

   `uvm_object_utils_begin(iob_transaction)
      `uvm_field_int(valid, UVM_ALL_ON)
      `uvm_field_int(addr, UVM_ALL_ON)
      `uvm_field_int(wdata, UVM_ALL_ON)
      `uvm_field_int(wstrb, UVM_ALL_ON)
      `uvm_field_int(rdata, UVM_ALL_ON)
      `uvm_field_int(rvalid, UVM_ALL_ON)
      `uvm_field_int(ready, UVM_ALL_ON)
   `uvm_object_utils_end

endclass



// Define the sequence with file I/O
class iob_sequence extends uvm_sequence #(iob_transaction);
   `uvm_object_utils(iob_sequence)

   function new(string name = "");
      super.new(name);
   endfunction

   virtual task body();
      integer c2v_read_fp;
      integer v2c_write_fp;
      integer req = -100, ack = 0, mode = -100, address = -100, data = -100, data_w = -100;

      iob_transaction trans;
      trans = iob_transaction::type_id::create(.name("trans"), .contxt(get_full_name()));
      if (trans == null) `uvm_fatal("SEQ", "Transaction creation failed!")

      while (1) begin
         c2v_read_fp = $fopen("c2v.txt", "rb");
         if (c2v_read_fp != 0) begin
            if ($fscanf(c2v_read_fp, "%08x %08x %08x %08x %08x\n", req, mode, address, data_w, data)) begin
               if (req == ack) begin
                  `uvm_info("SEQ", $sformatf("Read c2v.txt file: req=%08x mode=%08x address=%08x data_w=%08x data=%08x", req, mode, address, data_w, data), UVM_LOW)
                  v2c_write_fp = $fopen("v2c.txt", "wb");
                  if (v2c_write_fp != 0) begin
                     if (mode == `F) begin // Finish request
                        `uvm_info("SEQ", "Finish request received", UVM_LOW)
                        $fclose(c2v_read_fp);
                        $fclose(v2c_write_fp);
                        return;
                     end
                     else if (mode == `R) begin // Read request
                        trans.valid = 1;
                        trans.addr =  `IOB_WORD_ADDRESS(address);
                        trans.wstrb = 0;
                        `uvm_info("SEQ", $sformatf("Read request received: addr=%08x wstrb=%08x", trans.addr, trans.wstrb), UVM_LOW)
                        start_item(trans);
                        //`uvm_info("SEQ", "Item started", UVM_LOW)
                        finish_item(trans);
                        //`uvm_info("SEQ", "Item finished", UVM_LOW)
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w, `IOB_GET_RDATA(address, trans.rdata, data_w));
                       `uvm_info("SEQ", $sformatf("Write v2c.txt file: ack=%08x mode=%08x address=%08x data_w=%08x data=%08x", ack, mode, address, data_w, trans.rdata), UVM_LOW)
                     end
                     else if (mode == `W) begin // Write request
                        trans.valid = 1;
                        trans.addr =  `IOB_WORD_ADDRESS(address);
                        trans.wdata = `IOB_GET_WDATA(address, data);
                        trans.wstrb = `IOB_GET_WSTRB(address, data_w);
                        `uvm_info("SEQ", $sformatf("Write request received: addr=%08x wdata=%08x wstrb=%08x data_w=%08x", trans.addr, trans.wdata, trans.wstrb, data_w), UVM_LOW)
                        start_item(trans);
                        //`uvm_info("SEQ", "Item started", UVM_LOW)
                        finish_item(trans);
                        //`uvm_info("SEQ", "Item finished", UVM_LOW)
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w, data);
                        `uvm_info("SEQ", $sformatf("Write v2c.txt file: ack=%08x mode=%08x address=%08x data_w=%08x data=%08x", ack, mode, address, data_w, data), UVM_LOW)
                     end
                     $fclose(v2c_write_fp);
                  end // if (v2c_write_fp != 0)
                  ack = ack + 1;
               end
            end
            $fclose(c2v_read_fp);
         end 
      end
   endtask
endclass

typedef uvm_sequencer#(iob_transaction) iob_sequencer;
