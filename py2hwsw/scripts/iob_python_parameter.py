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
    process_elements_from_list,
)

from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_python_parameter")
@dataclass
class iob_python_parameter:
    """Class to represent a Python Parameter option."""

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Every Python Parameter must have a name!")


@internal_api_class("user_api.api", "iob_python_parameter_group")
@dataclass
class iob_python_parameter_group:
    """Class to represent a Group of Python Parameters."""

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Python Parameter group name is not set", ValueError)


attrs = [
    "name",
    ["-v", "val"],
    ["-p", "python_parameters", {"nargs": "+"}],
]


@str_to_kwargs(attrs)
def create_python_parameter_group(core, *args, **kwargs):
    """Creates a new python parameter group object and adds it to the core's python_parameters list
    param core: core object
    """
    try:
        # Ensure 'python_parameters' list exists
        core.set_default_attribute("python_parameters", [])

        general_group_ref = None
        group_kwargs = kwargs
        python_parameters = kwargs.pop("python_parameters", None)
        # If kwargs provided a single python_parameters instead of a group, then create a general group for it.
        if python_parameters is None:
            python_parameters = [kwargs]
            group_kwargs = {
                "name": "general_python_parameters",
                "descr": "General Python Parameters group",
            }
            # Try to use existing "general_python_parameters" group if was previously created
            general_group_ref = find_obj_in_list(
                core.python_parameters, "general_python_parameters"
            )

        python_parameters_obj_list = []
        if type(python_parameters) is list:
            # Convert user python_parameters dictionaries into 'iob_python_parameter' objects
            python_parameters_obj_list = convert_dict2obj_list(
                python_parameters, iob_python_parameter
            )
        else:
            fail_with_msg(
                f"'python_parameters' attribute must be a list. Error at python_parameters group \"{group_kwargs.get('name', '')}\".\n{python_parameters}",
                TypeError,
            )

        assert_attributes(
            iob_python_parameter_group,
            group_kwargs,
            error_msg=f"Invalid {group_kwargs.get('name', '')} python_parameters group attribute '[arg]'!",
        )

        # Use existing "general_python_parameters" group if possible
        if general_group_ref:
            general_group_ref.python_parameters += python_parameters_obj_list
        else:
            python_parameters_group = iob_python_parameter_group(
                python_parameters=python_parameters_obj_list, **group_kwargs
            )
            core.python_parameters.append(python_parameters_group)
    except Exception:
        add_traceback_msg(
            f"Failed to create python_parameter/group '{kwargs['name']}'."
        )
        raise


def python_parameter_from_dict(python_parameter_dict):
    return iob_python_parameter(**python_parameter_dict)


def python_parameter_from_text(python_parameter_text):
    python_parameter_dict = {}
    # TODO: parse short notation text
    return iob_python_parameter(**python_parameter_dict)


def python_parameter_group_from_dict(python_parameter_group_dict):
    python_parameter_group_obj = iob_python_parameter_group()

    key_attribute_mapping = {}
    preprocessor_functions = {
        "python_parameters": lambda lst: process_elements_from_list(
            lst, python_parameter_from_dict
        ),
    }
    # Update python_parameter_group_obj attributes with values from given dictionary
    update_obj_from_dict(
        python_parameter_group_obj._get_py2hwsw_internal_obj(),
        python_parameter_group_dict,
        key_attribute_mapping,
        preprocessor_functions,
        python_parameter_group_obj.__annotations__.keys(),
    )

    return python_parameter_group_obj


def python_parameter_group_from_text(python_parameter_group_text):
    python_parameter_group_dict = {}
    # TODO: parse short notation text
    return iob_python_parameter_group(**python_parameter_group_dict)
