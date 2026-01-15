# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os
import shlex
import argparse
from dataclasses import dataclass
import importlib
import traceback
from functools import wraps
import inspect
import shutil

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


def convert_dict2obj_list(dict_list: dict, obj_class):
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


def process_elements_from_list(list2process: list, process_func):
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


def debug(msg, level=0):
    """Print a message if project debug_level >= level
    :param str msg: message to print
    :param int level: debug level
    """
    if debug_level >= level:
        print(f"[Debug {level}]: " + msg)


#
# Decorators
#


def str_to_kwargs(attrs: list):
    """Decorator to convert a string to keyword arguments.
    @param attrs: list of attributes to parse
        for a positional argument, its element should be a string
        for a keyword argument, its element should be a list with the following format:
            [flag, dest, kwargs, case]
            flag: str, the flag to use in the command line
            dest: str, the name of the argument
            kwargs: dict, the keyword arguments to pass to the add_argument method
            case: str, a keyword to describe a special case
        for a parser, its element should be a dictionary with the following format:
            {parser_name: list}
            parser_name: str, the name of the parser
            list: list, the list of attributes to parse
            parser_name can have the following format:
                parser_name or parser_name&dest if the name in the string and the name in the parser are different
    """

    def create_parsers(attrs: list, parser_name: str = "main") -> dict:
        """Create a dictionary of parsers and other usefull information"""
        parser = argparse.ArgumentParser()
        dicts = {}
        parser_dest = parser_name
        if "&" in parser_name:
            parser_name, parser_dest = parser_name.split("&")
        parser_dict = {
            parser_name: {
                "parser": parser,
                "dicts": dicts,
                "vars": {},
                "dest": parser_dest,
            }
        }
        if (d := ["-d", "descr"]) not in attrs:
            attrs.append(d)
        for attr in attrs:
            if isinstance(attr, str):
                parser.add_argument(attr)
            elif isinstance(attr, list):
                args = None
                if len(attr) >= 3:
                    if len(attr) == 4:
                        dicts[attr[1]] = attr[3]
                    parser.add_argument(attr[0], dest=attr[1], **attr[2])
                else:
                    parser.add_argument(attr[0], dest=attr[1])
            elif isinstance(attr, dict):
                for key, value in attr.items():
                    new_dict = create_parsers(value, key)
                    parser_dict[parser_name]["vars"].update({key.split("&")[0]: []})
                    parser_dict.update(new_dict)
        return parser_dict

    def parse_args(parser_dict: dict, args: list) -> dict:
        """Parse the arguments of a list given a dictionary of parsers
        The first element of the list must be the key of the parser
        """
        key = args[0]
        parser = parser_dict[key]["parser"]
        dicts = parser_dict[key]["dicts"]
        args = args[1:]
        args = parser.parse_args(args)
        kwargs = vars(args)
        try:
            for arg in list(kwargs.keys()):
                if arg in dicts and kwargs[arg] is not None:
                    if isinstance(dicts[arg], str):
                        if dicts[arg] == "pairs":
                            kwargs[arg.split("&")[0]] = dict(
                                pair.split(":") for pair in kwargs[arg]
                            )
                    elif isinstance(dicts[arg], list):
                        _keys = [key for item in dicts[arg] for key in item.split(":")]
                        _values = [
                            value for item in kwargs[arg] for value in item.split(":")
                        ]
                        kwargs[arg.split("&")[0]] = [
                            dict(zip(_keys, _values[i:]))
                            for i in range(0, len(_values), len(_keys))
                        ]
                    elif isinstance(dicts[arg], tuple):
                        kwargs[arg.split("&")[0]] = dict(zip(dicts[arg], kwargs[arg]))
                    if "&" in arg:
                        kwargs.pop(arg)
            for key, value in list(kwargs.items()):
                if ":" in key:
                    kwargs.pop(key)
                    keys = key.split(":")
                    if isinstance(value, list):
                        values = [pair.split(":") for pair in value]
                        for i in range(len(keys)):
                            kwargs[keys[i]] = [v[i] for v in values]
                    else:
                        values = value.split(":")
                        for i in range(len(keys)):
                            kwargs[keys[i]] = values[i]

        except Exception as e:
            print(
                iob_colors.FAIL
                + f"Failed to parse arguments:\n"
                + str(args)
                + "\nException: "
                + str(e)
                + iob_colors.ENDC
            )
            exit(1)
        return {k: v for k, v in kwargs.items() if v is not None}

    def organize_kwargs(parser_dict: dict, string: str) -> dict:
        """Splits the strint into a list of lists and parse each list with the correct parser
        The first element of the list must be the key of the parser
        The hyerarchy of the parsers is defined by the order of the elements in the list and the parser_dict
        """
        args = ["main"] + shlex.split(string)
        lists = []
        while args:
            key = args.pop(0)
            if key in parser_dict:
                lists.append([key])
            else:
                lists[-1].append(key)

        def make_hierarchy(sub_lists: list, parser: str) -> dict:
            if parser_dict[parser]["vars"] != {}:
                output = {}
                output[parser_dict[parser]["dest"]] = []
                sub_kwargs = {}
                sub_kwargs[parser] = []
                last_key = None
                for key in parser_dict[parser]["vars"]:
                    output[parser_dict[key]["dest"]] = []
                    sub_kwargs[key] = []
                while sub_lists:
                    element = sub_lists.pop(0)
                    if (
                        element[0] in parser_dict[parser]["vars"]
                        or element[0] == parser
                    ):
                        key = element[0]
                        sub_kwargs[key].append(element)
                        last_key = key
                    else:
                        sub_kwargs[last_key][-1].append(element)
                for key in sub_kwargs.keys():
                    if parser_dict[key]["vars"] != {} and key != parser:
                        output[parser][-1].update(make_hierarchy(sub_kwargs[key], key))
                    else:
                        for sub_list in sub_kwargs[key]:
                            extracted = [
                                item for item in sub_list if isinstance(item, list)
                            ]
                            not_extracted = [
                                item for item in sub_list if not isinstance(item, list)
                            ]
                            output[parser_dict[key]["dest"]].append(
                                parse_args(parser_dict, not_extracted)
                            )
                            if extracted:
                                output[parser_dict[key]["dest"]][-1].update(
                                    make_hierarchy(extracted, key)
                                )
            else:
                if isinstance(sub_lists, list):
                    sub_lists = sub_lists[0]
                output = parse_args(parser_dict, sub_lists)
            for key in output.keys():
                if isinstance(output[key], list):
                    for i in range(len(output[key])):
                        if "core_name" in output[key][i]:
                            output[key][i]["instance_description"] = output[key][i].pop(
                                "descr"
                            )
            return {k: v for k, v in output.items() if v != []}

        kwargs = make_hierarchy(lists, "main")
        if "main" in kwargs:
            return kwargs["main"][0]
        return kwargs

    def decorator(func):
        @wraps(func)
        def wrapper(core, *args, **kwargs):
            if len(args) == 1 and isinstance(args[0], str):
                parser_dict = create_parsers(attrs)
                lines = [line.strip() for line in args[0].split("\n\n") if line.strip()]
                for line in lines:
                    kwargs = organize_kwargs(parser_dict, line)
                    func(core, **kwargs)
                return None
            else:
                return func(core, *args, **kwargs)

        return wrapper

    return decorator


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


def import_python_module(module_path, module_name=None):
    """Import a python module from a given filepath
    param module_path: path of the module's python file
    param module_name: optinal name of the module. By default equal to file name.
    """
    if not module_name:
        module_name = os.path.splitext(os.path.basename(module_path))[0]

    # Don't import the same module twice
    if module_name in sys.modules:
        return

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)


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
        ), f"{iob_colors.FAIL}Invalid format for wire '{value}'! Expected <width>'<base><value>', got {value}.{iob_colors.ENDC}"

        _bases = {"b": "01", "d": "0123456789", "h": "0123456789abcdef"}
        _, _v = value.split("'")
        if _v[0] not in _bases:
            fail_with_msg(
                f"Invalid base for wire '{value}'! Expected b, d or h, got {_v[0]}."
            )
        elif not all(c in _bases[_v[0]] for c in _v[1:]):
            fail_with_msg(
                f"Invalid value for wire '{value}'! Expected [{_bases[_v[0]]}], got {_v[1:]}."
            )
    elif direction == "output":
        assert (
            "z" in value.lower()
        ), f"{iob_colors.FAIL}If not connected, output wire '{value}' must be a high impedance value (z)!{iob_colors.ENDC}"

    else:
        fail_with_msg(
            f"Invalid direction '{direction}' for wire '{value}'! Expected input or output."
        )


def find_folder_by_name(root_dir, folder_name):
    """
    Searches for a folder by name within a given root directory.

    Args:
        root_dir (str): The directory to start the search from.
        folder_name (str): The name of the folder to search for.

    Returns:
        str: The full path to the found folder, or None if not found.
    """
    for root, dirs, files in os.walk(root_dir):
        if folder_name in dirs:
            return os.path.join(root, folder_name)
    return None

def try_evaluate(math_str):
    """
    Evaluate a mathematical expression safely.

    Args:
        math_str (str): The mathematical expression to evaluate.

    Returns:
        Union[int, float, str]: The evaluated result as int or float, or the original string if evaluation fails.
    """
    try:
        # Evaluate with restricted globals/locals for security
        result = eval(math_str, {"__builtins__": None}, {})

        # Check if result is a float but has no decimal part
        if isinstance(result, float) and result.is_integer():
            return int(result)
        # Keep as float if there are actual decimals
        return result
    except Exception:
        # Return original string if evaluation fails
        return math_str
