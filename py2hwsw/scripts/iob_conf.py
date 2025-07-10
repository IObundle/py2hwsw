# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from iob_base import (
    convert_dict2obj_list,
    fail_with_msg,
    add_traceback_msg,
    str_to_kwargs,
    assert_attributes,
    find_obj_in_list,
)

from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_conf")
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


@internal_api_class("user_api.api", "iob_conf_group")
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
                "descr": "Core configuration.",
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


def rename_dictionary_keys(dictionary, key_mapping):
    """
    Rename keys in dictionary using a mapping.
    Mapping format:
    {
        "old_key": "new_key",
        ...
    }

    Attributes:
        dictionary (dict): Dictionary to rename keys in.
        key_mapping (dict): Mapping of keys to rename.

    Returns:
        dict: Dictionary with renamed keys.
    """
    # Replace key with corresponding attribute name
    for old_key, new_key in key_mapping.items():
        if old_key in key_mapping:
            dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def conf_from_dict(conf_dict):
    # NOTE: Using a Lazy import here to avoid circular import.
    #       Is there a better way to instantiate API class?
    key_attribute_mapping = {
        "type": "kind",
        "val": "value",
        "min": "min_value",
        "max": "max_value",
    }
    # Replace key with corresponding attribute name
    for key, attr in key_attribute_mapping.items():
        if key in conf_dict:
            conf_dict[attr] = conf_dict.pop(key)
    return iob_conf(**conf_dict)


import argparse
import shlex


def short_notation_create_parser(flags: list) -> argparse.ArgumentParser:
    """
    TODO:
    - import argparse
    - or add this to iob_base.py or short_notation.py
    """
    breakpoint()
    parser = argparse.ArgumentParser()
    for flag in flags:
        if isinstance(flag, str):
            parser.add_argument(flag)
        elif isinstance(flag, list):
            parser.add_argument(flag[0], **flag[1])
        else:
            raise ValueError(f"ERROR: unsupported flag format: {flag}")
    breakpoint()
    return parser


def _conf_parse_text(conf_text: str) -> dict:
    # parse conf text into a dictionary
    conf_text_flags = [
        "name",
        ["-t", {"dest": "kind"}],
        ["-v", {"dest": "value"}],
        ["-m", {"dest": "min_value"}],
        ["-M", {"dest": "max_value"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
        ["-doc", {"dest": "doc_only", "action": "store_true"}],
    ]

    # preprocess short notation text
    pre_process_conf_text = shlex.split(conf_text.strip('\n'))
    # create argument parser
    parser = short_notation_create_parser(conf_text_flags)
    print(f"DEBUG: pre_process_conf_text = {pre_process_conf_text}")
    breakpoint()
    # parse and return conf_text as dict
    return parser.parse_args(pre_process_conf_text).__dict__


def conf_from_text(conf_text: str) -> iob_conf:
    conf_dict = _conf_parse_text(conf_text)
    print(f"DEBUG: {conf_dict}")
    breakpoint()
    return iob_conf(**conf_dict)


def conf_group_from_dict(conf_group_dict):
    # Convert list of confs dictionaries into 'confs' objects
    confs_objs = []
    for conf in conf_group_dict.get("confs", []):
        confs_objs.append(conf_from_dict(conf))
    conf_group_dict["confs"] = confs_objs
    return iob_conf_group(**conf_group_dict)


def conf_group_from_text(conf_group_text):
    conf_group_dict = {}
    # TODO: parse short notation text
    return iob_conf_group(**conf_group_dict)
