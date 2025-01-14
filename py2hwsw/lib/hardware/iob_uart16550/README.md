## IOb-UART16550 ##

This is an adaptation of the UART16550 at https://opencores.org/projects/uart16550 to the IOb-SoC.

Note: This version has a FIFO with [256 bytes](https://github.com/IObundle/iob-uart16550/blob/master/hardware/src/uart_defines.vh#L231).

Note: This version was modified to use a dedicated hardware based control of RTS/CTS signals (software control of these signals is ignored). Therefore, the software should have hardware flow control disabled to avoid issues.

## How to build the core w/ python-setup
The python-setup workflow allows to automatically generate verilog components used by the projects core Verilog. It allows to create bus interfaces with ease and use existing Verilog modules. To use python-setup the project should have a *project*_setup.py file in the root directory. The main commands to use the python-setup workflow are:
- `make setup`: creates a build directory in the projects parent directory.
- `make clean`: removes the build directory.

An example of cleaning a previous build, creating a new build and simulating the project is:
- `make clean && make setup && make -C ../iob_uart16550_V0.10 sim-run`
