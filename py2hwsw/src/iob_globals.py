# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from iob_base import fail_with_msg


class iob_globals:
    """
    A singleton class for managing project-wide global variables.

    This class ensures that only one instance exists throughout the project.
    It allows for the creation and management of global variables in a controlled manner.

    Attributes:
        None (attributes are set dynamically)

    Notes:
        - Existing attributes cannot be modified once set.
        - New attributes can be added, but not changed if they already exist.
    """

    _instance = None
    _is_set = False

    def __new__(cls, **kwargs):
        """
        Creates or returns the singleton instance of `iob_globals`.

        If the instance already exists and new attributes are provided,
        only new attributes are added, ignoring existing ones.

        Args:
            **kwargs: Key-value pairs of attributes to set.

        Returns:
            The singleton instance of `iob_globals`.
        """
        if cls._is_set:
            # Only set new attributes — ignore existing ones
            for k, v in kwargs.items():
                if not hasattr(cls._instance, k):
                    setattr(cls._instance, k, v)
            return cls._instance

        # First-time init
        cls._instance = super().__new__(cls)
        for k, v in kwargs.items():
            setattr(cls._instance, k, v)
        cls._is_set = True
        return cls._instance

    def __setattr__(self, key, value):
        """
        Sets a new attribute on the instance.

        Args:
            key (str): The name of the attribute to set.
            value: The value of the attribute to set.

        Raises:
            AttributeError: If the attribute already exists.
        """
        if hasattr(self, key):
            fail_with_msg(
                f"Cannot modify existing attribute '{key}'.",
                AttributeError,
            )
        super().__setattr__(key, value)

    @staticmethod
    def create_globals(core, attr_name, value):
        """
        Creates a singleton instance of `iob_globals` with the given attribute.

        If the instance already exists, it will not be modified.

        Args:
            core: The core object.
            attr_name (str): The name of the attribute to set.
            value: The value of the attribute to set.
        """
        if core.is_top_module:
            core.set_default_attribute(
                attr_name, getattr(iob_globals(**{attr_name: value}), attr_name)
            )
