#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import termios

print("IOb-TerminalMode: inverting terminal canonical and echo mode")

stdin = sys.stdin
fd = stdin.fileno()

old = termios.tcgetattr(fd)
new = termios.tcgetattr(fd)
new[3] &= ~termios.ECHO
new[3] &= ~termios.ICANON

termios.tcsetattr(fd, termios.TCSAFLUSH, new)
