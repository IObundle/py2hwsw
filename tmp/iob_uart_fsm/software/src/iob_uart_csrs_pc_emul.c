/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

/* PC Emulation of UART peripheral */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "iob_uart_csrs.h"

static uint16_t div_value;

static FILE *cnsl2soc_fd;
static FILE *soc2cnsl_fd;

void pc_emul_error(char *s) {
  printf("ERROR in iob-uart PC emulation: %s", s);
  exit(1);
}

static int base;
void iob_uart_csrs_init_baseaddr(uint32_t addr) {

  // wait for console to create communication files
  while ((cnsl2soc_fd = fopen("./cnsl2soc", "rb")) == NULL)
    ;
  fclose(cnsl2soc_fd);
  soc2cnsl_fd = fopen("./soc2cnsl", "wb");

  base = addr;
  return;
}

void iob_uart_csrs_set_softreset(uint8_t value) {
  div_value = 0;
  return;
}

void iob_uart_csrs_set_div(uint16_t value) {
  div_value = value;
  return;
}

void iob_uart_csrs_set_txdata(uint8_t value) {
  // send byte to console
  char aux_char;
  int nbytes;

  fwrite(&value, sizeof(char), 1, soc2cnsl_fd);
  fflush(soc2cnsl_fd);
}

void iob_uart_csrs_set_txen(uint8_t value) { return; }

void iob_uart_csrs_set_rxen(uint8_t value) { return; }

uint8_t iob_uart_csrs_get_txready() { return 1; }

uint8_t iob_uart_csrs_get_rxdata() {
  // get byte from console
  uint8_t c;
  int nbytes;

  while (1) {
    cnsl2soc_fd = fopen("./cnsl2soc", "rb");
    if (!cnsl2soc_fd)
      fclose(soc2cnsl_fd);

    nbytes = fread(&c, sizeof(char), 1, cnsl2soc_fd);
    if (nbytes == 1) {
      fclose(cnsl2soc_fd);

      // the following removes file contents
      cnsl2soc_fd = fopen("./cnsl2soc", "wb");
      fclose(cnsl2soc_fd);

      break;
    }
    fclose(cnsl2soc_fd);
  }
  return c;
}

uint8_t iob_uart_csrs_get_rxready() { return 1; }
