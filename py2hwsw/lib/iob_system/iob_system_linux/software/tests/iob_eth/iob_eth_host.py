#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

"""
IOb-ETH ethoc Driver Test — Host Companion Script

Runs on the Linux host connected to the SoC via Ethernet.
Listens for test command packets from the SoC-side test program
(iob_eth_test) and responds accordingly.

Usage:
    python3 iob_eth_host.py <interface> [--soc-ip <ip>] [--port <port>]

Example:
    python3 iob_eth_host.py enp0s3 --soc-ip 192.168.1.10

The script sets up a static ARP entry for the SoC and listens on UDP port
9000 for command frames. It processes each command and sends the appropriate
response back to the SoC.
"""

import argparse
import fcntl
import os
import socket
import struct
import sys
import time

# ---------------------------------------------------------------
# Command IDs (must match iob_eth_test.c)
# ---------------------------------------------------------------

CMD_ECHO = 0x01
CMD_BROADCAST = 0x02
CMD_STRESS_TX = 0x03
CMD_STRESS_RX = 0x04
CMD_GET_HOST_MAC = 0x05
CMD_DONE = 0x06

# Packet header: cmd(1) + id(1) + len(2) = 4 bytes
HDR_SIZE = 4

# ---------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------

stats = {
    "frames_received": 0,
    "frames_sent": 0,
    "echo_count": 0,
    "broadcast_count": 0,
    "stress_tx_count": 0,
    "stress_rx_count": 0,
    "errors": 0,
    "start_time": None,
}


def log(msg):
    print(f"  [host] {msg}", flush=True)


def get_mac_str(iface):
    """Get MAC address string of a network interface."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        info = fcntl.ioctl(
            s.fileno(),
            0x8927,  # SIOCGIFHWADDR
            struct.pack("256s", iface.encode("utf-8")[:15]),
        )
        mac = info[18:24]
        return ":".join(f"{b:02X}" for b in mac)
    except OSError:
        return None
    finally:
        s.close()


def setup_static_arp(iface, ip, mac):
    """Log ARP info (kernel handles ARP automatically)."""
    log(f"Static ARP: {ip} -> {mac}")


def get_interface_ip(iface):
    """Get the IP address of a network interface."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        info = fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack("256s", iface.encode("utf-8")[:15]),
        )
        return socket.inet_ntoa(info[20:24])
    except OSError:
        return None
    finally:
        s.close()


# ---------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------


def handle_echo(data):
    """Echo back the payload unchanged."""
    stats["echo_count"] += 1
    return data


def handle_broadcast(data):
    """Acknowledge broadcast receipt."""
    stats["broadcast_count"] += 1
    log(f"Broadcast frame received ({len(data)} bytes)")
    return b"\x42"


def handle_stress_tx(data, sock, soc_addr):
    """
    SoC is about to send us a burst of frames.
    Payload: count(2) + size(2).
    We just acknowledge; the SoC sends the frames separately.
    """
    count = (data[0] << 8) | data[1]
    size = (data[2] << 8) | data[3]
    stats["stress_tx_count"] += count
    log(f"Stress TX: expecting {count} frames of {size} bytes")
    return b"\x42"


def handle_stress_rx(data, sock, soc_addr):
    """
    SoC wants us to send a burst of frames.
    Payload: count(2) + size(2).
    """
    count = (data[0] << 8) | data[1]
    size = (data[2] << 8) | data[3]

    log(f"Stress RX: sending {count} frames of {size} bytes")

    # Build the packet header for echo frames
    pkt = bytearray(HDR_SIZE + size)
    pkt[0] = CMD_ECHO  # cmd
    pkt[1] = 0  # id
    struct.pack_into("!H", pkt, 2, size)  # len

    # Fill payload with repeating pattern
    for i in range(size):
        pkt[HDR_SIZE + i] = (i + 1) & 0xFF

    for i in range(count):
        pkt[1] = i & 0xFF  # update id
        try:
            sock.sendto(bytes(pkt), soc_addr)
            stats["frames_sent"] += 1
        except OSError as e:
            log(f"Send error at frame {i}: {e}")
            stats["errors"] += 1
            break
        time.sleep(0.01)  # 10ms delay for SoC to drain RX ring

    log(f"Stress RX: sent {count} frames")
    return b"\x42"


def handle_get_host_mac(data):
    """Return our MAC address."""
    mac_hex = stats.get("mac_bytes", b"\x00" * 6)
    return mac_hex


def handle_done(data):
    """Test complete. Print summary."""
    log("DONE received — test complete")
    return b"\x00"


# ---------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------


def run_server(args):
    """Main event loop: receive commands from SoC and respond."""
    iface = args.interface
    port = args.port
    soc_ip = args.soc_ip

    # Get our MAC address
    mac_str = get_mac_str(iface)
    if not mac_str:
        print(f"Error: Could not get MAC address of {iface}", file=sys.stderr)
        sys.exit(1)

    mac_bytes = bytes.fromhex(mac_str.replace(":", ""))
    stats["mac_bytes"] = mac_bytes

    # Get our IP
    local_ip = get_interface_ip(iface)
    log(f"Interface: {iface}")
    log(f"Local MAC: {mac_str}")
    log(f"Local IP:  {local_ip}")

    if soc_ip:
        log(f"SoC IP:    {soc_ip}")
        setup_static_arp(iface, soc_ip, mac_str)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))

    log(f"Listening on UDP port {port}...")
    log("Waiting for test commands from SoC...")
    print()

    stats["start_time"] = time.time()

    while True:
        try:
            data, addr = sock.recvfrom(1536)
        except KeyboardInterrupt:
            break
        except OSError as e:
            log(f"recv error: {e}")
            stats["errors"] += 1
            continue

        if len(data) < HDR_SIZE:
            continue

        cmd = data[0]
        pkt_id = data[1]
        pkt_len = struct.unpack("!H", data[2:4])[0]
        payload = data[HDR_SIZE : HDR_SIZE + pkt_len]

        stats["frames_received"] += 1

        soc_addr = (soc_ip if soc_ip else addr[0], port)

        response = None

        if cmd == CMD_ECHO:
            response = handle_echo(payload)

        elif cmd == CMD_BROADCAST:
            response = handle_broadcast(payload)

        elif cmd == CMD_STRESS_TX:
            response = handle_stress_tx(payload, sock, soc_addr)

        elif cmd == CMD_STRESS_RX:
            response = handle_stress_rx(payload, sock, soc_addr)

        elif cmd == CMD_GET_HOST_MAC:
            response = handle_get_host_mac(payload)

        elif cmd == CMD_DONE:
            response = handle_done(payload)
            # send final response then break
            if response is not None:
                resp_pkt = bytearray(HDR_SIZE + len(response))
                resp_pkt[0] = cmd
                resp_pkt[1] = pkt_id
                struct.pack_into("!H", resp_pkt, 2, len(response))
                resp_pkt[HDR_SIZE:] = response
                try:
                    sock.sendto(bytes(resp_pkt), soc_addr)
                    stats["frames_sent"] += 1
                except OSError:
                    pass
            break

        else:
            log(f"Unknown command: 0x{cmd:02x}")
            continue

        # Send response
        if response is not None:
            resp_pkt = bytearray(HDR_SIZE + len(response))
            resp_pkt[0] = cmd
            resp_pkt[1] = pkt_id
            struct.pack_into("!H", resp_pkt, 2, len(response))
            resp_pkt[HDR_SIZE:] = response
            try:
                sock.sendto(bytes(resp_pkt), soc_addr)
                stats["frames_sent"] += 1
            except OSError as e:
                log(f"Send error: {e}")
                stats["errors"] += 1

    sock.close()

    # Print summary
    elapsed = time.time() - stats["start_time"]
    print()
    log("=== Host Script Summary ===")
    log(f"Duration:         {elapsed:.2f}s")
    log(f"Frames received:  {stats['frames_received']}")
    log(f"Frames sent:      {stats['frames_sent']}")
    log(f"Echo requests:    {stats['echo_count']}")
    log(f"Broadcast tests:  {stats['broadcast_count']}")
    log(f"Stress TX frames: {stats['stress_tx_count']}")
    log(f"Errors:           {stats['errors']}")


def main():
    parser = argparse.ArgumentParser(
        description="IOb-ETH ethoc Driver Test — Host Companion Script"
    )
    parser.add_argument("interface", help="Network interface connected to SoC")
    parser.add_argument("--soc-ip", help="SoC IP address for static ARP")
    parser.add_argument(
        "--port", type=int, default=9000, help="UDP port (default: 9000)"
    )
    args = parser.parse_args()

    run_server(args)


if __name__ == "__main__":
    main()
