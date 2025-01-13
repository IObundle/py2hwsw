# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import copy

def setup(py_params_dict):

    mem_if_names = py_params_dict["mem_if_names"]
    attrs = py_params_dict["instantiator"]

    attributes_dict = {
        "name": f"{attrs['name']}_mwrap",
        "generate_hw": True,
        "version": "0.1",
        "confs": attrs['confs'],
    }

    mwrap_wires = []
    mwrap_ports = []
    snippets = [{"verilog_code": ""}] 
    for port in attrs["ports"]:
        if isinstance(port["signals"], dict):
            if port["signals"]["type"] in mem_if_names:
                wire = copy.deepcopy(port)
                mwrap_wires.append(wire)
                snippet = f"    assign {wire['signals']['prefix']}clk = clk_i;\n"
                snippets[0]["verilog_code"] += snippet
            else:
                mwrap_ports.append(port)
        else:
            mwrap_ports.append(port)

    attributes_dict["ports"] = mwrap_ports

    attributes_dict["wires"] = mwrap_wires

    attributes_dict["snippets"] = snippets

    attributes_dict["subblocks"] = [
        {
            "core_name": attrs['name'],
            "instance_name": f"{attrs['name']}_inst",
            "instance_description": "Wrapped module",
            "parameters": {
                i["name"]: i["name"]
                for i in attrs["confs"]
                if i["type"] in ["P", "F"]
            },
            "connect": {
                i["name"]: i["name"] for i in attrs["ports"]
            },
        }
    ]

    for wire in mwrap_wires:
        attributes_dict["subblocks"].append(
            {
                "core_name": f"iob_{wire['signals']['type']}",
                "instance_name": f"{wire['signals']['prefix']}_mem",
                "connect": {
                    f"{wire['signals']['type']}_s": wire["name"],
                }
            }
        )

    if "superblocks" in attrs:
        attributes_dict["superblocks"] = attrs["superblocks"]

    return attributes_dict
