# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import importlib
from dataclasses import dataclass
from iob_base import (
    convert_dict2obj_list,
    fail_with_msg,
    add_traceback_msg,
    str_to_kwargs,
    assert_attributes,
    find_obj_in_list,
)

from api_base import api_class


@api_class
@dataclass
class iob_conf:
    """Class to represent a configuration option."""

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Every conf must have a name!")
        if self.kind not in ["P", "M", "C", "D"]:
            fail_with_msg(
                f"Conf '{self.name}' type must be either P (Parameter), M (Macro), C (Constant) or D (Derived Parameter)!"
            )

        try:
            value = int(self.value)
            min_value = int(self.min_value)
            max_value = int(self.max_value)
            if value < min_value or value > max_value:
                fail_with_msg(
                    f"Conf '{self.name}' value '{value}' must be between {min_value} and {max_value}!"
                )
        except ValueError:
            pass


@api_class
@dataclass
class iob_conf_group:
    """Class to represent a group of configurations."""

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


#
# API methods
#


def conf_from_dict(conf_dict):
    # NOTE: Using a Lazy import here to avoid circular import.
    #       Is there a better way to instantiate API class?
    api_iob_conf = importlib.import_module("user_api.api").iob_conf
    # Replace 'type' key with 'kind' key
    if "type" in conf_dict:
        conf_dict["kind"] = conf_dict.pop("type")
    return api_iob_conf(**conf_dict)


def conf_from_text(conf_text):
    api_iob_conf = importlib.import_module("user_api.api").iob_conf
    conf_dict = {}
    # TODO: parse short notation text
    return api_iob_conf(**conf_dict)


def conf_group_from_dict(conf_group_dict):
    api_iob_conf_group = importlib.import_module("user_api.api").iob_conf_group
    # Convert list of confs dictionaries into 'confs' objects
    confs_objs = []
    for conf in conf_group_dict.get("confs", []):
        confs_objs.append(conf_from_dict(conf))
    conf_group_dict["confs"] = confs_objs
    return api_iob_conf_group(**conf_group_dict)


def conf_group_from_text(conf_group_text):
    api_iob_conf_group = importlib.import_module("user_api.api").iob_conf_group
    conf_group_dict = {}
    # TODO: parse short notation text
    return api_iob_conf_group(**conf_group_dict)
