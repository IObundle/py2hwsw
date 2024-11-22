# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from iob_base import (
    convert_dict2obj_list,
    fail_with_msg,
    add_traceback_msg,
    str_to_kwargs,
    assert_attributes,
)


@dataclass
class iob_conf:
    name: str = ""
    type: str = ""
    val: str | int | bool = ""
    min: str | int = "NA"
    max: str | int = "NA"
    descr: str = "Default description"
    # Only set this macro if the Verilog macro specified here is defined
    if_defined: str = ""
    if_not_defined: str = ""
    doc_only: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Every conf must have a name!")
        if not self.type:
            fail_with_msg(f"Conf '{self.name}' must have a type!")
        elif self.type not in ["M", "P", "F"]:
            fail_with_msg(f"Conf '{self.name}' type must be either M, P or F!")

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
    """Class to represent a group of confs."""

    name: str = ""
    descr: str = "Default description"
    confs: list = field(default_factory=list)
    doc_only: bool = False
    doc_clearpage: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Conf group name is not set", ValueError)


# attrs = ["name", ["-t", "type"], ["-v", "val"], ["-m", "min"], ["-M", "max"]]
attrs = [
    "name",
    ["-c", "confs", {"nargs": "+"}, ["name:width"]],  # FIXME: According to above
]


@str_to_kwargs(attrs)
def create_conf_group(core, *args, confs=[], **kwargs):
    """Creates a new conf group object and adds it to the core's conf list
    param core: core object
    """
    try:
        # Ensure 'confs' list exists
        core.set_default_attribute("confs", [])

        conf_obj_list = []
        if type(confs) is list:
            # Convert user confs dictionaries into 'iob_conf' objects
            conf_obj_list = convert_dict2obj_list(confs, iob_conf)
        else:
            fail_with_msg(
                f"Confs attribute must be a list. Error at conf group \"{kwargs.get('name', '')}\".\n{confs}",
                TypeError,
            )

        assert_attributes(
            iob_conf_group,
            kwargs,
            error_msg=f"Invalid {kwargs.get('name', '')} conf group attribute '[arg]'!",
        )

        conf_group = iob_conf_group(*args, confs=conf_obj_list, **kwargs)
        core.confs.append(conf_group)
    except Exception:
        add_traceback_msg(f"Failed to create conf_group '{kwargs['name']}'.")
        raise
