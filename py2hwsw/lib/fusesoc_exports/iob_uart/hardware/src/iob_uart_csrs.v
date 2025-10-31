// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_uart_csrs_conf.vh"

module iob_uart_csrs #(
   parameter ADDR_W = `IOB_UART_CSRS_ADDR_W,  // Don't change this parameter value!
   parameter DATA_W = `IOB_UART_CSRS_DATA_W
) (
   // clk_en_rst_s: Clock, clock enable and reset
   input                              clk_i,
   input                              cke_i,
   input                              arst_i,
   // control_if_s: CSR control interface. Interface type defined by `csr_if` parameter.
   input                              iob_valid_i,
   input  [                    3-1:0] iob_addr_i,
   input  [               DATA_W-1:0] iob_wdata_i,
   input  [             DATA_W/8-1:0] iob_wstrb_i,
   output                             iob_rvalid_o,
   output [               DATA_W-1:0] iob_rdata_o,
   output                             iob_ready_o,
   // softreset_o: softreset register interface
   output                             softreset_rdata_o,
   // div_o: div register interface
   output [                   16-1:0] div_rdata_o,
   // txdata_io: txdata register interface
   output                             txdata_valid_o,
   output [                    8-1:0] txdata_wdata_o,
   output [((8/8 > 1) ? 8/8 : 1)-1:0] txdata_wstrb_o,
   input                              txdata_ready_i,
   // txen_o: txen register interface
   output                             txen_rdata_o,
   // rxen_o: rxen register interface
   output                             rxen_rdata_o,
   // txready_i: txready register interface
   input                              txready_wdata_i,
   // rxready_i: rxready register interface
   input                              rxready_wdata_i,
   // rxdata_io: rxdata register interface
   output                             rxdata_valid_o,
   input  [                    8-1:0] rxdata_rdata_i,
   input                              rxdata_ready_i,
   input                              rxdata_rvalid_i
);

   // Internal iob interface
   wire                             internal_iob_valid;
   wire [               ADDR_W-1:0] internal_iob_addr;
   wire [               DATA_W-1:0] internal_iob_wdata;
   wire [             DATA_W/8-1:0] internal_iob_wstrb;
   wire                             internal_iob_rvalid;
   wire [               DATA_W-1:0] internal_iob_rdata;
   wire                             internal_iob_ready;
   wire                             state;
   reg                              state_nxt;
   wire                             write_en;
   wire [               ADDR_W-1:0] internal_iob_addr_stable;
   wire [               ADDR_W-1:0] internal_iob_addr_reg;
   wire                             internal_iob_addr_reg_en;
   wire                             softreset_wdata;
   wire                             softreset_w_valid;
   wire [                   16-1:0] div_wdata;
   wire                             div_w_valid;
   wire [                    8-1:0] txdata_wdata;
   wire [((8/8 > 1) ? 8/8 : 1)-1:0] txdata_wstrb;
   wire                             txen_wdata;
   wire                             txen_w_valid;
   wire                             rxen_wdata;
   wire                             rxen_w_valid;
   wire                             txready_rdata;
   wire                             rxready_rdata;
   wire                             iob_rvalid_out;
   reg                              iob_rvalid_nxt;
   wire [                   32-1:0] iob_rdata_out;
   reg  [                   32-1:0] iob_rdata_nxt;
   wire                             iob_ready_out;
   reg                              iob_ready_nxt;
   // Rvalid signal of currently addressed CSR
   reg                              rvalid_int;
   // Ready signal of currently addressed CSR
   reg                              ready_int;


   // Include iob_functions for use in parameters
   localparam IOB_MAX_W = ADDR_W;
   function [IOB_MAX_W-1:0] iob_max;
      input [IOB_MAX_W-1:0] a;
      input [IOB_MAX_W-1:0] b;
      begin
         if (a > b) iob_max = a;
         else iob_max = b;
      end
   endfunction

   function integer iob_abs;
      input integer a;
      begin
         iob_abs = (a >= 0) ? a : -a;
      end
   endfunction

   `define IOB_NBYTES (DATA_W/8)
   `define IOB_NBYTES_W $clog2(`IOB_NBYTES)
   `define IOB_WORD_ADDR(ADDR) ((ADDR>>`IOB_NBYTES_W)<<`IOB_NBYTES_W)

   localparam WSTRB_W = DATA_W / 8;

   //FSM states
   localparam WAIT_REQ = 1'd0;
   localparam WAIT_RVALID = 1'd1;


   assign internal_iob_addr_reg_en = internal_iob_valid;
   assign internal_iob_addr_stable = internal_iob_valid ? internal_iob_addr : internal_iob_addr_reg;

   assign write_en = |internal_iob_wstrb;

   //write address
   wire [($clog2(WSTRB_W)+1)-1:0] byte_offset;
   iob_ctls #(
      .W     (WSTRB_W),
      .MODE  (0),
      .SYMBOL(0)
   ) bo_inst (
      .data_i (internal_iob_wstrb),
      .count_o(byte_offset)
   );

   wire [ADDR_W-1:0] wstrb_addr;
   assign wstrb_addr = `IOB_WORD_ADDR(internal_iob_addr_stable) + byte_offset;

   // Create a special readstrobe for "REG" (auto) CSRs.
   // LSBs 0 = read full word; LSBs 1 = read byte; LSBs 2 = read half word; LSBs 3 = read byte.
   reg [1:0] shift_amount;
   always @(*) begin
      case (internal_iob_addr_stable[1:0])
         // Access entire word
         2'b00:   shift_amount = 2;
         // Access single byte
         2'b01:   shift_amount = 0;
         // Access half word
         2'b10:   shift_amount = 1;
         // Access single byte
         2'b11:   shift_amount = 0;
         default: shift_amount = 0;
      endcase
   end


   //NAME: softreset;
   //MODE: W; WIDTH: 1; RST_VAL: 0; ADDR: 0; SPACE (bytes): 1 (max); TYPE: REG. 

   assign softreset_wdata = internal_iob_wdata[0+:1];
   wire softreset_addressed_w;
   assign softreset_addressed_w = (wstrb_addr < 1);
   assign softreset_w_valid     = internal_iob_valid & (write_en & softreset_addressed_w);
   iob_reg_cae #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) softreset_datareg_wr (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (softreset_w_valid),
      .data_i(softreset_wdata),
      .data_o(softreset_rdata_o)
   );



   //NAME: div;
   //MODE: W; WIDTH: 16; RST_VAL: 0; ADDR: 2; SPACE (bytes): 2 (max); TYPE: REG. 

   assign div_wdata = internal_iob_wdata[16+:16];
   wire div_addressed_w;
   assign div_addressed_w = (wstrb_addr >= (2)) && (wstrb_addr < 4);
   assign div_w_valid     = internal_iob_valid & (write_en & div_addressed_w);
   iob_reg_cae #(
      .DATA_W (16),
      .RST_VAL(16'd0)
   ) div_datareg_wr (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (div_w_valid),
      .data_i(div_wdata),
      .data_o(div_rdata_o)
   );



   //NAME: txdata;
   //MODE: W; WIDTH: 8; RST_VAL: 0; ADDR: 4; SPACE (bytes): 1 (max); TYPE: NOAUTO. 

   assign txdata_wdata = internal_iob_wdata[0+:8];
   wire txdata_addressed;
   assign txdata_addressed = (internal_iob_addr_stable >= (4)) && (internal_iob_addr_stable < 5);
   assign txdata_valid_o   = internal_iob_valid & txdata_addressed;
   assign txdata_wstrb     = internal_iob_wstrb[0/8+:((8/8>1)?8/8 : 1)];
   assign txdata_wstrb_o   = txdata_wstrb;
   assign txdata_wdata_o   = txdata_wdata;


   //NAME: txen;
   //MODE: W; WIDTH: 1; RST_VAL: 0; ADDR: 5; SPACE (bytes): 1 (max); TYPE: REG. 

   assign txen_wdata       = internal_iob_wdata[8+:1];
   wire txen_addressed_w;
   assign txen_addressed_w = (wstrb_addr >= (5)) && (wstrb_addr < 6);
   assign txen_w_valid     = internal_iob_valid & (write_en & txen_addressed_w);
   iob_reg_cae #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) txen_datareg_wr (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (txen_w_valid),
      .data_i(txen_wdata),
      .data_o(txen_rdata_o)
   );



   //NAME: rxen;
   //MODE: W; WIDTH: 1; RST_VAL: 0; ADDR: 6; SPACE (bytes): 1 (max); TYPE: REG. 

   assign rxen_wdata = internal_iob_wdata[16+:1];
   wire rxen_addressed_w;
   assign rxen_addressed_w = (wstrb_addr >= (6)) && (wstrb_addr < 7);
   assign rxen_w_valid     = internal_iob_valid & (write_en & rxen_addressed_w);
   iob_reg_cae #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) rxen_datareg_wr (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (rxen_w_valid),
      .data_i(rxen_wdata),
      .data_o(rxen_rdata_o)
   );



   //NAME: txready;
   //MODE: R; WIDTH: 1; RST_VAL: 0; ADDR: 0; SPACE (bytes): 1 (max); TYPE: REG. 

   wire txready_addressed_r;
   assign txready_addressed_r = (internal_iob_addr_stable >> shift_amount <= iob_max(
       1, 0 >> shift_amount
   ));
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) txready_datareg_rd (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(txready_wdata_i),
      .data_o(txready_rdata)
   );



   //NAME: rxready;
   //MODE: R; WIDTH: 1; RST_VAL: 0; ADDR: 1; SPACE (bytes): 1 (max); TYPE: REG. 

   wire rxready_addressed_r;
   assign rxready_addressed_r = (internal_iob_addr_stable>>shift_amount >= (1>>shift_amount)) && (internal_iob_addr_stable>>shift_amount <= iob_max(
       1, 1 >> shift_amount
   ));
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) rxready_datareg_rd (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rxready_wdata_i),
      .data_o(rxready_rdata)
   );



   //NAME: rxdata;
   //MODE: R; WIDTH: 8; RST_VAL: 0; ADDR: 4; SPACE (bytes): 1 (max); TYPE: NOAUTO. 

   wire rxdata_addressed;
   assign rxdata_addressed = (internal_iob_addr_stable >= (4)) && (internal_iob_addr_stable < 5);
   assign rxdata_valid_o   = internal_iob_valid & rxdata_addressed & ~write_en;


   //NAME: version;
   //MODE: R; WIDTH: 16; RST_VAL: 0081; ADDR: 6; SPACE (bytes): 2 (max); TYPE: REG. 

   wire version_addressed_r;
   assign version_addressed_r = (internal_iob_addr_stable>>shift_amount >= (6>>shift_amount)) && (internal_iob_addr_stable>>shift_amount <= iob_max(
       1, 7 >> shift_amount
   ));


   wire auto_addressed;
   wire auto_addressed_r;
   reg  auto_addressed_nxt;

   //RESPONSE SWITCH

   // Don't register response signals if accessing non-auto CSR
   assign internal_iob_rvalid = auto_addressed ? iob_rvalid_out : rvalid_int;
   assign internal_iob_rdata  = auto_addressed ? iob_rdata_out : iob_rdata_nxt;
   assign internal_iob_ready  = auto_addressed ? iob_ready_out : ready_int;

   // auto_addressed register
   assign auto_addressed      = (state == WAIT_REQ) ? auto_addressed_nxt : auto_addressed_r;
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) auto_addressed_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(auto_addressed_nxt),
      // data_o port: Data output
      .data_o(auto_addressed_r)
   );

   always @* begin
      iob_rdata_nxt      = 32'd0;

      rvalid_int         = 1'b1;
      ready_int          = 1'b1;
      auto_addressed_nxt = auto_addressed_r;
      if (internal_iob_valid) begin
         auto_addressed_nxt = 1'b1;
      end
      if (txready_addressed_r) begin
         iob_rdata_nxt[0+:8] = {{7{1'b0}}, txready_rdata} | 8'd0;
      end

      if (rxready_addressed_r) begin
         iob_rdata_nxt[8+:8] = {{7{1'b0}}, rxready_rdata} | 8'd0;
      end

      if (rxdata_addressed) begin

         iob_rdata_nxt[0+:8] = rxdata_rdata_i | 8'd0;
         rvalid_int          = rxdata_rvalid_i;
         ready_int           = rxdata_ready_i;
         if (internal_iob_valid & (~|internal_iob_wstrb)) begin
            auto_addressed_nxt = 1'b0;
         end
      end

      if (version_addressed_r) begin
         iob_rdata_nxt[16+:16] = 16'h0081 | 16'd0;
      end

      if (write_en && (wstrb_addr >= (4)) && (wstrb_addr < 5)) begin
         ready_int = txdata_ready_i;
         if (internal_iob_valid & (|internal_iob_wstrb)) begin
            auto_addressed_nxt = 1'b0;
         end
      end



      // ######  FSM  #############

      //FSM default values
      iob_ready_nxt  = 1'b0;
      iob_rvalid_nxt = 1'b0;
      state_nxt      = state;

      //FSM state machine
      case (state)
         WAIT_REQ: begin
            if (internal_iob_valid) begin  // Wait for a valid request

               iob_ready_nxt = ready_int;

               // If is read and ready, go to WAIT_RVALID
               if (iob_ready_nxt && (!write_en)) begin
                  state_nxt = WAIT_RVALID;
               end
            end
         end

         default: begin  // WAIT_RVALID

            if (auto_addressed & iob_rvalid_out) begin  // Transfer done
               state_nxt = WAIT_REQ;
            end else if ((!auto_addressed) & rvalid_int) begin  // Transfer done
               state_nxt = WAIT_REQ;
            end else begin
               iob_rvalid_nxt = rvalid_int;

            end
         end
      endcase

   end  //always @*



        // store iob addr
   iob_reg_cae #(
      .DATA_W (ADDR_W),
      .RST_VAL({ADDR_W{1'b0}})
   ) internal_addr_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .en_i  (internal_iob_addr_reg_en),
      // data_i port: Data input
      .data_i(internal_iob_addr),
      // data_o port: Data output
      .data_o(internal_iob_addr_reg)
   );

   // state register
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) state_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(state_nxt),
      // data_o port: Data output
      .data_o(state)
   );

   // Convert CSR interface into internal IOb port
   iob_universal_converter_iob_iob #(
      .ADDR_W(ADDR_W),
      .DATA_W(DATA_W)
   ) iob_universal_converter (
      // s_s port: Subordinate port
      .iob_valid_i (iob_valid_i),
      .iob_addr_i  (iob_addr_i),
      .iob_wdata_i (iob_wdata_i),
      .iob_wstrb_i (iob_wstrb_i),
      .iob_rvalid_o(iob_rvalid_o),
      .iob_rdata_o (iob_rdata_o),
      .iob_ready_o (iob_ready_o),
      // m_m port: Manager port
      .iob_valid_o (internal_iob_valid),
      .iob_addr_o  (internal_iob_addr),
      .iob_wdata_o (internal_iob_wdata),
      .iob_wstrb_o (internal_iob_wstrb),
      .iob_rvalid_i(internal_iob_rvalid),
      .iob_rdata_i (internal_iob_rdata),
      .iob_ready_i (internal_iob_ready)
   );

   // rvalid register
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) rvalid_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(iob_rvalid_nxt),
      // data_o port: Data output
      .data_o(iob_rvalid_out)
   );

   // rdata register
   iob_reg_ca #(
      .DATA_W (32),
      .RST_VAL(32'b0)
   ) rdata_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(iob_rdata_nxt),
      // data_o port: Data output
      .data_o(iob_rdata_out)
   );

   // ready register
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) ready_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(iob_ready_nxt),
      // data_o port: Data output
      .data_o(iob_ready_out)
   );


endmodule
