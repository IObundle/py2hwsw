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
from iob_signal import get_real_signal
from iob_wire import iob_wire


@dataclass
class iob_portmap(iob_port):
    """Describes an IO portmap connection."""

    # External wire that connects this port
    e_connect: iob_wire | None = None
    # Dictionary of bit slices for external connections. Name: signal name; Value: bit slice
    e_connect_bit_slices: list = field(default_factory=list)

    # TODO: create constructor from port?
    def __init__(self, port: iob_port):
        # Iterate over the port attributes
        for key, value in port.__dict__.items():
            setattr(self, key, value)

    def connect_external(self, wire, bit_slices={}):
        """Connects the port to an external wire
        Verifies that the wire is compatible with the port
        :param iob_wire wire: external wire
        :param list bit_slices: bit slices of signals in wire
        """
        # wire must be iob_wire or str
        if isinstance(wire, str):
            if len(self.signals) != 1:
                fail_with_msg(
                    f"{iob_colors.FAIL}Port '{self.name}' has more than one signal but is connected to one constant value '{self.e_connect}'!{iob_colors.ENDC}",
                    ValueError,
                )
            else:
                validate_verilog_const(value=wire, direction=self.signals[0].direction)
        elif isinstance(wire, iob_wire):
            if self.interface and wire.interface:
                if self.interface.type == wire.interface.type:
                    for signal in self.signals:
                        search_name = signal.name.replace(
                            self.interface.prefix, wire.interface.prefix, 1
                        )
                        if self.name[-2] != wire.name[-2]:
                            swap_suffix = {
                                "_i": "_o",
                                "_o": "_i",
                            }
                            if wire.name[-2:] in ["_s", "_m"]:
                                search_name += (
                                    search_name[:-2] + swap_suffix[search_name[-2:]]
                                )
                            else:
                                search_name = search_name[:-2]
                        e_signal = find_obj_in_list(
                            wire.signals, search_name, get_real_signal
                        )
                        if not e_signal:
                            if not any(
                                [
                                    f"{signal.name}:" in bit_slice
                                    for bit_slice in bit_slices
                                ]
                            ):
                                newlinechar = "\n"
                                fail_with_msg(
                                    f"""Port '{self.name}' signal '{signal.name}' not connected to external wire '{wire.name}'!
Port '{self.name}' has the following signals:                                                                   

{newlinechar.join("- " + signal.name for signal in self.signals)}                                               
External connection '{wire.name}' has the following signals:                                                    
{newlinechar.join("- " + signal.name for signal in wire.signals)}                                               
""",
                                    ValueError,
                                )
                elif len(self.signals) != len(wire.signals):
                    newlinechar = "\n"
                    fail_with_msg(
                        f"""Port '{self.name}' has different number of signals compared to external connection '{wire.name}'!
Port '{self.name}' has the following signals:
{newlinechar.join("- " + signal.name for signal in self.signals)}

External connection '{wire.name}' has the following signals:
{newlinechar.join("- " + signal.name for signal in wire.signals)}
""",
                        ValueError,
                    )
            elif len(self.signals) != len(wire.signals):
                newlinechar = "\n"
                fail_with_msg(
                    f"""Port '{self.name}' has different number of signals compared to external connection '{wire.name}'!
Port '{self.name}' has the following signals:
{newlinechar.join("- " + get_real_signal(signal).name for signal in self.signals)}

External connection '{wire.name}' has the following signals:
{newlinechar.join("- " + get_real_signal(signal).name for signal in wire.signals)}
""",
                    ValueError,
                )
            else:
                for p, w in zip(self.signals, wire.signals):
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
