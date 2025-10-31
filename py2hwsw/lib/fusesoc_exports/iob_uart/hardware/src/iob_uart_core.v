// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_core_conf.vh"

module iob_uart_core (
   // clk_en_rst_s: Clock and reset
   input               clk_i,
   input               cke_i,
   input               arst_i,
   // reg_interface_io: 
   input               rst_soft_i,
   input               tx_en_i,
   input               rx_en_i,
   output              tx_ready_o,
   output              rx_ready_o,
   input      [ 8-1:0] tx_data_i,
   output     [ 8-1:0] rx_data_o,
   input               data_write_en_i,
   input               data_read_en_i,
   input      [16-1:0] bit_duration_i,
   // rs232_m: RS232 interface
   input               rs232_rxd_i,
   output reg          rs232_txd_o,
   output              rs232_rts_o,
   input               rs232_cts_i
);

   // CTS internal wire
   wire          cts_int;
   // TX Enable internal wire
   reg           txen;
   // TX Data internal wire
   wire [ 8-1:0] tx_data_int;
   // TX Parity Check internal wire
   wire [ 2-1:0] tx_pc;
   // TX Pattern internal wire
   wire [10-1:0] tx_pattern;
   // TX Pattern internal wire next
   reg  [10-1:0] tx_pattern_nxt;
   // TX Bit Count internal wire
   wire [ 4-1:0] tx_bitcnt;
   // TX Cycle Count internal wire
   wire [16-1:0] tx_cyclecnt;
   // RX Parity Check internal wire
   wire [ 3-1:0] rx_pc;
   // RX Cycle Count internal wire
   wire [16-1:0] rx_cyclecnt;
   // RX Cycle Count internal wire next
   reg  [16-1:0] rx_cyclecnt_nxt;
   // RX Bit Count internal wire
   wire [ 4-1:0] rx_bitcnt;
   // RX Bit Count internal wire
   wire [ 8-1:0] rx_pattern;
   reg  [ 2-1:0] tx_pc_nxt;
   reg           tx_pc_en;
   reg           tx_pc_rst;
   reg           tx_pattern_en;
   reg           tx_pattern_rst;
   reg  [ 4-1:0] tx_bitcnt_nxt;
   reg           tx_bitcnt_en;
   reg           tx_bitcnt_rst;
   reg  [16-1:0] tx_cyclecnt_nxt;
   reg           tx_cyclecnt_en;
   reg           tx_cyclecnt_rst;
   reg  [ 3-1:0] rx_pc_nxt;
   reg           rx_pc_en;
   reg           rx_pc_rst;
   reg           rx_cyclecnt_en;
   reg           rx_cyclecnt_rst;
   reg  [ 4-1:0] rx_bitcnt_nxt;
   reg           rx_bitcnt_en;
   reg           rx_bitcnt_rst;
   reg  [ 8-1:0] rx_pattern_nxt;
   reg           rx_pattern_en;
   reg           rx_pattern_rst;
   reg           tx_ready_o_nxt;
   reg           tx_ready_o_en;
   reg           tx_ready_o_rst;
   reg           rx_ready_o_nxt;
   reg           rx_ready_o_en;
   reg           rx_ready_o_rst;
   reg  [ 8-1:0] rx_data_o_nxt;
   reg           rx_data_o_en;
   reg           rx_data_o_rst;
   reg           rs232_rts_o_nxt;
   reg           rs232_rts_o_en;
   reg           rs232_rts_o_rst;

   always @(*) begin

      rs232_txd_o     = tx_pattern[0];
      txen            = tx_en_i & cts_int;
      //TX
      tx_pc_nxt       = tx_pc + 2'd1;  //increment pc by default
      tx_pc_rst       = rst_soft_i;
      tx_pc_en        = txen;

      tx_pattern_nxt  = tx_pattern;
      tx_pattern_rst  = rst_soft_i;
      tx_pattern_en   = txen;

      tx_bitcnt_nxt   = tx_bitcnt;
      tx_bitcnt_rst   = rst_soft_i;
      tx_bitcnt_en    = txen;

      tx_cyclecnt_nxt = tx_cyclecnt;
      tx_cyclecnt_rst = rst_soft_i;
      tx_cyclecnt_en  = txen;

      tx_ready_o_nxt  = tx_ready_o;
      tx_ready_o_rst  = rst_soft_i;
      tx_ready_o_en   = txen;

      case (tx_pc)

         0: begin  //wait for data to send
            tx_ready_o_nxt  = 1'b1;
            tx_bitcnt_nxt   = 4'd0;
            tx_cyclecnt_nxt = 16'd1;
            tx_pattern_nxt  = ~10'b0;
            if (!data_write_en_i) tx_pc_nxt = tx_pc;
            else tx_ready_o_nxt = 1'b0;
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

      //RX

      rx_pc_nxt       = rx_pc + 3'd1;  //increment pc by default
      rx_pc_rst       = rst_soft_i;
      rx_pc_en        = rx_en_i;

      rx_cyclecnt_nxt = rx_cyclecnt;
      rx_cyclecnt_rst = rst_soft_i;
      rx_cyclecnt_en  = rx_en_i;

      rx_bitcnt_nxt   = rx_bitcnt;
      rx_bitcnt_rst   = rst_soft_i;
      rx_bitcnt_en    = rx_en_i;

      rx_pattern_nxt  = rx_pattern;
      rx_pattern_rst  = rst_soft_i;
      rx_pattern_en   = rx_en_i;

      rx_ready_o_nxt  = rx_ready_o;
      rx_ready_o_rst  = rst_soft_i | data_read_en_i;
      rx_ready_o_en   = rx_en_i;

      rs232_rts_o_nxt = rs232_rts_o;
      rs232_rts_o_rst = rst_soft_i;
      rs232_rts_o_en  = rx_en_i;

      rx_data_o_nxt   = rx_data_o;
      rx_data_o_rst   = rst_soft_i;
      rx_data_o_en    = rx_en_i;


      case (rx_pc)

         0: begin  //sync up
            rs232_rts_o_nxt = 1'b1;
            rx_ready_o_nxt  = 1'b0;
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
                  rx_data_o_nxt  = rx_pattern;  //register rx data
                  rx_ready_o_nxt = 1'b1;
                  rx_bitcnt_nxt  = 4'd0;
                  rx_pc_nxt      = 3'd2;
               end else begin
                  rx_pc_nxt = rx_pc;  //wait for more bits
               end
            end else begin
               rx_pc_nxt = rx_pc;  //wait for more cycles
            end
         end
      endcase

   end

   // Default description
   iob_sync #(
      .DATA_W(1)
   ) cts_sync (
      // clk_rst_s port: Clock and reset
      .clk_i   (clk_i),
      .arst_i  (arst_i),
      // signal_i port: Input port
      .signal_i(rs232_cts_i),
      // signal_o port: Output port
      .signal_o(cts_int)
   );

   // Default description
   iob_reg_cae #(
      .DATA_W (8),
      .RST_VAL(8'b0)
   ) txdata_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (data_write_en_i),
      // data_i port: Data input
      .data_i(tx_data_i),
      // data_o port: Data output
      .data_o(tx_data_int)
   );

   // Default description
   iob_reg_care #(
      .DATA_W (10),
      .RST_VAL({10{1'b1}})
   ) tx_pattern_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (tx_pattern_rst),
      .en_i  (tx_pattern_en),
      // data_i port: Data input
      .data_i(tx_pattern_nxt),
      // data_o port: Data output
      .data_o(tx_pattern)
   );

   // Default description
   iob_reg_care #(
      .DATA_W (16),
      .RST_VAL(16'b1)
   ) rx_cyclecnt_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (rx_cyclecnt_rst),
      .en_i  (rx_cyclecnt_en),
      // data_i port: Data input
      .data_i(rx_cyclecnt_nxt),
      // data_o port: Data output
      .data_o(rx_cyclecnt)
   );

   // tx_pc register
   iob_reg_care #(
      .DATA_W (2),
      .RST_VAL(0)
   ) tx_pc_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (tx_pc_rst),
      .en_i  (tx_pc_en),
      // data_i port: Data input
      .data_i(tx_pc_nxt),
      // data_o port: Data output
      .data_o(tx_pc)
   );

   // tx_bitcnt register
   iob_reg_care #(
      .DATA_W (4),
      .RST_VAL(0)
   ) tx_bitcnt_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (tx_bitcnt_rst),
      .en_i  (tx_bitcnt_en),
      // data_i port: Data input
      .data_i(tx_bitcnt_nxt),
      // data_o port: Data output
      .data_o(tx_bitcnt)
   );

   // tx_cyclecnt register
   iob_reg_care #(
      .DATA_W (16),
      .RST_VAL(0)
   ) tx_cyclecnt_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (tx_cyclecnt_rst),
      .en_i  (tx_cyclecnt_en),
      // data_i port: Data input
      .data_i(tx_cyclecnt_nxt),
      // data_o port: Data output
      .data_o(tx_cyclecnt)
   );

   // rx_pc register
   iob_reg_care #(
      .DATA_W (3),
      .RST_VAL(0)
   ) rx_pc_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (rx_pc_rst),
      .en_i  (rx_pc_en),
      // data_i port: Data input
      .data_i(rx_pc_nxt),
      // data_o port: Data output
      .data_o(rx_pc)
   );

   // rx_bitcnt register
   iob_reg_care #(
      .DATA_W (4),
      .RST_VAL(0)
   ) rx_bitcnt_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (rx_bitcnt_rst),
      .en_i  (rx_bitcnt_en),
      // data_i port: Data input
      .data_i(rx_bitcnt_nxt),
      // data_o port: Data output
      .data_o(rx_bitcnt)
   );

   // rx_pattern register
   iob_reg_care #(
      .DATA_W (8),
      .RST_VAL(0)
   ) rx_pattern_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (rx_pattern_rst),
      .en_i  (rx_pattern_en),
      // data_i port: Data input
      .data_i(rx_pattern_nxt),
      // data_o port: Data output
      .data_o(rx_pattern)
   );

   // tx_ready_o register
   iob_reg_care #(
      .DATA_W (1),
      .RST_VAL(0)
   ) tx_ready_o_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (tx_ready_o_rst),
      .en_i  (tx_ready_o_en),
      // data_i port: Data input
      .data_i(tx_ready_o_nxt),
      // data_o port: Data output
      .data_o(tx_ready_o)
   );

   // rx_ready_o register
   iob_reg_care #(
      .DATA_W (1),
      .RST_VAL(0)
   ) rx_ready_o_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (rx_ready_o_rst),
      .en_i  (rx_ready_o_en),
      // data_i port: Data input
      .data_i(rx_ready_o_nxt),
      // data_o port: Data output
      .data_o(rx_ready_o)
   );

   // rx_data_o register
   iob_reg_care #(
      .DATA_W (8),
      .RST_VAL(0)
   ) rx_data_o_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (rx_data_o_rst),
      .en_i  (rx_data_o_en),
      // data_i port: Data input
      .data_i(rx_data_o_nxt),
      // data_o port: Data output
      .data_o(rx_data_o)
   );

   // rs232_rts_o register
   iob_reg_care #(
      .DATA_W (1),
      .RST_VAL(0)
   ) rs232_rts_o_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (rs232_rts_o_rst),
      .en_i  (rs232_rts_o_en),
      // data_i port: Data input
      .data_i(rs232_rts_o_nxt),
      // data_o port: Data output
      .data_o(rs232_rts_o)
   );


endmodule
