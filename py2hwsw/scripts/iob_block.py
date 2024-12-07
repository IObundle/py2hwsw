# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from iob_base import (
    convert_dict2obj_list,
    str_to_kwargs,
    fail_with_msg,
    assert_attributes,
    add_traceback_msg,
    debug,
    find_obj_in_list,
)


@dataclass
class iob_block_group:
    """Class to represent a group of blocks."""

    name: str = ""
    descr: str = "Default description"
    blocks: list = field(default_factory=list)
    doc_clearpage: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Block group name is not set", ValueError)


attrs = [
    "core_name",
    "instance_name",
    ["-p", "parameters", {"nargs": "+"}, "pairs"],
    ["-c", "connect", {"nargs": "+"}, "pairs"],
    ["--no_autoaddr", "autoaddr", {"action": "store_false"}],
    ["--rw_overlap", "rw_overlap", {"action": "store_true"}],
    ["--csr_if", "csr_if"],
    {
        "--csr-group&csrs": [
            "name",
            {
                "-r&regs": [
                    "name:n_bits",
                    ["-t", "type"],
                    ["--rst_val", "rst_val"],
                    ["--addr", "addr", {"type": int}],
                    ["--log2n_items", "log2n_items"],
                    ["--no_autoreg", "autoreg", {"action": "store_false"}],
                ],
            },
        ]
    },
    ["-b", "blocks", {"nargs": "+"}],
]


@str_to_kwargs(attrs)
def create_block_group(core, *args, blocks_attribute_name="subblocks", **kwargs):
    """Creates a new block group object and adds it to the core's block list
    param core: core object
    """
    if core.abort_reason:
        return
    try:
        # Ensure list given by 'blocks_attribute_name' exists
        core.set_default_attribute(blocks_attribute_name, [])

        general_group_ref = None
        group_kwargs = kwargs
        blocks = kwargs.pop("blocks", None)
        # If kwargs provided a single block instead of a group, then create a general group for it or use existing one.
        if blocks is None:
            blocks = [kwargs]
            group_kwargs = {
                "name": "general_operation",
                "descr": "General operation group",
            }
            # Try to use existing "general_operation" group if was previously created
            general_group_ref = find_obj_in_list(
                getattr(core, blocks_attribute_name), "general_operation"
            )

        block_obj_list = []
        if type(blocks) is list:
            # Convert user blocks dictionaries into 'iob_block' objects
            for block in blocks:
                # Copy some attributes from group to all of its blocks
                if "instantiate" in group_kwargs:
                    block["instantiate"] = group_kwargs["instantiate"]
                if "is_superblock" in group_kwargs:
                    block["is_superblock"] = group_kwargs["is_superblock"]

                # Convert into 'iob_block' object
                block_obj = create_block(core, **block)
                if block_obj:
                    block_obj_list.append(block_obj)
        else:
            fail_with_msg(
                f"{blocks_attribute_name} attribute must be a list. Error at block group \"{group_kwargs.get('name', '')}\".\n{blocks}",
                TypeError,
            )

        assert_attributes(
            iob_block_group,
            group_kwargs,
            error_msg=f"Invalid {group_kwargs.get('name', '')} block group attribute '[arg]'!",
        )

        # Use existing "general_operation" group if possible
        if general_group_ref:
            general_group_ref.blocks += block_obj_list
        else:
            block_group = iob_block_group(blocks=block_obj_list, **group_kwargs)
            getattr(core, blocks_attribute_name).append(block_group)
    except Exception:
        add_traceback_msg(
            f"Failed to create block/group '{kwargs.get('name',None) or kwargs.get('core_name',None)}'."
        )
        raise


def create_block(core, core_name: str = "", instance_name: str = "", **kwargs):
    """Create an instante of a module, but only if we are not using a
    project wide special target (like clean)
    param core_name: Name of the core
    param instance_name: Verilog instance name
    """
    # Don't setup other destinations (like simulation) if this is a submodule and
    # the sub-submodule (we are trying to setup) is not for hardware/src/
    if not core.is_top_module and (
        core.dest_dir == "hardware/src"
        and "dest_dir" in kwargs
        and kwargs["dest_dir"] != "hardware/src"
    ):
        debug(f"Not setting up submodule '{core_name}' of '{core.name}' core!", 1)
        return

    assert core_name, fail_with_msg("Missing core_name argument", ValueError)
    # Ensure 'subblocks' list exists

    # Ensure global top module is set
    core.update_global_top_module()

    # Set submodule destination dir equal to current module
    if "dest_dir" not in kwargs:
        kwargs["dest_dir"] = core.dest_dir

    try:
        instance = core.get_core_obj(
            core_name, instance_name=instance_name, instantiator=core, **kwargs
        )

        return instance
    except ModuleNotFoundError:
        add_traceback_msg(f"Failed to create instance '{instance_name}'.")
        raise
