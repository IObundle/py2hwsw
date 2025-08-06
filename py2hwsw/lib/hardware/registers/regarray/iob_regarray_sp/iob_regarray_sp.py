# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "ADDR_W",
                "type": "P",
                "val": 2,
                "min": "NA",
                "max": "NA",
                "descr": "Address width in bits",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": 21,
                "min": "NA",
                "max": "NA",
                "descr": "Width of the data in bits",
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
                "name": "we_i",
                "descr": "Write enable signal for the register array",
                "signals": [
                    {
                        "name": "we_i",
                        "width": "1",
                        "descr": "Write enable input signal",
                    },
                ],
            },
            {
                "name": "addr_i",
                "descr": "Address input for the register array",
                "signals": [
                    {
                        "name": "addr_i",
                        "width": "ADDR_W",
                        "descr": "Address input signal",
                    },
                ],
            },
            {
                "name": "d_i",
                "descr": "Data input for the register array",
                "signals": [
                    {
                        "name": "d_i",
                        "width": "DATA_W",
                        "descr": "Data input signal",
                    },
                ],
            },
            {
                "name": "d_o",
                "descr": "Data output from the register array",
                "signals": [
                    {
                        "name": "d_o",
                        "width": "DATA_W",
                        "descr": "Data output signal",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "data_in",
                "descr": "Internal data input for the register array",
                "signals": [
                    {
                        "name": "data_in",
                        "width": "DATA_W*(2**ADDR_W)",
                        "descr": "Internal data input signal for the register array",
                    },
                ],
            },
            {
                "name": "data_out",
                "descr": "Internal data output from the register array",
                "signals": [
                    {
                        "name": "data_out",
                        "width": "DATA_W*(2**ADDR_W)",
                        "descr": "Internal data output signal from the register array",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "instantiate": False,
            },
        ],
        "snippets": [
            {
                "verilog_code": r"""
    assign data_in = d_i << (addr_i * DATA_W);           
    assign d_o = data_out >> (addr_i * DATA_W);
    genvar i;
    generate
      for (i = 0; i < 2 ** ADDR_W; i = i + 1) begin : g_regarray
            wire reg_en_i;
            assign reg_en_i = we_i & (addr_i == i);
            iob_reg_care #(
                .DATA_W(DATA_W)
            ) regarray_sp_inst (
                .clk_i (clk_i),
                .cke_i(cke_i),
                .arst_i (arst_i),
                .rst_i (rst_i),
                .en_i  (reg_en_i),
                .data_i(data_in[DATA_W*(i+1)-1:DATA_W*i]),
                .data_o(data_out[DATA_W*(i+1)-1:DATA_W*i])
            );
       end
    endgenerate

                """
            }
        ],
    }

    return attributes_dict
