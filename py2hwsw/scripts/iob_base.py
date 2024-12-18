# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os
import shlex
import argparse
from dataclasses import dataclass
import importlib
import traceback
import re
from functools import wraps
import inspect

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
        """
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
            properties.set_handler = lambda v: setattr(self, name, v)
        if descr:
            properties.descr = descr

        self.ATTRIBUTE_PROPERTIES[name] = properties


@dataclass
class iob_attribute_properties:
    """Class that stores properties of an attribute"""

    datatype: object = None
    # Function to use to set the attribute value based on info given in the 'py2hw'
    # interface
    set_handler: object = None
    descr: str = "Default attribute description"


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
            for arg in kwargs:
                if arg in dicts and kwargs[arg] is not None:
                    if isinstance(dicts[arg], str):
                        if dicts[arg] == "pairs":
                            kwargs[arg] = dict(pair.split(":") for pair in kwargs[arg])
                    elif isinstance(dicts[arg], list):
                        _keys = [key for item in dicts[arg] for key in item.split(":")]
                        _values = [
                            value for item in kwargs[arg] for value in item.split(":")
                        ]
                        kwargs[arg] = [
                            dict(zip(_keys, _values[i:]))
                            for i in range(0, len(_values), len(_keys))
                        ]
                    elif isinstance(dicts[arg], tuple):
                        kwargs[arg] = dict(zip(dicts[arg], kwargs[arg]))
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
    param filter_extensions: list of extensions to filter
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


def import_python_module(module_path, module_name=None):
    """Import a python module from a given filepath
    param module_path: path of the module's python file
    param module_name: optinal name of the module. By default equal to file name.
    """
    # Don't import the same module twice
    if module_name in sys.modules:
        return
    if not module_name:
        module_name = os.path.splitext(os.path.basename(module_path))[0]
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
