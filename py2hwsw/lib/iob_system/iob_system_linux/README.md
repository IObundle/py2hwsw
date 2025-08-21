<!--
SPDX-FileCopyrightText: 2025 IObundle

SPDX-License-Identifier: MIT
-->

# IOb-System-Linux

The IOb-System-Linux System-on-Chip (SoC) is a Linux system which builds upon the existing functionality of the [IOb-System](https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/lib/iob_system) SoC. This IOb-System-Linux SoC is part of the wider [SoCLinux](https://nlnet.nl/project/SoCLinux/) project.

For users looking to create Linux-compatible SoC designs, the [SoCLinux template](https://github.com/IObundle/soc-linux) is available.
The SoCLinux template is a derivative system of the IOb-System-Linux, inheriting all of its components by default.

The IOb-System-Linux SoC is based on the system developed during the [OpenCryptoLinux](https://nlnet.nl/project/OpenCryptoLinux/) project.

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
The SoCLinux project is funded through [NGI Zero Core](https://nlnet.nl/core), a fund established by [NLnet](https://nlnet.nl) with financial support from the European Commission's [Next Generation Internet](https://ngi.eu) program. Learn more at the [NLnet project page](https://nlnet.nl/project/SoCLinux).

[<img src="https://nlnet.nl/logo/banner.png" alt="NLnet foundation logo" width="20%" />](https://nlnet.nl)
[<img src="https://nlnet.nl/image/logos/NGI0_tag.svg" alt="NGI Zero Logo" width="20%" />](https://nlnet.nl/core)
