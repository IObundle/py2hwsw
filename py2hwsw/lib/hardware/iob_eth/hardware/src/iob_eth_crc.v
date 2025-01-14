`timescale 1ns / 1ps
module iob_eth_crc (
   input             arst_i,
   input             clk_i,
   input             start_i,
   input      [ 7:0] data_i,
   input             data_en_i,
   output reg [31:0] crc_o
);

   function static [31:0] crc_nxt;
      input [7:0] D;
      input [31:0] C;
      reg [31:0] crc;
      begin
         crc[0] = C[24] ^ C[30] ^ D[1] ^ D[7];
         crc[1] = C[25] ^ C[31] ^ D[0] ^ D[6] ^ C[24] ^ C[30] ^ D[1] ^ D[7];
         crc[2] = C[26] ^ D[5] ^ C[25] ^ C[31] ^ D[0] ^ D[6] ^ C[24] ^ C[30] ^ D[1] ^ D[7];
         crc[3] = C[27] ^ D[4] ^ C[26] ^ D[5] ^ C[25] ^ C[31] ^ D[0] ^ D[6];
         crc[4] = C[28] ^ D[3] ^ C[27] ^ D[4] ^ C[26] ^ D[5] ^ C[24] ^ C[30] ^ D[1] ^ D[7];
         crc[5]=C[29]^D[2]^C[28]^D[3]^C[27]^D[4]^C[25]^C[31]^D[0]^D[6]^C[24]^C[30]^D[1]^D[7];
         crc[6]=C[30]^D[1]^C[29]^D[2]^C[28]^D[3]^C[26]^D[5]^C[25]^C[31]^D[0]^D[6];
         crc[7] = C[31] ^ D[0] ^ C[29] ^ D[2] ^ C[27] ^ D[4] ^ C[26] ^ D[5] ^ C[24] ^ D[7];
         crc[8] = C[0] ^ C[28] ^ D[3] ^ C[27] ^ D[4] ^ C[25] ^ D[6] ^ C[24] ^ D[7];
         crc[9] = C[1] ^ C[29] ^ D[2] ^ C[28] ^ D[3] ^ C[26] ^ D[5] ^ C[25] ^ D[6];
         crc[10] = C[2] ^ C[29] ^ D[2] ^ C[27] ^ D[4] ^ C[26] ^ D[5] ^ C[24] ^ D[7];
         crc[11] = C[3] ^ C[28] ^ D[3] ^ C[27] ^ D[4] ^ C[25] ^ D[6] ^ C[24] ^ D[7];
         crc[12]=C[4]^C[29]^D[2]^C[28]^D[3]^C[26]^D[5]^C[25]^D[6]^C[24]^C[30]^D[1]^D[7];
         crc[13]=C[5]^C[30]^D[1]^C[29]^D[2]^C[27]^D[4]^C[26]^D[5]^C[25]^C[31]^D[0]^D[6];
         crc[14] = C[6] ^ C[31] ^ D[0] ^ C[30] ^ D[1] ^ C[28] ^ D[3] ^ C[27] ^ D[4] ^ C[26] ^ D[5];
         crc[15] = C[7] ^ C[31] ^ D[0] ^ C[29] ^ D[2] ^ C[28] ^ D[3] ^ C[27] ^ D[4];
         crc[16] = C[8] ^ C[29] ^ D[2] ^ C[28] ^ D[3] ^ C[24] ^ D[7];
         crc[17] = C[9] ^ C[30] ^ D[1] ^ C[29] ^ D[2] ^ C[25] ^ D[6];
         crc[18] = C[10] ^ C[31] ^ D[0] ^ C[30] ^ D[1] ^ C[26] ^ D[5];
         crc[19] = C[11] ^ C[31] ^ D[0] ^ C[27] ^ D[4];
         crc[20] = C[12] ^ C[28] ^ D[3];
         crc[21] = C[13] ^ C[29] ^ D[2];
         crc[22] = C[14] ^ C[24] ^ D[7];
         crc[23] = C[15] ^ C[25] ^ D[6] ^ C[24] ^ C[30] ^ D[1] ^ D[7];
         crc[24] = C[16] ^ C[26] ^ D[5] ^ C[25] ^ C[31] ^ D[0] ^ D[6];
         crc[25] = C[17] ^ C[27] ^ D[4] ^ C[26] ^ D[5];
         crc[26] = C[18] ^ C[28] ^ D[3] ^ C[27] ^ D[4] ^ C[24] ^ C[30] ^ D[1] ^ D[7];
         crc[27] = C[19] ^ C[29] ^ D[2] ^ C[28] ^ D[3] ^ C[25] ^ C[31] ^ D[0] ^ D[6];
         crc[28] = C[20] ^ C[30] ^ D[1] ^ C[29] ^ D[2] ^ C[26] ^ D[5];
         crc[29] = C[21] ^ C[31] ^ D[0] ^ C[30] ^ D[1] ^ C[27] ^ D[4];
         crc[30] = C[22] ^ C[31] ^ D[0] ^ C[28] ^ D[3];
         crc[31] = C[23] ^ C[29] ^ D[2];
         crc_nxt = crc;
      end
   endfunction

   always @(posedge clk_i or posedge arst_i)
      if (arst_i) crc_o <= 32'hffffffff;
      else if (start_i) crc_o <= 32'hffffffff;
      else if (data_en_i) crc_o <= crc_nxt(data_i, crc_o);

endmodule


