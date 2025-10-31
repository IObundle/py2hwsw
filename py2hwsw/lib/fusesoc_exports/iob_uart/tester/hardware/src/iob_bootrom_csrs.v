// SPDX-FileCopyrightText: 2025 IObundle, Lda
//
// SPDX-License-Identifier: MIT
//
// Py2HWSW Version 0.81 has generated this code (https://github.com/IObundle/py2hwsw).

`timescale 1ns / 1ps
`include "iob_bootrom_csrs_conf.vh"

module iob_bootrom_csrs #(
    parameter ADDR_W = `IOB_BOOTROM_CSRS_ADDR_W,  // Don't change this parameter value!
    parameter DATA_W = `IOB_BOOTROM_CSRS_DATA_W,  // Don't change this parameter value!
    parameter AXI_ID_W = `IOB_BOOTROM_CSRS_AXI_ID_W,
    parameter AXI_LEN_W = `IOB_BOOTROM_CSRS_AXI_LEN_W
) (
    // clk_en_rst_s: Clock, clock enable and reset
    input clk_i,
    input cke_i,
    input arst_i,
    // control_if_s: CSR control interface. Interface type defined by `csr_if` parameter.
    input [13-1:0] axi_araddr_i,
    input axi_arvalid_i,
    output axi_arready_o,
    output [DATA_W-1:0] axi_rdata_o,
    output [2-1:0] axi_rresp_o,
    output axi_rvalid_o,
    input axi_rready_i,
    input [AXI_ID_W-1:0] axi_arid_i,
    input [AXI_LEN_W-1:0] axi_arlen_i,
    input [3-1:0] axi_arsize_i,
    input [2-1:0] axi_arburst_i,
    input [2-1:0] axi_arlock_i,
    input [4-1:0] axi_arcache_i,
    input [4-1:0] axi_arqos_i,
    output [AXI_ID_W-1:0] axi_rid_o,
    output axi_rlast_o,
    input [13-1:0] axi_awaddr_i,
    input axi_awvalid_i,
    output axi_awready_o,
    input [DATA_W-1:0] axi_wdata_i,
    input [DATA_W/8-1:0] axi_wstrb_i,
    input axi_wvalid_i,
    output axi_wready_o,
    output [2-1:0] axi_bresp_o,
    output axi_bvalid_o,
    input axi_bready_i,
    input [AXI_ID_W-1:0] axi_awid_i,
    input [AXI_LEN_W-1:0] axi_awlen_i,
    input [3-1:0] axi_awsize_i,
    input [2-1:0] axi_awburst_i,
    input [2-1:0] axi_awlock_i,
    input [4-1:0] axi_awcache_i,
    input [4-1:0] axi_awqos_i,
    input axi_wlast_i,
    output [AXI_ID_W-1:0] axi_bid_o,
    // rom_bus_m: External rom ROM signals.
    output rom_clk_o,
    output [10-1:0] rom_addr_o,
    output rom_en_o,
    input [DATA_W-1:0] rom_r_data_i
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
// Register input
    wire rom_ren;
// Register output
    wire rom_rvalid;
    wire iob_rvalid_out;
    reg iob_rvalid_nxt;
    wire [32-1:0] iob_rdata_out;
    reg [32-1:0] iob_rdata_nxt;
    wire iob_ready_out;
    reg iob_ready_nxt;
// Rvalid signal of currently addressed CSR
    reg rvalid_int;
// Ready signal of currently addressed CSR
    reg ready_int;
// rom register interface
    wire rom_valid;
    wire [10+$clog2(DATA_W/8)-1:0] rom_addr;
    wire [((DATA_W > 1) ? DATA_W : 1)-1:0] rom_rdata;
    wire rom_ready;


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


   // Connect ROM to external memory signals
   assign rom_clk_o = clk_i;
   assign rom_en_o   = rom_ren;
   assign rom_addr_o = rom_addr[2+:10];
   assign rom_rdata   = rom_r_data_i;
   assign rom_ready  = 1'b1;  // ROM is always ready

   assign rom_ren = rom_valid & rom_ready;


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


//NAME: rom;
//MODE: R; WIDTH: DATA_W; RST_VAL: 0; ADDR: 0; SPACE (bytes): 4096 (max); TYPE: NOAUTO. For use with rom: rom

    wire rom_addressed;
    assign rom_addressed = (internal_iob_addr_stable >= (0)) && (internal_iob_addr_stable < 4096);
   assign rom_valid = internal_iob_valid & rom_addressed & ~write_en;
   assign rom_addr = internal_iob_addr_stable - 0;


//NAME: version;
//MODE: R; WIDTH: 16; RST_VAL: 0081; ADDR: 4096; SPACE (bytes): 2 (max); TYPE: REG. 

    wire version_addressed_r;
    assign version_addressed_r = (internal_iob_addr_stable>>shift_amount >= (4096>>shift_amount)) && (internal_iob_addr_stable>>shift_amount <= iob_max(1,4097>>shift_amount));


    wire auto_addressed;
    wire auto_addressed_r;
    reg auto_addressed_nxt;

    //RESPONSE SWITCH

    // Don't register response signals if accessing non-auto CSR
    assign internal_iob_rvalid = auto_addressed ? iob_rvalid_out : rvalid_int;
    assign internal_iob_rdata = auto_addressed ? iob_rdata_out : iob_rdata_nxt;
    assign internal_iob_ready = auto_addressed ? iob_ready_out : ready_int;

   // auto_addressed register
   assign auto_addressed = (state == WAIT_REQ) ? auto_addressed_nxt : auto_addressed_r;
   iob_reg_ca #(
      .DATA_W (1),
      .RST_VAL(1'b0)
   ) auto_addressed_reg (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      // data_i port: Data input
      .data_i(auto_addressed_nxt),
      // data_o port: Data output
      .data_o(auto_addressed_r)
   );

    always @* begin
        iob_rdata_nxt = 32'd0;

        rvalid_int = 1'b1;
        ready_int = 1'b1;
        auto_addressed_nxt = auto_addressed_r;
        if (internal_iob_valid) begin
            auto_addressed_nxt = 1'b1;
        end
        if(rom_addressed) begin

            iob_rdata_nxt[0+:32] = rom_rdata|32'd0;
            rvalid_int = rom_rvalid;
            ready_int = rom_ready;
            if (internal_iob_valid & (~|internal_iob_wstrb)) begin
                auto_addressed_nxt = 1'b0;
            end
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

                    iob_ready_nxt = ready_int;

                    // If is read and ready, go to WAIT_RVALID
                    if (iob_ready_nxt && (!write_en)) begin
                        state_nxt = WAIT_RVALID;
                    end
                end
            end

            default: begin  // WAIT_RVALID

                if (auto_addressed & iob_rvalid_out) begin // Transfer done
                    state_nxt = WAIT_REQ;
                end else if ((!auto_addressed) & rvalid_int) begin // Transfer done
                    state_nxt = WAIT_REQ;
                end else begin
                    iob_rvalid_nxt = rvalid_int;

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

            // rom rvalid register
        iob_reg_ca #(
        .DATA_W(1),
        .RST_VAL(1'b0)
    ) rom_rvalid_r (
            // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i),
        // data_i port: Data input
        .data_i(rom_ren),
        // data_o port: Data output
        .data_o(rom_rvalid)
        );

            // Convert CSR interface into internal IOb port
        iob_universal_converter_axi_iob #(
        .ADDR_W(ADDR_W),
        .DATA_W(DATA_W),
        .AXI_ID_W(AXI_ID_W),
        .AXI_LEN_W(AXI_LEN_W)
    ) iob_universal_converter (
            // s_s port: Subordinate port
        .axi_araddr_i(axi_araddr_i),
        .axi_arvalid_i(axi_arvalid_i),
        .axi_arready_o(axi_arready_o),
        .axi_rdata_o(axi_rdata_o),
        .axi_rresp_o(axi_rresp_o),
        .axi_rvalid_o(axi_rvalid_o),
        .axi_rready_i(axi_rready_i),
        .axi_arid_i(axi_arid_i),
        .axi_arlen_i(axi_arlen_i),
        .axi_arsize_i(axi_arsize_i),
        .axi_arburst_i(axi_arburst_i),
        .axi_arlock_i(axi_arlock_i),
        .axi_arcache_i(axi_arcache_i),
        .axi_arqos_i(axi_arqos_i),
        .axi_rid_o(axi_rid_o),
        .axi_rlast_o(axi_rlast_o),
        .axi_awaddr_i(axi_awaddr_i),
        .axi_awvalid_i(axi_awvalid_i),
        .axi_awready_o(axi_awready_o),
        .axi_wdata_i(axi_wdata_i),
        .axi_wstrb_i(axi_wstrb_i),
        .axi_wvalid_i(axi_wvalid_i),
        .axi_wready_o(axi_wready_o),
        .axi_bresp_o(axi_bresp_o),
        .axi_bvalid_o(axi_bvalid_o),
        .axi_bready_i(axi_bready_i),
        .axi_awid_i(axi_awid_i),
        .axi_awlen_i(axi_awlen_i),
        .axi_awsize_i(axi_awsize_i),
        .axi_awburst_i(axi_awburst_i),
        .axi_awlock_i(axi_awlock_i),
        .axi_awcache_i(axi_awcache_i),
        .axi_awqos_i(axi_awqos_i),
        .axi_wlast_i(axi_wlast_i),
        .axi_bid_o(axi_bid_o),
        // m_m port: Manager port
        .iob_valid_o(internal_iob_valid),
        .iob_addr_o(internal_iob_addr),
        .iob_wdata_o(internal_iob_wdata),
        .iob_wstrb_o(internal_iob_wstrb),
        .iob_rvalid_i(internal_iob_rvalid),
        .iob_rdata_i(internal_iob_rdata),
        .iob_ready_i(internal_iob_ready),
        // clk_en_rst_s port: Clock, clock enable and reset
        .clk_i(clk_i),
        .cke_i(cke_i),
        .arst_i(arst_i)
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
