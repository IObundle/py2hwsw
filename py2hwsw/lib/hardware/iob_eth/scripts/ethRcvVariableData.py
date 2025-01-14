"""ethRcvVariableData.py

Size of data to be received is unknown at the start.
"""

# Import libraries
from ethBase import CreateSocket, FormPacket, SyncAckLast, RcvAndAck
from ethRcvData import RcvFile
import sys
import struct


def RcvVariableFile(socket, output_filename):
    # Receive file size
    payload = RcvAndAck(socket)

    rcv_file_size = struct.unpack("<i", payload[0:4])[0]

    RcvFile(socket, output_filename, rcv_file_size)


if __name__ == "__main__":
    print("\nStarting file reception...")

    socket = CreateSocket()

    SyncAckLast(socket)
    RcvVariableFile(socket, sys.argv[3])
