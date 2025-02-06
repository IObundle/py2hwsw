#!/usr/bin/env python

# SPDX-FileCopyrightText: 2018 Alex Forencich
# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

"""
Generates an AXI crossbar wrapper with the specified number of ports
"""

import argparse
from jinja2 import Template


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument(
        "-p", "--ports", type=int, default=[4], nargs="+", help="number of ports"
    )
    parser.add_argument("-n", "--name", type=str, help="module name")
    parser.add_argument("-o", "--output", type=str, help="output file name")

    args = parser.parse_args()

    try:
        generate(**args.__dict__)
    except IOError as ex:
        print(ex)
        exit(1)


def generate(ports=4, name=None, output=None):
    if type(ports) is int:
        m = n = ports
    elif len(ports) == 1:
        m = n = ports[0]
    else:
        m, n = ports

    if name is None:
        name = "axi_crossbar_wrap_{0}x{1}".format(m, n)

    if output is None:
        output = name + ".v"

    print("Generating {0}x{1} port AXI crossbar wrapper {2}...".format(m, n, name))

    cm = (m - 1).bit_length()
    cn = (n - 1).bit_length()

    t = Template(
        """\
// SPDX-FileCopyrightText: 2018 Alex Forencich
// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

// Language: Verilog 2001

`resetall
//
`timescale 1ns / 1ps
//
`default_nettype none

/*
 * AXI4 {{m}}x{{n}} crossbar (wrapper)
 */
module {{name}} #
(
    // Width of data bus in bits
    parameter DATA_WIDTH = 32,
    // Width of address bus in bits
    parameter ADDR_WIDTH = 32,
    // Width of wstrb (width of data bus in words)
    parameter STRB_WIDTH = (DATA_WIDTH/8),
    // Input ID field width (from AXI masters)
    parameter S_ID_WIDTH = 8,
    // Output ID field width (towards AXI slaves)
    // Additional bits required for response routing
    parameter M_ID_WIDTH = S_ID_WIDTH+$clog2(S_COUNT),
    // Propagate awuser signal
    parameter AWUSER_ENABLE = 0,
    // Width of awuser signal
    parameter AWUSER_WIDTH = 1,
    // Propagate wuser signal
    parameter WUSER_ENABLE = 0,
    // Width of wuser signal
    parameter WUSER_WIDTH = 1,
    // Propagate buser signal
    parameter BUSER_ENABLE = 0,
    // Width of buser signal
    parameter BUSER_WIDTH = 1,
    // Propagate aruser signal
    parameter ARUSER_ENABLE = 0,
    // Width of aruser signal
    parameter ARUSER_WIDTH = 1,
    // Propagate ruser signal
    parameter RUSER_ENABLE = 0,
    // Width of ruser signal
    parameter RUSER_WIDTH = 1,
{%- for p in range(m) %}
    // Number of concurrent unique IDs
    parameter S{{'%02d'%p}}_THREADS = 2,
    // Number of concurrent operations
    parameter S{{'%02d'%p}}_ACCEPT = 16,
{%- endfor %}
    // Number of regions per master interface
    parameter M_REGIONS = 1,
{%- for p in range(n) %}
    // Master interface base addresses
    // M_REGIONS concatenated fields of ADDR_WIDTH bits
    parameter M{{'%02d'%p}}_BASE_ADDR = 0,
    // Master interface address widths
    // M_REGIONS concatenated fields of 32 bits
    parameter M{{'%02d'%p}}_ADDR_WIDTH = {M_REGIONS{32'd24}},
    // Read connections between interfaces
    // S_COUNT bits
    parameter M{{'%02d'%p}}_CONNECT_READ = {{m}}'b{% for p in range(m) %}1{% endfor %},
    // Write connections between interfaces
    // S_COUNT bits
    parameter M{{'%02d'%p}}_CONNECT_WRITE = {{m}}'b{% for p in range(m) %}1{% endfor %},
    // Number of concurrent operations for each master interface
    parameter M{{'%02d'%p}}_ISSUE = 4,
    // Secure master (fail operations based on awprot/arprot)
    parameter M{{'%02d'%p}}_SECURE = 0,
{%- endfor %}
{%- for p in range(m) %}
    // Slave interface AW channel register type (input)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter S{{'%02d'%p}}_AW_REG_TYPE = 0,
    // Slave interface W channel register type (input)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter S{{'%02d'%p}}_W_REG_TYPE = 0,
    // Slave interface B channel register type (output)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter S{{'%02d'%p}}_B_REG_TYPE = 1,
    // Slave interface AR channel register type (input)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter S{{'%02d'%p}}_AR_REG_TYPE = 0,
    // Slave interface R channel register type (output)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter S{{'%02d'%p}}_R_REG_TYPE = 2,
{%- endfor %}
{%- for p in range(n) %}
    // Master interface AW channel register type (output)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter M{{'%02d'%p}}_AW_REG_TYPE = 1,
    // Master interface W channel register type (output)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter M{{'%02d'%p}}_W_REG_TYPE = 2,
    // Master interface B channel register type (input)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter M{{'%02d'%p}}_B_REG_TYPE = 0,
    // Master interface AR channel register type (output)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter M{{'%02d'%p}}_AR_REG_TYPE = 1,
    // Master interface R channel register type (input)
    // 0 to bypass, 1 for simple buffer, 2 for skid buffer
    parameter M{{'%02d'%p}}_R_REG_TYPE = 0{% if not loop.last %},{% endif %}
{%- endfor %}
)
(
    input  wire                     clk_i,
    input  wire                     rst_i,

    /*
     * AXI slave interface
     */
{%- for p in range(m) %}
    input  wire [S_ID_WIDTH-1:0]    s{{'%02d'%p}}_axi_awid_i,
    input  wire [ADDR_WIDTH-1:0]    s{{'%02d'%p}}_axi_awaddr_i,
    input  wire [7:0]               s{{'%02d'%p}}_axi_awlen_i,
    input  wire [2:0]               s{{'%02d'%p}}_axi_awsize_i,
    input  wire [1:0]               s{{'%02d'%p}}_axi_awburst_i,
    input  wire                     s{{'%02d'%p}}_axi_awlock_i,
    input  wire [3:0]               s{{'%02d'%p}}_axi_awcache_i,
    input  wire [2:0]               s{{'%02d'%p}}_axi_awprot_i,
    input  wire [3:0]               s{{'%02d'%p}}_axi_awqos_i,
    input  wire [AWUSER_WIDTH-1:0]  s{{'%02d'%p}}_axi_awuser_i,
    input  wire                     s{{'%02d'%p}}_axi_awvalid_i,
    output wire                     s{{'%02d'%p}}_axi_awready_o,
    input  wire [DATA_WIDTH-1:0]    s{{'%02d'%p}}_axi_wdata_i,
    input  wire [STRB_WIDTH-1:0]    s{{'%02d'%p}}_axi_wstrb_i,
    input  wire                     s{{'%02d'%p}}_axi_wlast_i,
    input  wire [WUSER_WIDTH-1:0]   s{{'%02d'%p}}_axi_wuser_i,
    input  wire                     s{{'%02d'%p}}_axi_wvalid_i,
    output wire                     s{{'%02d'%p}}_axi_wready_o,
    output wire [S_ID_WIDTH-1:0]    s{{'%02d'%p}}_axi_bid_o,
    output wire [1:0]               s{{'%02d'%p}}_axi_bresp_o,
    output wire [BUSER_WIDTH-1:0]   s{{'%02d'%p}}_axi_buser_o,
    output wire                     s{{'%02d'%p}}_axi_bvalid_o,
    input  wire                     s{{'%02d'%p}}_axi_bready_i,
    input  wire [S_ID_WIDTH-1:0]    s{{'%02d'%p}}_axi_arid_i,
    input  wire [ADDR_WIDTH-1:0]    s{{'%02d'%p}}_axi_araddr_i,
    input  wire [7:0]               s{{'%02d'%p}}_axi_arlen_i,
    input  wire [2:0]               s{{'%02d'%p}}_axi_arsize_i,
    input  wire [1:0]               s{{'%02d'%p}}_axi_arburst_i,
    input  wire                     s{{'%02d'%p}}_axi_arlock_i,
    input  wire [3:0]               s{{'%02d'%p}}_axi_arcache_i,
    input  wire [2:0]               s{{'%02d'%p}}_axi_arprot_i,
    input  wire [3:0]               s{{'%02d'%p}}_axi_arqos_i,
    input  wire [ARUSER_WIDTH-1:0]  s{{'%02d'%p}}_axi_aruser_i,
    input  wire                     s{{'%02d'%p}}_axi_arvalid_i,
    output wire                     s{{'%02d'%p}}_axi_arready_o,
    output wire [S_ID_WIDTH-1:0]    s{{'%02d'%p}}_axi_rid_o,
    output wire [DATA_WIDTH-1:0]    s{{'%02d'%p}}_axi_rdata_o,
    output wire [1:0]               s{{'%02d'%p}}_axi_rresp_o,
    output wire                     s{{'%02d'%p}}_axi_rlast_o,
    output wire [RUSER_WIDTH-1:0]   s{{'%02d'%p}}_axi_ruser_o,
    output wire                     s{{'%02d'%p}}_axi_rvalid_o,
    input  wire                     s{{'%02d'%p}}_axi_rready_i,
{% endfor %}
    /*
     * AXI master interface
     */
{%- for p in range(n) %}
    output wire [M_ID_WIDTH-1:0]    m{{'%02d'%p}}_axi_awid_o,
    output wire [ADDR_WIDTH-1:0]    m{{'%02d'%p}}_axi_awaddr_o,
    output wire [7:0]               m{{'%02d'%p}}_axi_awlen_o,
    output wire [2:0]               m{{'%02d'%p}}_axi_awsize_o,
    output wire [1:0]               m{{'%02d'%p}}_axi_awburst_o,
    output wire                     m{{'%02d'%p}}_axi_awlock_o,
    output wire [3:0]               m{{'%02d'%p}}_axi_awcache_o,
    output wire [2:0]               m{{'%02d'%p}}_axi_awprot_o,
    output wire [3:0]               m{{'%02d'%p}}_axi_awqos_o,
    output wire [3:0]               m{{'%02d'%p}}_axi_awregion_o,
    output wire [AWUSER_WIDTH-1:0]  m{{'%02d'%p}}_axi_awuser_o,
    output wire                     m{{'%02d'%p}}_axi_awvalid_o,
    input  wire                     m{{'%02d'%p}}_axi_awready_i,
    output wire [DATA_WIDTH-1:0]    m{{'%02d'%p}}_axi_wdata_o,
    output wire [STRB_WIDTH-1:0]    m{{'%02d'%p}}_axi_wstrb_o,
    output wire                     m{{'%02d'%p}}_axi_wlast_o,
    output wire [WUSER_WIDTH-1:0]   m{{'%02d'%p}}_axi_wuser_o,
    output wire                     m{{'%02d'%p}}_axi_wvalid_o,
    input  wire                     m{{'%02d'%p}}_axi_wready_i,
    input  wire [M_ID_WIDTH-1:0]    m{{'%02d'%p}}_axi_bid_i,
    input  wire [1:0]               m{{'%02d'%p}}_axi_bresp_i,
    input  wire [BUSER_WIDTH-1:0]   m{{'%02d'%p}}_axi_buser_i,
    input  wire                     m{{'%02d'%p}}_axi_bvalid_i,
    output wire                     m{{'%02d'%p}}_axi_bready_o,
    output wire [M_ID_WIDTH-1:0]    m{{'%02d'%p}}_axi_arid_o,
    output wire [ADDR_WIDTH-1:0]    m{{'%02d'%p}}_axi_araddr_o,
    output wire [7:0]               m{{'%02d'%p}}_axi_arlen_o,
    output wire [2:0]               m{{'%02d'%p}}_axi_arsize_o,
    output wire [1:0]               m{{'%02d'%p}}_axi_arburst_o,
    output wire                     m{{'%02d'%p}}_axi_arlock_o,
    output wire [3:0]               m{{'%02d'%p}}_axi_arcache_o,
    output wire [2:0]               m{{'%02d'%p}}_axi_arprot_o,
    output wire [3:0]               m{{'%02d'%p}}_axi_arqos_o,
    output wire [3:0]               m{{'%02d'%p}}_axi_arregion_o,
    output wire [ARUSER_WIDTH-1:0]  m{{'%02d'%p}}_axi_aruser_o,
    output wire                     m{{'%02d'%p}}_axi_arvalid_o,
    input  wire                     m{{'%02d'%p}}_axi_arready_i,
    input  wire [M_ID_WIDTH-1:0]    m{{'%02d'%p}}_axi_rid_i,
    input  wire [DATA_WIDTH-1:0]    m{{'%02d'%p}}_axi_rdata_i,
    input  wire [1:0]               m{{'%02d'%p}}_axi_rresp_i,
    input  wire                     m{{'%02d'%p}}_axi_rlast_i,
    input  wire [RUSER_WIDTH-1:0]   m{{'%02d'%p}}_axi_ruser_i,
    input  wire                     m{{'%02d'%p}}_axi_rvalid_i,
    output wire                     m{{'%02d'%p}}_axi_rready_o{% if not loop.last %},{% endif %}
{% endfor -%}
);

localparam S_COUNT = {{m}};
localparam M_COUNT = {{n}};

// parameter sizing helpers
function [ADDR_WIDTH*M_REGIONS-1:0] w_a_r(input [ADDR_WIDTH*M_REGIONS-1:0] val);
    w_a_r = val;
endfunction

function [32*M_REGIONS-1:0] w_32_r(input [32*M_REGIONS-1:0] val);
    w_32_r = val;
endfunction

function [S_COUNT-1:0] w_s(input [S_COUNT-1:0] val);
    w_s = val;
endfunction

function [31:0] w_32(input [31:0] val);
    w_32 = val;
endfunction

function [1:0] w_2(input [1:0] val);
    w_2 = val;
endfunction

function w_1(input val);
    w_1 = val;
endfunction

{{name}}_core #(
    .S_COUNT(S_COUNT),
    .M_COUNT(M_COUNT),
    .DATA_WIDTH(DATA_WIDTH),
    .ADDR_WIDTH(ADDR_WIDTH),
    .STRB_WIDTH(STRB_WIDTH),
    .S_ID_WIDTH(S_ID_WIDTH),
    .M_ID_WIDTH(M_ID_WIDTH),
    .AWUSER_ENABLE(AWUSER_ENABLE),
    .AWUSER_WIDTH(AWUSER_WIDTH),
    .WUSER_ENABLE(WUSER_ENABLE),
    .WUSER_WIDTH(WUSER_WIDTH),
    .BUSER_ENABLE(BUSER_ENABLE),
    .BUSER_WIDTH(BUSER_WIDTH),
    .ARUSER_ENABLE(ARUSER_ENABLE),
    .ARUSER_WIDTH(ARUSER_WIDTH),
    .RUSER_ENABLE(RUSER_ENABLE),
    .RUSER_WIDTH(RUSER_WIDTH),
    .S_THREADS({ {% for p in range(m-1,-1,-1) %}w_32(S{{'%02d'%p}}_THREADS){% if not loop.last %}, {% endif %}{% endfor %} }),
    .S_ACCEPT({ {% for p in range(m-1,-1,-1) %}w_32(S{{'%02d'%p}}_ACCEPT){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_REGIONS(M_REGIONS),
    .M_BASE_ADDR({ {% for p in range(n-1,-1,-1) %}w_a_r(M{{'%02d'%p}}_BASE_ADDR){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_ADDR_WIDTH({ {% for p in range(n-1,-1,-1) %}w_32_r(M{{'%02d'%p}}_ADDR_WIDTH){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_CONNECT_READ({ {% for p in range(n-1,-1,-1) %}w_s(M{{'%02d'%p}}_CONNECT_READ){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_CONNECT_WRITE({ {% for p in range(n-1,-1,-1) %}w_s(M{{'%02d'%p}}_CONNECT_WRITE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_ISSUE({ {% for p in range(n-1,-1,-1) %}w_32(M{{'%02d'%p}}_ISSUE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_SECURE({ {% for p in range(n-1,-1,-1) %}w_1(M{{'%02d'%p}}_SECURE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .S_AR_REG_TYPE({ {% for p in range(m-1,-1,-1) %}w_2(S{{'%02d'%p}}_AR_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .S_R_REG_TYPE({ {% for p in range(m-1,-1,-1) %}w_2(S{{'%02d'%p}}_R_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .S_AW_REG_TYPE({ {% for p in range(m-1,-1,-1) %}w_2(S{{'%02d'%p}}_AW_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .S_W_REG_TYPE({ {% for p in range(m-1,-1,-1) %}w_2(S{{'%02d'%p}}_W_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .S_B_REG_TYPE({ {% for p in range(m-1,-1,-1) %}w_2(S{{'%02d'%p}}_B_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_AR_REG_TYPE({ {% for p in range(n-1,-1,-1) %}w_2(M{{'%02d'%p}}_AR_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_R_REG_TYPE({ {% for p in range(n-1,-1,-1) %}w_2(M{{'%02d'%p}}_R_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_AW_REG_TYPE({ {% for p in range(n-1,-1,-1) %}w_2(M{{'%02d'%p}}_AW_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_W_REG_TYPE({ {% for p in range(n-1,-1,-1) %}w_2(M{{'%02d'%p}}_W_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} }),
    .M_B_REG_TYPE({ {% for p in range(n-1,-1,-1) %}w_2(M{{'%02d'%p}}_B_REG_TYPE){% if not loop.last %}, {% endif %}{% endfor %} })
)
axi_crossbar_inst (
    .clk(clk_i),
    .rst(rst_i),
    .s_axi_awid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awaddr({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awaddr_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awlen({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awlen_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awsize({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awsize_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awburst({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awburst_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awlock({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awlock_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awcache({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awcache_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awprot({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awprot_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awqos({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awqos_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awuser({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awuser_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awvalid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awvalid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_awready({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_awready_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_wdata({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_wdata_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_wstrb({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_wstrb_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_wlast({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_wlast_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_wuser({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_wuser_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_wvalid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_wvalid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_wready({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_wready_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_bid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_bid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_bresp({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_bresp_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_buser({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_buser_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_bvalid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_bvalid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_bready({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_bready_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_araddr({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_araddr_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arlen({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arlen_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arsize({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arsize_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arburst({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arburst_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arlock({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arlock_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arcache({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arcache_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arprot({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arprot_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arqos({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arqos_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_aruser({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_aruser_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arvalid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arvalid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_arready({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_arready_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_rid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_rid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_rdata({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_rdata_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_rresp({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_rresp_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_rlast({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_rlast_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_ruser({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_ruser_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_rvalid({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_rvalid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .s_axi_rready({ {% for p in range(m-1,-1,-1) %}s{{'%02d'%p}}_axi_rready_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awaddr({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awaddr_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awlen({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awlen_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awsize({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awsize_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awburst({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awburst_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awlock({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awlock_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awcache({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awcache_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awprot({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awprot_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awqos({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awqos_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awregion({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awregion_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awuser({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awuser_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awvalid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awvalid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_awready({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_awready_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_wdata({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_wdata_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_wstrb({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_wstrb_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_wlast({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_wlast_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_wuser({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_wuser_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_wvalid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_wvalid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_wready({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_wready_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_bid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_bid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_bresp({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_bresp_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_buser({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_buser_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_bvalid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_bvalid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_bready({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_bready_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_araddr({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_araddr_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arlen({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arlen_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arsize({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arsize_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arburst({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arburst_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arlock({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arlock_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arcache({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arcache_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arprot({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arprot_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arqos({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arqos_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arregion({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arregion_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_aruser({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_aruser_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arvalid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arvalid_o{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_arready({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_arready_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_rid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_rid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_rdata({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_rdata_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_rresp({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_rresp_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_rlast({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_rlast_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_ruser({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_ruser_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_rvalid({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_rvalid_i{% if not loop.last %}, {% endif %}{% endfor %} }),
    .m_axi_rready({ {% for p in range(n-1,-1,-1) %}m{{'%02d'%p}}_axi_rready_o{% if not loop.last %}, {% endif %}{% endfor %} })
);

endmodule

`resetall

"""
    )

    print(f"Writing file '{output}'...")

    with open(output, "w") as f:
        f.write(t.render(m=m, n=n, cm=cm, cn=cn, name=name))
        f.flush()

    print("Done")


if __name__ == "__main__":
    main()
