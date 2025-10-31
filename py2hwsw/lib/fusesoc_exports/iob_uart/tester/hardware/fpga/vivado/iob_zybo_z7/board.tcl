# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

set PART xc7z010clg400-1
set_property part $PART [current_project]

if { ![file isdirectory "./ip"]} {
    file mkdir ./ip
}

file mkdir ./ip
set ip_dir ./ip

create_project -force ip_packaging_project $ip_dir -part xc7z010clg400-1
set_property target_language Verilog [current_project]

# Add sources (Verilog RTL)
# all my files are in the list VSRC already sert as this scripts is sourced from build.tcl, add them here
foreach file $VSRC {
    add_files -fileset sources_1 $file
    #check if file $NAME.v exists
    if {[file exists $file]} {
        puts "Added source file: $file"
    } else {
        puts "Warning: Source file $file does not exist!"
    }
}


set_property ip_repo_paths ./ip [current_project]
# Update IP catalog to include the new IP
update_ip_catalog -rebuild

ipx::package_project -root_dir ./ip/$NAME -import_files -force

set core [ipx::current_core]
# Set required metadata
set_property vendor iobundle.com $core
set_property library user $core
set_property name $NAME $core
set_property version 1.0 $core

set_property taxonomy {{/UserIP}} $core
set_property supported_families {zynq Production} $core

set_property display_name "IOB System" $core
set_property description "IObundle system wrapper" $core

ipx::save_core
ipx::check_integrity $core
#ipx::unload_core iobundle.com:user:$NAME:1.0
close_project -delete
puts "IP $NAME packaged at ./ip/$NAME"



# =========== Now create new top-level project and instantiate the IP ===========
# Delete any existing project files
file delete -force .Xil


# Re-open a new project and re-add the IP repo path
create_project -force top_project ./top_project -part $PART
set_property target_language Verilog [current_project]

# Add the parent directory of the IP to the repo path (not the IP directory itself!). use the current dirctory as the repo path. It is a directory called ip in the current directory
set_property ip_repo_paths "./ip" [current_project]
update_ip_catalog -rebuild 

puts "Found IPs:"
foreach ip [get_ipdefs *] {
    puts $ip
}
puts "Repo paths: [get_property ip_repo_paths [current_project]]"

# Create block design
create_bd_design "design_1"

# Create PS7 IP
create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0

# Set PS7 properties (enable FCLK0, reset0, disable M_AXI_GP0)
set_property -dict [list \
    CONFIG.PCW_EN_CLK0_PORT {1} \
    CONFIG.PCW_EN_RST0_PORT {1} \
    CONFIG.PCW_USE_M_AXI_GP0 {0} \
    CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {50.0}\
] [get_bd_cells processing_system7_0]


create_bd_cell -type ip -vlnv iobundle.com:user:$NAME:1.0 $NAME\_0

#instantiate a constant 1 cell
create_bd_cell -type ip -vlnv xilinx.com:ip:xlconstant:1.1 constant_1

# Connect PS7 clocks and resets to your design ports as needed
connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins $NAME\_0/clk_i]
connect_bd_net [get_bd_pins processing_system7_0/FCLK_RESET0_N] [get_bd_pins $NAME\_0/arst_i]

#connect cke_i and cts to constant 1
connect_bd_net [get_bd_pins $NAME\_0/cke_i] [get_bd_pins constant_1/dout]
connect_bd_net [get_bd_pins $NAME\_0/rs232_cts_i] [get_bd_pins constant_1/dout]

#make uart_tx and uart_rx pins external
make_bd_pins_external [get_bd_pins $NAME\_0/rs232_txd_o]
make_bd_pins_external [get_bd_pins $NAME\_0/rs232_rxd_i]
#make_bd_pins_external [get_bd_pins $NAME\_0/led0]
#make_bd_pins_external [get_bd_pins $NAME\_0/led3]

puts "Synthesizing for FPGA"
if {[file exists "vivado/$BOARD/$NAME\_dev.sdc"]} {
    add_files -fileset constrs_1 vivado/$BOARD/$NAME\_dev.sdc
}
if {[file exists "../src/$NAME.sdc"]} {
    add_files -fileset constrs_1 ../src/$NAME.sdc
}
if {[file exists "../../src/$NAME\_$CSR_IF.sdc"]} {
    add_files -fileset constrs_1 ../src/$NAME\_$CSR_IF.sdc
}
if {[file exists "vivado/$NAME\_tool.sdc"]} {
    add_files -fileset constrs_1 vivado/$NAME\_tool.sdc
}


# Connect AXI interface if needed (not used here since M_AXI_GP0 disabled)
# You can also connect UART pins externally

# Validate design
validate_bd_design

# Generate output products
generate_target all [get_bd_designs design_1.bd]

# Save the design
save_bd_design

# Launch synthesis, implementation, and bitstream generation (adjust as needed)
set_property include_dirs "../src ../common_src ./src ./vivado/$BOARD" [get_filesets sources_1]

#print all elements in SYNTH_FLAGS
puts "SYNTH_FLAGS: $SYNTH_FLAGS"

#remove all '-include_dirs' from SYNTH_FLAGS
#set SYNTH_FLAGS [regsub -all { -include_dirs .*} $SYNTH_FLAGS ""]
#puts "SYNTH_FLAGS after cleanup: $SYNTH_FLAGS"


# Create HDL wrapper for the block design
make_wrapper -files [get_files design_1.bd] -top

# Add the wrapper to your project
add_files -norecurse ./top_project/top_project.gen/sources_1/bd/design_1/hdl/design_1_wrapper.v

# Set the top module for synthesis
set_property top design_1_wrapper [current_fileset]

launch_runs synth_1 -verbose
wait_on_run synth_1

launch_runs impl_1 -to_step write_bitstream -verbose
wait_on_run impl_1

# Export hardware including bitstream
write_hw_platform -fixed -include_bit -force ./$NAME.xsa

#rename the bitstream to match the project name
#set bitstream_file [get_files -of_objects [get_runs impl_1] -filter {FILE_TYPE == "Bit"}]
#set_property FILE_NAME "$NAME.bit" $bitstream_file




exit 0
