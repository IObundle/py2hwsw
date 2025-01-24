<!--
SPDX-FileCopyrightText: 2024 IObundle

SPDX-License-Identifier: MIT
-->

# py2hwsw

## A Python framework for embedded HW/SW projects

This project introduces a Python framework to (1) manage the
files of an embedded hardware/software (HW/SW) codesign project and (2) generate
the Verilog code of the hardware components. The flow uses only open-source tools.

An embedded HW/SW project requires that various source files be conveniently
organized in a directory tree so that the various EDA tools can run. Typically, 
makefiles and different scripting languages are employed to drive these tools,
which is often a barrier for new developers. The Python framework raises
developer accessibility by providing a single cockpit for the design
process.

Hardware Design Languages such as Verilog and VHDL give a lot of flexibility to
users. Still, the industry imposes strict linting rules that reverse this flexibility,
allowing only a small subset of these languages that ensure sound FPGAs and ASIC designs.
Writing HDL code in a  lint-friendly fashion is tedious and error-prone.

Py2HWSW solves this problem by generating lint-friendly and portable Verilog code that can 
be ported seamlessly between FPGA and ASIC flows.

### Installation

Py2HWSW runs on a Nix shell. First, download and install
[nix-shell](https://nixos.org/download.html#nix-install-linux).

Py2HWSW will self-install when nix-shell is run in a directory that contains the
[py2hwsw default.nix
file](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/default.nix). All
dependencies will also be installed.

Alternatively, it is possible but more complex to install Py2HWSW and its
dependencies manually. The explanation of the manual installation process is
beyond the scope of this README. To do that, check the list of dependencies in
the default.nix file and figure out how to install them on your system.


## Usage

The Py2HWSW framework's leading usage example is
[IOb-SoC](https://github.com/IObundle/iob-soc), a System-on-Chip (SoC) template
comprising an open-source RISC-V processor, a memory subsystem, and a UART.

Simpler examples, including the submodules used in IOb-SoC, are available in the
python/lib directory. Follow its README.md file for more information.


### User Guide

A preliminary version of the Py2HWSW user guide can be found
[here](py2hwsw/py2hwsw_document/document/ug.pdf).  This user guide is a work in
progress and will be updated as the project evolves. It uses LaTeX and can be
built with the following command:

```bash
make -C py2hwsw/lib doc-build
```


## Funding

This project is funded through [NGI Zero Core](https://nlnet.nl/core), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/Py2HWSW).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/core)

