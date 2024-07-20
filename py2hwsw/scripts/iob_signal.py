from dataclasses import dataclass

from iob_base import fail_with_msg


@dataclass
class iob_signal:
    """Class that represents a wire/port signal"""

    name: str = ""
    width: str or int = 1
    descr: str = "Default description"

    # Only used when signal belongs to a port
    direction: str = ""

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Signal name is not set", ValueError)

        if self.direction not in ["", "input", "output", "inout"]:
            fail_with_msg(f"Invalid signal direction: '{self.direction}'", ValueError)

    def get_verilog_wire(self):
        """Generate a verilog wire string from this signal"""
        return f"wire [{self.width}-1:0] {self.name};\n"

    def assert_direction(self):
        if not self.direction:
            fail_with_msg(f"Signal '{self.name}' has no direction", ValueError)

    def get_verilog_port(self, comma=True):
        """Generate a verilog port string from this signal"""
        self.assert_direction()
        comma_char = "," if comma else ""
        return f"{self.direction} [{self.width}-1:0] {self.get_verilog_port_name()}{comma_char}\n"

    def get_verilog_port_name(self):
        """Return the verilog port name, including direction suffix"""
        self.assert_direction()
        if self.direction == "input":
            return f"{self.name}_i"
        elif self.direction == "output":
            return f"{self.name}_o"
        else:
            return f"{self.name}_io"


@dataclass
class iob_signal_reference:
    """Class that references another signal
    Use to distinguish from a real signal (for generator scripts)
    """

    signal: iob_signal | None = None


def get_real_signal(signal):
    """Given a signal reference, follow the reference (recursively) and
    return the real signal
    """
    while isinstance(signal, iob_signal_reference):
        signal = signal.signal
    return signal
