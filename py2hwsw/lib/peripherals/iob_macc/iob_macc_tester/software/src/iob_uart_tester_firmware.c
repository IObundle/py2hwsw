/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_uart.h"
#include "iob_uart_tester_conf.h"
#include "iob_uart_tester_mmap.h"
#include <string.h>

int main() {
  char pass_string[] = "Test passed!";
  char fail_string[] = "Test failed!";

  // init uart
  uart_init(UART0_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);

  // Initial Tester message
  uart_puts("\nHello world from Tester of 'iob_uart' core!\n\n\n");

  uart_puts("Verification of 'iob_uart' successful!\n\n");

  //
  // End test
  //

  uart_sendfile("test.log", strlen(pass_string), pass_string);

  uart_finish();
}
