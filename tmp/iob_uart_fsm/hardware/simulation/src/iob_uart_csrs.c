/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_uart_csrs.h"

int base_uart = -1;

// Core Setters and Getters
void iob_uart_set_softreset(uint8_t value) {
  iob_write(IOB_UART_SOFTRESET_ADDR, IOB_UART_SOFTRESET_W, value);
}

void iob_uart_set_div(uint16_t value) {
  iob_write(IOB_UART_DIV_ADDR, IOB_UART_DIV_W, value);
}

void iob_uart_set_txdata(uint8_t value) {
  iob_write(IOB_UART_TXDATA_ADDR, IOB_UART_TXDATA_W, value);
}

void iob_uart_set_txen(uint8_t value) {
  iob_write(IOB_UART_TXEN_ADDR, IOB_UART_TXEN_W, value);
}

void iob_uart_set_rxen(uint8_t value) {
  iob_write(IOB_UART_RXEN_ADDR, IOB_UART_RXEN_W, value);
}

void iob_uart_set_baseaddr(uint32_t value) { base_uart = value; }

uint8_t iob_uart_get_txready() {
  return (uint8_t)iob_read(IOB_UART_TXREADY_ADDR, IOB_UART_TXREADY_W);
}

uint8_t iob_uart_get_rxready() {
  return (uint8_t)iob_read(IOB_UART_RXREADY_ADDR, IOB_UART_RXREADY_W);
}

uint8_t iob_uart_get_rxdata() {
  return (uint8_t)iob_read(IOB_UART_RXDATA_ADDR, IOB_UART_RXDATA_W);
}

uint16_t iob_uart_get_version() {
  return (uint16_t)iob_read(IOB_UART_VERSION_ADDR, IOB_UART_VERSION_W);
}

uint32_t iob_uart_get_baseaddr() { return base_uart; }
