#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    wire_gen.py: build Verilog module wires
#
import if_gen
import os
from iob_signal import iob_signal


def generate_wires(core):
    """Generate verilog code with wires of this module.
    returns: Generated verilog code
    """
    code = ""
    for wire in core.wires:
        # Open ifdef if conditional interface
        if wire.if_defined:
            code += f"`ifdef {wire.if_defined}\n"
        if wire.if_not_defined:
            code += f"`ifndef {wire.if_not_defined}\n"

        signals_code = ""
        for signal in wire.signals:
            if isinstance(signal, iob_signal):
                if signal.get_verilog_wire():
                    signals_code += "    " + signal.get_verilog_wire()
        if signals_code:
            # Add description for the wire if it is not the default one
            if wire.descr != "" and wire.descr != "Default description":
                code += f"// {wire.descr}\n"
            code += signals_code

        # Close ifdef if conditional interface
        if wire.if_defined or wire.if_not_defined:
            code += "`endif\n"

    return code


def generate_wires_snippet(core):
    """Write verilog snippet ('.vs' file) with wires of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_wires(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_wires.vs", "w+") as f:
        f.write(code)

    for wire in core.wires:
        # Generate the specific interface snippet as well
        # Note: This is only used by manually written verilog modules.
        #       May not be needed in the future.
        if wire.interface:
            if_gen.gen_wires(wire.interface)

            # move all .vs files from current directory to out_dir
            for file in os.listdir("."):
                if file.endswith(".vs"):
                    os.rename(file, f"{out_dir}/{file}")
