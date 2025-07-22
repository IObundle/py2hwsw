#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This is a custom Python shell for Py2HWSW with a custom help function

import code
import sys
import os
import importlib

# Do NOT remove this 'import readline'. It looks like its not used, but it is!
# It allows arrow_up and arrow_down keys to work for previous/next commands
import readline

from iob_base import get_lib_cores, import_python_module
from iob_core import iob_core

HELP_MSG = """\
Py2HWSW Python Shell
------------------------------------------------------------------------

To create IP cores using Py2HWSW refer to our examples by typing:

>>> show("example_name")

Currently the following examples are available:

iob_and: illustrates a basic module with a generic parameter
iob_aoi: illustrates a structural description based on subblocks

Type 'help(api)' for a complete reference.
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


def import_py2hwsw_scripts():
    """
    Returns a dictionary with all imported py2hwsw scripts.
    Note: This function also includes imported modules into the current namespace.
    Returns:
        dict: Dictionary with imported py2hwsw scripts.
    """
    # List all scripts in scripts/
    scripts_dir = os.path.dirname(os.path.realpath(__file__))
    py2_scripts_paths = [os.path.join(scripts_dir, f) for f in os.listdir(scripts_dir)]
    py2_scripts = {}
    for module_path in py2_scripts_paths:
        if not module_path.endswith(".py"):
            continue

        module_name = os.path.basename(module_path).split(".")[0]

        print(module_name, module_path)
        # Don't import the same module twice
        if module_name in sys.modules:
            py2_scripts[module_name] = sys.modules[module_name]
            continue

        # Import the module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # Include module in current namespace
        py2_scripts[module_name] = module
        spec.loader.exec_module(module)

    return py2_scripts


def import_lib_cores(namespace: dict, py2_scripts: dict):
    """Import lib cores into given python namespace
    Args:
        namespace (dict): python namespace to include the imported modules in
        py2_scripts (dict): objects to include in the namespace of each imported module
    """
    cores_paths = get_lib_cores()
    for path in cores_paths:
        module_name, file_extension = os.path.basename(path).split(".")
        # Skip .json cores
        # TODO: Instead of skipping, Convert dictionaries from .json cores into dynamic subclass of iob_core
        if file_extension == "json":
            continue
        imported_module = import_python_module(
            path, module_name=module_name, extra_namespace_objs=py2_scripts
        )

        # FIXME: Temporarily only import a few modules (the ones that have a class defined inside)
        if module_name not in ["iob_and", "iob_aoi"]:
            continue

        # Import only the class defined in that module
        namespace[module_name] = imported_module.__dict__[module_name]


def show_lib_core_code(core_name: str = None):
    if not core_name:
        print(
            "No lib core name given. Please provide a name, like: 'show(\"iob_and\")'."
        )
        return
    if type(core_name) is not str:
        print("Lib core name must be a string.")
        return
    cores_paths = get_lib_cores()
    for path in cores_paths:
        module_name, file_extension = os.path.basename(path).split(".")
        if module_name == core_name:
            print(f"Displaying code for {core_name} core")
            with open(path, "r") as f:
                print(f.read())
            break
    else:
        print(f"Could not find lib core '{core_name}'.")


# Create an instance of the custom shell
def main():
    sys.ps1 = ">>> "
    # Import py2 scripts
    py2_scripts = import_py2hwsw_scripts()
    # Create a custom namespace
    local_vars = globals().copy()
    # Include py2_scripts in namespace
    local_vars.update(py2_scripts)
    # Include  py2hwsw lib cores in namespace
    import_lib_cores(local_vars, py2_scripts)
    # Include custom functions in namespace
    local_vars["help"] = CustomFunction(help, HELP_MSG)
    local_vars["show"] = show_lib_core_code
    shell = Py2hwswShell(locals=local_vars)
    shell.interact()


if __name__ == "__main__":
    main()
