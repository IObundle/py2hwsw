# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#include "iob_system_linux_conf.h"
#include "iob_system_linux_mmap.h"

#define STACK_ADDR (IOB_SYSTEM_LINUX_FW_BASEADDR + (1 << IOB_SYSTEM_LINUX_FW_ADDR_W))

.section .init
.globl _start
.type _start,@function

_start:
.option push
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
