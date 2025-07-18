# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    subblocks_gen.py: instantiate Verilog modules and generate their documentation
#

from latex import write_table

import iob_colors
from iob_wire import get_real_wire
from iob_port import port_obj_list_process
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
                block.name,
                block.description,
            ]
        )

    write_table(f"{out_dir}/subblocks", tex_table)


def generate_subblocks(core):
    """Generate verilog code with verilog instances of this module.
    returns: Generated verilog code
    """
    code = ""
    for api_instance in core.subblocks:
        instance = convert2internal(api_instance)
        if not instance.instantiate:
            continue

        params_str = ""
        if instance.parameters:
            params_str = f"""#(
{param_gen.generate_inst_params(instance)}\
    ) """

        code += f"""\
        // {instance.description}
        {instance.name} {params_str}{instance.name} (
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
    """Returns a multi-line string with all port's wires connections
    for the given Verilog instance.
    """
    instance_portmap = ""

    # Iterate over all ports of the instance
    for api_portmap in instance.portmap_connections:
        portmap = convert2internal(api_portmap)

        portmap.validate_attributes()

        port = find_obj_in_list(
            [convert2internal(i) for i in core.ports], portmap.port, process_func=port_obj_list_process
        )
        if not port:
            fail_with_msg(
                f"Port '{portmap.port}' not found in instance '{instance.name}'!"
            )

        e_connect = find_obj_in_list(
            [convert2internal(i) for i in core.buses], portmap.e_connect
        ) or find_obj_in_list(
            [convert2internal(i) for i in core.ports], portmap.e_connect, process_func=port_obj_list_process
        )
        if not e_connect:
            fail_with_msg(
                f"Bus/Port '{portmap.e_connect}' not found in core '{core.name}'!"
            )

        # If port has 'doc_only' attribute set to True, skip it
        if port.doc_only:
            continue

        # If one of the ports is not a standard inferface, check if the number of wires is the same
        if not port.interface or not e_connect.interface:
            newlinechar = "\n"
            assert len(port.wires) == len(
                e_connect.wires
            ), f"""{iob_colors.FAIL}Port '{port.name}' of instance '{instance.name}' has different number of wires compared to external connection '{port.e_connect.name}'!
Port '{port.name}' has the following wires:
{newlinechar.join("- " + get_real_wire(port).name for port in port.wires)}

External connection '{get_real_wire(e_connect).name}' has the following wires:
{newlinechar.join("- " + get_real_wire(port).name for port in e_connect.wires)}
{iob_colors.ENDC}
"""

        # Is this still possible? I think iob_port.wires may only contain iob_wire objects
        # # If port has only non-iob wires, skip it
        # if not any(isinstance(port_wire, iob_wire) for port_wire in port.wires):
        #     continue

        # If port has a description, add it to the portmap
        if port.descr and not port.doc_only:
            instance_portmap += f"        // {port.name} port: {port.descr}\n"

        # Handle ports connected to constants
        if isinstance(e_connect, str):
            if "z" in e_connect.lower():
                instance_portmap += f"        .{port.wires[0].name}(),\n"
            else:
                instance_portmap += f"        .{port.wires[0].name}({e_connect}),\n"
            continue

        # Connect individual wires
        for idx, api_port_wire in enumerate(port.wires):
            port_wire = convert2internal(api_port_wire)
            # Is this still possible? Port should only contain iob_wires objects
            # # Skip wires that are not iob_wires
            # if not isinstance(port_wire, iob_wire):
            #     continue
            port_name = port_wire.name

            # If both ports are standard interfaces, connect by name
            if port.interface and e_connect.interface:
                # Remove prefix and suffix from port name
                port_name = port_name.replace(port.interface.prefix, "", 1)[:-2]
                for api_e_wire in e_connect.wires:
                    e_wire = convert2internal(api_e_wire)
                    real_e_wire = get_real_wire(e_wire)
                    e_wire_name = real_e_wire.name
                    # Remove prefix and suffix from external wire name
                    if e_wire_name[-2:] in ["_o", "_i"]:
                        e_wire_name = e_wire_name[:-2]
                    e_wire_name = e_wire_name.replace(e_connect.interface.prefix, "", 1)
                    if e_wire_name == port_name:
                        e_wire_name = real_e_wire.name
                        port_name = port_wire.name
                        break
                port_name = port_wire.name
            else:
                # If both ports are not standard interfaces, connect by index
                real_e_wire = get_real_wire(convert2internal(e_connect.wires[idx]))
                e_wire_name = real_e_wire.name

            # If the wire is a bit slice, get the name of the bit slice
            # and the name of the port (this overwrites the previous connection)
            for bit_slice in portmap.e_connect_bit_slices:
                if e_wire_name in bit_slice:
                    # Connection is not a bit_slice
                    if f"{port_wire.name}:" in bit_slice:
                        e_wire_name = bit_slice.split(":")[1]
                        port_name = port_wire.name
                    else:
                        # Connection is a bit slice
                        e_wire_name = bit_slice
                    break
                elif port_wire.name in bit_slice:
                    # Connection is not a bit_slice
                    if f"{port_wire.name}:" in bit_slice:
                        e_wire_name = bit_slice.split(":")[1]
                        port_name = port_wire.name
                    else:
                        # Connection is a bit slice
                        e_wire_name = bit_slice
                    break

            if e_wire_name.lower() == "z":
                # If the external wire is 'z', do not connect it
                instance_portmap += f"        .{port_name}(),\n"
            else:
                instance_portmap += f"        .{port_name}({e_wire_name}),\n"

    instance_portmap = instance_portmap[:-2] + "\n"  # Remove last comma

    return instance_portmap
