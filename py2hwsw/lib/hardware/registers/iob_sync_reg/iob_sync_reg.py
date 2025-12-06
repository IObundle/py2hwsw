# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys

sys.path.append("../../../scripts")
from iob_globals import iob_globals


def setup(py_params_dict):

    clk_port_params = "a"

    reset_polarity = getattr(iob_globals(), "reset_polarity", "positive")

    if reset_polarity != "positive":
        clk_port_params = "an"
        reg_snippet = """
         always @(posedge clk_i, negedge arst_i) begin
            if (~arst_i) begin
               iob_sync_reg_data_o <= RST_VAL;
            end else begin
               iob_sync_reg_data_o <= iob_sync_reg_data_i;
            end
         end
         """
    else:
        reg_snippet = """
         always @(posedge clk_i, posedge arst_i) begin
            if (arst_i) begin
               iob_sync_reg_data_o <= RST_VAL;
            end else begin
               iob_sync_reg_data_o <= iob_sync_reg_data_i;
            end
         end
      """

    reg_name = f"iob_sync_reg_{clk_port_params}"

    attributes_dict = {
        "name": reg_name,
        "generate_hw": True,
        "description": "Generated sync register module. Module used for CDC circuits.",
        "version": "0.1",
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "RST_VAL",
                "type": "P",
                "val": "{DATA_W{1'b0}}",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": clk_port_params,
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "data_i",
                "descr": "Data input",
                "signals": [
                    {
                        "name": "iob_sync_reg_data_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Data output",
                "signals": [
                    {
                        "name": "iob_sync_reg_data_o",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": reg_snippet,
            },
        ],
    }

    return attributes_dict
