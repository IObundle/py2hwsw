# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# debug_ila.tcl - ILA debug probe setup
#
# Usage:
#   vivado -mode gui -source vivado/debug_ila.tcl -tclargs <same args as build_gui.tcl>
#
# The script:
#   - Creates a fresh project (replaces any stale/auto-created ones)
#   - Reads all sources and creates the Block Design
#   - Runs synthesis
#   - Inserts an ILA core connected to all (* mark_debug = "true" *) nets
#   - Runs implementation and bitstream generation
#   - Opens Hardware Manager and connects to target
#

set script_dir [file dirname [info script]]

# Remove stale project artifacts from disk that Vivado may auto-open
file delete -force "./New Project" "./New Project.xpr"

# ========== Parse args (same order as build_gui.tcl) ==========
if { $argc < 8 } {
    error "Usage: NAME FPGA_TOP CSR_IF BOARD VSRC INCLUDE_DIRS IS_FPGA USE_EXTMEM USE_ETHERNET"
}
set vars {NAME FPGA_TOP CSR_IF BOARD VSRC INCLUDE_DIRS IS_FPGA USE_EXTMEM USE_ETHERNET}
foreach var $vars arg $argv {
    set $var $arg
    puts "$var = $arg"
}

puts "Setting up project '$NAME' for board '$BOARD'..."

# ========== Force-create a fresh project ==========
# This properly closes any open project (including Vivado's auto-created "New Project")
create_project -force $BOARD ./${BOARD}

# ========== Read Verilog sources ==========
foreach file [split $VSRC \ ] {
    puts $file
    if {[file extension $file] == ".edif"} {
        read_edif $file
    } elseif {$file != "" && $file != " " && $file != "\n"} {
        read_verilog -sv $file
    }
}

# ========== Create Block Design (board.tcl uses set_property part in else branch) ==========
source [file join $script_dir $BOARD board.tcl]

# ========== Read constraints ==========
if { $IS_FPGA == "1" } {
    puts "Loading design for FPGA"
    if {[file exists [file join $script_dir $BOARD ${NAME}_dev.sdc]]} {
        read_xdc [file join $script_dir $BOARD ${NAME}_dev.sdc]
    }
    if {[file exists "../src/${NAME}.sdc"]} {
        read_xdc "../src/${NAME}.sdc"
    }
    if {[file exists "../../src/${NAME}_${CSR_IF}.sdc"]} {
        read_xdc "../src/${NAME}_${CSR_IF}.sdc"
    }
    if {[file exists [file join $script_dir ${NAME}_tool.sdc]]} {
        read_xdc [file join $script_dir ${NAME}_tool.sdc]
    }
}

set_property top $FPGA_TOP [current_fileset]
update_compile_order -fileset sources_1

# ========== Run Synthesis ==========
# Always reset and re-run synthesis so $readmemh picks up the hex file
set synth_run [get_runs synth_1]
if { $synth_run != "" } {
    reset_run synth_1
}

# Copy hex files into synth_1 where $readmemh resolves from (synthesis subprocess CWD)
set synth_dir [file normalize ./${BOARD}/${BOARD}.runs/synth_1]
file mkdir $synth_dir
foreach hexfile [glob -nocomplain *.hex] {
    puts "Copying $hexfile to $synth_dir"
    file copy -force [file join [file normalize .] $hexfile] [file join $synth_dir $hexfile]
}

puts "Running synthesis..."
launch_runs synth_1
wait_on_run synth_1
set progress [get_property PROGRESS [get_runs synth_1]]
if { $progress != "100%" } {
    error "Synthesis failed. Check reports/synth_1 for details."
}
puts "Synthesis completed successfully."

# ========== ILA Core Insertion ==========
open_run synth_1

# Find all (* mark_debug = "true" *) nets
set marked_nets [get_nets -hierarchical -filter {MARK_DEBUG == 1}]
set total_count [llength $marked_nets]
puts "Found $total_count marked net(s)"

if { $total_count == 0 } {
    error "No mark_debug nets found in design. Add (* mark_debug = \"true\" *) attributes to signals you want to probe."
}

# Delete any stale ILA core to force fresh configuration
if { [get_debug_cores -quiet u_ila_0] != "" } {
    delete_debug_core [get_debug_cores u_ila_0]
}
puts "Creating ILA debug core 'u_ila_0'..."

create_debug_core u_ila_0 ila
set_property C_DATA_DEPTH 1024 [get_debug_cores u_ila_0]
set_property C_TRIGIN_EN false [get_debug_cores u_ila_0]
set_property C_TRIGOUT_EN false [get_debug_cores u_ila_0]
set_property C_ADV_TRIGGER false [get_debug_cores u_ila_0]
set_property C_INPUT_PIPE_STAGES 0 [get_debug_cores u_ila_0]
set_property C_EN_STRG_QUAL false [get_debug_cores u_ila_0]
set_property ALL_PROBE_SAME_MU true [get_debug_cores u_ila_0]
set_property ALL_PROBE_SAME_MU_CNT 1 [get_debug_cores u_ila_0]

# Connect clock
set clk_net [get_nets -hierarchical -filter {NAME =~ *FCLK_CLK0}]
if { $clk_net == "" } {
    set clk_net [get_nets -hierarchical -filter {NAME =~ *clk}]
}
if { $clk_net != "" } {
    connect_debug_port u_ila_0/clk [lindex $clk_net 0]
    puts "  Clock: [lindex $clk_net 0]"
} else {
    error "Could not find a clock net for the ILA."
}

# Group bit-selects into bus probes; collect actual net names per group
array unset bus_nets
set single_nets {}
foreach net $marked_nets {
    if { [regexp {^(.+)\[(\d+)\]$} $net -> basename idx] } {
        lappend bus_nets($basename) $net
    } else {
        lappend single_nets $net
    }
}

set probe_list {}
# Process bus groups (connect all individual bit-selects, width = actual count)
foreach basename [array names bus_nets] {
    set nets [lsort -dictionary $bus_nets($basename)]
    lappend probe_list [list $nets [llength $nets]]
}
# Process standalone nets (no bit-select)
foreach net $single_nets {
    set width 1
    catch { set width [expr {abs([get_property LEFT $net] - [get_property RIGHT $net]) + 1}] }
    lappend probe_list [list [list $net] $width]
}

set num_marked [llength $probe_list]
puts "Consolidated into $num_marked probe(s)"

set i 0
foreach entry $probe_list {
    set nets [lindex $entry 0]
    set width [lindex $entry 1]

    set pname "probe${i}"
    if { [get_debug_ports -quiet u_ila_0/$pname] == "" } {
        create_debug_port u_ila_0 $pname
    }
    set_property port_width $width [get_debug_ports u_ila_0/$pname]
    set_property PROBE_TYPE DATA_AND_TRIGGER [get_debug_ports u_ila_0/$pname]
    connect_debug_port u_ila_0/$pname $nets
    puts "  $pname <- $width net(s)"
    incr i
}

# ========== Save ==========
save_project_as [current_project] -force

puts ""
puts "=== ILA Debug Setup Complete ==="
puts "ILA 'u_ila_0' with $num_marked probe(s)."
puts ""

# ========== Run Implementation ==========
puts "Running implementation and bitstream generation..."
set impl_run [get_runs impl_1]
if { $impl_run != "" } {
    reset_run impl_1
}
launch_runs impl_1 -to_step write_bitstream
wait_on_run impl_1
set progress [get_property PROGRESS [get_runs impl_1]]
if { $progress != "100%" } {
    error "Implementation failed. Check reports/impl_1 for details."
}
puts "Implementation completed successfully."

# ========== Open Hardware Manager ==========
puts ""
puts "Opening Hardware Manager..."
open_hw_manager
connect_hw_server
puts "Hardware server connected. Opening target..."
if { [catch {open_hw_target} result] } {
    puts "Warning: Could not open hardware target: $result"
    puts "Please connect to the target manually in the Hardware Manager."
}
puts ""
puts "=== Ready for Debug ==="
puts "To program the device:"
puts "  1. Select the device in the Hardware Manager"
puts "  2. Right-click → Program Device → select ${BOARD}.bit"
puts "  3. Add ILA probes to the waveform window and trigger"
