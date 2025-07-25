#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


class iob_reg(iob_core):
    """
    Class to represent a register module.
    It is configurable via iob_parameters.
    It supports the following control ports: clk, cke, arst, rst, en, anrst

    The reset polarity used will be based on the project-wide global variable 'reset_polarity'.
    """

    def __init__(self, port_params: dict = {"clk_en_rst_s": "c_a"}):
        """
        Args:
           port_params (dict): Dictionary of port parameters. Example format:
                               {
                                   "clk_en_rst_s": "c_a",
                               },
        """
        assert "clk_en_rst_s" in port_params, "clk_en_rst_s port is missing"

        reset_polarity = getattr(iob_globals(), "reset_polarity", "positive")

        clk_port_params = port_params["clk_en_rst_s"]

        if reset_polarity != "positive":
            port_params["clk_en_rst_s"] = port_params["clk_en_rst_s"].replace("a", "an")

        clk_s_params_list = [
            x for x in port_params["clk_en_rst_s"].split("_") if x != ""
        ]

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

        sensitivity_list = (
            "negedge clk_i" if "n" in clk_s_params_list else "posedge clk_i"
        )

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

        core_dictionary = {
            "name": reg_name,
            "generate_hw": True,
            "description": "Generated register module.",
            # FIXME: Will this be deprecated?
            # Should we store the values that we received via python parameters in this attribute? I think only use case would be for later reference or documentation.
            # "iob_parameters": [
            #     {
            #         "name": "port_params",
            #         "value": port_params,
            #         "descr": "Port parameters are passed to interfaces to generate different interfaces.",
            #     },
            # ],
            "version": "0.1",
            "confs": [
                {
                    "name": "DATA_W",
                    "descr": "Data bus width",
                    "kind": "P",
                    "value": "1",
                    "min_value": "NA",
                    "max_value": "NA",
                },
                {
                    "name": "RST_VAL",
                    "descr": "Reset value.",
                    "kind": "P",
                    "value": "{DATA_W{1'b0}}",
                    "min_value": "NA",
                    "max_value": "NA",
                },
            ],
            "ports": [
                {
                    "name": "clk_en_rst_s",
                    "descr": "Clock, clock enable and reset port (bus with multiple wires)",
                    "interface": {
                        "kind": "iob_clk",
                        "params": clk_port_params,
                    },
                },
                {
                    "name": "data_i",
                    "descr": "Data input port (single wire)",
                    "width": "DATA_W",
                },
                {
                    "name": "data_o",
                    "descr": "Data output port (single wire)",
                    "width": "DATA_W",
                    "isvar": True,
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

        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_reg_obj = iob_reg()
    iob_reg_obj.generate_build_dir()
