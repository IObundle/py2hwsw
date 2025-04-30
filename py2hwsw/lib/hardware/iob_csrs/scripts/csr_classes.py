# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field

FAIL = "\033[91mError: "  # Red
ENDC = "\033[0m"  # White


@dataclass
class iob_csr:
    """Class to represent a Control/Status Register."""

    name: str = ""
    mode: str = ""
    n_bits: str or int = 1
    rst_val: int = 0
    addr: int = -1
    log2n_items: int = 0
    autoreg: bool = True
    descr: str = "Default description"
    # Select if should generate internal wires or ports for this CSR
    internal_use: bool = False
    # List of configurations that use this CSR (used for documentation)
    doc_conf_list: list or None = None
    volatile: bool = True
    # Bit fields
    fields: list or None = None

    def __post_init__(self):
        if not self.name:
            fail_with_msg("CSR name is not set", ValueError)

        if self.mode not in ["R", "W", "RW"]:
            fail_with_msg(f"Invalid CSR mode: '{self.mode}'", ValueError)

        # try to convert n_bits to int
        try:
            self.n_bits = int(self.n_bits)
        except ValueError:
            pass

        if not self.fields:
            self.fields = [
                csr_field(
                    name=self.name,
                    mode=self.mode,
                    base_bit=0,
                    width=self.n_bits,
                    volatile=self.volatile,
                    rst_val=self.rst_val,
                )
            ]
            # fail_with_msg(f"CSR '{self.name}' has no bit fields", ValueError)

        # Check if fields properties match CSR properties
        for _field in self.fields:
            if self.mode == "R" and _field.mode != "R":
                fail_with_msg(
                    f"CSR '{self.name}' defined with mode '{self.mode}' has invalid field mode '{_field.mode}'.",
                    ValueError,
                )
            elif self.mode == "W" and _field.mode != "W":
                fail_with_msg(
                    f"CSR '{self.name}' defined with mode '{self.mode}' has invalid field mode '{_field.mode}'.",
                    ValueError,
                )

            # CSR may have non-volatile fields and be volatile itself, but not vice versa
            if not self.volatile and _field.volatile:
                fail_with_msg(
                    f"CSR '{self.name}' defined as non-volatile but has volatile field '{_field.name}'.",
                    ValueError,
                )

        # Don't try to manage field bits, if n_bits is not integer (likely contains parameters)
        if type(self.n_bits) is not int:
            return

        # CSRs should have width multiple of 8 bits
        quantized_n_bits = (self.n_bits + 7) // 8 * 8

        # List of csr bits. Value corresponds to index of associated field. -1 means free.
        used_bits = [-1 for i in range(quantized_n_bits)]
        # Check if any fields overlap
        for idx, _field in enumerate(self.fields):
            for bit in range(_field.base_bit, _field.base_bit + _field.width):
                if used_bits[bit] > -1:
                    fail_with_msg(
                        f"CSR '{self.name}' has overlapping fields: '{_field.name}' and '{self.fields[used_bits[bit]].name}'.",
                        ValueError,
                    )
                used_bits[bit] = idx

        # Automatically create RSVD fields for unused bits
        width = 0
        for idx, bit in enumerate(used_bits):
            if bit < 0:
                width += 1
            elif width > 0:
                self.fields.append(
                    csr_field(
                        name="RSVD", mode=self.mode, base_bit=idx - width, width=width
                    )
                )
                width = 0
        if width > 0:
            self.fields.append(
                csr_field(
                    name="RSVD",
                    mode=self.mode,
                    base_bit=len(used_bits) - width,
                    width=width,
                )
            )


@dataclass
class csr_field:
    name: str = ""
    mode: str = ""
    base_bit: int = 0
    width: int = 1
    volatile: bool = True
    rst_val: int = 0

    def __post_init__(self):
        if not self.name:
            fail_with_msg("CSR field name is not set", ValueError)

        if self.mode not in ["R", "W", "RW"]:
            fail_with_msg(f"Invalid CSR field mode: '{self.mode}'", ValueError)


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
