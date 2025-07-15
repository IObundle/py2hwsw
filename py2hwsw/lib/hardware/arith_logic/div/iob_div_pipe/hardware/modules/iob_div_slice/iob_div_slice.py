# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "STAGE",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "OUTPUT_REG",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "dividend_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "dividend_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "divisor_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "divisor_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "quotient_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "quotient_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "dividend_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "dividend_o",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
            {
                "name": "divisor_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "divisor_o",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
            {
                "name": "quotient_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "quotient_o",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "sub_sign",
                "descr": "sub_sign bus",
                "signals": [
                    {"name": "sub_sign", "width": 1},
                ],
            },
            {
                "name": "sub_res",
                "descr": "sub_res bus",
                "signals": [
                    {"name": "sub_res", "width": "2*DATA_W-STAGE+1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            assign sub_res  = {{DATA_W{1'b0}}, dividend_i} - {{STAGE{1'b0}}, divisor_i, {(DATA_W-STAGE){1'b0}}};
   assign sub_sign = sub_res[2*DATA_W-STAGE];

   generate
      if (OUTPUT_REG) begin
         always @(posedge clk_i) begin
            dividend_o <= (sub_sign) ? dividend_i : sub_res[DATA_W-1:0];
            quotient_o <= quotient_i << 1 | {{(DATA_W - 1) {1'b0}}, ~sub_sign};
            divisor_o  <= divisor_i;
         end
      end else begin
         always @* begin
            dividend_o = (sub_sign) ? dividend_i : sub_res[DATA_W-1:0];
            quotient_o = quotient_i << 1 | {{(DATA_W - 1) {1'b0}}, ~sub_sign};
            divisor_o  = divisor_i;
         end
      end
   endgenerate

            """,
            },
        ],
    }
    return attributes_dict
