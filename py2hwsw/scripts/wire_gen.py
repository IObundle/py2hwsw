#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    bus_gen.py: build Verilog module buses
#
from iob_wire import iob_wire


def generate_wires(core):
    """Generate verilog code with buses of this module.
    returns: Generated verilog code
    """
    code = ""
    for wire in core.wires:
        wires_code = ""
        if isinstance(wire, iob_wire):
            if wire:
                wires_code += "    " + wire.get_verilog_wire()
        if wires_code:
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
