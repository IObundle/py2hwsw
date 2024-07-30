from dataclasses import dataclass, field
from iob_snippet import iob_snippet


@dataclass
class iob_fsm(iob_snippet):
    """Class to represent a Verilog finite state machine in an iob module"""


def create_fsm(core, *args, **kwargs):
    """Create a Verilog finite state machine to insert in a given core."""
    # Ensure 'fsms' list exists
    core.set_default_attribute("fsms", [])
    #TODO: go through arguments and build verilog code and add clk rst en if necessary

    fsm = iob_fsm(verilog_code=verilog_code)
    fsm.set_needed_reg(core)
    core.fsms.append(fsm)
