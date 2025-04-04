// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps


module iob_iob2axi_read #(
   `include "iob_iob2axi_read_params.vs"
) (
   `include "iob_iob2axi_read_io.vs"
);

   localparam axi_arsize = $clog2(DATA_W / 8);

   localparam ADDR_HS = 1'h0, READ = 1'h1;

   // State signals
   reg state, state_nxt;

   // Counter, error and ready register signals
   reg [AXI_LEN_W-1:0] counter, counter_nxt;
   reg                  error_nxt;
   reg                  ready_nxt;

   reg                  m_axi_arvalid_int;
   reg                  m_axi_rready_int;

   // Control register signals
   reg  [   ADDR_W-1:0] addr_reg;
   reg  [AXI_LEN_W-1:0] length_reg;

   // Hold
   reg                  m_iob_valid_reg;
   wire                 hold;
   assign hold = m_iob_valid_reg & ~m_iob_ready_i;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         m_iob_valid_reg <= 1'b0;
      end else begin
         m_iob_valid_reg <= m_iob_valid_o;
      end
   end

   reg [DATA_W-1:0] m_axi_rdata_reg;
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         m_axi_rdata_reg <= {DATA_W{1'b0}};
      end else if (~hold) begin
         m_axi_rdata_reg <= m_axi_rdata_i;
      end
   end

   assign m_iob_wdata_o   = hold ? m_axi_rdata_reg : m_axi_rdata_i;
   assign m_iob_wstrb_o   = {(DATA_W / 8) {1'b1}};

   // Read address
   assign m_axi_arid_o    = {AXI_ID_W{1'd0}};
   assign m_axi_arvalid_o = m_axi_arvalid_int;
   assign m_axi_araddr_o  = run_i ? addr_i : addr_reg;
   assign m_axi_arlen_o   = run_i ? length_i : length_reg;
   assign m_axi_arsize_o  = axi_arsize;
   assign m_axi_arburst_o = {AXI_BURST_W{1'd1}};
   assign m_axi_arlock_o  = {AXI_LOCK_W{1'b0}};
   assign m_axi_arcache_o = 'd2;
   assign m_axi_arprot_o  = 'd2;
   assign m_axi_arqos_o   = {AXI_QOS_W{1'd0}};

   // Read
   assign m_axi_rready_o  = m_axi_rready_int;

   reg ready_reg;
   assign ready_o = ready_reg;
   reg error_reg;
   assign error_o = error_reg;
   // Counter, error and ready registers
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         counter   <= {AXI_LEN_W{1'd0}};
         error_reg <= 1'b0;
         ready_reg <= 1'b1;
      end else begin
         counter   <= counter_nxt;
         error_reg <= error_nxt;
         ready_reg <= ready_nxt;
      end
   end

   // Control registers
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         addr_reg   <= {ADDR_W{1'b0}};
         length_reg <= {AXI_LEN_W{1'd0}};
      end else if (run_i) begin
         addr_reg   <= addr_i;
         length_reg <= length_i;
      end
   end

   wire rst_valid_int;
   assign rst_valid_int = (state_nxt == ADDR_HS) ? 1'b1 : 1'b0;
   reg arvalid_int;

   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         arvalid_int <= 1'b0;
      end else if (rst_valid_int) begin
         arvalid_int <= 1'b1;
      end else if (m_axi_arready_i) begin
         arvalid_int <= 1'b0;
      end
   end

   //
   // FSM
   //

   // State register
   always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         state <= ADDR_HS;
      end else begin
         state <= state_nxt;
      end
   end


   reg m_iob_valid_o_reg;
   assign m_iob_valid_o = m_iob_valid_o_reg;
   // State machine
   always @* begin
      state_nxt         = state;

      error_nxt         = error_o;
      ready_nxt         = 1'b0;
      counter_nxt       = counter;

      m_iob_valid_o_reg = 1'b0;

      m_axi_arvalid_int = 1'b0;
      m_axi_rready_int  = 1'b0;

      case (state)
         // Read address handshake
         ADDR_HS: begin
            counter_nxt = {AXI_LEN_W{1'd0}};
            ready_nxt   = 1'b1;

            if (run_i) begin
               m_axi_arvalid_int = 1'b1;

               if (m_axi_arready_i) begin
                  state_nxt = READ;

                  ready_nxt = 1'b0;
               end
            end
         end
         // Read data
         READ: begin
            m_iob_valid_o_reg = m_axi_rvalid_i;

            m_axi_arvalid_int = arvalid_int;
            m_axi_rready_int  = ~hold;

            if (~hold & m_axi_rvalid_i) begin
               if (counter == length_reg) begin
                  error_nxt = |{~m_axi_rlast_i, m_axi_rresp_i};

                  state_nxt = ADDR_HS;
               end

               counter_nxt = counter + 1'b1;
            end
         end
      endcase
   end

endmodule
