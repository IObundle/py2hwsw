# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

from iob_base import (
    str_to_kwargs,
    fail_with_msg,
    add_traceback_msg,
    debug,
)


attrs = [
    "core",
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
    module,
    instance_name: str = "",
    blocks_attribute_name="subblocks",
    **kwargs,
):
    """Create an instante of a module, but only if we are not using a
    project wide special target (like clean)
    param module: The parent module object
    param instance_name: Verilog instance name
    """
    # core name from kwargs (short notation or programmatic)
    core = kwargs["core"]

    # Create "iob_csrs" even when abort_reason is "ipxact_gen" in order to create CSRs memory map
    # Skip all other blocks
    if module.abort_reason and not (
        module.abort_reason == "ipxact_gen" and core == "iob_csrs"
    ):
        return
    # Don't setup other destinations (like simulation) if this is a submodule and
    # the sub-submodule (we are trying to setup) is not for hardware/src/
    if (
        not module.is_top_module
        and not module.is_superblock
        and (
            module.dest_dir == "hardware/src"
            and "dest_dir" in kwargs
            and kwargs["dest_dir"] != "hardware/src"
        )
    ):
        debug(f"Not setting up submodule '{core}' of '{module.name}' core!", 1)
        return

    assert core, fail_with_msg("Missing core argument", ValueError)
    # Ensure 'subblocks' list exists

    # Ensure global top module is set
    module.update_global_top_module()

    # Ensure list given by 'blocks_attribute_name' exists
    module.set_default_attribute(blocks_attribute_name, [])

    # Set submodule destination dir equal to current module
    if "dest_dir" not in kwargs:
        kwargs["dest_dir"] = module.dest_dir

    try:
        # Pop 'core' from kwargs to avoid conflict with get_core_obj's first parameter 'core'
        kwargs.pop("core", None)
        instance = module.get_core_obj(
            core, instance_name=instance_name, issuer=module, **kwargs
        )

        getattr(module, blocks_attribute_name).append(instance)
    except ModuleNotFoundError:
        add_traceback_msg(f"Failed to create instance '{instance_name}'.")
        raise
