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

    def set_needed_reg(self, core):
        blocking_regex = re.compile(r"^\s*(\w+)\s*=", re.MULTILINE)
        non_blocking_regex = re.compile(r"^\s*(\w+)\s*<=", re.MULTILINE)

        outputs = set()

        for match in blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in non_blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for signal_name in outputs:
            if signal_name.endswith("_o"):
                signal = find_signal_in_wires(
                    core.ports,
                    signal_name[:-2],
                    process_func=generate_direction_process_func("output"),
                )
            elif signal_name.endswith("_io"):
                signal = find_signal_in_wires(
                    core.ports,
                    signal_name[:-3],
                    process_func=generate_direction_process_func("inout"),
                )
            else:
                signal = find_signal_in_wires(core.wires + core.ports, signal_name)
            if signal is not None:
                signal.isvar = True
            else:
                fail_with_msg(f"output '{signal_name}' not found in wires/ports lists!")


def generate_direction_process_func(direction):
    """Generates a process function that returns a signal if it matches the direction"""

    def filter_signal(signal):
        signal = get_real_signal(signal)
        if signal.direction == direction:
            return signal
        # Return empty object if not correct signal direction
        return None

    return filter_signal


def create_snippet(core, *args, **kwargs):
    """Create a Verilog snippet to insert in given core."""
    # Ensure 'snippets' list exists
    core.set_default_attribute("snippets", [])
    snippet = iob_snippet(*args, **kwargs)
    snippet.set_needed_reg(core)
    core.snippets.append(snippet)
