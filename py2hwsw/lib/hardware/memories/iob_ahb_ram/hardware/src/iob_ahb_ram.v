// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

/*
 * AHB RAM
 */
module iob_ahb_ram #(
   // Width of address bus in bits
   parameter ADDR_WIDTH   = 32,
   // Width of input (slave/master) AXIS/AHB interface data bus in bits
   parameter DATA_WIDTH   = 32
) (
   `include "iob_ahb_ram_io.vs"
   // // ahb_m
   // input  [  ADDR_WIDTH-1:0] m_ahb_addr_i,
   // input  [           2-1:0] m_ahb_burst_i,
   // input                     m_ahb_mastlock_i,
   // input  [           3-1:0] m_ahb_prot_i,
   // input  [           3-1:0] m_ahb_size_i,
   // input  [           2-1:0] m_ahb_trans_i,
   // input  [  DATA_WIDTH-1:0] m_ahb_wdata_i,
   // input  [DATA_WIDTH/8-1:0] m_ahb_wstrb_i,
   // input                     m_ahb_write_i,
   // output [  DATA_WIDTH-1:0] m_ahb_rdata_o,
   // output                    m_ahb_readyout_o,
   // output                    m_ahb_resp_o,
   // input                     m_ahb_sel_i
);

    // TODO instantiate AHB2BRAM module
    // - connections:
    //  - clk?
    //  - reset?
    //  - HREADY?
    // - set some outputs:
    //  - m_ahb_resp_o
    AHB2MEM #(
        .MEMWIDTH(ADDR_WIDTH)
    ) ahb2bram_inst (
        // Slave Select Signals
        .HSEL(m_ahb_sel_i),
        // Global Signals
        .HCLK(),
        .HRESETn(),
        // Address, Control & Write Data
        .HREADY(),
        .HADDR(m_ahb_addr_i),
        .HTRANS(m_ahb_trans_i),
        .HWRITE(m_ahb_write_i),
        .HSIZE(m_ahb_size_i),
        .HWDATA(m_ahb_wdata_i),
        // Transfer Response & Read Data
        .HREADYOUT(m_ahb_readyout_o),
        .HRDATA(m_ahb_rdata_o)
    );

endmodule
