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


@internal_api_class("user_api.api", "iob_bus")
@dataclass
class iob_bus:
    """Class to represent a bus in an iob module"""

    def create_signals_from_interface(self):
        if not self.interface:
            fail_with_msg(f"Bus '{self.name}' has no interface!", ValueError)

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
            fail_with_msg("All buses must have a name!", ValueError)


attrs = [
    "name",
    ["-i", "signals&i", {"nargs": 1}, ("type",)],
    ["-s", "signals&s", {"nargs": "+"}, ["name:width"]],
]


@str_to_kwargs(attrs)
def create_bus(core, *args, signals=[], **kwargs):
    """Creates a new bus object and adds it to the core's bus list
    param core: core object
    """
    try:
        # Ensure 'buses' list exists
        core.set_default_attribute("buses", [])
        # Check if there are any references to signals in other buses/ports
        sig_obj_list = []
        interface_obj = None
        if type(signals) is list:
            # Convert user signal dictionaries into 'iob_signal' objects
            replace_duplicate_signals_by_references(core.buses + core.ports, signals)
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
            iob_bus,
            kwargs,
            error_msg=f"Invalid {kwargs.get('name', '')} bus attribute '[arg]'!",
        )
        bus = iob_bus(*args, signals=sig_obj_list, interface=interface_obj, **kwargs)
        replace_duplicate_signals_by_references(core.buses + core.ports, bus.signals)
        core.buses.append(bus)
    except Exception:
        add_traceback_msg(f"Failed to create bus '{kwargs['name']}'.")
        raise


def get_bus_signal(core, bus_name: str, signal_name: str):
    """Return a signal reference from a given bus.
    param core: core object
    param bus_name: name of bus in the core's local bus list
    param signal_name: name of signal in the bus's signal list
    """
    bus = find_obj_in_list(core.buses, bus_name) or find_obj_in_list(
        core.ports, bus_name
    )
    if not bus:
        fail_with_msg(f"Could not find bus/port '{bus_name}'!")

    signal = find_obj_in_list(bus.signals, signal_name, process_func=get_real_signal)
    if not signal:
        fail_with_msg(
            f"Could not find signal '{signal_name}' of bus/port '{bus_name}'!"
        )

    return iob_signal_reference(signal=signal)


def replace_duplicate_signals_by_references(buses, signals):
    """Ensure that given list of 'signals' does not contain duplicates of other signals
    in the given 'buses' list, by replacing the duplicates with references to the
    original.
    param buses: list of buses with (original) signals
    param signals: list of new signals to be processed. If this list has a signal with
    the same name as another signal in the buses list, then this signal is replaced by a
    reference to the original.
    """
    for idx, signal in enumerate(signals):
        if isinstance(signal, iob_signal_reference):
            continue
        if type(signal) is iob_signal:
            signal = signal.__dict__
        original_signal = find_signal_in_buses(buses, signal["name"])
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


def find_signal_in_buses(buses, signal_name, process_func=get_real_signal):
    """Search for a signal in given list of buses
    param buses: list of buses
    param signal_name: name of signal to search for
    param process_func: function to process each signal before search
    """
    for bus in buses:
        signal = find_obj_in_list(bus.signals, signal_name, process_func=process_func)
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


# Dictionary of attributes that need to be preprocessed when set from a bus_dictionary, and their corresponding preprocessor functions
BUS_ATTRIBUTES_PREPROCESSOR_FUNCTIONS = {
    "signals": lambda lst: [signal_from_dict(i) for i in lst],
}

#
# API methods
#


def bus_from_dict(bus_dict):
    api_bus_obj = iob_bus()

    key_attribute_mapping = {}
    preprocessor_functions = BUS_ATTRIBUTES_PREPROCESSOR_FUNCTIONS
    # Update bus_obj attributes with values from given dictionary
    update_obj_from_dict(
        api_bus_obj._get_py2hwsw_internal_obj(),
        bus_dict,
        key_attribute_mapping,
        preprocessor_functions,
        api_bus_obj.get_supported_attributes().keys(),
    )

    return api_bus_obj


def bus_from_text(bus_text):
    bus_flags = [
        "name",
        ["-i", {"dest": "interface"}],
        ["-s", {"dest": "signals", "action": "append"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
    ]
    bus_dict = parse_short_notation_text(bus_text, bus_flags)
    bus_signals = []
    for s in bus_dict.get("signals", []):
        try:
            [s_name, s_width] = s.split(":")
        except ValueError:
            fail_with_msg(
                f"Invalid signal format '{s}'! Expected 'name:width' format.",
                ValueError,
            )
        bus_signals.append(signal_from_dict({"name": s_name, "width": s_width}))
    bus_dict.update({"signals": bus_signals})
    return iob_bus(**bus_dict)
