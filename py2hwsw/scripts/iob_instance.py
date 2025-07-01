# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import copy
from typing import Dict

from iob_base import iob_base


class iob_instance(iob_base):
    """Class to describe a module's (Verilog) instance"""

    def __init__(
        self,
        *args,
        instance_name: str = None,
        instance_description: str = None,
        parameters: Dict = {},
        if_defined: str = None,
        if_not_defined: str = None,
        instantiate: bool = True,
        **kwargs,
    ):
        """Build a (Verilog) instance
        param parameters: Verilog parameter values for this instance
                          Key: Verilog parameter name, Value: Verilog parameter value
        """
        self.set_default_attribute(
            "instance_name",
            instance_name or self.__class__.__name__ + "_inst",
            str,
            descr="Name of the instance",
        )
        self.set_default_attribute(
            "instance_description",
            instance_description or "Default description",
            str,
            descr="Description of the instance",
        )
        # Verilog parameter values
        self.set_default_attribute(
            "parameters", parameters, Dict, descr="Verilog parameter values"
        )
        # Only use this instance in Verilog if this Verilog macro is defined
        self.set_default_attribute(
            "if_defined",
            if_defined,
            str,
            descr="Only use this instance in Verilog if this Verilog macro is defined",
        )
        # Only use this instance in Verilog if this Verilog macro is not defined
        self.set_default_attribute(
            "if_not_defined",
            if_not_defined,
            str,
            descr="Only use this instance in Verilog if this Verilog macro is not defined",
        )
        # Select if should intantiate inside another Verilog module.
        # May be False if this is a software only module.
        self.set_default_attribute(
            "instantiate",
            instantiate,
            bool,
            descr="Select if should intantiate the module inside another Verilog module.",
        )

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
            "parameters",
            "if_defined",
            "if_not_defined",
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
