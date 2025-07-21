# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import (
    fail_with_msg,
    find_obj_in_list,
    validate_verilog_const,
)
import iob_colors
from iob_wire import get_real_wire, iob_wire_reference
from iob_bus import iob_bus

from api_base import internal_api_class


@internal_api_class("user_api.draft_api", "iob_portmap")
@dataclass
class iob_portmap:
    """Describes an IO portmap connection."""

    def validate_attributes(self):
        if not self.port_name:
            fail_with_msg("Port is not specified", ValueError)
        if not self.e_connect:
            fail_with_msg(f"Port '{self.port_name}' is not connected!", ValueError)

        # TODO: validate if port and external buses really exist.
        pass

    # NOTE: THis connect_external already performs validation (including search for external bus (that may be non-existent).
    # We should probably only call this with `validate_attributes()`
    def connect_external(self, bus, bit_slices={}):
        """Connects the port to an external bus
        Verifies that the bus is compatible with the port
        :param iob_bus bus: external bus
        :param list bit_slices: bit slices of wires in bus
        """
        # bus must be iob_bus or str
        if isinstance(bus, str):
            if len(self.port.wires) != 1:
                fail_with_msg(
                    f"{iob_colors.FAIL}Port '{self.port.name}' has more than one wire but is connected to one constant value '{self.e_connect}'!{iob_colors.ENDC}",
                    ValueError,
                )
            else:
                validate_verilog_const(
                    value=bus, direction=self.port.wires[0].direction
                )
        elif isinstance(bus, iob_bus):
            if self.port.interface and bus.interface:
                if type(self.port.interface) == type(bus.interface):
                    for wire in self.port.wires:
                        # If it is a wire reference, get the real wire
                        if isinstance(wire, iob_wire_reference):
                            wire = get_real_wire(wire)
                        search_name = wire.name.replace(
                            self.port.interface.prefix, bus.interface.prefix, 1
                        )
                        if self.port.name[-2] != bus.name[-2]:
                            # Swap the suffixes if the port is a master/slave port
                            if bus.name[-2:] in ["_s", "_m"]:
                                if search_name[-2:] == "_i":
                                    search_name += search_name[:-2] + "_o"
                                else:
                                    search_name += search_name[:-2] + "_i"
                            else:
                                search_name = search_name[:-2]

                        e_wire = find_obj_in_list(bus.wires, search_name, get_real_wire)
                        if not e_wire:
                            if not any(
                                [
                                    f"{get_real_wire(wire).name}:" in bit_slice
                                    for bit_slice in bit_slices
                                ]
                            ):
                                newlinechar = "\n"
                                fail_with_msg(
                                    f"Port '{self.port.name}' wire '{wire.name}' not connected to external bus '{bus.name}'!\n"
                                    f"Port '{self.port.name}' has the following wires:\n"
                                    f"{newlinechar.join('- ' + get_real_wire(wire).name for wire in self.port.wires)}\n"
                                    f"External connection '{bus.name}' has the following wires:\n"
                                    f"{newlinechar.join('- ' + get_real_wire(wire).name for wire in bus.wires)}\n",
                                    ValueError,
                                )
                elif len(self.port.wires) != len(bus.wires):
                    newlinechar = "\n"
                    fail_with_msg(
                        f"Port '{self.port.name}' has different number of wires compared to external connection '{bus.name}'!\n"
                        f"Port '{self.port.name}' has the following wires:\n"
                        f"{newlinechar.join('- ' + get_real_wire(wire).name for wire in self.port.wires)}\n\n"
                        f"External connection '{bus.name}' has the following wires:\n"
                        f"{newlinechar.join('- ' + get_real_wire(wire).name for wire in bus.wires)}\n",
                        ValueError,
                    )
            elif len(self.port.wires) != len(bus.wires):
                newlinechar = "\n"
                fail_with_msg(
                    f"Port '{self.port.name}' has different number of wires compared to external connection '{bus.name}'!\n"
                    f"Port '{self.port.name}' has the following wires:\n"
                    f"{newlinechar.join('- ' + get_real_wire(wire).name for wire in self.port.wires)}\n\n"
                    f"External connection '{bus.name}' has the following wires:\n"
                    f"{newlinechar.join('- ' + get_real_wire(wire).name for wire in bus.wires)}",
                    ValueError,
                )
            else:
                for p, w in zip(self.port.wires, bus.wires):
                    w = get_real_wire(w)
                    if "'" in w.name or w.name.lower() == "z":
                        validate_verilog_const(value=w.name, direction=p.direction)
        else:
            fail_with_msg(
                f"Invalid bus type! {bus}. Must be iob_bus or str",
                TypeError,
            )

        self.e_connect = bus
        self.e_connect_bit_slices = bit_slices


def get_portmap_port(portmap):
    """Given a portmap reference, return the associated port"""
    port = None
    if isinstance(portmap, iob_portmap):
        port = portmap.port
    return port


#
# API methods
#


def portmap_from_dict(portmap_dict):
    portmap_list = []
    for port_name, connection in portmap_dict.items():

        # Extract external bus and bit slices from connection
        bit_slices = []
        if type(connection) is str:
            external_bus_name = connection
        elif type(connection) is tuple:
            external_bus_name = connection[0]
            bit_slices = connection[1]
            if type(bit_slices) is not list:
                fail_with_msg(
                    f"Second element of tuple must be a list of bit slices/connections: {connection}"
                )
        else:
            fail_with_msg(f"Invalid connection value: {connection}")

        # Create portmap and add to list
        portmap = iob_portmap(
            port_name=port_name,
            e_connect=external_bus_name,
            e_connect_bit_slices=bit_slices,
        )
        portmap_list.append(portmap)

    return portmap_list


def portmap_from_text(portmap_text):
    portmap_dict = {}
    # TODO: parse short notation text
    return iob_portmap(**portmap_dict)
