# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys

# set path for imports
sys.path.append("../../../../scripts")
from iob_globals import iob_globals


def setup(py_params_dict):
    reset_polarity = getattr(iob_globals(reset_polarity="negative"), "reset_polarity")
    rst_wire = "arst_n_i" if reset_polarity == "negative" else "~arst_i"
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "ADDR_WIDTH",
                "descr": "",
                "type": "P",
                "val": "14",
                "min": "1",
                "max": "32",
            },
            {
                "name": "DATA_WIDTH",
                "descr": "",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "wires": {
                    "type": "iob_clk",
                    "params": "a",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "ahb_s",
                "descr": "Subordinate AHB interface",
                "wires": {
                    "type": "ahb",
                    "prefix": "s_",
                    "ADDR_W": "ADDR_WIDTH",
                    "DATA_W": "DATA_WIDTH",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
   AHB2MEM #(
      .MEMWIDTH(ADDR_WIDTH)
   ) ahb2bram_inst (
      // Subordinate Select Signals
      .HSEL     (s_ahb_sel_i),
      // Global Signals
      .HCLK     (clk_i),
      .HRESETn  ({rst_wire}),
      // Address, Control & Write Data
      .HREADY   (1'b1),
      .HADDR    (s_ahb_addr_i),
      .HTRANS   (s_ahb_trans_i),
      .HWRITE   (s_ahb_write_i),
      .HSIZE    (s_ahb_size_i),
      .HWDATA   (s_ahb_wdata_i),
      // Transfer Response & Read Data
      .HREADYOUT(s_ahb_readyout_o),
      .HRDATA   (s_ahb_rdata_o)
   );

    // Transfer Response always okay
    assign s_ahb_resp_o = 1'b0;

""",
            },
        ],
    }

    return attributes_dict
