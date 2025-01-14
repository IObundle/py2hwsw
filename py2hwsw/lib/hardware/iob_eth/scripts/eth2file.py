#!/usr/bin/env python3
# Script to relay raw ethernet frames from a network device to a file, and
# vice-versa. This allows ethernet access for the simulation tesbench.

import socket
import os
from threading import Thread

ETH_P_ALL = 0x0003


def file_2_eth(socket_object, file_object):
    while True:
        # Get frame size
        frame_size = int.from_bytes(file_object.read(2), byteorder="little")
        # Send frame to socket (ignore last 4 CRC bytes)
        socket_object.send(file_object.read(frame_size)[:-4])


def eth_2_file(socket_object, file_object, mac_filter=None):
    # Convert mac_filter (str) to bytes
    if type(mac_filter) is str:
        mac_filter = int(mac_filter, 16).to_bytes(6, "big")
    while True:
        # Capture frames and check their destination mac
        while True:
            frame_data, _ = socket_object.recvfrom(4096)
            # print(f"*detected frame {len(frame_data)} bytes")  # DEBUG
            if frame_data[0:6] == mac_filter:
                break
        # Ensure soc has read the previous frame by checking file size
        while file_object.tell() > 0:
            file_object.seek(0, os.SEEK_END)
        # Write two bytes with size of frame_data
        frame_size = len(frame_data).to_bytes(2, byteorder="little")
        file_object.write(frame_size + frame_data)
        # Not sure why but we need to move the cursor to make the Icarus testbench read
        # the file correctly.
        file_object.seek(0, os.SEEK_END)
        # print(f"*rcvd frame {len(frame_data)} bytes")  # DEBUG


def file_2_eth_thread(socket_object, fifo_file_path):
    # With a name pipe, we don't need keep polling and deleting chars from the file
    os.mkfifo(fifo_file_path)
    with open(fifo_file_path, "rb") as input_file:
        file_2_eth(socket_object, input_file)


def relay_frames(interface, input_file, output_file, mac_filter=None):
    """Relay frames from network device to file and vice-versa.
    param interface: name of network device
    param input_file: path to the generated input file. Will be a named pipe.
    param output_file: path to the generated output file
    param mac_filter: Filter out frames that do not have specified MAC addr as destination
    """

    # Delete old files
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(output_file):
        os.remove(output_file)

    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL)) as s:
        s.bind((interface, 0))

        f2e_thread = Thread(target=file_2_eth_thread, args=(s, input_file), daemon=True)
        f2e_thread.start()

        with open(output_file, "ab") as output_file:
            eth_2_file(s, output_file, mac_filter)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print(
            f"Usage: {sys.argv[0]} <interface> <input_file> <output_file> [-f <dest_mac_addr>]"
        )
        sys.exit(1)

    interface = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    dest_mac_addr = (sys.argv[sys.argv.index("-f") + 1] if "-f" in sys.argv else None,)

    try:
        relay_frames(interface, input_file, output_file, dest_mac_addr)
    except PermissionError as e:
        print(e)
        print(
            "Error: This script requires CAP_NET_RAW privileges to capture"
            "and relay raw Ethernet frames."
        )
    except KeyboardInterrupt:
        print("\nRelaying stopped.")
