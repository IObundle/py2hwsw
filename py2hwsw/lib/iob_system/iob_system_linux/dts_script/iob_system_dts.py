# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
import iob_system_utils

#
# Functions
#


def generate_dts(attributes_dict, params, py_params):
    """Generate a Linux device tree for iob_system.
    :param dict attributes_dict: iob_system attributes
    :param dict params: iob_system python parameters
    :param dict py_params: iob_system argument python parameters
    """
    # Don't create DTS file for other targets (like clean)
    if "py2hwsw_target" not in py_params or py_params["py2hwsw_target"] != "setup":
        return

    # Get peripherals list
    peripherals = iob_system_utils.get_iob_system_peripherals_list(attributes_dict)

    # Generate memory map
    iob_system_utils.generate_memory_map(
        attributes_dict, peripherals, params, py_params
    )

    # Read generated memory map
    memory_map = {}
    with open(
        os.path.join(
            attributes_dict["build_dir"],
            "software/src",
            f"{attributes_dict['name']}_mmap.h",
        ),
        "r",
    ) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#define"):
                parts = line.split()
                memory_map[parts[1]] = int(parts[2], 0)

    # Generate DTS file
    dts = f"""
/dts-v1/;

/ {{
    #address-cells = <1>;
    #size-cells = <1>;
    model = "IOb-System-Linux, VexRiscv";
    compatible = "IOb-System-Linux, VexRiscv";
    cpus {{
        #address-cells = <0x1>;
        #size-cells = <0x0>;
        timebase-frequency = <{params.get("freq", "/*FREQ_MACRO*/")}>;
        CPU0: cpu@0 {{
            clock-frequency = <{params.get("freq", "/*FREQ_MACRO*/")}>;
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
        reg = <0x0 {params.get("mem_size", "/*OS_RANGE_MACRO*/")}>;
    }};
    chosen {{
        bootargs = "rootwait console=hvc0 earlycon=sbi root=/dev/ram0 init=/sbin/init swiotlb=32 loglevel=8";
        linux,initrd-start = <0x01000000>;
        linux,initrd-end = <0x01800000>; // max 8MB ramdisk image
    }};
    soc {{
        #address-cells = <1>;
        #size-cells = <1>;
        compatible = "iobundle,iob-system-linux", "simple-bus";
        ranges;
"""

    for peripheral in peripherals:
        p_name = peripheral["instance_name"]
        p_addr = memory_map.get(f"{p_name}_BASE", f"/*{p_name}_BASE_MACRO*/")
        dts += f"""
        {p_name}: {p_name.lower()}@{p_addr:x} {{
            compatible = "iobundle,{peripheral['core_name']}";
            reg = <0x{p_addr:x} 0x1000>;
"""
        if p_name == "UART0":
            dts += f"""            clock-frequency = <{params.get("freq", "/*FREQ_MACRO*/")}>;
            current-speed = <{params.get("baud", "/*BAUD_MACRO*/")}>;
"""
        dts += "        };\n"

    # Add CLINT0 and PLIC0
    clint_addr = memory_map.get("CLINT0_BASE", "/*CLINT0_BASE_MACRO*/")
    dts += f"""
        CLINT0: clint@{clint_addr:x} {{
            compatible = "riscv,clint0";
            interrupts-extended = < &CPU0_intc 3
                                    &CPU0_intc 7 >;
            reg = <0x{clint_addr:x} 0xc0000>;
            reg-names = "control";
        }};
"""

    plic_addr = memory_map.get("PLIC0_BASE", "/*PLIC0_BASE_MACRO*/")
    dts += f"""
        PLIC0: plic@{plic_addr:x} {{
            #address-cells = <0>;
            #interrupt-cells = <1>;
            compatible = "riscv,plic0";
            interrupt-controller;
            interrupts-extended = < &CPU0_intc 11
                                    &CPU0_intc 9 >;
            reg = <0x{plic_addr:x} 0x4000000>;
            reg-names = "control";
            riscv,max-priority = <7>;
            riscv,ndev = <31>;
        }};
"""

    dts += """
    };
};
"""

    # Write DTS file
    os.makedirs(
        os.path.join(attributes_dict["build_dir"], "software/src"), exist_ok=True
    )
    with open(
        os.path.join(
            attributes_dict["build_dir"],
            "software/src",
            f"{attributes_dict['name']}.dts",
        ),
        "w",
    ) as f:
        f.write(dts)
    print(
        f"Generated DTS file: {attributes_dict['build_dir']}/software/src/{attributes_dict['name']}.dts"
    )


#
# Main
#

if __name__ == "__main__":
    # Dummy data for testing
    attributes = {
        "name": "iob_system",
        "version": "0.1",
        "build_dir": "build",
        "subblocks": [
            {"instance_name": "cpu", "core_name": "VexRiscv"},
            {"instance_name": "iob_pbus_split"},
            {
                "instance_name": "TIMER0",
                "core_name": "iob_timer",
                "is_peripheral": True,
            },
            {"instance_name": "SPI0", "core_name": "iob_spi", "is_peripheral": True},
            {"instance_name": "UART0", "core_name": "iob_uart", "is_peripheral": True},
        ],
        "wires": [],
    }
    parameters = {
        "addr_w": 32,
        "use_peripherals": True,
        "use_intmem": True,
        "use_extmem": True,
        "use_bootrom": True,
        "freq": 100000000,
        "mem_size": 0x8000000,
        "baud": 115200,
        "cpu": "VexRiscv",
        "init_mem": True,
        "use_ethernet": False,
        "fw_baseaddr": 0,
        "fw_addr_w": 24,
        "bootrom_addr_w": 16,
    }
    python_params = {"py2hwsw_target": "setup"}

    generate_dts(attributes, parameters, python_params)
