#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    ios.py: build Verilog module IO and documentation
#
from latex import write_table
import os

import interfaces
from iob_signal import iob_signal


def reverse_port(port_type):
    if port_type == "input":
        return "output"
    else:
        return "input"


def generate_ports(core):
    """Generate verilog code with ports of this module.
    returns: Generated verilog code
    """
    lines = []
    for port_idx, port in enumerate(core.ports):
        # If port has 'doc_only' attribute set to True, skip it
        if port.doc_only:
            continue

        # Open ifdef if conditional interface
        if port.if_defined:
            lines.append(f"`ifdef {port.if_defined}\n")
        if port.if_not_defined:
            lines.append(f"`ifndef {port.if_not_defined}\n")

        lines.append(f"    // {port.name}: {port.descr}\n")

        for signal_idx, signal in enumerate(port.signals):
            if isinstance(signal, iob_signal):
                if signal.get_verilog_port():
                    lines.append("    " + signal.get_verilog_port())

        # Close ifdef if conditional interface
        if port.if_defined or port.if_not_defined:
            lines.append("`endif\n")

    # Remove comma from last port line
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

    for port_idx, port in enumerate(core.ports):
        # If port has 'doc_only' attribute set to True, skip it
        if port.doc_only:
            continue
        # Also generate snippets for all interface subtypes (portmaps, tb_portmaps, wires, ...)
        # Note: This is only used by manually written verilog modules.
        #       May not be needed in the future.
        if port.interface:
            port.interface.gen_all_vs_files()

            # move all .vs files from current directory to out_dir
            for file in os.listdir("."):
                if file.endswith(".vs"):
                    os.rename(file, f"{out_dir}/{file}")


# Generate if.tex file with list TeX tables of IOs
def generate_if_tex(ports, out_dir):
    if_file = open(f"{out_dir}/if.tex", "w")

    if_file.write(
        """The interface signals of the core are described in the following tables.
Note that the ouput signals are registered in the core, while the input signals are not."""
    )

    for port in ports:
        if_file.write(
            """
\\begin{xltabular}{\\textwidth}{|l|l|r|X|}

  \\hline
  \\rowcolor{iob-green}
  {\\bf Name} & {\\bf Direction} & {\\bf Width} & {\\bf Description}  \\\\ \\hline \\hline

  \\input """
            + port.name
            + """_if_tab

  \\caption{"""
            + port.descr.replace("_", "\\_")
            + """}
\\end{xltabular}
\\label{"""
            + port.name
            + """_if_tab:is}
"""
        )
        if port.doc_clearpage:
            if_file.write("\\clearpage")

    if_file.close()


# Generate TeX tables of IOs
def generate_ios_tex(ports, out_dir):
    # Create if.tex file
    generate_if_tex(ports, out_dir)

    for port in ports:
        tex_table = []
        # Interface is not standard, read ports
        for signal in port.signals:
            if isinstance(signal, iob_signal):
                tex_table.append(
                    [
                        signal.name,
                        signal.direction,
                        signal.width,
                        signal.descr,
                    ]
                )

        write_table(f"{out_dir}/{port.name}_if", tex_table)
