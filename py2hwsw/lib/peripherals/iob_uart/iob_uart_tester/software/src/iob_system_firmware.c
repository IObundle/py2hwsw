/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_printf.h"
#include "iob_system_conf.h"
#include "iob_system_mmap.h"
#include "iob_uart.h"
#include <string.h>

int main() {
  uart_init(UART0_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);
  uart_puts("\nHello from iob_uart's Tester!\n\n\n");
  uart_finish();
}
