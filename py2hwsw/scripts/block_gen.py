# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    subblocks_gen.py: instantiate Verilog modules and generate their documentation
#

from latex import write_table

import iob_colors
from iob_signal import get_real_signal
import param_gen
from api_base import convert2internal
from iob_base import fail_with_msg, find_obj_in_list


# Generate subblocks.tex file with TeX table of subblocks (Verilog modules instances)
def generate_subblocks_table_tex(subblocks, out_dir):
    subblocks_file = open(f"{out_dir}/subblocks.tex", "w")

    subblocks_file.write(
        "The Verilog modules in the top-level entity of the core are \
        described in the following tables. The table elements represent \
        the subblocks in the Block Diagram.\n"
    )

    subblocks_file.write(
        """
\\begin{xltabular}{\\textwidth}{|l|l|X|}

  \\hline
  \\rowcolor{iob-green}
  {\\bf Module} & {\\bf Name} & {\\bf Description}  \\\\ \\hline \\hline

  \\input subblocks_tab

  \\caption{Table of subblocks in the core.}
\\end{xltabular}
\\label{subblocks_tab:is}
"""
    )

    subblocks_file.write("\\clearpage")
    subblocks_file.close()


# Generate TeX table of subblocks
def generate_subblocks_tex(subblocks, out_dir):
    # Create subblocks.tex file
    generate_subblocks_table_tex(subblocks, out_dir)

    # Create table for subblocks
    tex_table = []
    for block in subblocks:
        if not block.instantiate:
            continue
        tex_table.append(
            [
                block.name,
                block.instance_name,
                block.instance_description,
            ]
        )

    write_table(f"{out_dir}/subblocks", tex_table)


def generate_subblocks(core):
    """Generate verilog code with verilog instances of this module.
    returns: Generated verilog code
    """
    code = ""
    for instance in core.subblocks:
        instance = convert2internal(instance)
        if not instance.instantiate:
            continue

        params_str = ""
        if instance.parameters:
            params_str = f"""#(
{param_gen.generate_inst_params(instance)}\
    ) """

        code += f"""\
        // {instance.instance_description}
        {instance.name} {params_str}{instance.instance_name} (
    {get_instance_port_connections(core, instance)}\
        );

    """

    return code


def generate_subblocks_snippet(core):
    """Write verilog snippet ('.vs' file) with subblocks of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_subblocks(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_subblocks.vs", "w+") as f:
        f.write(code)


def get_instance_port_connections(core, instance):
    """Returns a multi-line string with all port's signals connections
    for the given Verilog instance.
    """
    instance_portmap = ""

    # Iterate over all ports of the instance
    for portmap in instance.portmap_connections:
        portmap = convert2internal(portmap)

        portmap.validate_attributes()

        port = find_obj_in_list(
            [convert2internal(i) for i in instance.ports], portmap.port
        )
        if not port:
            fail_with_msg(
                f"Port '{portmap.port}' not found in instance '{instance.name}'!"
            )

        e_connect = find_obj_in_list(
            [convert2internal(i) for i in core.wires], portmap.e_connect
        ) or find_obj_in_list(
            [convert2internal(i) for i in core.ports], portmap.e_connect
        )
        if not e_connect:
            fail_with_msg(
                f"Wire/Port '{portmap.e_connect}' not found in core '{core.name}'!"
            )

        # If port has 'doc_only' attribute set to True, skip it
        if port.doc_only:
            continue

        # If one of the ports is not a standard inferface, check if the number of signals is the same
        if not port.interface or not e_connect.interface:
            newlinechar = "\n"
            assert len(port.signals) == len(
                e_connect.signals
            ), f"""{iob_colors.FAIL}Port '{port.name}' of instance '{instance.name}' has different number of signals compared to external connection '{port.e_connect.name}'!
Port '{port.name}' has the following signals:
{newlinechar.join("- " + get_real_signal(port).name for port in port.signals)}

External connection '{get_real_signal(e_connect).name}' has the following signals:
{newlinechar.join("- " + get_real_signal(port).name for port in e_connect.signals)}
{iob_colors.ENDC}
"""

        # Is this still possible? I think iob_port.signals may only contain iob_signal objects
        # # If port has only non-iob signals, skip it
        # if not any(isinstance(port_signal, iob_signal) for port_signal in port.signals):
        #     continue

        # If port has a description, add it to the portmap
        if port.descr and not port.doc_only:
            instance_portmap += f"        // {port.name} port: {port.descr}\n"

        # Handle ports connected to constants
        if isinstance(e_connect, str):
            if "z" in e_connect.lower():
                instance_portmap += f"        .{port.signals[0].name}(),\n"
            else:
                instance_portmap += f"        .{port.signals[0].name}({e_connect}),\n"
            continue

        # Connect individual signals
        for idx, port_signal in enumerate(port.signals):
            port_signal = convert2internal(port_signal)
            # Is this still possible? Port should only contain iob_signals objects
            # # Skip signals that are not iob_signals
            # if not isinstance(port_signal, iob_signal):
            #     continue
            port_name = port_signal.name

            # If both ports are standard interfaces, connect by name
            if port.interface and e_connect.interface:
                # Remove prefix and suffix from port name
                port_name = port_name.replace(port.interface.prefix, "", 1)[:-2]
                for e_signal in e_connect.signals:
                    e_signal = convert2internal(e_signal)
                    real_e_signal = get_real_signal(e_signal)
                    e_signal_name = real_e_signal.name
                    # Remove prefix and suffix from external signal name
                    if e_signal_name[-2:] in ["_o", "_i"]:
                        e_signal_name = e_signal_name[:-2]
                    e_signal_name = e_signal_name.replace(
                        e_connect.interface.prefix, "", 1
                    )
                    if e_signal_name == port_name:
                        e_signal_name = real_e_signal.name
                        port_name = port_signal.name
                        break
                port_name = port_signal.name
            else:
                # If both ports are not standard interfaces, connect by index
                real_e_signal = get_real_signal(
                    convert2internal(e_connect.signals[idx])
                )
                e_signal_name = real_e_signal.name

            # If the signal is a bit slice, get the name of the bit slice
            # and the name of the port (this overwrites the previous connection)
            for bit_slice in portmap.e_connect_bit_slices:
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

            if e_signal_name.lower() == "z":
                # If the external signal is 'z', do not connect it
                instance_portmap += f"        .{port_name}(),\n"
            else:
                instance_portmap += f"        .{port_name}({e_signal_name}),\n"

    instance_portmap = instance_portmap[:-2] + "\n"  # Remove last comma

    return instance_portmap
