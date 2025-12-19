# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#extract cli positional args
set vars {NAME FPGA_TOP CSR_IF BOARD VSRC INCLUDE_DIRS IS_FPGA USE_EXTMEM USE_ETHERNET SEED USE_QUARTUS_PRO}
foreach var $vars arg $argv {
    set $var $arg
    puts "$var = $arg"
}


load_package flow

project_new $FPGA_TOP -overwrite

if {[project_exists $FPGA_TOP]} {
    project_open $FPGA_TOP -force
} else {
    project_new $FPGA_TOP
}

set_global_assignment -name NUM_PARALLEL_PROCESSORS ALL

set_global_assignment -name TOP_LEVEL_ENTITY $FPGA_TOP

#board data
source quartus/$BOARD/board.tcl

set_global_assignment -name FAMILY $FAMILY
set_global_assignment -name DEVICE $PART
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY reports
set_global_assignment -name VERILOG_INPUT_VERSION SYSTEMVERILOG_2005

#verilog heders search path
set_global_assignment -name SEARCH_PATH ../src
set_global_assignment -name SEARCH_PATH ../common_src
set_global_assignment -name SEARCH_PATH ./src
set_global_assignment -name SEARCH_PATH quartus/$BOARD

foreach dir $INCLUDE_DIRS {
    set_global_assignment -name SEARCH_PATH $dir
}

#verilog sources, quartus IPs, use extension
foreach file [split $VSRC \ ] {
    if { [ file extension $file ] == ".qsys" } {
        set_global_assignment -name QSYS_FILE $file
    } elseif {$file != ""} {
        set_global_assignment -name VERILOG_FILE $file
    }
}

if {$IS_FPGA != "1"} {
    set_global_assignment -name INCREMENTAL_COMPILATION_EXPORT_NETLIST_TYPE POST_FIT
    set_global_assignment -name INCREMENTAL_COMPILATION_EXPORT_ROUTING OFF
}


#read synthesis design constraints
set_global_assignment -name SDC_FILE ./quartus/$BOARD/$NAME\_dev.sdc
set_global_assignment -name SDC_FILE ../src/$NAME.sdc
set_global_assignment -name SDC_FILE ../src/$NAME\_$CSR_IF.sdc
set_global_assignment -name SDC_FILE ./src/$NAME.sdc
if {[file exists "quartus/$BOARD/auto_board.sdc"]} {
    set_global_assignment -name SDC_FILE ./quartus/$BOARD/auto_board.sdc
}

set_global_assignment -name SYNCHRONIZER_IDENTIFICATION "Forced if Asynchronous"


# random seed for fitting
set_global_assignment -name SEED $SEED

export_assignments

if {$USE_QUARTUS_PRO == 1} {
    set synth_tool "syn"
} else {
    set synth_tool "map"
}

#read pre-synthesis script
if {[file exists "quartus/quartus\_premap.tcl"]} {
    source quartus/quartus\_premap.tcl
}

#Incremental compilation
#run quartus pro synthesis
if {[catch {execute_module -tool $synth_tool} result]} {
    puts "\nResult: $result\n"
    puts "ERROR: Synthesis failed. See report files.\n"
    qexit -error
} else {
    puts "\nINFO: Synthesis was successful.\n"
}

if {$IS_FPGA != "1"} {
    #assign virtual pins
    set name_ids [get_names -filter * -node_type pin]
    foreach_in_collection name_id $name_ids {
        set pin_name [get_name_info -info full_path $name_id]
        post_message "Making VIRTUAL_PIN assignment to $pin_name"
        set_instance_assignment -to $pin_name -name VIRTUAL_PIN ON
    }
    
    export_assignments
    
    #rerun quartus pro synthesis to apply virtual pin assignments
    if {[catch {execute_module -tool $synth_tool} result]} {
        puts "\nResult: $result\n"
        puts "ERROR: Synthesis failed. See report files.\n"
        qexit -error
    } else {
        puts "\nINFO: Synthesis was successful.\n"
    }
}

#read post-synthesis script
if {[file exists "quartus/postmap.tcl"]} {
    source quartus/postmap.tcl
}

#read implementation design constraints
if {[file exists "quartus/$NAME\_tool.sdc"] == 0} {
    puts [open "quartus/$NAME\_tool.sdc" w] "derive_clock_uncertainty"
}
set_global_assignment -name SDC_FILE ./quartus/$NAME\_tool.sdc

#run quartus fit
if {[catch {execute_module -tool fit} result]} {
    puts "\nResult: $result\n"
    puts "ERROR: Fit failed. See report files.\n"
    qexit -error
} else {
    puts "\nINFO: Fit was successful.\n"
}

#run quartus sta
if {[catch {execute_module -tool sta} result]} {
    puts "\nResult: $result\n"
    puts "ERROR: STA failed. See report files.\n"
    qexit -error
} else {
    puts "\nINFO: STA was successful.\n"
}

#rerun quartus sta to generate reports
if [catch {qexec "[file join $::quartus(binpath) quartus_sta] -t quartus/timing.tcl $FPGA_TOP"} result] {
    puts "\nResult: $result\n"
    puts "ERROR: STA failed. See report files.\n"
    qexit -error
} else {
    puts "\nINFO: STA was successful.\n"
}
    
if {$IS_FPGA != "1"} {

    #write netlist
    if {$USE_QUARTUS_PRO == 1} {
        if {[catch {execute_module -tool eda -args "--resynthesis --format verilog"} result]} {
            qexit -error
        }
    } else {
        if {[catch {execute_module -tool cdb -args "--vqm=resynthesis/$FPGA_TOP"} result]} {
            qexit -error
        }
    }
    
    #rename netlist
    set netlist_file "$FPGA_TOP\_netlist.v"
    if {[file exists $netlist_file] == 1} {
        file delete $netlist_file
    }
    file rename resynthesis/$FPGA_TOP.vqm $netlist_file
} else {
    if {[catch {execute_module -tool asm} result]} {
        qexit -error
    }
    #Move bitstream out of the reports directory
    file rename reports/$FPGA_TOP.sof $FPGA_TOP.sof
}

project_close

#rename report files
file rename reports/$FPGA_TOP.fit.summary reports/$FPGA_TOP\_$PART.fit.summary
file rename reports/$FPGA_TOP.sta.summary reports/$FPGA_TOP\_$PART.sta.summary
