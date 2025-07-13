# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
import re
from typing import List

import interfaces
from iob_base import (
    find_obj_in_list,
    convert_dict2obj_list,
    fail_with_msg,
    add_traceback_msg,
    str_to_kwargs,
    assert_attributes,
    update_obj_from_dict,
    parse_short_notation_text,
)
from iob_signal import (
    iob_signal,
    iob_signal_reference,
    get_real_signal,
    signal_from_dict,
    signal_from_text,
)

from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_wire")
@dataclass
class iob_wire:
    """Class to represent a wire in an iob module"""

    def create_signals_from_interface(self):
        if not self.interface:
            fail_with_msg(f"Wire '{self.name}' has no interface!", ValueError)

        self.signals += self.interface.get_signals()

        # Remove signal direction information
        for signal in self.signals:
            # Skip signal references
            if isinstance(signal, iob_signal_reference):
                continue
            if hasattr(signal, "direction"):
                # Remove direction suffix from signal name
                if signal.name.endswith("_i") or signal.name.endswith("_o"):
                    signal.name = signal.name[:-2]
                elif signal.name.endswith("_io"):
                    signal.name = signal.name[:-3]
                signal.direction = ""

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("All wires must have a name!", ValueError)


attrs = [
    "name",
    ["-i", "signals&i", {"nargs": 1}, ("type",)],
    ["-s", "signals&s", {"nargs": "+"}, ["name:width"]],
]


@str_to_kwargs(attrs)
def create_wire(core, *args, signals=[], **kwargs):
    """Creates a new wire object and adds it to the core's wire list
    param core: core object
    """
    try:
        # Ensure 'wires' list exists
        core.set_default_attribute("wires", [])
        # Check if there are any references to signals in other wires/ports
        sig_obj_list = []
        interface_obj = None
        if type(signals) is list:
            # Convert user signal dictionaries into 'iob_signal' objects
            replace_duplicate_signals_by_references(core.wires + core.ports, signals)
            sig_obj_list = convert_dict2obj_list(signals, iob_signal)
        elif type(signals) is dict:
            # Convert user interface dictionary into '_interface' object
            interface_obj = dict2interface(
                name=kwargs.get("name", ""), interface_dict=signals
            )
            if interface_obj and not interface_obj.file_prefix:
                interface_obj.file_prefix = core.name + "_"
        else:
            fail_with_msg(f"Invalid signal type! {signals}", TypeError)
        assert_attributes(
            iob_wire,
            kwargs,
            error_msg=f"Invalid {kwargs.get('name', '')} wire attribute '[arg]'!",
        )
        wire = iob_wire(*args, signals=sig_obj_list, interface=interface_obj, **kwargs)
        replace_duplicate_signals_by_references(core.wires + core.ports, wire.signals)
        core.wires.append(wire)
    except Exception:
        add_traceback_msg(f"Failed to create wire '{kwargs['name']}'.")
        raise


def get_wire_signal(core, wire_name: str, signal_name: str):
    """Return a signal reference from a given wire.
    param core: core object
    param wire_name: name of wire in the core's local wire list
    param signal_name: name of signal in the wire's signal list
    """
    wire = find_obj_in_list(core.wires, wire_name) or find_obj_in_list(
        core.ports, wire_name
    )
    if not wire:
        fail_with_msg(f"Could not find wire/port '{wire_name}'!")

    signal = find_obj_in_list(wire.signals, signal_name, process_func=get_real_signal)
    if not signal:
        fail_with_msg(
            f"Could not find signal '{signal_name}' of wire/port '{wire_name}'!"
        )

    return iob_signal_reference(signal=signal)


def replace_duplicate_signals_by_references(wires, signals):
    """Ensure that given list of 'signals' does not contain duplicates of other signals
    in the given 'wires' list, by replacing the duplicates with references to the
    original.
    param wires: list of wires with (original) signals
    param signals: list of new signals to be processed. If this list has a signal with
    the same name as another signal in the wires list, then this signal is replaced by a
    reference to the original.
    """
    for idx, signal in enumerate(signals):
        if isinstance(signal, iob_signal_reference):
            continue
        if type(signal) is iob_signal:
            signal = signal.__dict__
        original_signal = find_signal_in_wires(wires, signal["name"])
        if not original_signal:
            continue
        original_signal = get_real_signal(original_signal)
        # print(f"[DEBUG] Replacing signal '{signal['name']}' by reference to original.")
        # Verify that new signal has same parameters as the original_signal
        for key, value in signal.items():
            if original_signal.__dict__[key] != value:
                fail_with_msg(
                    f"Signal reference '{signal['name']}' has different '{key}' than the original signal!\n"
                    f"Original signal '{original_signal.name}' value: '{original_signal.__dict__[key]}'.\n"
                    f"Signal reference '{signal['name']}' value: '{value}'."
                )
        # Replace signal by a reference to the original
        signals[idx] = iob_signal_reference(signal=original_signal)


def find_signal_in_wires(wires, signal_name, process_func=get_real_signal):
    """Search for a signal in given list of wires
    param wires: list of wires
    param signal_name: name of signal to search for
    param process_func: function to process each signal before search
    """
    for wire in wires:
        signal = find_obj_in_list(wire.signals, signal_name, process_func=process_func)
        if signal:
            return signal
    return None


#
# Convert interface dictionary to an interface object
# Note: This function is to be deprecated in the future, since objects should be created directly for
# each interface type.
#
def dict2interface(name, interface_dict):
    """Convert dictionary to an interface.
    Example interface dict:
    {
        "type": "iob",
        # Generic string parameter
        "params": "",
        # Widths/Other parameters
        "DATA_W": "DATA_W",
        "ADDR_W": "ADDR_W",
    }
    To use an assymmetric memory interface, the dictionary should look like this:
    {
        "type": "ram_at2p",
        # Generic string parameter
        "params": "",
        # Widths/Other parameters
        "ADDR_W": "ADDR_W",
        "W_DATA_W": "W_DATA_W",
        "R_DATA_W": "R_DATA_W",
    }
    """
    if not interface_dict:
        return None

    genre = interface_dict.get("type", "")

    if name.endswith("_m"):
        if_direction = "manager"
    elif name.endswith("_s"):
        if_direction = "subordinate"
    else:
        if_direction = ""

    prefix = interface_dict.get("prefix", "")
    mult = interface_dict.get("mult", 1)
    params = interface_dict.get("params", None)
    if params is not None:
        params = params.split("_")
    file_prefix = interface_dict.get("file_prefix", "")
    portmap_port_prefix = interface_dict.get("portmap_port_prefix", "")

    # Remaining entries in the interface_dict (usually widths or other parameters)
    remaining_entries = {
        k: v
        for k, v in interface_dict.items()
        if k
        not in [
            "type",
            "prefix",
            "mult",
            "params",
            "file_prefix",
            "portmap_port_prefix",
        ]
    }

    interface = interfaces.create_interface(
        genre=genre,
        if_direction=if_direction,
        mult=mult,
        widths=remaining_entries,
        prefix=prefix,
        params=params,
        portmap_port_prefix=portmap_port_prefix,
        file_prefix=file_prefix,
    )

    return interface


# Dictionary of attributes that need to be preprocessed when set from a wire_dictionary, and their corresponding preprocessor functions
WIRE_ATTRIBUTES_PREPROCESSOR_FUNCTIONS = {
    "signals": lambda lst: [signal_from_dict(i) for i in lst],
}

#
# API methods
#


def wire_from_dict(wire_dict):
    wire_obj = iob_wire()

    key_attribute_mapping = {}
    preprocessor_functions = WIRE_ATTRIBUTES_PREPROCESSOR_FUNCTIONS
    # Update wire_obj attributes with values from given dictionary
    update_obj_from_dict(
        wire_obj._get_py2hwsw_internal_obj(),
        wire_dict,
        key_attribute_mapping,
        preprocessor_functions,
        wire_obj.get_supported_attributes().keys(),
    )

    return wire_obj


def wire_from_text(wire_text):
    wire_flags = [
        "name",
        ["-i", {"dest": "interface"}],
        ["-s", {"dest": "signals", "action": "append"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
    ]
    wire_dict = parse_short_notation_text(wire_text, wire_flags)
    wire_signals = []
    for s in wire_dict.get("signals", []):
        try:
            [s_name, s_width] = s.split(":")
        except ValueError:
            fail_with_msg(
                f"Invalid signal format '{s}'! Expected 'name:width' format.",
                ValueError,
            )
        wire_signals.append(signal_from_dict({"name": s_name, "width": s_width}))
    wire_dict.update({"signals": wire_signals})
    return iob_wire(**wire_dict)
