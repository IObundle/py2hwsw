// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_nco_conf.vh"
`include "iob_nco_csrs.vh"

module iob_nco #(
   `include "iob_nco_params.vs"
) (
   `include "iob_nco_io.vs"
);

   wire [PERIOD_W-1:0] period_r;
   wire [PERIOD_W-1:0] cnt;
   reg  [PERIOD_W-1:0] cnt_nxt;
   reg                 clk_int;

   wire                soft_reset;
   wire                enable;
   wire [PERIOD_W-1:0] period_wdata;
   wire                period_wen;

   `include "iob_nco_wires.vs"

   // configuration control and status register file.
   `include "iob_nco_subblocks.vs"

   wire                  period_int_wen_wr;
   assign period_int_wen_wr = period_int_valid_wr & (|period_int_wstrb_wr);

   wire                  period_frac_wen_wr;
   assign period_frac_wen_wr = period_frac_valid_wr & (|period_frac_wstrb_wr);


   // Concatenate Integer and fractional Period registers
   wire [(2*DATA_W)-1:0] period_full_wdata;
   wire                  period_full_wen;
   // integer period value register
   iob_reg_care #(
      .DATA_W(DATA_W)
   ) int_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (soft_reset_wr),
      .en_i  (period_int_wen_wr),
      .data_i(period_int_wdata_wr),
      .data_o(period_full_wdata[DATA_W+:DATA_W])
   );
   // fractional period value register
   iob_reg_care #(
      .DATA_W(DATA_W)
   ) frac_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (soft_reset_wr),
      .en_i  (period_frac_wen_wr),
      .data_i(period_frac_wdata_wr),
      .data_o(period_full_wdata[0+:DATA_W])
   );
   // period valid register
   wire         per_valid_en;
   wire         per_valid_rst;
   wire [2-1:0] per_valid_nxt;
   wire [2-1:0] per_valid;
   assign per_valid_en  = period_int_wen_wr | period_frac_wen_wr;
   assign per_valid_rst = soft_reset_wr | (&per_valid);
   assign per_valid_nxt = per_valid | ({period_int_wen_wr, period_frac_wen_wr});
   iob_reg_care #(
      .DATA_W(2)
   ) valid_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .rst_i (per_valid_rst),
      .en_i  (per_valid_en),
      .data_i(per_valid_nxt),
      .data_o(per_valid)
   );
   assign period_full_wen = &per_valid;


   iob_nco_sync #(
      .PERIOD_W(PERIOD_W)
   ) nco_sync_inst (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),

      .in_clk_i (clk_in_i),
      .in_arst_i(clk_in_arst_i),
      .in_cke_i (clk_in_cke_i),

      .soft_reset_i  (soft_reset_wr),
      .enable_i      (enable_wr),
      .period_wdata_i(period_full_wdata),
      .period_wen_i  (period_full_wen),

      .soft_reset_o  (soft_reset),
      .enable_o      (enable),
      .period_wdata_o(period_wdata),
      .period_wen_o  (period_wen)
   );


   // PERIOD Manual logic
   assign period_int_ready_wr  = 1'b1;
   assign period_frac_ready_wr = 1'b1;

   always @* begin
      clk_int = (cnt[PERIOD_W-1:FRAC_W] > (period_r[PERIOD_W-1:FRAC_W] / 2));

      if (cnt >= period_r)
         cnt_nxt = cnt - period_r;
      else
         cnt_nxt = cnt + {1'b1, {FRAC_W{1'b0}}};
   end

   //period value register
   iob_reg_care #(
      .DATA_W(PERIOD_W)
   ) per_reg (
      .clk_i (clk_in_i),
      .cke_i (clk_in_cke_i),
      .arst_i(clk_in_arst_i),
      .rst_i (soft_reset),
      .en_i  (period_wen),
      .data_i(period_wdata),
      .data_o(period_r)
   );

   //output clock register
   iob_reg_care #(
      .DATA_W(1)
   ) clk_out_reg (
      .clk_i (clk_in_i),
      .cke_i (clk_in_cke_i),
      .arst_i(clk_in_arst_i),
      .rst_i (soft_reset),
      .en_i  (enable),
      .data_i(clk_int),
      .data_o(clk_out_o)
   );

   //output period counter
   iob_reg_care #(
      .DATA_W(PERIOD_W)
   ) cnt_reg (
      .clk_i (clk_in_i),
      .cke_i (clk_in_cke_i),
      .arst_i(clk_in_arst_i),
      .rst_i (soft_reset),
      .en_i  (enable),
      .data_i(cnt_nxt),
      .data_o(cnt)
   );

endmodule
