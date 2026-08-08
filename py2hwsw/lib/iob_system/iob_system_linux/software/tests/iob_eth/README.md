<!--
SPDX-FileCopyrightText: 2026 IObundle

SPDX-License-Identifier: GPL-3.0-only
-->

# IOb-ETH ethoc Driver Compatibility Test

This test suite validates the **IOb-Eth** hardware core's compatibility with the standard Linux `ethoc` (OpenCores Ethernet MAC) network driver. It exercises the main driver operation modes through the standard Linux networking API (sockets, ioctl, ethtool, sysfs, /proc).

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

The test suite validates the primary ethoc driver operation modes:

### 1. Interface Detection & Driver Binding
Scans `/sys/class/net/` to find the interface whose driver resolves to `ethoc`.

### 2. Interface Bring-Up
Sets `IFF_UP` via `SIOCSIFFLAGS` and verifies the flag sticks via `SIOCGIFFLAGS`.

### 3. MAC Address Read/Write
Validates `ethoc_get_mac_address()`, `ethoc_set_mac_address()`, `MAC_ADDR0/1` register read/write via `ioctl(SIOCGIFHWADDR)` / `ioctl(SIOCSIFHWADDR)`.

### 4. Default Register State
Dumps all 21 MAC registers via ethtool. Verifies MODER = `CRC|PAD|FULLD|RXEN|TXEN`, IPGT = `0x15`, INT_MASK = `0x7F`, TX_BD_NUM valid.

### 5. Link State Detection
Reads link state via sysfs and ethtool (always passes — informational only).

### 6. MII/MDIO PHY Access
Reads PHY registers 0–4 via `SIOCGMIIPHY`/`SIOCGMIIREG`. Values are displayed but not validated against expected bit patterns.

### 7. Basic TX Frame Transmission
Sends a UDP frame, checks `tx_packets` increased and `tx_errors` did not.

### 8. TX Frame Size Range
Tests frames at 60, 128, 512, and 1468 bytes. Checks `tx_packets` increased and `tx_errors` did not for each size.

### 9. Basic RX Frame Reception
Sends a UDP echo request, receives the echo response, validates payload length and content, checks `rx_packets` increased and `rx_errors` did not.

### 10. RX Frame Size Range
Tests reception of various frame sizes with payload integrity verification.

### 11. Broadcast Reception
Checks `IFF_BROADCAST` flag, sends a broadcast frame, validates host acknowledges receipt.

### 12. Promiscuous Mode
Sets `IFF_PROMISC` via `SIOCSIFFLAGS` and verifies the flag is reflected back.

### 13. Loopback Mode
Attempts to set `IFF_LOOPBACK`. Passes regardless of support (informational).

### 14. MTU Change Rejection
Verifies MTU change is rejected (accepts `EINVAL`/`EOPNOTSUPP`/`ENODEV`/`ENOSYS`) and MTU remains at 1500.

### 15. ethtool Ring Parameters
Validates `ethoc_get_ringparam()`: TX power-of-two, total BDs ≤ 128, no mini/jumbo pending.

### 16. ethtool Register Dump
Validates `ethoc_get_regs()`, `ethoc_get_regs_len()` — full register map at offset 0x00–0x50.

### 17. Interrupt Verification
Reads IRQ count from `/proc/interrupts` before and after traffic; verifies count increased.

### 18. Error Counter Clean Check
Verifies that error counters (rx_errors, rx_frame_errors, tx_errors, tx_fifo_errors, tx_carrier_errors) did not increase during traffic. tx_collisions increase is informational only.

### 19. Stress TX Burst
Sends 50 frames (512 bytes each) and checks tx_packets ≥ 50 with no errors.

### 20. Stress RX Burst
Requests 10 frames from the host and verifies at least 10 are received with no errors.

### 21. Stress Bidirectional
Interleaved TX+RX (50 cycles) to exercise full-duplex path; checks at least one frame sent with no errors.

### 22. Interface Down
Clears `IFF_UP` via `SIOCSIFFLAGS` and verifies the flag is cleared; restores interface state.

### 23. Final Statistics Summary
Dumps key statistics, register values, and ring parameters.

## Protocol

SoC and host exchange UDP packets on port 9000 with a simple command protocol:

```
[cmd(1)] [id(1)] [len(2)] [payload(0-1468)]
```

| Command | ID | Description |
|---------|-----|-------------|
| ECHO | 0x01 | Host echoes payload back |
| BROADCAST | 0x02 | Host acknowledges broadcast frame |
| STRESS_TX | 0x03 | SoC sends burst; host acknowledges |
| STRESS_RX | 0x04 | Host sends burst of frames |
| GET_HOST_MAC | 0x05 | Host returns its MAC address |
| DONE | 0x06 | Test complete signal |

## ethoc Driver Functions Exercised

| Driver Function | What Is Actually Validated | Test(s) |
|----------------|---------------------------|---------|
| `ethoc_open` | IFF_UP flag via SIOCGIFFLAGS | 2, 4 |
| `ethoc_stop` | IFF_UP cleared via SIOCGIFFLAGS | 22 |
| `ethoc_reset` | MODER, IPGT, INT_MASK, TX_BD_NUM register defaults via ethtool dump | 4 |
| `ethoc_init_ring` | TX_BD_NUM range, ring parameter counts | 4, 15 |
| `ethoc_set_mac_address` | MAC read/write via SIOCGIFHWADDR/SIOCSIFHWADDR | 3 |
| `ethoc_set_multicast_list` | IFF_BROADCAST, IFF_PROMISC flags (userspace); loopback attempt | 11, 12, 13 |
| `ethoc_start_xmit` | tx_packets counter increments, tx_errors unchanged | 7, 8, 19, 21 |
| `ethoc_rx` | rx_packets counter increments, payload integrity (echo) | 9, 10, 20 |
| `ethoc_interrupt` | IRQ count in /proc/interrupts increases with traffic | 17 |
| `ethoc_mdio_read/write` | PHY register reads via SIOCGMIIPHY/SIOCGMIIREG (no value assertions) | 6 |
| `ethoc_mdio_poll` | Link state read from sysfs/ethtool (always passes) | 5 |
| `ethoc_change_mtu` | Rejects MTU change (accepts EINVAL/EOPNOTSUPP/ENODEV/ENOSYS) | 14 |
| `ethoc_get_regs` | Register count ≥ 21, full dump at offset 0x00-0x50 | 4, 16 |
| `ethoc_get_ringparam` | tx_pending power-of-2, total ≤ 128, no mini/jumbo pending | 15 |

## Limitations and Future Improvements

The test suite validates the main ethoc driver operation modes (TX, RX, interface lifecycle, MAC configuration, promiscuous/broadcast/loopback modes, and basic ethtool ops). The following areas are **not** covered and would strengthen the validation:

### Driver Entry Points Not Exercised
- `ndo_set_rx_mode` / hash table (multicast filtering)
- `ndo_tx_timeout` (TX hang recovery)
- `ndo_vlan_rx_add_vid` / `ndo_vlan_rx_kill_vid`
- ethtool `set_*` ops (set_ringparam, nway_reset, set_wol, etc.)
- `ethtool_ops.get_drvinfo` / `get_strings` / `get_ethtool_stats` / `get_sset_count`

### Registers Never Directly Validated
INT_SOURCE, IPGR1, IPGR2, PACKETLEN, COLLCONF, CTRLMODER, MIIMODER, MIICOMMAND, MIIADDRESS, MIITX_DATA, MIIRX_DATA, MIISTATUS, ETH_HASH0, ETH_HASH1, ETH_TXCTRL are never read or checked for expected values.

### PHY / MII Gaps
- No `SIOCSMIIREG` calls — PHY register writes are never tested
- Register values are displayed but never validated against expected values (BMCR bits, PHY ID, etc.)
- MII controller registers (MIIMODER, MIIADDRESS, MIICOMMAND, etc.) are never read directly

### Descriptor Rings Never Inspected
TX/RX buffer descriptor content, pointers, and status bits are not examined — only aggregate packet counters are checked.

### Interrupt Coverage
Only proves that IRQs fired (count increased). Does not verify which interrupt cause (TX vs RX vs error) or that NAPI was scheduled.

### Hardware / Link Limitations
- ~80% packet loss observed on some setups (CRC / physical layer issues); 4 tests may fail in practice
- ARP cache warm-up workaround required before tests
- UDP-only on a single port; no TCP, ICMP, or raw socket testing

### Suggested Additions
1. PHY register write-back verification (`SIOCSMIIREG`)
2. Descriptor ring inspection via debugfs or a small kernel module
3. Hash/multicast filter tests
4. ethtool stats, strings, and drvinfo
5. TX timeout recovery injection test
6. Register-level write-read-verify for all 21 MAC registers
7. Link-quality prerequisite check to skip RX tests on unreliable links
8. True concurrent bidirectional traffic (threads or async I/O)
9. Soak test (long-duration traffic)
