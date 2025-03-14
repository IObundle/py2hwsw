`timescale 1ns / 1ps

module iob_dma_write #(
   // parameter AXI_ADDR_W = 0,
   // parameter AXI_LEN_W  = 8,
   // parameter AXI_DATA_W = 32,
   // parameter AXI_ID_W   = 1,
   // parameter DMA_WLEN_W = 0
   `include "iob_dma_write_params.vs"
) (
   `include "iob_dma_write_io.vs"
   // // Global signals
   // input clk_i,
   // input cke_i,
   // input arst_i,
   // input rst_i,
   //
   // // Configuration IO's
   // input      [   AXI_ADDR_W-1:0] w_addr_i,
   // input      [   DMA_WLEN_W-1:0] w_length_i,
   // input                          w_start_transfer_i,
   // input      [(AXI_LEN_W+1)-1:0] w_max_len_i,
   // output     [   DMA_WLEN_W-1:0] w_remaining_data_o,
   // output reg                     w_busy_o,
   //
   // // AXIS Slave Interface
   // input  [AXI_DATA_W-1:0] axis_in_data_i,
   // input                   axis_in_valid_i,
   // output                  axis_in_ready_o,
   //
   // // External memory interface
   // output                  ext_mem_clk_o,
   // output                  ext_mem_w_en_o,
   // output [AXI_LEN_W-1:0] ext_mem_w_addr_o,
   // output [AXI_DATA_W-1:0] ext_mem_w_data_o,
   // output                  ext_mem_r_en_o,
   // output [AXI_LEN_W-1:0] ext_mem_r_addr_o,
   // input  [AXI_DATA_W-1:0] ext_mem_r_data_i,
   //
   // // AXI Master (write only) Interface
);

   localparam WAIT_START = 1'd0, WAIT_DATA_IN_FIFO = 1'd1;
   localparam LEN_DIFF = DMA_WLEN_W - (AXI_LEN_W+1);

   wire [(AXI_LEN_W+1)-1:0] fifo_level;
   wire                     fifo_full;
   assign axis_in_ready_o = ~fifo_full;
   wire                  fifo_ren;
   wire [AXI_DATA_W-1:0] fifo_rdata;
   wire                  fifo_empty;

   // FIFO
   iob_fifo_sync #(
      .W_DATA_W(AXI_DATA_W),
      .R_DATA_W(AXI_DATA_W),
      .ADDR_W  (AXI_LEN_W)
   ) buffer_inst (
      // Global signals
      .clk_i           (clk_i),
      .cke_i           (cke_i),
      .arst_i          (arst_i),
      .rst_i           (rst_i),
      // Write port
      .w_en_i          (axis_in_valid_i),
      .w_data_i        (axis_in_data_i),
      .w_full_o        (fifo_full),
      // Read port
      .r_en_i          (fifo_ren),
      .r_data_o        (fifo_rdata),
      .r_empty_o       (fifo_empty),
      // External memory interface
      .ext_mem_clk_o   (ext_mem_clk_o),
      .ext_mem_w_en_o  (ext_mem_w_en_o),
      .ext_mem_w_addr_o(ext_mem_w_addr_o),
      .ext_mem_w_data_o(ext_mem_w_data_o),
      .ext_mem_r_en_o  (ext_mem_r_en_o),
      .ext_mem_r_addr_o(ext_mem_r_addr_o),
      .ext_mem_r_data_i(ext_mem_r_data_i),
      // FIFO level
      .level_o         (fifo_level)
   );

   wire [         2-1:0] fifo2axis_lvl;
   wire                  axis_tvalid_int;
   wire [AXI_DATA_W-1:0] axis_tdata_int;
   wire                  axis_tready_int;
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
      .level_o      (fifo2axis_lvl),
      // FIFO I/F
      .fifo_empty_i (fifo_empty),
      .fifo_read_o  (fifo_ren),
      .fifo_rdata_i (fifo_rdata),
      // AXIS I/F
      .axis_tvalid_o(axis_tvalid_int),
      .axis_tdata_o (axis_tdata_int),
      .axis_tready_i(axis_tready_int),
      .axis_tlast_o ()
   );

   wire [(AXI_LEN_W+2)-1:0] level_int = {1'd0,fifo_level} + {1'd0,fifo2axis_lvl};

   reg                      w_state_nxt;
   wire                     w_state;
   reg  [   DMA_WLEN_W-1:0] w_remaining_data_nxt;
   reg  [(AXI_LEN_W+1)-1:0] burst_length;
   reg  [   AXI_ADDR_W-1:0] w_addr_int_nxt;
   wire [   AXI_ADDR_W-1:0] burst_addr;
   reg                      start_burst;
   wire                     busy;

   always @* begin
      // FSM
      // Default assignments
      w_busy_o             = 1'b1;
      w_state_nxt          = w_state;
      w_remaining_data_nxt = w_remaining_data_o;
      w_addr_int_nxt       = burst_addr;
      start_burst          = 1'b0;
      burst_length         = 0;

      case (w_state)
         WAIT_START: begin
            w_busy_o = 1'b0;
            if (w_start_transfer_i) begin
               w_remaining_data_nxt = w_length_i;
               w_addr_int_nxt       = w_addr_i;
               w_state_nxt          = WAIT_DATA_IN_FIFO;
            end
         end
         default: begin  // WAIT_DATA_IN_FIFO
            if (!busy) begin
               if (w_remaining_data_o > 0) begin
                  if (({{(LEN_DIFF-1){1'b0}}, level_int} >= w_remaining_data_o) &&
                        (w_remaining_data_o <= {{LEN_DIFF{1'b0}}, w_max_len_i})) begin
                     // RX FIFO has enough data to transfer the remaining data
                     burst_length = w_remaining_data_o[0+:(AXI_LEN_W+1)];
                  end else if (level_int >= {1'd0,w_max_len_i}) begin
                     // RX FIFO has enough data for a burst transfer
                     burst_length = w_max_len_i;
                  end

                  if (burst_length > 0) begin
                     // Start the transfer
                     start_burst          = 1'd1;
                     // Set values for the next transfer
                     w_remaining_data_nxt = w_remaining_data_o - burst_length;
                     w_addr_int_nxt       = burst_addr + (burst_length << 2);
                  end
               end else begin
                  w_state_nxt = WAIT_START;
               end
            end
         end
      endcase
   end

   // State register
   iob_reg_r #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) w_state_reg (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i (rst_i),
      .data_i(w_state_nxt),
      .data_o(w_state)
   );

   // Length registers
   iob_reg_r #(
      .DATA_W (DMA_WLEN_W),
      .RST_VAL({DMA_WLEN_W{1'b0}})
   ) w_length_reg (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i (rst_i),
      .data_i(w_remaining_data_nxt),
      .data_o(w_remaining_data_o)
   );

   // Address registers
   iob_reg_r #(
      .DATA_W (AXI_ADDR_W),
      .RST_VAL({AXI_ADDR_W{1'b0}})
   ) w_addr_reg (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i (rst_i),
      .data_i(w_addr_int_nxt),
      .data_o(burst_addr)
   );

   iob_axis2axi #(
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_DATA_W(AXI_DATA_W),
      .AXI_LEN_W (AXI_LEN_W),
      .AXI_ID_W  (AXI_ID_W)
   ) axis2axi_inst (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i(rst_i),

      //TODO: axi write portmap

      .w_addr_i          (burst_addr),
      .w_length_i        (burst_length),
      .w_start_transfer_i(start_burst),
      .w_busy_o          (busy),

      .axis_in_data_i (axis_tdata_int),
      .axis_in_valid_i(axis_tvalid_int),
      .axis_in_ready_o(axis_tready_int)
   );

endmodule
