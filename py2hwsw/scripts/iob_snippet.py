from dataclasses import dataclass, field
import re
from typing import List
from iob_base import fail_with_msg
from iob_wire import *
from iob_signal import iob_signal


@dataclass
class iob_snippet:
    """Class to represent a Verilog snippet in an iob module"""

    # List of outputs of this snippet (use to generate global wires)
    verilog_code: str = ""

    def set_needed_reg(self, core):
        assign_regex = re.compile(r"\bassign\s+(\w+)\s*=")
        blocking_regex = re.compile(r"\b(\w+)\s*=")
        non_blocking_regex = re.compile(r"\b(\w+)\s*<=")

        outputs = set()

        for match in blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in non_blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in assign_regex.findall(self.verilog_code):
            outputs.discard(match)

        for signal_name in outputs:
            if signal_name.endswith("_o"):
                signal = find_signal_in_wires(core.wires + core.ports, signal_name[:-2])
            elif signal_name.endswith("_io"):
                signal = find_signal_in_wires(core.wires + core.ports, signal_name[:-3])
            else:
                signal = find_signal_in_wires(core.wires + core.ports, signal_name)
            if signal != None:
                signal.isreg = True
            else:
                fail_with_msg(f"output '{signal_name}' not found in wires/ports lists!")


def create_snippet(core, *args, **kwargs):
    """Create a Verilog snippet to insert in given core."""
    # Ensure 'snippets' list exists
    core.set_default_attribute("snippets", [])
    snippet = iob_snippet(*args, **kwargs)
    snippet.set_needed_reg(core)
    core.snippets.append(snippet)
