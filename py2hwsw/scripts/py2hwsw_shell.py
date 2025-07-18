#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This is a custom Python shell for Py2HWSW with a custom help function

import code
import sys

HELP_MSG = """\
Py2HWSW Python Shell
------------------------------------------------------------------------
Type 'exit' or 'quit' to exit the shell.
Type 'help' for this message.
Type 'help(api)' to view the entire Py2HWSW API.
Type 'help(<api_object>)' for API object-specific help. Example: 'help(iob_conf)'

All classes and functions in Py2HWSW API have been imported into this shell.
------------------------------------------------------------------------
Type help() for interactive help, or help(object) for help about object.
"""


class CustomFunction:
    """Create a wrapper for a function with a custom string representation."""

    def __init__(self, func, custom_string):
        self.func = func
        self.custom_string = custom_string

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return self.custom_string

    def __repr__(self):
        return self.custom_string


# Create a custom shell class
class Py2hwswShell(code.InteractiveConsole):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_help_message()

    def print_help_message(self):
        print(HELP_MSG)


# Create an instance of the custom shell
def main():
    sys.ps1 = ">>> "
    # Create a custom namespace and include the py2hwsw API
    local_vars = globals().copy()
    # Import api and everything from py2hwsw_api into local_vars
    exec("import py2hwsw_api as api", local_vars)
    exec("from py2hwsw_api import *", local_vars)
    local_vars["help"] = CustomFunction(help, HELP_MSG)
    shell = Py2hwswShell(locals=local_vars)
    shell.interact()


if __name__ == "__main__":
    main()
