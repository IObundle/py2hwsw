# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    """AXI to AXI-Lite converter
    This converter has the same limitations as AXI-Lite:
    - No Burst Support: burst-related signals (like AWLEN, AWSIZE, ARBURST, etc.) are ignored.
    """
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "4",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LOCK_W",
                "descr": "AXI lock width",
                "type": "P",
                "val": "2",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
            {
                "name": "axil_s",
                "descr": "AXI Lite subordinate interface to connect to external manager",
                "signals": {
                    "type": "axil",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "axi_m",
                "descr": "AXI manager interface to connect to external subordinate",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "AXI_LOCK_W",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   // Write Address Channel
   assign axi_awaddr_o = axil_awaddr_i;
   assign axi_awvalid_o = axil_awvalid_i;
   assign axil_awready_o = axi_awready_i;
   // Write Data Channel
   assign axi_wdata_o = axil_wdata_i;
   assign axi_wstrb_o = axil_wstrb_i;
   assign axi_wvalid_o = axil_wvalid_i;
   assign axil_wready_o = axi_wready_i;
   // Write Response Channel
   assign axil_bresp_o = axi_bresp_i;
   assign axil_bvalid_o = axi_bvalid_i;
   assign axi_bready_o = axil_bready_i;
   // Read Address Channel
   assign axi_araddr_o = axil_araddr_i;
   assign axi_arvalid_o = axil_arvalid_i;
   assign axil_arready_o = axi_arready_i;
   // Read Data Channel
   assign axil_rdata_o = axi_rdata_i;
   assign axil_rresp_o = axi_rresp_i;
   assign axil_rvalid_o = axi_rvalid_i;
   assign axi_rready_o = axil_rready_i;

   // Unused axi outputs
   assign axi_awid_o = 'b0;
   assign axi_awlen_o = 'b0;
   assign axi_awsize_o = 'd2; // 4 byte data transfer
   assign axi_awburst_o = 'b0;
   assign axi_awlock_o = 'b0;
   assign axi_awcache_o = 'b0;
   assign axi_awqos_o = 'b0;
   assign axi_wlast_o = 'd1; // All bursts are single transfers: always the last burst
   assign axi_arid_o = 'b0;
   assign axi_arlen_o = 'b0;
   assign axi_arsize_o = 'd2; // 4 byte data transfer
   assign axi_arburst_o = 'b0;
   assign axi_arlock_o = 'b0;
   assign axi_arcache_o = 'b0;
   assign axi_arqos_o = 'b0;

   // Unused axi inputs
   // axi_bid_i
   // axi_rid_i
   // axi_rlast_i
"""
            }
        ],
    }

    return attributes_dict
