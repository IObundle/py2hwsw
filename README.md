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

This project will benefit from a significant body of work constructed over the years, which is described in the following links.


### Useful Links

[IOb-SoC](https://github.com/IObundle/iob-soc) is a System-on-Chip (SoC) template comprising an open-source RISC-V processor, a memory subsystem, and a UART.
IOb-SoC is the departing repository; it already uses a collection of Python scripts to create a build directory for compiling and running various tools.


[IOb-Lib](https://github.com/IObundle/iob-lib.git) contains a set of Python scripts, Verilog, and C sources to simplify the development of subsystem IP cores.
It is used as a submodule in the IOb-SoC repository and associated projects.


[IOb-SoC-OpenCryptoHW](https://github.com/IObundle/iob-soc-opencryptohw.git) is a reconfigurable cryptographic hardware IP core for Next Generation Internet.
Security and privacy are more important than ever with the Internet of Things.


[IOb-Py2HW](https://github.com/IObundle/iob-py2hw.git) aims to develop a Python generator of portable Verilog code. Py2HW is not a High-Level Synthesis (HLS) language. It is instead a tool to help hardware designers produce readable, lint-clean, and portable Verilog code that can be used seamlessly in any FPGA or ASIC. 

### Install with pip

Use the following command to install the `py2hwsw` program with [pip](https://pip.pypa.io/en/stable/) globally:
`pip install git+https://github.com/IObundle/py2hwsw#egg=py2hwsw`

### Usage examples

Since this project started recently, usage examples are still being constructed and will be available soon.
