// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_timer_csrs_conf.vh"

module iob_timer_csrs #(
    parameter ADDR_W = `IOB_TIMER_CSRS_ADDR_W,  // Don't change this parameter value!
    parameter DATA_W = `IOB_TIMER_CSRS_DATA_W
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // control_if_s: CSR control interface. Interface type defined by `csr_if` parameter.
    input iob_valid_i,
    input [4-1:0] iob_addr_i,
    input [DATA_W-1:0] iob_wdata_i,
    input [DATA_W/8-1:0] iob_wstrb_i,
    output iob_rvalid_o,
    output [DATA_W-1:0] iob_rdata_o,
    output iob_ready_o,
    // reset_o: reset register interface
    output reset_rdata_o,
    // enable_o: enable register interface
    output enable_rdata_o,
    // sample_o: sample register interface
    output sample_rdata_o,
    // data_low_i: data_low register interface
    input [32-1:0] data_low_wdata_i,
    // data_high_i: data_high register interface
    input [32-1:0] data_high_wdata_i
);

// Internal iob interface
    wire internal_iob_valid;
    wire [ADDR_W-1:0] internal_iob_addr;
    wire [DATA_W-1:0] internal_iob_wdata;
    wire [DATA_W/8-1:0] internal_iob_wstrb;
    wire internal_iob_rvalid;
    wire [DATA_W-1:0] internal_iob_rdata;
    wire internal_iob_ready;
    wire state;
    reg state_nxt;
    wire write_en;
    wire [ADDR_W-1:0] internal_iob_addr_stable;
    wire [ADDR_W-1:0] internal_iob_addr_reg;
    wire internal_iob_addr_reg_en;
    wire reset_wdata;
    wire reset_w_valid;
    wire enable_wdata;
    wire enable_w_valid;
    wire sample_wdata;
    wire sample_w_valid;
    wire [32-1:0] data_low_rdata;
    wire [32-1:0] data_high_rdata;
    wire iob_rvalid_out;
    reg iob_rvalid_nxt;
    wire [32-1:0] iob_rdata_out;
    reg [32-1:0] iob_rdata_nxt;
    wire iob_ready_out;
    reg iob_ready_nxt;


    // Include iob_functions for use in parameters
    localparam IOB_MAX_W = ADDR_W;
    function [IOB_MAX_W-1:0] iob_max;
       input [IOB_MAX_W-1:0] a;
       input [IOB_MAX_W-1:0] b;
       begin
          if (a > b) iob_max = a;
          else iob_max = b;
       end
    endfunction

    function integer iob_abs;
       input integer a;
       begin
          iob_abs = (a >= 0) ? a : -a;
       end
    endfunction

    `define IOB_NBYTES (DATA_W/8)
    `define IOB_NBYTES_W $clog2(`IOB_NBYTES)
    `define IOB_WORD_ADDR(ADDR) ((ADDR>>`IOB_NBYTES_W)<<`IOB_NBYTES_W)

    localparam WSTRB_W = DATA_W/8;

    //FSM states
    localparam WAIT_REQ = 1'd0;
    localparam WAIT_RVALID = 1'd1;


    assign internal_iob_addr_reg_en = internal_iob_valid;
    assign internal_iob_addr_stable = internal_iob_valid ? internal_iob_addr : internal_iob_addr_reg;

    assign write_en = |internal_iob_wstrb;

    //write address
    wire [($clog2(WSTRB_W)+1)-1:0] byte_offset;
    iob_ctls #(.W(WSTRB_W), .MODE(0), .SYMBOL(0)) bo_inst (.data_i(internal_iob_wstrb), .count_o(byte_offset));

    wire [ADDR_W-1:0] wstrb_addr;
    assign wstrb_addr = `IOB_WORD_ADDR(internal_iob_addr_stable) + byte_offset;

// Create a special readstrobe for "REG" (auto) CSRs.
// LSBs 0 = read full word; LSBs 1 = read byte; LSBs 2 = read half word; LSBs 3 = read byte.
   reg [1:0] shift_amount;
   always @(*) begin
      case (internal_iob_addr_stable[1:0])
         // Access entire word
         2'b00: shift_amount = 2;
         // Access single byte
         2'b01: shift_amount = 0;
         // Access half word
         2'b10: shift_amount = 1;
         // Access single byte
         2'b11: shift_amount = 0;
         default: shift_amount = 0;
      endcase
    end


//NAME: reset;
//MODE: W; WIDTH: 1; RST_VAL: 0; ADDR: 0; SPACE (bytes): 1 (max); TYPE: REG. 

    assign reset_wdata = internal_iob_wdata[0+:1];
    wire reset_addressed_w;
    assign reset_addressed_w =  (wstrb_addr < 1);
    assign reset_w_valid = internal_iob_valid & (write_en & reset_addressed_w);
    iob_reg_cae #(
      .DATA_W(1),
      .RST_VAL(1'd0)
    ) reset_datareg_wr (
      .clk_i  (clk_i),
      .cke_i  (cke_i),
      .arst_i (arst_i),
      .en_i   (reset_w_valid),
      .data_i (reset_wdata),
      .data_o (reset_rdata_o)
    );



//NAME: enable;
//MODE: W; WIDTH: 1; RST_VAL: 0; ADDR: 1; SPACE (bytes): 1 (max); TYPE: REG. 

    assign enable_wdata = internal_iob_wdata[8+:1];
    wire enable_addressed_w;
    assign enable_addressed_w = (wstrb_addr >= (1)) &&  (wstrb_addr < 2);
    assign enable_w_valid = internal_iob_valid & (write_en & enable_addressed_w);
    iob_reg_cae #(
      .DATA_W(1),
      .RST_VAL(1'd0)
    ) enable_datareg_wr (
      .clk_i  (clk_i),
      .cke_i  (cke_i),
      .arst_i (arst_i),
      .en_i   (enable_w_valid),
      .data_i (enable_wdata),
      .data_o (enable_rdata_o)
    );



//NAME: sample;
//MODE: W; WIDTH: 1; RST_VAL: 0; ADDR: 2; SPACE (bytes): 1 (max); TYPE: REG. 

    assign sample_wdata = internal_iob_wdata[16+:1];
    wire sample_addressed_w;
    assign sample_addressed_w = (wstrb_addr >= (2)) &&  (wstrb_addr < 3);
    assign sample_w_valid = internal_iob_valid & (write_en & sample_addressed_w);
    iob_reg_cae #(
      .DATA_W(1),
      .RST_VAL(1'd0)
    ) sample_datareg_wr (
      .clk_i  (clk_i),
      .cke_i  (cke_i),
      .arst_i (arst_i),
      .en_i   (sample_w_valid),
      .data_i (sample_wdata),
      .data_o (sample_rdata_o)
    );



//NAME: data_low;
//MODE: R; WIDTH: 32; RST_VAL: 0; ADDR: 4; SPACE (bytes): 4 (max); TYPE: REG. 

    wire data_low_addressed_r;
    assign data_low_addressed_r = (internal_iob_addr_stable>>shift_amount >= (4>>shift_amount)) && (internal_iob_addr_stable>>shift_amount <= iob_max(1,7>>shift_amount));
    iob_reg_ca #(
      .DATA_W(32),
      .RST_VAL(32'd0)
    ) data_low_datareg_rd (
      .clk_i  (clk_i),
      .cke_i  (cke_i),
      .arst_i (arst_i),
      .data_i (data_low_wdata_i),
      .data_o (data_low_rdata)
    );



//NAME: data_high;
//MODE: R; WIDTH: 32; RST_VAL: 0; ADDR: 8; SPACE (bytes): 4 (max); TYPE: REG. 

    wire data_high_addressed_r;
    assign data_high_addressed_r = (internal_iob_addr_stable>>shift_amount >= (8>>shift_amount)) && (internal_iob_addr_stable>>shift_amount <= iob_max(1,11>>shift_amount));
    iob_reg_ca #(
      .DATA_W(32),
      .RST_VAL(32'd0)
    ) data_high_datareg_rd (
      .clk_i  (clk_i),
      .cke_i  (cke_i),
      .arst_i (arst_i),
      .data_i (data_high_wdata_i),
      .data_o (data_high_rdata)
    );



//NAME: version;
//MODE: R; WIDTH: 16; RST_VAL: 0081; ADDR: 12; SPACE (bytes): 2 (max); TYPE: REG. 

    wire version_addressed_r;
    assign version_addressed_r = (internal_iob_addr_stable>>shift_amount >= (12>>shift_amount)) && (internal_iob_addr_stable>>shift_amount <= iob_max(1,13>>shift_amount));

    //RESPONSE SWITCH

    assign internal_iob_rvalid = iob_rvalid_out;
    assign internal_iob_rdata = iob_rdata_out;
    assign internal_iob_ready = iob_ready_out;

    always @* begin
        iob_rdata_nxt = 32'd0;
        if(data_low_addressed_r) begin
            iob_rdata_nxt[0+:32] = data_low_rdata|32'd0;
        end

        if(data_high_addressed_r) begin
            iob_rdata_nxt[0+:32] = data_high_rdata|32'd0;
        end

        if(version_addressed_r) begin
            iob_rdata_nxt[0+:16] = 16'h0081|16'd0;
        end



        // ######  FSM  #############

        //FSM default values
        iob_ready_nxt = 1'b0;
        iob_rvalid_nxt = 1'b0;
        state_nxt = state;

        //FSM state machine
        case(state)
            WAIT_REQ: begin
                if(internal_iob_valid) begin // Wait for a valid request

                    iob_ready_nxt = 1'b1;

                    // If is read and ready, go to WAIT_RVALID
                    if (iob_ready_nxt && (!write_en)) begin
                        state_nxt = WAIT_RVALID;
                    end
                end
            end

            default: begin  // WAIT_RVALID

                if (iob_rvalid_out) begin // Transfer done
                    state_nxt = WAIT_REQ;
                end else begin
                    iob_rvalid_nxt = 1'b1;

                end
            end
        endcase

    end //always @*



        // store iob addr
        iob_reg_cae #(
        .DATA_W(ADDR_W),
        .RST_VAL({ADDR_W{1'b0}})
    ) internal_addr_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        .en_i(internal_iob_addr_reg_en),
        // data_i port: Data input
        .data_i(internal_iob_addr),
        // data_o port: Data output
        .data_o(internal_iob_addr_reg)
        );

            // state register
        iob_reg_ca #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) state_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // data_i port: Data input
        .data_i(state_nxt),
        // data_o port: Data output
        .data_o(state)
        );

            // Convert CSR interface into internal IOb port
        iob_universal_converter_iob_iob #(
        .ADDR_W(ADDR_W),
        .DATA_W(DATA_W)
    ) iob_universal_converter (
            // s_s port: Subordinate port
        .iob_valid_i(iob_valid_i),
        .iob_addr_i(iob_addr_i),
        .iob_wdata_i(iob_wdata_i),
        .iob_wstrb_i(iob_wstrb_i),
        .iob_rvalid_o(iob_rvalid_o),
        .iob_rdata_o(iob_rdata_o),
        .iob_ready_o(iob_ready_o),
        // m_m port: Manager port
        .iob_valid_o(internal_iob_valid),
        .iob_addr_o(internal_iob_addr),
        .iob_wdata_o(internal_iob_wdata),
        .iob_wstrb_o(internal_iob_wstrb),
        .iob_rvalid_i(internal_iob_rvalid),
        .iob_rdata_i(internal_iob_rdata),
        .iob_ready_i(internal_iob_ready)
        );

            // rvalid register
        iob_reg_ca #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) rvalid_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // data_i port: Data input
        .data_i(iob_rvalid_nxt),
        // data_o port: Data output
        .data_o(iob_rvalid_out)
        );

            // rdata register
        iob_reg_ca #(
        .DATA_W(32),
        .RST_VAL(32'b0)
    ) rdata_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // data_i port: Data input
        .data_i(iob_rdata_nxt),
        // data_o port: Data output
        .data_o(iob_rdata_out)
        );

            // ready register
        iob_reg_ca #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) ready_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // data_i port: Data input
        .data_i(iob_ready_nxt),
        // data_o port: Data output
        .data_o(iob_ready_out)
        );

    
endmodule
