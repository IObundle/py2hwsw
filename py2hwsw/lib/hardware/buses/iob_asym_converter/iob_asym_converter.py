# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {"name": "W_DATA_W", "type": "P", "val": 21, "min": 1, "max": "NA"},
            {"name": "R_DATA_W", "type": "P", "val": 21, "min": 1, "max": "NA"},
            {
                "name": "ADDR_W",
                "type": "P",
                "val": 3,
                "min": 1,
                "max": "NA",
                "descr": "higher ADDR_W lower DATA_W",
            },
            {
                "name": "BIG_ENDIAN",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 1,
                "descr": "0: little endian, 1: big endian",
            },
            # determine W_ADDR_W and R_ADDR_W
            {"name": "MAXDATA_W", "type": "D", "val": "iob_max(W_DATA_W, R_DATA_W)"},
            {"name": "MINDATA_W", "type": "D", "val": "iob_min(W_DATA_W, R_DATA_W)"},
            {"name": "R", "type": "D", "val": "MAXDATA_W / MINDATA_W"},
            {
                "name": "MINADDR_W",
                "type": "D",
                "val": "ADDR_W - $clog2(R)",
                "descr": "lower ADDR_W (higher DATA_W)",
            },
            {
                "name": "W_ADDR_W",
                "type": "D",
                "val": "(W_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
            },
            {
                "name": "R_ADDR_W",
                "type": "D",
                "val": "(R_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "write_i",
                "descr": "Write interface",
                "signals": [
                    {
                        "name": "w_en_i",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": "w_addr_i",
                        "width": "W_ADDR_W",
                        "descr": "Write address",
                    },
                    {
                        "name": "w_data_i",
                        "width": "W_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
            {
                "name": "read_io",
                "descr": "Read interface",
                "signals": [
                    {
                        "name": "r_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": "r_addr_i",
                        "width": "R_ADDR_W",
                        "descr": "Read address",
                    },
                    {
                        "name": "r_data_o",
                        "width": "R_DATA_W",
                        "descr": "Read data",
                    },
                ],
            },
            {
                "name": "extmem_io",
                "descr": "External memory interface",
                "signals": [
                    #  Write port
                    {
                        "name": "ext_mem_w_en_o",
                        "width": "R",
                        "descr": "Memory write enable",
                    },
                    {
                        "name": "ext_mem_w_addr_o",
                        "width": "MINADDR_W",
                        "descr": "Memory write address",
                    },
                    {
                        "name": "ext_mem_w_data_o",
                        "width": "MAXDATA_W",
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": "ext_mem_r_en_o",
                        "width": "R",
                        "descr": "Memory read enable",
                    },
                    {
                        "name": "ext_mem_r_addr_o",
                        "width": "MINADDR_W",
                        "descr": "Memory read address",
                    },
                    {
                        "name": "ext_mem_r_data_i",
                        "width": "MAXDATA_W",
                        "descr": "Memory read data",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "r_data_valid_reg",
                "descr": "Read data valid register",
                "signals": [
                    {
                        "name": "r_data_valid_reg",
                        "width": "1",
                        "descr": "Read data valid register wire",
                    },
                ],
            },
            {
                "name": "r_data_reg",
                "descr": "Read data register",
                "signals": [
                    {
                        "name": "r_data_reg",
                        "width": "MAXDATA_W",
                        "descr": "Read data register wire",
                    },
                ],
            },
            {
                "name": "r_data_int",
                "descr": "Read data internal",
                "signals": [
                    {
                        "name": "r_data_int",
                        "width": "MAXDATA_W",
                        "descr": "Read data internal wire",
                    },
                ],
            },
            {
                "name": "ext_mem_r_data",
                "descr": "Memory read data",
                "signals": [
                    {
                        "name": "ext_mem_r_data_i",
                        "width": "MAXDATA_W",
                        "descr": "Memory read data",
                    },
                ],
            },
            {
                "name": "r_en",
                "descr": "Read_enable",
                "signals": [
                    {
                        "name": "r_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "r_data_valid_reg_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
                "parameters": {
                    "DATA_W": "1",
                    "RST_VAL": "1'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "r_en",
                    "data_o": "r_data_valid_reg",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "r_data_reg_inst",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "parameters": {
                    "DATA_W": "MAXDATA_W",
                    "RST_VAL": "{MAXDATA_W{1'd0}}",
                },
                "connect": {
                    "clk_en_rst_s": ("clk_en_rst_s", ["en_i: r_data_valid_reg"]),
                    "data_i": "ext_mem_r_data",
                    "data_o": "r_data_reg",
                },
            },
            {
                "core_name": "iob_functions",
                "instantiate": False,
            },
        ],
        "comb": {
            "code": """
                if (r_data_valid_reg) begin
                    r_data_int = ext_mem_r_data_i;
                end else begin
                    r_data_int = r_data_reg;
                end
            """,
        },
        "snippets": [
            {
                "verilog_code": r"""
                 `include "iob_functions.vs"
                //Generate the RAM based on the parameters
   generate
      if (W_DATA_W > R_DATA_W) begin : g_write_wider
         //memory write port
         assign ext_mem_w_en_o   = {R{w_en_i}};
         assign ext_mem_w_addr_o = w_addr_i;
         assign ext_mem_w_data_o = w_data_i;

         //register to hold the LSBs of r_addr
         wire [$clog2(R)-1:0] r_addr_lsbs_reg;
         iob_reg_cae #(
            .DATA_W ($clog2(R)),
            .RST_VAL({$clog2(R) {1'd0}})
         ) r_addr_reg_inst (
            .clk_i (clk_i),
            .cke_i (cke_i),
            .arst_i(arst_i),
            .en_i  (r_en_i),
            .data_i(r_addr_i[$clog2(R)-1:0]),
            .data_o(r_addr_lsbs_reg)
         );

         //memory read port
         assign ext_mem_r_addr_o = r_addr_i[R_ADDR_W-1:$clog2(R)];

         wire [W_DATA_W-1:0] r_data;
         if (BIG_ENDIAN) begin : g_big_endian
            assign ext_mem_r_en_o = {{(R - 1) {1'd0}}, r_en_i} << ((R - 1) - r_addr_i[$clog2(
                R
            )-1:0]);
            assign r_data = r_data_int >> (((R - 1) - r_addr_lsbs_reg) * R_DATA_W);
         end else begin : g_little_endian
            assign ext_mem_r_en_o = {{(R - 1) {1'd0}}, r_en_i} << r_addr_i[$clog2(R)-1:0];
            assign r_data         = r_data_int >> (r_addr_lsbs_reg * R_DATA_W);
         end
         assign r_data_o = r_data[0+:R_DATA_W];

      end else if (W_DATA_W < R_DATA_W) begin : g_read_wider
         //memory write port
         assign ext_mem_w_en_o = {{(R - 1) {1'd0}}, w_en_i} << w_addr_i[$clog2(R)-1:0];
         assign ext_mem_w_data_o = {{(R_DATA_W - W_DATA_W) {1'd0}}, w_data_i} << (w_addr_i[$clog2(
             R
         )-1:0] * W_DATA_W);
         assign ext_mem_w_addr_o = w_addr_i[W_ADDR_W-1:$clog2(R)];

         //memory read port
         assign ext_mem_r_en_o = {R{r_en_i}};
         assign ext_mem_r_addr_o = r_addr_i;
         if (BIG_ENDIAN) begin : g_big_endian
            genvar data_sel;
            for (data_sel = 0; data_sel < R; data_sel = data_sel + 1) begin : gen_r_data
               assign r_data_o[data_sel * W_DATA_W +: W_DATA_W] =
                        r_data_int[((R - 1) - data_sel) * W_DATA_W +: W_DATA_W];
            end
         end else begin : g_little_endian
            assign r_data_o = r_data_int;
         end

      end else begin : g_same_width
         //W_DATA_W == R_DATA_W
         //memory write port
         assign ext_mem_w_en_o   = w_en_i;
         assign ext_mem_w_addr_o = w_addr_i;
         assign ext_mem_w_data_o = w_data_i;

         //memory read port
         assign ext_mem_r_en_o   = r_en_i;
         assign ext_mem_r_addr_o = r_addr_i;
         assign r_data_o         = r_data_int;
      end
   endgenerate


                """
            }
        ],
    }

    return attributes_dict
