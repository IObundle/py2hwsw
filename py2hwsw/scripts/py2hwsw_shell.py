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

# Import modules from py2hwsw/src/ directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../src"))
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

Type 'list_py2_modules' for a complete reference of Py2HWSW script modules.
Type 'list_lib_modules' for a complete reference of Py2HWSW lib modules.
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
    def __init__(self, *args, interactive=sys.stdin.isatty(), **kwargs):
        super().__init__(*args, **kwargs)
        # Print help message on startup
        self.print_help_message()
        self.interactive = interactive
        self.evaluated_last_line = False

    def print_help_message(self):
        print(HELP_MSG)

    def raw_input(self, prompt):
        try:
            line = super().raw_input(prompt)  # Reads from stdin
        except EOFError:
            # Evaluate last line of file, if running non-interactively
            if not self.interactive and not self.evaluated_last_line:
                self.evaluated_last_line = True
                return ""
            raise
        if not self.interactive:
            # Not interactive: Echo input line to stdout
            print(line)
        return line


def import_py2hwsw_modules():
    """
    Returns a dictionary with all imported py2hwsw modules.
    Note: This function also includes imported modules into the current namespace.
    Returns:
        dict: Dictionary with imported py2hwsw modules.
    """
    # List all modules in py2hwsw/src/
    modules_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../src")
    py2_modules_paths = [os.path.join(modules_dir, f) for f in os.listdir(modules_dir)]
    py2_modules = {}
    for module_path in py2_modules_paths:
        if not module_path.endswith(".py"):
            continue

        module_name = os.path.basename(module_path).split(".")[0]

        # FIXME: Temporarily only import a few py2 modules (the ones that are really used in iob_aoi.py and its dependencies)
        if module_name not in ["iob_core", "iob_globals"]:
            continue

        # Don't import the same module twice
        if module_name in sys.modules:
            # Only return the class defined inside that module
            py2_modules[module_name] = sys.modules[module_name].__dict__[module_name]
            continue

        # Import the module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module  # Include module in global namespace
        spec.loader.exec_module(module)

        # Only return the class defined inside that module
        py2_modules[module_name] = module.__dict__[module_name]

    return py2_modules


def import_lib_cores(py2_modules: dict):
    """
    Returns a dictionary with all imported lib cores.
    Args:
        py2_modules (dict): objects to include in the namespace of each imported module
    Returns:
        dict: Dictionary with imported lib modules
    """
    cores_paths = get_lib_cores()
    lib_modules = {}
    for path in cores_paths:
        module_name, file_extension = os.path.basename(path).split(".")

        # FIXME: Temporarily only import a few modules (iob_aoi and its dependencies)
        if module_name not in ["iob_and", "iob_inv", "iob_or", "iob_aoi"]:
            continue

        # Don't import the same module twice
        if module_name in sys.modules:
            # Only return the class defined inside that module
            lib_modules[module_name] = sys.modules[module_name].__dict__[module_name]
            continue

        # Skip .json cores
        # TODO: Instead of skipping, Convert dictionaries from .json cores into dynamic subclass of iob_core
        if file_extension == "json":
            continue

        imported_module = import_python_module(
            path, module_name=module_name, extra_namespace_objs=py2_modules
        )
        # Only return the class defined inside that module
        lib_modules[module_name] = imported_module.__dict__[module_name]

    return lib_modules


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


def list_modules_msg(header: str, modules: dict):
    msg = header + "\n"
    for module in modules:
        msg += f"- {module}\n"
    return msg


def indent_code(code, indent="    "):
    # Indent each non-empty line by the chosen number of spaces (default: 4)
    return "\n".join(
        indent + line if line.strip() != "" else "" for line in code.split("\n")
    )


def code_with_error_on_exit(code):
    """Wrap given code in a try block that exits with non-zero status on error.
    By default, shell exits with status 0 (success) even when exception is raised.
    Using this wrapper, shell exits with non-zero status on error.
    """

    wrapped_code = f"""
try:
{indent_code(code)}
except:
    import sys
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
    return wrapped_code


# Create an instance of the custom shell
def main():
    sys.ps1 = ">>> "
    # Import py2 modules and lib cores
    py2_modules = import_py2hwsw_modules()
    lib_modules = import_lib_cores(py2_modules)
    # Create a custom namespace
    local_vars = globals().copy()
    # Include py2 modules and lib cores in namespace
    local_vars.update(py2_modules)
    local_vars.update(lib_modules)
    # Include custom functions in namespace
    local_vars["help"] = CustomFunction(help, HELP_MSG)
    local_vars["show"] = show_lib_core_code
    local_vars["list_py2_modules"] = CustomFunction(
        None, list_modules_msg("List of Py2HWSW modules:", py2_modules)
    )
    local_vars["list_lib_modules"] = CustomFunction(
        None, list_modules_msg("List of Py2HWSW lib modules:", lib_modules)
    )
    shell = Py2hwswShell(locals=local_vars)

    if len(sys.argv) > 1:
        # Run non-interactive shell
        # Example: py2hwsw_shell path/to/script.py
        script_file = sys.argv[1]
        with open(script_file) as f:
            code = f.read()
        code = code_with_error_on_exit(code)
        shell.runcode(code)
    else:
        # Run interactive shell
        # Example: py2hwsw_shell < path/to/script.py
        shell.interact()


if __name__ == "__main__":
    main()
