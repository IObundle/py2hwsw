#!/usr/bin/env python3

"""
example_python.py
Python script to send input data and receive output data.
This script performs the following sequence of transfers:
  (Host PC) <- (FPGA Board): receive data [known size before runtime]
  (Host PC) <- (FPGA Board): receive variable data [unknown size before runtime]
  (Host PC) -> (FPGA Board): send data [known size before runtime]
  (Host PC) -> (FPGA Board): send variable data [known size before runtime]
test
"""

# Import Ethernet package
import sys

sys.path.append("../../")
from submodules.ETHERNET.software.python.ethBase import (
    CreateSocket,
    SyncAckFirst,
    SyncAckLast,
)
from submodules.ETHERNET.software.python.ethRcvData import RcvFile
from submodules.ETHERNET.software.python.ethRcvVariableData import RcvVariableFile
from submodules.ETHERNET.software.python.ethSendData import SendFile
from submodules.ETHERNET.software.python.ethSendVariableData import SendVariableFile

if __name__ == "__main__":
    print("\nIOb-Ethernet Example Python\n")

    # Check input arguments
    if len(sys.argv) != 6:
        print(
            f"Usage: ./{sys.argv[0]} [RMAC_INTERFACE] [RMAC] [output.bin] [output.bin_size] [variable_output.bin]"
        )
        quit()
    else:
        rcv_file = sys.argv[3]
        rcv_file_size = int(sys.argv[4])
        rcv_file_var = sys.argv[5]

    socket = CreateSocket()

    # Receive Data File
    print("\nReceiving data...")
    SyncAckLast(socket)
    RcvFile(socket, rcv_file, rcv_file_size)
    print("done!")

    # Receive Variable Data File
    print("\nReceiving variable data...")
    SyncAckLast(socket)
    RcvVariableFile(socket, rcv_file_var)
    print("done!")

    # Send Data File
    # Send back received file
    send_file = rcv_file
    print("\nSending data...")
    SyncAckFirst(socket)
    SendFile(socket, send_file)
    print("done!")

    # Send Variable Data File
    # Send back received file
    send_file_var = rcv_file_var
    print("\nSending variable data...")
    SyncAckFirst(socket)
    SendVariableFile(socket, send_file_var)
    print("done!")

    # Close Socket
    socket.close()
