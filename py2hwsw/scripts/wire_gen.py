#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    bus_gen.py: build Verilog module buses
#
from iob_wire import iob_wire
from api_base import convert2internal


def generate_wires(core):
    """Generate verilog code with buses of this module.
    returns: Generated verilog code
    """
    code = ""
    for api_wire in core.wires:
        wires_code = ""
        wire = convert2internal(api_wire)
        if isinstance(wire, iob_wire):
            if wire:
                wires_code += "    " + wire.get_verilog_bus()
        if wires_code:
            # Add description for the wire if it is not the default one
            if wire.descr != "" and wire.descr != "Default description":
                code += f"// {wire.descr}\n"
            code += wires_code

    return code


def generate_wires_snippet(core):
    """Write verilog snippet ('.vs' file) with wires of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_wires(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_wires.vs", "w+") as f:
        f.write(code)
