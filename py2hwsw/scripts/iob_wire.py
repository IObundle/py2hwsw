# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
import copy
import importlib

from iob_base import fail_with_msg, parse_short_notation_text
from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_wire")
@dataclass
class iob_wire:
    """Class that represents a core's internal wire"""

    def __post_init__(self):
        # print("DEBUG: Replacing global_wire attrs in current (local) wire by setters and getters")
        global_wire_attributes = self.__create_global_wire_attribute_wrappers()
        # print("DEBUG: Creating global wire")
        self.global_wire = iob_global_wire(**global_wire_attributes)

    def __create_global_wire_attribute_wrappers(self) -> dict:
        """
        Deletes global wire attributes from current iob_wire object;
        Generates setter and getter for them, pointing to the attributes of the corresponding global wire.
        Returns:
            dict: The attributes of the global wire and their default values (the ones from the locally deleted attributes).
        """
        # Lazy import the global API class to get its attributes
        global_wire_api_class = getattr(
            importlib.import_module("user_api.api"), "iob_global_wire"
        )

        # Local utility functions
        def _generate_setter(attribute_name):
            """
            Function to generate setter for a given attribute.
            Setter will pass the given value to the corresponding attribute in the internal object.
            """

            def setter(self, value):
                # print("Setter called for attribute: ", attribute_name)
                setattr(self.global_wire, attribute_name, value)

            return setter

        def _generate_getter(attribute_name):
            """
            Function to generate getter for a given attribute.
            Getter will get value from the corresponding attribute in the internal object.
            """

            def getter(self):
                # print("Getter called for attribute: ", attribute_name)
                return getattr(self.global_wire, attribute_name)

            return getter

        # Remove API attributes of global wire from this class;
        # Generate setter and getter for them
        global_wire_attributes = {}
        for global_attr in global_wire_api_class.__annotations__:
            wrapper_attr = global_attr
            # Replace real "name" attribute of global wire by "global_name" wrapper attribute
            if wrapper_attr == "name":
                wrapper_attr = "global_name"

            # Extract values of attributes set by API and delete them
            global_wire_attributes[global_attr] = getattr(self, wrapper_attr)
            delattr(self, wrapper_attr)

            # Create setter and getter for the attribute
            # print("DEBUG: Creating wrapper attribute", wrapper_attr)
            setter = _generate_setter(wrapper_attr)
            getter = _generate_getter(wrapper_attr)
            setattr(self, f"set_{wrapper_attr}", setter)
            setattr(self, f"get_{wrapper_attr}", getter)

            # Create a property for the wrapped attribute
            setattr(
                self,
                wrapper_attr,
                property(getter, setter),
            )

        return global_wire_attributes


@internal_api_class("user_api.api", "iob_global_wire")
@dataclass
class iob_global_wire:
    """Class that represents a global wire (net)"""

    # Undefined by default. Will be set based on suffix of name (_i, _o, _io)
    direction: str = ""

    # Used for `iob_comb`: If enabled, iob_comb will infer a register for this wire.
    isreg: bool = False
    # Used for `iob_comb`: List of wires associated to the infered register.
    reg_wires: list[str] = field(default_factory=list)

    def __post_init__(self):
        print("DEBUG: Creating global wire")

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Wire name is not set", ValueError)

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
            fail_with_msg(f"Wire '{self.name}' has no direction", ValueError)

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

    wire: iob_global_wire | None = None


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
    # Create iob_global_wire if it does not exist?

    return iob_wire(**wire_dict)


def wire_from_text(wire_text):
    # TODO:
    pass


def global_wire_from_dict(global_wire_dict):
    return iob_global_wire(**global_wire_dict)


def global_wire_text2dict(global_wire_text):
    global_wire_flags = [
        "name",
        ["-w", {"dest": "width"}],
        ["-v", {"dest": "isvar", "action": "store_true"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
    ]
    return parse_short_notation_text(global_wire_text, global_wire_flags)


def global_wire_from_text(global_wire_text):
    return global_wire_from_dict(global_wire_text2dict(global_wire_text))
