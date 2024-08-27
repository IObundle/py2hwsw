from dataclasses import dataclass
import re
from iob_base import fail_with_msg
from iob_wire import find_signal_in_wires
from iob_signal import get_real_signal


@dataclass
class iob_snippet:
    """Class to represent a Verilog snippet in an iob module"""

    # List of outputs of this snippet (use to generate global wires)
    verilog_code: str = ""

def create_snippet(core, *args, **kwargs):
    """Create a Verilog snippet to insert in given core."""
    # Ensure 'snippets' list exists
    core.set_default_attribute("snippets", [])
    snippet = iob_snippet(*args, **kwargs)
    core.snippets.append(snippet)
