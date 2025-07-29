# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    subblocks_gen.py: instantiate Verilog modules and generate their documentation
#

from iob_port import iob_port
import param_gen
from iob_base import fail_with_msg, find_obj_in_list

port_obj_list_process = iob_port.port_obj_list_process


def generate_subblocks(core):
    """Generate verilog code with verilog instances of this module.
    returns: Generated verilog code
    """
    code = ""
    for instance in core.subblocks:
        if not instance.instantiate:
            continue

        params_str = ""
        if instance.parameters:
            params_str = f"""#(
{param_gen.generate_inst_params(instance)}\
    ) """

        code += f"""\
        // {instance.description}
        {instance.core.name} {params_str}{instance.name} (
    {get_instance_port_connections(core, instance)}\
        );

    """

    return code


def get_instance_port_connections(core, instance):
    """Returns a multi-line string with all port's wires connections
    for the given Verilog instance.
    """
    instance_portmap = ""

    # Iterate over all ports of the instance
    for portmap in instance.portmap_connections:

        # connect portmap port_name name to matching core port
        portmap.connect_port(instance.core.ports)

        port = portmap.port
        if not port:
            fail_with_msg(
                f"Port '{portmap.port}' not found in instance '{instance.name}'!"
            )

        # search for matching connection in core wires, and ports
        e_connect = (
            find_obj_in_list(core.wires, portmap.e_connect)
            or find_obj_in_list(
                core.ports,
                portmap.e_connect,
                process_func=port_obj_list_process,
            )
        )
        if not e_connect:
            fail_with_msg(
                f"Bus/Port '{portmap.e_connect}' not found in core '{core.name}'!"
            )
        if isinstance(e_connect, iob_port):
            e_connect = e_connect.wire

        # If port has 'doc_only' attribute set to True, skip it
        if port.doc_only:
            continue

        # If port has a description, add it to the portmap
        if port.wire.descr and not port.doc_only:
            instance_portmap += f"        // {port.wire.name} port: {port.wire.descr}\n"

        # Handle ports connected to constants
        if isinstance(e_connect, str):
            if "z" in e_connect.lower():
                instance_portmap += f"        .{port.wire.name}(),\n"
            else:
                instance_portmap += f"        .{port.wire.name}({e_connect}),\n"
            continue

        e_wire_name = e_connect.name

        # If the wire is a bit slice, get the name of the bit slice
        # and the name of the port (this overwrites the previous connection)
        for bit_slice in portmap.e_connect_bit_slices:
            if e_wire_name in bit_slice:
                # Connection is not a bit_slice
                if f"{port.wire.name}:" in bit_slice:
                    e_wire_name = bit_slice.split(":")[1]
                else:
                    # Connection is a bit slice
                    e_wire_name = bit_slice
                break
            elif port.wire.name in bit_slice:
                # Connection is not a bit_slice
                if f"{port.wire.name}:" in bit_slice:
                    e_wire_name = bit_slice.split(":")[1]
                else:
                    # Connection is a bit slice
                    e_wire_name = bit_slice
                break

        if e_wire_name.lower() == "z":
            # If the external wire is 'z', do not connect it
            instance_portmap += f"        .{port.wire.name}(),\n"
        else:
            instance_portmap += f"        .{port.wire.name}({e_wire_name}),\n"

    instance_portmap = instance_portmap[:-2] + "\n"  # Remove last comma

    return instance_portmap
