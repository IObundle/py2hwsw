"""ethRcvData.py

Size of data to be received is known at the start.
"""

# Import libraries
from ethBase import (
    PrintBaseUsage,
    TimedPrintProgress,
    CreateSocket,
    FormPacket,
    SyncAckLast,
    RcvAndAck,
    ETH_NBYTES,
)
from os.path import getsize
import sys
import struct
import time


def RcvFile(socket, output_filename, expected_size):
    if expected_size == 0:
        print("Expected size is zero. Check if parameters are correct")
        return

    # Frame parameters
    num_frames = ((expected_size - 1) // ETH_NBYTES) + 1
    print("file_size: %d" % expected_size)
    print("num_frames: %d" % num_frames)

    # Open output file
    f_output = open(output_filename, "wb")

    # Reset byte counter
    count_bytes = 0

    # Loop to send input frames
    for j in range(num_frames):
        TimedPrintProgress(j, num_frames - 1)

        # receive data
        payload = RcvAndAck(socket)

        # Write into file
        f_output.write(payload)

        # accumulate sent bytes
        count_bytes += len(payload)

    if count_bytes != expected_size:
        print(
            "Error, bytes received (%d) is different than expected (%d)"
            % (count_bytes, expected_size)
        )

    # Close file
    f_output.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        PrintBaseUsage()
        print("<expected size>")
        sys.exit()

    print("\nStarting file reception...")

    socket = CreateSocket()

    SyncAckLast(socket)
    RcvFile(socket, sys.argv[3], int(sys.argv[4]))
