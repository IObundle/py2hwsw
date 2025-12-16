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
                "val": 21,
                "min": 1,
                "max": 32,
                "descr": "APB address bus width in bits",
            },
            {
                "name": "APB_DATA_W",
                "type": "P",
                "val": 21,
                "min": 1,
                "max": 32,
                "descr": "APB data bus width in bits",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": 21,
                "min": 1,
                "max": 32,
                "descr": "IOb address bus width in bits",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": 21,
                "min": 1,
                "max": 32,
                "descr": "IOb data bus width in bits",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "apb_s",
                "signals": {
                    "type": "apb",
                    "ADDR_W": "APB_ADDR_W",
                    "DATA_W": "APB_DATA_W",
                },
                "descr": "APB interface",
            },
            {
                "name": "iob_m",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "CPU native interface",
            },
        ],
        "wires": [
            {
                "name": "iob_valid",
                "descr": "IOb valid signal",
                "signals": [
                    {
                        "name": "iob_valid",
                        "isvar": True,
                        "width": "1",
                        "descr": "IOb valid signal",
                    },
                ],
            },
            {
                "name": "nxt_apb_ready",
                "descr": "Next APB ready signal",
                "signals": [
                    {
                        "name": "nxt_apb_ready",
                        "isvar": True,
                        "width": "1",
                        "descr": "Next APB ready signal",
                    },
                ],
            },
            {
                "name": "pc_cnt",
                "descr": "PC counter",
                "signals": [
                    {
                        "name": "pc_cnt",
                        "width": "2",
                        "descr": "PC counter",
                    },
                ],
            },
            {
                "name": "pc_cnt_nxt",
                "descr": "Next PC counter",
                "signals": [
                    {
                        "name": "pc_cnt_nxt",
                        "isvar": True,
                        "width": "2",
                        "descr": "Next PC counter",
                    },
                ],
            },
            {
                "name": "apb_ready",
                "descr": "APB ready output signal",
                "signals": [
                    {
                        "name": "apb_ready_o",
                    },
                ],
            },
            {
                "name": "iob_rvalid",
                "descr": "IOb read valid",
                "signals": [
                    {
                        "name": "iob_rvalid_i",
                    },
                ],
            },
            {
                "name": "iob_rdata",
                "descr": "IOb read data",
                "signals": [
                    {
                        "name": "iob_rdata_i",
                    },
                ],
            },
            {
                "name": "apb_rdata",
                "descr": "APB read data",
                "signals": [
                    {
                        "name": "apb_rdata_o",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "pc_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a",
                },
                "parameters": {
                    "DATA_W": "2",
                    "RST_VAL": "2'd0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "pc_cnt_nxt",
                    "data_o": "pc_cnt",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "apb_ready_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a",
                },
                "parameters": {
                    "DATA_W": "1",
                    "RST_VAL": "1'd0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "nxt_apb_ready",
                    "data_o": "apb_ready",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "apb_rdata_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_e",
                },
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "{DATA_W{1'd0}}",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i: iob_rvalid_i",
                        ],
                    ),
                    "data_i": "iob_rdata",
                    "data_o": "apb_rdata",
                },
            },
        ],
        "comb": {
            "code": """
                iob_valid_o  = iob_valid;
                iob_addr_o   = apb_addr_i;
                iob_wdata_o  = apb_wdata_i;
                iob_wstrb_o  = apb_write_i ? apb_wstrb_i : {WSTRB_W{1'b0}};
                 pc_cnt_nxt     = pc_cnt + 1'b1;
      iob_valid      = 1'b0;
        nxt_apb_ready  = 1'b0;

      case (pc_cnt)
         WAIT_ENABLE: begin
            if (!(apb_sel_i & apb_enable_i)) begin
               pc_cnt_nxt = pc_cnt;
            end else begin
               iob_valid = 1'b1;
            end
         end
         WAIT_READY: begin
            iob_valid = 1'b1;
            if (!iob_ready_i) begin
               pc_cnt_nxt = pc_cnt;
            end else begin
               if (apb_write_i) begin
                  pc_cnt_nxt    = WAIT_APB_READY;
                    nxt_apb_ready = 1'b1;
               end
            end
         end
         RVALID: begin
            nxt_apb_ready  = iob_rvalid_i;
            if (!iob_rvalid_i) begin
               pc_cnt_nxt = pc_cnt;
            end
         end
         default: begin  // WAIT_APB_READY
            pc_cnt_nxt = WAIT_ENABLE;
         end
      endcase
            """,
        },
        "snippets": [
            {
                "verilog_code": r"""
   localparam WSTRB_W = DATA_W / 8;
   localparam WAIT_ENABLE = 2'd0;
   localparam WAIT_READY = 2'd1;
   localparam RVALID = 2'd2;
   localparam WAIT_APB_READY = 2'd3;


                """
            }
        ],
    }

    return attributes_dict
