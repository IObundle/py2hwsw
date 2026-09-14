# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

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

    cpu_name = dts_parameters.get("cpu", "iob_vexriscv")

    if "vexiiriscv" in cpu_name:
        cpu_model = "IOb-System-Linux, VexiiRiscv"
        riscv_isa = "rv32imac_zicsr_zifencei_zicbom"
        extra_cpu_props = "            riscv,cbom-block-size = <64>; // Define the cache line size (VexiiRiscv default is 64 bytes) - needed for zicbom cache management\n"
        bus_dma_prop = "        dma-noncoherent; // tells Linux that every peripheral of this bus using DMA need explicit cache flushes\n"
    elif "cva6" in cpu_name:
        # CVA6 rv32imac + Sv32 MMU (cv32a6_imac_sv32 config). CVA6
        # implements Zicsr and Zifencei natively but does NOT implement
        # Zicbom (cache-block management) - leave the IO region
        # non-coherent and let software fall back to the SBI
        # cache-flush calls.
        cpu_model = "IOb-System-Linux, CVA6"
        riscv_isa = "rv32imac_zicsr_zifencei"
        extra_cpu_props = ""
        bus_dma_prop = "        dma-noncoherent; // tells Linux that every peripheral of this bus using DMA need explicit cache flushes\n"
    else:  # vexriscv / default
        cpu_model = "IOb-System-Linux, VexRiscv"
        riscv_isa = "rv32imac_zicsr_zifencei"
        extra_cpu_props = ""
        bus_dma_prop = ""
        # FIXME: AN: I think vexriscv is also noncoherent with DMA peripherals since it has a data cache that must be invalidated to ensure peripehral DMA data is read correctly.
        # bus_dma_prop = "        dma-noncoherent; // tells Linux that every peripheral of this bus using DMA need explicit cache flushes\n"

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
    model = "{cpu_model}";
    compatible = "{cpu_model}";
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
            riscv,isa = "{riscv_isa}";
{extra_cpu_props}            mmu-type = "riscv,sv32";
            d-cache-block-size = <0x40>;
            d-cache-sets = <0x40>;
            d-cache-size = <0x1000>;
            i-cache-block-size = <0x40>;
            i-cache-sets = <0x40>;
            i-cache-size = <0x2000>;
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
        // rng-seed: 32 bytes of bootloader-supplied randomness used to seed the
        // kernel CRNG immediately at boot (requires CONFIG_RANDOM_TRUST_BOOTLOADER).
        // The kernel consumes and zeroes this property. NOTE: this is a fixed
        // development seed; for production, OpenSBI/bootloader should generate a
        // fresh seed per boot (e.g. from a hardware RNG) instead of a constant.
        rng-seed = <0x6f1e5c8a 0x3a29d04b 0x8c72e6f9 0x4bd05c3a
                    0x1a9f3e27 0x5c8d2b74 0xe6f0a419 0x3b75d28c>;
    }};
    soc: soc {{
        #address-cells = <1>;
        #size-cells = <1>;
        compatible = "iobundle,{dts_parameters['name']}", "simple-bus";
        ranges;
{bus_dma_prop}
        // Peripherals added via #include statements.
        {extra_peripherals}
        // Sys clock for Ethernet MII MDIO clock divider
        sys_clk: clock {{
          compatible = "fixed-clock";
          #clock-cells = <0>;
          clock-frequency = </*FREQ_MACRO*/>;
        }};
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
