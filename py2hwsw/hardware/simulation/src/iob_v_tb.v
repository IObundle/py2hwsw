`timescale 1ns / 1ps

module iob_testbench;

   // Signals (examples - adjust as needed for your design)
   reg clk;
   reg rst;
   
   // File handles
   integer c2v_read_fp;
   integer v2c_write_fp;
   
   // Variables
   reg [31:0] c2v_address;
   reg [31:0] c2v_data;
   reg [31:0] v2c_address;
   reg [31:0] v2c_data;
   reg        mode;
   


   // Example test sequence (replace with your actual test logic)
   initial begin

      //open files for reading and writing
      c2v_read_fp = $fopen("c2v.txt", "r");
      if (c2v_read_fp == 0) begin
        $display("Error opening c2v.txt for reading!");
        $finish;
      end

      v2c_write_fp = $fopen("v2c.txt", "a"); // Append mode!
      if (v2c_write_fp == 0) begin
        $display("Error opening v2c.txt for writing!");
        $finish;
      end
      
      clk = 0;
      rst = 1;
      #10;
      rst = 0;
      #10;

      mode = 0;
      
      // Example interaction with C code
      while(mode != 2) begin //Check if C program finished sending data
         while ($feof(c2v_read_fp));
         $fscanf(c2v_read_fp, "%d %d %d", mode, c2v_address, c2v_data);
         $display("Verilog read Mode=%d Addr=%d, Data=%d", mode, c2v_address, c2v_data);
         $fwrite(v2c_write_fp, "%d %d\n", v2c_address, v2c_data);
      end
      
      $finish;
   end
   
   always #5 clk = ~clk; // Clock generation
   
endmodule
