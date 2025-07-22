#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    bus_gen.py: build Verilog module buses
#
import os
from iob_wire import iob_wire


def generate_buses(core):
    """Generate verilog code with buses of this module.
    returns: Generated verilog code
    """
    code = ""
    for bus in core.buses:

        wires_code = ""
        for wire in bus.wires:
            if isinstance(wire, iob_wire):
                global_wire = wire.global_wire
                if global_wire:
                    wires_code += "    " + global_wire.get_verilog_bus()
        if wires_code:
            # Add description for the bus if it is not the default one
            if bus.descr != "" and bus.descr != "Default description":
                code += f"// {bus.descr}\n"
            code += wires_code

    return code


def generate_buses_snippet(core):
    """Write verilog snippet ('.vs' file) with buses of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_buses(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_buses.vs", "w+") as f:
        f.write(code)

    for bus in core.buses:
        # Generate the specific interface snippet as well
        # Note: This is only used by manually written verilog modules.
        #       May not be needed in the future.
        if bus.interface:
            bus.interface.gen_buses_vs_file()

            # move all .vs files from current directory to out_dir
            for file in os.listdir("."):
                if file.endswith(".vs"):
                    os.rename(file, f"{out_dir}/{file}")
