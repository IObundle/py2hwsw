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
                "signals": {
                    "type": "iob_clk",
                    "params": "arst",
                },
                "descr": "clock and reset",
            },
            {
                "name": "arst_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "arst_o",
                        "width": 1,
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "data_int",
                "descr": "data_int wire",
                "signals": [
                    {"name": "data_int", "width": 2},
                ],
            },
            {
                "name": "sync",
                "descr": "sync wire",
                "signals": [
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
                    "clk_en_rst_s": "arst",
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
