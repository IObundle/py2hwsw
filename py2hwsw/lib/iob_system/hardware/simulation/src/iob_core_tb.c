/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_system_conf.h"
#include "iob_uart_csrs.h"
#include <stdio.h>
#include <stdlib.h>

#define FREQ 100000000
#define BAUD 3000000

#ifdef IOB_SYSTEM_USE_ETHERNET
#include "iob_eth_driver_tb.h"
#endif

int iob_core_tb() {

  // print welcome message
  printf("IOB SYSTEM testbench\n");

  // UART init
  //  disable TX and RX
  IOB_UART_SET_TXEN(0);
  IOB_UART_SET_RXEN(0);

  // set the divisor
  int div = FREQ / BAUD;
  IOB_UART_SET_DIV(div);
  printf("Baud rate set to %d\n", BAUD);

  // pulse soft reset
  IOB_UART_SET_SOFTRESET(1);
  IOB_UART_SET_SOFTRESET(0);

  // enable RX
  IOB_UART_SET_RXEN(1);

  unsigned int version;

  // read version 20 times to burn time
  for (int i = 0; i < 20; i++) {
    version = IOB_UART_GET_VERSION();
  }
  printf("Version is %d\n", version);

  // enable TX
  IOB_UART_SET_TXEN(1);
  printf("TX and RX enabled\n");

  ///////////////////////////////////////////////////////////////

  FILE *soc2cnsl_fd;
  FILE *cnsl2soc_fd;
  char cpu_char = 0;
  char rxread_reg = 0, txread_reg = 0;
  int able2write = 0, able2read = 0;

  while ((cnsl2soc_fd = fopen("./cnsl2soc", "rb")) == NULL)
    ;

  printf("cnsl2soc opened\n");

  fclose(cnsl2soc_fd);
  soc2cnsl_fd = fopen("./soc2cnsl", "wb");

#ifdef IOB_SYSTEM_USE_ETHERNET
  eth_setup(&eth_if);
#endif

  while (1) {
    while (!rxread_reg && !txread_reg) {
      rxread_reg = IOB_UART_GET_RXREADY();
      txread_reg = IOB_UART_GET_TXREADY();
    }

    if (rxread_reg) {
      cpu_char = IOB_UART_GET_RXDATA();
      fwrite(&cpu_char, sizeof(char), 1, soc2cnsl_fd);
      fflush(soc2cnsl_fd);
      rxread_reg = 0;
    }
    if (txread_reg) {
      if ((cnsl2soc_fd = fopen("./cnsl2soc", "rb")) == NULL) {
        fclose(soc2cnsl_fd);
        break;
      }
      able2write = fread(&cpu_char, sizeof(char), 1, cnsl2soc_fd);
      if (able2write > 0) {
        IOB_UART_SET_TXDATA(cpu_char);
        fclose(cnsl2soc_fd);
        cnsl2soc_fd = fopen("./cnsl2soc", "w");
      }
      fclose(cnsl2soc_fd);
      txread_reg = 0;
    }

#ifdef IOB_SYSTEM_USE_ETHERNET
    eth_relay_frames(&eth_if);
#endif
  }

  return 0;
}
