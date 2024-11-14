<!--
SPDX-FileCopyrightText: 2024 IObundle

SPDX-License-Identifier: MIT
-->

# py2hwsw

## A Python framework for embedded HW/SW projects

In this project, we propose to develop a Python framework to (1) manage the
files of an embedded hardware/software (HW/SW) codesign project and (2) generate
the Verilog code of the hardware components. The flow will
use only open-source tools.

An embedded HW/SW project requires that various source files be conveniently
organized in a directory tree so that the build scripts can produce the needed
artifacts. Typically, Makefiles and different scripting languages are employed,
which is often a barrier for new developers. The proposed Python framework will
raise developer accessibility by providing a single cockpit for the design
process.

Hardware Design Languages such as Verilog and VHDL give a lot of flexibility to
users. Still, the design tools reject most of their features and force users to
use a small, low-level subset if we want the code to be human-readable and
portable to both FPGAs and ASICs. The result is a very tedious and error-prone
hardware design process.

Py2HWSW aims to develop a Python generator of portable Verilog code. Py2HW is
not a High-Level Synthesis (HLS) language. It is instead a tool to help hardware
designers produce readable, lint-clean, and portable Verilog code that can be
used seamlessly in any FPGA or ASIC.

### Installation

Py2HWSW runs on [nix-shell](https://nixos.org/download.html#nix-install-linux)
and self installs when an example is run. Alternatively you may manuall install
the program and all its dependendencies listed in the [py2hwsw default.nix
file](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/default.nix).


## Usage example

The Py2HWSW framework main usage example is
[IOb-SoC](https://github.com/IObundle/iob-soc), a System-on-Chip (SoC) template
comprising an open-source RISC-V processor, a memory subsystem, and a UART.

### Build user guide

Py2HWSW can generate a user guide with LaTeX using the `--py2hwsw_docs` argument.

To generate a documentation directory with the user guide sources and build it, run:
```bash
py2hwsw --py2hwsw_docs
make -C py2hwsw_docs/document/ build
```

## Funding

This project is funded through [NGI Zero Core](https://nlnet.nl/core), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/Py2HWSW).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/core)

