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
                name=self.interface.type,
                if_type="",
                mult=self.interface.mult,
                params=self.interface.params,
                widths=self.interface.widths,
                signal_prefix=self.interface.prefix,
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
            # Convert user interface dictionary into 'if_gen.interface' object
            interface_obj = dict2interface(signals)
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
def dict2interface(interface_dict):
    """Convert dictionary to an interface.
    Example interface dict:
    {
        "name": "cpu_m",
        "descr": "cpu instruction bus",
        "signals": {
            "type": "iob",
            # Generic string parameter
            "params": "",
            # Widths/Other parameters
            "DATA_W": "DATA_W",
            "ADDR_W": "ADDR_W",
        },
    },
    To use an assymmetric memory interface, the dictionary should look like this:
    {
        "name": "mem_m",
        "descr": "Memory interface",
        "signals": {
            "type": "ram_at2p",
            # Generic string parameter
            "params": "",
            # Widths/Other parameters
            "ADDR_W": "ADDR_W",
            "W_DATA_W": "W_DATA_W",
            "R_DATA_W": "R_DATA_W",
        },
    """
    if not interface_dict:
        return None

    signals_dict = interface_dict.get("signals", {})

    if "type" not in signals_dict:
        raise ValueError("Interface dictionary must contain a 'type' key.")

    type = signals_dict["type"]
    prefix = signals_dict.get("prefix", "")
    mult = signals_dict.get("mult", 1)
    params = signals_dict.get("params", None)
    params = params.split("_")
    file_prefix = signals_dict.get("file_prefix", "")
    portmap_port_prefix = signals_dict.get("portmap_port_prefix", "")
    # Remaining entries in the interface_dict
    remaining_entries = {
        k: v
        for k, v in signals_dict.items()
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

    # Retrieve widths and parameters even if not needed
    # IOb
    data_w = remaining_entries.get("DATA_W", 32)
    addr_w = remaining_entries.get("ADDR_W", 32)
    # Memory
    w_data_w = remaining_entries.get("W_DATA_W", 32)
    r_data_w = remaining_entries.get("R_DATA_W", 32)
    # AXI
    id_w = remaining_entries.get("ID_W", 1)
    size_w = remaining_entries.get("SIZE_W", 3)
    burst_w = remaining_entries.get("BURST_W", 2)
    lock_w = remaining_entries.get("LOCK_W", 2)
    cache_w = remaining_entries.get("CACHE_W", 4)
    prot_w = remaining_entries.get("PROT_W", 3)
    qos_w = remaining_entries.get("QOS_W", 4)
    resp_w = remaining_entries.get("RESP_W", 2)
    len_w = remaining_entries.get("LEN_W", 8)
    # AXIStream
    has_tlast = "tlast" in params
    # AHB
    ahb_prot_w = remaining_entries.get("AHB_PROT_W", 4)
    ahb_burst_w = remaining_entries.get("AHB_BURST_W", 3)
    ahb_trans_w = remaining_entries.get("AHB_TRANS_W", 2)
    ahb_size_w = remaining_entries.get("AHB_SIZE_W", 3)
    # rs232
    n_pins = remaining_entries.get("N_PINS", 4)

    # Check if widths are integers
    if not isinstance(data_w, int):
        raise ValueError("DATA_W must be an integer.")
    if not isinstance(addr_w, int) and not isinstance(addr_w, str):
        raise ValueError("ADDR_W must be an integer or a string.")
    if not isinstance(w_data_w, int):
        raise ValueError("W_DATA_W must be an integer.")
    if not isinstance(r_data_w, int):
        raise ValueError("R_DATA_W must be an integer.")
    if not isinstance(id_w, int):
        raise ValueError("ID_W must be an integer.")
    if not isinstance(size_w, int):
        raise ValueError("SIZE_W must be an integer.")
    if not isinstance(burst_w, int):
        raise ValueError("BURST_W must be an integer.")
    if not isinstance(lock_w, int):
        raise ValueError("LOCK_W must be an integer.")
    if not isinstance(cache_w, int):
        raise ValueError("CACHE_W must be an integer.")
    if not isinstance(prot_w, int):
        raise ValueError("PROT_W must be an integer.")
    if not isinstance(qos_w, int):
        raise ValueError("QOS_W must be an integer.")
    if not isinstance(resp_w, int):
        raise ValueError("RESP_W must be an integer.")
    if not isinstance(len_w, int):
        raise ValueError("LEN_W must be an integer.")

    match type:
        case "iob_clk":
            # Check the params for the IOb clock interface
            has_cke = False
            has_arst = False
            has_rst = False
            has_en = False
            for param in params:
                if param == "c":
                    has_cke = True
                elif param == "a":
                    has_arst = True
                elif param == "r":
                    has_rst = True
                elif param == "e":
                    has_en = True
                else:
                    raise ValueError(
                        f"Unknown parameter '{param}' for IOb clock interface."
                    )

            interface = IobClkInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                has_cke=has_cke,
                has_arst=has_arst,
                has_rst=has_rst,
                has_en=has_en,
            )
        case "iob":
            interface = IobInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
            )
        case mem if mem in mem_if_names:
            if "W_DATA_W" in remaining_entries and "R_DATA_W" in remaining_entries:
                interface = AsymMemInterface(
                    prefix=prefix,
                    mult=mult,
                    file_prefix=file_prefix,
                    portmap_port_prefix=portmap_port_prefix,
                    addr_w=remaining_entries.get("ADDR_W", 32),
                    type=type,
                    w_data_w=w_data_w,
                    r_data_w=r_data_w,
                )
            else:
                # Symmetric memory interface
                interface = SymMemInterface(
                    prefix=prefix,
                    mult=mult,
                    file_prefix=file_prefix,
                    portmap_port_prefix=portmap_port_prefix,
                    addr_w=addr_w,
                    type=type,
                    data_w=data_w,
                )
        case "axis":
            interface = AXIStreamInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                has_tlast=has_tlast,
            )
        case "axil_read":
            interface = AXILiteInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                prot_w=prot_w,
                resp_w=resp_w,
                has_write_if=False,
                has_prot="PROT_W" in remaining_entries,
            )
        case "axil_write":
            interface = AXIInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                prot_w=prot_w,
                resp_w=resp_w,
                has_read_if=False,
                has_prot="PROT_W" in remaining_entries,
            )
        case "axil":
            interface = AXILiteInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                prot_w=prot_w,
                resp_w=resp_w,
            )
        case "axi_read":
            interface = AXIInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                id_w=id_w,
                size_w=size_w,
                burst_w=burst_w,
                lock_w=lock_w,
                cache_w=cache_w,
                prot_w=prot_w,
                qos_w=qos_w,
                resp_w=resp_w,
                len_w=len_w,
                has_write_if=False,
            )
        case "axi_write":
            interface = AXIInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                id_w=id_w,
                size_w=size_w,
                burst_w=burst_w,
                lock_w=lock_w,
                cache_w=cache_w,
                prot_w=prot_w,
                qos_w=qos_w,
                resp_w=resp_w,
                len_w=len_w,
                has_read_if=False,
            )
        case "axi":
            interface = AXIInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                id_w=id_w,
                size_w=size_w,
                burst_w=burst_w,
                lock_w=lock_w,
                cache_w=cache_w,
                prot_w=prot_w,
                qos_w=qos_w,
                resp_w=resp_w,
                len_w=len_w,
            )
        case "apb":
            interface = APBInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
            )
        case "ahb":
            interface = AHBInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                prot_w=ahb_prot_w,
                burst_w=ahb_burst_w,
                trans_w=ahb_trans_w,
                size_w=ahb_size_w,
            )
        case "rs232":
            interface = RS232Interface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                n_pins=n_pins,
            )
        case "wb":
            interface = WishboneInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
            )
        case "wb_full":
            interface = WishboneInterface(
                prefix=prefix,
                mult=mult,
                file_prefix=file_prefix,
                portmap_port_prefix=portmap_port_prefix,
                data_w=data_w,
                addr_w=addr_w,
                is_full=True,
            )
        case _:
            raise ValueError(f"Unknown interface type: {type}")

    return interface
