# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import copy

from iob_base import (
    add_traceback_msg,
    debug_print,
    fail_with_msg,
    iob_base,
    process_elements_from_list,
)
from iob_globals import iob_globals

create_globals = iob_globals.create_globals


class iob_module(iob_base):
    """Class to describe a (Verilog) module"""

    global_top_module = None  # Datatype is 'iob_module'

    def __init__(self):
        # Auto-fill global attributes
        if not __class__.global_top_module:
            __class__.global_top_module = self

    def set_rst_polarity(self, polarity):
        if self.is_top_module:
            create_globals(self, "reset_polarity", polarity)
        else:
            if polarity != getattr(iob_globals(), "reset_polarity", "positive"):
                fail_with_msg(
                    f"Reset polarity '{polarity}' is not the same as global reset polarity '{getattr(iob_globals(), 'reset_polarity', 'positive')}'."
                )

    def create_superblock(self, *args, **kwargs):
        kwargs.pop("instantiate", None)
        create_block(
            self,
            *args,
            instantiate=False,
            is_superblock=True,
            blocks_attribute_name="superblocks",
            **kwargs,
        )

    def create_subblock(self, *args, **kwargs):
        if self.is_superblock:
            # Remove issuer subblock to ensure that it is not setup again
            if self.handle_issuer_subblock(*args, **kwargs):
                return
        create_block(self, *args, **kwargs)

    def create_sw_instance(self, *args, **kwargs):
        kwargs.pop("instantiate", None)
        self.create_subblock(*args, instantiate=False, **kwargs)

    def update_global_top_module(self):
        """Update global top module if it has not been set before.
        The first module to call this method is the global top module.
        """
        if not __class__.global_top_module:
            __class__.global_top_module = self

    def handle_issuer_subblock(self, *args, **kwargs):
        """If given kwargs describes the issuer subblock, return True. Otherwise return False.
        Also append issuer object found to the core's 'subblocks' list.
        """
        issuer = self.issuer
        if kwargs.get("core_name") == issuer.original_name:
            self.update_issuer_obj(issuer, kwargs)
            return True
        else:
            return False

    def update_issuer_obj(self, issuer_obj, instance_dict):
        """Update given issuer object with values for verilog parameters and external port connections.
        Also, add issuer object to the 'subblocks' list of this superblock.
        :param issuer_obj: issuer object
        :param instance_dict: Dictionary describing verilog instance. Includes port connections and verilog parameter values.
        """
        new_issuer_instance = copy.deepcopy(issuer_obj)
        new_issuer_instance.instantiate = True
        # Set instance name
        if "instance_name" in instance_dict:
            new_issuer_instance.instance_name = instance_dict["instance_name"]
        # Set instance description
        if "instance_description" in instance_dict:
            new_issuer_instance.instance_description = instance_dict[
                "instance_description"
            ]
        # Set values to pass via verilog parameters
        new_issuer_instance.parameters = instance_dict.get("parameters", {})
        # Connect ports of issuer to external buses (buses of this superblock)
        new_issuer_instance.connect_instance_ports(
            instance_dict.get("connect", {}), self
        )
        # Create a issuer subblock, and add it to the 'subblocks' list of current superblock
        self.subblocks.append(new_issuer_instance)


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


def create_block(
    core,
    core_name: str = "",
    instance_name: str = "",
    blocks_attribute_name="subblocks",
    **kwargs,
):
    """Create an instante of a module, but only if we are not using a
    project wide special target (like clean)
    param core_name: Name of the core
    param instance_name: Verilog instance name
    """
    # Create "iob_csrs" even when abort_reason is "ipxact_gen" in order to create CSRs memory map
    # Skip all other blocks
    if core.abort_reason and not (
        core.abort_reason == "ipxact_gen" and core_name == "iob_csrs"
    ):
        return
    # Don't setup other destinations (like simulation) if this is a submodule and
    # the sub-submodule (we are trying to setup) is not for hardware/src/
    if (
        not core.is_top_module
        and not core.is_superblock
        and (
            core.dest_dir == "hardware/src"
            and "dest_dir" in kwargs
            and kwargs["dest_dir"] != "hardware/src"
        )
    ):
        debug_print(f"Not setting up submodule '{core_name}' of '{core.name}' core!", 1)
        return

    assert core_name, fail_with_msg("Missing core_name argument", ValueError)
    # Ensure 'subblocks' list exists

    # Ensure global top module is set
    core.update_global_top_module()

    # Ensure list given by 'blocks_attribute_name' exists
    core.set_default_attribute(blocks_attribute_name, [])

    # Set submodule destination dir equal to current module
    if "dest_dir" not in kwargs:
        kwargs["dest_dir"] = core.dest_dir

    try:
        instance = core.get_core_obj(
            core_name, instance_name=instance_name, issuer=core, **kwargs
        )

        getattr(core, blocks_attribute_name).append(instance)
    except ModuleNotFoundError:
        add_traceback_msg(f"Failed to create instance '{instance_name}'.")
        raise
