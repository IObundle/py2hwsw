// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_axistream_in_conf.vh"
`include "iob_axistream_in_csrs.vh"

module iob_axistream_in #(
   `include "iob_axistream_in_params.vs"
) (
   `include "iob_axistream_in_io.vs"
);

   localparam R = DATA_W / TDATA_W;
   localparam R_W = $clog2(R);
   localparam RAM_ADDR_W = FIFO_ADDR_W - $clog2(R);

   //rst and enable synced to axis_clk
   wire                                                 axis_sw_rst;
   wire                                                 axis_sw_enable;
   wire                                                 axis_sw_mode;

   //fifo write
   wire                                                 axis_fifo_write;
   wire                                                 axis_fifo_full;

   //tlast detected
   wire                                                 axis_tlast;
   wire                                                 axis_tlast_detected;

   //word counter
   wire [                                   DATA_W-1:0] axis_word_count;
   wire                                                 axis_word_count_en;


   //fifo read
   wire                                                 fifo_read;
   wire [                                   DATA_W-1:0] fifo_data;
   wire                                                 fifo_empty;
   wire [((FIFO_ADDR_W+1 > 1) ? FIFO_ADDR_W+1 : 1)-1:0] fifo_level;

   //fifo RAM
   wire                                                 ext_mem_w_clk;
   wire [                                        R-1:0] ext_mem_w_en;
   wire [                               RAM_ADDR_W-1:0] ext_mem_w_addr;
   wire [                                   DATA_W-1:0] ext_mem_w_data;
   wire                                                 ext_mem_r_clk;
   wire [                                        R-1:0] ext_mem_r_en;
   wire [                               RAM_ADDR_W-1:0] ext_mem_r_addr;
   wire [                                   DATA_W-1:0] ext_mem_r_data;

   wire                                                 int_tvalid;
   wire [                                   DATA_W-1:0] int_tdata;
   wire                                                 int_tready;

   `include "iob_axistream_in_wires.vs"

   // configuration control and status register file.
   `include "iob_axistream_in_subblocks.vs"

   wire tlast_detected_reg;
   wire data_read_nxt;
   wire data_read;

   //CPU INTERFACE
   assign data_ready_rd  = int_tvalid;
   assign interrupt_o    = fifo_level_rd >= fifo_threshold_wr;
   assign data_rvalid_rd = int_tvalid & (~mode_wr);
   assign data_rdata_rd  = int_tdata;

   //System Stream output interface
   // System output valid only if in system stream mode
   assign sys_tvalid_o   = int_tvalid & mode_wr;
   assign sys_tdata_o    = int_tdata;

   assign int_tready     = (mode_wr) ? sys_tready_i : data_read;

   // read data only after valid + ready handshake
   assign data_read_nxt = data_valid_rd & data_ready_rd;
   iob_reg_ca #(
    .DATA_W (1),
    .RST_VAL(1'd0)
   ) data_valid_reg_inst (
       .clk_i (clk_i),
       .cke_i (cke_i),
       .arst_i(arst_i),
       .data_i(data_read_nxt),
       .data_o(data_read)
   );
        

   // empty = fifo empty + no data in fifo2axis
   assign fifo_empty_rd  = fifo_empty & (~int_tvalid);
   // level = fifo level + data in fifo2axis
   assign fifo_level_rd  = fifo_level + int_tvalid;

   wire ready_int;
   // Ready if not full and, if in CSR mode, tlast not detected
   assign ready_int = ~axis_fifo_full & axis_sw_enable & ~(~axis_sw_mode & tlast_detected_reg);

   //word count enable
   assign axis_word_count_en = axis_fifo_write & ~tlast_detected_reg;

   generate
      if (R == 1) begin : gen_no_padding
         //AXI Stream input interface
         assign axis_tready_o   = ready_int;
         //FIFO write
         assign axis_fifo_write = axis_tvalid_i & axis_tready_o;
      end else begin : gen_padding
         //FIFO write FSM
         reg  fifo_write_state_nxt;
         wire fifo_write_state;
         always @* begin
            fifo_write_state_nxt = fifo_write_state;
            case (fifo_write_state)
               0: begin  // Idle
                  // If tvalid, fifo not full, tlast,  and the write wont fill the DATA_W with TDATA_W
                  if (((axis_tvalid_i & ~axis_fifo_full) & axis_tlast_i) &
                           axis_word_count[0+:R_W] != {R_W{1'd1}}) begin
                     fifo_write_state_nxt = 1'b1;
                  end
               end
               default: begin  // Padding
                  if (axis_word_count[0+:R_W] == {R_W{1'd1}} && ~axis_fifo_full) begin
                     fifo_write_state_nxt = 1'b0;
                  end
               end
            endcase
         end

         iob_reg_care #(
            .DATA_W (1),
            .RST_VAL(1'd0)
         ) fifo_write_state_reg (
            .clk_i (axis_clk_i),
            .cke_i (axis_cke_i),
            .arst_i(axis_arst_i),
            .rst_i (axis_sw_rst),
            .en_i  (axis_sw_enable),
            .data_i(fifo_write_state_nxt),
            .data_o(fifo_write_state)
         );

         // Ready if not full, if in CSR mode, tlast not detected and not in padding state
         assign axis_tready_o   = ready_int & ~fifo_write_state;
         //FIFO write if tvalid, tlast, not full or in padding state
         assign axis_fifo_write = (axis_tvalid_i & axis_tready_o) | fifo_write_state;
      end
   endgenerate

   //tlast
   assign axis_tlast = axis_tlast_i & axis_fifo_write;

   // received words counter - count in gray code to use in CDC
   wire [DATA_W-1:0] axis_gray_word_count;
   iob_gray_counter #(
      .W(DATA_W)
   ) word_gray_counter_inst (
      .clk_i (axis_clk_i),
      .cke_i (axis_cke_i),
      .arst_i(axis_arst_i),
      .rst_i (axis_sw_rst),
      .en_i  (axis_word_count_en),
      .data_o(axis_gray_word_count)
   );

   iob_gray2bin #(
      .DATA_W(DATA_W)
   ) gray2bin_axis_word_count (
      .gr_i (axis_gray_word_count),
      .bin_o(axis_word_count)
   );

   //Synchronizers from clk (csrs) to axis domain
   iob_sync #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) sw_rst (
      .clk_i   (axis_clk_i),
      .arst_i  (axis_arst_i),
      .signal_i(soft_reset_wr),
      .signal_o(axis_sw_rst)
   );

   iob_sync #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) sw_enable (
      .clk_i   (axis_clk_i),
      .arst_i  (axis_arst_i),
      .signal_i(enable_wr),
      .signal_o(axis_sw_enable)
   );

   iob_sync #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) sw_mode (
      .clk_i   (axis_clk_i),
      .arst_i  (axis_arst_i),
      .signal_i(mode_wr),
      .signal_o(axis_sw_mode)
   );


   //Synchronizers from axis to clk domain (sw_regs)
   iob_sync #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) tlast_detected_sync (
      .clk_i   (clk_i),
      .arst_i  (arst_i),
      .signal_i(tlast_detected_reg),
      .signal_o(tlast_detected_rd)
   );

   wire [DATA_W-1:0] nwords_rd_gray;
   iob_sync #(
      .DATA_W (DATA_W),
      .RST_VAL({DATA_W{1'd0}})
   ) axis_word_count_gray_sync0 (
      .clk_i   (clk_i),
      .arst_i  (arst_i),
      .signal_i(axis_gray_word_count),
      .signal_o(nwords_rd_gray)
   );

   iob_gray2bin #(
      .DATA_W(DATA_W)
   ) gray2bin_nword_rd (
      .gr_i (nwords_rd_gray),
      .bin_o(nwords_rd)
   );

   //tlast detection
   iob_edge_detect #(
      .EDGE_TYPE("rising"),
      .OUT_TYPE ("step")
   ) tlast_detect (
      .clk_i     (axis_clk_i),
      .cke_i     (axis_cke_i),
      .arst_i    (axis_arst_i),
      .rst_i     (axis_sw_rst),
      .bit_i     (axis_tlast),
      .detected_o(axis_tlast_detected)
   );

   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) tlast_detect_reg (
      .clk_i (axis_clk_i),
      .cke_i (axis_cke_i),
      .arst_i(axis_arst_i),
      .data_i(axis_tlast_detected),
      .data_o(tlast_detected_reg)
   );

   //FIFOs RAM
   genvar p;
   generate
      for (p = 0; p < R; p = p + 1) begin : gen_fifo_ram
         iob_ram_at2p #(
            .DATA_W(TDATA_W),
            .ADDR_W(RAM_ADDR_W)
         ) iob_ram_at2p (
            .w_clk_i (ext_mem_w_clk),
            .w_en_i  (ext_mem_w_en[p]),
            .w_addr_i(ext_mem_w_addr),
            .w_data_i(ext_mem_w_data[p*TDATA_W+:TDATA_W]),

            .r_clk_i (ext_mem_r_clk),
            .r_en_i  (ext_mem_r_en[p]),
            .r_addr_i(ext_mem_r_addr),
            .r_data_o(ext_mem_r_data[p*TDATA_W+:TDATA_W])
         );
      end
   endgenerate

   iob_fifo2axis #(
      .DATA_W    (DATA_W),
      .AXIS_LEN_W(1)
   ) fifo2axis_inst (
      `include "iob_axistream_in_iob_clk_s_s_portmap.vs"
      .rst_i        (soft_reset_wr),
      .en_i         (1'b1),
      .len_i        (1'b1),
      .level_o      (),
      // FIFO I/F
      .fifo_empty_i (fifo_empty),
      .fifo_read_o  (fifo_read),
      .fifo_rdata_i (fifo_data),
      // AXIS I/F
      .axis_tvalid_o(int_tvalid),
      .axis_tdata_o (int_tdata),
      .axis_tready_i(int_tready),
      .axis_tlast_o ()
   );

   //async fifo
   iob_fifo_async #(
      .W_DATA_W(TDATA_W),
      .R_DATA_W(DATA_W),
      .ADDR_W  (FIFO_ADDR_W)
   ) data_fifo (
      .ext_mem_w_clk_o (ext_mem_w_clk),
      .ext_mem_w_en_o  (ext_mem_w_en),
      .ext_mem_w_addr_o(ext_mem_w_addr),
      .ext_mem_w_data_o(ext_mem_w_data),
      .ext_mem_r_clk_o (ext_mem_r_clk),
      .ext_mem_r_en_o  (ext_mem_r_en),
      .ext_mem_r_addr_o(ext_mem_r_addr),
      .ext_mem_r_data_i(ext_mem_r_data),
      //read port (sys clk domain)
      .r_clk_i         (clk_i),
      .r_cke_i         (cke_i),
      .r_arst_i        (arst_i),
      .r_rst_i         (soft_reset_wr),
      .r_en_i          (fifo_read),
      .r_data_o        (fifo_data),
      .r_empty_o       (fifo_empty),
      .r_full_o        (fifo_full_rd),
      .r_level_o       (fifo_level),
      //write port (axis clk domain)
      .w_clk_i         (axis_clk_i),
      .w_cke_i         (axis_cke_i),
      .w_arst_i        (axis_arst_i),
      .w_rst_i         (axis_sw_rst),
      .w_en_i          (axis_fifo_write),
      .w_data_i        (axis_tdata_i),
      .w_empty_o       (),
      .w_full_o        (axis_fifo_full),
      .w_level_o       ()
   );

endmodule
