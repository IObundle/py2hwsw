// SPDX-FileCopyrightText: 2024 IObundle
//
// SPDX-License-Identifier: MIT

module BUF(A, Y);
input A;
output Y = A;
endmodule

module NOT(A, Y);
input A;
output Y = ~A;
endmodule

module MUX(A, B, S, Y);
input A;
input B;
input S;
output Y = (S & B) | (~S & A);
endmodule

module NAND(A, B, Y);
input A, B;
output Y = ~(A & B);
endmodule

module AND(A, B, Y);
input A, B;
output Y = (A & B);
endmodule

module NOR(A, B, Y);
input A, B;
output Y = ~(A | B);
endmodule

module OR(A, B, Y);
input A, B;
output Y = (A | B);
endmodule

module DFFAR(AR, C, D, Q);
input C, D, AR;
output reg Q;
always @(posedge C or posedge AR)
   if (AR)
      Q <= 1'b0;
   else
	Q <= D;
endmodule

module DFFP(P, C, D, Q);
input C, D, P;
output reg Q;
always @(posedge C or posedge AR)
   if (P)
      Q <= 1'b1;
   else
	Q <= D;
endmodule

