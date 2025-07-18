# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "W",
                "descr": "Width",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a_r_e",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "data_o",
                "descr": "Data output",
                "signals": [
                    {
                        "name": "data_o",
                        "width": "W",
                        "descr": "Data output signal",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "bin_counter",
                "descr": "Binary counter",
                "signals": [
                    {
                        "name": "bin_counter",
                        "width": "W",
                        "descr": "Binary counter wire",
                    },
                ],
            },
            {
                "name": "bin_counter_nxt",
                "descr": "Binary counter next",
                "signals": [
                    {
                        "name": "bin_counter_nxt",
                        "width": "W",
                        "descr": "Binary counter next wire",
                    },
                ],
            },
            {
                "name": "gray_counter",
                "descr": "Gray counter",
                "signals": [
                    {
                        "name": "gray_counter",
                        "width": "W",
                        "descr": "Gray counter wire",
                    },
                ],
            },
            {
                "name": "gray_counter_nxt",
                "descr": "Gray counter next",
                "signals": [
                    {
                        "name": "gray_counter_nxt",
                        "width": "W",
                        "descr": "Gray counter next wire",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "bin_counter_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "parameters": {
                    "DATA_W": "W",
                    "RST_VAL": "{{(W - 1) {1'd0}}, 1'd1}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "bin_counter_nxt",
                    "data_o": "bin_counter",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "gray_counter_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "parameters": {
                    "DATA_W": "W",
                    "RST_VAL": "{W{1'd0}}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "gray_counter_nxt",
                    "data_o": "gray_counter",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
                assign bin_counter_nxt = bin_counter + 1'b1;
                generate
                    if (W > 1) begin : g_width_gt1
                        assign gray_counter_nxt = {{bin_counter[W-1], bin_counter[W-2:0] ^ bin_counter[W-1:1]}};
                     end else begin : g_width_eq1
                        assign gray_counter_nxt = bin_counter;
                    end
                endgenerate
                assign data_o = gray_counter;


                """
            }
        ],
    }

    return attributes_dict
