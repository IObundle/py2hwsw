# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import (
    create_obj_list,
    fail_with_msg,
    add_traceback_msg,
    assert_attributes,
    find_obj_in_list,
    empty_list,
)


@dataclass
class iob_parameter:
    """
    Class that represents a IOb parameter attribute.

    Attributes:
        name (str): Identifier name for the IOb Parameter option.
        val (Any): Value of the IOb Parameter option.
        descr (str): Description of the IOb Parameter option.
    """

    name: str = ""
    val: object = ""
    descr: str = "Default description"

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Every IOb Parameter must have a name!")

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(iob_parameter_dict):
        """
        Function to create iob_iob_parameter object from dictionary attributes.

        Attributes:
            iob_parameter_dict (dict): dictionary with values to initialize attributes of iob_iob_parameter object.
                This dictionary supports the following keys corresponding to the iob_parameter attributes:
                - name -> iob_parameter.name
                - val -> iob_parameter.val
                - descr -> iob_parameter.descr

        Returns:
            iob_parameter: iob_parameter object
        """
        return iob_parameter(**iob_parameter_dict)


@dataclass
class iob_parameter_group:
    """
    Class that represents a group of IOb Parameters.

    Attributes:
        name (str): Identifier name for the group of IOb Parameters.
        descr (str): Description of the IOb Parameter group.
        iob_parameters (list): List of IOb Parameter objects.
        doc_clearpage (bool): If enabled, the documentation table for this group will be terminated by a TeX '\clearpage' command.
    """

    name: str = ""
    descr: str = "Default description"
    iob_parameters: list = empty_list()
    doc_clearpage: bool = False

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("IOb Parameter group name is not set", ValueError)

    @staticmethod
    def create_iob_parameter_group(core, *args, **kwargs):
        """Creates a new IOb parameter group object and adds it to the core's iob_parameters list
        param core: core object
        """
        try:
            # Ensure 'iob_parameters' list exists
            core.set_default_attribute("iob_parameters", [])

            general_group_ref = None
            group_kwargs = kwargs
            iob_parameters = kwargs.pop("iob_parameters", None)
            # If kwargs provided a single iob_parameters instead of a group, then create a general group for it.
            if iob_parameters is None:
                iob_parameters = [kwargs]
                group_kwargs = {
                    "name": "general_iob_parameters",
                    "descr": "General IOb Parameters group",
                }
                # Try to use existing "general_iob_parameters" group if was previously created
                general_group_ref = find_obj_in_list(
                    core.iob_parameters, "general_iob_parameters"
                )

            iob_parameters_obj_list = []
            if type(iob_parameters) is list:
                # Convert user iob_parameters dictionaries into 'iob_parameter' objects
                iob_parameters_obj_list = create_obj_list(iob_parameters, iob_parameter)
            else:
                fail_with_msg(
                    f"'iob_parameters' attribute must be a list. Error at iob_parameters group \"{group_kwargs.get('name', '')}\".\n{iob_parameters}",
                    TypeError,
                )

            assert_attributes(
                iob_parameter_group,
                group_kwargs,
                error_msg=f"Invalid {group_kwargs.get('name', '')} iob_parameters group attribute '[arg]'!",
            )

            # Use existing "general_iob_parameters" group if possible
            if general_group_ref:
                general_group_ref.iob_parameters += iob_parameters_obj_list
            else:
                iob_parameters_group = iob_parameter_group(
                    iob_parameters=iob_parameters_obj_list, **group_kwargs
                )
                core.iob_parameters.append(iob_parameters_group)
        except Exception:
            add_traceback_msg(
                f"Failed to create iob_parameter/group '{kwargs['name']}'."
            )
            raise

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(iob_parameter_group_dict):
        """
        Function to create iob_parameter_group object from dictionary attributes.

        Attributes:
            iob_parameter_group_dict (dict): dictionary with values to initialize attributes of iob_parameter_group object.
                This dictionary supports the following keys corresponding to the iob_parameter_group attributes:
                - name -> iob_parameter_group.name
                - descr -> iob_parameter_group.descr
                - iob_parameters -> iob_parameter_group.iob_parameters
                - doc_clearpage -> iob_parameter_group.doc_clearpage

        Returns:
            iob_parameter_group: iob_parameter_group object
        """
        # Convert dictionary elements to objects
        kwargs = iob_parameter_group_dict.copy()
        kwargs["iob_parameters"] = [
            __class__.create_from_dict(i)
            for i in iob_parameter_group_dict["iob_parameters"]
        ]
        return iob_parameter_group(**kwargs)
