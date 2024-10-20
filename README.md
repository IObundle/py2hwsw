<!--
SPDX-FileCopyrightText: 2024 IObundle

SPDX-License-Identifier: MIT
-->

# py2hwsw

## A Python framework for embedded HW/SW projects

In this project, we propose to develop a Python framework to (1) manage the
files of an embedded hardware/software (HW/SW) codesign project and (2) generate
the Verilog code of the hardware components. The framework will be tested on the
OpenCrypto system created in previously NGI-supported projects. The flow will
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
hardware design process. So, we'd like to propose a tool to generate portable Verilog
code using a Python API.

Py2HWSW aims to develop a Python generator of portable Verilog code. Py2HW is not a High-Level Synthesis (HLS) language. It is instead a tool to help hardware designers produce readable, lint-clean, and portable Verilog code that can be used seamlessly in any FPGA or ASIC. 

This project will benefit from a significant body of work constructed over the years, which is described in the following links.


### Useful Links

[IOb-SoC](https://github.com/IObundle/iob-soc) is a System-on-Chip (SoC) template comprising an open-source RISC-V processor, a memory subsystem, and a UART.
IOb-SoC is the departing repository; it already uses a collection of Python scripts to create a build directory for compiling and running various tools.


[IOb-SoC-OpenCryptoHW](https://github.com/IObundle/iob-soc-opencryptohw.git) is a reconfigurable cryptographic hardware IP core for Next Generation Internet.
Security and privacy are more important than ever with the Internet of Things.

### Install with pip

Optionally, create a python virtual environment before installing the `py2hwsw` package:
```bash
python -m venv py2hwsw_env
source py2hwsw_env/bin/activate
```

Use the following command to install the `py2hwsw` program with [pip](https://pip.pypa.io/en/stable/):
```bash
pip install git+https://github.com/IObundle/py2hwsw#egg=py2hwsw
```

As an alternative, to install the `py2hwsw` package from the locally cloned repository:
```bash
pip install -e path/to/py2hwsw_directory
```

### Install with nix

Use the following commands to install the `py2hwsw` program with [Nix](https://nixos.org/):
```bash
export PY2HWSW_PATH=path/to/py2hwsw_directory
nix-shell path/to/py2hwsw_directory
```

If the `Py2HWSW_PATH` environment variable is not set, the nix environment will only install the project dependencies. Not the `py2hwsw` package itself.

### Run from a local repository (without install)

To use the `py2hwsw` program from a local repository without having to rebuild the package (as with nix and pip), run the `py2hwsw.py` script directly:

Ensure the `~/.local/bin/` is in the `PATH` environment variable.
Otherwise, set it by adding the following to your `.bashrc` file:
```
# set PATH so it includes user's private ~/.local/bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

Then create a symlink to the `py2hwsw.py` script in the `~/.local/bin` directory:
```
ln -s path/to/py2hwsw_directory/py2hwsw/scripts/py2hwsw.py ~/.local/bin/py2hwsw
```

### Usage examples

Since this project started recently, usage examples are still being constructed and will be available soon.

## Funding

This project is funded through [NGI Zero Core](https://nlnet.nl/core), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/Py2HWSW).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/core)

