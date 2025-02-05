#include "iob_uart_csrs.h"

// Core Setters and Getters
void IOB_UART_SET_SOFTRESET(uint8_t value) {
  iob_write(IOB_UART_SOFTRESET_ADDR, value);
}

void IOB_UART_SET_DIV(uint16_t value) { iob_write(IOB_UART_DIV_ADDR, value); }

void IOB_UART_SET_TXDATA(uint8_t value) {
  iob_write(IOB_UART_TXDATA_ADDR, value);
}

void IOB_UART_SET_TXEN(uint8_t value) { iob_write(IOB_UART_TXEN_ADDR, value); }

void IOB_UART_SET_RXEN(uint8_t value) { iob_write(IOB_UART_RXEN_ADDR, value); }

uint8_t IOB_UART_GET_TXREADY() { return iob_read(IOB_UART_TXREADY_ADDR); }

uint8_t IOB_UART_GET_RXREADY() { return iob_read(IOB_UART_RXREADY_ADDR); }

uint8_t IOB_UART_GET_RXDATA() { return iob_read(IOB_UART_RXDATA_ADDR); }

uint16_t IOB_UART_GET_VERSION() { return iob_read(IOB_UART_VERSION_ADDR); }
