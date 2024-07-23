from dataclasses import dataclass, field
import re
from typing import List


@dataclass
class iob_snippet:
    """Class to represent a Verilog snippet in an iob module"""

    # List of outputs of this snippet (use to generate global wires)
    outputs: List[str] = field(default_factory=list)
    verilog_code: str = ""

    def __post_init__(self):
        """If outputs list is empty, parse verilog_code to find them"""
        if self.outputs == []:
            self.parse_outputs()

    def parse_outputs(self):
        assign_regex = re.compile(r'\bassign\s+(\w+)\s*=')
        blocking_regex = re.compile(r'\b(\w+)\s*=')
        non_blocking_regex = re.compile(r'\b(\w+)\s*<=')

        outputs = set()

        for match in assign_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in non_blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for signal in outputs:
            if signal.endswith("_o"):
                self.outputs.append(signal[:-2])
            elif signal.endswith("_io"):
                self.outputs.append(signal[:-3])
            else:
                self.outputs.append(signal)

def create_snippet(core, *args, **kwargs):
    """Create a Verilog snippet to insert in given core."""
    # Ensure 'snippets' list exists
    core.set_default_attribute("snippets", [])
    snippet = iob_snippet(*args, **kwargs)
    core.snippets.append(snippet)
