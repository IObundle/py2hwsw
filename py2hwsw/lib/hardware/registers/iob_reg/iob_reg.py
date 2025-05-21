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

    clk_s_params = [x for x in port_params["clk_en_rst_s"].split("_") if x != ""]

    # Remove duplicated entries
    clk_s_params = list(dict.fromkeys(clk_s_params))

    global_params = "_".join([x for x in clk_s_params if x in ["c", "cn", "a", "an"]])
    global_params = iob_globals(clk_params=global_params).clk_params.split("_")

    # Set default values if not provided
    if not any([x in global_params for x in ["c", "cn"]]):
        global_params.append("c")
    if not any([x in global_params for x in ["a", "an"]]):
        global_params.append("a")

    for g in global_params:
        for p in clk_s_params:
            if p.startswith(g[0]):
                clk_s_params.remove(p)
                clk_s_params.append(g)

    suffix_list = [
        "c",
        "cn",
        "a",
        "an",
        "r",
        "rn",
        "e",
        "en",
    ]

    suffix = "".join([x for x in suffix_list if x in clk_s_params])

    reg_type = "iob_regn" if "n" in clk_s_params else "iob_reg"

    reg_name = "_".join(filter(lambda x: x != "", [reg_type, suffix]))

    rst_str = ""
    en_str = ""

    sensitivity_list = "negedge clk_i" if "n" in clk_s_params else "posedge clk_i"
    if "a" in clk_s_params:
        sensitivity_list = f"{sensitivity_list}, posedge arst_i"
    elif "an" in clk_s_params:
        sensitivity_list = f"{sensitivity_list}, negedge arst_n_i"

    if any([x in clk_s_params for x in ["a", "an"]]):
        arst_con = f"{'arst' if 'a' in clk_s_params else '~arst_n'}_i"
        rst_str += f"        if ({arst_con}) begin\n            data_o <= RST_VAL;\n        end"
    if any([x in clk_s_params for x in ["r", "rn"]]):
        rst_con = f"{'rst' if 'r' in clk_s_params else '~rst_n'}_i"
        rst_str += f"{' else ' if rst_str != '' else '        '}if ({rst_con}) begin\n            data_o <= RST_VAL;\n        end"

    if any([x in clk_s_params for x in ["c", "cn", "e", "en"]]):
        en_con = (
            " & ".join([f"{x}_i" for x in ["c", "cn", "e", "en"] if x in clk_s_params])
            .replace("cn_i", "~cke_n_i")
            .replace("en_i", "~en_n_i")
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
                "descr": "Port parameters are passed to if_gen interfaces to generate different interfaces based on the parameters.",
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
                    "params": port_params["clk_en_rst_s"],
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
