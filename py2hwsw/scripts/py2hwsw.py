#!/usr/bin/env python3

import sys
import argparse

import iob_base
from iob_base import fail_with_msg
from iob_core import iob_core

PY2HWSW_VERSION = "0.7.13"

if __name__ == "__main__":
    sys.dont_write_bytecode = True

    parser = argparse.ArgumentParser(
        description="Python to hardware/software generator"
    )
    parser.add_argument("core_name", type=str, help="The name of the core to use.")
    parser.add_argument(
        "target",
        type=str,
        default="setup",
        help="The target action to perform on the core.",
        choices=[
            "setup",
            "clean",
            "print_build_dir",
            "print_core_dict",
            "print_py2hwsw_attributes",
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
        "--debug_level",
        dest="debug_level",
        type=int,
        default=0,
        help="Set the debug level (default: 0)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {PY2HWSW_VERSION}",
    )
    args = parser.parse_args()

    # print(f"Args: {args}", file=sys.stderr)  # DEBUG

    iob_core.global_build_dir = args.build_dir
    iob_core.global_project_root = args.project_root
    iob_core.global_project_vformat = args.verilog_format
    iob_core.global_project_vlint = args.verilog_lint
    iob_base.debug_level = args.debug_level

    py_params = {}
    if args.py_params:
        for param in args.py_params.split(":"):
            k, v = param.split("=")
            py_params[k] = v

    if args.target == "setup":
        iob_core.get_core_obj(args.core_name, **py_params)
    elif args.target == "clean":
        iob_core.clean_build_dir(args.core_name)
    elif args.target == "print_build_dir":
        iob_core.print_build_dir(args.core_name)
    elif args.target == "print_core_dict":
        iob_core.print_core_dict(args.core_name)
    elif args.target == "print_py2hwsw_attributes":
        iob_core.print_py2hwsw_attributes(args.core_name)
    else:
        fail_with_msg(f"Unknown target: {args.target}")
