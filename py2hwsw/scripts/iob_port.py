# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_wire import (
    iob_wire,
    replace_duplicate_signals_by_references,
    dict2interface,
    WIRE_ATTRIBUTES_PREPROCESSOR_FUNCTIONS,
)
from iob_base import (
    convert_dict2obj_list,
    fail_with_msg,
    str_to_kwargs,
    assert_attributes,
    update_obj_from_dict,
)
from iob_signal import iob_signal
from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_port")
@dataclass
class iob_port(iob_wire):
    """Describes an IO port."""

    def create_signals_from_interface(self):
        if not self.interface:
            fail_with_msg(f"Wire '{self.name}' has no interface!", ValueError)

        self.signals += self.interface.get_signals()

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
        for signal in self.signals:
            # Get internal representation of signal, because 'direction' is a internal attribute
            signal = signal._get_py2hwsw_internal_obj()
            if not signal.direction:
                raise Exception("Port direction is required")
            elif signal.direction not in ["input", "output", "inout"]:
                raise Exception(
                    "Error: Direction must be 'input', 'output', or 'inout'."
                )

            if _direction in ["input", "output"] and signal.direction != _direction:
                fail_with_msg(
                    f"Signal direction '{signal.direction}' does not match port name '{self.name}'",
                    ValueError,
                )

            if signal.direction == "input":
                port_has_inputs = True
            elif signal.direction == "output":
                port_has_outputs = True
            elif signal.direction == "inout":
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
    ["-i", "signals&i", {"nargs": 1}, ("type",)],
    ["-s", "signals&s", {"nargs": "+"}, ["name:width"]],
]


@str_to_kwargs(attrs)
def create_port_from_dict(core, *args, signals=[], **kwargs):
    """Creates a new port object using a dictionary and adds it to the core's port list
    Also creates a new internal module wire to connect to the new port
    param core: core object
    """
    # Ensure 'ports' list exists
    core.set_default_attribute("ports", [])
    sig_obj_list = []
    interface_obj = None

    if type(signals) is list:
        # Convert user signal dictionaries into 'iob_signal' objects
        sig_obj_list = convert_dict2obj_list(signals, iob_signal)
    elif type(signals) is dict:
        # Convert user interface dictionary into an interface object
        interface_obj = dict2interface(kwargs.get("name", ""), signals)
        if interface_obj and not interface_obj.file_prefix:
            interface_obj.file_prefix = core.name + "_"
    else:
        fail_with_msg(f"Invalid signal type! {signals}", TypeError)
    assert_attributes(
        iob_port,
        kwargs,
        error_msg=f"Invalid {kwargs.get('name', '')} port attribute '[arg]'!",
    )
    port = iob_port(*args, signals=sig_obj_list, interface=interface_obj, **kwargs)
    replace_duplicate_signals_by_references(core.ports, port.signals)
    core.ports.append(port)


@str_to_kwargs(attrs)
def add_signals_port(core, *args, signals=[], **kwargs):
    """Creates a new port object and adds it to the core's port list
    Also creates a new internal module wire to connect to the new port
    param core: core object
    """
    # Ensure 'ports' list exists
    core.set_default_attribute("ports", [])
    # Check if the list of signals has only iob_signal types
    if type(signals) is list:
        for signal in signals:
            if not isinstance(signal, iob_signal):
                fail_with_msg(
                    f"Signals must be a list of iob_signals! {signals}", TypeError
                )
    # Create the port with the signals
    port = iob_port(*args, signals=signals, **kwargs)
    replace_duplicate_signals_by_references(core.ports, port.signals)
    core.ports.append(port)


@str_to_kwargs(attrs)
def add_interface_port(core, *args, name, interface, **kwargs):
    """Creates a new port object and adds it to the core's port list
    Also creates a new internal module wire to connect to the new port
    param core: core object
    """
    # Ensure 'ports' list exists
    core.set_default_attribute("ports", [])
    # Check if the interface is a valid interface object
    if not hasattr(interface, "get_signals"):
        fail_with_msg(
            f"Interface must be a valid interface object! {interface}", TypeError
        )
    if not interface.file_prefix:
        interface.file_prefix = core.name + "_"
    if interface.prefix == "":
        interface.prefix = f"{name}_"
    # Create the port with the interface
    port = iob_port(*args, name=name, interface=interface, **kwargs)
    replace_duplicate_signals_by_references(core.ports, port.signals)
    core.ports.append(port)


#
# API methods
#


def port_from_dict(port_dict):
    port_obj = iob_port()

    key_attribute_mapping = {}
    preprocessor_functions = WIRE_ATTRIBUTES_PREPROCESSOR_FUNCTIONS
    # Update port_obj attributes with values from given dictionary
    update_obj_from_dict(
        port_obj._get_py2hwsw_internal_obj(),
        port_dict,
        key_attribute_mapping,
        preprocessor_functions,
        port_obj.__annotations__.keys(),
    )

    return port_obj


def port_from_text(port_text):
    port_dict = {}
    # TODO: parse short notation text
    return iob_port(**port_dict)
