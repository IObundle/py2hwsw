/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_uart.h"
#include <stdint.h>

// TX FUNCTIONS
void uart_txwait() {
  while (!iob_uart_csrs_get_txready())
    ;
}

void uart_putc(char c) {
  while (!iob_uart_csrs_get_txready())
    ;
  iob_uart_csrs_set_txdata(c);
}

// RX FUNCTIONS
void uart_rxwait() {
  while (!iob_uart_csrs_get_rxready())
    ;
}

uint8_t uart_getc() {
  while (!iob_uart_csrs_get_rxready())
    ;
  return iob_uart_csrs_get_rxdata();
}

// UART basic functions
void uart_init(int base_address, uint16_t div) {
  // capture base address for good
  IOB_UART_CSRS_INIT_BASEADDR(base_address);

  // pulse soft reset
  iob_uart_csrs_set_softreset(1);
  iob_uart_csrs_set_softreset(0);

  // Set the division factor div
  // div should be equal to round (fclk/baudrate)
  // E.g for fclk = 100 Mhz for a baudrate of 115200 we should
  // iob_uart_csrs_set_div(868)
  iob_uart_csrs_set_div(div);

  // enable TX and RX
  iob_uart_csrs_set_txen(1);
  iob_uart_csrs_set_rxen(1);
}

void uart_finish() {
  uart_putc(EOT);
  uart_txwait();
}

// Print string, excluding end of string (0)
void uart_puts(const char *s) {
  while (*s)
    uart_putc(*s++);
}

// Sends the name of the file to use, including end of string (0)
void uart_sendstr(char *name) {
  int i = 0;
  do
    uart_putc(name[i]);
  while (name[i++]);
}

// Receives file into mem
uint32_t uart_recvfile(char *file_name, char *mem) {

  uart_puts(UART_PROGNAME);
  uart_puts(": requesting to receive file\n");

  // send file receive request
  uart_putc(FRX);

  // send file name
  uart_sendstr(file_name);

  // receive file size
  uint32_t file_size = uart_getc();
  file_size |= ((uint32_t)uart_getc()) << 8;
  file_size |= ((uint32_t)uart_getc()) << 16;
  file_size |= ((uint32_t)uart_getc()) << 24;

  // send ACK before receiving file
  uart_putc(ACK);

  // write file to memory
  for (uint32_t i = 0; i < file_size; i++) {
    mem[i] = uart_getc();
  }

  uart_puts(UART_PROGNAME);
  uart_puts(": file received\n");

  return file_size;
}

// Sends mem contents to a file
void uart_sendfile(char *file_name, int file_size, char *mem) {

  uart_puts(UART_PROGNAME);
  uart_puts(": requesting to send file\n");

  // send file transmit command
  uart_putc(FTX);

  // send file name
  uart_sendstr(file_name);

  // send file size
  uart_putc((char)(file_size & 0x0ff));
  uart_putc((char)((file_size & 0x0ff00) >> 8));
  uart_putc((char)((file_size & 0x0ff0000) >> 16));
  uart_putc((char)((file_size & 0x0ff000000) >> 24));

  // send file contents
  for (int i = 0; i < file_size; i++)
    uart_putc(mem[i]);

  uart_puts(UART_PROGNAME);
  uart_puts(": file sent\n");
}
