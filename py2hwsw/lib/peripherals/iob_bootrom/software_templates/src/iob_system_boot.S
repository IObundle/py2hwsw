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

#ifdef IOB_SYSTEM_FENCEI
  // Ensure that instruction fetches after jump are synced with previous writes - uses RISC-V 'Zifencei' extension
  fence.i
#endif

  // Jump to the firmware
  li x5, IOB_SYSTEM_FW_BASEADDR
  jalr x0, 0(x5)
