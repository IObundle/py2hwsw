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

   wire wvalid_reg_en;
   wire wvalid_reg_rst;
   wire wvalid_reg_i;
   assign wvalid_reg_en  = axil_awvalid_o;
   assign wvalid_reg_rst = axil_wready_i;
   assign wvalid_reg_i   = 1'b1;
   wire wvalid_reg_o;

   iob_reg_cear_re #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) wvalid_re (
      // clk_en_rst_s port
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // en_rst_i port
      .en_i  (wvalid_reg_en),
      .rst_i (wvalid_reg_rst),
      // data_i port
      .data_i(wvalid_reg_i),
      // data_o port
      .data_o(wvalid_reg_o)
   );

   //
   // COMPUTE IOb OUTPUTS
   //
   assign iob_rvalid_o   = axil_rvalid_i;
   assign iob_rdata_o    = axil_rdata_i;
   assign iob_ready_o    = (|iob_wstrb_i) ? (axil_wready_i | axil_awready_i) : axil_arready_i;

   //
   // COMPUTE AXIL OUTPUTS
   //

   // write address
   assign axil_awvalid_o = iob_valid_i & |iob_wstrb_i;
   assign axil_awaddr_o  = iob_addr_i;

   // write
   assign axil_wvalid_o  = wvalid_reg_o;
   assign axil_wdata_o   = iob_wdata_i;
   assign axil_wstrb_o   = iob_wstrb_i;

   // write response
   assign axil_bready_o  = iob_rready_i;

   // read address
   assign axil_arvalid_o = iob_valid_i & ~|iob_wstrb_i;
   assign axil_araddr_o  = iob_addr_i;

   // read
   assign axil_rready_o  = iob_rready_i;

endmodule
