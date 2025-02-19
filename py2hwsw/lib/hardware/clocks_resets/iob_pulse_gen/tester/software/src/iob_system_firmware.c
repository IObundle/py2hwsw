/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_gpio_csrs.h"
#include "iob_printf.h"
#include "iob_system_conf.h"
#include "iob_system_mmap.h"
#include "iob_timer.h"
#include "iob_uart.h"
#include <string.h>

// Enable debug messages.
#define DEBUG 0

int main() {
  int i;
  uint32_t file_size = 0;
  char c, buffer[2048];
  char pass_string[] = "Test passed!";
  char fail_string[] = "Test failed!";
  uint32_t gpio_output;

  // init timer
  timer_init(TIMER0_BASE);

  // init gpio
  IOB_GPIO_INIT_BASEADDR(GPIO0_BASE);

  // init uart
  uart_init(UART0_BASE, FREQ / BAUD);
  printf_init(&uart_putc);

  // test puts
  uart_puts("\n\n\nHello world from 'iob_pulse_gen' Tester!\n\n\n");

  // Check that output of iob_pulse_gen is zero
  gpio_output = IOB_GPIO_GET_INPUT_0();
  if (gpio_output != 0) {
    uart_puts("ERROR: Initial output of iob_pulse_gen is non-zero!\n");
    uart_finish();
    return 1;
  }

  // Toggle enable of iob_pulse_gen
  IOB_GPIO_SET_OUTPUT_0(1);
  IOB_GPIO_SET_OUTPUT_0(0);

  // Check that output of iob_pulse_gen is enabled
  // NOTE: GPIO is not the best verification tool for iob_pulse_gen, since it is
  // not very precise in the timing for sampling its output. Ideally we should
  // use a dedicated verification tool that measures the timing of the output of
  // iob_pulse_gen.
  gpio_output = IOB_GPIO_GET_INPUT_0();
  if (gpio_output != 1) {
    uart_puts("ERROR: iob_pulse_gen did not generate output!\n");
    uart_finish();
    return 1;
  }

  uart_puts("Test passed!\n");

  //
  // End test
  //

  uart_sendfile("test.log", strlen(pass_string), pass_string);

  uart_finish();
}
