`timescale 1ns / 1ps
`include "iob_nco_conf.vh"
`include "iob_nco_csrs_def.vh"

module iob_nco #(
   `include "iob_nco_params.vs"
) (
   `include "iob_nco_io.vs"
);
   wire [     DATA_W-1:0] period_r;
   wire [     DATA_W-1:0] diff;
   wire [DATA_W-1:FRAC_W] cnt;
   wire [DATA_W-1:0] acc_in, acc_out;
   wire                clk_int;

   wire                soft_reset;
   wire                enable;
   wire [PERIOD_W-1:0] period_wdata;
   wire                period_wen;

   `include "iob_nco_wires.vs"

   // configuration control and status register file.
   `include "iob_nco_blocks.vs"

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
      .period_wdata_i(period_wdata_wr),
      .period_wen_i  (period_wen_wr),

      .soft_reset_o  (soft_reset),
      .enable_o      (enable),
      .period_wdata_o(period_wdata),
      .period_wen_o  (period_wen)
   );


   // PERIOD Manual logic
   assign period_wready_wr = 1'b1;

   reg [DATA_W-1:FRAC_W] quant;

   assign diff    = period_r - {quant, {FRAC_W{1'b0}}};
   assign clk_int = (cnt > (quant / 2));

   always @* begin
      if (acc_out[FRAC_W-1:0] == {1'b1, {FRAC_W - 1{1'b0}}})
         quant = acc_out[DATA_W-1:FRAC_W] + ^acc_out[DATA_W-1:FRAC_W];
      else if (acc_out[FRAC_W-1]) quant = acc_out[DATA_W-1:FRAC_W] + 1'b1;
      else quant = acc_out[DATA_W-1:FRAC_W];
   end

   //fractional period value register
   iob_reg_re #(
      .DATA_W(DATA_W)
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
   iob_reg_re #(
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

   //modulator accumulator
   iob_acc_ld #(
      .DATA_W(DATA_W)
   ) acc_ld (
      .clk_i   (clk_in_i),
      .cke_i   (clk_in_cke_i),
      .arst_i  (clk_in_arst_i),
      .rst_i   (soft_reset),
      .en_i    (enable),
      .ld_i    (period_wen),
      .ld_val_i(period_wdata),
      .incr_i  (diff),
      .data_o  (acc_out)
   );

   //output period counter
   iob_modcnt #(
      .DATA_W(DATA_W - FRAC_W)
   ) modcnt (
      .clk_i (clk_in_i),
      .cke_i (clk_in_cke_i),
      .arst_i(clk_in_arst_i),
      .rst_i (period_wen),
      .en_i  (enable),
      .mod_i (quant),
      .data_o(cnt)
   );

endmodule
