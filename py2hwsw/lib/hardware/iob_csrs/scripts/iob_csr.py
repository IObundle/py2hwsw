# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field

FAIL = "\033[91mError: "  # Red
ENDC = "\033[0m"  # White


def fail_with_msg(msg, exception_type=Exception):
    """Raise an error with a given message
    param msg: message to print
    param exception_type: type of python exception to raise
    """
    raise exception_type(FAIL + msg + ENDC)


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


@dataclass
class iob_csr:
    """Class to represent a Control/Status Register."""

    name: str = ""
    type: str = ""
    n_bits: str or int = 1
    rst_val: int = 0
    addr: int = -1
    log2n_items: int = 0
    autoreg: bool = True
    descr: str = "Default description"
    # Select if should generate internal wires or ports for this CSR
    internal_use: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("CSR name is not set", ValueError)

        if self.type not in ["R", "W", "RW"]:
            fail_with_msg(f"Invalid CSR type: '{self.type}'", ValueError)


@dataclass
class iob_csr_group:
    """Class to represent a Control/Status Register group."""

    name: str = ""
    descr: str = "Default description"
    regs: list = field(default_factory=list)
    doc_only: bool = False
    doc_clearpage: bool = False

    def __post_init__(self):
        if not self.name:
            fail_with_msg("CSR group name is not set", ValueError)


def create_csr_group(*args, **kwargs):
    """Creates a new csr group object"""

    group_kwargs = kwargs
    regs = kwargs.pop("regs", None)
    # If kwargs provided a single reg instead of a group, then create a general group for it.
    if regs is None:
        regs = [kwargs]
        group_kwargs = {
            "name": "general_operation",
            "descr": "General operation group",
        }

    # Convert user reg dictionaries into 'iob_csr' objects
    csr_obj_list = convert_dict2obj_list(regs, iob_csr)
    csr_group = iob_csr_group(regs=csr_obj_list, **group_kwargs)
    return csr_group
