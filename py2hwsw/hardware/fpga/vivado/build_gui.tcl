# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# Parse positional args (same order as build.tcl)
set vars {NAME FPGA_TOP CSR_IF BOARD VSRC INCLUDE_DIRS IS_FPGA USE_EXTMEM USE_ETHERNET}
foreach var $vars arg $argv {
    set $var $arg
    puts "$var = $arg"
}

# Read verilog sources
foreach file [split $VSRC \ ] {
    puts $file
    if { [ file extension $file ] == ".edif" } {
        read_edif $file
    } elseif {$file != "" && $file != " " && $file != "\n"} {
        read_verilog -sv $file
    }
}

# Include directories
set SYNTH_FLAGS {}
foreach dir $INCLUDE_DIRS {
    lappend SYNTH_FLAGS "-include_dirs" "${dir}"
}

# Read board properties (creates project and Block Design with PS7)
source vivado/$BOARD/board.tcl

# Pre-map custom assignments
if {[file exists "vivado/premap.tcl"]} {
    source "vivado/premap.tcl"
}

# Read design constraints (but do NOT run synthesis)
if { $IS_FPGA == "1" } {
    puts "Loading design for FPGA"
    if {[file exists "vivado/$BOARD/$NAME\_dev.sdc"]} {
        read_xdc vivado/$BOARD/$NAME\_dev.sdc
    }
    if {[file exists "../src/$NAME.sdc"]} {
        read_xdc ../src/$NAME.sdc
    }
    if {[file exists "../../src/$NAME\_$CSR_IF.sdc"]} {
        read_xdc ../src/$NAME\_$CSR_IF.sdc
    }
    if {[file exists "vivado/$NAME\_tool.sdc"]} {
        read_xdc vivado/$NAME\_tool.sdc
    }
} else {
    puts "Loading design for out-of-context"
    read_xdc -mode out_of_context vivado/$BOARD/$NAME\_dev.sdc
    read_xdc -mode out_of_context ../src/$NAME.sdc
    if {[file exists "../src/$NAME\_$CSR_IF.sdc"]} {
        read_xdc ../src/$NAME\_$CSR_IF.sdc
    }
    if {[file exists "./src/$NAME.sdc"]} {
        read_xdc ./src/$NAME.sdc
    }
    if {[file exists "vivado/$NAME\_tool.sdc"]} {
        read_xdc -mode out_of_context vivado/$NAME\_tool.sdc
    }
}

# Set top-level module
set_property top $FPGA_TOP [current_fileset]

# Open the Block Design diagram in the GUI
if {[get_files system.bd] != ""} {
    open_bd_design [get_files system.bd]
    regenerate_bd_layout
}

# Save project so GUI Flow Navigator recognizes project state
save_project_as [current_project] -force

puts ""
puts "Design loaded in GUI. No synthesis has been run."
puts "From here you can:"
puts "  - Inspect / edit the Block Design in the IP Integrator"
puts "  - Run Synthesis: Flow -> Run Synthesis"
puts "  - Add debug probes (ILA): Tools -> Set Up Debug (after synthesis)"
puts "  - Run Implementation: Flow -> Run Implementation"
puts "  - Generate Bitstream: Flow -> Generate Bitstream"
puts "  - Program device: Open Hardware Manager -> Program device"
puts "Type 'exit' in the Tcl Console or close Vivado when done."
puts ""
