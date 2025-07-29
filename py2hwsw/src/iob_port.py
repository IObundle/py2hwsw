# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import fail_with_msg
from iob_wire import iob_wire


@dataclass
class iob_port:
    """
    Describes an IO port.

    Attributes:
        wire (iob_wire): Reference to the wire that is connected to the port.
        direction (str): Port direction
        doc_only (bool): Only add to documentation
        doc_clearpage (bool): If enabled, the documentation table for this port will be terminated by a TeX '\clearpage' command.
    """

    wire: iob_wire = None
    direction: str = ""
    doc_only: bool = False
    doc_clearpage: bool = False

    def validate_attributes(self):
        if not self.wire:
            fail_with_msg("Port not associated to wire!")
        if self.direction not in ["input", "output", "inout"]:
            fail_with_msg(f"Missing direction for port {self.wire.name}!")

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

    @staticmethod
    def port_obj_list_process(port):
        """Process ports for `find_obj_in_list()`"""
        return port.wire

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(port_dict):
        """
        Function to create iob_port object from dictionary attributes.

        Attributes:
            port_dict (dict): dictionary with values to initialize attributes of iob_port object.
                This dictionary supports the following keys corresponding to the iob_port attributes:
                - wire -> iob_port.wire
                - doc_only -> iob_port.doc_only
                - doc_clearpage -> iob_port.doc_clearpage

        Returns:
            iob_port: iob_port object
        """
        # Create a wire for this port
        iob_wire_obj = iob_wire(name=port_dict["name"], width=port_dict["width"])

        # Get port direction form name suffix
        dir_suffix = port_dict["name"].split("_")[-1]
        dirs = {"i": "input", "o": "output", "io": "inout"}

        return iob_port(wire=iob_wire_obj, direction=dirs[dir_suffix])
