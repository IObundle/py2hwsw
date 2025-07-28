`timescale 1ns / 1ps

module xunitM #(
         parameter DELAY_W = 7,
         parameter DATA_W = 32
              )
    (
    //control
    input               clk,
    input               rst,
    
    input               running,
    input               run,
    output              done,

    //input / output data
    input [DATA_W-1:0]  in0,

    (* versat_latency = 17 *) output reg [DATA_W-1:0] out0,

    //configurations
    input [DELAY_W-1:0]         delay0 // Encodes delay
    );

assign done = 1'b1;

reg [DELAY_W-1:0] delay;
reg [4:0] latency;
reg [31:0] w[15:0];

// Extract from array to view on gtkwave
wire [31:0] w0 = w[0];
wire [31:0] w1 = w[1];
wire [31:0] w2 = w[2];
wire [31:0] w3 = w[3];
wire [31:0] w4 = w[4];
wire [31:0] w5 = w[5];
wire [31:0] w6 = w[6];
wire [31:0] w7 = w[7];
wire [31:0] w8 = w[8];
wire [31:0] w9 = w[9];
wire [31:0] w10 = w[10];
wire [31:0] w11 = w[11];
wire [31:0] w12 = w[12];
wire [31:0] w13 = w[13];
wire [31:0] w14 = w[14];
wire [31:0] w15 = w[15];

function [31:0] ROTR_32(input [31:0] x,input [4:0] c);
begin
   ROTR_32 = (((x) >> (c)) | ((x) << (32 - (c))));
end
endfunction

function [31:0] SHR(input [31:0] x,input [4:0] c); 
begin
   SHR = ((x) >> (c));
end
endfunction

function [31:0] sigma0_32(input [31:0] x);
begin
   sigma0_32 = (ROTR_32(x, 7) ^ ROTR_32(x,18) ^ SHR(x, 3));
end
endfunction

function [31:0] sigma1_32(input [31:0] x);
begin
   sigma1_32 = (ROTR_32(x,17) ^ ROTR_32(x,19) ^ SHR(x,10));
end
endfunction

wire [31:0] val = (sigma1_32(w[14]) + (w[9]) + sigma0_32(w[1]) + (w[0]));

integer i;
always @(posedge clk,posedge rst)
begin
   if(rst) begin
      delay <= 0;
      for(i = 0; i < 16; i = i + 1) 
         w[i] <= 0;
   end else if(run) begin
      delay <= delay0; // wait delay0 cycles for valid input data
      latency <= 5'h11; // cycles from valid input to valid output
   end else if (|delay) begin
     delay <= delay - 1;
   end else begin
      if(|latency) begin
         latency <= latency - 1;
      end

      out0 <= w[0];

      for(i = 0; i < 15; i = i + 1) begin
         w[i] <= w[i+1];
      end

      if(latency[4:1] != 0) begin // latency > 1
         w[15] <= in0;
      end else begin
         w[15] <= val;
      end
      
      out0 <= val;
   end
end

endmodule
