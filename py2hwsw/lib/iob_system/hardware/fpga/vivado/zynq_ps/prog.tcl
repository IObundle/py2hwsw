# Connect to the board via JTAG
connect

# Set target to the Zynq device (usually one target with 'Zynq' in the name)
targets -set -filter {name =~ "*Zynq*"}

# Open the hardware platform from the XSA file
open_hw_platform -xsa ./path/to/your_platform.xsa

# Program the FPGA bitstream contained in the XSA platform
program_hw_device

# Load your PS application ELF
# Replace with the path to your ELF built with Vitis
load_hw_elf ./path/to/your_ps_app.elf

# Run the PS application
concurrent_hw_execute

# Done: exit XSCT
exit
