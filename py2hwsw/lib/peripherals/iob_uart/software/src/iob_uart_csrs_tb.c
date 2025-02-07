/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_tasks.h"
#include "iob_uart_csrs.h"

// Base Address
static int base;
void IOB_UART_INIT_BASEADDR(uint32_t addr) { base = addr; }

// Core Setters and Getters
void IOB_UART_SET_SOFTRESET(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_SOFTRESET_ADDR))) = (value));
}

void IOB_UART_SET_DIV(uint16_t value) {
  (*((volatile uint16_t *)((base) + (IOB_UART_DIV_ADDR))) = (value));
}

void IOB_UART_SET_TXDATA(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_TXDATA_ADDR))) = (value));
}

void IOB_UART_SET_TXEN(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_TXEN_ADDR))) = (value));
}

void IOB_UART_SET_RXEN(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_RXEN_ADDR))) = (value));
}

uint8_t IOB_UART_GET_TXREADY() {
  return (*((volatile uint8_t *)((base) + (IOB_UART_TXREADY_ADDR))));
}

uint8_t IOB_UART_GET_RXREADY() {
  return (*((volatile uint8_t *)((base) + (IOB_UART_RXREADY_ADDR))));
}

uint8_t IOB_UART_GET_RXDATA() {
  return (*((volatile uint8_t *)((base) + (IOB_UART_RXDATA_ADDR))));
}

uint16_t IOB_UART_GET_VERSION() {
  return (*((volatile uint16_t *)((base) + (IOB_UART_VERSION_ADDR))));
}
