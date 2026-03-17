#!/bin/sh
echo === Interrupt Test ===
echo CLINT Timer: $(cat /proc/interrupts | grep timer | awk '{print $2}')
echo PLIC Contexts: $(dmesg | grep plic | grep contexts)
echo Total IRQs: $(wc -l < /proc/interrupts)
echo Uptime: $(uptime)
