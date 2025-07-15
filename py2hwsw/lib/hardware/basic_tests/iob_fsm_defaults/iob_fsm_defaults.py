# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "a_o",
                "descr": "Output port",
                "wires": [
                    {"name": "a_o", "width": "8"},
                ],
            },
        ],
        "fsm": {
            "default_assignments": """
a_o = 10;
""",
            "state_descriptions": """
A: a_o = 0;

B: a_o = 1;

a_o = 2;

if(a_o == 0)
begin
    pcnt_nxt = A;
end
else
begin
    pcnt_nxt = B;
end
""",
        },
    }

    return attributes_dict
