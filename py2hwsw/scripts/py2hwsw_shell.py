#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This is a custom Python shell for Py2HWSW with a custom help function

import code
import sys
import os

from iob_base import get_lib_cores, import_python_module
from iob_core import iob_core

HELP_MSG = """\
Py2HWSW Python Shell
------------------------------------------------------------------------

To create IP cores using Py2HWSW refer to our exemples by typing:

>>> show(example_name)

Currently the following examples are available:

iob_and: illustrates a basic module with a generic parameter
iob_aoi: illustrates a structural description based on subblocks

Type 'help(api) for a complete reference'
Type 'exit' or 'quit' to exit the shell.
Type 'help' for this message.
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


def import_lib_cores(namespace: dict):
    """Import lib cores into given python namespace"""
    cores_paths = get_lib_cores()
    for path in cores_paths:
        module_name, file_extension = os.path.basename(path).split(".")
        # Convert dictionaries from .json cores into dynamic subclass of iob_core
        if file_extension == "json":
            continue
        imported_module = import_python_module(path, module_name=module_name)

        # FIXME: Temporarily only import a few modules (the ones that have a class defined inside)
        if module_name not in ["iob_and", "iob_aoi"]:
            continue

        # Import only the class defined in that module
        namespace[module_name] = imported_module.__dict__[module_name]


# Create an instance of the custom shell
def main():
    sys.ps1 = ">>> "
    # Create a custom namespace and include the py2hwsw API
    local_vars = globals().copy()
    # Import api and everything from py2hwsw_api into local_vars
    exec("import py2hwsw_api as api", local_vars)
    exec("from py2hwsw_api import *", local_vars)
    local_vars["help"] = CustomFunction(help, HELP_MSG)
    import_lib_cores(local_vars)
    shell = Py2hwswShell(locals=local_vars)
    shell.interact()


if __name__ == "__main__":
    main()
