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
    for port in attrs["ports"]:
        if isinstance(port["signals"], dict):
            if port["signals"]["type"] in mem_if_names:
                wire = copy.deepcopy(port)
                mwrap_wires.append(wire)
            else:
                mwrap_ports.append(port)
        else:
            mwrap_ports.append(port)

    attributes_dict["ports"] = mwrap_ports

    attributes_dict["wires"] = mwrap_wires

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
        if wire["signals"]["prefix"]:
            prefix_str = wire["signals"]["prefix"]
        else:
            prefix_str = wire["name"] + '_'
        attributes_dict["subblocks"].append(
            {
                "core_name": f"iob_{wire['signals']['type']}",
                "instance_name": f"{prefix_str}_mem",
                "parameters": {
                    "DATA_W": f"{prefix_str.upper()}_DATA_W",
                    "ADDR_W": f"{prefix_str.upper()}_ADDR_W",
                    "HEXFILE": f"{prefix_str.upper()}_HEXFILE",
                },
                "connect": {
                    f"{wire['signals']['type']}_s": wire["name"],
                }
            }
        )

    if "superblocks" in attrs:
        attributes_dict["superblocks"] = attrs["superblocks"]

    return attributes_dict
