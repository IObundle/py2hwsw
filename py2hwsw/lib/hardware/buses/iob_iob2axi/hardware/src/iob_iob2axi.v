// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
`include "iob_iob2axi_conf.vh"

module iob_iob2axi #(
   `include "iob_iob2axi_params.vs"
) (
   `include "iob_iob2axi_io.vs"
);

   `include "iob_functions.vs"

   wire rst_i;
   assign rst_i = arst_i;

   wire run_int;
   wire run_wr, run_rd;
   wire ready_int;
   wire ready_rd, ready_wr;
   wire error_rd, error_wr;

   wire in_fifo_ready, out_fifo_ready;

   wire rd_valid, wr_valid;
   wire [ADDR_W-1:0] rd_addr, wr_addr;  //**
   wire [DATA_W-1:0] rd_wdata, wr_rdata;
   wire [DATA_W/8-1:0] rd_wstrb, wr_rstrb;
   wire rd_ready, wr_ready;

   assign ready_o     = ready_int & ~run_int;
   assign error_o     = error_rd | error_wr;

   assign iob_ready_o = |iob_wstrb_i ? in_fifo_ready : out_fifo_ready;

   //
   // Input FIFO
   //
   wire                       in_fifo_full;
   wire                       in_fifo_wr;
   assign                       in_fifo_wr = iob_valid_i & |iob_wstrb_i & ~in_fifo_full;
   wire [DATA_W+DATA_W/8-1:0] in_fifo_wdata;
   assign in_fifo_wdata = {iob_wdata_i, iob_wstrb_i};

   wire                       in_fifo_empty;
   wire                       in_fifo_rd;
   assign                       in_fifo_rd = wr_valid;
   wire [DATA_W+DATA_W/8-1:0] in_fifo_rdata;

   wire [       AXI_LEN_W:0] in_fifo_level;

   reg                        in_fifo_empty_reg;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         in_fifo_empty_reg <= 1'b1;
      end else begin
         in_fifo_empty_reg <= in_fifo_empty;
      end
   end

   assign wr_rdata = in_fifo_rdata[DATA_W/8+:DATA_W];
   assign wr_rstrb = in_fifo_rdata[0+:DATA_W/8];

   reg wr_ready_int;
   assign wr_ready = wr_ready_int & ~in_fifo_empty_reg;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         wr_ready_int <= 1'b0;
      end else begin
         wr_ready_int <= wr_valid;
      end
   end

   reg in_fifo_ready_int;
   assign in_fifo_ready = in_fifo_ready_int & ~in_fifo_full;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         in_fifo_ready_int <= 1'b0;
      end else begin
         in_fifo_ready_int <= iob_valid_i & |iob_wstrb_i;
      end
   end

   iob_fifo_sync #(
      .W_DATA_W(DATA_W + DATA_W / 8),
      .R_DATA_W(DATA_W + DATA_W / 8),
      .ADDR_W  (AXI_LEN_W)
   ) iob_fifo_sync0 (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),

      .rst_i(1'b0),

      .w_en_i  (in_fifo_wr),
      .w_data_i(in_fifo_wdata),
      .w_full_o(in_fifo_full),

      .r_en_i   (in_fifo_rd),
      .r_data_o (in_fifo_rdata),
      .r_empty_o(in_fifo_empty),

      .level_o(in_fifo_level)
   );

   //
   // Output FIFO
   //
   wire                out_fifo_full;
   wire                out_fifo_wr;
   assign                out_fifo_wr = rd_valid & |rd_wstrb & ~out_fifo_full;
   wire [  DATA_W-1:0] out_fifo_wdata;
   assign out_fifo_wdata = rd_wdata;

   wire                out_fifo_empty;
   wire                out_fifo_rd;
   assign                out_fifo_rd = iob_valid_i & ~|iob_wstrb_i & ~out_fifo_empty;
   wire [  DATA_W-1:0] out_fifo_rdata;

   wire [AXI_LEN_W:0] out_fifo_level;
   wire [AXI_LEN_W:0] out_fifo_capacity;
   assign out_fifo_capacity = {1'b1, AXI_LEN_W'd0} - out_fifo_level;

   reg                 out_fifo_empty_reg;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         out_fifo_empty_reg <= 1'b1;
      end else begin
         out_fifo_empty_reg <= out_fifo_empty;
      end
   end

   reg rd_ready_int;
   assign rd_ready = rd_ready_int & ~out_fifo_full;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         rd_ready_int <= 1'b0;
      end else begin
         rd_ready_int <= rd_valid;
      end
   end

   assign iob_rdata_o = out_fifo_rdata;

   reg out_fifo_ready_int;
   assign out_fifo_ready = out_fifo_ready_int & ~out_fifo_empty_reg;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         out_fifo_ready_int <= 1'b0;
      end else begin
         out_fifo_ready_int <= iob_valid_i & ~|iob_wstrb_i;
      end
   end

   iob_fifo_sync #(
      .W_DATA_W(DATA_W),
      .R_DATA_W(DATA_W),
      .ADDR_W  (AXI_LEN_W)
   ) iob_fifo_sync1 (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),

      .rst_i(1'b0),

      .w_en_i  (out_fifo_wr),
      .w_data_i(out_fifo_wdata),
      .w_full_o(out_fifo_full),

      .r_en_i   (out_fifo_rd),
      .r_data_o (out_fifo_rdata),
      .r_empty_o(out_fifo_empty),

      .level_o(out_fifo_level)
   );

   //
   // Compute next run
   //
   wire [  AXI_LEN_W:0] length_int;
   assign length_int = direction ? in_fifo_level : out_fifo_capacity;

   reg  [AXI_LEN_W-1:0] count;
   wire                  count_en;
   assign                  count_en = ~&count & |length_int;

   assign run_int   = ready_int & |length_int & (length_int[AXI_LEN_W] | &count);
   assign run_wr    = direction ? run_int : 1'b0;
   assign run_rd    = direction ? 1'b0 : run_int;

   assign ready_int = ready_wr & ready_rd;

   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         count <= AXI_LEN_W'd0;
      end else if (run_int) begin
         count <= AXI_LEN_W'd0;
      end else if (count_en) begin
         count <= count + 1'b1;
      end
   end

   //
   // Compute first address and burst length for the next data transfer
   //
   localparam WADDR_W = ADDR_W - $clog2(DATA_W / 8);  // Word address width

   reg  [AXI_LEN_W-1:0] length_burst;

   reg  [    ADDR_W-1:0] addr_int;
   reg  [   WADDR_W-1:0] addr_int_next;
   wire [   WADDR_W-1:0] addr4k;
   wire [   WADDR_W-1:0] addrRem;
   wire [   WADDR_W-1:0] minAddr;
   assign addr4k = {addr_int[ADDR_W-1:12], {(12 - (ADDR_W - WADDR_W)) {1'b1}}};
   assign addrRem = addr_int[ADDR_W-1-:WADDR_W] + length_int - 1'b1;
   assign minAddr = iob_min(addr4k, addrRem);

   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         addr_int <= {ADDR_W{1'b0}};
      end else if (run_i) begin
         addr_int <= addr_i;
      end else if (run_int) begin
         addr_int <= {addr_int_next, {(ADDR_W - WADDR_W) {1'b0}}};
      end
   end

   always @* begin
      addr_int_next = minAddr + 1'b1;

      if (minAddr == addr4k) begin
         length_burst = addr4k - addr_int[ADDR_W-1-:WADDR_W];
      end else begin  // minAddr == addrRem
         length_burst = length_int - 1'b1;
      end
   end

   //
   // AXI Read
   //
   iob_iob2axi_rd #(
      .ADDR_W(ADDR_W),
      .DATA_W(DATA_W)
   ) iob_iob2axi_rd0 (
      .clk_i(clk_i),
      .rst_i(rst_i),

      // Control I/F
      .run_i   (run_rd),
      .addr_i  (addr_int),
      .length_i(length_burst),
      .ready_o (ready_rd),
      .error_o (error_rd),

      // AXI-4 full read manager I/F
      `include "iob_iob2axi_rd_m_axi_read_m_m_portmap.vs"
      // Native Manager Write I/F
      .m_iob_valid_o(rd_valid),
      .m_iob_addr_o (rd_addr),
      .m_iob_wdata_o(rd_wdata),
      .m_iob_wstrb_o(rd_wstrb),
      .m_iob_ready_i(rd_ready)
   );

   //
   // AXI Write
   //
   iob_iob2axi_wr #(
      .ADDR_W(ADDR_W),
      .DATA_W(DATA_W)
   ) iob_iob2axi_wr0 (
      .clk_i(clk_i),
      .rst_i(rst_i),

      // Control I/F
      .run_i   (run_wr),
      .addr_i  (addr_int),
      .length_i(length_burst),
      .ready_o (ready_wr),
      .error_o (error_wr),

      // AXI-4 full write manager I/F
      `include "iob_iob2axi_wr_m_axi_write_m_m_portmap.vs"

      // Native Manager Read I/F
      .m_iob_valid_o(wr_valid),
      .m_iob_addr_o (wr_addr),
      .m_iob_rdata_i(wr_rdata),
      .m_iob_rstrb_i(wr_rstrb),
      .m_iob_ready_i(wr_ready)
   );

endmodule
