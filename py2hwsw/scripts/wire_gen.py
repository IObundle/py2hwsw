#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    bus_gen.py: build Verilog module buses
#
import interfaces
import os
from iob_signal import iob_signal
from api_base import convert2internal


def generate_buses(core):
    """Generate verilog code with buses of this module.
    returns: Generated verilog code
    """
    code = ""
    for bus in core.buses:
        bus = convert2internal(bus)

        signals_code = ""
        for signal in bus.signals:
            signal = convert2internal(signal)
            if isinstance(signal, iob_signal):
                if signal.get_verilog_bus():
                    signals_code += "    " + signal.get_verilog_bus()
        if signals_code:
            # Add description for the bus if it is not the default one
            if bus.descr != "" and bus.descr != "Default description":
                code += f"// {bus.descr}\n"
            code += signals_code

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
        bus = convert2internal(bus)
        # Generate the specific interface snippet as well
        # Note: This is only used by manually written verilog modules.
        #       May not be needed in the future.
        if bus.interface:
            bus.interface.gen_buses_vs_file()

            # move all .vs files from current directory to out_dir
            for file in os.listdir("."):
                if file.endswith(".vs"):
                    os.rename(file, f"{out_dir}/{file}")
