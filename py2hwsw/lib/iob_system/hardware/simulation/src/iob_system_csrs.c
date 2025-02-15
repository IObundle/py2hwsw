/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_system_csrs.h"

int base_uart = -1;

// Core Setters and Getters
void IOB_UART_SET_SOFTRESET(uint8_t value) {
  iob_write(IOB_UART_SOFTRESET_ADDR, IOB_UART_SOFTRESET_W, value);
}

void IOB_UART_SET_DIV(uint16_t value) {
  iob_write(IOB_UART_DIV_ADDR, IOB_UART_DIV_W, value);
}

void IOB_UART_SET_TXDATA(uint8_t value) {
  iob_write(IOB_UART_TXDATA_ADDR, IOB_UART_TXDATA_W, value);
}

void IOB_UART_SET_TXEN(uint8_t value) {
  iob_write(IOB_UART_TXEN_ADDR, IOB_UART_TXEN_W, value);
}

void IOB_UART_SET_RXEN(uint8_t value) {
  iob_write(IOB_UART_RXEN_ADDR, IOB_UART_RXEN_W, value);
}

void IOB_UART_SET_BASEADDR(uint32_t value) { base_uart = value; }

uint8_t IOB_UART_GET_TXREADY() {
  return (uint8_t)iob_read(IOB_UART_TXREADY_ADDR, IOB_UART_TXREADY_W);
}

uint8_t IOB_UART_GET_RXREADY() {
  return (uint8_t)iob_read(IOB_UART_RXREADY_ADDR, IOB_UART_RXREADY_W);
}

uint8_t IOB_UART_GET_RXDATA() {
  return (uint8_t)iob_read(IOB_UART_RXDATA_ADDR, IOB_UART_RXDATA_W);
}

uint16_t IOB_UART_GET_VERSION() {
  return (uint16_t)iob_read(IOB_UART_VERSION_ADDR, IOB_UART_VERSION_W);
}

uint32_t IOB_UART_GET_BASEADDR() { return base_uart; }
