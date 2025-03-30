/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_uart_csrs.h"
#include "iob_vlt_tasks.h"

// Base Address
static int base;
void iob_uart_init_baseaddr(uint32_t addr) { base = addr; }

// Core Setters and Getters
void iob_uart_set_softreset(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_SOFTRESET_ADDR))) = (value));
}

void iob_uart_set_div(uint16_t value) {
  (*((volatile uint16_t *)((base) + (IOB_UART_DIV_ADDR))) = (value));
}

void iob_uart_set_txdata(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_TXDATA_ADDR))) = (value));
}

void iob_uart_set_txen(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_TXEN_ADDR))) = (value));
}

void iob_uart_set_rxen(uint8_t value) {
  (*((volatile uint8_t *)((base) + (IOB_UART_RXEN_ADDR))) = (value));
}

uint8_t iob_uart_get_txready() {
  return (*((volatile uint8_t *)((base) + (IOB_UART_TXREADY_ADDR))));
}

uint8_t iob_uart_get_rxready() {
  return (*((volatile uint8_t *)((base) + (IOB_UART_RXREADY_ADDR))));
}

uint8_t iob_uart_get_rxdata() {
  return (*((volatile uint8_t *)((base) + (IOB_UART_RXDATA_ADDR))));
}

uint16_t iob_uart_get_version() {
  return (*((volatile uint16_t *)((base) + (IOB_UART_VERSION_ADDR))));
}
