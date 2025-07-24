# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import fail_with_msg, parse_short_notation_text
from iob_wire import iob_wire
from iob_bus import iob_bus


@dataclass
class iob_port:
    """
    Describes an IO port.

    Attributes:
        wire (iob_wire | iob_bus): Reference to the wire or bus that is connected to the port.
        direction (str): Port direction.
                         Either 'input', 'output', or 'inout' if the port references a single wire.
                         Either 'manager' or 'subordinate' if the port references a bus.
        description (str): Description of the port.
        doc_only (bool): Only add to documentation
        doc_clearpage (bool): If enabled, the documentation table for this port will be terminated by a TeX '\clearpage' command.
    """

    wire: iob_wire | iob_bus = None
    direction: str = ""
    descr: str = "Default description"
    doc_only: bool = False
    doc_clearpage: bool = False

    def validate_attributes(self):
        if not self.wire:
            fail_with_msg("Port not associated to a wire or bus!")
        if isinstance(self.wire, iob_wire):
            if self.direction not in ["input", "output", "inout"]:
                fail_with_msg(f"Missing direction for port {self.wire.name}!")
        elif isinstance(self.wire, iob_bus):
            if self.direction not in ["manager", "subordinate"]:
                fail_with_msg(f"Missing direction for port {self.wire.name}!")
        else:
            fail_with_msg("Unknown type for wire associated to port!")

    def get_verilog_port(self, comma=True):
        """Generate a verilog port string from this wire"""
        self.validate_attributes()
        port_name = self.wire.name
        port_width = self.wire.width
        port_isvar = self.wire.isvar
        if "'" in port_name or port_name.lower() == "z":
            return None
        comma_char = "," if comma else ""
        port_type = " reg" if port_isvar else ""
        width_str = "" if self.get_width_int() == 1 else f"[{port_width}-1:0] "
        return f"{self.direction}{port_type} {width_str}{port_name}{comma_char}\n"

    def get_width_int(self):
        port_width = self.wire.width
        try:
            return int(port_width)
        except ValueError:
            return port_width


def port_obj_list_process(port):
    """Process ports for `find_obj_in_list()`"""
    return port.wire


#
# Other Py2HWSW interface methods
#


def create_port_from_dict(port_dict):
    """
    Function to create iob_port object from dictionary attributes.

    Attributes:
        port_dict (dict): dictionary with values to initialize attributes of iob_port object.
            - name (str): Name of the wire/bus associated to the port. Use one of the available suffixes to indicate direction:
                          Suffixes for wires: _i, _o, _io; Suffixes for buses: _m, _s.
            - interface (dict): If this key is provided, a bus will be created instead of a wire.
                                See `iob_bus.create_bus_from_dict` method for information about the format and supported keys of this dictionary.
            - width (int | str): Width of the wire associated to the port. Only applicable for wires, not for buses.
            This dictionary also supports the following keys corresponding to the iob_port attributes:
            - descr -> iob_port.descr
            - doc_only -> iob_port.doc_only
            - doc_clearpage -> iob_port.doc_clearpage

    Returns:
        iob_port: iob_port object
    """

    kwargs = port_dict.copy()

    # Remove non-port attributes from kwargs
    name = kwargs.pop("name")
    interface = kwargs.pop("interface", None)
    width = kwargs.pop("width", None)
    # From this point on, kwargs only contains iob_port attributes

    if interface and width:
        fail_with_msg(
            f"Interface and width cannot be specified together in port '{name}'!"
        )
    elif interface:
        # Create a bus for this port
        reference_obj = iob_bus(name=name, interface=interface)
    else:
        # Create a wire for this port
        reference_obj = iob_wire(name=name, width=width)

    # Get port direction form name suffix
    dir_suffix = name.split("_")[-1]
    dirs = {
        "i": "input",
        "o": "output",
        "io": "inout",
        "s": "subordinate",
        "m": "manager",
    }

    return iob_port(wire=reference_obj, direction=dirs[dir_suffix], **kwargs)


def port_text2dict(port_text):
    """Convert port short notation text to dictionary.
    Atributes:
        port_text (str): Short notation text. See `create_port_from_text` for format.

    Returns:
        dict: Dictionary with port attributes.
    """
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


def create_port_from_text(port_text):
    """
    Function to create iob_port object from short notation text.

    Attributes:
        port_text (str): Short notation text. Object attributes are specified using the following format:
            name [-i interface] [-d descr] [-s wire_name:width]+ [-doc] [-doc_clearpage]
            Example:
                control -d 'control bus' -s start_i:1 -s done_o:1 -s cmd_i:CMD_W -doc

    Returns:
        iob_port: iob_port object
    """
    return create_port_from_dict(port_text2dict(port_text))
