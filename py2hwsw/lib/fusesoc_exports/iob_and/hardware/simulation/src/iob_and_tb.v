// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

// verilator coverage_off
module iob_and_tb;

   reg     [1:0] data_i = 0;
   wire          data_o;

   integer       i;
   integer       fp;

   initial begin

      for (i = 0; i < 5; i = i + 1) begin
         #10 data_i = i[1:0];
         #10 $display("data_i = %b, data_o = %b", data_i, data_o);
      end
      #10 $display("%c[1;34m", 8'd27);
      $display("Test completed successfully.");
      $display("%c[0m", 8'd27);

      fp = $fopen("test.log", "w");
      $fdisplay(fp, "Test passed!");

      $finish();
   end

   iob_and #(
      .W(1)
   ) iob_and_inst (
      .a_i(data_i[0]),
      .b_i(data_i[1]),
      .y_o(data_o)
   );

endmodule
// verilator coverage_on
