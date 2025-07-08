// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps


//
// APB subordinate port to IOb manager interface

module iob_apb2iob #(
   `include "iob_apb2iob_params.vs"
) (
   `include "iob_apb2iob_io.vs"
);
   localparam WSTRB_W = DATA_W / 8;

   localparam WAIT_ENABLE = 2'd0;
   localparam WAIT_READY = 2'd1;
   localparam RVALID = 2'd2;
   localparam WAIT_APB_READY = 2'd3;

   reg iob_valid;
   reg apb_ready_nxt;

   assign iob_valid_o  = iob_valid;
   assign iob_addr_o   = apb_addr_i;
   assign iob_wdata_o  = apb_wdata_i;
   assign iob_wstrb_o  = apb_write_i ? apb_wstrb_i : {WSTRB_W{1'b0}};

   //program counter
   wire [1:0] pc_cnt;
   reg  [1:0] pc_cnt_nxt;
   iob_reg_ca #(
      .DATA_W (2),
      .RST_VAL(2'd0)
   ) pc_reg (
      `include "iob_apb2iob_iob_clk_s_s_portmap.vs"
      .data_i(pc_cnt_nxt),
      .data_o(pc_cnt)
   );

   always @* begin

      pc_cnt_nxt     = pc_cnt + 1'b1;
      iob_valid      = 1'b0;
      apb_ready_nxt  = 1'b0;

      case (pc_cnt)
         WAIT_ENABLE: begin
            if (!(apb_sel_i & apb_enable_i)) begin
               pc_cnt_nxt = pc_cnt;
            end else begin
               iob_valid = 1'b1;
            end
         end
         WAIT_READY: begin
            iob_valid = 1'b1;
            if (!iob_ready_i) begin
               pc_cnt_nxt = pc_cnt;
            end else begin
               if (apb_write_i) begin
                  pc_cnt_nxt    = WAIT_APB_READY;
                  apb_ready_nxt = 1'b1;
               end
            end
         end
         RVALID: begin
            apb_ready_nxt  = iob_rvalid_i;
            if (!iob_rvalid_i) begin
               pc_cnt_nxt = pc_cnt;
            end
         end
         default: begin  // WAIT_APB_READY
            pc_cnt_nxt = WAIT_ENABLE;
         end
      endcase
   end  // always @ *


   //APB outputs
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) apb_ready_reg (
      `include "iob_apb2iob_iob_clk_s_s_portmap.vs"
      .data_i(apb_ready_nxt),
      .data_o(apb_ready_o)
   );

   iob_reg_cae #(
      .DATA_W (DATA_W),
      .RST_VAL({DATA_W{1'd0}})
   ) apb_rdata_reg (
      `include "iob_apb2iob_iob_clk_s_s_portmap.vs"
      .en_i  (iob_rvalid_i),
      .data_i(iob_rdata_i),
      .data_o(apb_rdata_o)
   );


endmodule
