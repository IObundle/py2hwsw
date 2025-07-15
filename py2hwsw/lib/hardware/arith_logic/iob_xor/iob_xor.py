# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "W",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "N",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
        ],
        "ports": [
            {
                "name": "in_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "in_i",
                        "width": "N*W",
                    },
                ],
            },
            {
                "name": "out_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "out_o",
                        "width": "W",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "xor_vec",
                "descr": "xor_vec bus",
                "wires": [
                    {"name": "xor_vec", "width": "N*W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
            assign xor_vec[0 +: W] = in_i[0 +: W];
   
   genvar i;
   generate
      for (i = 1; i < N; i = i + 1) begin : gen_mux
         assign xor_vec[i*W +: W] = in_i[i*W +: W] ^ xor_vec[(i-1)*W +: W];
      end
   endgenerate

   assign out_o = xor_vec[(N-1)*W +: W];
            """,
            },
        ],
    }

    return attributes_dict
