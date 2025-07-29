# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
import copy

from iob_base import fail_with_msg


@dataclass
class iob_wire:
    """
    Class that represents a core's py2hwsw wire.

    Attributes:
        name (str): Name for the wire inside the core. Verilog wire will be generated with this name.
        width (str or int): Number of bits in the wire.
        descr (str): Description of the wire.
        isvar (bool): If enabled, wire will be generated with type `reg` in Verilog.
    """

    name: str = ""
    width: str or int = 1
    descr: str = "Default description"
    isvar: bool = False

    # Undocumented. Used for `iob_comb`: If enabled, iob_comb will infer a register for this wire.
    isreg: bool = False
    # Undocumented. Used for `iob_comb`: List of wires associated to the infered register.
    reg_wires: list[str] = field(default_factory=list)

    def __post_init__(self):
        # print("DEBUG: Creating wire")
        pass

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Wire name is not set", ValueError)

    def get_verilog_bus(self):
        """Generate a verilog bus string from this wire"""
        if "'" in self.name or self.name.lower() == "z":
            return None
        bus_type = "reg" if self.isvar else "wire"
        width_str = "" if self.get_width_int() == 1 else f"[{self.width}-1:0] "
        return f"{bus_type} {width_str}{self.name};\n"

    def get_width_int(self):
        width_v = self.width
        try:
            return int(width_v)
        except ValueError:
            return width_v

    @staticmethod
    def remove_wire_direction_suffixes(wire_list):
        """Given a wire list (usually from a port) that includes direction suffixes in their names (like _i, _o, _io),
        return a new list with the suffixes removed"""
        new_list = copy.deepcopy(wire_list)
        for wire in new_list:
            wire.name = wire.name.rsplit("_", 1)[0]
        return new_list

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(wire_dict):
        """
        Function to create iob_wire object from dictionary attributes.

        Attributes:
            wire_dict (dict): dictionary with values to initialize attributes of iob_wire object.
                This dictionary supports the following keys corresponding to the iob_wire attributes:
                - name          -> iob_wire.name
                - width         -> iob_wire.width
                - descr         -> iob_wire.descr
                - isvar         -> iob_wire.isvar

        Returns:
            iob_wire: iob_wire object
        """
        return iob_wire(**wire_dict)
