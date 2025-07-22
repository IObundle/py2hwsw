# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import (
    fail_with_msg,
    find_obj_in_list,
    validate_verilog_const,
    empty_list,
)
import iob_colors
from iob_wire import get_real_wire, iob_wire_reference
from iob_bus import iob_bus


@dataclass
class iob_portmap:
    """
    Class that represents a portmap attribute.

    Attributes:
        e_connect (iob_bus): Identifier name of external bus that connects this port
        e_connect_bit_slices (list): List of bit slices for external connections.
        port (str): IDentifier name of port associated with portmap
    """

    e_connect: iob_bus | None = None
    e_connect_bit_slices: list[str] = empty_list()
    port: str = None

    def validate_attributes(self):
        if not self.port:
            fail_with_msg("Port is not specified", ValueError)
        if not self.e_connect:
            fail_with_msg(f"Port '{self.port}' is not connected!", ValueError)

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
# Other Py2HWSW interface methods
#


def create_portmap_from_dict(portmap_dict):
    """
    Function to create iob_portmap object from dictionary attributes.

    Attributes:
        portmap_dict (dict): dictionary with values to initialize attributes of iob_portmap object.
            Dictionary format:
            {
                "port1_name": "external_connection1_name",
                "port2_name": "external_connection2_name",
                "port3_name": ("external_connection3_name", ["bit_slice_1", "bit_slice_2", ...]),
            }
            Dictionary element to attribute mapping:
            port1_name -> iob_portmap.port
            external_connection1_name -> iob_portmap.e_connect
            ["bit_slice_1", "bit_slice_2", ...] -> iob_portmap.e_connect_bit_slices

            Bit slices may perform multiple functions:
            - Slice bits from a wire that is being connected.
              For example, if we have a wire (iob_addr_wire) with 32 bits, from a bus (iob_bus_bus), and we want to connect it to a port (iob_bus_port) that only accepts an address of 8 bits, we could use:
              "iob_bus_port": ("iob_bus_bus", ["iob_addr_wire[7:0]"]),
            - Connect extra wires that do not exist in the bus.
              For example, if we have a wire (independent_iob_data_wire) that is not included in the bus (iob_bus_bus), but exists in the port (iob_bus_port), we could use:
              "iob_bus_port": ("iob_bus_bus", ["iob_data_wire_i: independent_iob_data_wire"]),
              If we didn't have the independent_iob_data_wire, we could instead connect that port's wire to a constant value or high impedance, like so:
              "iob_bus_port": ("iob_bus_bus", ["iob_data_wire_i: 'b1"]),
              "iob_bus_port": ("iob_bus_bus", ["iob_data_wire_i: 'bz"]),

              # FIXME: For some reason, connecting extra wires with bit slices only works for connections between ports and buses that have standard interfaces! Not sure why its implemented this way: https://github.com/IObundle/py2hwsw/blob/0679fc64576380c19be96567efb5093667eeb9fd/py2hwsw/scripts/block_gen.py#L121
              # Also, I'm not sure we can connect them to constants/high impedance.
              # It seems to be possible to connect ports to constants like so: https://github.com/IObundle/py2hwsw/pull/236



    Returns:
        list[iob_portmap]: List of iob_portmap objects
    """
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
            port=port_name,
            e_connect=external_bus_name,
            e_connect_bit_slices=bit_slices,
        )
        portmap_list.append(portmap)

    return portmap_list


def create_portmap_from_text(portmap_text):
    """
    Function to create iob_portmap object from short notation text.

    Attributes:
        portmap_text (str): Short notation text. Object attributes are specified using the following format:
            TODO

    Returns:
        iob_portmap: iob_portmap object
    """
    portmap_dict = {}
    # TODO: parse short notation text
    return iob_portmap(**portmap_dict)
