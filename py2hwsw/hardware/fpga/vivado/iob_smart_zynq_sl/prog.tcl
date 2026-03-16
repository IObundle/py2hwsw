# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Zynq Programming Script for XSCT
set FPGA_TOP [lindex $argv 0]
set DEVICE_ID [lindex $argv 1]
set BOARD [lindex $argv 2]

connect

# 1. Reset System first to clean PS state
targets -set -nocase -filter {name =~ "ARM Cortex-A9 MPCore #0"}
puts "--- Resetting System ---"
rst -system
after 1000

# 2. Program the PL
targets -set -nocase -filter {name =~ "xc7z020"}
puts "--- Programming PL ---"
fpga "$FPGA_TOP.bit"

# 3. Initialize PS
targets -set -nocase -filter {name =~ "ARM Cortex-A9 MPCore #0"}
puts "--- Initializing PS ---"
# Find ps7_init.tcl. In Py2HWSW it should be in the generated ip directory.
set PS7_INIT_FILE [glob -nocomplain -directory ./ip/system/ip/ *ps7_init.tcl]
if {[llength $PS7_INIT_FILE] == 0} {
    # Fallback to alternative location
    set PS7_INIT_FILE [glob -nocomplain -directory . -recursive ps7_init.tcl]
}

if {[llength $PS7_INIT_FILE] > 0} {
    set PS7_INIT_FILE [lindex $PS7_INIT_FILE 0]
    puts "--- Sourcing $PS7_INIT_FILE ---"
    source $PS7_INIT_FILE
    ps7_init
    ps7_post_config
} else {
    puts "WARNING: ps7_init.tcl not found!"
}

# 4. Unblock AFI / Enable Level Shifters (Standard Zynq registers)
puts "--- Enabling Level Shifters ---"
mwr 0xF8000008 0xDF0D
mwr 0xF8000900 0xF

# 5. Load and Run PS Application (if ELF exists)
# In Py2HWSW, software is usually built in software/ folder.
set elf_path "../../software/ps_app.elf"
if {[file exists $elf_path]} {
    puts "--- Loading PS Application: $elf_path ---"
    dow $elf_path
    puts "--- Running PS Application ---"
    con
} else {
    puts "INFO: No PS application found at $elf_path"
}

puts "--- Deployment Complete ---"
exit
