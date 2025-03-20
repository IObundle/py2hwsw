# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DIVIDEND_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Dividend width",
            },
            {
                "name": "DIVISOR_W",
                "type": "P",
                "val": "DIVIDEND_W",
                "min": "NA",
                "max": "NA",
                "descr": "Divisor width",
            },
            {
                "name": "QUOTIENT_W",
                "type": "P",
                "val": "DIVIDEND_W",
                "min": "NA",
                "max": "NA",
                "descr": "Quotient width",
            },
            # Localparam
            {
                "name": "DQR_W",
                "type": "F",
                "val": "(DIVISOR_W+DIVIDEND_W)+1",
                "min": "NA",
                "max": "NA",
                "descr": "",
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
                "name": "status_io",
                "descr": "",
                "signals": [
                    {
                        "name": "start_i",
                        "width": 1,
                        "descr": "Start signal",
                    },
                    {
                        "name": "done_o",
                        "width": 1,
                        "descr": "Done signal",
                    },
                ],
            },
            {
                "name": "div_io",
                "descr": "Division interface",
                "signals": [
                    {
                        "name": "dividend_i",
                        "width": "DIVIDEND_W",
                        "descr": "",
                    },
                    {
                        "name": "divisor_i",
                        "width": "DIVISOR_W",
                        "descr": "",
                    },
                    {
                        "name": "quotient_o",
                        "width": "QUOTIENT_W",
                        "descr": "",
                    },
                    {
                        "name": "remainder_o",
                        "width": "DIVISOR_W",
                        "descr": "",
                    },
                ],
            },
        ],
        "wires": [
            # { # NOTE: This wire is implicitly create by py2
            #     "name": "dqr_reg_nxt",
            #     "descr": "dqr_reg_nxt wire",
            #     "signals": [
            #         {"name": "dqr_reg_nxt", "width": "DQR_W"},
            #     ],
            # },
            {
                "name": "dqr_reg",
                "descr": "dqr_reg wire",
                "signals": [
                    {"name": "dqr_reg", "width": "DQR_W"},
                ],
            },
            # { # NOTE: This wire is implicitly create by py2
            #    "name": "divisor_reg_nxt",
            #    "descr": "divisor_reg_nxt wire",
            #    "signals": [
            #        {"name": "divisor_reg_nxt", "width": "DIVISOR_W"},
            #    ],
            # },
            {
                "name": "divisor_reg",
                "descr": "divisor_reg wire",
                "signals": [
                    {"name": "divisor_reg", "width": "DIVISOR_W"},
                ],
            },
            {
                "name": "subtraend",
                "descr": "subtraend wire",
                "signals": [
                    {"name": "subtraend", "width": "DIVISOR_W+1"},
                ],
            },
            {
                "name": "tmp",
                "descr": "tmp wire",
                "signals": [
                    {"name": "tmp", "width": "DIVISOR_W+2"},
                ],
            },
            # { # NOTE: This wire is implicitly create by py2
            #    "name": "pcnt_nxt",
            #    "descr": "pcnt_nxt wire",
            #    "signals": [
            #        {"name": "pcnt_nxt", "width": "$clog2(DIVIDEND_W+1)"},
            #    ],
            # },
            {
                "name": "pcnt",
                "descr": "pcnt wire",
                "signals": [
                    {"name": "pcnt", "width": "$clog2(DIVIDEND_W+1)"},
                ],
            },
            {
                "name": "done_reg",
                "descr": "done_reg wire",
                "signals": [
                    {"name": "done_reg", "width": 1},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            assign subtraend = dqr_reg[(DQR_W-2)-:(DIVISOR_W+1)];
            assign quotient_o  = dqr_reg[QUOTIENT_W-1:0];
            assign remainder_o = dqr_reg[(DQR_W-2)-:DIVISOR_W];
            assign done_o = done_reg;
         """,
            },
        ],
        "comb": {
            "code": """
    tmp = {1'b0, subtraend} - {1'b0, divisor_reg};
    pcnt_nxt    = pcnt + 1'b1;
    dqr_reg_nxt     = dqr_reg;
    divisor_reg_nxt = divisor_reg;
    done_reg    = 1'b1;

    if (pcnt == 0) begin  //wait for start, load operands and do it
      if (!start_i) begin
        pcnt_nxt = pcnt;
      end else begin
        divisor_reg_nxt = divisor_i;
        dqr_reg_nxt     = {{(DIVISOR_W+1){1'b0}}, dividend_i};
      end
    end else if (pcnt == (DIVIDEND_W+1)) begin
      pcnt_nxt = 0;
    end else begin  //shift and subtract
      done_reg = 1'b0;
      if (~tmp[DIVISOR_W+1]) begin
        dqr_reg_nxt = {tmp[DIVISOR_W:0], dqr_reg[DIVIDEND_W-2 : 0], 1'b1};
      end else begin
        dqr_reg_nxt = {1'b0,dqr_reg[DQR_W-3 : 0], 1'b0};
      end
    end
""",
        },
    }

    return attributes_dict
