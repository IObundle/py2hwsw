# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Width",
                "type": "P",
                "val": "4",
                "min": "NA",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "gr_i",
                "descr": "Gray input",
                "signals": [
                    {
                        "name": "gr_i",
                        "width": "DATA_W",
                        "descr": "Gray input signal",
                    },
                ],
            },
            {
                "name": "bin_o",
                "descr": "Binary output",
                "signals": [
                    {
                        "name": "bin_o",
                        "width": "DATA_W",
                        "descr": "Binary output signal",
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
                genvar pos;

                generate
                   for (pos = 0; pos < DATA_W; pos = pos + 1) begin : gen_bin
                      assign bin_o[pos] = ^gr_i[DATA_W-1:pos];
                   end
                endgenerate
                """
            }
        ],
    }

    return attributes_dict
