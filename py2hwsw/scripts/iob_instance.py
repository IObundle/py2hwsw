# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import copy
from typing import Dict

import interfaces
from iob_base import (
    iob_base,
    find_obj_in_list,
    fail_with_msg,
    debug_print,
    prevent_instantiation,
)
from iob_portmap import iob_portmap, get_portmap_port
from iob_signal import remove_signal_direction_suffixes
from api_base import internal_api_class, convert2internal


@internal_api_class("user_api.api", "iob_instance")
class iob_instance(iob_base):
    """Class to describe a module's (Verilog) instance"""

    def validate_attributes(self):
        """Validate instance attributes"""
        if not self.name:
            fail_with_msg("Instance must have a name!")
        if not self.core:
            fail_with_msg(f"Instance '{self.name}' has no core reference!")
        pass

    # def __init__(
    #     self,
    #     *args,
    #     instance_name: str = None,
    #     instance_description: str = None,
    #     connect: Dict = {},
    #     parameters: Dict = {},
    #     instantiate: bool = True,
    #     **kwargs,
    # ):
    #     """Build a (Verilog) instance
    #     param parameters: Verilog parameter values for this instance
    #                       Key: Verilog parameter name, Value: Verilog parameter value
    #     """
    #     self.set_default_attribute(
    #         "instance_name",
    #         instance_name or self.__class__.__name__ + "_inst",
    #         str,
    #         descr="Name of the instance",
    #         copy_by_reference=False,
    #     )
    #     self.set_default_attribute(
    #         "instance_description",
    #         instance_description or "Default description",
    #         str,
    #         descr="Description of the instance",
    #         copy_by_reference=False,
    #     )
    #     # Instance portmap connections
    #     self.set_default_attribute(
    #         "portmap_connections", [], list, descr="Instance portmap connections",
    #         copy_by_reference=False,
    #     )
    #     # Verilog parameter values
    #     self.set_default_attribute(
    #         "parameters", parameters, Dict, descr="Verilog parameter values",
    #         copy_by_reference=False,
    #     )
    #     # Select if should intantiate inside another Verilog module.
    #     # May be False if this is a software only module.
    #     self.set_default_attribute(
    #         "instantiate",
    #         instantiate,
    #         bool,
    #         descr="Select if should intantiate the module inside another Verilog module.",
    #         copy_by_reference=False,
    #     )

    def __deepcopy__(self, memo):
        """Create a deep copy of this instance:
        - iob_instance attributes are copied by value
        - super() attributes are copied by reference
        """
        # Create a new instance without calling __init__ to avoid side effects
        cls = self.__class__
        new_obj = cls.__new__(cls)

        # Add to memo to handle circular references
        memo[id(self)] = new_obj

        # Copy class iob_instance attributes by value (deep copy)
        instance_attributes = {
            "instance_name",
            "instance_description",
            "portmap_connections",
            "parameters",
            "instantiate",
        }

        for attr_name, attr_value in self.__dict__.items():
            if attr_name in instance_attributes:
                # Deep copy iob_instance attributes
                setattr(new_obj, attr_name, copy.deepcopy(attr_value, memo))
            else:
                # Copy inherited attributes by reference (shallow copy)
                setattr(new_obj, attr_name, attr_value)

        return new_obj

    def connect_instance_ports(self, connect, issuer):
        """
        param connect: External wires to connect to ports of this instance
                       Key: Port name, Value: Wire name or tuple with wire name and signal bit slices
                       Tuple has format:
                       (wire_name, signal_name[bit_start:bit_end], other_signal[bit_start:bit_end], ...)
        param issuer: Module that is instantiating this instance
        """
        # Connect instance ports to external wires
        for port_name, connection_value in connect.items():
            port = find_obj_in_list(self.ports, port_name)
            if not port:
                fail_with_msg(
                    f"Port '{port_name}' not found in instance '{self.instance_name}' of module '{issuer.name}'!\n"
                    f"Available ports:\n- "
                    + "\n- ".join([port.name for port in self.ports])
                )

            bit_slices = []
            if type(connection_value) is str:
                wire_name = connection_value
            elif type(connection_value) is tuple:
                wire_name = connection_value[0]
                bit_slices = connection_value[1]
                if type(bit_slices) is not list:
                    fail_with_msg(
                        f"Second element of tuple must be a list of bit slices/connections: {connection_value}"
                    )
            else:
                fail_with_msg(f"Invalid connection value: {connection_value}")

            if "'" in wire_name or wire_name.lower() == "z":
                wire = wire_name
            else:
                wire = find_obj_in_list(issuer.wires, wire_name) or find_obj_in_list(
                    issuer.ports, wire_name
                )
                if not wire:
                    debug_print(
                        f"Creating implicit wire '{port.name}' in '{issuer.name}'.", 1
                    )
                    # Add wire to issuer
                    wire_signals = remove_signal_direction_suffixes(port.signals)
                    issuer.create_wire(
                        name=wire_name, signals=wire_signals, descr=port.descr
                    )
                    # Add wire to attributes_dict as well
                    issuer.attributes_dict["wires"].append(
                        {
                            "name": wire_name,
                            "signals": wire_signals,
                            "descr": port.descr,
                        }
                    )
                    wire = issuer.wires[-1]

            # create portmap and add to instance list
            portmap = iob_portmap(port=port)
            portmap.connect_external(wire, bit_slices=bit_slices)
            self.portmap_connections.append(portmap)
        # If this module has an issuer and is not a tester
        if issuer and not self.is_tester:
            for port in self.ports:
                if (
                    not find_obj_in_list(
                        self.portmap_connections, port.name, get_portmap_port
                    )
                    and port.interface
                ):
                    if isinstance(
                        port.interface, interfaces.symMemInterface
                    ) or isinstance(port.interface, interfaces.asymMemInterface):
                        self.__connect_memory(port, issuer)
                    elif isinstance(port.interface, interfaces.iobClkInterface):
                        self.__connect_clk_interface(port, issuer)

        # iob_csrs specific code
        if self.original_name == "iob_csrs" and issuer:
            self.__connect_cbus_port(issuer)

    def __connect_memory(self, port, issuer):
        """Create memory port in issuer and connect it to self"""
        if not issuer.generate_hw or not self.instantiate:
            return
        _name = f"{port.name}"
        issuer.add_interface_port(
            name=_name, interface=port.interface, descr=port.descr
        )
        # Translate interface to a dictionary (TODO: remove along with attributes_dict)
        interface_dict = {
            "type": port.interface.genre,
            "prefix": port.interface.prefix,
            "mult": port.interface.mult,
            "file_prefix": port.interface.file_prefix,
            "portmap_port_prefix": port.interface.portmap_port_prefix,
            "ADDR_W": port.interface.addr_w,
        }
        if isinstance(port.interface, interfaces.symMemInterface):
            # If symmetric memory, add 'DATA_W'
            interface_dict["DATA_W"] = port.interface.data_w
        elif isinstance(port.interface, interfaces.asymMemInterface):
            # If asymmetric memory, add 'W_DATA_W' and 'R_DATA_W'
            interface_dict["W_DATA_W"] = port.interface.w_data_w
            interface_dict["R_DATA_W"] = port.interface.r_data_w
        # Add port also to attributes_dict
        issuer.attributes_dict["ports"].append(
            {
                "name": _name,
                "signals": interface_dict,
                "descr": port.descr,
            }
        )
        # Connect newly created port to self
        mem_portmap = iob_portmap(port=port)
        _port = find_obj_in_list(issuer.ports + issuer.wires, _name)
        mem_portmap.connect_external(_port, bit_slices=[])
        self.portmap_connections.append(mem_portmap)

    def __connect_clk_interface(self, port, issuer):
        """Create, if needed, a clock interface port in issuer and connect it to self"""
        if not issuer.generate_hw or not self.instantiate:
            return
        _name = f"{port.name}"

        # create new clk portmap
        clk_portmap = iob_portmap(port=port)
        self.portmap_connections.append(clk_portmap)

        for p in issuer.ports:
            if isinstance(p.interface, interfaces.iobClkInterface):
                # If interface is the same, connect it and add parameters if needed
                if p.interface.prefix == port.interface.prefix:
                    p.interface.has_cke |= port.interface.has_cke
                    p.interface.has_arst |= port.interface.has_arst
                    p.interface.has_rst |= port.interface.has_rst
                    p.interface.has_en |= port.interface.has_en
                    p.signals = []
                    p.__post_init__()  # FIXME: no longer exists
                    clk_portmap.connect_external(p, bit_slices=[])
                    return

        issuer.add_interface_port(
            name=_name, interface=port.interface, descr=port.descr
        )
        _port = find_obj_in_list(issuer.ports, _name)
        clk_portmap.connect_external(_port, bit_slices=[])

    def __connect_cbus_port(self, issuer):
        """Automatically adds "<prefix>_cbus_s" port to issuers of iob_csrs (are usually iob_system peripherals).
        The '<prefix>' is replaced by instance name of iob_csrs subblock.
        Also, connects the newly created issuer port to the iob_csrs `control_if_s` port.
        :param issuer: issuer core object
        """
        assert (
            self.original_name == "iob_csrs"
        ), "Internal error: cbus can only be created for issuer of 'iob_csrs' module."
        # Find CSR control port in iob_csrs, and copy its properites to a newly generated "<prefix>_cbus_s" port of issuer
        csrs_port = find_obj_in_list(self.ports, "control_if_s")

        # Copy interface from csrs_port to create a new interface and set its prefix
        new_interface = copy.deepcopy(csrs_port.interface)
        new_interface.prefix = self.instance_name + "_"

        issuer.add_interface_port(
            name=f"{self.instance_name}_cbus_s",
            interface=new_interface,
            descr="Control and Status Registers interface (auto-generated)",
        )
        # Connect newly created port to self
        csrs_portmap = iob_portmap(port=csrs_port)
        csrs_portmap.connect_external(issuer.ports[-1], bit_slices=[])
        self.portmap_connections.append(csrs_portmap)

        # TODO: Remove attributes_dict from the system
        # Add port to instantiator's attributes_dict
        csr_if_genre = "iob_clk"
        if isinstance(csrs_port.interface, interfaces.AXILiteInterface):
            csr_if_genre = "axil"
        if isinstance(csrs_port.interface, interfaces.APBInterface):
            csr_if_genre = "apb"

        # Add port to issuer's attributes_dict
        issuer.attributes_dict["ports"].append(
            {
                "name": f"{self.instance_name}_cbus_s",
                "signals": {
                    "type": csr_if_genre,
                    "prefix": self.instance_name + "_",
                    "DATA_W": csrs_port.interface.data_w,
                    "ADDR_W": csrs_port.interface.addr_w,
                },
                "descr": "Control and Status Registers interface (auto-generated)",
            }
        )
