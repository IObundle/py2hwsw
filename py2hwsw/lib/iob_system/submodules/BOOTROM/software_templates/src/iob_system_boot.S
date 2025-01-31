# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

#include "iob_system_conf.h"
#include "iob_system_periphs.h"
#include "iob_system_system.h"

.section .init
.globl main

  //set stack pointer
  lui sp, %hi(1 << IOB_SYSTEM_FW_ADDR_W)
  addi sp, sp, %lo(1 << IOB_SYSTEM_FW_ADDR_W)

  //call main
  jal ra, main

  // Jump to the firmware
  li x5, IOB_SYSTEM_FW_BASEADDR
  jalr x0, 0(x5)
