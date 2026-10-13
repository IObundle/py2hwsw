# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

#include "iob_system_conf.h"
#include "iob_system_mmap.h"
#include "iob_cpu.s"

// Bootloader stack address: at the end of the bootloader region == at the end of the firmware region
#define STACK_ADDR (IOB_SYSTEM_FW_BASEADDR + (1 << IOB_SYSTEM_FW_ADDR_W))

.section .init
.globl main

  //set stack pointer
  lui sp, %hi(STACK_ADDR)
  addi sp, sp, %lo(STACK_ADDR)

  //call main
  jal ra, main

  // The firmware was stored through the data cache: write it back to memory
  // before the instruction cache fetches it
  iob_cpu_flush_dcache
  iob_cpu_invalidate_icache

  // Jump to the firmware
  li x5, IOB_SYSTEM_FW_BASEADDR
  jalr x0, 0(x5)