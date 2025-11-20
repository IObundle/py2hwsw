# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#include "iob_system_conf.h"
#include "iob_system_mmap.h"

// Bootloader stack address: at the end of the bootloader region == at the end of the firmware region
#define STACK_ADDR (IOB_SYSTEM_FW_BASEADDR + (1 << IOB_SYSTEM_FW_ADDR_W))

.section .init
.globl main

  //set stack pointer
  lui sp, %hi(STACK_ADDR)
  addi sp, sp, %lo(STACK_ADDR)

  //call main
  jal ra, main

  // Ensure write commits and invalidate the cache
  fence rw, rw
  fence.i

  // Jump to the firmware
  li x5, IOB_SYSTEM_FW_BASEADDR
  jalr x0, 0(x5)
