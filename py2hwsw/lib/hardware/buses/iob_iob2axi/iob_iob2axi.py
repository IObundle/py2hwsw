# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LOCK_W",
                "descr": "",
                "type": "P",
                "val": "2",
                "min": "1",
                "max": "32",
            },
            {
                "name": "ADDR_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
            {
                "name": "DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {"type": "iob_clk"},
            },
            {
                "name": "iob_s",
                "descr": "Subordinate IOb interface",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "axi_m",
                "descr": "Manager AXI interface",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "LEN_W": "AXI_LEN_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LOCK_W": "AXI_LOCK_W",
                },
            },
        ],
        "wires": [
            {
                "name": "axil",
                "descr": "Internal AXI Lite interface",
                "signals": {
                    "type": "axil",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_iob2axil",
                "instance_name": "iob2axil_inst",
                "instance_description": "Convert IOb instruction bus to AXI Lite",
                "parameters": {
                    "AXIL_ADDR_W": "AXI_ADDR_W",
                    "AXIL_DATA_W": "AXI_DATA_W",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_s": "iob_s",
                    "axil_m": "axil",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   //
   // AXI-Lite Write
   //
   // AW Channel
   assign axi_awaddr_o = axil_awaddr;
   // assign axi_awprot_o = axil_awprot;
   assign axi_awvalid_o = axil_awvalid;
   assign axil_awready = axi_awready_i;
   // W Channel
   assign axi_wdata_o = axil_wdata;
   assign axi_wstrb_o = axil_wstrb;
   assign axi_wvalid_o = axil_wvalid;
   assign axil_wready = axi_wready_i;
   // B Channel
   assign axil_bresp = axi_bresp_i;
   assign axil_bvalid = axi_bvalid_i;
   assign axi_bready_o = axil_bready;
   //
   // AXI specific write
   //
   // AW Channel
   assign axi_awid_o = 'b0;
   assign axi_awlen_o = 'b0;
   assign axi_awsize_o = 'd2;
   assign axi_awburst_o = 'b0;
   assign axi_awlock_o = 'b0;
   assign axi_awcache_o = 'b0;
   assign axi_awqos_o = 'b0;
   // W Channel
   assign axi_wlast_o = 'b1;
   // B Channel
   // assign  = axi_bid_i;

   //
   // AXI-Lite Read
   //
   // AR Channel
   assign axi_araddr_o = axil_araddr;
   // assign axi_arprot_o = axil_arprot;
   assign axi_arvalid_o = axil_arvalid;
   assign axil_arready = axi_arready_i;
   // R Channel
   assign axil_rdata = axi_rdata_i;
   assign axil_rresp = axi_rresp_i;
   assign axil_rvalid = axi_rvalid_i;
   assign axi_rready_o = axil_rready;
   //
   // AXI specific read
   //
   // AR Channel
   assign axi_arid_o = 'b0;
   assign axi_arlen_o = 'b0;
   assign axi_arsize_o = 'd2;
   assign axi_arburst_o = 'b0;
   assign axi_arlock_o = 'b0;
   assign axi_arcache_o = 'b0;
   assign axi_arqos_o = 'b0;
   // R Channel
   // assign  = axi_rid_i;
   // assign  = axi_rlast_i;
"""
            }
        ],
    }

    return attributes_dict
