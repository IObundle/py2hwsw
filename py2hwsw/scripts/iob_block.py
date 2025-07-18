# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from iob_base import (
    str_to_kwargs,
    fail_with_msg,
    add_traceback_msg,
    debug,
)


attrs = [
    "core_name",
    "instance_name",
    ["-p", "parameters", {"nargs": "+"}, "pairs"],
    ["-c", "connect", {"nargs": "+"}, "pairs"],
    ["--no_autoaddr", "autoaddr", {"action": "store_false"}],
    ["--rw_overlap", "rw_overlap", {"action": "store_true"}],
    ["--no_instance", "instantiate", {"action": "store_false"}],
    ["--dest_dir", "dest_dir"],
    ["--csr_if", "csr_if"],
    {
        "--csr-group&csrs": [
            "name",
            {
                "-r&regs": [
                    "name:n_bits",
                    ["-t", "type"],
                    ["-m", "mode"],
                    ["--rst_val", "rst_val"],
                    ["--addr", "addr", {"type": int}],
                    ["--log2n_items", "log2n_items"],
                ],
            },
        ]
    },
]


@str_to_kwargs(attrs)
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
        debug(f"Not setting up submodule '{core_name}' of '{core.name}' core!", 1)
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
