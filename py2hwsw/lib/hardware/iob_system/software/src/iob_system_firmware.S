# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

#include "iob_system_conf.h"
#include "iob_system_periphs.h"
#include "iob_system_system.h"

#define STACK_ADDR (IOB_SYSTEM_FW_ADDR + (1 << IOB_SYSTEM_FW_ADDR_W))

.section .init
.globl main

  //set stack pointer
  lui sp, %hi(STACK_ADDR)
  addi sp, sp, %lo(STACK_ADDR)

  //call main
  jal ra, main

  // Jump to the pre-bootloader
  li x5, 0x80000000
  jalr x0, 0(x5)
