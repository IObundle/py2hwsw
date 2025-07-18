# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field

from iob_base import parse_short_notation_text

FAIL = "\033[91mError: "  # Red
ENDC = "\033[0m"  # White


@dataclass
class iob_csr:
    """Class to represent a Control/Status Register."""

    name: str = ""
    kind: str = "REG"
    mode: str = ""
    n_bits: str or int = 1
    rst_val: int = 0
    addr: int = -1
    log2n_items: int = 0
    descr: str = "Default description"
    # Select if should generate internal buses or ports for this CSR
    internal_use: bool = False
    # List of configurations that use this CSR (used for documentation)
    doc_conf_list: list or None = None
    volatile: bool = True
    # Bit fields
    fields: list or None = None
    # Asymetric ration between internal and external interfaces address
    # asym >= 1: W_INT = W_EXT * asym
    # asym <= -1: W_INT = W_EXT / (-asym)
    asym: int = 1
    # Optional comment to include in generated verilog of each csr (inside *_csrs.v)
    optional_comment: str = ""

    def validate_attributes(self):
        # TODO: Implement this method in a similar fashion as the Py2HWSW ones
        pass

    def __post_init__(self):
        if not self.name:
            fail_with_msg("CSR name is not set", ValueError)

        if self.kind not in ["REG", "NOAUTO"]:
            # FUTURE IMPROVEMENT: Add REGFILE type (different from regarray) to instantiate LUTRAMs.
            fail_with_msg(f"Invalid CSR type: '{self.kind}'", ValueError)

        if self.mode not in ["R", "W", "RW"]:
            fail_with_msg(f"Invalid CSR mode: '{self.mode}'", ValueError)

        if self.asym == 0:
            fail_with_msg(
                "CSR asym attribute cannot be 0. Must be either >= 1 or <= -1.",
                ValueError,
            )

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
        else:  # Convert fields to objects
            self.fields = convert_dict2obj_list(self.fields, csr_field)

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
    # Similar to 'modifiedWriteValue' in IPxact.
    write_action: str = ""
    # SImilar to 'readAction' in IPxact
    read_action: str = ""

    def __post_init__(self):
        if not self.name:
            fail_with_msg("CSR field name is not set", ValueError)

        if self.mode not in ["R", "W", "RW"]:
            fail_with_msg(
                f"Invalid CSR field mode '{self.mode}' in field '{self.name}'",
                ValueError,
            )

        if self.write_action not in [
            "",  # Indicates that the value written to a field is the value stored in the field. This is the default.
            "oneToClear",  # Each written '1' bit will assign the corresponding bit to '0'.
            "oneToSet",  # Each written '1' bit will assign the corresponding bit to '1'.
            "oneToToggle",  # Each written '1' bit will toggle the corresponding bit.
            "zeroToClear, zeroToSet, zeroToToggle",  # Similar to previous ones, except that written '0' bit triggers the action.
            "clear",  # Each write operation will clear all bits in the field to '0'.
            "set",  # Each write operation will set all bits in the field to '1'.
            "modify",  # Indicates that after a write operation all bits in the field can be modified.
        ]:
            fail_with_msg(
                f"Invalid CSR write_action: '{self.write_action}'", ValueError
            )

        if self.read_action not in [
            "",  # Indicates that field is not modified after a read operation. This is the default.
            "clear",  # All bits in the field are cleared to '0' after a read operation.
            "set",  # All bits in the field are set to '1' after a read operation.
            "modify",  # Indicates that the bits in the field are modified in some way after a read operation.
        ]:
            fail_with_msg(f"Invalid CSR read_action: '{self.read_action}'", ValueError)


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

    # FIXME: call this validate_attributes. Maybe in a similar fashion as Py2HWSW ones
    def validate_attributes(self):
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
            "descr": "Core configuration.",
        }

    # Convert user reg dictionaries into 'iob_csr' objects
    csr_obj_list = convert_dict2obj_list(regs, iob_csr)
    csr_group = iob_csr_group(regs=csr_obj_list, **group_kwargs)
    return csr_group


def iob_csr_text2dict(csr_text: str):
    """Convert iob_csr short notation text to dictionary
    Attributes:
        csr_text (str): short notation text. Specified with the following format:
            name:width [-k KIND] [-m MODE] [--ret_val RST_VAL] [--addr ADDR]
            [-d descr] [--int_use] [--field FIELD]+ [--doc_conf DOC_CONF]+
            [--no-volatile] [--assym A] [--opt_comment COMMENT]
            Example:
                "softreset:1 -m W -d 'Soft reset' --rst_val 0 --addr 0 --log2n_items 0

    Returns:
        dict: dictionary with iob_csr attributes
    """
    csr_flags = [
        "name&width",
        ["-k", {"dest": "kind", "choices": ["REG", "NOAUTO"]}],
        ["-m", {"dest": "mode", "choices": ["R", "W", "RW"]}],
        ["--rst_val", {"dest": "rst_val"}],
        ["--addr", {"dest": "addr"}],
        ["--log2n_items", {"dest": "log2n_items"}],
        ["-d", {"dest": "descr"}],
        ["--doc_conf", {"dest": "doc_conf_list", "action": "append"}],
        ["--no-volatile", {"dest": "volatile", "action": "store_false"}],
        ["--int_use", {"dest": "internal_use", "action": "store_true"}],
        ["--field", {"dest": "fields", "action": "append"}],
        ["--assym", {"dest": "assym"}],
        ["--opt_comment", {"dest": "optional_comment"}],
    ]

    csr_dict = parse_short_notation_text(csr_text, csr_flags)
    # process 'name&width', with format '[name]:[width]'
    name_and_width = csr_dict.pop("name&width", "")
    try:
        csr_dict["name"], csr_dict["width"] = name_and_width.split(":", 1)
    except ValueError:
        csr_dict["name"] = name_and_width
        csr_dict["width"] = 1  # default width 1 if not specified
    return csr_dict


def iob_csr_group_text2dict(csr_group_text: str):
    """Convert iob_csr_group short notation text to dictionary
    Attributes:
        csr_group_text (str): short notation text
            [csr group name] [-d descr] [-r reg]+ [-doc] [-doc_clearpage]
            See `iob_csr_text2dict()` for `csr` format details.
            Example:
                ctrl_regs
                -d 'control registers'
                -doc
                -doc_clearpage
                -r "softreset:1 -m W -d 'Soft reset' --rst_val 0 --addr 0 --log2n_items 0"
                -r "start:1 -m W -d 'Start operation' --rst_val 0 --addr 1 --log2n_items 1"
                -r "done:1 -m R -d 'Operation Complete' --rst_val 1 --addr 2 --log2n_items 1"

    Returns:
        dict: dictionary with iob_csr attributes
    """
    csr_group_flags = [
        "name",
        ["-d", {"dest": "descr"}],
        ["-doc", {"dest": "doc_only", "action": "store_true"}],
        ["-doc_clearpage", {"dest": "doc_clearpage", "action": "store_true"}],
        ["-r", {"dest": "regs", "action": "append"}],
    ]

    csr_group_dict = parse_short_notation_text(csr_group_text, csr_group_flags)
    # process regs
    csr_group_regs = []
    for r in csr_group_dict.get("regs", []):
        # Convert each reg from text to dict
        csr_group_regs.append(iob_csr_text2dict(r))
    # update csr_group regs
    csr_group_dict.update({"regs": csr_group_regs})
    return csr_group_dict
