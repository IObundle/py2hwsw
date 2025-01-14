`timescale 1ns / 1ps

`include "iob_eth_conf.vh"

module iob_eth_tx (
   input             arst_i,

   // Buffer interface
   output reg [10:0] addr_o,
   input [ 7:0]      data_i,

   // DMA control interface
   input             send_i,
   output reg        ready_o,
   input [10:0]      nbytes_i,
   input             crc_en_i,

   // MII interface
   input             tx_clk_i,
   output reg        tx_en_o,
   output reg [ 3:0] tx_data_o
   );

   function automatic [7:0] reverse_byte;
      input [7:0]                    word;
      integer                        i;

      begin
         for (i = 0; i < 8; i = i + 1) reverse_byte[i] = word[7-i];
      end
   endfunction

   // state
   reg  [ 3:0] pc;

   // crc
   reg         crc_en_int;
   wire [31:0] crc_value;
   wire [31:0] crc_out;

   //
   // TRANSMITTER PROGRAM
   //
   always @(posedge tx_clk_i, posedge arst_i)
     if (arst_i) begin
        pc      <= 0;
        crc_en_int  <= 0;
        addr_o    <= 0;
        ready_o   <= 1;
        tx_en_o   <= 0;
        tx_data_o <= 0;
     end else begin

        pc     <= pc + 1'b1;
        addr_o   <= addr_o + pc[0];
        crc_en_int <= 0;

        case (pc)

          0:
            if (send_i) ready_o <= 0;
            else pc <= pc;

          1: begin
             tx_en_o   <= 1;
             tx_data_o <= data_i[3:0];
          end

          2: begin  // Addr is different here, but data only changes in the next cycle
             tx_data_o <= data_i[7:4];
             if (addr_o != (`IOB_ETH_PREAMBLE_LEN + 1)) pc <= pc - 1'b1;
             else crc_en_int <= 1;
          end

          3: tx_data_o <= data_i[3:0];

          4: begin
             tx_data_o <= data_i[7:4];
             if (addr_o < nbytes_i) begin
                crc_en_int <= 1;
                pc     <= pc - 1'b1;
             end
             else if (!crc_en_i)
               pc     <= 13;
          end

          5: tx_data_o <= crc_out[27:24];

          6: tx_data_o <= crc_out[31:28];

          7: tx_data_o <= crc_out[19:16];

          8: tx_data_o <= crc_out[23:20];

          9: tx_data_o <= crc_out[11:8];

          10: tx_data_o <= crc_out[15:12];

          11: tx_data_o <= crc_out[3:0];

          12: tx_data_o <= crc_out[7:4];

          13: begin
             tx_en_o <= 0;
             pc    <= 0;
             ready_o <= 1;
             addr_o  <= 0;
          end

          default: begin
             pc      <= 0;
             crc_en_int  <= 0;
             addr_o    <= 0;
             ready_o   <= 1;
             tx_en_o   <= 0;
             tx_data_o <= 0;
          end

        endcase
     end

   //
   // CRC MODULE
   //

   iob_eth_crc crc_tx (
                       .clk_i(tx_clk_i),
                       .arst_i(arst_i),

                       .start_i(pc == 0),

                       .data_i(data_i),
                       .data_en_i(crc_en_int),
                       .crc_o(crc_value)
                       );

   assign crc_out = ~{reverse_byte(
                                   crc_value[31:24]
                                   ), reverse_byte(
                                                   crc_value[23:16]
                                                   ), reverse_byte(
                                                                   crc_value[15:8]
                                                                   ), reverse_byte(
                                                                                   crc_value[7:0]
                                                                                   )};
endmodule
