`timescale 1ns / 1ps

`define R 0
`define W 1
`define F 2

module iob_testbench;

   // Signals (examples - adjust as needed for your design)
   reg clk;
   reg rst;
   
   // File handles
   integer c2v_read_fp = 0;
   integer v2c_write_fp = 0;
   
   // Variables
   integer req=0, ack=0, mode=0, address=0, data=0;
  

   // Example test sequence (replace with your actual test logic)
   initial begin


      //////////////////////////

      clk = 0;
      rst = 1;
      #10;
      rst = 0;
      #10;

      mode = 0;
      
      //create the v2c file
      v2c_write_fp = $fopen("v2c.txt", "wb");
      if (v2c_write_fp == 0) begin
         $display("V: Error opening v2c.txt for writing!");
         $finish;
      end
      $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", -10, mode, address, data);
      $display("V: v2c.txt created");
      $fclose(v2c_write_fp);

      //wait for the c2v file to be created
      while (c2v_read_fp == 0) 
        c2v_read_fp = $fopen("c2v.txt", "rb"); 
      $fclose(c2v_read_fp);
      
      // Server loop
      while(1) begin
         c2v_read_fp = $fopen("c2v.txt", "rb"); 
         //$display("V: c2v.txt opened for reading!");
         while (c2v_read_fp && $fscanf(c2v_read_fp, "%08x %08x %08x %08x", req, mode, address, data) != 4);
         //$display("V: req=%d, mode=%d, address=%08x, data=%08x", req, mode, address, data);
         $fclose(c2v_read_fp);
         c2v_read_fp = 0;

         if(mode == `F) begin
            //finish
            $display("V: Finish");
            $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", req, mode, address, data);
            $fclose(v2c_write_fp);
            $fclose(c2v_read_fp);
            $finish;
         end


         //$display("V: req=%d, mode=%d, address=%08x, data=%08x", req, mode, address, data);
         if(req == ack) begin
            if(mode == `R) begin
               $display("V: Read address=%08x", address);
               //send ack  and data
               v2c_write_fp = $fopen("v2c.txt", "wb");
               $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", ack, mode, address, data);
               $fclose(v2c_write_fp);
               ack = ack+1;
            end
            else if(mode == `W) begin
               $display("V: Write address=%08x, data=%08x", address, data);               
               //send ack
               v2c_write_fp = $fopen("v2c.txt", "wb");
               $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", ack, mode, address, data);
               $fclose(v2c_write_fp);
               ack = ack+1;
            end
         end
      end
   end
   always #5 clk = ~clk; // Clock generation
   
endmodule
