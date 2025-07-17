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
    update_obj_from_dict,
    parse_short_notation_text,
)
from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_conf")
@dataclass
class iob_conf:
    """Class to represent a configuration option."""

    def validate_attributes(self):
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

    def validate_attributes(self):
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


#
# API methods
#


def conf_from_dict(conf_dict):
    conf_obj = iob_conf()

    key_attribute_mapping = {
        "type": "kind",
        "val": "value",
        "min": "min_value",
        "max": "max_value",
    }
    preprocessor_functions = {}
    # Update conf_obj attributes with values from given dictionary
    update_obj_from_dict(
        conf_obj._get_py2hwsw_internal_obj(),
        conf_dict,
        key_attribute_mapping,
        preprocessor_functions,
        conf_obj.get_supported_attributes().keys(),
    )

    return conf_obj


def conf_text2dict(conf_text: str) -> dict:
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
    return parse_short_notation_text(conf_text, conf_text_flags)


def conf_from_text(conf_text: str) -> iob_conf:
    return conf_from_dict(conf_text2dict(conf_text))


def conf_group_from_dict(conf_group_dict):
    conf_group_obj = iob_conf_group()

    # If "confs" key is missing, then assume dictionary describes a single conf
    if "confs" not in conf_group_dict:
        internal_conf_group_obj = conf_group_obj._get_py2hwsw_internal_obj()
        internal_conf_group_obj.name = "general_operation"
        internal_conf_group_obj.descr = "Core configuration."
        internal_conf_group_obj.confs = [conf_from_dict(conf_group_dict)]
        return conf_group_obj

    key_attribute_mapping = {}
    preprocessor_functions = {
        "confs": lambda lst: [conf_from_dict(i) for i in lst],
    }
    # Update conf_group_obj attributes with values from given dictionary
    update_obj_from_dict(
        conf_group_obj._get_py2hwsw_internal_obj(),
        conf_group_dict,
        key_attribute_mapping,
        preprocessor_functions,
        conf_group_obj.get_supported_attributes().keys(),
    )

    return conf_group_obj


def conf_group_text2dict(conf_group_text: str) -> dict:
    # Create conf_group from short notation text
    conf_group_flags = [
        "name",
        ["--confs", {"dest": "confs"}],
        ["-doc", {"dest": "doc_only", "action": "store_true"}],
        ["-doc_clearpage", {"dest": "doc_clearpage", "action": "store_true"}],
        ["-d", {"dest": "descr"}],
    ]
    # Parse conf group text into a dictionary
    conf_group_dict = parse_short_notation_text(conf_group_text, conf_group_flags)

    # Special processing for conf subflags
    confs: list[iob_conf] = []
    for conf_text in conf_group_dict.get("confs", "").split("\n\n"):
        confs.append(conf_text2dict(conf_text))
    # replace "confs" short notation text with list of conf objects
    conf_group_dict.update({"confs": confs})
    return conf_group_dict


def conf_group_from_text(conf_group_text: str):
    return conf_group_from_dict(conf_group_text2dict(conf_group_text))
