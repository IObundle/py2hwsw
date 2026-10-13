# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#include "iob_system_linux_conf.h"
#include "iob_system_linux_mmap.h"
#include "iob_cpu.s"

// Bootloader stack address: at the end of the bootloader region == at the end of the firmware region
#define STACK_ADDR (IOB_SYSTEM_LINUX_FW_BASEADDR + (1 << IOB_SYSTEM_LINUX_FW_ADDR_W))

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

  // Set up OpenSBI entry arguments (must be here, not in C code, to avoid
  // clobbering by function calls)
  li a0, 0                   // Hart ID (single-core)
  li a1, 0x00F80000          // DTB address
  li a2, 0
  li a3, 0
  li a4, 0
  li a5, 0
  li a6, 0
  li a7, 0

  // Jump to the firmware
  li x5, IOB_SYSTEM_LINUX_FW_BASEADDR
  jalr x0, 0(x5)