// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

`include "iob_axis_s_axi_m_read_conf.vh"

module iob_axis_s_axi_m_read #(
   `include "iob_axis_s_axi_m_read_params.vs"
) (
   `include "iob_axis_s_axi_m_read_io.vs"
);

   localparam WAIT_START = 1'd0, WAIT_SPACE_IN_FIFO = 1'd1;
   localparam FIFO_MAX_LEVEL = 1 << AXI_LEN_W;

   // Calculate empty space in FIFO
   wire [(AXI_ADDR_W+1)-1:0] fifo_level;
   wire [(AXI_LEN_W+1)-1:0] space_in_fifo = FIFO_MAX_LEVEL - fifo_level;

   wire [   AXI_DATA_W-1:0] fifo_wdata;
   wire                     fifo_wen;
   wire                     fifo_full;
   wire fifo_wready;
   assign fifo_wready = ~fifo_full;
   wire                     fifo_ren;
   wire [   AXI_DATA_W-1:0] fifo_rdata;
   wire                     fifo_empty;

   // FIFO2AXIS converter
   iob_fifo2axis #(
      .DATA_W    (AXI_DATA_W),
      .AXIS_LEN_W(1)
   ) fifo2axis_inst (
      // Global signals
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i        (rst_i),
      .en_i         (1'b1),
      .len_i        (1'b1),
      .level_o      (),
      .fifo_empty_i (fifo_empty),
      .fifo_read_o  (fifo_ren),
      .fifo_rdata_i (fifo_rdata),
      .axis_tvalid_o(axis_out_tvalid_o),
      .axis_tdata_o (axis_out_tdata_o),
      .axis_tready_i(axis_out_tready_i),
      .axis_tlast_o ()
   );

   // FIFO
   iob_fifo_sync #(
      .W_DATA_W(AXI_DATA_W),
      .R_DATA_W(AXI_DATA_W),
      .ADDR_W  (AXI_ADDR_W)
   ) buffer_inst (
      // Global signals
      .clk_i           (clk_i),
      .cke_i           (cke_i),
      .arst_i          (arst_i),
      .rst_i           (rst_i),
      // Write port
      .w_en_i          (fifo_wen),
      .w_data_i        (fifo_wdata),
      .w_full_o        (fifo_full),
      // Read port
      .r_en_i          (fifo_ren),
      .r_data_o        (fifo_rdata),
      .r_empty_o       (fifo_empty),
      // External memory interface
      .ext_mem_clk_o   (ext_mem_read_clk_o),
      .ext_mem_w_en_o  (ext_mem_read_w_en_o),
      .ext_mem_w_addr_o(ext_mem_read_w_addr_o),
      .ext_mem_w_data_o(ext_mem_read_w_data_o),
      .ext_mem_r_en_o  (ext_mem_read_r_en_o),
      .ext_mem_r_addr_o(ext_mem_read_r_addr_o),
      .ext_mem_r_data_i(ext_mem_read_r_data_i),
      // FIFO level
      .level_o         (fifo_level)
   );

   reg                      r_state_nxt;
   wire                     r_state;
   reg  [   RLEN_W-1:0]     r_remaining_data_nxt;
   reg  [(AXI_LEN_W+1)-1:0] burst_length;
   reg  [   AXI_ADDR_W-1:0] r_addr_int_nxt;
   wire [   AXI_ADDR_W-1:0] burst_addr;
   reg                      start_burst;
   wire                     busy;
   reg                      r_busy_int;

   assign r_busy_o = r_busy_int;

   always @* begin
      // FSM
      // Default assignments
      r_busy_int             = 1'b1;
      r_state_nxt          = r_state;
      r_remaining_data_nxt = r_remaining_data_o;
      r_addr_int_nxt       = burst_addr;
      start_burst          = 1'b0;
      burst_length         = 0;

      case (r_state)
         WAIT_START: begin
            r_busy_int = 1'b0;
            if (r_start_transfer_i) begin
               r_remaining_data_nxt = r_length_i;
               r_addr_int_nxt       = r_addr_i;
               r_state_nxt          = WAIT_SPACE_IN_FIFO;
            end
         end
         default: begin  // WAIT_SPACE_IN_FIFO
            if (!busy) begin
               if (r_remaining_data_o > 0) begin
                  if (({{RLEN_W-(AXI_LEN_W+1){1'b0}}, space_in_fifo} >= r_remaining_data_o)
                        && (r_remaining_data_o <= {{RLEN_W-(AXI_LEN_W+1){1'b0}}, r_max_len_i}))
                  begin
                     // TX FIFO has enough space left to transfer the remaining data
                     burst_length = r_remaining_data_o[0+:(AXI_LEN_W+1)];
                  end else if (space_in_fifo >= r_max_len_i) begin
                     // TX FIFO has enough space for a burst transfer
                     burst_length = r_max_len_i;
                  end

                  if (burst_length > 0) begin
                     // Start the transfer
                     start_burst          = 1'd1;
                     // Set values for the next transfer
                     r_remaining_data_nxt = r_remaining_data_o - burst_length;
                     r_addr_int_nxt       = burst_addr + (burst_length << 2);
                  end
               end else begin
                  r_state_nxt = WAIT_START;
               end
            end
         end
      endcase
   end

   iob_reg_car #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) r_state_reg (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i (rst_i),
      .data_i(r_state_nxt),
      .data_o(r_state)
   );

   iob_reg_car #(
      .DATA_W (RLEN_W),
      .RST_VAL({RLEN_W{1'b0}})
   ) r_length_reg (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i (rst_i),
      .data_i(r_remaining_data_nxt),
      .data_o(r_remaining_data_o)
   );

   iob_reg_car #(
      .DATA_W (AXI_ADDR_W),
      .RST_VAL({AXI_ADDR_W{1'b0}})
   ) r_addr_reg (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i (rst_i),
      .data_i(r_addr_int_nxt),
      .data_o(burst_addr)
   );

   iob_axis_s_axi_m_read_int #(
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_DATA_W(AXI_DATA_W),
      .AXI_LEN_W (AXI_LEN_W),
      .AXI_ID_W  (AXI_ID_W)
   ) axi2axis_inst (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i(rst_i),

      `include "iob_axis_s_axi_m_read_m_axi_read_m_m_portmap.vs"

      .r_addr_i          (burst_addr),
      .r_length_i        (burst_length),
      .r_start_transfer_i(start_burst),
      .r_busy_o          (busy),

      .axis_out_data_o (fifo_wdata),
      .axis_out_valid_o(fifo_wen),
      .axis_out_ready_i(fifo_wready)
   );

endmodule

