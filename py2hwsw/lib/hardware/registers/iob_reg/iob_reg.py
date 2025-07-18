# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys

sys.path.append("../../../scripts")
from iob_globals import iob_globals


def setup(py_params_dict):

    port_params = (
        py_params_dict["port_params"]
        if "port_params" in py_params_dict
        else {"clk_en_rst_s": "c_a"}
    )
    assert "clk_en_rst_s" in port_params, "clk_en_rst_s port is missing"

    reset_polarity = getattr(iob_globals(), "reset_polarity", "positive")

    clk_port_params = port_params["clk_en_rst_s"]

    if reset_polarity != "positive":
        port_params["clk_en_rst_s"] = port_params["clk_en_rst_s"].replace("a", "an")

    clk_s_params_list = [x for x in port_params["clk_en_rst_s"].split("_") if x != ""]

    suffix_list = [
        "c",
        "a",
        "an",
        "r",
        "e",
    ]

    suffix = "".join([x for x in suffix_list if x in clk_s_params_list])

    reg_type = "iob_regn" if "n" in clk_s_params_list else "iob_reg"

    reg_name = "_".join(filter(lambda x: x != "", [reg_type, suffix]))

    rst_str = ""
    en_str = ""

    sensitivity_list = "negedge clk_i" if "n" in clk_s_params_list else "posedge clk_i"

    if "a" in clk_s_params_list:
        sensitivity_list = f"{sensitivity_list}, posedge arst_i"
    elif "an" in clk_s_params_list:
        sensitivity_list = f"{sensitivity_list}, negedge arst_n_i"

    if any([x in clk_s_params_list for x in ["a", "an"]]):
        arst_con = f"{'arst' if 'a' in clk_s_params_list else '~arst_n'}_i"
        rst_str += f"        if ({arst_con}) begin\n            data_o <= RST_VAL;\n        end"

    if "r" in clk_s_params_list:
        rst_str += f"{' else ' if rst_str != '' else '        '}if (rst_i) begin\n            data_o <= RST_VAL;\n        end"

    if any([x in clk_s_params_list for x in ["c", "e"]]):
        en_con = (
            " & ".join([f"{x}_i" for x in ["c", "e"] if x in clk_s_params_list])
            .replace("e_i", "en_i")
            .replace("c_i", "cke_i")
        )
        en_str = f"{'else ' if rst_str != '' else '        '}if ({en_con}) begin\n            data_o <= data_i;\n        end"
    else:
        en_str = f"{'else begin' if rst_str != '' else '        '}\n            data_o <= data_i;\n        {'end' if rst_str != '' else ''}"

    attributes_dict = {
        "name": reg_name,
        "generate_hw": True,
        "description": f"Generated register module.",
        "python_parameters": [
            {
                "name": "port_params",
                "val": port_params,
                "descr": "Port parameters are passed to interfaces to generate different interfaces.",
            },
        ],
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
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": clk_port_params,
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "data_i",
                "descr": "Data input",
                "signals": [
                    {
                        "name": "data_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Data output",
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
