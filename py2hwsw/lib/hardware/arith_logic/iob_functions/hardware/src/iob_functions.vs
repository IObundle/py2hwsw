// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

function [31:0] iob_max;
   input [31:0] a;
   input [31:0] b;
   begin
      if (a > b) iob_max = a;
      else iob_max = b;
   end
endfunction

function [31:0] iob_min;
   input [31:0] a;
   input [31:0] b;
   begin
      if (a < b) iob_min = a;
      else iob_min = b;
   end
endfunction

function [31:0] iob_cshift_left;
   input [31:0] DATA;
   input integer DATA_WIDTH;
   input integer SHIFT;
   begin
      iob_cshift_left = (DATA << SHIFT) | (DATA >> (DATA_WIDTH - SHIFT));
   end
endfunction

function [31:0] iob_cshift_right;
   input [31:0] DATA;
   input integer DATA_WIDTH;
   input integer SHIFT;
   begin
      iob_cshift_right = (DATA >> SHIFT) | (DATA << (DATA_WIDTH - SHIFT));
   end
endfunction

function integer iob_abs;
   input integer a;
   begin
      iob_abs = (a >= 0) ? a : -a;
   end
endfunction

function integer iob_sign;
   input integer a;
   begin
      if (a < 0)
        iob_sign = -1;
      else
        iob_sign = 1;
   end
endfunction
