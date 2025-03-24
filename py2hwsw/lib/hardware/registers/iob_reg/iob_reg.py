# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    port_params = (
        py_params_dict["port_params"]
        if "port_params" in py_params_dict
        else {"clk_en_rst_s": "cke_arst"}
    )
    assert "clk_en_rst_s" in port_params, "clk_en_rst_s port is missing"

    clk_s_params = [x for x in port_params["clk_en_rst_s"].split("_") if x != ""]

    clk_suff_dict = {
        "cke": "ce",
        "cken": "cen",
        "arst": "ar",
        "arstn": "arn",
    }

    sync_suff_dict = {
        "rst": "r",
        "rstn": "rn",
        "en": "e",
        "enn": "en",
    }

    clk_suffix = "".join([clk_suff_dict[x] for x in clk_s_params if x in clk_suff_dict])
    sync_suffix = "".join(
        [sync_suff_dict[x] for x in clk_s_params if x in sync_suff_dict]
    )

    reg_type = "iob_regn" if "n" in clk_s_params else "iob_reg"

    reg_name = "_".join(filter(lambda x: x != "", [reg_type, clk_suffix, sync_suffix]))

    rst_str = ""
    en_str = ""

    sensitivity_list = "negedge clk_i" if "n" in clk_s_params else "posedge clk_i"
    if "arst" in clk_s_params:
        sensitivity_list = f"{sensitivity_list}, posedge arst_i"
    elif "arstn" in clk_s_params:
        sensitivity_list = f"{sensitivity_list}, negedge arst_n_i"

    if any([x in clk_s_params for x in ["arst", "arstn", "rst", "rstn"]]):
        rst_con = (
            " | ".join(
                [
                    f"{x}_i"
                    for x in ["arst", "arstn", "rst", "rstn"]
                    if x in clk_s_params
                ]
            )
            .replace("arstn", "~arst_n")
            .replace("rstn", "~rst_n")
        )
        rst_str = (
            f"        if ({rst_con}) begin\n            data_o <= RST_VAL;\n        end"
        )

    if any([x in clk_s_params for x in ["cke", "cken", "en", "enn"]]):
        en_con = (
            " & ".join(
                [f"{x}_i" for x in ["cke", "cken", "en", "enn"] if x in clk_s_params]
            )
            .replace("cken", "~cke_n")
            .replace("enn", "~en_n")
        )
        en_str = f"{'else ' if rst_str != '' else '        '}if ({en_con}) begin\n            data_o <= data_i;\n        end"
    else:
        en_str = f"{'else begin' if rst_str != '' else '        '}\n            data_o <= data_i;\n        {'end' if rst_str != '' else ''}"

    attributes_dict = {
        "name": reg_name,
        "generate_hw": True,
        "description": f"Generated register module.",
        "python_parameters": {
            "name": "port_params",
            "val": port_params,
            "descr": "Port parameters are passed to if_gen interfaces to generate different interfaces based on the parameters.",
        },
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
