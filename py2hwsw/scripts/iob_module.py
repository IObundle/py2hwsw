# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from iob_base import iob_base, process_elements_from_list
from iob_conf import create_conf_group
from iob_port import create_port
from iob_wire import create_wire, get_wire_signal
from iob_snippet import create_snippet
from iob_comb import iob_comb, create_comb
from iob_fsm import iob_fsm, create_fsm
from iob_block import create_block_group, iob_block_group


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
            get_list_attr_handler(self.create_conf_group),
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
            "subblocks",
            [],
            list,
            get_list_attr_handler(self.create_subblock_group),
            "List of instances of other cores inside this core.",
        )
        # List of wrappers for this core
        self.set_default_attribute(
            "superblocks",
            [],
            list,
            get_list_attr_handler(self.create_superblock_group),
            "List of wrappers for this core. Will only be setup if this core is a top module, or a wrapper of the top module.",
        )
        # List of software modules required by this core
        self.set_default_attribute(
            "sw_modules",
            [],
            list,
            get_list_attr_handler(self.create_sw_instance_group),
            "List of software modules required by this core.",
        )

    def create_conf_group(self, *args, **kwargs):
        create_conf_group(self, *args, **kwargs)

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

    def create_superblock_group(self, *args, **kwargs):
        kwargs.pop("instantiate", None)
        create_block_group(
            self,
            *args,
            instantiate=False,
            is_superblock=True,
            blocks_attribute_name="superblocks",
            **kwargs
        )

    def create_subblock_group(self, *args, **kwargs):
        if self.is_superblock:
            # Remove instantiator subblock from the group to ensure that it is not setup again
            if self.handle_instantiator_subblock(*args, **kwargs):
                return
        create_block_group(self, *args, **kwargs)

    def create_sw_instance_group(self, *args, **kwargs):
        kwargs.pop("instantiate", None)
        self.create_subblock_group(*args, instantiate=False, **kwargs)

    def update_global_top_module(self):
        """Update global top module if it has not been set before.
        The first module to call this method is the global top module.
        """
        if not __class__.global_top_module:
            __class__.global_top_module = self

    def handle_instantiator_subblock(self, *args, **kwargs):
        """If given kwargs describes the instantiator subblock, return True. Otherwise return False.
        If given kwargs describes a group of blocks that contains the instantiator subblock, then remove it from that list.
        Also append instantiator object found to the core's 'subblocks' list.
        """
        blocks = kwargs.pop("blocks", None)
        instantiator = kwargs.get("instantiator", None)
        if blocks is None and kwargs.get("core_name") == instantiator.original_name:
            self.append_instantiator_subblock_to_list(kwargs)
            return True

        for idx, block in blocks:
            if block["core_name"] == instantiator.original_name:
                self.append_instantiator_subblock_to_list(block)
                del blocks[idx]
                break

        return False

    def append_instantiator_subblock_to_list(self, instantiator_subblock):
        """Create a block group for instantiator subblock, and append it to the subblocks list"""
        self.subblocks.append(
            iob_block_group(
                name="instantiator_subblock",
                descr="Block group for instantiator subblock (the subblock that uses this one as a superblock)",
                blocks=instantiator_subblock,
            )
        )


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
