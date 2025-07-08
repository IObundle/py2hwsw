#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os
import argparse

import iob_base
from iob_base import list_dir, copy_dir, cat_file
from iob_core import iob_core

from py2hwsw_version import PY2HWSW_VERSION

if __name__ == "__main__":
    sys.dont_write_bytecode = True

    parser = argparse.ArgumentParser(
        description="Python to hardware/software generator"
    )
    parser.add_argument(
        "core_name", nargs="?", type=str, help="The name of the core to use."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=str,
        default="setup",
        help="The target action to perform on the core.",
        choices=[
            "setup",
            "clean",
            "print_build_dir",
            "print_core_name",
            "print_core_version",
            "print_core_dict",
            "deliver",
        ],
    )
    parser.add_argument(
        "--build_dir",
        dest="build_dir",
        type=str,
        default="",
        help="The core's build directory",
    )
    parser.add_argument(
        "--project_root",
        dest="project_root",
        type=str,
        default=".",
        help="The project root directory",
    )
    parser.add_argument(
        "--py_params",
        dest="py_params",
        type=str,
        help="Parameters to pass to the `setup` function of the core's python module. "
        "Parameters will be passed as a dictionary to the `setup` function. "
        # Would be nice to use spaces between params but not possible due to argparse bug:
        # https://github.com/python/cpython/pull/20924
        "Format: param1=value1:param2=value2:...",
    )

    parser.add_argument(
        "--no_verilog_format",
        dest="verilog_format",
        action="store_false",
        help="Disable verilog formatter",
    )
    parser.add_argument(
        "--no_verilog_lint",
        dest="verilog_lint",
        action="store_false",
        help="Disable verilog linter",
    )
    parser.add_argument(
        "--clang_rules",
        dest="clang_rules",
        type=str,
        help="Path to custom clang-format rules file.",
    )
    parser.add_argument(
        "--debug_level",
        dest="debug_level",
        type=int,
        default=0,
        help="Set the debug level (default: 0)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {PY2HWSW_VERSION}",
    )
    parser.add_argument(
        "--py2hwsw_docs",
        dest="py2hwsw_docs",
        action="store_true",
        help="Setup Py2HWSW documentation directory",
    )
    parser.add_argument(
        "--print_py2hwsw_attributes",
        dest="print_py2hwsw_attributes",
        action="store_true",
        help="Print supported Py2HWSW core dictionary attributes",
    )
    parser.add_argument(
        "--print_lib_cores",
        dest="print_lib_cores",
        action="store_true",
        help="Print cores provided by Py2HWSW's library",
    )
    parser.add_argument(
        "--browse",
        dest="browse_lib",
        action="store_true",
        help="Generate IP-XACT library including every lib core",
    )
    # Browse/Copy/Manage py2hwsw files
    # https://github.com/IObundle/iob-soc/pull/975#discussion_r1843025005
    dirs = {
        "root": ".",
        "lib": "lib",
        "sim": "hardware/simulation",
        "fpga": "hardware/fpga",
        "syn": "hardware/syn",
    }
    for dir in dirs:
        parser.add_argument(
            f"--{dir}-ls",
            type=str,
            metavar=(f"<relative/path/to/py2hwsw/{dir}>"),
            help=f"List contents of a given {dir} directory.",
        )
        parser.add_argument(
            f"--{dir}-cp",
            type=str,
            nargs=2,
            metavar=(f"<relative/path/to/py2hwsw/{dir}>", "<destination/dir>"),
            help=f"Copy contents of a given {dir} directory.",
        )
        parser.add_argument(
            f"--{dir}-cat",
            type=str,
            metavar=(f"<relative/path/to/py2hwsw/{dir}>"),
            help=f"List contents of a given {dir} file.",
        )

    args = parser.parse_args()

    # print(f"Args: {args}", file=sys.stderr)  # DEBUG

    iob_core.global_build_dir = args.build_dir
    iob_core.global_project_root = args.project_root
    iob_core.global_project_vformat = args.verilog_format
    iob_core.global_project_vlint = args.verilog_lint
    iob_core.global_clang_format_rules_filepath = args.clang_rules
    iob_base.debug_level = args.debug_level

    if args.py2hwsw_docs:
        iob_core.setup_py2_docs(PY2HWSW_VERSION)
        exit(0)
    elif args.print_py2hwsw_attributes:
        iob_core.print_py2hwsw_attributes()
        exit(0)
    elif args.print_lib_cores:
        iob_core.print_lib_cores()
        exit(0)
    elif args.browse_lib:
        iob_core.browse_lib()
        exit(0)

    # Browse/Copy/Manage py2hwsw files
    # https://github.com/IObundle/iob-soc/pull/975#discussion_r1843025005
    for dir in dirs:
        py2hwsw_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", dirs[dir]
        )
        if args.__dict__[f"{dir}_ls"]:
            list_dir(os.path.join(py2hwsw_dir, args.__dict__[f"{dir}_ls"]))
            exit(0)
        if args.__dict__[f"{dir}_cp"]:
            copy_dir(
                os.path.join(py2hwsw_dir, args.__dict__[f"{dir}_cp"][0]),
                args.__dict__[f"{dir}_cp"][1],
            )
            exit(0)
        if args.__dict__[f"{dir}_cat"]:
            cat_file(os.path.join(py2hwsw_dir, args.__dict__[f"{dir}_cat"]))
            exit(0)

    if not args.core_name:
        parser.print_usage(sys.stderr)
        exit(1)

    py_params = {}
    if args.py_params:
        for param in args.py_params.split(":"):
            k, v = param.split("=")
            py_params[k] = v

    if args.target == "setup":
        instance = iob_core.get_core_obj(args.core_name, **py_params)
        instance.generate_build_dir()
    elif args.target == "clean":
        iob_core.clean_build_dir(args.core_name)
    elif args.target == "print_build_dir":
        iob_core.print_build_dir(args.core_name, **py_params)
    elif args.target == "print_core_name":
        iob_core.print_core_name(args.core_name, **py_params)
    elif args.target == "print_core_version":
        iob_core.print_core_version(args.core_name, **py_params)
    elif args.target == "print_core_dict":
        iob_core.print_core_dict(args.core_name, **py_params)
    elif args.target == "deliver":
        iob_core.deliver_core(args.core_name, **py_params)
