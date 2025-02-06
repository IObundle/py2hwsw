#include "iob_bsp.h"
#include "iob_uart_csrs.h"
#include <stdio.h>

void iob_arst_pulse();

int iob_uart_tb() {

  int failed = 0;

  // print welcome message
  printf("IOB UART testbench\n");

  // issue a hard async reset to the DUT
  iob_arst_pulse();

  // print the reset message
  printf("Reset complete\n");

  // hold soft reset low
  IOB_UART_SET_SOFTRESET(0);

  // print the soft reset message
  printf("Soft reset complete\n");

  // disable TX and RX
  IOB_UART_SET_TXEN(0);
  IOB_UART_SET_RXEN(0);

  // set the divisor
  IOB_UART_SET_DIV(FREQ / BAUD);

  // print the baud rate
  printf("Baud rate set to %d\n", BAUD);

  // assert tx and rx not ready
  uint8_t tx_ready = IOB_UART_GET_TXREADY();
  if (tx_ready != 0) {
    printf("Error: TX ready initially");
    failed = 1;
  }
  printf("TX ready initially\n");

  uint8_t rx_ready = IOB_UART_GET_RXREADY();
  if (rx_ready != 0) {
    printf("Error: RX ready initially");
    failed = 1;
  }

  // pulse soft reset
  IOB_UART_SET_SOFTRESET(1);
  IOB_UART_SET_SOFTRESET(0);

  // enable RX and TX
  IOB_UART_SET_RXEN(1);
  IOB_UART_SET_TXEN(1);

  // open test log file
  FILE *log = fopen("test.log", "w");

  // data send/receive loop
  for (int i = 0; i < 256; i++) {
    // wait for tx ready
    while (!IOB_UART_GET_TXREADY())
      ;

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
  if (failed != 0) {
    fprintf(log, "Test failed!");
  } else {
    fprintf(log, "Test passed!");
  }
  fclose(log);
  return failed;
}
