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
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
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
                "name": "data_l_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "data_l_o",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "data_h_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "data_h_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
            always @(posedge clk_i) 
            data_h_o <= data_i;
            always @(negedge clk_i) 
            data_l_o <= data_i;
         """,
            },
        ],
    }

    return attributes_dict
