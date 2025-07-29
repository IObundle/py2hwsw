#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    ios.py: build Verilog module IO and documentation
#


def generate_ports(core):
    """Generate verilog code with ports of this module.
    returns: Generated verilog code
    """
    lines = []
    for port_idx, port in enumerate(core.ports):
        lines.append("    " + port.get_verilog_port())

    # Remove comma from last interface line
    if lines:
        i = -1
        while lines[i].startswith("`endif") or lines[i].startswith("    // "):
            i -= 1
        lines[i] = lines[i].replace(",", "", 1)

    return "".join(lines)
