# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

#include "iob_system_conf.h"
#include "iob_system_mmap.h"

.section .init
.globl main

  //set stack pointer
  lui sp, %hi(1 << IOB_SYSTEM_FW_ADDR_W)
  addi sp, sp, %lo(1 << IOB_SYSTEM_FW_ADDR_W)

  //call main
  jal ra, main

  // Stop the processor
  ebreak
