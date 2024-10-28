# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
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
                "name": "status",
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
                "name": "quotient_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "quotient_o",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "remainder_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "remainder_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "divisor_reg",
                "descr": "divisor_reg wire",
                "signals": [
                    {"name": "divisor_reg", "width": "DATA_W"},
                ],
            },
            {
                "name": "quotient_int",
                "descr": "quotient_int wire",
                "signals": [
                    {"name": "quotient_int", "width": "DATA_W"},
                ],
            },
            {
                "name": "incr",
                "descr": "incr wire",
                "signals": [
                    {"name": "incr", "width": 1},
                ],
            },
            {
                "name": "res_acc",
                "descr": "res_acc wire",
                "signals": [
                    {"name": "res_acc", "width": "DATA_W+1"},
                ],
            },
            {
                "name": "pc",
                "descr": "pc wire",
                "signals": [
                    {"name": "pc", "width": 2},
                ],
            },
            {
                "name": "div_frac",
                "descr": "Division interface",
                "signals": [
                    {
                        "name": "dividend_i",
                    },
                    {
                        "name": "divisor_i",
                    },
                    {
                        "name": "quotient_int",
                    },
                    {
                        "name": "remainder_o",
                    },
                ],
            },
        ],
        "blocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "divisor_reg0",
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "1'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "divisor_i",
                    "data_o": "divisor_reg",
                },
            },
            {
                "core_name": "iob_div_subshift",
                "instance_name": "div_subshift0",
                "parameters": {
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "status": "status",
                    "div": "div_frac",
                },
            },
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "instantiate": False,
                "dest_dir": "hardware/simulation/src",
            },
        ],
        "fsm": {
            "verilog_code": """
default_assignments:
    incr        = 1'b0;
    quotient_o  = quotient_int + incr;
    res_acc_nxt = res_acc + remainder_o;
    res_acc_en  = 1'b0;

    if (!start_i) begin //wait for div start
        pc_nxt = pc;
    end

    if (!done_o) begin //wait for div done
        pc_nxt = pc;
    end

    res_acc_en = 1'b1;
    if (res_acc_nxt >= divisor_i) begin
        incr        = 1'b1;
        res_acc_nxt = res_acc + remainder_o - divisor_i;
    end
    if (!start_i) begin
        pc_nxt = pc;
    end
    else begin
        pc_nxt = 1'b1;
    end
""",
        },
    }

    return attributes_dict
