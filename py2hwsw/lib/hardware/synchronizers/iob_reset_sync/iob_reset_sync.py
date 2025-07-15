# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

edge = 1


def setup(py_params_dict):
    global edge
    if "RST_POL" in py_params_dict:
        edge = py_params_dict["RST_POL"]
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "clk_rst_s",
                "wires": {
                    "type": "iob_clk",
                    "params": "a",
                },
                "descr": "clock and reset",
            },
            {
                "name": "arst_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "arst_o",
                        "width": 1,
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "data_int",
                "descr": "data_int bus",
                "wires": [
                    {"name": "data_int", "width": 2},
                ],
            },
            {
                "name": "sync",
                "descr": "sync bus",
                "wires": [
                    {"name": "sync", "width": 2},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "reg1",
                "parameters": {
                    "DATA_W": 2,
                    "RST_VAL": "2'd3" if edge else "2'd0",
                },
                "port_params": {
                    "clk_en_rst_s": "a",
                },
                "connect": {
                    "clk_en_rst_s": "clk_rst_s",
                    "data_i": "data_int",
                    "data_o": "sync",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
    assign data_int = {{sync[0], {"1'b0" if edge else "1'b1"}}};
    assign arst_o = sync[1];
            """,
            },
        ],
    }

    return attributes_dict
