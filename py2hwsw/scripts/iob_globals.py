# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from iob_base import fail_with_msg


class iob_globals:
    _instance = None
    _is_set = False

    def __new__(cls, **kwargs):
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
        if hasattr(self, key):
            fail_with_msg(
                f"Cannot modify existing attribute '{key}'.",
                AttributeError,
            )
        super().__setattr__(key, value)


def create_globals(core, attr_name, value):
    """
    Create a singleton instance of iob_globals with the given attributes.
    If the instance already exists, it will not be modified.
    """
    if core.is_top_module:
        core.set_default_attribute(
            attr_name, getattr(iob_globals(**{attr_name: value}), attr_name)
        )
