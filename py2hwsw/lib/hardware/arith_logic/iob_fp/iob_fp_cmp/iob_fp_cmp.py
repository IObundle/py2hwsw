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
                "name": "EXP_W",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
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
                "name": "rst_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "start_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "start_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "fn_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "fn_i",
                        "width": 2,
                    },
                ],
            },
            {
                "name": "op_a_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "op_a_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "op_b_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "op_b_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "done_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "done_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "res_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "res_o",
                        "width": 1,
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "equal_int",
                "descr": "equal bus",
                "signals": [
                    {"name": "equal_int", "width": 1},
                ],
            },
            {
                "name": "less_int",
                "descr": "less bus",
                "signals": [
                    {"name": "less_int", "width": 1},
                ],
            },
            {
                "name": "op_a_nan_int",
                "descr": "op_a_nan bus",
                "signals": [
                    {"name": "op_a_nan_int", "width": 1},
                ],
            },
            {
                "name": "op_b_nan_int",
                "descr": "op_b_nan bus",
                "signals": [
                    {"name": "op_b_nan_int", "width": 1},
                ],
            },
            {
                "name": "res_int",
                "descr": "res bus",
                "signals": [
                    {"name": "res_int", "width": 1},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        assign equal_int = (op_a_i == op_b_i)? 1'b1: 1'b0;
        assign less_int = (op_a_i[DATA_W-1] ^ op_b_i[DATA_W-1])? (op_a_i[DATA_W-1]? 1'b1: 1'b0):op_a_i[DATA_W-1]? ((op_a_i[DATA_W-2:0] > op_b_i[DATA_W-2:0])? 1'b1: 1'b0):((op_a_i[DATA_W-2:0] > op_b_i[DATA_W-2:0])? 1'b0: 1'b1);
        assign op_a_nan_int = &op_a_i[DATA_W-2 -: EXP_W] & |op_a_i[DATA_W-EXP_W-2:0];
        assign op_b_nan_int = &op_b_i[DATA_W-2 -: EXP_W] & |op_b_i[DATA_W-EXP_W-2:0];
        assign res_int = (op_a_nan_int | op_b_nan_int)? 1'b0:fn_i[1]? equal_int:fn_i[0]? less_int:less_int|equal_int;

        always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         res_o <= 1'b0;
         done_o <= 1'b0;
      end else begin
         res_o <= res_int;
         done_o <= start_i;
      end
    end
            """,
            },
        ],
    }

    return attributes_dict
