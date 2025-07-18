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
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "iob_s",
                "wires": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "CPU native interface",
            },
            {
                "name": "apb_m",
                "wires": {
                    "type": "apb",
                    "ADDR_W": "APB_ADDR_W",
                    "DATA_W": "APB_DATA_W",
                },
                "descr": "APB interface",
            },
        ],
        "buses": [
            {
                "name": "pc_int",
                "descr": "pc_int bus",
                "wires": [
                    {"name": "pc_int", "width": 1},
                ],
            },
            {
                "name": "pc_nxt_int",
                "descr": "pc_nxt_int bus",
                "wires": [
                    {"name": "pc_nxt_int", "width": 1},
                ],
            },
            {
                "name": "apb_rdata_i",
                "descr": "apb_rdata_i bus",
                "wires": [
                    {"name": "apb_rdata_i"},
                ],
            },
            {
                "name": "iob_rdata_o",
                "descr": "iob_rdata_o bus",
                "wires": [
                    {"name": "iob_rdata_o"},
                ],
            },
            {
                "name": "apb_ready_i",
                "descr": "apb_ready_i bus",
                "wires": [
                    {"name": "apb_ready_i"},
                ],
            },
            {
                "name": "iob_rvalid_nxt_int",
                "descr": "iob_rvalid_nxt_int bus",
                "wires": [
                    {"name": "iob_rvalid_nxt_int", "width": 1},
                ],
            },
            {
                "name": "iob_rvalid_o",
                "descr": "iob_rvalid_o bus",
                "wires": [
                    {"name": "iob_rvalid_o"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "pc_reg",
                "parameters": {
                    "DATA_W": 1,
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
                    "clk_en_rst_s": "c_a_e",
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
        localparam WAIT_VALID  = 1'd0;
        localparam WAIT_READY  = 1'd1;

        reg pcnt_nxt;
        reg apb_enable;
        reg iob_rvalid_nxt;

        //IOb outputs
        assign iob_ready_o = apb_ready_i;

        //APB outputs
        assign apb_sel_o    = apb_enable;
        assign apb_enable_o = apb_enable;
        assign apb_wdata_o  = iob_wdata_i;

        assign apb_addr_o   = iob_addr_i;
        assign apb_wstrb_o  = iob_wstrb_i;
        assign apb_write_o  = |iob_wstrb_i;

        assign iob_rvalid_nxt_int = iob_rvalid_nxt;
        assign pc_nxt_int = pcnt_nxt;

        always @* begin
    pcnt_nxt    = pc_int + 1'b1;
    apb_enable = 1'b0;
    iob_rvalid_nxt = 1'b0;

    case (pc_int)
      WAIT_VALID: begin
        if (!iob_valid_i) begin
          pcnt_nxt = pc_int;
        end else begin
          apb_enable = 1'b1;
        end
      end
      WAIT_READY: begin
        apb_enable = 1'b1;
        if (!apb_ready_i) begin
          pcnt_nxt = pc_int;
        end else if (apb_write_o) begin  // No need to wait for rvalid
          pcnt_nxt = WAIT_VALID;
        end else begin
           iob_rvalid_nxt = 1'd1;
        end
      end
    endcase
  end
            """,
            },
        ],
    }

    return attributes_dict
