/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_system_conf.h"
#include "iob_system_mmap.h"
#include "iob_uart.h"

#define PROGNAME "IOb-Bootloader"

//
// Trap handler
//

// Simple hex conversion for 32-bit integer into a buffer (without stdlib)
void uint32_to_hex_str(uint32_t value, char *buffer) {
  const char hex_chars[] = "0123456789ABCDEF";
  for (int i = 0; i < 8; i++) {
    buffer[7 - i] = hex_chars[value & 0xF];
    value >>= 4;
  }
  buffer[8] = '\0';
}

void trap_handler(void) {
  uint32_t mcause, mepc;

  asm volatile("csrr %0, mcause" : "=r"(mcause));
  asm volatile("csrr %0, mepc" : "=r"(mepc));

  // Buffers for printing
  char buffer[20];

  uart_puts("Trap occurred!\nMCause: 0x");
  uint32_to_hex_str(mcause, buffer);
  uart_puts(buffer);
  uart_puts("\nMEPC: 0x");
  uint32_to_hex_str(mepc, buffer);
  uart_puts(buffer);
  uart_puts("\n");

  asm volatile("ebreak"); // halt for debugger, optional
}

void set_trap_vector(void (*handler)(void)) {
  uintptr_t addr = (uintptr_t)handler;
  asm volatile("csrw mtvec, %0" : : "r"(addr));
}

//
// Main
//

int main() {

  // init uart
  uart_init(UART0_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);

  // connect with console
  do {
    if (iob_uart_csrs_get_txready())
      uart_putc((char)ENQ);
  } while (!iob_uart_csrs_get_rxready());

  set_trap_vector(trap_handler);

  // welcome message
  uart_puts(PROGNAME);
  uart_puts(": connected!\n");

#ifdef IOB_SYSTEM_USE_EXTMEM
  uart_puts(PROGNAME);
  uart_puts(": DDR in use.\n");
#endif

  // address to copy firmware to
  char *prog_start_addr = (char *)IOB_SYSTEM_FW_BASEADDR;

  while (uart_getc() != ACK) {
    uart_puts(PROGNAME);
    uart_puts(": Waiting for Console ACK.\n");
  }

#ifndef IOB_SYSTEM_INIT_MEM
  // receive firmware from host
  int file_size = 0;
  char r_fw[] = "iob_system_firmware.bin";
  file_size = uart_recvfile(r_fw, prog_start_addr);
  uart_puts(PROGNAME);
  uart_puts(": Loading firmware...\n");

  // sending firmware back for debug
  char s_fw[] = "s_fw.bin";

  if (file_size)
    uart_sendfile(s_fw, file_size, prog_start_addr);
  else {
    uart_puts(PROGNAME);
    uart_puts(": ERROR loading firmware\n");
  }
#endif

  // run firmware
  uart_puts(PROGNAME);
  uart_puts(": Restart CPU to run user program...\n");
  uart_txwait();
}
