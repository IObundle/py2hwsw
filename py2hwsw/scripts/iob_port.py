# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import fail_with_msg, parse_short_notation_text
from api_base import internal_api_class, convert2internal
from iob_wire import iob_global_wire


@internal_api_class("user_api.api", "iob_port")
@dataclass
class iob_port:
    """Py2HWSW's internal implementation of 'iob_port' API class."""

    def validate_attributes(self):
        if not self.global_wire:
            fail_with_msg("Port not associated to global wire!")
        if self.direction not in ["input", "output", "inout"]:
            fail_with_msg(f"Missing direction for port {self.global_wire.name}!")

    def get_verilog_port(self, comma=True):
        """Generate a verilog port string from this wire"""
        self.validate_attributes()
        port_name = convert2internal(self.global_wire).name
        port_width = convert2internal(self.global_wire).width
        port_isvar = convert2internal(self.global_wire).isvar
        if "'" in port_name or port_name.lower() == "z":
            return None
        comma_char = "," if comma else ""
        port_type = " reg" if port_isvar else ""
        width_str = "" if self.get_width_int() == 1 else f"[{port_width}-1:0] "
        return f"{self.direction}{port_type} {width_str}{port_name}{comma_char}\n"

    def get_width_int(self):
        port_width = convert2internal(self.global_wire).width
        try:
            return int(port_width)
        except ValueError:
            return port_width


#
# API methods
#


def port_from_dict(port_dict):
    # Create a global wire for this port
    api_iob_global_wire = iob_global_wire(
        name=port_dict["name"], width=port_dict["width"]
    )

    # Get port direction form name suffix
    dir_suffix = port_dict["name"].split("_")[-1]
    dirs = {"i": "input", "o": "output", "io": "inout"}

    return iob_port(global_wire=api_iob_global_wire, direction=dirs[dir_suffix])


def port_text2dict(port_text):
    port_flags = [
        "name",
        ["-i", {"dest": "interface"}],
        ["-w", {"dest": "wires", "action": "append"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
        ["-doc", {"dest": "doc_only", "action": "store_true"}],
        ["-doc_clearpage", {"dest": "doc_clearpage", "action": "store_true"}],
    ]
    port_dict = parse_short_notation_text(port_text, port_flags)
    port_wires = []
    for s in port_dict.get("wires", []):
        try:
            [s_name, s_width] = s.split(":")
        except ValueError:
            fail_with_msg(
                f"Invalid wire format '{s}'! Expected 'name:width' format.",
                ValueError,
            )
        port_wires.append({"name": s_name, "width": s_width})
    port_dict.update({"wires": port_wires})
    return port_dict


def port_from_text(port_text):
    return port_from_dict(port_text2dict(port_text))
