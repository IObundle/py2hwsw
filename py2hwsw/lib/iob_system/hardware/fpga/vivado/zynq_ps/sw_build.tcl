# Set project name and paths
set hw_file "your_hw_platform.xsa"
set platform_name "zybo_platform"
set app_name "baremetal_app"
set domain_name "standalone_domain"

# Create workspace
setws ./vitis_workspace

# Create platform project
platform create -name $platform_name -hw $hw_file -out ./$platform_name

# Create domain (bare-metal, Cortex-A9)
platform write
platform active $platform_name
domain create -name $domain_name -os standalone -proc ps7_cortexa9_0 -arch 32-bit
platform generate

# Create application project
app create -name $app_name -platform $platform_name -domain $domain_name -template "Empty Application"

# Add source files
app addsrc -name $app_name -path ./src

# Build the application
app build -name $app_name
