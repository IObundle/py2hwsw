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


@dataclass
class iob_portmap:
    """Describes an IO portmap connection."""

    # External wire that connects this port
    e_connect: iob_wire | None = None
    # Dictionary of bit slices for external connections. Name: signal name; Value: bit slice
    e_connect_bit_slices: list = field(default_factory=list)
    # Port associated with portmap
    port: iob_port = None

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
                validate_verilog_const(value=wire, direction=self.port.signals[0].direction)
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
    """Given a portmap reference, return the associated port
    """
    port = None
    if isinstance(portmap, iob_portmap):
        port = portmap.port
    return port
