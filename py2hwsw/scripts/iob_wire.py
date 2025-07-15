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
    """Class that represents a bus/port wire"""

    # Undefined by default. Will be set based on suffix of name (_i, _o, _io)
    direction: str = ""

    # Used for `iob_comb`: If enabled, iob_comb will infer a register for this wire.
    isreg: bool = False
    # Used for `iob_comb`: List of wires associated to the infered register.
    reg_wires: list[str] = field(default_factory=list)

    # Logic value for future simulation effort using global wires list.
    # See 'TODO' in iob_core.py for more info: https://github.com/IObundle/py2hwsw/blob/a1e2e2ee12ca6e6ad81cc2f8f0f1c1d585aaee73/py2hwsw/scripts/iob_core.py#L251-L259
    value: str or int = 0

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Signal name is not set", ValueError)

        if self.name.endswith("_i"):
            self.direction = "input"
        elif self.name.endswith("_o"):
            self.direction = "output"
        elif self.name.endswith("_io"):
            self.direction = "inout"

    def get_verilog_bus(self):
        """Generate a verilog bus string from this wire"""
        if "'" in self.name or self.name.lower() == "z":
            return None
        bus_type = "reg" if self.isvar else "wire"
        width_str = "" if self.get_width_int() == 1 else f"[{self.width}-1:0] "
        return f"{bus_type} {width_str}{self.name};\n"

    def assert_direction(self):
        self.validate_attributes()  # FIXME: Not sure if this is the right place to call validate_attributes
        if not self.direction:
            fail_with_msg(f"Signal '{self.name}' has no direction", ValueError)

    def get_verilog_port(self, comma=True):
        """Generate a verilog port string from this wire"""
        if "'" in self.name or self.name.lower() == "z":
            return None
        self.assert_direction()
        comma_char = "," if comma else ""
        port_type = " reg" if self.isvar else ""
        width_str = "" if self.get_width_int() == 1 else f"[{self.width}-1:0] "
        return f"{self.direction}{port_type} {width_str}{self.name}{comma_char}\n"

    def get_width_int(self):
        try:
            return int(self.width)
        except ValueError:
            return self.width


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


def wire_from_text(wire_text):
    wire_flags = [
        "name",
        ["-w", {"dest": "width"}],
        ["-v", {"dest": "isvar", "action": "store_true"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
    ]
    wire_dict = parse_short_notation_text(wire_text, wire_flags)
    return iob_wire(**wire_dict)
