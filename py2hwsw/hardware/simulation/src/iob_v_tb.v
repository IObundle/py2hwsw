// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

`include "iob_v_tb.vh"

`define R 0
`define W 1
`define F 2


`define IOB_GET_NBYTES(WIDTH) (WIDTH/8 + |(WIDTH%8))

`define IOB_BYTE_OFFSET(ADDR) (ADDR%(32/8))

`define IOB_GET_WDATA(ADDR, DATA) (DATA<<(8*`IOB_BYTE_OFFSET(ADDR)))
`define IOB_GET_WSTRB(ADDR, WIDTH) (((1<<`IOB_GET_NBYTES(WIDTH))-1)<<`IOB_BYTE_OFFSET(ADDR))
`define IOB_GET_RDATA(ADDR, DATA, WIDTH) ((DATA>>(8*`IOB_BYTE_OFFSET(ADDR)))&((1<<WIDTH)-1))



module iob_v_tb;

   // Signals (examples - adjust as needed for your design)
   reg                            clk;
   reg                            cke;
   reg                            arst;

   //iob interface (backend)
   reg                            iob_valid_i;
   reg     [                31:0] iob_wdata_i;
   reg     [`IOB_CSRS_ADDR_W-1:0] iob_addr_i;
   reg     [                 3:0] iob_wstrb_i;
   wire                           iob_rvalid_o;
   wire    [                31:0] iob_rdata_o;
   wire                           iob_ready_o;

   // File handles
   integer                        c2v_read_fp = 0;
   integer                        v2c_write_fp = 0;

   // Variables
   integer req = -100, ack = 0, mode = -100, address = -100, data = -100, data_w = -100;

   // Example test sequence (replace with your actual test logic)
   initial begin
`ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
`endif
      iob_valid_i  = 0;
      iob_wdata_i  = 0;
      iob_addr_i   = 0;
      iob_wstrb_i  = 0;

      clk          = 0;
      cke          = 1;
      arst         = 0;
      #10;
      arst = 1;
      #10;
      arst = 0;
      #10;

      // Open IPC files
      c2v_read_fp = $fopen("c2v.txt", "rb");
      if (c2v_read_fp == 0) begin
         $display("Error: Could not open c2v.txt");
         $finish;
      end
      $fclose(c2v_read_fp);
      v2c_write_fp = $fopen("v2c.txt", "wb");
      if (v2c_write_fp == 0) begin
         $display("Error: Could not open v2c.txt");
         $finish;
      end

      // Server loop
      while (1) begin
         //read request
         c2v_read_fp = $fopen("c2v.txt", "rb");
         if ($fscanf(
                 c2v_read_fp, "%08x %08x %08x %08x %08x\n", req, mode, address, data_w, data
             )) begin
            cke= 1;  // Enable clock
            $fclose(c2v_read_fp);
            /*$display("V: req=%08x mode=%08x address=%08x data_w=%08x data=%08x", req, mode,
                     address, data_w, data);*/  // DEBUG
            //check if request number matches with ack number
            if (req == ack) begin
               //process request
               if (mode == `F) begin  //finish request
                  $display("V: finish request");
                  $finish;
               end
               if (mode == `R) begin  //read request
                  iob_read(address, data, data_w);
                  //send ack  and data
                  $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w,
                            data);
                  $fflush(v2c_write_fp);
                  //$display("V: read request: ack=%d adress=%08x data=%08x", ack, address, data); // DEBUG
               end else if (mode == `W) begin  //write request
                  iob_write(address, data, data_w);
                  //send ack
                  $fdisplay(v2c_write_fp, "%08x %08x %08x %08x %08x", ack, mode, address, data_w,
                            data);
                  $fflush(v2c_write_fp);
                  // $display("V: write request: ack=%d adress=%08x data=%08x", ack, address, data); // DEBUG
               end
               ack = ack + 1;
            end  // if (req == ack)
         end else begin  // if (fscanf_ret == 5)
            $fclose(c2v_read_fp);
            cke=0;  // Disable clock
         end  // if (fscanf_ret != 5)
         @(posedge clk);  //advance clock
      end  // while (1)
      $fclose(v2c_write_fp);
   end  // initial begin



   // Instantiate the Unit Under Test (UUT)
   iob_uut uut (
      .clk_i (clk),
      .arst_i(arst),
      .cke_i (cke),

      .iob_valid_i (iob_valid_i),
      .iob_addr_i  (iob_addr_i),
      .iob_wdata_i (iob_wdata_i),
      .iob_wstrb_i (iob_wstrb_i),
      .iob_rvalid_o(iob_rvalid_o),
      .iob_rdata_o (iob_rdata_o),
      .iob_ready_o (iob_ready_o)
   );

   // Write data to IOb Native subordinate
   task iob_write;
      input [`IOB_CSRS_ADDR_W-1:0] addr;
      input [31:0] data;
      input [$clog2(32):0] width;

      begin
         @(posedge clk) #1 iob_valid_i = 1;  //sync and assign
         iob_addr_i  = addr;
         iob_wdata_i = `IOB_GET_WDATA(addr, data);
         iob_wstrb_i = `IOB_GET_WSTRB(addr, width);

         #1 while (!iob_ready_o) #1;

         @(posedge clk) iob_valid_i = 0;
         iob_wstrb_i = 0;
      end
   endtask

   // Read data from IOb Native subordinate
   task iob_read;
      input [`IOB_CSRS_ADDR_W-1:0] addr;
      output [31:0] data;
      input [$clog2(32):0] width;

      begin
         @(posedge clk) #1 iob_valid_i = 1;
         iob_addr_i  = addr;
         iob_wstrb_i = 0;

         #1 while (!iob_ready_o) #1;
         @(posedge clk) #1 iob_valid_i = 0;

         while (!iob_rvalid_o) #1;
         data = #1 `IOB_GET_RDATA(addr, iob_rdata_o, width);
      end
   endtask



   always if (cke) #5 clk = ~clk;  // Clock generation

endmodule
