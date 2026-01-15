// SPDX-FileCopyrightText: 2014-2018 Alex Forencich
// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

// Language: Verilog 2001

`timescale 1ns / 1ps

/*
 * Arbiter module
 */
module iob_arbiter #(
   parameter PORTS        = 4,
   // arbitration type: "PRIORITY" or "ROUND_ROBIN"
   parameter [11*8-1:0] TYPE         = "PRIORITY",
   // block type: "NONE", "REQUEST", "ACKNOWLEDGE"
   parameter [11*8-1:0] BLOCK        = "NONE",
   // LSB priority: "LOW", "HIGH"
   parameter [4*8-1:0] LSB_PRIORITY = "LOW"
) (
   input wire clk,
   input wire arst,
   input wire rst,

   input wire [PORTS-1:0] request,
   input wire [PORTS-1:0] acknowledge,

   output wire [        PORTS-1:0] grant,
   output wire                     grant_valid,
   output wire [$clog2(PORTS)-1:0] grant_encoded
);

   reg [PORTS-1:0] grant_reg, grant_next;
   reg grant_valid_reg, grant_valid_next;
   reg [$clog2(PORTS)-1:0] grant_encoded_reg, grant_encoded_next;

   assign grant_valid   = grant_valid_reg;
   assign grant         = grant_reg;
   assign grant_encoded = grant_encoded_reg;

   wire                     request_valid;
   wire [$clog2(PORTS)-1:0] request_index;
   wire [        PORTS-1:0] request_mask;

   iob_priority_encoder #(
      .WIDTH       (PORTS),
      .LSB_PRIORITY(LSB_PRIORITY)
   ) iob_priority_encoder_inst (
      .input_unencoded (request),
      .output_valid    (request_valid),
      .output_encoded  (request_index),
      .output_unencoded(request_mask)
   );

   reg [PORTS-1:0] mask_reg, mask_next;

   wire                     masked_request_valid;
   wire [$clog2(PORTS)-1:0] masked_request_index;
   wire [        PORTS-1:0] masked_request_mask;

   iob_priority_encoder #(
      .WIDTH       (PORTS),
      .LSB_PRIORITY(LSB_PRIORITY)
   ) iob_priority_encoder_masked (
      .input_unencoded (request & mask_reg),
      .output_valid    (masked_request_valid),
      .output_encoded  (masked_request_index),
      .output_unencoded(masked_request_mask)
   );

   wire grant_condition;

   generate
       if (BLOCK == "REQUEST") begin : g_block_request
           assign grant_condition = |(grant_reg & request);
       end else if (BLOCK == "ACKNOWLEDGE") begin : g_block_acknowledge
           assign grant_condition = grant_valid && !(|(grant_reg & acknowledge));
       end else begin : g_block_none
           assign grant_condition = 1'b0;
       end
   endgenerate

   generate
       if (TYPE == "ROUND_ROBIN") begin : g_type_rr_wires
           wire [PORTS-1:0] mask_next_req_valid;
           wire [PORTS-1:0] mask_next_else;
           if (LSB_PRIORITY == "HIGH") begin : g_mask_next_lsb_priority_high
               assign mask_next_req_valid = {PORTS{1'b1}} << (masked_request_index + 1);
               assign mask_next_else      = {PORTS{1'b1}} << (request_index + 1);
           end else begin : g_mask_next_lsb_priority_low
               assign mask_next_req_valid = {PORTS{1'b1}} >> (PORTS - masked_request_index);
               assign mask_next_else      = {PORTS{1'b1}} >> (PORTS - request_index);
           end

           always @* begin
              grant_next         = 0;
              grant_valid_next   = 0;
              grant_encoded_next = 0;
              mask_next          = mask_reg;

              if (grant_condition) begin
                 // granted request still asserted; hold it
                 grant_valid_next   = grant_valid_reg;
                 grant_next         = grant_reg;
                 grant_encoded_next = grant_encoded_reg;
              end else if (request_valid) begin
                 if (masked_request_valid) begin
                    grant_valid_next   = 1;
                    grant_next         = masked_request_mask;
                    grant_encoded_next = masked_request_index;
                    mask_next          = mask_next_req_valid;
                 end else begin
                    grant_valid_next   = 1;
                    grant_next         = request_mask;
                    grant_encoded_next = request_index;
                    mask_next          = mask_next_else;
                 end
              end
           end
       end else begin : g_type_priority
           always @* begin
              grant_next         = 0;
              grant_valid_next   = 0;
              grant_encoded_next = 0;
              mask_next          = mask_reg;

              if (grant_condition) begin
                 // granted request still asserted; hold it
                 grant_valid_next   = grant_valid_reg;
                 grant_next         = grant_reg;
                 grant_encoded_next = grant_encoded_reg;
              end else if (request_valid) begin
                 grant_valid_next   = 1;
                 grant_next         = request_mask;
                 grant_encoded_next = request_index;
              end
           end
       end
    endgenerate

   always @(posedge clk, posedge arst) begin
      if (arst) begin
         grant_reg         <= 0;
         grant_valid_reg   <= 0;
         grant_encoded_reg <= 0;
         mask_reg          <= 0;
      end else if (rst) begin
         grant_reg         <= 0;
         grant_valid_reg   <= 0;
         grant_encoded_reg <= 0;
         mask_reg          <= 0;
      end else begin
         grant_reg         <= grant_next;
         grant_valid_reg   <= grant_valid_next;
         grant_encoded_reg <= grant_encoded_next;
         mask_reg          <= mask_next;
      end
   end

endmodule
