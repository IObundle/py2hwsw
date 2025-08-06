#!/bin/sh 

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


insmod versat.ko

# 3000 per block, 12000 total
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\060" > small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\061" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\062" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\063" >> small.txt

dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\064" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\065" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\066" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\067" >> small.txt

dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\067" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\070" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\071" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\072" >> small.txt

dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\073" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\074" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\075" >> small.txt
dd if=/dev/zero bs=750 count=1 2> /dev/null | tr "\000" "\076" >> small.txt

# 12000 * 8 = 96000
cat small.txt > medium.txt
cat small.txt >> medium.txt
cat small.txt >> medium.txt
cat small.txt >> medium.txt
cat small.txt >> medium.txt
cat small.txt >> medium.txt
cat small.txt >> medium.txt
cat small.txt >> medium.txt

# 96000 * 8 = 768000
cat medium.txt > large.txt
cat medium.txt >> large.txt
cat medium.txt >> large.txt
cat medium.txt >> large.txt
cat medium.txt >> large.txt
cat medium.txt >> large.txt
cat medium.txt >> large.txt
cat medium.txt >> large.txt

