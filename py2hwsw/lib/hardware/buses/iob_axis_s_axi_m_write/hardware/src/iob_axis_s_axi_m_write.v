// SPDX-FileCopyrightText: 2026 IObundle
//
// SPDX-License-Identifier: CERN-OHL-S-2.0

`timescale 1ns / 1ps

module iob_axis_s_axi_m_write #(
   parameter AXI_ADDR_W = 0,
   parameter AXI_DATA_W = 32,  // We currently only support 4 byte transfers
   parameter AXI_LEN_W  = 8,
   parameter AXI_ID_W   = 1
) (
   // Global signals
   `include "iob_axis_s_axi_m_write_iob_clk_s_port.vs"
   input rst_i,

   // Axi master interface
   `include "iob_axis_s_axi_m_write_axi_write_m_port.vs"

   // Configuration
   input  [AXI_ADDR_W-1:0] w_addr_i,
   input  [ AXI_LEN_W-1:0] w_length_i,
   input                   w_start_transfer_i,
   input  [         2-1:0] w_burst_type_i,
   output                  w_busy_o,
   output [         2-1:0] w_resp_o,

   // Axi stream input
   input      [AXI_DATA_W-1:0] axis_in_data_i,
   input                       axis_in_valid_i,
   output reg                  axis_in_ready_o
);

   localparam WAIT_START = 2'd0, TRANSF_BURST = 2'd1, WAIT_BRESP = 2'd2;

   // Internal signals
   wire [   AXI_DATA_W-1:0] axi_wdata_nxt;


   // Instantiation wires
   wire [            2-1:0] state;
   wire [    AXI_LEN_W-1:0] transf_data_count;
   wire [(AXI_LEN_W+1)-1:0] length;
   wire [(AXI_LEN_W+1)-1:0] burst_length_beats = {1'b0, w_length_i} + 1'b1;

   // Assignment to outputs
   // AXI
   assign axi_wdata_nxt = axis_in_data_i;
   // W channel output registers can load a new beat when the current one is
   // accepted by the subordinate or when they hold no valid beat
   wire w_reg_en = axi_wready_i | ~axi_wvalid_o;
   // Constants
   assign axi_awid_o    = {AXI_ID_W{1'd0}};
   assign axi_awsize_o  = 3'd2;
   assign axi_awburst_o = w_burst_type_i;
   assign axi_awlock_o  = 2'd0;
   assign axi_awcache_o = 4'd2;
   assign axi_awprot_o  = 3'd2;
   assign axi_awqos_o   = 4'd0;
   assign axi_wstrb_o   = 4'b1111;
   assign axi_bready_o  = 1'b1;

   // Busy signal
   assign w_busy_o      = state != WAIT_START;

   // FSM signals
   reg                       transfer_count_rst;
   reg                       transfer_count_incr;
   reg                       axi_awvalid_nxt;
   reg  [    AXI_ADDR_W-1:0] axi_awaddr_nxt;
   reg  [     AXI_LEN_W-1:0] axi_awlen_nxt;
   reg                       axi_wvalid_nxt;
   reg                       axi_wlast_nxt;
   reg  [             2-1:0] state_nxt;
   reg  [ (AXI_LEN_W+1)-1:0] length_nxt;
   reg  [(AXI_ADDR_W+1)-1:0] last_addr;
   reg                       address_done_nxt;
   reg                       data_done_nxt;
   wire                      address_done;
   wire                      data_done;
   reg  [             2-1:0] w_resp_nxt;

   always @* begin
      // Calculate the last address of the burst using the normal burst length
      last_addr           = w_addr_i + ((burst_length_beats << 2) - 1);

      // State machine
      // Default assignments
      state_nxt           = state;
      axi_awvalid_nxt     = 1'd0;
      axi_awaddr_nxt      = axi_awaddr_o;
      axi_awlen_nxt       = axi_awlen_o;
      length_nxt          = length;
      axi_wvalid_nxt      = 1'd0;
      axis_in_ready_o     = 1'd0;
      axi_wlast_nxt       = 1'd0;

      address_done_nxt    = address_done;
      data_done_nxt       = data_done;
      transfer_count_rst  = 1'd0;
      transfer_count_incr = 1'd0;
      w_resp_nxt          = w_resp_o;

      case (state)
         WAIT_START: begin
            w_resp_nxt = 2'b00;
            if (w_start_transfer_i) begin  // Start transfer in the next state
               // FIXED bursts do not advance address, so no 4k split is required.
               // INCR bursts use full length only if they remain in the same 4k boundary.
               if ((w_burst_type_i == 2'b00) || (w_addr_i[12] == last_addr[12])) begin
                  axi_awlen_nxt = w_length_i;
               end else begin
                  // If the burst's last address is in the next 4k boundary,
                  // the burst length is the remaining space in the current 4k boundary
                  axi_awlen_nxt = ((13'd4096 - (w_addr_i[0+:13])) >> 2) - 1;
               end

               // Set address and length for the burst
               axi_awaddr_nxt = w_addr_i;  // Set start address
               axi_awvalid_nxt = 1'd1;  // Start transfer
               length_nxt = burst_length_beats - (axi_awlen_nxt + 1);  // Set remaining length
               // Set valid data for this burst and count it when the transfer is done
               axis_in_ready_o = w_reg_en;
               axi_wvalid_nxt = axis_in_valid_i;
               transfer_count_incr = w_reg_en & axis_in_valid_i;

               // Set the last signal in the last data
               if ((transf_data_count == axi_awlen_nxt) && axis_in_valid_i) begin
                  axi_wlast_nxt = 1'd1;
                  if (w_reg_en) begin
                     data_done_nxt = 1'd1;
                  end
               end
               state_nxt = TRANSF_BURST;
            end
         end

         TRANSF_BURST: begin  // Set burst address, send data and wait for both ready signals
            // Check if the address channel is done
            if (!address_done) begin
               if (axi_awready_i) begin
                  address_done_nxt = 1'd1;
               end else begin
                  axi_awvalid_nxt = 1'd1;  // Send address
               end
            end

            // Check if the data channel is done
            if (!data_done) begin
               axis_in_ready_o     = w_reg_en;  // Set ready signal for the input stream
               transfer_count_incr = w_reg_en & axis_in_valid_i;
               axi_wvalid_nxt      = axis_in_valid_i;
               if ((transf_data_count == axi_awlen_o) && axis_in_valid_i) begin
                  axi_wlast_nxt = 1'd1;
                  if (w_reg_en) begin
                     data_done_nxt = 1'd1;
                  end
               end
            end

            // Check if both channels are done
            if((data_done_nxt && address_done_nxt) ||
               ((data_done && address_done_nxt) ||
               (data_done_nxt && address_done))) begin
               state_nxt = WAIT_BRESP;  // Wait for the response
            end

         end

         default: begin  // WAIT_BRESP: Wait for response
            if (axi_bvalid_i) begin  // When the response is valid, check if the transfer is done
               w_resp_nxt         = axi_bresp_i;
               transfer_count_rst = 1'd1;
               // Reset the done signals
               address_done_nxt   = 1'd0;
               data_done_nxt      = 1'd0;
               if ((length == 0) || (axi_bresp_i != 2'b00)) begin
                  state_nxt = WAIT_START;
               end else begin  // Transfer the remaining data
                  // The previous burst was not in the same 4k boundary, so the next burst will be
                  axi_awlen_nxt   = length - 1;
                  axi_awaddr_nxt  = axi_awaddr_o + ((axi_awlen_o + 1) << 2);
                  axi_awvalid_nxt = 1'd1;
                  length_nxt      = 0;
                  state_nxt       = TRANSF_BURST;
               end
            end
         end
      endcase
   end

   // Registers for address_done and data_done
   iob_reg_car #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) address_done_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(address_done_nxt),
       .data_o(address_done)
   );

   iob_reg_car #(
      .DATA_W (1),
      .RST_VAL(1'd0)
   ) data_done_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(data_done_nxt),
       .data_o(data_done)
   );

   iob_counter #(
      .DATA_W (AXI_LEN_W),
      .RST_VAL(0)
   ) transfer_count_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (transfer_count_rst),
       .en_i  (transfer_count_incr),
       .data_o(transf_data_count)
   );

   iob_reg_car #(
      .DATA_W ((AXI_LEN_W + 1)),
      .RST_VAL(0)
   ) length_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(length_nxt),
       .data_o(length)
   );

   iob_reg_car #(
      .DATA_W (2),
      .RST_VAL(0)
   ) state_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(state_nxt),
       .data_o(state)
   );

   // AXI Interface registers
   iob_reg_car #(
      .DATA_W (AXI_LEN_W),
      .RST_VAL(0)
   ) axi_awlen_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(axi_awlen_nxt),
       .data_o(axi_awlen_o)
   );

   iob_reg_car #(
      .DATA_W (AXI_ADDR_W),
      .RST_VAL(0)
   ) axi_awaddr_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(axi_awaddr_nxt),
       .data_o(axi_awaddr_o)
   );

   iob_reg_car #(
      .DATA_W (1),
      .RST_VAL(0)
   ) axi_awvalid_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(axi_awvalid_nxt),
       .data_o(axi_awvalid_o)
   );

   iob_reg_care #(
      .DATA_W (AXI_DATA_W),
      .RST_VAL(0)
   ) axi_wdata_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .en_i  (w_reg_en),
       .data_i(axi_wdata_nxt),
       .data_o(axi_wdata_o)
   );

   iob_reg_care #(
      .DATA_W (1),
      .RST_VAL(0)
   ) axi_wvalid_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .en_i  (w_reg_en),
       .data_i(axi_wvalid_nxt),
       .data_o(axi_wvalid_o)
   );

   iob_reg_care #(
      .DATA_W (1),
      .RST_VAL(0)
   ) axi_wlast_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .en_i  (w_reg_en),
       .data_i(axi_wlast_nxt),
       .data_o(axi_wlast_o)
   );

   iob_reg_car #(
      .DATA_W (2),
      .RST_VAL(2'b00)
   ) w_resp_reg (
       `include "iob_axis_s_axi_m_write_iob_clk_s_s_portmap.vs"
       .rst_i (rst_i),
       .data_i(w_resp_nxt),
       .data_o(w_resp_o)
   );

endmodule
