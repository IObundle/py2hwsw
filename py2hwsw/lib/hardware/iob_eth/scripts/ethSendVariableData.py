"""ethSendVariableData.py

Size of data transfered is not known by destination address.
"""

# Import libraries
from ethBase import CreateSocket, SendAndAck, SyncAckFirst
from ethSendData import SendFile
from os.path import getsize
import sys
import struct


def SendVariableFile(socket, input_filename):
    input_file_size = getsize(input_filename)

    print("Size: %d " % input_file_size)

    errors = SendAndAck(socket, struct.pack("<i", input_file_size))

    if errors:
        print("Error sending file size")

    SendFile(socket, input_filename)


if __name__ == "__main__":
    print("\nStarting file transmission...")

    socket = CreateSocket()

    SyncAckFirst(socket)
    SendVariableFile(socket, sys.argv[3])
