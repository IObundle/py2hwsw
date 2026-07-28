<!--
SPDX-FileCopyrightText: 2026 IObundle

SPDX-License-Identifier: GPL-3.0-only
-->

# IOb-ETH ethoc Driver Compatibility Test

This test suite validates the **IOb-Eth** hardware core's compatibility with the standard Linux `ethoc` (OpenCores Ethernet MAC) network driver. It exercises all driver configurations and operation modes through the standard Linux networking API (sockets, ioctl, ethtool, sysfs, /proc).

## Architecture

```
SoC (RISC-V Linux)                     Host (x86 Linux)
┌────────────────────────┐  100Mbps  ┌────────────────────────┐
│ iob_eth_test (C)       │◄─────────►│ iob_eth_host.py (Py3)  │
│ UDP sockets (port 9000)│  eth0↔X  │ echo/reply to commands  │
│ ioctl / ethtool / sysfs│           │                         │
└────────────────────────┘           └────────────────────────┘
```

The SoC-side test program sends command packets to the host companion script and validates the responses, statistics, and driver state at each step.

## Prerequisites

- IOb-Eth core integrated into the SoC, connected at 100Mbps to a Linux host
- Linux `ethoc` driver loaded (`compatible = "opencores,ethoc"` in device tree)
- Network interface available on both SoC and host
- Python 3 on the host (no external dependencies)
- `riscv64-unknown-linux-gnu-gcc` cross-compiler (in `nix-shell`)

## Building

The test program is cross-compiled for RISC-V (rv32imac) using the provided `nix-shell` environment. By default, it uses dynamic linking to minimize binary size.

```bash
nix-shell path/to/iob_linux --run 'make'
```

If your SoC lacks a full C library, build a standalone static binary:

```bash
nix-shell path/to/iob_linux --run 'make STATIC=1'
```

## Running

### Automated Validation (Recommended)

The `validate_eth.sh` script runs the entire test suite end-to-end:

```bash
# On the host, with SSH access to the SoC:
sh validate_eth.sh -S root -s 192.168.1.10 -i enp0s3

# Without SSH (run test manually on SoC):
sh validate_eth.sh -s 192.168.1.10 -i enp0s3
```

### Manual Execution

**On the host machine:**
```bash
python3 iob_eth_host.py <interface> --soc-ip <soc_ip>
# Example: python3 iob_eth_host.py enp0s3 --soc-ip 192.168.1.10
```

**On the SoC (in a separate terminal):**
```bash
./iob_eth_test -s <soc_ip> -c <host_ip> [-v]
# Example: ./iob_eth_test -s 192.168.1.10 -c 192.168.1.1 -v
```

## Command-Line Options

### iob_eth_test

| Option | Description |
|--------|-------------|
| `-i <iface>` | Network interface (auto-detected if omitted) |
| `-s <soc_ip>` | SoC IP address |
| `-c <host_ip>` | Host IP address (**required**) |
| `-v` | Verbose output (register dumps, detailed stats) |
| `-h` | Show help |

### iob_eth_host.py

| Option | Description |
|--------|-------------|
| `<interface>` | Host Ethernet interface (**required**) |
| `--soc-ip <ip>` | SoC IP address (for static ARP entry) |
| `--port <port>` | UDP port (default: 9000) |
| `-h` | Show help |

## Test Coverage

The test suite validates all ethoc driver configurations and operation modes:

### 1. Interface Detection & Driver Binding
Scans `/sys/class/net/` to find the interface whose driver resolves to `ethoc`. Validates `register_netdev` succeeded.

### 2. Interface Bring-Up
Exercises `ethoc_open()` — IRQ registration, NAPI enable, ring initialization, `ethoc_reset()`, PHY start.

### 3. MAC Address Read/Write
Validates `ethoc_get_mac_address()`, `ethoc_set_mac_address()`, `MAC_ADDR0/1` register read/write via `ioctl(SIOCGIFHWADDR)` / `ioctl(SIOCSIFHWADDR)`.

### 4. Default Register State
Dumps all 21 MAC registers via ethtool. Verifies MODER = `CRC|PAD|FULLD|RXEN|TXEN`, IPGT = `0x15`, INT_MASK = `0x7F`, TX_BD_NUM valid.

### 5. Link State Detection
Validates `ethoc_mdio_probe()`, `ethoc_mdio_poll()`, PHY link detection via sysfs and ethtool.

### 6. MII/MDIO PHY Access
Tests `SIOCGMIIPHY`, `SIOCGMIIREG` for PHY registers 0–4 (BMCR, BMSR, ID, ANAR). Validates `MIIMODER`, `MIIADDRESS`, `MIICOMMAND`, `MIIRX_DATA`, `MIISTATUS`.

### 7. Basic TX Frame Transmission
Validates `ethoc_start_xmit()`, TX BD ring, `TX_BD_CRC`, `TX_BD_READY`, CRC generation.

### 8. TX Frame Size Range
Tests frames at 60, 128, 512, and 1500 bytes. Validates `ETHOC_ZLEN` (64B minimum), `ETHOC_BUFSIZ` (1536B maximum), `TX_BD_PAD` for short frames.

### 9. Basic RX Frame Reception
Validates `ethoc_rx()`, RX BD ring, `RX_BD_EMPTY`, CRC checking, `ethoc_update_rx_stats()`.

### 10. RX Frame Size Range
Tests reception of various frame sizes with payload integrity verification.

### 11. Broadcast Reception
Validates `ethoc_set_multicast_list()` with `IFF_BROADCAST`, `MODER_BRO` (inverted logic).

### 12. Promiscuous Mode
Validates `ethoc_set_multicast_list()` with `IFF_PROMISC`, `MODER_PRO`.

### 13. Loopback Mode
Validates `ethoc_set_multicast_list()` with `IFF_LOOPBACK`, `MODER_LOOP`.

### 14. MTU Change Rejection
Verifies `ethoc_change_mtu()` returns `-ENOSYS` — MTU cannot be changed.

### 15. ethtool Ring Parameters
Validates `ethoc_get_ringparam()`: TX power-of-two, total BDs ≤ 128, no mini/jumbo pending.

### 16. ethtool Register Dump
Validates `ethoc_get_regs()`, `ethoc_get_regs_len()` — full register map at offset 0x00–0x50.

### 17. Interrupt Verification
Validates `ethoc_interrupt()`, NAPI scheduling, `INT_MASK_ALL` — IRQ count increases with traffic.

### 18. Error Counter Clean Check
Verifies all error counters (CRC, overrun, frame, carrier, FIFO, collisions) are zero.

### 19. Stress TX Burst
Sends 200 frames rapidly to exercise TX BD ring wrap-around, NAPI under load.

### 20. Stress RX Burst
Receives 200 frames rapidly to exercise RX BD ring wrap-around, `RX_BD_EMPTY` recycling.

### 21. Stress Bidirectional
Simultaneous TX+RX to validate full-duplex operation and concurrent BD usage.

### 22. Interface Down
Validates `ethoc_stop()` — NAPI disable, PHY stop, RX/TX disable, IRQ free.

### 23. Final Statistics Summary
Comprehensive dump of all statistics, registers, and ring parameters.

## Protocol

SoC and host exchange UDP packets on port 9000 with a simple command protocol:

```
[cmd(1)] [id(1)] [len(2)] [payload(0-64)]
```

| Command | ID | Description |
|---------|-----|-------------|
| ECHO | 0x01 | Host echoes payload back |
| BROADCAST | 0x02 | Host acknowledges broadcast frame |
| STRESS_TX | 0x03 | SoC sends burst; host acknowledges |
| STRESS_RX | 0x04 | Host sends burst of frames |
| GET_HOST_MAC | 0x05 | Host returns its MAC address |
| DONE | 0x06 | Test complete signal |

## ethoc Driver Configurations Tested

| Driver Function | Register(s) | Test(s) |
|----------------|-------------|---------|
| `ethoc_open` | MODER, IPGT, INT_MASK | 2, 4 |
| `ethoc_stop` | MODER | 22 |
| `ethoc_reset` | MODER(CRC,PAD,FULLD,RXEN,TXEN), IPGT, INT_MASK | 4 |
| `ethoc_init_ring` | TX_BD_NUM, BD memory | 4, 15 |
| `ethoc_set_mac_address` | MAC_ADDR0, MAC_ADDR1 | 3 |
| `ethoc_set_multicast_list` | MODER(LOOP,BRO,PRO), ETH_HASH0/1 | 11, 12, 13 |
| `ethoc_start_xmit` | TX BD ring, TX_BD_CRC, TX_BD_PAD | 7, 8 |
| `ethoc_rx` | RX BD ring, RX_BD_EMPTY | 9, 10 |
| `ethoc_interrupt` | INT_SOURCE, INT_MASK | 17 |
| `ethoc_mdio_read/write` | MIIMODER, MIIADDRESS, MIICOMMAND, MIIRX_DATA, MIISTATUS | 6 |
| `ethoc_mdio_poll` | MODER(FULLD) | 5 |
| `ethoc_change_mtu` | (returns -ENOSYS) | 14 |
| `ethoc_get_regs` | All 21 registers | 4, 16 |
| `ethoc_get_ringparam` | num_bd, num_tx, num_rx | 15 |
| `ethoc_update_rx_stats` | RX BD error bits | 18 |
| `ethoc_update_tx_stats` | TX BD error bits | 18 |
