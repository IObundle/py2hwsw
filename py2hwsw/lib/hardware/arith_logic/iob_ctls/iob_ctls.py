# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "W",
                "descr": "Write data width",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "MODE",
                "descr": "Mode",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "SYMBOL",
                "descr": "Symbol",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "data_i",
                "descr": "Input data",
                "signals": [
                    {
                        "name": "data_i",
                        "width": "W",
                        "descr": "Input data",
                    },
                ],
            },
            {
                "name": "count_o",
                "descr": "Output counter",
                "signals": [
                    {
                        "name": "count_o",
                        "width": "$clog2(W+1)",
                        "descr": "Output counter",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "data_int1",
                "descr": "Potentially inverted data signal, based on SYMBOL parameter",
                "signals": [
                    {
                        "name": "data_int1",
                        "width": "W",
                        "descr": "Internal write enable signal",
                    },
                ],
            },
            {
                "name": "data_int2",
                "descr": "Potentially reversed data signal",
                "signals": [
                    {
                        "name": "data_int2",
                        "width": "W",
                        "descr": "Internal write enable signal",
                    },
                ],
            },
            {
                "name": "count_int",
                "descr": "Counter wire",
                "signals": [
                    {
                        "name": "count_o",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reverse",
                "instantiate": False,
            },
            {
                "core_name": "iob_prio_enc",
                "instance_name": "prio_encoder0",
                "parameters": {
                    "W": "W",
                    "MODE": '"LOW"',
                },
                "connect": {
                    "unencoded_i": "data_int2",
                    "encoded_o": "count_int",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": r"""
                generate
                   if (SYMBOL == 0) begin : g_zeros
                     assign data_int1 = data_i;
                   end else begin : g_ones
                     assign data_int1 = ~data_i;
                   end
                endgenerate
                generate
                    if (MODE == 1) begin : g_reverse
                       iob_reverse #(W) reverse0 (
                            .data_i(data_int1),
                            .data_o(data_int2)
                        );
                    end else begin : g_noreverse
                        assign data_int2 = data_int1;
                    end
                endgenerate

                """
            }
        ],
    }

    return attributes_dict
