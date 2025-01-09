/*
 * SPDX-FileCopyrightText: 2024 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_system_conf.h"
#include "iob_system_periphs.h"
#include "iob_system_system.h"
#include "iob_timer.h"
#include "iob_uart.h"
#include "printf.h"
#include <string.h>

// Enable debug messages.
#define DEBUG 0

int main() {
  int i;
  uint32_t file_size = 0;
  char c, buffer[2048];
  char pass_string[] = "Test passed!";
  char fail_string[] = "Test failed!";

  // init timer
  timer_init(TIMER0_BASE);

  // init uart
  uart_init(UART0_BASE, FREQ / BAUD);
  printf_init(&uart_putc);

  // test puts
  uart_puts("\n\n\nHello world from Tester!\n\n\n");

  //
  // Init SUT
  //

  uart_puts("[Tester]: Initializing SUT via UART...\n");

  // Init and switch to uart1 (connected to the SUT)
  uart_init(UART1_BASE, FREQ / BAUD);

  // Wait for ENQ signal from SUT
  while ((c = uart_getc()) != ENQ)
    if (DEBUG) {
      IOB_UART_INIT_BASEADDR(UART0_BASE);
      uart_putc(c);
      IOB_UART_INIT_BASEADDR(UART1_BASE);
    };

  // Send ack to sut
  uart_puts("\nTester ACK");

  IOB_UART_INIT_BASEADDR(UART0_BASE);
  uart_puts("[Tester]: Received SUT UART enquiry and sent acknowledge.\n");

  //
  // Read SUT messages
  //

  uart_puts("\n[Tester]: Reading SUT messages...\n");
  IOB_UART_INIT_BASEADDR(UART1_BASE);

  i = 0;
  // Read and store messages sent from SUT
  while ((c = uart_getc()) != EOT) {
    buffer[i] = c;
    if (DEBUG) {
      IOB_UART_INIT_BASEADDR(UART0_BASE);
      uart_putc(c);
      IOB_UART_INIT_BASEADDR(UART1_BASE);
    }
    i++;
  }
  buffer[i] = EOT;

  //
  // Print (stored) SUT messages
  //

  // Switch back to UART0
  IOB_UART_INIT_BASEADDR(UART0_BASE);

  // Send messages previously stored from SUT
  uart_puts("[Tester]: #### Messages received from SUT: ####\n\n");
  if (!DEBUG) {
    for (i = 0; buffer[i] != EOT; i++) {
      uart_putc(buffer[i]);
    }
  }
  uart_puts("\n[Tester]: #### End of messages received from SUT ####\n\n");

  //
  // End test
  //

  uart_sendfile("test.log", strlen(pass_string), pass_string);

  uart_finish();
}
