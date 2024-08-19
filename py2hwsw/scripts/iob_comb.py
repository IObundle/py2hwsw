from dataclasses import dataclass, field
from iob_snippet import iob_snippet


@dataclass
class iob_comb(iob_snippet):
    """Class to represent a Verilog combinatory circuit in an iob module"""

    def __post_init__(self):
        """Wrap verilog code with the always block"""
        self.verilog_code = (
            f"""\talways @ (*)\n\t\tbegin\n"""
            + """\t\t\t"""
            + self.verilog_code
            + """\n\t\tend"""
        )


def create_comb(core, *args, **kwargs):
    """Create a Verilog combinatory circuit to insert in a given core."""
    if core.fsms != None:
        raise ValueError("Comb circuits and FSMs are mutually exclusive. Use separate submodules.")
    core.set_default_attribute("combs", None)
    verilog_code = kwargs.get("verilog_code", None)
    comb = iob_comb(verilog_code=verilog_code)
    comb.set_needed_reg(core)
    comb.infer_registers(core)
    core.combs = comb


if __name__ == "__main__":
    circ = iob_comb(verilog_code="a = b & c;")
    print(circ.verilog_code)
