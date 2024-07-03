from dataclasses import dataclass, field
from iob_snippet import iob_snippet

@dataclass
class iob_comb(iob_snippet):
    """Class to represent a Verilog combinatory circuit in an iob module"""

    def __post_init__(self):
        """Wrap verilog code with the always block"""
        self.verilog_code = f'''\talways @ (*)\n\t\tbegin\n''' + '''\t\t\t''' +  self.verilog_code + '''\t\tend\n'''

def create_comb(core, *args, **kwargs):
    """Create a Verilog combinatory circuit to insert in a given core."""
    # Ensure 'combs' list exists
    core.set_default_attribute("combs", [])
    comb = iob_comb(*args, **kwargs)
    core.combs.append(comb)
    # TODO: find signals in outputs list and change to reg
                                                
if __name__ == '__main__':
    circ = iob_comb(outputs=['a'],verilog_code='a = b & c\n')
    print(circ.verilog_code)
