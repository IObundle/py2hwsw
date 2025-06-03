# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    subblocks_gen.py: instantiate Verilog modules and generate their documentation
#

from latex import write_table
import sys

import iob_colors
from iob_base import fail_with_msg
from iob_signal import get_real_signal, iob_signal
import param_gen


# Generate subblocks.tex file with TeX table of subblocks (Verilog modules instances)
def generate_subblocks_table_tex(subblocks, out_dir):
    subblocks_file = open(f"{out_dir}/subblocks.tex", "w")

    subblocks_file.write(
        "The Verilog modules in the top-level entity of the core are \
        described in the following tables. The table elements represent \
        the subblocks in the Block Diagram.\n"
    )

    for group in subblocks:
        subblocks_file.write(
            """
\\begin{xltabular}{\\textwidth}{|l|l|X|}

  \\hline
  \\rowcolor{iob-green}
  {\\bf Module} & {\\bf Name} & {\\bf Description}  \\\\ \\hline \\hline

  \\input """
            + group.name
            + """_subblocks_tab

  \\caption{"""
            + group.descr.replace("_", "\\_")
            + """}
\\end{xltabular}
\\label{"""
            + group.name
            + """_subblocks_tab:is}
"""
        )
        if group.doc_clearpage:
            subblocks_file.write("\\clearpage")

    subblocks_file.write("\\clearpage")
    subblocks_file.close()


# Generate TeX table of subblocks
def generate_subblocks_tex(subblocks, out_dir):
    # Create subblocks.tex file
    generate_subblocks_table_tex(subblocks, out_dir)

    # Create table for each group
    for group in subblocks:
        tex_table = []
        for block in group.blocks:
            if not block.instantiate:
                continue
            tex_table.append(
                [
                    block.name,
                    block.instance_name,
                    block.instance_description,
                ]
            )

        write_table(f"{out_dir}/{group.name}_subblocks", tex_table)


def generate_subblocks(core):
    """Generate verilog code with verilog instances of this module.
    returns: Generated verilog code
    """
    code = ""
    for group in core.subblocks:
        for instance in group.blocks:
            if not instance.instantiate:
                continue
            # Open ifdef if conditional interface
            if instance.if_defined:
                code += f"`ifdef {instance.if_defined}\n"
            if instance.if_not_defined:
                code += f"`ifndef {instance.if_not_defined}\n"

            params_str = ""
            if instance.parameters:
                params_str = f"""#(
{param_gen.generate_inst_params(instance)}\
    ) """

            code += f"""\
        // {instance.instance_description}
        {instance.name} {params_str}{instance.instance_name} (
    {get_instance_port_connections(instance)}\
        );

    """
            # Close ifdef if conditional interface
            if instance.if_defined or instance.if_not_defined:
                code += "`endif\n"

    return code


def generate_subblocks_snippet(core):
    """Write verilog snippet ('.vs' file) with subblocks of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_subblocks(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_subblocks.vs", "w+") as f:
        f.write(code)


def get_instance_port_connections(instance):
    """Returns a multi-line string with all port's signals connections
    for the given Verilog instance.
    """
    instance_portmap = ""

    # Iterade over all ports of the instance
    for port_idx, port in enumerate(instance.ports):
        # If port has 'doc_only' attribute set to True, skip it
        if port.doc_only:
            continue

        # Check if there are connections for this instance
        assert (
            port.e_connect
        ), f"{iob_colors.FAIL}Port '{port.name}' of instance '{instance.name}' is not connected!{iob_colors.ENDC}"

        # If one of the ports is not a standard inferface, check if the number of signals is the same
        if not port.interface or not port.e_connect.interface:
            newlinechar = "\n"
            assert len(port.signals) == len(
                port.e_connect.signals
            ), f"""{iob_colors.FAIL}Port '{port.name}' of instance '{instance.name}' has different number of signals compared to external connection '{port.e_connect.name}'!
Port '{port.name}' has the following signals:
{newlinechar.join("- " + get_real_signal(port).name for port in port.signals)}

External connection '{get_real_signal(port.e_connect).name}' has the following signals:
{newlinechar.join("- " + get_real_signal(port).name for port in port.e_connect.signals)}
{iob_colors.ENDC}
"""

        # If port has only non-iob signals, skip it
        if not any(isinstance(port_signal, iob_signal) for port_signal in port.signals):
            continue

        # If port has a description, add it to the portmap
        if port.descr and not port.doc_only:
            instance_portmap += f"        // {port.name} port: {port.descr}\n"

        if isinstance(port.e_connect, str):
            if "z" in port.e_connect.lower():
                instance_portmap += f"        .{port.signals[0].name}(),\n"
            else:
                instance_portmap += (
                    f"        .{port.signals[0].name}({port.e_connect}),\n"
                )
            continue
        # Connect individual signals
        for idx, port_signal in enumerate(port.signals):
            # Skip signals that are not iob_signals
            if not isinstance(port_signal, iob_signal):
                continue
            port_name = port_signal.name

            # If both ports are standard interfaces, connect by name
            if port.interface and port.e_connect.interface:
                # Remove prefix and suffix from port name
                port_name = port_name.replace(port.interface.prefix, "", 1)[:-2]
                for e_signal in port.e_connect.signals:
                    real_e_signal = get_real_signal(e_signal)
                    e_signal_name = real_e_signal.name
                    # Remove prefix and suffix from external signal name
                    if e_signal_name[-2:] in ["_o", "_i"]:
                        e_signal_name = e_signal_name[:-2]
                    e_signal_name = e_signal_name.replace(
                        port.e_connect.interface.prefix, "", 1
                    )
                    if e_signal_name == port_name:
                        e_signal_name = real_e_signal.name
                        port_name = port_signal.name
                        break
                port_name = port_signal.name
            else:
                # If both ports are not standard interfaces, connect by index
                real_e_signal = get_real_signal(port.e_connect.signals[idx])
                e_signal_name = real_e_signal.name

            # If the signal is a bit slice, get the name of the bit slice
            # and the name of the port (this overwrites the previous connection)
            for bit_slice in port.e_connect_bit_slices:
                if e_signal_name in bit_slice:
                    # Connection is not a bit_slice
                    if f"{port_signal.name}:" in bit_slice:
                        e_signal_name = bit_slice.split(":")[1]
                        port_name = port_signal.name
                    else:
                        # Connection is a bit slice
                        e_signal_name = bit_slice
                    break
                elif port_signal.name in bit_slice:
                    # Connection is not a bit_slice
                    if f"{port_signal.name}:" in bit_slice:
                        e_signal_name = bit_slice.split(":")[1]
                        port_name = port_signal.name
                    else:
                        # Connection is a bit slice
                        e_signal_name = bit_slice
                    break

            instance_portmap += f"        .{port_name}({e_signal_name}),\n"

    instance_portmap = instance_portmap[:-2] + "\n"  # Remove last comma

    return instance_portmap
