`timescale 1ns / 1ps

module Mux4 #(
         parameter DATA_W = 32
      )
    (
    //control
    input                         clk,
    input                         rst,
    input                         running,

    input                         run,

    //input / output data
    input [DATA_W-1:0]            in0,
    input [DATA_W-1:0]            in1,
    input [DATA_W-1:0]            in2,
    input [DATA_W-1:0]            in3,

    (* versat_latency = 1 *) output reg [DATA_W-1:0]       out0,
    
    input [1:0]                   sel

    );


always @(posedge clk,posedge rst)
begin
   if(rst) begin
      out0 <= 0;
   end else begin
      case(sel)
      2'b00: out0 <= in0;
      2'b01: out0 <= in1;
      2'b10: out0 <= in2;
      2'b11: out0 <= in3;
      endcase
   end
end

endmodule
