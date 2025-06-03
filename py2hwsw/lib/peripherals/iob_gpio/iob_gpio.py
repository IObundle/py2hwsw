# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import copy


def setup(py_params_dict):
    NAME = py_params_dict["name"] if "name" in py_params_dict else "iob_gpio"
    N_INPUTS = int(py_params_dict["n_inputs"]) if "n_inputs" in py_params_dict else 1
    N_OUTPUTS = int(py_params_dict["n_outputs"]) if "n_outputs" in py_params_dict else 1
    # Create a dedicated output for tristate (output enable) of each output port
    TRISTATE = (
        bool(py_params_dict["tristate"]) if "tristate" in py_params_dict else False
    )

    params = {
        "csr_if_widths": {"ADDR_W": 32, "DATA_W": 32},
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    attributes_dict = {
        "name": NAME,
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "32",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                # "val": "`IOB_GPIO_CSRS_ADDR_W",
                "val": "4",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "INPUT_GPIO_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "DATA_W",
                "descr": "Width of GPIO input ports",
            },
            {
                "name": "OUTPUT_GPIO_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "DATA_W",
                "descr": "Width of GPIO output ports",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
        ],
    }
    for idx in range(N_INPUTS):
        attributes_dict["ports"].append(
            {
                "name": "input_" + str(idx) + "_i",
                "descr": "",
                "signals": [
                    {
                        "name": "input_port_" + str(idx) + "_i",
                        "width": "INPUT_GPIO_W",
                        "descr": "Input interface " + str(idx),
                    },
                ],
            }
        )
    for idx in range(N_OUTPUTS):
        attributes_dict["ports"].append(
            {
                "name": "output_" + str(idx) + "_o",
                "descr": "",
                "signals": [
                    {
                        "name": "output_port_" + str(idx) + "_o",
                        "width": "OUTPUT_GPIO_W",
                        "descr": "Output interface " + str(idx),
                    },
                ],
            }
        )
        if TRISTATE:
            attributes_dict["ports"][-1]["signals"].append(
                {
                    "name": "output_enable_" + str(idx) + "_o",
                    "width": "OUTPUT_GPIO_W",
                    "descr": f"Output Enable interface bits can be used to tristate output {idx} on external module",
                },
            )
    verilog_snippet = ""
    verilog_snippet_generate = ""
    attributes_dict["wires"] = []
    # Create wires based on copy of ports
    for port in attributes_dict["ports"]:
        if not port["name"].startswith("input") and not port["name"].startswith(
            "output"
        ):
            continue
        wire = copy.deepcopy(port)
        # Remove port direction suffix
        wire["name"] = wire["name"][:-2]
        wire["signals"][0]["name"] = wire["signals"][0]["name"][:-2]
        # Set correct width for connection with csrs
        wire["signals"][0]["width"] = 32
        attributes_dict["wires"].append(wire)

        if port["name"].endswith("_i"):
            verilog_snippet += f"""
   assign {wire["signals"][0]["name"]}[INPUT_GPIO_W-1:0] = {port["signals"][0]["name"]};
"""
            verilog_snippet_generate += f"""
   assign {wire["signals"][0]["name"]}[32-1:INPUT_GPIO_W] = {{32-INPUT_GPIO_W{{1'b0}}}};
"""
        else:
            verilog_snippet += f"""
   assign {port["signals"][0]["name"]} = {wire["signals"][0]["name"]}[OUTPUT_GPIO_W-1:0];
"""

    regs = []
    reg_connections = {}
    # Create regs and reg connections for each input
    for idx in range(N_INPUTS):
        # Create Reg
        regs.append(
            {
                "name": "input_" + str(idx),
                "mode": "R",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "descr": "Value of GPIO input port " + str(idx),
            }
        )
        # Connect reg to port
        reg_connections["input_" + str(idx) + "_i"] = "input_" + str(idx)
    # Create regs and reg connections for each output
    for idx in range(N_OUTPUTS):
        # Create Regs
        regs.append(
            {
                "name": "output_" + str(idx),
                "mode": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "descr": "Value of GPIO output port " + str(idx),
            }
        )
        if TRISTATE:
            regs.append(
                {
                    "name": "output_enable_" + str(idx),
                    "mode": "W",
                    "n_bits": 32,
                    "rst_val": 0,
                    "log2n_items": 0,
                    "descr": f'32 bits: 1 bit for each bit in GPIO output {idx}. Bits with "1" are driven with output value, bits with "0" are in tristate.',
                }
            )
        # Connect regs to wires
        reg_connections["output_" + str(idx) + "_o"] = "output_" + str(idx)
        if TRISTATE:
            reg_connections["output_enable_" + str(idx) + "_o"] = (
                "output_enable_" + str(idx)
            )

    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_csrs",
            "instance_name": "iob_csrs",
            "instance_description": "Control/Status Registers",
            "csrs": [
                {
                    "name": "gpio",
                    "descr": "GPIO software accessible registers.",
                    "regs": regs,
                }
            ],
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # 'control_if_m' port connected automatically
                **reg_connections,
            },
        },
    ]
    verilog_snippet += f"""
   generate
      if (INPUT_GPIO_W < 32) begin : gen_if_input_less_than_32
        {verilog_snippet_generate}
      end
   endgenerate
"""
    attributes_dict["snippets"] = [{"verilog_code": verilog_snippet}]

    return attributes_dict
