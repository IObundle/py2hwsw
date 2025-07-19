# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
import copy

from iob_base import fail_with_msg, parse_short_notation_text
from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_wire")
@dataclass
class iob_wire:
    """Py2HWSW's internal implementation of 'iob_wire' API class."""

    # Used for `iob_comb`: If enabled, iob_comb will infer a register for this wire.
    isreg: bool = False
    # Used for `iob_comb`: List of wires associated to the infered register.
    reg_wires: list[str] = field(default_factory=list)

    def __post_init__(self):
        print("DEBUG: Creating wire")
        pass

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Wire name is not set", ValueError)

    def get_verilog_bus(self):
        """Generate a verilog bus string from this wire"""
        if "'" in self.name or self.name.lower() == "z":
            return None
        bus_type = "reg" if self.isvar else "wire"
        width_str = "" if self.get_width_int() == 1 else f"[{self.width}-1:0] "
        return f"{bus_type} {width_str}{self.name};\n"

    def get_width_int(self):
        width_v = self.width
        try:
            return int(width_v)
        except ValueError:
            return width_v


@dataclass
class iob_wire_reference:
    """Class that references another wire
    Use to distinguish from a real wire (for generator scripts)
    """

    wire: iob_wire | None = None


def get_real_wire(wire):
    """Given a wire reference, follow the reference (recursively) and
    return the real wire
    """
    while isinstance(wire, iob_wire_reference):
        wire = wire.wire
    return wire


def remove_wire_direction_suffixes(wire_list):
    """Given a wire list (usually from a port) that includes direction suffixes in their names (like _i, _o, _io),
    return a new list with the suffixes removed"""
    new_list = copy.deepcopy(wire_list)
    for wire in new_list:
        wire.name = wire.name.rsplit("_", 1)[0]
    return new_list


#
# API methods
#


def wire_from_dict(wire_dict):
    return iob_wire(**wire_dict)


def wire_text2dict(wire_text):
    wire_flags = [
        "name",
        ["-w", {"dest": "width"}],
        ["-v", {"dest": "isvar", "action": "store_true"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
    ]
    return parse_short_notation_text(wire_text, wire_flags)


def wire_from_text(wire_text):
    return wire_from_dict(wire_text2dict(wire_text))
