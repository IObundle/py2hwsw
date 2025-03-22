# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "APB_ADDR_W",
                "type": "P",
                "val": "22",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "APB_DATA_W",
                "type": "P",
                "val": "22",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "APB_ADDR_W",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "APB_DATA_W",
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
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "iob_s",
                "signals": {
                    "type": "iob",
                },
                "descr": "CPU native interface",
            },
            {
                "name": "apb_m",
                "signals": {
                    "type": "apb",
                },
                "descr": "APB interface",
            },
        ],
        "wires": [
            {
                "name": "pc_int",
                "descr": "pc_int wire",
                "signals": [
                    {"name": "pc_int", "width": 2},
                ],
            },
            {
                "name": "pc_nxt_int",
                "descr": "pc_nxt_int wire",
                "signals": [
                    {"name": "pc_nxt_int", "width": 2},
                ],
            },
            {
                "name": "apb_rdata_i",
                "descr": "apb_rdata_i wire",
                "signals": [
                    {"name": "apb_rdata_i"},
                ],
            },
            {
                "name": "iob_rdata_o",
                "descr": "iob_rdata_o wire",
                "signals": [
                    {"name": "iob_rdata_o"},
                ],
            },
            {
                "name": "apb_ready_i",
                "descr": "apb_ready_i wire",
                "signals": [
                    {"name": "apb_ready_i"},
                ],
            },
            {
                "name": "iob_rvalid_nxt_int",
                "descr": "iob_rvalid_nxt_int wire",
                "signals": [
                    {"name": "iob_rvalid_nxt_int", "width": 1},
                ],
            },
            {
                "name": "iob_rvalid_o",
                "descr": "iob_rvalid_o wire",
                "signals": [
                    {"name": "iob_rvalid_o"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "pc_reg",
                "parameters": {
                    "DATA_W": 2,
                    "RST_VAL": 0,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "pc_nxt_int",
                    "data_o": "pc_int",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_rdata_reg",
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": 0,
                },
                "port_params": {
                    "clk_en_rst_s": "cke_arst_en",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i:apb_ready_i",
                        ],
                    ),
                    "data_i": "apb_rdata_i",
                    "data_o": "iob_rdata_o",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_rvalid_reg",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": 0,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "iob_rvalid_nxt_int",
                    "data_o": "iob_rvalid_o",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        reg  [1:0] pc_nxt;
        reg  [1:0] apb_enable;
        reg        iob_rvalid_nxt;
        assign iob_rvalid_nxt_int = iob_rvalid_nxt;
        always @* begin
    pc_nxt_int    = pc_int + 1'b1;
    apb_enable = 1'b0;
    iob_rvalid_nxt = 1'b0;

    case (pc_int)
      WAIT_VALID: begin
        if (!iob_valid_i) begin
          pc_nxt_int = pc_int;
        end else begin
          apb_enable = 1'b1;
        end
      end
      WAIT_READY: begin
        apb_enable = 1'b1;
        if (!apb_ready_i) begin
          pc_nxt_int = pc_int;
        end else if (apb_write_o) begin  // No need to wait for rvalid
          pc_nxt_int = WAIT_VALID;
        end else begin
           iob_rvalid_nxt = 1'd1;
        end
      end
      default: begin // WAIT_RREADY
         if (iob_rready_i) begin
            pc_nxt_int = WAIT_VALID;
         end else begin
            iob_rvalid_nxt = iob_rvalid_o;
            pc_nxt         = pc;
         end
      end
    endcase
  end
            """,
            },
        ],
    }

    return attributes_dict
