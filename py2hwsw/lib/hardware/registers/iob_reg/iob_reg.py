# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    
    port_params = py_params_dict["port_params"] if "port_params" in py_params_dict else {"clk_s": "cke_arst"}
    assert "clk_s" in port_params, "clk_s port is missing"

    clk_s_params = [x for x in port_params["clk_s"].split("_") if x != ""] if "clk_s" in port_params else []
    if all(x in clk_s_params for x in ["arst", "anrst"]) or all(x in clk_s_params for x in ["rst", "nrst"]):
        raise ValueError("There can only be one type of reset signal for each synchronous and asynchronous reset")

    rst_str = ""
    en_str = ""

    if "arst" in clk_s_params:
        sensitivity_list = "posedge clk_i, posedge arst_i"
    elif "anrst" in clk_s_params:
        sensitivity_list = "posedge clk_i, negedge anrst_i"
    else:
        sensitivity_list = "posedge clk_i"

    if any([x in clk_s_params for x in ["arst", "anrst", "rst", "nrst"]]):
        rst_con = ' | '.join([f"{'~' if 'n' in x else ''}{x}_i" for x in ["arst", "anrst", "rst", "nrst"] if x in clk_s_params])
        rst_str = f"        if ({rst_con}) begin\n            data_o <= RST_VAL;\n        end"

    if "cke" in clk_s_params or "en" in clk_s_params:
        en_con = ' & '.join([f"{x}_i" for x in ["cke", "en"] if x in clk_s_params])
        en_str = f"{'else ' if rst_str != '' else '        '}if ({en_con}) begin\n            data_o <= data_i;\n        end"
    else:
        en_str = f"{'else begin' if rst_str != '' else '        '}\n            data_o <= data_i;\n        {'end' if rst_str != '' else ''}"

    attributes_dict = {
        "generate_hw": True,
        "version": "0.1",
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
                "name": "clk_s",
                "signals": {
                    "type": "iob_clk",
                    "params": port_params["clk_s"],
                },
                "descr": "Clock, clock enable and reset",
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
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": f"""
    always @({sensitivity_list}) begin
{rst_str} {en_str}
    end
         """,
            },
        ],
    }

    return attributes_dict
