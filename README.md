<!--
SPDX-FileCopyrightText: 2024 IObundle

SPDX-License-Identifier: MIT
-->

# py2hwsw

## A Python framework for embedded HW/SW projects

This project introduces a Python framework to (1) manage the
files of an embedded hardware/software (HW/SW) codesign project and (2) generate
the Verilog code of the hardware components. The flow will
use only open-source tools.

An embedded HW/SW project requires that various source files be conveniently
organized in a directory tree so that the various EDA tools can run. Typically, 
makefiles and different scripting languages are employed to drive these tools,
which is often a barrier for new developers. The proposed Python framework will
raise developer accessibility by providing a single cockpit for the design
process.

Hardware Design Languages such as Verilog and VHDL give a lot of flexibility to
users. Still, the industry imposes strict linting rules that reverse this flexibility,
allowing only a small subset of these languages that ensure sound FPGAs and ASIC designs.
Writing HDL code in a  lint-friendly fashion is tedious and error-prone.

Py2HWSW solves this problem by generating lint-friendly and portable Verilog code that can 
be ported seamlessly between FPGA and ASIC flows.

### Installation

Py2HWSW runs on [nix-shell](https://nixos.org/download.html#nix-install-linux)
and self-installs when an example is run. Alternatively, manually install
the program and all its dependencies listed in the [py2hwsw default.nix
file](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/default.nix).


## Usage example

The Py2HWSW framework's leading usage example is
[IOb-SoC](https://github.com/IObundle/iob-soc), a System-on-Chip (SoC) template
comprising an open-source RISC-V processor, a memory subsystem, and a UART.

### Build user guide

Py2HWSW can generate a user guide with LaTeX using the `--py2hwsw_docs` argument.

To generate a documentation directory with the user guide sources and build it, run:
```bash
py2hwsw --py2hwsw_docs
make -C py2hwsw_docs/document/ build
```

A prebuilt user guide can be found [here](py2hwsw/py2hwsw_document/document/ug.pdf).

## Funding

This project is funded through [NGI Zero Core](https://nlnet.nl/core), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/Py2HWSW).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/core)

