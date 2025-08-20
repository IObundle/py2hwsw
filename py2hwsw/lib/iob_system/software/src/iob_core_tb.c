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
#define UART0_BASE 0x0

#ifdef IOB_SYSTEM_USE_ETHERNET
#include "iob_eth_tb_driver.h"
// Configure testbench memory map
#define ETH0_BASE 0x40000000
#define ETH0_RAM_BASE 0x80000000
#endif

int iob_core_tb() {

  // print welcome message
  printf("IOB SYSTEM testbench\n");

  // UART init
  iob_uart_csrs_init_baseaddr(UART0_BASE);
  //  disable TX and RX
  iob_uart_csrs_set_txen(0);
  iob_uart_csrs_set_rxen(0);

  // set the divisor
  int div = FREQ / BAUD;
  iob_uart_csrs_set_div(div);
  printf("Baud rate set to %d\n", BAUD);

  // pulse soft reset
  iob_uart_csrs_set_softreset(1);
  iob_uart_csrs_set_softreset(0);

  // enable RX
  iob_uart_csrs_set_rxen(1);

  unsigned int version;

  // read version 20 times to burn time
  int i;
  for (i = 0; i < 20; i++) {
    version = iob_uart_csrs_get_version();
  }
  printf("Version is %d\n", version);

  // enable TX
  iob_uart_csrs_set_txen(1);
  printf("TX and RX enabled\n");

  ///////////////////////////////////////////////////////////////

  FILE *soc2cnsl_fd;
  FILE *cnsl2soc_fd;
  char cpu_char = 0;
  int able2write = 0, able2read = 0;

  while ((cnsl2soc_fd = fopen("./cnsl2soc", "rb")) == NULL)
    ;

  printf("cnsl2soc opened\n");

  fclose(cnsl2soc_fd);
  soc2cnsl_fd = fopen("./soc2cnsl", "wb");

#ifdef IOB_SYSTEM_USE_ETHERNET
  eth_setup(ETH0_BASE);
#endif

  while (1) {
    if (iob_uart_csrs_get_rxready()) {
      //      printf("RX ready\n");
      cpu_char = iob_uart_csrs_get_rxdata();
      fwrite(&cpu_char, sizeof(char), 1, soc2cnsl_fd);
      fflush(soc2cnsl_fd);
    }
    if (iob_uart_csrs_get_txready()) {
      if ((cnsl2soc_fd = fopen("./cnsl2soc", "rb")) == NULL) {
        fclose(soc2cnsl_fd);
        break;
      }
      able2write = fread(&cpu_char, sizeof(char), 1, cnsl2soc_fd);
      if (able2write > 0) {
        iob_uart_csrs_set_txdata(cpu_char);
        fclose(cnsl2soc_fd);
        cnsl2soc_fd = fopen("./cnsl2soc", "w");
      }
      fclose(cnsl2soc_fd);
    }

#ifdef IOB_SYSTEM_USE_ETHERNET
    eth_relay_frames();
#endif
  }

  // TODO: Return code based on test result (pass/fail)
  return 0;
}
