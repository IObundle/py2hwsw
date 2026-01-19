# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os

SPDX_PREFIX = "SPDX-"


def create_dts_file(path, peripheral):
    """Create device tree file with demo on how to include the peripheral in the device tree"""
    content = f"""\
// {SPDX_PREFIX}FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
//
// {SPDX_PREFIX}License-Identifier: {peripheral['spdx_license']}

/* Auto-generated device tree file template for a SoC that includes the {peripheral['name']} peripheral core. */

/dts-v1/;

// Include peripheral's device tree file
#include \"{peripheral['name']}.dtsi\"

/ {{
    #address-cells = <1>;
    #size-cells = <1>;
    model = \"IOb-SoC, VexRiscv\";
    compatible = \"IOb-SoC, VexRiscv\";
    // CPU
    // Memory
    // Choosen
    soc {{
        #address-cells = <1>;
        #size-cells = <1>;
        compatible = \"iobundle,iob-soc\", \"simple-bus\";
        ranges;

        // {peripheral['name']} added via #include statement.

        // Other SoC peripherals go here

    }};
}};"""
    with open(os.path.join(path, f"{peripheral['name']}_soc.dts"), "w") as f:
        f.write(content)


def create_dtsi_file(path, peripheral, extra_properties=""):
    """Create device tree include file to be included in the main SoC's device tree"""
    # NOTE: Using 'INSTANCE_NAME' as a special keyword that will be replaced with correct peripheral instance name by scripts in build dir.
    content = f"""\
// {SPDX_PREFIX}FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
//
// {SPDX_PREFIX}License-Identifier: {peripheral['spdx_license']}

/* Auto-generated device tree include file (.dtsi) for {peripheral['name']} peripheral core.
 * Include this file in your main SoC device tree.
 */

&soc {{
    // Include this core as a peripheral of main system labeled 'soc'.
    INSTANCE_NAME: {peripheral['name']}@/*INSTANCE_NAME_BASE_MACRO*/ {{
        compatible = \"{peripheral['compatible_str']}\";
        reg = <0x/*INSTANCE_NAME_BASE_MACRO*/ 0x/*{peripheral['name'].upper()}_CSRS_ADDR_RANGE_MACRO*/>;
        {extra_properties}
    }};
}};"""
    with open(os.path.join(path, f"{peripheral['name']}.dtsi"), "w") as f:
        f.write(content)


def create_device_tree_files(path, peripheral, extra_properties=""):
    """Generate device tree files for a given peripheral"""
    create_dts_file(path, peripheral)
    create_dtsi_file(path, peripheral, extra_properties)
