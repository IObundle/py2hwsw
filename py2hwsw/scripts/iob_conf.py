# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from iob_base import str_to_kwargs, fail_with_msg, assert_attributes


@dataclass
class iob_conf:
    name: str = ""
    type: str = ""
    val: str | int | bool = ""
    min: str | int = 0
    max: str | int = 1
    descr: str = "Default description"
    # Only set this macro if the Verilog macro specified here is defined
    if_defined: str = ""
    if_not_defined: str = ""

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Every conf must have a name!")
        if not self.type:
            fail_with_msg(f"Conf '{self.name}' must have a type!")
        elif self.type not in ["M", "P", "F"]:
            fail_with_msg(f"Conf '{self.name}' type must be either M, P or F!")

        try:
            val = int(self.val)
            min = int(self.min)
            max = int(self.max)
            if val < min or val > max:
                fail_with_msg(
                    f"Conf '{self.name}' value '{val}' must be between {min} and {max}!"
                )
        except ValueError:
            pass


attrs = ["name", ["-t", "type"], ["-v", "val"], ["-m", "min"], ["-M", "max"]]


@str_to_kwargs(attrs)
def create_conf(core, *args, **kwargs):
    """Creates a new conf object and adds it to the core's conf list
    param core: core object
    """
    # Ensure 'confs' list exists
    core.set_default_attribute("confs", [])
    assert_attributes(
        iob_conf,
        kwargs,
        error_msg=f"Invalid {kwargs.get("name", "")} conf attribute '[arg]'!",
    )
    conf = iob_conf(*args, **kwargs)
    core.confs.append(conf)
