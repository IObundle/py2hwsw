# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field

from iob_base import (
    fail_with_msg,
    find_obj_in_list,
    validate_verilog_const,
)
import iob_colors
from iob_port import iob_port
from iob_signal import get_real_signal, iob_signal_reference
from iob_wire import iob_wire

from api_base import internal_api_class, convert2internal


@internal_api_class("user_api.api", "iob_portmap")
@dataclass
class iob_portmap:
    """Describes an IO portmap connection."""

    def validate_attributes(self):
        pass

    # NOTE: THis connect_external already performs validation (including search for external wire (that may be non-existent).
    # We should probably only call this with `validate_attributes()`
    def connect_external(self, wire, bit_slices={}):
        """Connects the port to an external wire
        Verifies that the wire is compatible with the port
        :param iob_wire wire: external wire
        :param list bit_slices: bit slices of signals in wire
        """
        # wire must be iob_wire or str
        if isinstance(wire, str):
            if len(self.port.signals) != 1:
                fail_with_msg(
                    f"{iob_colors.FAIL}Port '{self.port.name}' has more than one signal but is connected to one constant value '{self.e_connect}'!{iob_colors.ENDC}",
                    ValueError,
                )
            else:
                validate_verilog_const(
                    value=wire, direction=self.port.signals[0].direction
                )
        elif isinstance(wire, iob_wire):
            if self.port.interface and wire.interface:
                if type(self.port.interface) == type(wire.interface):
                    for signal in self.port.signals:
                        # If it is a signal reference, get the real signal
                        if isinstance(signal, iob_signal_reference):
                            signal = get_real_signal(signal)
                        search_name = signal.name.replace(
                            self.port.interface.prefix, wire.interface.prefix, 1
                        )
                        if self.port.name[-2] != wire.name[-2]:
                            # Swap the suffixes if the port is a master/slave port
                            if wire.name[-2:] in ["_s", "_m"]:
                                if search_name[-2:] == "_i":
                                    search_name += search_name[:-2] + "_o"
                                else:
                                    search_name += search_name[:-2] + "_i"
                            else:
                                search_name = search_name[:-2]

                        e_signal = find_obj_in_list(
                            wire.signals, search_name, get_real_signal
                        )
                        if not e_signal:
                            if not any(
                                [
                                    f"{get_real_signal(signal).name}:" in bit_slice
                                    for bit_slice in bit_slices
                                ]
                            ):
                                newlinechar = "\n"
                                fail_with_msg(
                                    f"Port '{self.port.name}' signal '{signal.name}' not connected to external wire '{wire.name}'!\n"
                                    f"Port '{self.port.name}' has the following signals:\n"
                                    f"{newlinechar.join('- ' + get_real_signal(signal).name for signal in self.port.signals)}\n"
                                    f"External connection '{wire.name}' has the following signals:\n"
                                    f"{newlinechar.join('- ' + get_real_signal(signal).name for signal in wire.signals)}\n",
                                    ValueError,
                                )
                elif len(self.port.signals) != len(wire.signals):
                    newlinechar = "\n"
                    fail_with_msg(
                        f"Port '{self.port.name}' has different number of signals compared to external connection '{wire.name}'!\n"
                        f"Port '{self.port.name}' has the following signals:\n"
                        f"{newlinechar.join('- ' + get_real_signal(signal).name for signal in self.port.signals)}\n\n"
                        f"External connection '{wire.name}' has the following signals:\n"
                        f"{newlinechar.join('- ' + get_real_signal(signal).name for signal in wire.signals)}\n",
                        ValueError,
                    )
            elif len(self.port.signals) != len(wire.signals):
                newlinechar = "\n"
                fail_with_msg(
                    f"Port '{self.port.name}' has different number of signals compared to external connection '{wire.name}'!\n"
                    f"Port '{self.port.name}' has the following signals:\n"
                    f"{newlinechar.join('- ' + get_real_signal(signal).name for signal in self.port.signals)}\n\n"
                    f"External connection '{wire.name}' has the following signals:\n"
                    f"{newlinechar.join('- ' + get_real_signal(signal).name for signal in wire.signals)}",
                    ValueError,
                )
            else:
                for p, w in zip(self.port.signals, wire.signals):
                    w = get_real_signal(w)
                    if "'" in w.name or w.name.lower() == "z":
                        validate_verilog_const(value=w.name, direction=p.direction)
        else:
            fail_with_msg(
                f"Invalid wire type! {wire}. Must be iob_wire or str",
                TypeError,
            )

        self.e_connect = wire
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


def portmap_from_dict(core, portmap_dict):
    core = convert2internal(core)
    portmap_list = []
    for port_name, connection in portmap_dict.items():
        # Get port from core's ports list
        port = find_obj_in_list([convert2internal(i) for i in core.ports], port_name)
        if not port:
            fail_with_msg(
                f"Port '{port_name}' not found in instance '{core.instance_name}' of module '{core.issuer.name}'!\n"
                f"Available ports:\n- "
                + "\n- ".join([port.name for port in core.ports])
            )

        # Extract external wire and bit slices from connection
        bit_slices = []
        if type(connection) is str:
            external_wire_name = connection
        elif type(connection) is tuple:
            external_wire_name = connection[0]
            bit_slices = connection[1]
            if type(bit_slices) is not list:
                fail_with_msg(
                    f"Second element of tuple must be a list of bit slices/connections: {connection}"
                )
        else:
            fail_with_msg(f"Invalid connection value: {connection}")

        # # Set wire as 'str' when connecting to constant/floating
        # # Otherwise, find wire
        # if "'" in external_wire_name or external_wire_name.lower() == "z":
        #     wire = external_wire_name
        # else:
        #     wire = find_obj_in_list(
        #         issuer.wires, external_wire_name
        #     ) or find_obj_in_list(issuer.ports, external_wire_name)
        #     if not wire:
        #         debug(f"Creating implicit wire '{port.name}' in '{issuer.name}'.", 1)
        #         # Add wire to issuer
        #         wire_signals = remove_signal_direction_suffixes(port.signals)
        #         issuer.create_wire(
        #             name=external_wire_name, signals=wire_signals, descr=port.descr
        #         )
        #         # Add wire to attributes_dict as well
        #         issuer.attributes_dict["wires"].append(
        #             {
        #                 "name": external_wire_name,
        #                 "signals": wire_signals,
        #                 "descr": port.descr,
        #             }
        #         )
        #         wire = issuer.wires[-1]

        # Create portmap and add to list
        portmap = iob_portmap(port=port)
        portmap_list.append(portmap)

        internal_portmap = convert2internal(portmap)
        internal_portmap.connect_external(external_wire_name, bit_slices=bit_slices)

    return portmap_list


def portmap_from_text(portmap_text):
    portmap_dict = {}
    # TODO: parse short notation text
    return iob_portmap(**portmap_dict)
