/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_uart_csrs.h"
#include <stdio.h>

int iob_core_tb() {

  int failed = 0;

  // print welcome message
  printf("IOB UART testbench\n");

  // print the reset message
  printf("Reset complete\n");

  // hold soft reset low
  IOB_UART_SET_SOFTRESET(0);

  // print the soft reset message
  printf("Soft reset set to 0\n");

  // disable TX and RX

  IOB_UART_SET_TXEN(0);
  IOB_UART_SET_RXEN(0);

  // set the divisor

  int div = FREQ / BAUD;
  IOB_UART_SET_DIV(div);

  // print the baud rate
  printf("Baud rate set to %d\n", BAUD);

  // assert tx and rx not ready
  uint8_t tx_ready = IOB_UART_GET_TXREADY();
  if (tx_ready != 0) {
    printf("Error: TX ready initially\n");
    failed = 1;
  }

  uint8_t rx_ready = IOB_UART_GET_RXREADY();
  if (rx_ready != 0) {
    printf("Error: RX ready initially");
    failed = 1;
  }

  printf("TX and RX ready deasserted\n");

  // pulse soft reset
  IOB_UART_SET_SOFTRESET(1);
  IOB_UART_SET_SOFTRESET(0);

  // enable RX and TX
  IOB_UART_SET_RXEN(1);
  IOB_UART_SET_TXEN(1);

  printf("TX and RX enabled\n");

  // data send/receive loop
  for (int i = 0; i < 256; i++) {
    // wait for tx ready
    while (!IOB_UART_GET_TXREADY())
      ;

    printf("TX ready asserted\n");

    // write word to send
    IOB_UART_SET_TXDATA(i);
    // wait for rx ready
    while (!IOB_UART_GET_RXREADY())
      ;

    // read received word
    uint8_t rx_data = IOB_UART_GET_RXDATA();

    // check if received word is the same as sent word
    if (rx_data != i) {
      // signal error printing expected and received word
      printf("Error: expected %d, received %d\n", i, rx_data);
      failed += 1;
    }
  }

  return failed;
}
