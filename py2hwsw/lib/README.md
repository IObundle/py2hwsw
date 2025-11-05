<!--
SPDX-FileCopyrightText: 2025 IObundle

SPDX-License-Identifier: MIT
-->

# Py2HWSW Library

This folder contains the iob_system module, which is a RISC-V-based System on
Chip, a few peripherals and many hardware and software modules that can be used
to create a complete system.

The hardware modules are writen in Python, Verilog or a combination of both and
reside in the hardware directory. The Py2HWSW framework can genrate
human-readable Verilog code from the Python code, coordinate the integration of
pre-existing Verilog modules an snippets in the system and generate the software
drivers for the hardware modules. 

The software modules are written in C/C++ and can be compiled using the RISC-V
GCC. The ones provided in the software directory are utilities that can be used
in the system.


## Running Py2HWSW on the Examples in this Folder

The modules in this folder can be run on the Py2HWSW framework. To do so, follow
the installation instructions in the README.md file in the root directory of
this repository. Then, clone this repository and navigate to the `lib`with the
following commands:

```bash
git clone git@github.com:IObundle/py2hwsw.git --init --recursive

cd py2hwsw/lib
```

In this directory, there is a Makefile that has targets for different purposes,
and explained in the following sections.

## Build and simulate a hardware module

A hardware module is ready for simulation building if it has the `iob_sim` superblock.
To build a hardware module for simulation, run the following command:

```bash
make sim-build CORE=module_name SIMULATOR=[icarus|verilator|vcs|questa|xcelium]
```

Py2HWSW will find the module in the hardware directory and build it for
simulation of the specified simulator. The variable CORE defines the name of the
module to be built (`module_name` is the name of the module file without the .py
extension) and the variable SIMULATOR defines the simulator to be used.
The supported simulators are icarus, verilator, vcs, questa and
xcelium. The default simulator is icarus.

To build and run a hardware module for simulation, the module must have a
testbench. The testbench must be named module_name_tb.[v|cpp] and must be in the
module's `hardware/simulation/src` directory. To build and run a hardware module
for simulation, run the following command:

```bash
make sim-run CORE=module_name SIMULATOR=[icarus|verilator|vcs|questa|xcelium]
```

To run a set of simulation tests, run the following command:

```bash
make [all|sim-test] SIMULATOR=[icarus|verilator|vcs|questa|xcelium]
```

This target is also the default target of the Makefile so it can be omitted. To
clean the simulation files, run the following command:

```bash
make sim-clean
```

## Build and run a hardware module on an FPGA board

A hardware module is ready for FPGA building if it lists at least one FPGA board
in the `board_list` attribute and has the `iob_<boad_name>` superblock.
To build a hardware
module for an FPGA board, run the following command:

```bash
make fpga-build CORE=module_name BOARD=board_name
```

The variable BOARD defines the name of the FPGA board, among those listed in the
module's `board_list` attribute, to be used. The supported boards are listed in
the `py2hwsw/hardware/fpga/vivado` and `py2hwsw/hardware/fpga/quartus` directories.


To run a hardware module on an FPGA board, the module must have, its parent
attribute must either be the `iob_system` module or a module that has the
`iob_system` module as an ancestor. The board must be connected to the
computer. To run a hardware module on an FPGA board, run the following command:

```bash
make fpga-run CORE=module_name BOARD=board_name
```

If multiple users in the same computer need to use the same FPGA board, a script
to manage the board access is provided. This script is installed as a Linux
service by running the following command:

```bash
make board_server_install
```

To check the status of the board server, run the following command:

```bash
make board_server_status
```

Finally, to uninstall the board server, run the following command:

```bash
make board_server_uninstall
```

If the board server is not installed, the FPGA board can be accessed by any user
but collisions may occur, and one user may reprogram the board while another is
using it.

## Export Cores for FuseSoC

After generating the build directory for a core, users may call the Py2HWSW `export_fusesoc` target to export the core for [FuseSoC](https://github.com/olofk/fusesoc).

Use the following command to print all cores available in the Py2HWSW library:
```bash
nix-shell --run "py2hwsw --print_lib_cores"
```

Use the following to export a core for FuseSoC:
```bash
make fusesoc-export CORE=module_name
```

The `fusesoc-export` target will create the `fusesoc_exports/` directory containing the exported FuseSoC cores.
This directory can be imported as a library in a FuseSoC project.

Use the following to export a core for FuseSoC and run it in simulation:
```bash
make fusesoc-test CORE=module_name
```

The `fusesoc-test` target will create the `fusesoc_test/` project directory and import the `fusesoc_exports/` library into it.
It will then run the core in simulation using FuseSoC.

From the generated `fusesoc_test/` project directory, use FuseSoC commands to print info or perform operations on the exported core.
```bash
nix-shell
cd fusesoc_test
fusesoc list-cores  # List exported Py2HWSW cores
fusesoc core-info iobundle:py2hwsw:module_name:version  # Get details about a core
```

## Build the Py2HWSW User Guide

To build the Py2HWSW User Guide, run the following command:

```bash
make py2-doc-buid
```

## Code Style
#### Python Code
[![Recommended python code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
- Python format workflow:
    - install [black](https://black.readthedocs.io/en/stable/)
    - run black manually:
        - `make python-format` or `./scripts/sw_format.py black`
    - (optional): [integrate with your preferred
      IDE](https://black.readthedocs.io/en/stable/integrations/editors.html)
    - black formatting for other repositories:
        - call `sw_format.py black` script in LIB submodule from the repository
          top level:
        ```make
        # repository top level Makefile
        format:
           @./lib/scripts/sw_format.py black
        ```
#### C/C++ Code
- Recommended C/C++ code style: [LLVM](https://llvm.org/docs/CodingStandards.html)
- C/C++ format workflow:
    - install [clang-format](https://black.readthedocs.io/en/stable/)
    - run clang-format manually:
        - `make c-format` or `./scripts/sw_format.py clang`
    - (optional) [integrate with your preferred
      IDE](https://clang.llvm.org/docs/ClangFormat.html#vim-integration)
    - C/C++ formatting for other repositories:
        - copy `.clang-format` to new repository top level
        - call `sw_format.py clang` script in LIB submodule from the repository
          top level:
        ```make
        # repository top level Makefile
        format:
           @./lib/scripts/sw_format.py clang
        ```
