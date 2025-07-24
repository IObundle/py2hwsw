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
                "descr": "trailing (0), leading (1)",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "SYMBOL",
                "descr": "search zeros (0), search ones (1)",
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
<<<<<<< HEAD
                "descr": "Internal data",
=======
                "descr": "Potentially inverted data signal, based on SYMBOL parameter",
>>>>>>> cdd911ba0eeb9efca298e98fdf3834aebde65719
                "signals": [
                    {
                        "name": "data_int1",
                        "width": "W",
<<<<<<< HEAD
                        "descr": "Data internal wire",
=======
                        "descr": "Potentially inverted data signal derived from data_i",
>>>>>>> cdd911ba0eeb9efca298e98fdf3834aebde65719
                    },
                ],    
            },
            {
                "name": "data_int2",
<<<<<<< HEAD
                "descr": "Reversed data",
=======
                "descr": "Potentially reversed data signal",
>>>>>>> cdd911ba0eeb9efca298e98fdf3834aebde65719
                "signals": [
                    {
                        "name": "data_int2",
                        "width": "W",
<<<<<<< HEAD
                        "descr": "Reversed data internal wire",
=======
                        "descr": "Internal write enable signal",
>>>>>>> cdd911ba0eeb9efca298e98fdf3834aebde65719
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
                "instance_description": "count trailing zeros",
                "parameters": {
                    "W": "W",
                    "MODE": '"LOW"',
                },
                "connect": {
                    "unencoded_i": "data_int2",
                    "encoded_o": "count_o",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": r"""
<<<<<<< HEAD
               // invert if searching zeros or not
=======
                // invert if searching zeros or not
>>>>>>> cdd911ba0eeb9efca298e98fdf3834aebde65719
                generate
                   if (SYMBOL == 0) begin : g_zeros
                     assign data_int1 = data_i;
                   end else begin : g_ones
                     assign data_int1 = ~data_i;
                   end
                endgenerate
                // reverse if leading symbols or not
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
