# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from iob_base import iob_base, process_elements_from_list
from iob_conf import create_conf
from iob_port import create_port
from iob_wire import create_wire, get_wire_signal
from iob_snippet import create_snippet
from iob_comb import iob_comb, create_comb
from iob_fsm import iob_fsm, create_fsm


class iob_module(iob_base):
    """Class to describe a (Verilog) module"""

    global_top_module = None  # Datatype is 'iob_module'

    def __init__(self, *args, **kwargs):
        # Original name of the module.
        # (The module name commonly used in the files of the setup dir.)
        self.set_default_attribute(
            "original_name",
            "",
            str,
            descr="Original name of the module. (The module name commonly used in the files of the setup dir.)",
        )
        # Name of the generated module
        self.set_default_attribute(
            "name", "", str, descr="Name of the generated module."
        )
        self.set_default_attribute(
            "description",
            "Default description",
            str,
            descr="Description of the module",
        )
        # List of module macros and Verilog (false-)parameters
        self.set_default_attribute(
            "confs",
            [],
            list,
            get_list_attr_handler(self.create_conf),
            "List of module macros and Verilog (false-)parameters.",
        )
        self.set_default_attribute(
            "ports",
            [],
            list,
            get_list_attr_handler(self.create_port),
            "List of module ports.",
        )
        self.set_default_attribute(
            "wires",
            [],
            list,
            get_list_attr_handler(self.create_wire),
            "List of module wires.",
        )
        # List of core Verilog snippets
        self.set_default_attribute(
            "snippets",
            [],
            list,
            get_list_attr_handler(self.create_snippet),
            "List of core Verilog snippets.",
        )
        # List of core Verilog combinatory circuits
        self.set_default_attribute(
            "comb",
            None,
            iob_comb,
            lambda y: self.create_comb(**y),
            "Verilog combinatory circuit.",
        )
        # List of core Verilog finite state machines
        self.set_default_attribute(
            "fsm",
            None,
            iob_fsm,
            lambda y: self.create_fsm(**y),
            "Verilog finite state machine.",
        )
        # List of instances of other cores inside this core
        self.set_default_attribute(
            "blocks",
            [],
            list,
            get_list_attr_handler(self.create_instance),
            "List of instances of other cores inside this core.",
        )
        # List of software modules required by this core
        self.set_default_attribute(
            "sw_modules",
            [],
            list,
            get_list_attr_handler(self.create_sw_instance),
            "List of software modules required by this core.",
        )

    def create_conf(self, *args, **kwargs):
        create_conf(self, *args, **kwargs)

    def create_port(self, *args, **kwargs):
        create_port(self, *args, **kwargs)

    def create_wire(self, *args, **kwargs):
        create_wire(self, *args, **kwargs)

    def get_wire_signal(self, *args, **kwargs):
        return get_wire_signal(self, *args, **kwargs)

    def create_snippet(self, *args, **kwargs):
        create_snippet(self, *args, **kwargs)

    def create_comb(self, *args, **kwargs):
        create_comb(self, *args, **kwargs)

    def create_fsm(self, *args, **kwargs):
        create_fsm(self, *args, **kwargs)

    def create_instance(self, **kwargs):
        """Import core and create an instance of it inside this module"""
        # Method body implemented in subclass

    def create_sw_instance(self, **kwargs):
        """Import core and run its setup process"""
        # Setup process is equal to normal core, but should not be instantiated in Verilog
        self.create_instance(instantiate=False, **kwargs)

    def update_global_top_module(self):
        """Update global top module if it has not been set before.
        The first module to call this method is the global top module.
        """
        if not __class__.global_top_module:
            __class__.global_top_module = self


def get_list_attr_handler(func):
    """Returns a handler function to set attributes from a list using the function given
    The returned function has the format:
        returned_func(x), where x is a list of elements, likely in the 'py2hw' syntax.
    This 'returned_func' will run the given 'func' on each element of the list 'x'
    """
    return lambda x: process_elements_from_list(
        x,
        # 'y' is a dictionary describing an object in py2hw syntax
        # '**y' is used to unpack the dictionary and pass it as arguments to 'func'
        lambda y: (func(**y) if isinstance(y, dict) else func(y)),
    )
