#!/usr/bin/env python3
#
#    ios.py: build Verilog module IO and documentation
#

from latex import write_table
import os

import if_gen


def reverse_port(port_type):
    if port_type == "input":
        return "output"
    else:
        return "input"


def generate_ports(core):
    out_dir = core.build_dir + "/hardware/src"

    lines = []
    for port_idx, port in enumerate(core.ports):
        # If port has 'doc_only' attribute set to True, skip it
        if port.doc_only:
            continue

        # Open ifdef if conditional interface
        if port.if_defined:
            lines.append(f"`ifdef {core.name.upper()}_{port.if_defined}\n")

        for signal_idx, signal in enumerate(port.signals):
            is_last_signal = (
                port_idx == len(core.ports) - 1 and signal_idx == len(port.signals) - 1
            )
            lines.append("    " + signal.get_verilog_port(comma=not is_last_signal))

        # Close ifdef if conditional interface
        if port.if_defined:
            lines.append("`endif\n")

        # Also generate snippets for all interface subtypes (portmaps, tb_portmaps, wires, ...)
        # Note: This is only used by manually written verilog modules.
        #       May not be needed in the future.
        if port.interface:
            if_gen.gen_if(port.interface)

            # move all .vs files from current directory to out_dir
            for file in os.listdir("."):
                if file.endswith(".vs"):
                    os.rename(file, f"{out_dir}/{file}")

    f_io = open(f"{out_dir}/{core.name}_io.vs", "w+")
    f_io.writelines(lines)
    f_io.close()


# Generate if.tex file with list TeX tables of IOs
def generate_if_tex(ports, out_dir):
    if_file = open(f"{out_dir}/if.tex", "w")

    if_file.write(
        "The interface signals of the core are described in the following tables.\n"
    )

    for port in ports:
        if_file.write(
            """
\\begin{table}[H]
  \\centering
  \\begin{tabularx}{\\textwidth}{|l|l|r|X|}

    \\hline
    \\rowcolor{iob-green}
    {\\bf Name} & {\\bf Direction} & {\\bf Width} & {\\bf Description}  \\\\ \\hline \\hline

    \\input """
            + port.name
            + """_if_tab

  \\end{tabularx}
  \\caption{"""
            + port.descr.replace("_", "\\_")
            + """}
  \\label{"""
            + port.name
            + """_if_tab:is}
\\end{table}
"""
        )

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
            tex_table.append(
                [
                    signal.name,
                    signal.direction,
                    signal.width,
                    signal.descr,
                ]
            )

        write_table(f"{out_dir}/{port.name}_if", tex_table)
