/*
 * SPDX-FileCopyrightText: 2025 IObundle, Lda
 *
 * SPDX-License-Identifier: MIT
 *
 * Py2HWSW Version 0.81 has generated this code
 * (https://github.com/IObundle/py2hwsw).
 */

#include "iob_uart_csrs.h"

// Base Address
static uint32_t base;
void iob_uart_csrs_init_baseaddr(uint32_t addr) { base = addr; }

// Core Setters and Getters
void iob_uart_csrs_set_softreset(uint8_t value) {
  iob_write(base + IOB_UART_CSRS_SOFTRESET_ADDR, IOB_UART_CSRS_SOFTRESET_W,
            value);
}

void iob_uart_csrs_set_div(uint16_t value) {
  iob_write(base + IOB_UART_CSRS_DIV_ADDR, IOB_UART_CSRS_DIV_W, value);
}

void iob_uart_csrs_set_txdata(uint8_t value) {
  iob_write(base + IOB_UART_CSRS_TXDATA_ADDR, IOB_UART_CSRS_TXDATA_W, value);
}

void iob_uart_csrs_set_txen(uint8_t value) {
  iob_write(base + IOB_UART_CSRS_TXEN_ADDR, IOB_UART_CSRS_TXEN_W, value);
}

void iob_uart_csrs_set_rxen(uint8_t value) {
  iob_write(base + IOB_UART_CSRS_RXEN_ADDR, IOB_UART_CSRS_RXEN_W, value);
}

uint8_t iob_uart_csrs_get_txready() {
  return iob_read(base + IOB_UART_CSRS_TXREADY_ADDR, IOB_UART_CSRS_TXREADY_W);
}

uint8_t iob_uart_csrs_get_rxready() {
  return iob_read(base + IOB_UART_CSRS_RXREADY_ADDR, IOB_UART_CSRS_RXREADY_W);
}

uint8_t iob_uart_csrs_get_rxdata() {
  return iob_read(base + IOB_UART_CSRS_RXDATA_ADDR, IOB_UART_CSRS_RXDATA_W);
}

uint16_t iob_uart_csrs_get_version() {
  return iob_read(base + IOB_UART_CSRS_VERSION_ADDR, IOB_UART_CSRS_VERSION_W);
}
