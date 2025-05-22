# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from iob_base import (
    convert_dict2obj_list,
    fail_with_msg,
    add_traceback_msg,
    str_to_kwargs,
    assert_attributes,
    find_obj_in_list,
)


@dataclass
class iob_conf:
    """Class to represent a configuration option."""

    # Identifier name for the configuration option.
    name: str = ""
    # Type of configuration option, either M (Verilog macro), P (Verilog parameter), C (Constant) or D (Derived Parameter).
    # False-parameters are the same as verilog parameters except that the its value must not be overriden.
    type: str = "P"
    # Value of the configuration option.
    val: str | int | bool = ""
    # Minimum value supported by the configuration option (NA if not applicable).
    min: str | int = "NA"
    # Maximum value supported by the configuration option (NA if not applicable).
    max: str | int = "NA"
    # Description of the configuration option.
    descr: str = "Default description"
    # Only applicable to Verilog macros: Conditionally enable this configuration if the specified Verilog macro is defined/undefined.
    if_defined: str = ""
    if_not_defined: str = ""
    # If enabled, configuration option will only appear in documentation. Not in the verilog code.
    doc_only: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Every conf must have a name!")
        if self.type not in ["P", "M", "C", "D"]:
            fail_with_msg(
                f"Conf '{self.name}' type must be either P (Parameter), M (Macro), C (Constant) or D (Derived Parameter)!"
            )

        try:
            val = int(self.val)
            min = int(self.min)
            max = int(self.max)
            if val < min or val > max:
                fail_with_msg(
                    f"Conf '{self.name}' value '{val}' must be between {min} and {max}!"
                )
        except ValueError:
            pass


@dataclass
class iob_conf_group:
    """Class to represent a group of configurations."""

    # Identifier name for the group of configurations.
    name: str = ""
    # Description of the configuration group.
    descr: str = "Default description"
    # List of configuration objects.
    confs: list = field(default_factory=list)
    # If enabled, configuration group will only appear in documentation. Not in the verilog code.
    doc_only: bool = False
    # If enabled, the documentation table for this group will be terminated by a TeX '\clearpage' command.
    doc_clearpage: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Conf group name is not set", ValueError)


attrs = [
    "name",
    ["-t", "type"],
    ["-v", "val"],
    ["-m", "min"],
    ["-M", "max"],
    ["-c", "confs", {"nargs": "+"}],
]


@str_to_kwargs(attrs)
def create_conf_group(core, *args, **kwargs):
    """Creates a new conf group object and adds it to the core's conf list
    param core: core object
    """
    try:
        # Ensure 'confs' list exists
        core.set_default_attribute("confs", [])

        general_group_ref = None
        group_kwargs = kwargs
        confs = kwargs.pop("confs", None)
        # If kwargs provided a single conf instead of a group, then create a general group for it.
        if confs is None:
            confs = [kwargs]
            group_kwargs = {
                "name": "general_operation",
                "descr": "General operation group",
            }
            # Try to use existing "general_operation" group if was previously created
            general_group_ref = find_obj_in_list(core.confs, "general_operation")

        conf_obj_list = []
        if type(confs) is list:
            # Convert user confs dictionaries into 'iob_conf' objects
            conf_obj_list = convert_dict2obj_list(confs, iob_conf)
        else:
            fail_with_msg(
                f"Confs attribute must be a list. Error at conf group \"{group_kwargs.get('name', '')}\".\n{confs}",
                TypeError,
            )

        assert_attributes(
            iob_conf_group,
            group_kwargs,
            error_msg=f"Invalid {group_kwargs.get('name', '')} conf group attribute '[arg]'!",
        )

        # Use existing "general_operation" group if possible
        if general_group_ref:
            general_group_ref.confs += conf_obj_list
        else:
            conf_group = iob_conf_group(confs=conf_obj_list, **group_kwargs)
            core.confs.append(conf_group)
    except Exception:
        add_traceback_msg(f"Failed to create conf/group '{kwargs['name']}'.")
        raise
