// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_iob2axil_conf.vh"

module iob_iob2axil #(
   `include "iob_iob2axil_params.vs"
) (
   `include "iob_iob2axil_io.vs"
);

   localparam WAIT_AVALID  = 3'd0;
   localparam WAIT_AWREADY = 3'd1;
   localparam WAIT_WREADY  = 3'd2;
   localparam WAIT_BVALID  = 3'd3;
   localparam WAIT_RVALID  = 3'd4;

   reg axil_awvalid_int;
   reg axil_arvalid_int;
   reg axil_rready_int;
   reg axil_wvalid_int;
   reg axil_bready_int;
   reg iob_ready_int;

   wire wen;
   assign wen = |iob_wstrb_i;

   //
   // COMPUTE IOb OUTPUTS
   //
   assign iob_rvalid_o   = axil_rvalid_i;
   assign iob_rdata_o    = axil_rdata_i;
   assign iob_ready_o    = iob_ready_int;

   //
   // COMPUTE AXIL OUTPUTS
   //

   // write address
   assign axil_awvalid_o = axil_awvalid_int;
   assign axil_awaddr_o  = iob_addr_i;

   // write
   assign axil_wvalid_o  = axil_wvalid_int;
   assign axil_wdata_o   = iob_wdata_i;
   assign axil_wstrb_o   = iob_wstrb_i;

   // write response
   assign axil_bready_o  = axil_bready_int;

   // read address
   assign axil_arvalid_o = axil_arvalid_int;
   assign axil_araddr_o  = iob_addr_i;

   // read
   assign axil_rready_o  = axil_rready_int;

   //program counter
   wire [2:0] pc_cnt;
   reg  [2:0] pc_cnt_nxt;
   iob_reg_ca #(
      .DATA_W (3),
      .RST_VAL(3'd0)
   ) pc_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(pc_cnt_nxt),
      .data_o(pc_cnt)
   );

   always @* begin

      pc_cnt_nxt       = pc_cnt;
      axil_awvalid_int = 1'b0;
      axil_arvalid_int = 1'b0;
      axil_rready_int  = 1'b0;
      axil_wvalid_int  = 1'b0;
      axil_bready_int  = 1'b0;
      iob_ready_int    = 1'b0;

      case (pc_cnt)
         WAIT_AVALID: begin
             if (iob_valid_i)  begin
                 if (wen) begin
                     axil_awvalid_int = 1'b1;
                     axil_wvalid_int = 1'b1;
                     axil_bready_int = 1'b1;
                     pc_cnt_nxt = WAIT_AWREADY;
                end else begin
                    axil_arvalid_int = 1'b1;
                    axil_rready_int = 1'b1;
                    if (axil_arready_i) begin
                        iob_ready_int = 1'b1;
                        pc_cnt_nxt = WAIT_RVALID;
                    end
                end 
             end
         end
         WAIT_AWREADY: begin
             axil_awvalid_int = 1'b1;
             axil_wvalid_int = 1'b1;
             axil_bready_int = 1'b1;
             if (axil_awready_i & axil_wready_i) begin
                 pc_cnt_nxt = WAIT_BVALID;
             end else if (axil_awready_i) begin
                 pc_cnt_nxt = WAIT_WREADY;
             end
         end
         WAIT_WREADY: begin
             axil_wvalid_int = 1'b1;
             axil_bready_int = 1'b1;
             if (axil_wready_i) begin
                 pc_cnt_nxt = WAIT_BVALID;
             end
         end
         WAIT_BVALID: begin
             axil_bready_int = 1'b1;
             if (axil_bvalid_i) begin
                 pc_cnt_nxt = WAIT_AVALID;
                 iob_ready_int = 1'b1;
             end
         end
         WAIT_RVALID: begin
             axil_rready_int = 1'b1;
             if (axil_rvalid_i) begin
                 pc_cnt_nxt = WAIT_AVALID;
             end
         end
         default: begin
            pc_cnt_nxt = WAIT_AVALID;
         end
      endcase
   end  // always @ *

endmodule
