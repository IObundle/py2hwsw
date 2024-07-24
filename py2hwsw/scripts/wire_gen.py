#!/usr/bin/env python3
#
#    wire_gen.py: build Verilog module wires
#

import if_gen
import os
from iob_signal import iob_signal


def generate_wires(core):
    out_dir = core.build_dir + "/hardware/src"

    f_wires = open(f"{out_dir}/{core.name}_wires.vs", "w+")

    for wire in core.wires:
        # Open ifdef if conditional interface
        if wire.if_defined:
            f_wires.write(f"`ifdef {core.name.upper()}_{wire.if_defined}\n")
        if wire.if_not_defined:
            f_wires.write(f"`ifndef {core.name.upper()}_{wire.if_not_defined}\n")

        f_wires.write(f"    // {wire.name}\n")

        for signal in wire.signals:
            if isinstance(signal, iob_signal):
                f_wires.write("    " + signal.get_verilog_wire())

        # Close ifdef if conditional interface
        if wire.if_defined or wire.if_not_defined:
            f_wires.write("`endif\n")

        # Generate the specific interface snippet as well
        # Note: This is only used by manually written verilog modules.
        #       May not be needed in the future.
        if wire.interface:
            if_gen.gen_wires(wire.interface)

            # move all .vs files from current directory to out_dir
            for file in os.listdir("."):
                if file.endswith(".vs"):
                    os.rename(file, f"{out_dir}/{file}")

    f_wires.close()
