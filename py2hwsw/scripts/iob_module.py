# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from iob_base import iob_base, process_elements_from_list, fail_with_msg
from iob_conf import create_conf_group
from iob_port import create_port
from iob_wire import create_wire, get_wire_signal
from iob_snippet import create_snippet
from iob_globals import iob_globals, create_globals
from iob_comb import iob_comb, create_comb
from iob_fsm import iob_fsm, create_fsm
from iob_block import create_block_group, iob_block_group


class iob_module(iob_base):
    """Class to describe a (Verilog) module"""

    global_top_module = None  # Datatype is 'iob_module'

    def set_rst_polarity(self, polarity):
        if self.is_top_module:
            create_globals(self, "reset_polarity", polarity)
        else:
            if polarity != getattr(iob_globals(), "reset_polarity", "positive"):
                fail_with_msg(
                    f"Reset polarity '{polarity}' is not the same as global reset polarity '{getattr(iob_globals(), 'reset_polarity', 'positive')}'."
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
            **kwargs,
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
        instantiator = self.instantiator
        if blocks is None and kwargs.get("core_name") == instantiator.original_name:
            self.update_instantiator_obj(instantiator, kwargs)
            return True

        if blocks:
            for idx, block in blocks:
                if block["core_name"] == instantiator.original_name:
                    self.update_instantiator_obj(instantiator, block)
                    del blocks[idx]
                    break

        return False

    def update_instantiator_obj(self, instantiator_obj, instance_dict):
        """Update given instantiator object with values for verilog parameters and external port connections.
        Also, add instantiator object to the 'subblocks' list of this superblock.
        :param instantiator_obj: Instantiator object
        :param instance_dict: Dictionary describing verilog instance. Includes port connections and verilog parameter values.
        """
        instantiator_obj.instantiate = True
        # Set instance name
        if "instance_name" in instance_dict:
            instantiator_obj.instance_name = instance_dict["instance_name"]
        # Set instance description
        if "instance_description" in instance_dict:
            instantiator_obj.instance_description = instance_dict[
                "instance_description"
            ]
        # Set values to pass via verilog parameters
        instantiator_obj.parameters = instance_dict.get("parameters", {})
        # Connect ports of instantiator to external wires (wires of this superblock)
        instantiator_obj.connect_instance_ports(instance_dict.get("connect", {}), self)
        # Create a block group dedicated for instantiator subblock, and add it to the 'subblocks' list of current superblock
        self.subblocks.append(
            iob_block_group(
                name="instantiator_subblock",
                descr="Block group for instantiator subblock (the subblock that uses this one as a superblock)",
                blocks=[instantiator_obj],
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
