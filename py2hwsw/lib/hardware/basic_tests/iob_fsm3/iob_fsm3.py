# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "ports": [
            {
                "name": "a_o",
                "descr": "Output port",
                "signals": [
                    {"name": "a", "width": "8", "direction": "output"},
                ],
            },
        ],
        "fsm": {
            "verilog_code": """
A: a_o = 0;

B: a_o = 1;

a_o = 2;

if(a_o == 0)
begin
    pc_nxt = A;
end
else
begin
    pc_nxt = B;
end
"""
        },
    }

    return attributes_dict
