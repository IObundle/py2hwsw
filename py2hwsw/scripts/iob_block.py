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
    "name",
    [
        "-c",
        "blocks",
        {"nargs": "+"},
        ["name:width"],
    ],  # FIXME: According to block parameters
]


@str_to_kwargs(attrs)
def create_block_group(core, *args, blocks=[], **kwargs):
    """Creates a new block group object and adds it to the core's block list
    param core: core object
    """
    if core.abort_reason:
        return
    try:
        # Ensure 'blocks' list exists
        core.set_default_attribute("blocks", [])

        block_obj_list = []
        if type(blocks) is list:
            # Convert user blocks dictionaries into 'iob_block' objects
            for block in blocks:
                block_obj_list.append(create_block(core, **block))
        else:
            fail_with_msg(
                f"blocks attribute must be a list. Error at block group \"{kwargs.get('name', '')}\".\n{blocks}",
                TypeError,
            )

        assert_attributes(
            iob_block_group,
            kwargs,
            error_msg=f"Invalid {kwargs.get('name', '')} block group attribute '[arg]'!",
        )

        block_group = iob_block_group(*args, blocks=block_obj_list, **kwargs)
        core.blocks.append(block_group)
    except Exception:
        add_traceback_msg(f"Failed to create block_group '{kwargs['name']}'.")
        raise


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
]


@str_to_kwargs(attrs)
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
    # Ensure 'blocks' list exists

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
