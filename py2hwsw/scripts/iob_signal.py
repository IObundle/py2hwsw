# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
import copy

from iob_base import fail_with_msg, parse_short_notation_text
from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_signal")
@dataclass
class iob_signal:
    """Class that represents a bus/port signal"""

    # Undefined by default. Will be set based on suffix of name (_i, _o, _io)
    direction: str = ""

    # Used for `iob_comb`: If enabled, iob_comb will infer a register for this signal.
    isreg: bool = False
    # Used for `iob_comb`: List of signals associated to the infered register.
    reg_signals: list[str] = field(default_factory=list)

    # Logic value for future simulation effort using global signals list.
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
        """Generate a verilog bus string from this signal"""
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
        """Generate a verilog port string from this signal"""
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
class iob_signal_reference:
    """Class that references another signal
    Use to distinguish from a real signal (for generator scripts)
    """

    signal: iob_signal | None = None


def get_real_signal(signal):
    """Given a signal reference, follow the reference (recursively) and
    return the real signal
    """
    while isinstance(signal, iob_signal_reference):
        signal = signal.signal
    return signal


def remove_signal_direction_suffixes(signal_list):
    """Given a signal list (usually from a port) that includes direction suffixes in their names (like _i, _o, _io),
    return a new list with the suffixes removed"""
    new_list = copy.deepcopy(signal_list)
    for signal in new_list:
        signal.name = signal.name.rsplit("_", 1)[0]
    return new_list


#
# API methods
#


def signal_from_dict(signal_dict):
    return iob_signal(**signal_dict)


def signal_from_text(signal_text):
    signal_flags = [
        "name",
        ["-w", {"dest": "width"}],
        ["-v", {"dest": "isvar", "action": "store_true"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
    ]
    signal_dict = parse_short_notation_text(signal_text, signal_flags)
    return iob_signal(**signal_dict)
