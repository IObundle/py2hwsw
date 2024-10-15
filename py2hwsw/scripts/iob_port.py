# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Dict

import iob_colors
import if_gen
from iob_wire import iob_wire
from iob_base import convert_dict2obj_list, fail_with_msg, str_to_kwargs
from iob_signal import iob_signal


@dataclass
class iob_port(iob_wire):
    """Describes an IO port."""

    # External wire that connects this port
    e_connect: iob_wire | None = None
    # Dictionary of bit slices for external connections. Name: signal name; Value: bit slice
    e_connect_bit_slices: list = field(default_factory=list)
    doc_only: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Port name is not set", ValueError)

        _sufix_dict = {
            "_i": "input",
            "_o": "output",
            "_io": "inout",
            "_s": "slave",
            "_m": "master",
        }
        _direction = None
        for sufix, d in _sufix_dict.items():
            if self.name.endswith(sufix):
                _direction = d
                break

        if self.interface:
            if _direction != self.interface.subtype:
                fail_with_msg(
                    f"Port '{self.name}' is a '{_direction}' port but interface subtype is '{self.interface.subtype}'",
                    ValueError,
                )
            self.interface.subtype = _direction
            self.signals += if_gen.get_signals(
                self.interface.type,
                self.interface.subtype,
                self.interface.mult,
                self.interface.widths,
                self.interface.port_prefix,
            )
        elif _direction in ["slave", "master"]:
            fail_with_msg(
                f"Port '{self.name}' is a '{_direction}' port but no interface is defined",
                ValueError,
            )

        for signal in self.signals:
            if not signal.direction:
                raise Exception("Port direction is required")
            elif signal.direction not in ["input", "output", "inout"]:
                raise Exception(
                    "Error: Direction must be 'input', 'output', or 'inout'."
                )
            if (
                _direction in ["input", "output", "inout"]
                and signal.direction != _direction
            ):
                fail_with_msg(
                    f"Signal direction '{signal.direction}' does not match port name '{self.name}'",
                    ValueError,
                )

    def connect_external(self, wire, bit_slices={}):
        """Connects the port to an external wire
        :param iob_wire wire: external wire
        :param list bit_slices: bit slices of signals in wire
        """
        self.e_connect = wire
        self.e_connect_bit_slices = bit_slices


attrs = [
    "name",
    ["-i", "interface", {"nargs": 2}, ["type", "subtype"]],
    ["-s", "signals", {"nargs": 2, "action": "append"}, ["name", "width"]],
]


@str_to_kwargs(attrs)
def create_port(core, *args, signals=[], interface=None, **kwargs):
    """Creates a new port object and adds it to the core's port list
    Also creates a new internal module wire to connect to the new port
    param core: core object
    """
    # Ensure 'ports' list exists
    core.set_default_attribute("ports", [])
    # Convert user signal dictionaries into 'iob_signal' objects
    sig_obj_list = convert_dict2obj_list(signals, iob_signal)
    # Convert user interface dictionary into 'if_gen.interface' object
    interface_obj = if_gen.dict2interface(interface)
    if interface_obj and not interface_obj.file_prefix:
        interface_obj.file_prefix = core.name + "_"
    port = iob_port(*args, signals=sig_obj_list, interface=interface_obj, **kwargs)
    core.ports.append(port)
