# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import List

import if_gen
from iob_base import (
    find_obj_in_list,
    convert_dict2obj_list,
    fail_with_msg,
    add_traceback_msg,
    str_to_kwargs,
    assert_attributes,
)
from iob_signal import iob_signal, iob_signal_reference, get_real_signal


@dataclass
class iob_wire:
    """Class to represent a wire in an iob module"""

    # Identifier name for the wire.
    name: str = ""
    # Name of the standard interface to auto-generate with `if_gen.py` script.
    interface: if_gen.interface = None
    # Description of the wire.
    descr: str = "Default description"
    # Conditionally define this wire if the specified Verilog macro is defined/undefined.
    if_defined: str = ""
    if_not_defined: str = ""
    # List of signals belonging to this wire
    # (each signal represents a hardware Verilog wire).
    signals: List = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            fail_with_msg("All wires must have a name!", ValueError)

        if self.interface:
            self.signals += if_gen.get_signals(
                name = self.interface.type,
                if_type = "",
                mult = self.interface.mult,
                port_params = self.interface.port_params,
                widths = self.interface.widths,
                signal_prefix = self.interface.prefix,
            )

            # Remove signal direction information
            for signal in self.signals:
                # Skip signal references
                if isinstance(signal, iob_signal_reference):
                    continue
                if hasattr(signal, "direction"):
                    suffix = if_gen.get_suffix(signal.direction)
                    if signal.name.endswith(suffix):
                        signal.name = signal.name[: -len(suffix)]
                    signal.direction = ""


attrs = [
    "name",
    ["-i", "signals", {"nargs": 1}, ("type",)],
    ["-s", "signals", {"nargs": "+"}, ["name:width"]],
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
            # Convert user interface dictionary into 'if_gen.interface' object
            interface_obj = if_gen.dict2interface(signals)
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
