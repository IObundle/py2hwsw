"""ethSendData.py

Size of data transfered is known by destination address.
"""

# Import libraries
from ethBase import (
    TimedPrintProgress,
    CreateSocket,
    SendAndAck,
    SyncAckFirst,
    ETH_NBYTES,
)
from os.path import getsize
import sys


def SendFile(socket, input_filename):
    # Open input file
    f_input = open(input_filename, "rb")

    # Frame parameters
    input_file_size = getsize(input_filename)
    if input_file_size == 0:
        print("File is empty. Check if filepath is correct")
        return 0

    num_frames_input = ((input_file_size - 1) // ETH_NBYTES) + 1
    print("input_file_size: %d" % input_file_size)
    print("num_frames_input: %d" % num_frames_input)

    # Reset byte counter
    count_bytes = 0
    count_errors = 0

    # Loop to send input frames
    for j in range(num_frames_input):
        TimedPrintProgress(j, num_frames_input - 1)

        # check if it is last packet (not enough for full payload)
        if j == (num_frames_input - 1):
            bytes_to_send = input_file_size - count_bytes
        else:
            bytes_to_send = ETH_NBYTES

        # form frame
        payload = f_input.read(bytes_to_send)

        # accumulate sent bytes
        count_bytes += ETH_NBYTES

        count_errors += SendAndAck(socket, payload)

    # Close file
    f_input.close()
    print("\n\nFile transmitted with %d errors..." % (count_errors))


if __name__ == "__main__":
    print("\nStarting file transmission...")

    socket = CreateSocket()

    SyncAckFirst(socket)
    SendFile(socket, sys.argv[3])
