<!--
SPDX-FileCopyrightText: 2025 IObundle

SPDX-License-Identifier: MIT
-->

# IOb-System-Linux

[SoCLinux](https://nlnet.nl/project/SoCLinux/) is an open-source project that aims to configure and generate a Linux system for RISC-V processors, focusing on creating a robust and maintainable environment for designing and testing IP cores.
The project builds upon the existing open-source Py2HWSW framework powering the IOb-SoC platform, enhancing the functionality and portability of IP cores, by using as examples the key IOb-Cache, IOb-Eth, and IOb-UART16550 open-source cores.
By providing a Linux IP core testbed, SoCLinux enables developers to build and test Linux drivers for new IP cores quickly, accelerating the production of high-quality IP cores, open-source or otherwise. 
The project aims to establish a widely adopted and maintainable ecosystem for IP core development, benefiting the broader community of IP core providers and users.
SoCLinux will leverage the IP-XACT standard (IEEE 1685) for IP core packaging, and seamlessly exchange IP cores with FuseSoC, a well-known open-source IP core package manager.

IOb-System-Linux is based on the IOb-System System-on-Chip (SoC) template from the Py2HWSW library.
This system was initially developed during for the [OpenCryptoLinux](https://nlnet.nl/project/OpenCryptoLinux/) project.

## Differences to IOb-System
This section outlines the distinctions between IOb-System and IOb-System-Linux.

Compared to IOb-System, IOb-System-Linux features a distinct CPU and employs AXI in the internal signals, deviating from the IOb-bus used by IOb-System. Another significant difference is the placement of firmware, as the one in IOb-System-Linux always resides in external memory.

Additionally, the bootloader in IOb-System-Linux differs from that in IOb-System. In IOb-System-Linux, the bootloader is directly loaded into internal RAM, whereas in IOb-System, the bootloader binary starts in ROM and is then copied to RAM.

The boot control unit in IOb-System-Linux, unlike IOb-System, is a distinct module and exclusively manages the boot process state. On the software side, the IOb-System-Linux bootloader initially loads a file named iob_mem.config, which specifies the files and their respective memory addresses to be copied into external memory.

<!--
TODO: automate this in Makefile
## Ethernet simulation

The ethernet simulation requires setting up dummy interfaces with
`eth-[SIMULATOR]` that require `sudo`:
Setup the following interfaces with the commands:
```bash
sudo modprobe dummy
sudo ip link add eth-icarus type dummy
sudo ifconfig eth-icarus up
sudo ip link add eth-verilator type dummy
sudo ifconfig eth-verilator up
```

#### Make dummy interfaces permanent:
1. Add `dummy` to `/etc/modules`
2. Create `/etc/network/if-pre-up.d/dummy-eth-interfaces` with:
```bash
#!/usr/bin/env bash

# Create eth-SIMULATOR dummy interfaces
ip link add eth-icarus type dummy
ifconfig eth-icarus up
ip link add eth-verilator type dummy
ifconfig eth-verilator up
```
3. Set script as executable:
```bash
# Set script as executable
sudo chmod +x /etc/network/if-pre-up.d/dummy-eth-interfaces
```

## Ethernet Receiver MAC Address
The current ethernet setup uses a fake receiver MAC address (RMAC_ADDR) common
for all simulators and boards. To receive ethernet packets for any destination
address, the interface connected to the board needs to be in premiscuous mode.
Check premiscuous mode with the command:
```bash
ip -d link
# check for promiscuity 1
```
Set promiscuity to 1 with the command:
```bash
sudo ip link set [interface] promisc on
```

## Ethernet RAW frame access
The system's Python scripts need RAW frame access for Ethernet communication.
To achieve this, the Python interpreter must have the CAP_NET_RAW capability.

The 'ETHERNET' submodule already includes a Python wrapper that provides RAW frame access.
To build the python wrapper, run:
```bash
make -C submodules/ETHERNET/scripts/pyRawWrapper
```
-->

# Tutorial: Add New Device Driver
Checkout [this tutorial](document/device_driver_tutorial.md) for more details on
how to add a new device to be tested.

# Acknowledgement
This project is funded through [NGI Zero Core](https://nlnet.nl/core), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/SoCLinux).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/core)



The [OpenCryptoLinux](https://nlnet.nl/project/OpenCryptoLinux/) project was funded through the NGI Assure Fund, a fund established by NLnet with financial support from the European Commission's Next Generation Internet programme, under the aegis of DG Communications Networks, Content and Technology under grant agreement No 957073.

<table>
    <tr>
        <td align="center" width="50%"><img src="https://nlnet.nl/logo/banner.svg" alt="NLnet foundation logo" style="width:90%"></td>
        <td align="center"><img src="https://nlnet.nl/image/logos/NGIAssure_tag.svg" alt="NGI Assure logo" style="width:90%"></td>
    </tr>
</table>
