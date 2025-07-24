# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

import iob_interface
from iob_base import (
    find_obj_in_list,
    create_obj_list,
    fail_with_msg,
    add_traceback_msg,
    assert_attributes,
    parse_short_notation_text,
    empty_list,
)
from iob_wire import iob_wire, iob_wire_reference

get_real_wire = iob_wire.get_real_wire
create_wire_from_dict = iob_wire.create_wire_from_dict


@dataclass
class iob_bus:
    """
    Class to represent a bus in an iob module.

    Attributes:
        name (str): Identifier name for the bus.
        descr (str): Description of the bus.
        wires (list): List of wires belonging to this bus
                        (each wire represents a hardware Verilog bus).
    """

    name: str = ""
    descr: str = "Default description"
    wires: list[iob_wire] = empty_list()

    def get_wire(self, wire_name: str) -> iob_wire:
        """
        Find a wire by name and return it.

        Args:
            wire_name (str): Name of the wire to find

        Returns:
            iob_wire: The found wire.
        """
        pass

    def create_wires_from_interface(self):
        if not self.interface:
            fail_with_msg(f"Bus '{self.name}' has no interface!", ValueError)

        self.wires += self.interface.get_wires()

        # Remove wire direction information
        for wire in self.wires:
            # Skip wire references
            if isinstance(wire, iob_wire_reference):
                continue
            if hasattr(wire, "direction"):
                # Remove direction suffix from wire name
                if wire.name.endswith("_i") or wire.name.endswith("_o"):
                    wire.name = wire.name[:-2]
                elif wire.name.endswith("_io"):
                    wire.name = wire.name[:-3]
                wire.direction = ""

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("All buses must have a name!", ValueError)

    # attrs = [
    #     "name",
    #     ["-i", "wires&i", {"nargs": 1}, ("type",)],
    #     ["-s", "wires&s", {"nargs": "+"}, ["name:width"]],
    # ]
    #
    #
    #     @str_to_kwargs(attrs)
    @staticmethod
    def create_bus(core, *args, wires=[], **kwargs):
        """Creates a new bus object and adds it to the core's bus list
        param core: core object
        """
        try:
            # Ensure 'buses' list exists
            core.set_default_attribute("buses", [])
            # Check if there are any references to wires in other buses/ports
            sig_obj_list = []
            interface_obj = None
            if type(wires) is list:
                # Convert user wire dictionaries into 'iob_wire' objects
                __class__.replace_duplicate_wires_by_references(
                    core.buses + core.ports, wires
                )
                sig_obj_list = create_obj_list(wires, iob_wire)
            elif type(wires) is dict:
                # Convert user interface dictionary into '_interface' object
                interface_obj = __class__.dict2interface(
                    name=kwargs.get("name", ""), interface_dict=wires
                )
                if interface_obj and not interface_obj.file_prefix:
                    interface_obj.file_prefix = core.name + "_"
            else:
                fail_with_msg(f"Invalid wire type! {wires}", TypeError)
            assert_attributes(
                iob_bus,
                kwargs,
                error_msg=f"Invalid {kwargs.get('name', '')} bus attribute '[arg]'!",
            )
            bus = iob_bus(*args, wires=sig_obj_list, interface=interface_obj, **kwargs)
            __class__.replace_duplicate_wires_by_references(
                core.buses + core.ports, bus.wires
            )
            core.buses.append(bus)
        except Exception:
            add_traceback_msg(f"Failed to create bus '{kwargs['name']}'.")
            raise

    @staticmethod
    def get_bus_wire(core, bus_name: str, wire_name: str):
        """Return a wire reference from a given bus.
        param core: core object
        param bus_name: name of bus in the core's local bus list
        param wire_name: name of wire in the bus's wire list
        """
        bus = find_obj_in_list(core.buses, bus_name) or find_obj_in_list(
            core.ports, bus_name
        )
        if not bus:
            fail_with_msg(f"Could not find bus/port '{bus_name}'!")

        wire = find_obj_in_list(bus.wires, wire_name, process_func=get_real_wire)
        if not wire:
            fail_with_msg(
                f"Could not find wire '{wire_name}' of bus/port '{bus_name}'!"
            )

        return iob_wire_reference(wire=wire)

    @staticmethod
    def replace_duplicate_wires_by_references(buses, wires):
        """Ensure that given list of 'wires' does not contain duplicates of other wires
        in the given 'buses' list, by replacing the duplicates with references to the
        original.
        param buses: list of buses with (original) wires
        param wires: list of new wires to be processed. If this list has a wire with
        the same name as another wire in the buses list, then this wire is replaced by a
        reference to the original.
        """
        for idx, wire in enumerate(wires):
            if isinstance(wire, iob_wire_reference):
                continue
            if type(wire) is iob_wire:
                wire = wire.__dict__
            original_wire = __class__.find_wire_in_buses(buses, wire["name"])
            if not original_wire:
                continue
            original_wire = get_real_wire(original_wire)
            # print(f"[DEBUG] Replacing wire '{wire['name']}' by reference to original.")
            # Verify that new wire has same parameters as the original_wire
            for key, value in wire.items():
                if original_wire.__dict__[key] != value:
                    fail_with_msg(
                        f"Wire reference '{wire['name']}' has different '{key}' than the original wire!\n"
                        f"Original wire '{original_wire.name}' value: '{original_wire.__dict__[key]}'.\n"
                        f"Wire reference '{wire['name']}' value: '{value}'."
                    )
            # Replace wire by a reference to the original
            wires[idx] = iob_wire_reference(wire=original_wire)

    @staticmethod
    def find_wire_in_buses(buses, wire_name, process_func=get_real_wire):
        """Search for a wire in given list of buses
        param buses: list of buses
        param wire_name: name of wire to search for
        param process_func: function to process each wire before search
        """
        for bus in buses:
            wire = find_obj_in_list(bus.wires, wire_name, process_func=process_func)
            if wire:
                return wire
        return None

    #
    # Convert interface dictionary to an interface object
    # Note: This function is to be deprecated in the future, since objects should be created directly for
    # each interface type.
    #
    @staticmethod
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

        interface = iob_interface.create_interface(
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

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_bus_from_dict(bus_dict):
        """
        Function to create iob_bus object from dictionary attributes.

        Attributes:
            bus_dict (dict): dictionary with values to initialize attributes of iob_bus object.
                This dictionary supports the following keys corresponding to the iob_bus attributes:
                - name           -> iob_bus.name
                - descr          -> iob_bus.descr
                - wires        -> iob_bus.wires

        Returns:
            iob_bus: iob_bus object
        """
        # Convert dictionary elements to objects
        kwargs = bus_dict.copy()
        kwargs["wires"] = [create_wire_from_dict(i) for i in bus_dict.get("wires", [])]
        return iob_bus(**kwargs)

    @staticmethod
    def bus_text2dict(bus_text):
        bus_flags = [
            "name",
            ["-i", {"dest": "interface"}],
            ["-s", {"dest": "wires", "action": "append"}],
            ["-d", {"dest": "descr", "nargs": "?"}],
        ]
        bus_dict = parse_short_notation_text(bus_text, bus_flags)
        bus_wires = []
        for s in bus_dict.get("wires", []):
            try:
                [s_name, s_width] = s.split(":")
            except ValueError:
                fail_with_msg(
                    f"Invalid wire format '{s}'! Expected 'name:width' format.",
                    ValueError,
                )
            bus_wires.append({"name": s_name, "width": s_width})
        bus_dict.update({"wires": bus_wires})
        return bus_dict

    @staticmethod
    def create_bus_from_text(bus_text):
        """
        Function to create iob_bus object from short notation text.

        Attributes:
            bus_text (str): Short notation text. Object attributes are specified using the following format:
                name [-d descr] [-s wire_name1:width1] [-s wire_name2:width2]+
                Examples:
                    dbus -d 'data bus' -s wdata:32 -s wstrb:4

        Returns:
            iob_bus: iob_bus object
        """
        return __class__.create_bus_from_dict(__class__.bus_text2dict(bus_text))
