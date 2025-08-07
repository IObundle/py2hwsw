#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from sys import argv
import sys
import os


def print_usage():
    usage_str = """
Usage: ./makehex.py [--split] 1st_File 2nd_File 2nd_File_addr ... Firmware_Size output_file_name
The first file is the main file and its address is 0.
--split: Generate a separate hex file for each byte of memory words.
"""
    print(usage_str, file=sys.stderr)


def write_split_files(lines, output_file):
    """Split 4 byte words of single hex file contents into 4 separate hex files"""
    f0 = open(output_file + "_0.hex", "w")
    f1 = open(output_file + "_1.hex", "w")
    f2 = open(output_file + "_2.hex", "w")
    f3 = open(output_file + "_3.hex", "w")

    for line in lines:
        if line == "0\n":
            f3.write("0\n")
            f2.write("0\n")
            f1.write("0\n")
            f0.write("0\n")
        else:
            f3.write(line[0:2] + "\n")
            f2.write(line[2:4] + "\n")
            f1.write(line[4:6] + "\n")
            f0.write(line[6:8] + "\n")


def main():
    split_words = False
    if "--split" in argv:
        split_words = True
        argv.remove("--split")

    output_file = argv[-1]
    argv.remove(output_file)

    if len(argv) % 2 != 1:
        print("Error: number of arguments must be odd")
        print_usage()
        exit(1)
    nFiles = int((len(argv) - 3) / 2) + 1
    mem_size = 2 ** (int(argv[-1]))
    binfile = [argv[1]]
    binaddr = [0]
    bindata = []
    aux = []

    for i in range(nFiles - 1):
        binfile.append(argv[(i + 1) * 2])
        binaddr.append(int(argv[(i + 1) * 2 + 1], 16))

    for i in range(nFiles):
        with open(binfile[i], "rb") as f:
            bindata.append(f.read())
        aux.append(0)

    for i in range(nFiles):
        while len(bindata[i]) % 4 != 0:
            bindata[i] += b"0"

    for i in range(nFiles):
        assert binaddr[i] + len(bindata[i]) <= mem_size, (
            "File %d doesn't fit in memory" % i
        )
        assert (binaddr[i] + len(bindata[i])) % 4 == 0

    lines = []
    valid = False
    for i in range(int(mem_size / 4)):
        for j in range(nFiles):
            # If using the external memory than adress is 0x80..., but the place in the hex file sould not take into consideration the msb.
            aux[j] = i - int((binaddr[j] & ~(1 << 31)) / 4)
            if (aux[j] < (len(bindata[j]) / 4)) and (aux[j] >= 0):
                w = bindata[j]
                lines.append(
                    "%02x%02x%02x%02x\n"
                    % (
                        w[4 * aux[j] + 3],
                        w[4 * aux[j] + 2],
                        w[4 * aux[j] + 1],
                        w[4 * aux[j] + 0],
                    )
                )
                valid = True
                break
        if not valid:
            lines.append("00000000\n")
        valid = False

    if split_words:
        write_split_files(lines, os.path.splitext(output_file)[0])
    else:
        with open(output_file, "w") as f:
            f.writelines(lines)


main()
