# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

#include "iob_system_conf.h"
#include "iob_system_mmap.h"
#include "iob_cpu.s"

// Can't include iob_bootrom_csrs.h because the assembler doesn't recognize stdint.h,
// so define the constants here instead (these are address offsets).

// Bootloader start address within the ROM
#define IOB_BOOTROM_ROM_ADDR IOB_SYSTEM_BOOTLOADER_ROM_OFFSET
// Bootloader size
#define LENGTH ((1 << IOB_SYSTEM_BOOTROM_ADDR_W) - IOB_BOOTROM_ROM_ADDR)
// Bootloader start address in system's memory map
#define BOOTROM (BOOTROM_BASE + IOB_BOOTROM_ROM_ADDR)

// Destination address for the bootloader: at the last addresses of the firmware region
#define BOOTLDR_ADDR ((IOB_SYSTEM_FW_BASEADDR + (1 << IOB_SYSTEM_FW_ADDR_W)) - (1 << IOB_SYSTEM_BOOTROM_ADDR_W))

.section .init
.globl _start

_start:
  li x1, LENGTH
  li x2, BOOTROM
  li x3, BOOTLDR_ADDR

copy_loop:
  lw x4, 0(x2)
  sw x4, 0(x3)
  addi x2, x2, 4
  addi x3, x3, 4
  addi x1, x1, -4
  bne x1, x0, copy_loop

  // The bootloader was stored through the data cache: write it back to memory
  // before the instruction cache fetches it
  iob_cpu_flush_dcache
  iob_cpu_invalidate_icache

  // Jump to the bootloader
  li x5, BOOTLDR_ADDR
  jalr x0, 0(x5)
