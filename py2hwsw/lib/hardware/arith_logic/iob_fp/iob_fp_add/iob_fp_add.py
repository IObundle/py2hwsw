# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
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
                "descr": "Exponent width",
            },
            {
                "name": "MAN_W",
                "type": "D",
                "val": "DATA_W-EXP_W",
                "min": "NA",
                "max": "NA",
                "descr": "MAN width",
            },
            {
                "name": "BIAS",
                "type": "D",
                "val": "2**(EXP_W-1)-1",
                "min": "NA",
                "max": "NA",
                "descr": "BIAS",
            },
            {
                "name": "EXTRA",
                "type": "D",
                "val": "3",
                "min": "NA",
                "max": "NA",
                "descr": "EXTRA",
            },
            {
                "name": "STICKY_BITS",
                "type": "D",
                "val": "2*BIAS-1",
                "min": "NA",
                "max": "NA",
                "descr": "STICKY_BITS",
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
                "name": "op_a_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": " op_a_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "data_o",
                        "width": "$clog2(DATA_W+1)",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_fp_special",
                "instance_name": "iob_fp_special_inst",
            },
            {
                "core_name": "iob_fp_clz",
                "instance_name": "iob_fp_clz_inst",
            },
            {
                "core_name": "iob_fp_round",
                "instance_name": "iob_fp_round_inst",
            },
        ],
    }

    return attributes_dict
