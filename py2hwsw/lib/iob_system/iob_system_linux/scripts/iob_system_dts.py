# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
import iob_system_utils

#
# Functions
#

SPDX_PREFIX = "SPDX-"


def generate_dts(dts_parameters):
    """Generate a Linux device tree for iob_system."""
    spdx = {
        "author": dts_parameters.get("author", "IObundle"),
        "spdx_year": dts_parameters.get("spdx_year", "2025"),
        "spdx_license": dts_parameters.get("spdx_license", "MIT"),
    }
    # Use 'console=ttyS0,115200' for Linux 8250 serial driver (interrupts). Use 'console=hvc0` for OpenSBI serial driver (polling).
    bootargs = dts_parameters.get(
        "bootargs",
        "rootwait console=hvc0 earlycon=sbi root=/dev/ram0 init=/sbin/init swiotlb=32 loglevel=8",
    )

    extra_peripherals = ""
    if dts_parameters["hardcoded_plic_cint"]:
        # Only need hardcoded PLIC and CLINT if they included in the CPU wrapper (and are not in the iob_system's peripherals list)
        extra_peripherals += """
        // Hardcoded PLIC and CLINT

        CLINT0: clint@/*CLINT0_BASE_MACRO*/ {
            compatible = "riscv,clint0";
            reg = <0x/*CLINT0_BASE_MACRO*/ 0xc0000>;
            interrupts-extended = < &CPU0_intc 3
                                    &CPU0_intc 7 >;
            reg-names = "control";
        };

        PLIC0: plic@/*PLIC0_BASE_MACRO*/ {
            compatible = "riscv,plic0";
            reg = <0x/*PLIC0_BASE_MACRO*/ 0x4000000>;

            #address-cells = <0>; // No sub-nodes expected under PLIC (leaf interrupt controller)
            #interrupt-cells = <1>; // PLIC interrupt specifiers use 1 cell: the interrupt ID number
            interrupt-controller; // Declares this node as an interrupt controller
            // PLIC context connections to CPU interrupt controller:
            // Context 0 on CPU0 IRQ 11, Context 1 on CPU0 IRQ 9 (for M-mode/S-mode)
            interrupts-extended = < &CPU0_intc 11
                                    &CPU0_intc 9 >;
            reg-names = "control"; // Names the register region ("control" for PLIC CSRs)
            //riscv,max-priority = <4>; // Maximum interrupt priority level supported (0-4 scale)
            riscv,ndev = <31>; // Number of external interrupt sources/lines supported by this PLIC (1-31
        };
"""

    # Generate DTS file
    dts = f"""
// {SPDX_PREFIX}FileCopyrightText: {spdx['spdx_year']} {spdx['author']}
//
// {SPDX_PREFIX}License-Identifier: {spdx['spdx_license']}

/* Auto-generated device tree file for {dts_parameters['name']} SoC. */

/dts-v1/;

/ {{
    #address-cells = <1>;
    #size-cells = <1>;
    model = "IOb-System-Linux, VexRiscv";
    compatible = "IOb-System-Linux, VexRiscv";
    cpus {{
        #address-cells = <0x1>;
        #size-cells = <0x0>;
        timebase-frequency = <100000>; // Timebase frequency matches frequency of 'mtime' updates from PLIC peripheral (100 kHz for iob_plic). Change this value to match configured PLIC peripheral.
        CPU0: cpu@0 {{
            clock-frequency = </*FREQ_MACRO*/>;
            device_type = "cpu";
            reg = <0x0>;
            status = "okay";
            compatible = "riscv";
            riscv,isa = "rv32imac";
            mmu-type = "riscv,sv32";
            d-cache-block-size = <0x40>;
            d-cache-sets = <0x40>;
            d-cache-size = <0x8000>;
            d-tlb-sets = <0x1>;
            d-tlb-size = <0x20>;
            i-cache-block-size = <0x40>;
            i-cache-sets = <0x40>;
            i-cache-size = <0x8000>;
            i-tlb-sets = <0x1>;
            i-tlb-size = <0x20>;
            tlb-split;
            CPU0_intc: interrupt-controller {{
                #address-cells = <0>;
                #interrupt-cells = <1>;
                interrupt-controller;
                compatible = "riscv,cpu-intc";
            }};
        }};
    }};
    memory@0 {{
        device_type = "memory";
        reg = <0x0 /*OS_RANGE_MACRO*/>;
    }};
    chosen {{
        bootargs = "{bootargs}";
        linux,initrd-start = <0x01000000>;
        linux,initrd-end = <0x01C00000>; // max 12MB ramdisk (rootfs) image
    }};
    soc: soc {{
        #address-cells = <1>;
        #size-cells = <1>;
        compatible = "iobundle,{dts_parameters['name']}", "simple-bus";
        ranges;

        // Peripherals added via #include statements.
        {extra_peripherals}
    }};
}};

/* Include peripherals dtsi files here */
#include "peripherals.dtsi"
"""

    # Write DTS file
    os.makedirs(os.path.join(dts_parameters["build_dir"], "software"), exist_ok=True)
    with open(
        os.path.join(
            dts_parameters["build_dir"],
            "software",
            f"{dts_parameters['name']}.dts",
        ),
        "w",
    ) as f:
        f.write(dts)

    print(
        f"Generated DTS file: {dts_parameters['build_dir']}/software/src/{dts_parameters['name']}.dts"
    )


#
# Main
#

if __name__ == "__main__":
    # Dummy data for testing
    dts_parameters = {
        "name": "iob_system",
        "build_dir": "/tmp",
        "hardcoded_plic_cint": False,
    }

    generate_dts(dts_parameters)
