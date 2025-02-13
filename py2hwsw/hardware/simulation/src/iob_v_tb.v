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
   integer req=-100, ack=0, mode=-100, address=-100, data=-100;


   integer n=0;
   

   // Example test sequence (replace with your actual test logic)
   initial begin
      clk = 0;
      rst = 1;
      #10;
      rst = 0;
      #10;
      
      // Server loop
      while(n < 10000) begin
         //read request
         c2v_read_fp = $fopen("c2v.txt", "rb");
         if (c2v_read_fp != 0) begin
            if ($fscanf(c2v_read_fp, "%08x %08x %08x %08x\n", req, mode, address, data)) begin 
               $display("V: req=%08x mode=%08x address=%08x data=%08x", req, mode, address, data);

               //check if request number matches with ack number
               if(req == ack) begin
                  v2c_write_fp = $fopen("v2c.txt", "wb");
                  if (v2c_write_fp != 0) begin
                     //process request
                     if(mode == `F) begin //finish request
                        $display("V: finish request");
                        $finish;
                     end
                     if(mode == `R) begin //read request
                        //send ack  and data
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", ack, mode, address, data);
                        $display("V: read request: adress=%08x data=%08x", address, data);
                     end
                     else if(mode == `W) begin //write request
                        //send ack
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", ack, mode, address, data);
                        $display("V: write request: adress=%08x data=%08x", address, data);
                     end
                     $fclose(v2c_write_fp);
                  end // if (v2c_write_fp != 0)
                  ack = ack + 1;
               end // if (req == ack)
            end // if (fscanf_ret == 4)
            $fclose(c2v_read_fp);
         end // if (c2v_read_fp != 0)
         @(posedge clk);//advance clock
         n = n + 1;
      end // while (1)
   end // initial begin
   
   always #5 clk = ~clk; // Clock generation
   
endmodule
