/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

SECTIONS {
  /* Program code */
  INCLUDE auto_iob_system_firmware.lds
  .init : { *(.init) }
  .text : { *(.text) }

  .memory : {
    /* Read-only data */
    *(.rodata);

    /* Initialized data */
    *(.data);
    . = ALIGN(4);
    /* Define the global pointer symbol 2048 bytes (0x800) into the data 
       section. This allows reaching the start of data with a single 
       12-bit signed offset (-2048 to +2047). */
    PROVIDE(__global_pointer$ = . + 0x800);

    /* Uninitialized data */
    *(.bss);

    /* Any symbols not explicitly mentioned in previous sections are included in this section */
    *(*);
  }

  /* Stack */
  stack_start = .;
  .stack : { *(.stack) }
  stack_end = .;

  . = ALIGN(4);
  _heap_start = .;
  end = .;
}
