# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

set TOP [lindex $argv 0]
set CSR_IF [lindex $argv 1]
set INCLUDE_DIRS [lindex $argv 3]

puts "TOP: $TOP"
puts "CSR_IF: $CSR_IF"
puts "INCLUDE_DIRS: $INCLUDE_DIRS"

set WS alint/$TOP\_ws
set PRJ $TOP\_prj


if {![ file exists $WS.alintws ]} {
   workspace.create $WS
}
workspace.open $WS.alintws

if {![ file exists $PRJ.alintproj ]} {
   workspace.project.create $PRJ
}

workspace.project.open $PRJ.alintproj

puts "Reading files"


#includes
foreach dir $INCLUDE_DIRS {
    project.pref.vlogdirs -path $dir
}

workspace.file.add -destination $PRJ -f $TOP\_files.list

# List of SDC files to open
set sdcFiles {
    "../syn/umc130/$TOP_dev.sdc"
    "../syn/src/$TOP.sdc"
    "../syn/src/$TOP_$CSR_IF.sdc"
    "../syn/$TOP_tool.sdc"
}

# Open the output file for writing
set outfile [open "merged.sdc" "w"]

# Loop through each SDC file
foreach sdcFile $sdcFiles {
    # Check if the file exists before trying to open it
    if {[file exists $sdcFile]} {
        # Open the SDC file for reading
        set sdcFileHandle [open $sdcFile "r"]
        
        # Read the contents of the SDC file
        set contents [read $sdcFileHandle]
        
        # Write the contents to the output file
        puts $outfile $contents
        
        # Close the SDC file
        close $sdcFileHandle
    } else {
        puts "Warning: File $sdcFile does not exist."
    }
}

# Close the output file
close $outfile

workspace.file.add -destination $PRJ merged.sdc

project.pref.toplevels -top $TOP

project.pref.vlogstandard -format sv2005


#project.policy.add -policy STARC_VLOG_ALL

do ./alint_waiver.do

project.run -project $PRJ

#project.parse
#project.elaborate
#project.constrain -clocks
#project.constrain -resets
#project.constrain -chip
#project.constrain 
source merged.sdc

project.run -project $PRJ

#project.lint
#Synth reports
project.report.synthesis -report alint_synth.txt
project.report.violations -format simple_text -report alint_violations.txt
project.report.violations -format pdf -report alint_violations.pdf
project.report.quality -report alint_qor.txt

file delete $outfile
