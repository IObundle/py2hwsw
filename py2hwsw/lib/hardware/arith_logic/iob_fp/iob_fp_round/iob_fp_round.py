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
                "val": "24",
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
                "name": "exponent_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "exponent_i",
                        "width": "EXP_W",
                    },
                ],
            },
            {
                "name": "mantissa_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "mantissa_i",
                        "width": "DATA_W+3",
                    },
                ],
            },
            {
                "name": "exponent_rnd_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "exponent_rnd_o",
                        "width": "EXP_W",
                    },
                ],
            },
            {
                "name": "mantissa_rnd_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "mantissa_rnd_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "round",
                "descr": "round bus",
                "signals": [
                    {"name": "round", "width": 1},
                ],
            },
            {
                "name": "mantissa_rnd_int",
                "descr": "mantissa_rnd bus",
                "signals": [
                    {"name": "mantissa_rnd_int", "width": "DATA_W"},
                ],
            },
            {
                "name": "lzc",
                "descr": "lzc bus",
                "signals": [
                    {"name": "lzc", "width": "$clog2(DATA_W)"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_fp_clz",
                "instance_name": "clz0",
                "parameters": {
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "data_i": "mantissa_rnd_int",
                    "data_o": "lzc",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        assign round = ~mantissa_i[2]? 1'b0: ~|mantissa_i[1:0] & ~mantissa_i[3]? 1'b0: 1'b1;
        assign mantissa_rnd_int = round? mantissa_i[DATA_W+3-1:3] + 1'b1: mantissa_i[DATA_W+3-1:3];
        assign exponent_rnd_o = exponent_i - {{(EXP_W-$clog2(DATA_W)){1'b0}},lzc};
        assign mantissa_rnd_o = mantissa_rnd_int << lzc;
            """,
            },
        ],
    }

    return attributes_dict
