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


def generate_ports_snippet(core):
    """Write verilog snippet ('.vs' file) with ports of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_ports(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_io.vs", "w+") as f:
        f.write(code)
