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
                "descr": "width",
            },
            {
                "name": "EXP_W",
                "type": "P",
                "val": 8,
                "min": "NA",
                "max": "NA",
                "descr": "EXP_W value.",
            },
            {
                "name": "MAN_W",
                "type": "D",
                "val": "DATA_W-EXP_W",
                "min": "NA",
                "max": "NA",
                "descr": "MAN_W  value.",
            },
        ],
        "ports": [
            {
                "name": "data_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "data_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "nan_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "nan_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "infinite_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "infinite_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "zero_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "zero_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "sub_normal_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "sub_normal_o",
                        "width": 1,
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "sign",
                "descr": "sign bus",
                "wires": [
                    {"name": "sign", "width": 1},
                ],
            },
            {
                "name": "exponent",
                "descr": "exponent bus",
                "wires": [
                    {"name": "exponent", "width": "EXP_W"},
                ],
            },
            {
                "name": "mantissa",
                "descr": "mantissa bus",
                "wires": [
                    {"name": "mantissa", "width": "MAN_W-1"},
                ],
            },
            {
                "name": "exp_all_ones",
                "descr": "exp_all_ones bus",
                "wires": [
                    {"name": "exp_all_ones", "width": 1},
                ],
            },
            {
                "name": "exp_zero",
                "descr": "exp_zero bus",
                "wires": [
                    {"name": "exp_zero", "width": 1},
                ],
            },
            {
                "name": "man_zero",
                "descr": "man_zero bus",
                "wires": [
                    {"name": "man_zero", "width": 1},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        assign  sign = data_i[DATA_W-1];
        assign  exponent = data_i[DATA_W-2 -: EXP_W];
        assign  mantissa = data_i[MAN_W-2:0];
        assign  exp_all_ones = &exponent;
        assign  exp_zero = ~|exponent;
        assign  man_zero = ~|mantissa;
        assign nan_o        = exp_all_ones & ~man_zero;
        assign infinite_o   = exp_all_ones & man_zero;
        assign zero_o       = exp_zero & man_zero;
        assign sub_normal_o = exp_zero & ~man_zero;

            """,
            },
        ],
    }

    return attributes_dict
