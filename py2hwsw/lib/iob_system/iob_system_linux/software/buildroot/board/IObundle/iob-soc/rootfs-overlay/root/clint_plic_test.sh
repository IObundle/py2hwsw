#!/bin/sh

# SPDX-FileCopyrightText: 2026 IObundle, Lda
#
# SPDX-License-Identifier: MIT
#
# Py2HWSW Version 0.81.0 has generated this code (https://github.com/IObundle/py2hwsw).

echo "Verify that CLINT (RISC-V timer) interrupts triggered (interrupt count > 0)"

CLINT_COUNT=$(cat /proc/interrupts | awk '/RISC-V INTC/ && /riscv-timer/ {for(i=2; i<NF; i++) sum += $i; print sum+0}')
if [ "$CLINT_COUNT" -gt 0 ]; then
    echo "CLINT: PASS (count: $CLINT_COUNT)"
else
    echo "CLINT: FAIL (count: $CLINT_COUNT)"
fi

echo "Verify that PLIC (SiFive) interrupts triggered (interrupt count > 0)"

PLIC_COUNT=$(cat /proc/interrupts | awk '/SiFive PLIC/ && /iob_timer/ {for(i=2; i<NF; i++) sum += $i; print sum+0}')
if [ "$PLIC_COUNT" -gt 0 ]; then
    echo "PLIC: PASS (count: $PLIC_COUNT)"
else
    echo "PLIC: FAIL (count: $PLIC_COUNT)"
fi

echo "CLINT and PLIC test passed!"
