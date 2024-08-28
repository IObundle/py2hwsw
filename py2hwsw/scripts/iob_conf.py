from dataclasses import dataclass
from iob_base import str_to_kwargs

@dataclass
class iob_conf:
    name: str = ""
    type: str = ""
    val: str | bool = ""
    min: str | int = 0
    max: str | int = 1
    descr: str = "Default description"
    # Only set this macro if the Verilog macro specified here is defined
    if_defined: str = ""
    if_not_defined: str = ""

    def __post_init__(self):
        if not self.name:
            raise Exception("Conf name is required")
        if not self.type:
            raise Exception("Conf type is required")
        elif self.type not in ["M", "P", "F"]:
            raise Exception("Conf type must be either M, P or F")

attrs = {0: "name", 1: "type", 2: "val", "m": "min", "M": "max", "D": "descr"}
@str_to_kwargs(attrs)
def create_conf(core, *args, **kwargs):
    """Creates a new conf object and adds it to the core's conf list
    param core: core object
    """
    # Ensure 'confs' list exists
    core.set_default_attribute("confs", [])
    conf = iob_conf(*args, **kwargs)
    core.confs.append(conf)
