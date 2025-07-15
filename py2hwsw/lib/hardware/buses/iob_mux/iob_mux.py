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
                "descr": "Width of data interface",
            },
            {
                "name": "N",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Number of inputs",
            },
            {
                "name": "SEL_W",
                "type": "D",
                "val": "($clog2(N) == 0 ? 1 : $clog2(N))",
                "min": "NA",
                "max": "NA",
                "descr": "Width of selector interface",
            },
        ],
        "ports": [
            {
                "name": "sel_i",
                "descr": "Selector interface",
                "wires": [
                    {
                        "name": "sel_i",
                        "width": "SEL_W",
                    },
                ],
            },
            {
                "name": "data_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "data_i",
                        "width": "N*DATA_W",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "data_o",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        integer input_sel;
        always @* begin
            data_o = {DATA_W{1'b0}};
            for (input_sel = 0; input_sel < N; input_sel = input_sel + 1) begin : gen_mux
                if (input_sel[0+:SEL_W] == sel_i) begin
                     data_o = data_i[input_sel*DATA_W+:DATA_W];
                end
            end
        end
            """,
            },
        ],
    }

    return attributes_dict
