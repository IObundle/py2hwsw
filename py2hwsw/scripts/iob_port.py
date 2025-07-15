# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_bus import (
    iob_bus,
    replace_duplicate_wires_by_references,
    dict2interface,
)
from iob_base import (
    convert_dict2obj_list,
    fail_with_msg,
    str_to_kwargs,
    assert_attributes,
    update_obj_from_dict,
)
from iob_wire import iob_wire
from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_port")
@dataclass
class iob_port:
    """Describes an IO port."""

    def create_wires_from_interface(self):
        if not self.interface:
            fail_with_msg(f"Bus '{self.name}' has no interface!", ValueError)

        self.wires += self.interface.get_wires()

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("All ports must have a name!", ValueError)

        _sufix_dict = {
            "_i": "input",
            "_o": "output",
            "_io": "inout",
            "_s": "subordinate",
            "_m": "manager",
        }
        _direction = None
        for sufix, d in _sufix_dict.items():
            if self.name.endswith(sufix):
                _direction = d
                break
        else:
            fail_with_msg(
                f"Port name '{self.name}' does not end with a valid direction suffix!\n"
                f"Must have one of the following suffixes: {', '.join(_sufix_dict.keys())}.",
                ValueError,
            )

        if not self.interface and _direction in ["subordinate", "manager"]:
            fail_with_msg(
                f"Port '{self.name}' is a '{_direction}' port but no interface is defined",
                ValueError,
            )

        port_has_inputs = False
        port_has_outputs = False
        for api_wire in self.wires:
            # Get internal representation of wire, because 'direction' is a internal attribute
            wire = api_wire._get_py2hwsw_internal_obj()
            if not wire.direction:
                raise Exception("Port direction is required")
            elif wire.direction not in ["input", "output", "inout"]:
                raise Exception(
                    "Error: Direction must be 'input', 'output', or 'inout'."
                )

            if _direction in ["input", "output"] and wire.direction != _direction:
                fail_with_msg(
                    f"Signal direction '{wire.direction}' does not match port name '{self.name}'",
                    ValueError,
                )

            if wire.direction == "input":
                port_has_inputs = True
            elif wire.direction == "output":
                port_has_outputs = True
            elif wire.direction == "inout":
                port_has_inputs = True
                port_has_outputs = True

        if _direction == "inout" and not port_has_inputs:
            fail_with_msg(
                f"Port '{self.name}' has 'inout' direction but no inputs defined",
                ValueError,
            )
        elif _direction == "inout" and not port_has_outputs:
            fail_with_msg(
                f"Port '{self.name}' has 'inout' direction but no outputs defined",
                ValueError,
            )


attrs = [
    "name",
    ["-i", "wires&i", {"nargs": 1}, ("type",)],
    ["-s", "wires&s", {"nargs": "+"}, ["name:width"]],
]


@str_to_kwargs(attrs)
def create_port_from_dict(core, *args, wires=[], **kwargs):
    """Creates a new port object using a dictionary and adds it to the core's port list
    Also creates a new internal module bus to connect to the new port
    param core: core object
    """
    # Ensure 'ports' list exists
    core.set_default_attribute("ports", [])
    sig_obj_list = []
    interface_obj = None

    if type(wires) is list:
        # Convert user wire dictionaries into 'iob_wire' objects
        sig_obj_list = convert_dict2obj_list(wires, iob_wire)
    elif type(wires) is dict:
        # Convert user interface dictionary into an interface object
        interface_obj = dict2interface(kwargs.get("name", ""), wires)
        if interface_obj and not interface_obj.file_prefix:
            interface_obj.file_prefix = core.name + "_"
    else:
        fail_with_msg(f"Invalid wire type! {wires}", TypeError)
    assert_attributes(
        iob_port,
        kwargs,
        error_msg=f"Invalid {kwargs.get('name', '')} port attribute '[arg]'!",
    )
    port = iob_port(*args, wires=sig_obj_list, interface=interface_obj, **kwargs)
    replace_duplicate_wires_by_references(core.ports, port.wires)
    core.ports.append(port)


@str_to_kwargs(attrs)
def add_wires_port(core, *args, wires=[], **kwargs):
    """Creates a new port object and adds it to the core's port list
    Also creates a new internal module bus to connect to the new port
    param core: core object
    """
    # Ensure 'ports' list exists
    core.set_default_attribute("ports", [])
    # Check if the list of wires has only iob_wire types
    if type(wires) is list:
        for wire in wires:
            if not isinstance(wire, iob_wire):
                fail_with_msg(
                    f"Signals must be a list of iob_wires! {wires}", TypeError
                )
    # Create the port with the wires
    port = iob_port(*args, wires=wires, **kwargs)
    replace_duplicate_wires_by_references(core.ports, port.wires)
    core.ports.append(port)


@str_to_kwargs(attrs)
def add_interface_port(core, *args, name, interface, **kwargs):
    """Creates a new port object and adds it to the core's port list
    Also creates a new internal module bus to connect to the new port
    param core: core object
    """
    # Ensure 'ports' list exists
    core.set_default_attribute("ports", [])
    # Check if the interface is a valid interface object
    if not hasattr(interface, "get_wires"):
        fail_with_msg(
            f"Interface must be a valid interface object! {interface}", TypeError
        )
    if not interface.file_prefix:
        interface.file_prefix = core.name + "_"
    if interface.prefix == "":
        interface.prefix = f"{name}_"
    # Create the port with the interface
    port = iob_port(*args, name=name, interface=interface, **kwargs)
    replace_duplicate_wires_by_references(core.ports, port.wires)
    core.ports.append(port)


#
# API methods
#


def port_from_dict(port_dict):
    return iob_port(**port_dict)


def port_from_text(port_text):
    port_dict = {}
    # TODO: parse short notation text
    return iob_port(**port_dict)
