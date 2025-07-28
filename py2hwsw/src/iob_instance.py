# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
import os
import copy
import json

from iob_base import (
    iob_base,
    find_obj_in_list,
    fail_with_msg,
    debug_print,
    import_python_module,
    empty_list,
    empty_dict,
)
from iob_portmap import iob_portmap
from iob_wire import iob_wire
from iob_core import iob_core

get_portmap_port = iob_portmap.get_portmap_port
remove_direction_suffixes = iob_wire.remove_wire_direction_suffixes
find_module_setup_dir = iob_core.find_module_setup_dir


@dataclass
class iob_instance(iob_base):
    """
    Generic class to describe a module's instance.

    Attributes:
        core (str): Name of the core to instantiate.
        instance_name (str): Name of the instance. (Will be used as the instance's name in the Verilog module).
        instance_description (str): Description of the instance.
        portmap_connections (list): Instance portmap connections.
        parameters (dict): Verilog parameter values for this instance.
        instantiate (bool): Select if should intantiate the module inside another Verilog module.
    """

    # TODO: Make a new iob_instance class, independent from the iob_core class. Subblocks will instantiate iob_instance objects. Each iob_instance will store a reference to an iob_core.
    core: iob_core = None
    name: str = None
    description: str = "Default instance description"
    portmap_connections: list[str] = empty_list()
    parameters: dict[str, int | str] = empty_dict()
    instantiate: bool = True

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
            "name",
            "description",
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
        param connect: External buses to connect to ports of this instance
                       Key: Port name, Value: bus name or tuple with bus name and wire bit slices
                       Tuple has format:
                       (bus_name, wire_name[bit_start:bit_end], other_wire[bit_start:bit_end], ...)
        param issuer: Module that is instantiating this instance
        """
        # Connect instance ports to external buses
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
                bus_name = connection_value
            elif type(connection_value) is tuple:
                bus_name = connection_value[0]
                bit_slices = connection_value[1]
                if type(bit_slices) is not list:
                    fail_with_msg(
                        f"Second element of tuple must be a list of bit slices/connections: {connection_value}"
                    )
            else:
                fail_with_msg(f"Invalid connection value: {connection_value}")

            if "'" in bus_name or bus_name.lower() == "z":
                bus = bus_name
            else:
                bus = find_obj_in_list(issuer.buses, bus_name) or find_obj_in_list(
                    issuer.ports, bus_name
                )
                if not bus:
                    debug_print(
                        f"Creating implicit bus '{port.name}' in '{issuer.name}'.", 1
                    )
                    # Add bus to issuer
                    bus_wires = remove_wire_direction_suffixes(port.wires)
                    issuer.create_bus(name=bus_name, wires=bus_wires, descr=port.descr)
                    # Add bus to attributes_dict as well
                    issuer.attributes_dict["buses"].append(
                        {
                            "name": bus_name,
                            "wires": bus_wires,
                            "descr": port.descr,
                        }
                    )
                    bus = issuer.buses[-1]

            # create portmap and add to instance list
            portmap = iob_portmap(port=port)
            portmap.connect_external(bus, bit_slices=bit_slices)
            self.portmap_connections.append(portmap)

    @staticmethod
    def instantiate_block(
        block_name: str, iob_parameters: dict = {}, block_dict: dict = {}
    ):
        """
        Find a block based on given block_name and instatiate it.

        Attributes:
            block (str): The name of the block to instantiate. Will search for <block>.py or <block>.json files.
                        If <block>.py is found, it must contain a class called <block> that extends iob_block. This class will be used to instantiate the block.
                        If <block>.json is found, its contents will be read and parsed by the block_from_dict(<json_contents>) function.
            iob_parameters (dict): Optional. Dictionary of IOb parameters to pass to the instantiated block.
                                      Elements from this dictionary will be passed as **kwargs to the instantiated block's constructor.
                                      Only applicable if instantiated block has a constructor that accepts IOb parameters (excludes blocks defined in JSON or purely by dictionary).
            block_dict (dict): Dictionary of instance attributes to set on the instantiated block.
        Returns:
            iob_instance: The instantiated block object
        """
        block_dir, file_ext = find_module_setup_dir(block_name)

        if file_ext == ".py":
            debug_print(f"Importing {block_name}.py", 1)
            block_module = import_python_module(
                os.path.join(block_dir, f"{block_name}.py"),
            )

            # Instantiate block (call constructor from class defined inside the .py file)
            block_class = getattr(block_module, block_name)
            block_obj = block_class(**iob_parameters)

        elif file_ext == ".json":
            debug_print(f"Loading {block_name}.json", 1)
            block_obj = iob_core.create_from_dict(
                json.load(open(os.path.join(block_dir, f"{block_name}.json")))
            )

        # Create instance of block
        instance_obj = iob_instance(**block_dict, core=block_obj)

        # # Auto-set block attributes
        # if not block_obj.original_name:
        #     block_obj.original_name = block_name
        # if not block_obj.setup_dir:
        #     block_obj.setup_dir = block_dir

        return instance_obj

    #
    # Other Py2HWSW instance methods
    #

    @staticmethod
    def create_from_dict(instance_dict):
        """
        Function to create iob_instance object from dictionary attributes.

        Attributes:
            instance_dict (dict): dictionary with values to initialize attributes of iob_instance object.
                This dictionary supports the following keys corresponding to the iob_instance attributes:
                - core -> iob_instance.core
                - name -> iob_instance.name
                - description -> iob_instance.description
                - portmap_connections -> iob_instance.portmap_connections = iob_portmap.create_from_dict(portmap_connections)
                - parameters -> iob_instance.parameters
                - instantiate -> iob_instance.instantiate
                # Non-attribute instance keys
                - core (str): Optional. The name of the core to instantiate. Will search for <core>.py or <core>.json files.
                              If this key is set, all other keys will be ignored! (Except 'iob_parameters' key).
                              If <core>.py is found, it must contain a class called <core> that extends iob_core. This class will be used to instantiate the core.
                              If <core>.json is found, its contents will be read and parsed by the iob_core.create_from_dict(<json_contents>) function.
                - iob_parameters (dict): Optional. Dictionary of iob parameters to pass to the instantiated core.
                                            This key should be used in conjunction with the 'core' key.
                                            Elements from this dictionary will be passed as **kwargs to the instantiated core's constructor.
                                            Only applicable if instantiated core has a constructor that accepts IOb parameters (excludes cores defined in JSON or purely by dictionary).


        Returns:
            iob_instance: iob_instance object
        """
        # If 'instance' key is given, find corresponding instance and instantiate it. Ignore other non-instance attributes.
        # if instance_dict.get("instance", None):
        #     return instantiate_block(
        #         instance_dict["instance"],
        #         instance_dict.get("iob_parameters", {}),
        #         instance_dict,
        #     )
        # If 'core' key is given, find corresponding core and instantiate it. Ignore other non-instance attributes.

        # instantiate_block(instance_dict["core"], instance_dict.get("iob_parameters", {}), instance_dict)

        # instance_dict_with_objects["portmap_connections"] = iob_portmap.create_from_dict(instance_dictionary.get("portmap_connections", {}))
        # return iob_instance(**instance_dict)

        # remove non-attribute keys
        core = instance_dict.pop("core", "")
        iob_parameters = instance_dict.pop("iob_parameters", {})
        portmap_connections = instance_dict.pop("portmap_connections", {})
        instance_dict.update(
            {"portmap_connections": iob_portmap.create_from_dict(portmap_connections)}
        )
        return __class__.instantiate_block(core, iob_parameters, instance_dict)
