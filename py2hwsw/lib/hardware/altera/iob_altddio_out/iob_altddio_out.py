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
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
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
                "name": "data_l_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "data_l_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "data_h_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "data_h_i",
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
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "data_l_i_reg",
                "descr": "data_l_i_reg bus",
                "signals": [
                    {"name": "data_l_i_reg", "width": "DATA_W"},
                ],
            },
            {
                "name": "data_h_i_reg",
                "descr": "data_h_i_reg bus",
                "signals": [
                    {"name": "data_h_i_reg", "width": "DATA_W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            always @(posedge clk_i) 
            data_h_i_reg <= data_h_i;
            always @(negedge clk_i) 
            data_l_i_reg <= data_l_i;
            assign data_o = clk_i ? data_h_i_reg : data_l_i_reg;
            """,
            },
        ],
    }

    return attributes_dict
