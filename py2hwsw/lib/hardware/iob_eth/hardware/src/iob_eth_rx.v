`timescale 1ns / 1ps

`include "iob_eth_conf.vh"

module iob_eth_rx (
   input arst_i,

   // Buffer interface
   output reg        wr_o,
   output reg [10:0] addr_o,
   output reg [ 7:0] data_o,

   // DMA control interface
   input             rcv_ack_i,
   output reg data_rcvd_o,
   output            crc_err_o,

   // MII interface
   input       rx_clk_i,
   input       rx_dv_i,
   input [3:0] rx_data_i
);

   // Register MII inputs

   wire rx_dv;
   iob_reg #(
      .DATA_W (1),
      .RST_VAL(0)
   ) rx_dv_reg (
      .clk_i (rx_clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .data_i(rx_dv_i),
      .data_o(rx_dv)
   );

   wire [3:0] rx_data;
   iob_reg #(
      .DATA_W (4),
      .RST_VAL(0)
   ) rx_data_reg (
      .clk_i (rx_clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .data_i(rx_data_i),
      .data_o(rx_data)
   );


   // state
   reg  [ 2:0] pc;
   reg  [47:0] dest_mac_addr;

   // data
   wire [ 7:0] data_int;

   wire [31:0] crc_sum;

   //
   // RECEIVER PROGRAM
   //
   always @(posedge rx_clk_i, posedge arst_i)

      if (arst_i) begin
         pc            <= 0;
         addr_o          <= 0;
         dest_mac_addr <= 0;
         wr_o            <= 0;
         data_rcvd_o     <= 0;
      end else begin

         pc   <= pc + 1'b1;
         addr_o <= addr_o + pc[0];
         wr_o   <= 0;

         case (pc)

            0: if (data_int != `IOB_ETH_SFD || !rx_dv) pc <= pc;

            1: addr_o <= 0;

            2: begin
               dest_mac_addr <= {dest_mac_addr[39:0], data_int};
               wr_o            <= 1;
            end

            3:
            if (addr_o != (`IOB_ETH_MAC_ADDR_LEN - 1)) begin
               pc <= pc - 1'b1;
            end

            4: wr_o <= 1;

            5:
            if (rx_dv) begin
               pc <= pc - 1'b1;
            end

            6: begin
               pc        <= pc;
               data_rcvd_o <= 1;
               if (rcv_ack_i) begin
                  pc        <= 0;
                  addr_o      <= 0;
                  data_rcvd_o <= 0;
               end
            end

            // Wait for DV to deassert
            7:
            if (rx_dv) pc <= pc;
            else pc <= 0;

            default: pc <= 0;

         endcase
      end

   // capture RX_DATA
   assign data_int = {rx_data, data_o[7:4]};
   always @(posedge rx_clk_i, posedge arst_i)
      if (arst_i) data_o <= 0;
      else if (rx_dv) data_o <= data_int;

   //
   // CRC MODULE
   //
   iob_eth_crc crc_rx (
      .clk_i(rx_clk_i),
      .arst_i(arst_i),

      .start_i(pc == 0),

      .data_i(data_o),
      .data_en_i(wr_o),
      .crc_o(crc_sum)
   );

   wire crc_err = crc_sum != 32'hc704dd7b;
   iob_reg #(
      .DATA_W (1),
      .RST_VAL(0)
   ) crc_err_reg (
      .clk_i (rx_clk_i),
      .arst_i(arst_i),
      .cke_i (1'b1),
      .data_i(crc_err),
      .data_o(crc_err_o)
   );

endmodule
