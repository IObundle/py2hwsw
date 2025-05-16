# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT
from iob_base import fail_with_msg

class iob_config:
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
