`timescale 1ns / 1ps

module xunitF #(
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
    input [DATA_W-1:0]  in1,
    input [DATA_W-1:0]  in2,
    input [DATA_W-1:0]  in3,
    input [DATA_W-1:0]  in4,
    input [DATA_W-1:0]  in5,
    input [DATA_W-1:0]  in6,
    input [DATA_W-1:0]  in7,

    input [DATA_W-1:0]  in8,
    input [DATA_W-1:0]  in9,

    (* versat_latency = 16 *) output [DATA_W-1:0] out0,
    (* versat_latency = 16 *) output [DATA_W-1:0] out1,
    (* versat_latency = 16 *) output [DATA_W-1:0] out2,
    (* versat_latency = 16 *) output [DATA_W-1:0] out3,
    (* versat_latency = 16 *) output [DATA_W-1:0] out4,
    (* versat_latency = 16 *) output [DATA_W-1:0] out5,
    (* versat_latency = 16 *) output [DATA_W-1:0] out6,
    (* versat_latency = 16 *) output [DATA_W-1:0] out7,

    //configurations
    input [DELAY_W-1:0]         delay0 // Encodes delay
    );

reg [DELAY_W-1:0] delay;
reg [31:0] a,b,c,d,e,f,g,h;

assign out0 = a;
assign out1 = b;
assign out2 = c;
assign out3 = d;
assign out4 = e;
assign out5 = f;
assign out6 = g;
assign out7 = h;

assign done = (delay == 0);

wire [31:0] w = in8;
wire [31:0] k = in9;

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

function [31:0] Ch(input [31:0] x,y,z);
begin
   Ch = (((x) & (y)) ^ (~(x) & (z)));
end
endfunction

function [31:0] Maj(input [31:0] x,y,z); 
begin 
   Maj = (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)));
end
endfunction

function [31:0] Sigma0_32(input [31:0] x);
begin
   Sigma0_32 = (ROTR_32(x, 2) ^ ROTR_32(x,13) ^ ROTR_32(x,22));
end
endfunction

function [31:0] Sigma1_32(input [31:0] x);
begin
   Sigma1_32 = (ROTR_32(x, 6) ^ ROTR_32(x,11) ^ ROTR_32(x,25));
end
endfunction

wire [31:0] T1 = h + Sigma1_32(e) + Ch(e,f,g) + k + w;
wire [31:0] T2 = Sigma0_32(a) + Maj(a,b,c);

wire [31:0] T1_init = in7 + Sigma1_32(in4) + Ch(in4,in5,in6) + k + w;
wire [31:0] T2_init = Sigma0_32(in0) + Maj(in0,in1,in2);

reg working;

always @(posedge clk,posedge rst)
begin
   if(rst) begin
      delay <= 0;
      working <= 0;
      a <= 0;
      b <= 0;
      c <= 0;
      d <= 0;
      e <= 0;
      f <= 0;
      g <= 0;
      h <= 0;
   end else if(run) begin
      delay <= delay0;
      working <= 0;
   end else if(!working) begin
      if(delay == 0) begin
         a <= T1_init + T2_init;
         b <= in0;
         c <= in1;
         d <= in2;
         e <= in3 + T1_init;
         f <= in4;
         g <= in5;
         h <= in6;
         working <= 1'b1;
      end else begin
         delay <= delay - 1;
      end
   end else begin
      a <= T1 + T2;
      b <= a;
      c <= b;
      d <= c;
      e <= d + T1;
      f <= e;
      g <= f;
      h <= g;
   end
end

endmodule
