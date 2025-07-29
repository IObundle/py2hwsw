# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os
from dataclasses import dataclass
import importlib.util
import traceback
import inspect
import shutil
from dataclasses import field

import iob_colors


class iob_base:
    """Generic IOb base class with attributes and methods useful for other IOb classes"""

    def set_default_attribute(
        self,
        name: str,
        value,
        datatype=None,
        set_attribute_handler=None,
        descr: str = "",
        copy_by_reference: bool = True,
    ):
        """Set an attribute if it has not been set before (likely by a subclass)
        Also optionally verifies if the datatype of the attribute set
        previously is correct.
        param name: name of the attribute
        param value: value to set
        param datatype: optional data type of the attribute to check
        param set_attribute_handler: function to call to set the attribute
                                     Related to `parse_attributes_dict()` of iob_core.py
        param descr: description of the attribute
        param copy_by_reference: if True (default), the attribute is copied by reference
        """

        # Coditions to add to _attr_refs:
        # 1. copy_by_reference is True
        # 2. datatype is immutable
        add_attr_refs = False
        if copy_by_reference and is_immutable_type(value, datatype):
            add_attr_refs = True

        # Ensure that `_attr_refs` dictionary exists
        if add_attr_refs and "_attr_refs" not in self.__dict__:
            self._attr_refs = {}

        if add_attr_refs:
            if name not in self._attr_refs:
                self._attr_refs[name] = value
                self.__create_attr_ref_property(name)
            elif datatype:
                if not isinstance(self._attr_refs[name], datatype):
                    raise TypeError(
                        iob_colors.FAIL
                        + f"Shared attribute '{name}' must be of type {datatype}"
                        + iob_colors.ENDC
                    )
        else:
            if not hasattr(self, name):
                setattr(self, name, value)
            elif datatype is not None:
                if type(getattr(self, name)) != datatype:
                    raise TypeError(
                        iob_colors.FAIL
                        + f"Attribute '{name}' must be of type {datatype}"
                        + iob_colors.ENDC
                    )
        # Ensure that `ATTRIBUTE_PROPERTIES` dictionary exists
        # The 'ATTRIBUTE_PROPERTIES' is a dictionary that stores information about the
        # attributes, including the handlers used to set their values.
        if "ATTRIBUTE_PROPERTIES" not in self.__dict__:
            self.ATTRIBUTE_PROPERTIES = {}
        # Define the function to call to set the attribute from info given in a dict.
        # See `parse_attributes_dict()` of iob_core.py for details.
        # For example, the info given about this attribute may be of the type 'dict',
        # but we may want to set a type 'object' instead.
        # The `set_attribute_handler` is responsible for converting between these two
        # datatypes.
        if name in self.ATTRIBUTE_PROPERTIES:
            properties = self.ATTRIBUTE_PROPERTIES[name]
        else:
            properties = iob_attribute_properties()
        if datatype:
            properties.datatype = datatype
        if set_attribute_handler:
            # Set custom set_handler
            properties.set_handler = set_attribute_handler
        elif not properties.set_handler:
            # Set default set_handler
            if add_attr_refs:
                properties.set_handler = lambda v: self._attr_refs.update({name: v})
            else:
                properties.set_handler = lambda v: setattr(self, name, v)
        if descr:
            properties.descr = descr

        self.ATTRIBUTE_PROPERTIES[name] = properties

    def __create_attr_ref_property(self, name: str):
        """Create a property to access `name` as a regular attribute.
        This allows access to `name` attribute as a regular attribute,
        while copying by reference with copy(obj) for immutable types.
        params: name: name of the attribute to create a property for
        """

        def getter(self):
            return self._attr_refs.get(name, None)

        def setter(self, value):
            if "_attr_refs" not in self.__dict__:
                self._attr_refs = {}
            self._attr_refs[name] = value

        # Create property of the classe
        setattr(self.__class__, name, property(getter, setter))

@dataclass
class iob_attribute_properties:
    """Class that stores properties of an attribute"""

    datatype: object = None
    # Function to use to set the attribute value based on info given in the 'py2hw'
    # interface
    set_handler: object = None
    descr: str = "Default attribute description"


#
# Type check method
#


def is_immutable_type(value, datatype=None):
    """Check if a built-in datatype is immutable
    params value: value to check datatype
    params datatype: optional datatype to check against
    returns: True if the value is of immutable datatype, False otherwise
    """
    if datatype:
        immutable_type_values = (
            int(),
            float(),
            complex(),
            bool(),
            str(),
            tuple(),
            bytes(),
            frozenset(),
        )
        for t in immutable_type_values:
            if datatype == type(t):
                return True
        return False
    else:
        immutable_types = (int, float, complex, bool, str, tuple, bytes, frozenset)
        return isinstance(value, immutable_types)

#
# List manipulation methods
#


def find_obj_in_list(obj_list, obj_name, process_func=lambda o: o):
    """Returns an object with a given name from a list of objects
    param obj_list: list of objects (or dictionaries) to search
    param obj_name: name of the object to find
    param process_func: optional function to apply to each object before comparing
    """
    if not obj_list:
        return None
    processed_objs = list(process_func(o) for o in obj_list)
    # Support dictionaries as well
    if isinstance(obj_list[0], dict):
        for obj, obj_processed in zip(obj_list, processed_objs):
            if obj_processed and obj_processed["name"] == obj_name:
                return obj
    else:
        for obj, obj_processed in zip(obj_list, processed_objs):
            if obj_processed and obj_processed.name == obj_name:
                return obj
    return None


def create_obj_list(dict_list: dict, obj_class):
    """Convert a list of dictionaries to a list of objects
    If list contains elements that are not dictionaries, they are left as is
    param dict_list: list of dictionaries
    param obj_class: class of the objects to create
    """
    obj_list = []
    for dict_obj in dict_list:
        if isinstance(dict_obj, dict):
            obj_list.append(obj_class(**dict_obj))
        else:
            obj_list.append(dict_obj)
    return obj_list


def process_elements_from_list(list2process: list, process_func: callable):
    """Run processing function on each element of a list"""
    for e in list2process:
        process_func(e)


#
# Print methods
#


def fail_with_msg(msg, exception_type=Exception):
    """Raise an error with a given message
    param msg: message to print
    param exception_type: type of python exception to raise
    """
    raise exception_type(iob_colors.FAIL + msg + iob_colors.ENDC)


def warn_with_msg(msg):
    """Print a warning with a given message"""
    print(iob_colors.WARNING + msg + iob_colors.ENDC)


#
# Exception handling
#
printed_traceback = False


def add_traceback_msg(msg):
    """Should be called in exception handler block of try/except block.
    It prints the traceback on the first call.
    It also prints the message given.
    """
    global printed_traceback
    if not printed_traceback:
        printed_traceback = True
        traceback.print_exc()
    print(iob_colors.FAIL + msg + iob_colors.ENDC)


#
# Debug
#
debug_level = 0


def debug_print(msg, level=0):
    """Print a message if project debug_level >= level
    :param str msg: message to print
    :param int level: debug level
    """
    if debug_level >= level:
        print(f"[Debug {level}]: " + msg)


#
# Other methods
#


def find_file(search_directory, name_without_ext, filter_extensions=[]):
    """Find a file, without extension, in a given directory or subdirectories
    param name_without_ext: name_without_ext of the file without extension
    param search_directory: directory to search
    param filter_extensions: list of extensions to filter (example: [".py", ".tex"])
    """
    for root, _, files in os.walk(search_directory):
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            if file_name == name_without_ext and (
                filter_extensions == [] or file_ext in filter_extensions
            ):
                return os.path.join(root, file)
    return None


def hardcoded_find_file(name_without_ext, filter_extensions=[]):
    """Find a file in specific hardcoded directories
    param name_without_ext: name of the file without extension
    param filter_extensions: list of extensions to filter
    """
    hardcoded_directories = [
        ".",
        f"submodules/{name_without_ext}",
        f"lib/modules/{name_without_ext}",
    ]

    for dir in hardcoded_directories:
        files = os.listdir(dir)
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            if file_name == name_without_ext and (
                filter_extensions == [] or file_ext in filter_extensions
            ):
                return os.path.join(dir, file)
    return None


def find_path(search_directory, path):
    """Find a path inside the search_directory
    param search_directory: directory to search
    param path: path to find. Examples: "submodules/ethernet", "iob_uart.py", "iob_uart/hardware/simulation/src/iob_vlt_tb.vh"
    """
    for root, dirs, files in os.walk(search_directory):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir_path.endswith(path):
                return dir_path
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(path):
                return file_path
    return None


def import_python_module(module_path: str, module_name: str = None, extra_namespace_objs: dict = {}):
    """
    Import a python module from a given filepath.

    Args:
        module_path (str): path of the module's python file
        module_name (str): optinal name of the module. By default equal to file name.
        extra_namespace_objs (dict): optional extra objects to include in module's namespace
    Returns:
        module: the imported module
    """
    if not module_name:
        module_name = os.path.splitext(os.path.basename(module_path))[0]

    # Don't import the same module twice
    if module_name in sys.modules:
        return sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    # Add extra objects to module's namespace
    if extra_namespace_objs:
        for key, value in extra_namespace_objs.items():
            vars(module)[key] = value

    spec.loader.exec_module(module)

    return sys.modules[module_name]


def nix_permission_hack(path):
    """Set write permissions on all files and subdirectories in a given directory
    This is a hack to prevent issues with permissions on Nix systems.
    """
    os.system("chmod -R ug+w " + path)


def assert_attributes(
    func, kwargs, error_msg="Function [func] does not support argument '[arg]'!"
):
    """Assert that given function supports the given arguments
    :param func: function to check for compatible arguments
    :param kwargs: arguments to check
    """
    for arg in kwargs:
        if arg not in inspect.signature(func).parameters:
            fail_with_msg(error_msg.replace("[func]", str(func)).replace("[arg]", arg))


def get_lib_cores():
    """Search for py2hwsw library cores and return a list with their file paths"""
    lib_path = os.path.join(os.path.dirname(__file__), "../lib")
    cores = []
    # Find all .py files under lib_path
    for root, dirs, files in os.walk(lib_path):
        # Skip specific directories
        if os.path.basename(root) in ["scripts", "test", "document"]:
            dirs[:] = []
            continue
        for file in files:
            if file.endswith(".py") or file.endswith(".json"):
                cores.append(os.path.join(root, file))
                # Skip subdirectories of this core to avoid including subblocks specific of this core
                dirs[:] = []
                continue
    return cores


# Browse/Copy/Manage py2hwsw files
# https://github.com/IObundle/iob-soc/pull/975#discussion_r1843025005
def list_dir(path):
    """
    Lists the contents of a directory.
    Args:
        path (str): The path to the directory.
    Returns:
        list: A list of files and directories in the given path.
    """
    try:
        print("\n".join(os.listdir(path)))
    except FileNotFoundError:
        print(f"Directory '{path}' not found.")
        exit(1)


def copy_dir(src, dest):
    """
    Copies the contents of a directory to another directory.
    Args:
        src (str): The source directory path.
        dest (str): The destination directory path.
    Returns:
        None
    """
    try:
        if os.path.isfile(src):
            shutil.copy(src, dest)
        else:
            shutil.copytree(src, dest)
        nix_permission_hack(dest)
    except FileNotFoundError:
        print(f"Directory '{src}' not found.")
        exit(1)
    except FileExistsError:
        print(f"Directory '{dest}' already exists.")
        exit(1)


def cat_file(path):
    """
    Prints the contents of a file.
    Args:
        path (str): The path to the file.
    Returns:
        None
    """
    try:
        with open(path, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        exit(1)


def validate_verilog_const(value: str, direction: str):
    """Validate if constant is a valid Verilog constant and if it is compatible with the direction
    :param value: constant to validate
    :param direction: direction of the constant (input or output)"""
    if direction == "input":
        assert (
            "'" in value
        ), f"{iob_colors.FAIL}Invalid format for bus '{value}'! Expected <width>'<base><value>', got {value}.{iob_colors.ENDC}"

        _bases = {"b": "01", "d": "0123456789", "h": "0123456789abcdef"}
        _, _v = value.split("'")
        if _v[0] not in _bases:
            fail_with_msg(
                f"Invalid base for bus '{value}'! Expected b, d or h, got {_v[0]}."
            )
        elif not all(c in _bases[_v[0]] for c in _v[1:]):
            fail_with_msg(
                f"Invalid value for bus '{value}'! Expected [{_bases[_v[0]]}], got {_v[1:]}."
            )
    elif direction == "output":
        assert (
            "z" in value.lower()
        ), f"{iob_colors.FAIL}If not connected, output bus '{value}' must be a high impedance value (z)!{iob_colors.ENDC}"

    else:
        fail_with_msg(
            f"Invalid direction '{direction}' for bus '{value}'! Expected input or output."
        )


def update_obj_from_dict(obj, attributes_dict, preprocessor_functions={}, valid_attributes_list=[], key_attribute_mapping={}):
    """
    Update a given object's attributes with values from a dictionary.
    Supports mapping keys to different attribute names.
    Supports preprocessor functions for attribute's values.

    Attributes:
        obj (object): The object to update with new attribute values.
        attributes_dict (dict): The attributes and their values, in dictionary format.
        key_attribute_mapping (dict): Dictionary of key to attribute name mappings. Given dictionary keys will be replaced with corresponding attribute names.
            Example mapping:
                key_attribute_mapping = {
                    "key_name": "attribute_name",
                    "descr": "description",
                    "min": "min_value",
                    "max": "max_value",
                }
        preprocessor_functions (dict): Dictionary of attribute preprocessor functions. Each attribute's value will be preprocessed by the corresponding function before being set. Normally used to convert subdictionaries into objects.
            Example mapping:
                preprocessor_functions = {
                    "attribute_name": preprocessor_function_name,
                    "ports": port_from_dict,
                    "buses": bus_from_dict,
                    "snippets": snippet_from_dict,
                }
        valid_attributes_list (list): List of valid attributes for the given object. All valid if empty.
    """
    # Fill attributes
    for key, value in attributes_dict.items():
        # Find attribute name based on key-attribute mapping
        attribute_name = key_attribute_mapping.get(key, key)
        # Only allow valid attributes (if any specified)
        if valid_attributes_list:
            if attribute_name not in valid_attributes_list:
                fail_with_msg(f"Attribute '{attribute_name}' is not valid for object '{obj}'.")
        # Sanity check
        if not hasattr(obj, attribute_name):
            fail_with_msg(f"Attribute '{attribute_name}' does not exist for object '{obj}'.")
        # Check if should preprocess value
        if attribute_name in preprocessor_functions:
            value = preprocessor_functions[attribute_name](value)
        # Set attribute
        setattr(obj, attribute_name, value)


def find_common_deep(path1, path2):
    """Find common files (recursively) inside two given directories
    Taken from: https://stackoverflow.com/a/51625515
    :param str path1: Directory path 1
    :param str path2: Directory path 2
    """
    return set.intersection(
        *(
            set(
                os.path.relpath(os.path.join(root, file), path)
                for root, _, files in os.walk(path)
                for file in files
            )
            for path in (path1, path2)
        )
    )


#
# Utility functions
#


def empty_list():
    return field(default_factory=list)


def empty_dict():
    return field(default_factory=dict)
