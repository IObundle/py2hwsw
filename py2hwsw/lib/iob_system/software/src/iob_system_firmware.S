# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#include "iob_system_conf.h"
#include "iob_system_mmap.h"

#define STACK_ADDR (IOB_SYSTEM_FW_BASEADDR + (1 << IOB_SYSTEM_FW_ADDR_W))

.section .init
.globl main
.align 2

  // Set global pointer (gp) to speed up global variable access.
  // We use '.option push/pop' to isolate the 'norelax' setting.
  .option push
  // Disable 'relaxation' to prevent the linker from making this 
  // instruction relative to 'gp' itself before it is initialized.
  .option norelax
  la gp, __global_pointer$
  .option pop

  //set stack pointer
  lui sp, %hi(STACK_ADDR)
  addi sp, sp, %lo(STACK_ADDR)

  //call main
  jal ra, main

  // Stop the processor
  ebreak
