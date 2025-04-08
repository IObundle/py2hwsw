/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_uart_csrs.h"
#include <stdio.h>

#define FREQ 100000000
#define BAUD 3000000

int iob_core_tb() {

  int failed = 0;

  // print welcome message
  printf("IOB UART testbench\n");

  // print the reset message
  printf("Reset complete\n");

  // hold soft reset low
  iob_uart_csrs_set_softreset(0);

  // print the soft reset message
  printf("Soft reset set to 0\n");

  // disable TX and RX

  iob_uart_csrs_set_txen(0);
  iob_uart_csrs_set_rxen(0);

  // set the divisor

  int div = FREQ / BAUD;
  iob_uart_csrs_set_div(div);

  // print the baud rate
  printf("Baud rate set to %d\n", BAUD);

  // assert tx and rx not ready
  uint8_t tx_ready = iob_uart_csrs_get_txready();
  if (tx_ready != 0) {
    printf("Error: TX ready initially\n");
    failed = 1;
  }

  uint8_t rx_ready = iob_uart_csrs_get_rxready();
  if (rx_ready != 0) {
    printf("Error: RX ready initially");
    failed = 1;
  }

  printf("TX and RX ready deasserted\n");

  // pulse soft reset
  iob_uart_csrs_set_softreset(1);
  iob_uart_csrs_set_softreset(0);

  // enable RX
  iob_uart_csrs_set_rxen(1);

  unsigned int version;
  int i;
  // read version 20 times to burn time
  for (i = 0; i < 20; i++) {
    version = iob_uart_csrs_get_version();
  }
  printf("Version is %d\n", version);

  // enable TX
  iob_uart_csrs_set_txen(1);

  printf("TX and RX enabled\n");

  // data send/receive loop
  printf("Starting data send/receive loop\n");
  for (i = 0; i < 4; i++) {
    // wait for tx ready
    while (!iob_uart_csrs_get_txready())
      ;

    // write word to send
    iob_uart_csrs_set_txdata(i);
    // wait for rx ready
    while (!iob_uart_csrs_get_rxready())
      ;

    // read received word
    uint8_t rx_data = iob_uart_csrs_get_rxdata();

    // check if received word is the same as sent word
    if (rx_data != i) {
      // signal error printing expected and received word
      printf("Error: expected %d, received %d\n", i, rx_data);
      failed += 1;
    }
  }
  printf("Data send/receive loop complete\n");
  return failed;
}
