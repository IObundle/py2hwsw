// SPDX-FileCopyrightText: 2024 IObundle
//
// SPDX-License-Identifier: MIT

#include "iob_uart_csrs_tb.h"
void iob_write(uint32_t addr, uint8_t size, uint32_t data);
uint32_t iob_read(uint32_t addr, uint8_t size);

// Core Setters and Getters
void IOB_UART_SET_SOFTRESET(uint8_t value) {
  iob_write(IOB_UART_SOFTRESET_ADDR, IOB_UART_SOFTRESET_W, (uint32_t)value);
}

void IOB_UART_SET_DIV(uint16_t value) {
  iob_write(IOB_UART_DIV_ADDR, IOB_UART_DIV_W, (uint32_t)value);
}

void IOB_UART_SET_TXDATA(uint8_t value) {
  iob_write(IOB_UART_TXDATA_ADDR, IOB_UART_TXDATA_W, (uint32_t)value);
}

void IOB_UART_SET_TXEN(uint8_t value) {
  iob_write(IOB_UART_TXEN_ADDR, IOB_UART_TXEN_W, (uint32_t)value);
}

void IOB_UART_SET_RXEN(uint8_t value) {
  iob_write(IOB_UART_RXEN_ADDR, IOB_UART_RXEN_W, (uint32_t)value);
}

uint8_t IOB_UART_GET_TXREADY() {
  return iob_read(IOB_UART_TXREADY_ADDR, IOB_UART_TXREADY_W);
}

uint8_t IOB_UART_GET_RXREADY() {
  return iob_read(IOB_UART_RXREADY_ADDR, IOB_UART_RXREADY_W);
}

uint8_t IOB_UART_GET_RXDATA() {
  return iob_read(IOB_UART_RXDATA_ADDR, IOB_UART_RXDATA_W);
}

uint16_t IOB_UART_GET_VERSION() {
  return iob_read(IOB_UART_VERSION_ADDR, IOB_UART_VERSION_W);
}
