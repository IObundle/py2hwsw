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
                "val": 3,
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
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "w_clk_i",
                "descr": "Write clock input for the register array",
                "signals": [
                    {
                        "name": "w_clk_i",
                        "width": "1",
                        "descr": "Write clock input signal",
                    },
                ],
            },
            {
                "name": "w_cke_i",
                "descr": "Write clock enable input for the register array",
                "signals": [
                    {
                        "name": "w_cke_i",
                        "width": "1",
                        "descr": "Write clock enable input signal",
                    },
                ],
            },
            {
                "name": "w_arst_i",
                "descr": "Write asynchronous reset input for the register array",
                "signals": [
                    {
                        "name": "w_arst_i",
                        "width": "1",
                        "descr": "Write asynchronous reset input signal",
                    },
                ],
            },
            {
                "name": "w_addr_i",
                "descr": "Write address input for the register array",
                "signals": [
                    {
                        "name": "w_addr_i",
                        "width": "ADDR_W",
                        "descr": "Write address input signal",
                    },
                ],
            },
            {
                "name": "w_data_i",
                "descr": "Write data input for the register array",
                "signals": [
                    {
                        "name": "w_data_i",
                        "width": "DATA_W",
                        "descr": "Write data input signal",
                    },
                ],
            },
            {
                "name": "r_clk_i",
                "descr": "Read clock input for the register array",
                "signals": [
                    {
                        "name": "r_clk_i",
                        "width": "1",
                        "descr": "Read clock input signal",
                    },
                ],
            },
            {
                "name": "r_cke_i",
                "descr": "Read clock enable input for the register array",
                "signals": [
                    {
                        "name": "r_cke_i",
                        "width": "1",
                        "descr": "Read clock enable input signal",
                    },
                ],
            },
            {
                "name": "r_arst_i",
                "descr": "Read asynchronous reset input for the register array",
                "signals": [
                    {
                        "name": "r_arst_i",
                        "width": "1",
                        "descr": "Read asynchronous reset input signal",
                    },
                ],
            },
            {
                "name": "r_addr_i",
                "descr": "Read address input for the register array",
                "signals": [
                    {
                        "name": "r_addr_i",
                        "width": "ADDR_W",
                        "descr": "Read address input signal",
                    },
                ],
            },
            {
                "name": "r_data_o",
                "descr": "Read data output from the register array",
                "signals": [
                    {
                        "name": "r_data_o",
                        "width": "DATA_W",
                        "descr": "Read data output signal",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "regarray_in",
                "descr": "Internal data input for the register array",
                "signals": [
                    {
                        "name": "regarray_in",
                        "width": "((2**ADDR_W)*DATA_W)",
                        "descr": "Internal data input signal for the register array",
                    },
                ],
            },
            {
                "name": "regarray_en",
                "descr": "Enable signal for the register array",
                "signals": [
                    {
                        "name": "regarray_en",
                        "width": "(2**ADDR_W)",
                        "descr": "Enable signal for the register array",
                    },
                ],
            },
            {
                "name": "r_data",
                "descr": "Internal read data output from the register array",
                "signals": [
                    {
                        "name": "r_data",
                        "width": "DATA_W",
                        "descr": "Enable signal for the register array",
                    },
                ],
            },
            {
                "name": "r_clk_en_rst_s",
                "descr": "Clock, clock enable and reset for read operations",
                "signals": [
                    {
                        "name": "r_clk_i",
                        "width": "1",
                    },
                    {
                        "name": "r_cke_i",
                        "width": "1",
                    },
                    {
                        "name": "r_arst_i",
                        "width": "1",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_sync",
                "instantiate": False,
                "dest_dir": "hardware/simulation/src",
            },
            {
                "core_name": "iob_reg",
                "instantiate": False,
                "port_params": {
                    "clk_en_rst_s": "c_a_e",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "rdata",
                "port_params": {
                    "clk_en_rst_s": "c_a",
                },
                "parameters": {
                    "DATA_W": "DATA_W",
                    "RST_VAL": "{DATA_W{1'd0}}",
                },
                "connect": {
                    "clk_en_rst_s": "r_clk_en_rst_s",
                    "data_i": "r_data",
                    "data_o": "r_data_o",
                },
            },
        ],
        "comb": {
            "code": """
    r_data = regarray_in[r_addr_i*DATA_W+:DATA_W];
        """,
        },
        "snippets": [
            {
                "verilog_code": r"""

   genvar addr;
   generate
      for (addr = 0; addr < (2 ** ADDR_W); addr = addr + 1) begin : gen_register_file
         assign regarray_en[addr] = (w_addr_i == addr);
         iob_reg_cae #(
            .DATA_W (DATA_W),
            .RST_VAL({DATA_W{1'd0}})
         ) rdata (
            .clk_i (w_clk_i),
            .cke_i (w_cke_i),
            .arst_i(w_arst_i),
            .en_i  (regarray_en[addr]),
            .data_i(w_data_i),
            .data_o(regarray_in[addr*DATA_W+:DATA_W])
         );
      end
   endgenerate

                """
            }
        ],
    }

    return attributes_dict
