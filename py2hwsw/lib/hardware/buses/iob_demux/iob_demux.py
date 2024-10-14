# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
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
                "descr": "Number of outputs",
            },
        ],
        "ports": [
            {
                "name": "sel_i",
                "descr": "Selector interface",
                "signals": [
                    {
                        "name": "sel_i",
                        "width": "($clog2(N)+($clog2(N)==0))",
                    },
                ],
            },
            {
                "name": "data_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "data_i",
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
                        "width": "N*DATA_W",
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            // //Select the data to output
   genvar i;
   generate
      for (i = 0; i < N; i = i + 1) begin : gen_demux
         assign data_o[i*DATA_W+:DATA_W] = (sel_i==i)? data_i : {DATA_W{1'b0}};
      end
   endgenerate

            """,
            },
        ],
    }

    return attributes_dict
