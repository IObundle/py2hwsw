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
                "type": "D",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "Exponent width",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "rst_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "rst_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "start_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "start_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "max_n_min_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "max_n_min_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "op_a_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "op_a_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "op_b_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "op_b_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "done_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "done_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "res_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "res_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "bigger",
                "descr": "bigger bus",
                "wires": [
                    {"name": "bigger", "width": "DATA_W"},
                ],
            },
            {
                "name": "smaller",
                "descr": "smaller bus",
                "wires": [
                    {"name": "smaller", "width": "DATA_W"},
                ],
            },
            {
                "name": "op_a_nan",
                "descr": "op_a_nan bus",
                "wires": [
                    {"name": "op_a_nan", "width": 1},
                ],
            },
            {
                "name": "op_b_nan",
                "descr": "op_b_nan bus",
                "wires": [
                    {"name": "op_b_nan", "width": 1},
                ],
            },
            {
                "name": "rst_int",
                "descr": "rst bus",
                "wires": [
                    {"name": "rst_int", "width": "DATA_W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        // Canonical NAN
       `define NAN {1'b0, {EXP_W{1'b1}}, 1'b1, {(DATA_W-EXP_W-2){1'b0}}}
        // Infinite
        `define INF(SIGN) {SIGN, {EXP_W{1'b1}}, {(DATA_W-EXP_W-1){1'b0}}}
        assign bigger  = (op_a_i[DATA_W-1] ^ op_b_i[DATA_W-1])? (op_a_i[DATA_W-1]? op_b_i: op_a_i):op_a_i[DATA_W-1]? ((op_a_i[DATA_W-2:0] > op_b_i[DATA_W-2:0])? op_b_i: op_a_i):((op_a_i[DATA_W-2:0] > op_b_i[DATA_W-2:0])? op_a_i: op_b_i);
        assign smaller = (op_a_i[DATA_W-1] ^ op_b_i[DATA_W-1])? (op_a_i[DATA_W-1]? op_a_i: op_b_i):op_a_i[DATA_W-1]? ((op_a_i[DATA_W-2:0] > op_b_i[DATA_W-2:0])? op_a_i: op_b_i):((op_a_i[DATA_W-2:0] > op_b_i[DATA_W-2:0])? op_b_i: op_a_i);
        assign op_a_nan = &op_a_i[DATA_W-2 -: EXP_W] & |op_a_i[DATA_W-EXP_W-2:0];
        assign op_b_nan = &op_b_i[DATA_W-2 -: EXP_W] & |op_b_i[DATA_W-EXP_W-2:0];
        assign res_int = (op_a_nan & op_b_nan)? `NAN: op_a_nan? op_b_i:op_b_nan? op_a_i: max_n_min_i? bigger: smaller;
        always @(posedge clk_i, posedge rst_i) begin
      if (rst_i) begin
         res_o <= {DATA_W{1'b0}};
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
