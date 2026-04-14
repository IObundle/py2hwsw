#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

"""
Transfer files via serial communication to a Linux system with base64 encoding.
Needs 'base64' command available on the host and the target system.
Uses a slow transfer speed (configurable bursts of data with delay between them) to avoid skipping characters.
"""

import subprocess
import time
import sys
import os


def run_uart_cmd(cmd, uart_dev):
    """Run shell command on UART device."""
    full_cmd = f"echo '{cmd}' > {uart_dev}"
    subprocess.run(full_cmd, shell=True, check=True)
    time.sleep(1)


def send_base64_slowly(base64_data, uart_dev, chunk_size=8, delay=0.2):
    """Send base64 data slowly ending with two Ctrl+D using printf.
    Useful link does not support full baudrate speed.
    For example, if a receiving system uses uart without interrupts (with polling) and may skip characters if they are sent too fast.
    """
    total_chunks = (len(base64_data) + chunk_size - 1) // chunk_size
    print(
        f"Transfer using chunks of size {chunk_size} at every {delay}s ({total_chunks} chunks total)"
    )

    chunk_count = 0
    for i in range(0, len(base64_data), chunk_size):
        chunk = base64_data[i : i + chunk_size]
        full_cmd = f"printf '{chunk}' > {uart_dev}"
        subprocess.run(full_cmd, shell=True, check=True)
        time.sleep(delay)
        chunk_count += 1

        # Progress every 50 chunks or at end
        if chunk_count % 50 == 0 or chunk_count == total_chunks:
            percent = (chunk_count / total_chunks) * 100
            print(
                f"\rProgress: {chunk_count}/{total_chunks} chunks ({percent:.1f}%)",
                end="",
                flush=True,
            )

    # Send TWO Ctrl+D (ASCII 4) as requested
    subprocess.run(f"printf '\x04\x04' > {uart_dev}", shell=True)
    print("\n✓ Transfer complete")
    time.sleep(delay)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 uart_base64_transfer.py <input_file> <uart_device>")
        sys.exit(1)

    input_file = sys.argv[1]
    filename = os.path.basename(input_file)
    uart_dev = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        sys.exit(1)

    if not os.path.exists(uart_dev):
        print(f"Error: UART device {uart_dev} not found")
        sys.exit(1)

    print(f"Transferring {input_file} via {uart_dev}...")

    # Step 1: Encode file to base64
    print("1. Encoding file to base64...")
    base64_result = subprocess.run(
        ["base64", input_file], capture_output=True, text=True, check=True
    )
    base64_data = base64_result.stdout.strip()
    print(f"Base64 size: {len(base64_data)} chars")

    # Step 2: Prepare device to receive (starts base64 decoder)
    print("2. Preparing device to receive base64 data...")
    run_uart_cmd(f"base64 -d > {filename}", uart_dev)

    # Step 3: Send base64 data slowly with Ctrl+D EOF
    print("3. Sending base64 data slowly...")
    send_base64_slowly(base64_data, uart_dev, chunk_size=15, delay=0.1)

    # Step 4: Verify on device
    print("4. Verifying transfer...")
    run_uart_cmd("sync", uart_dev)
    run_uart_cmd(f"ls -l {filename}", uart_dev)

    print("Transfer complete! Ctrl+D sent as EOF signal.")


if __name__ == "__main__":
    main()
