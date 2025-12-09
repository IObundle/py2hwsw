# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

set INCLUDE $env(INCLUDE)
set TOP $env(TOP)

set YOSYS_FLAGS {}
foreach dir $INCLUDE {
    lappend YOSYS_FLAGS "-I${dir}"
}

# Read the Verilog files
yosys read_verilog -DSYNTHESIS -I./src -I../src -I../common_src $YOSYS_FLAGS ../src/*.v

set top $TOP

yosys hierarchy -check -top $top

yosys show -notitle -format dot -prefix $top\_00

# the high-level stuff
yosys proc; yosys opt
yosys memory; yosys opt
yosys fsm; yosys opt

yosys show -notitle -format dot -prefix $top\_01

# mapping to internal cell library
yosys techmap; yosys opt

yosys splitnets -ports;; yosys show -notitle -format dot -prefix $top\_02

# mapping flip-flops to iob_cells.lib
yosys dfflibmap -liberty ./iob/iob_cells.lib 

# mapping logic to iob_cells.lib
yosys abc -liberty  ./iob/iob_cells.lib "strash; dch; map"


# cleanup
yosys clean

yosys show -notitle -lib ./iob/iob_cells.v -format dot -prefix $top\_03

# write synthesized design
yosys write_verilog results/$top\_synth.v

