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
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "RST_VAL",
                "type": "P",
                "val": "{DATA_W{1'b0}}",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
        ],
        "ports": [
            {
                "name": "clk_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "arst",
                },
                "descr": "Clock and reset",
            },
            {
                "name": "iob_rn_data_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "iob_rn_data_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "iob_rn_data_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "iob_rn_data_o",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "iob_rn_data_o_reg",
                "descr": "Output register",
                "signals": [
                    {
                        "name": "iob_rn_data_o_reg",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
    assign iob_rn_data_o = iob_rn_data_o_reg;
    always @(posedge clk_i, {"posedge" if edge else "negedge"} arst_i) begin
            if (arst_i) begin
               iob_rn_data_o_reg <= RST_VAL;
            end else begin
               iob_rn_data_o_reg <= iob_rn_data_i;
            end
         end
         """,
            },
        ],
    }

    return attributes_dict
