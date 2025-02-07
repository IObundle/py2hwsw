#include "iob_bsp.h"
#include "iob_tasks.h"
#include "iob_uart_csrs.h"
#include <stdio.h>

extern iob_native_t uart_if;

int iob_uart_core_tb() {

  int failed = 0;

  // print welcome message
  printf("IOB UART testbench\n");

  // print the reset message
  printf("Reset complete\n");

  // hold soft reset low
  IOB_UART_SET_SOFTRESET(0, &uart_if);

  // print the soft reset message
  printf("Soft reset complete\n");

  // disable TX and RX

  // IOB_UART_SET_TXEN(0, &uart_if);
  // IOB_UART_SET_RXEN(0, &uart_if);
  iob_write(IOB_UART_TXEN_ADDR, 1, IOB_UART_TXEN_W / 8 + IOB_UART_TXEN_W % 8,
            &uart_if);
  iob_write(IOB_UART_RXEN_ADDR, 1, IOB_UART_RXEN_W / 8 + IOB_UART_RXEN_W % 8,
            &uart_if);

  return failed;

  // set the divisor
  IOB_UART_SET_DIV(FREQ / BAUD, &uart_if);

  // print the baud rate
  printf("Baud rate set to %d\n", BAUD);

  // assert tx and rx not ready
  uint8_t tx_ready = IOB_UART_GET_TXREADY(&uart_if);
  if (tx_ready != 0) {
    printf("Error: TX ready initially\n");
    failed = 1;
  }

  uint8_t rx_ready = IOB_UART_GET_RXREADY(&uart_if);
  if (rx_ready != 0) {
    printf("Error: RX ready initially");
    failed = 1;
  }

  printf("TX and RX ready deasserted\n");

  // pulse soft reset
  IOB_UART_SET_SOFTRESET(1, &uart_if);
  IOB_UART_SET_SOFTRESET(0, &uart_if);

  // enable RX and TX
  IOB_UART_SET_RXEN(1, &uart_if);
  IOB_UART_SET_TXEN(1, &uart_if);

  printf("TX and RX enabled\n");

  // data send/receive loop
  for (int i = 0; i < 256; i++) {
    // wait for tx ready
    while (!IOB_UART_GET_TXREADY(&uart_if))
      ;

    printf("TX ready asserted\n");

    // write word to send
    IOB_UART_SET_TXDATA(i, &uart_if);

    // wait for rx ready
    while (!IOB_UART_GET_RXREADY(&uart_if))
      ;

    // read received word
    uint8_t rx_data = IOB_UART_GET_RXDATA(&uart_if);

    // check if received word is the same as sent word
    if (rx_data != i) {
      // signal error printing expected and received word
      printf("Error: expected %d, received %d\n", i, rx_data);
      failed += 1;
    }
  }

  return failed;
}
