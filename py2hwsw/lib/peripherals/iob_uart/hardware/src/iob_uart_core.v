// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_uart_csrs.vh"
`include "iob_uart_conf.vh"

module iob_uart_core (
   input                             clk_i,
   input                             arst_i,
   input                             rst_soft_i,
   input                             tx_en_i,
   input                             rx_en_i,
   input  [                     7:0] tx_data_i,
   output [                     7:0] rx_data_o,
   output                            tx_ready_o,
   output                            rx_ready_o,
   input                             rs232_rxd_i,
   output                            rs232_txd_o,
   input                             rs232_cts_i,
   output                            rs232_rts_o,
   input                             data_write_en_i,
   input                             data_read_en_i,
   input  [`IOB_UART_CSRS_DIV_W-1:0] bit_duration_i
);

   ////////////////////////////////////////////////////////
   // TX
   ////////////////////////////////////////////////////////

   //clear to send (cts) synchronizer
   wire cts_int;

   iob_sync #(
      .DATA_W(1)
   ) cts_sync (
      .clk_i   (clk_i),
      .arst_i  (arst_i),
      .signal_i(rs232_cts_i),
      .signal_o(cts_int)
   );

   wire txen;
   assign txen = tx_en_i & cts_int;

   wire [7:0] tx_data_int;
   iob_reg_cae #(
      .DATA_W (8),
      .RST_VAL(8'b0)
   ) txdata_reg (
      // clk_en_rst port
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .en_i  (data_write_en_i),
      // data_i port
      .data_i(tx_data_i),
      // data_o port
      .data_o(tx_data_int)
   );


   // sender
   wire [ 1:0] tx_pc;
   reg  [ 1:0] tx_pc_nxt;

   wire [ 9:0] tx_pattern;
   reg  [ 9:0] tx_pattern_nxt;  //stop(1) + data(8) + start(1) = 10 bits

   wire [ 3:0] tx_bitcnt;
   reg  [ 3:0] tx_bitcnt_nxt;

   wire [15:0] tx_cyclecnt;
   reg  [15:0] tx_cyclecnt_nxt;

   reg         tx_ready_nxt;

   iob_reg_care #(
      .DATA_W(2)
   ) tx_pc_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (txen),
      .data_i(tx_pc_nxt),
      .data_o(tx_pc)
   );

   iob_reg_care #(
      .DATA_W(1)
   ) tx_ready_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (txen),
      .data_i(tx_ready_nxt),
      .data_o(tx_ready_o)
   );

   iob_reg_care #(
      .DATA_W (10),
      .RST_VAL({10{1'b1}})
   ) tx_pattern_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (txen),
      .data_i(tx_pattern_nxt),
      .data_o(tx_pattern)
   );
   assign rs232_txd_o = tx_pattern[0];

   iob_reg_care #(
      .DATA_W(4)
   ) tx_bitcnt_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (txen),
      .data_i(tx_bitcnt_nxt),
      .data_o(tx_bitcnt)
   );

   iob_reg_care #(
      .DATA_W(16)
   ) tx_cyclecnt_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (txen),
      .data_i(tx_cyclecnt_nxt),
      .data_o(tx_cyclecnt)
   );


   always @* begin
      tx_pc_nxt       = tx_pc + 2'd1;  //increment pc by default
      tx_pattern_nxt  = tx_pattern;
      tx_bitcnt_nxt   = tx_bitcnt;
      tx_cyclecnt_nxt = tx_cyclecnt;
      tx_ready_nxt    = tx_ready_o;

      case (tx_pc)

         0: begin  //wait for data to send
            tx_ready_nxt    = 1'b1;
            tx_bitcnt_nxt   = 4'd0;
            tx_cyclecnt_nxt = 16'd1;
            tx_pattern_nxt  = ~10'b0;
            if (!data_write_en_i) tx_pc_nxt = tx_pc;
            else tx_ready_nxt = 1'b0;
         end

         1: begin  //load tx pattern to send
            tx_pattern_nxt = {1'b1, tx_data_int[7:0], 1'b0};  //{stop, data, start}>>
         end

         default: begin  //send pattern
            tx_pc_nxt       = tx_pc;  //stay here util pattern sent
            tx_cyclecnt_nxt = tx_cyclecnt + 16'd1;  //increment cycle counter
            if (tx_cyclecnt == bit_duration_i)
               if (tx_bitcnt == 4'd9) begin  //stop bit sent sent
                  tx_pc_nxt = 2'd0;  //restart program 
               end else begin  //data bit sent
                  tx_pattern_nxt  = tx_pattern >> 1;
                  tx_bitcnt_nxt   = tx_bitcnt + 4'd1;  //send next bit
                  tx_cyclecnt_nxt = 16'd1;
               end
         end  // case: default
      endcase
   end  // always @*



        ////////////////////////////////////////////////////////
        // RX
        ////////////////////////////////////////////////////////

   wire [ 2:0] rx_pc;
   reg  [ 2:0] rx_pc_nxt;

   wire [15:0] rx_cyclecnt;
   reg  [15:0] rx_cyclecnt_nxt;

   wire [ 3:0] rx_bitcnt;
   reg  [ 3:0] rx_bitcnt_nxt;

   wire [ 7:0] rx_pattern;
   reg  [ 7:0] rx_pattern_nxt;

   reg         rx_ready_nxt;

   iob_reg_care #(
      .DATA_W(3)
   ) rx_pc_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (rx_en_i),
      .data_i(rx_pc_nxt),
      .data_o(rx_pc)
   );

   wire rxready_rst;
   assign rxready_rst = rst_soft_i | data_read_en_i;

   iob_reg_care #(
      .DATA_W(1)
   ) rx_ready_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rxready_rst),
      .en_i  (rx_en_i),
      .data_i(rx_ready_nxt),
      .data_o(rx_ready_o)
   );

   iob_reg_care #(
      .DATA_W(8)
   ) rx_pattern_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (rx_en_i),
      .data_i(rx_pattern_nxt),
      .data_o(rx_pattern)
   );

   iob_reg_care #(
      .DATA_W(4)
   ) rx_bitcnt_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (rx_en_i),
      .data_i(rx_bitcnt_nxt),
      .data_o(rx_bitcnt)
   );

   iob_reg_care #(
      .DATA_W (16),
      .RST_VAL(16'b1)
   ) rx_cyclecnt_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (rx_en_i),
      .data_i(rx_cyclecnt_nxt),
      .data_o(rx_cyclecnt)
   );


   reg rs232_rts_nxt;

   iob_reg_care #(
      .DATA_W(1)
   ) rts_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (rx_en_i),
      .data_i(rs232_rts_nxt),
      .data_o(rs232_rts_o)
   );

   reg [7:0] rx_data_nxt;

   iob_reg_care #(
      .DATA_W(8)
   ) rx_data_reg (
      .clk_i (clk_i),
      .cke_i (1'b1),
      .arst_i(arst_i),
      .rst_i (rst_soft_i),
      .en_i  (rx_en_i),
      .data_i(rx_data_nxt),
      .data_o(rx_data_o)
   );

   always @* begin
      rx_pc_nxt       = rx_pc + 3'd1;  //increment pc by default
      rx_cyclecnt_nxt = rx_cyclecnt;
      rx_bitcnt_nxt   = rx_bitcnt;
      rx_pattern_nxt  = rx_pattern;
      rx_ready_nxt    = rx_ready_o;

      rs232_rts_nxt   = rs232_rts_o;
      rx_data_nxt     = rx_data_o;

      case (rx_pc)

         0: begin  //sync up
            rs232_rts_nxt   = 1'b1;
            rx_ready_nxt    = 1'b0;
            rx_cyclecnt_nxt = 16'd1;
            rx_bitcnt_nxt   = 4'd0;
            if (!rs232_rxd_i)  //line is low, wait until it is high
               rx_pc_nxt = rx_pc;
         end

         1: begin  //line is high
            rx_cyclecnt_nxt = rx_cyclecnt + 16'd1;
            if (rx_cyclecnt != bit_duration_i) rx_pc_nxt = rx_pc;
            else if (!rs232_rxd_i)  //error: line returned to low early
               rx_pc_nxt = 3'd0;  //go back and resync
         end

         2: begin  //wait for start bit
            rx_cyclecnt_nxt = 16'd1;
            if (rs232_rxd_i)  //start bit (low) has not arrived, wait
               rx_pc_nxt = rx_pc;
         end

         3: begin  //start bit is here
            rx_cyclecnt_nxt = rx_cyclecnt + 16'd1;
            if (rx_cyclecnt != bit_duration_i / 2)  // wait half bit period
               rx_pc_nxt = rx_pc;
            else if (rs232_rxd_i)  //error: line returned to high unexpectedly 
               rx_pc_nxt = 3'd0;  //go back and resync
            else rx_cyclecnt_nxt = 16'd1;
         end

         default: begin  // receive data
            rx_cyclecnt_nxt = rx_cyclecnt + 16'd1;
            if (rx_cyclecnt_nxt == bit_duration_i) begin
               rx_cyclecnt_nxt = 16'd1;
               rx_bitcnt_nxt   = rx_bitcnt + 4'd1;
               rx_pattern_nxt  = {rs232_rxd_i, rx_pattern[7:1]};  //sample rx line
               if (rx_bitcnt == 4'd8) begin  //stop bit is here
                  rx_data_nxt   = rx_pattern;  //register rx data
                  rx_ready_nxt  = 1'b1;
                  rx_bitcnt_nxt = 4'd0;
                  rx_pc_nxt     = 3'd2;
               end else begin
                  rx_pc_nxt = rx_pc;  //wait for more bits
               end
            end else begin
               rx_pc_nxt = rx_pc;  //wait for more cycles
            end
         end
      endcase
   end

endmodule
