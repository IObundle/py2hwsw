#include <stdint.h>
#include "iob_uart16550.h"
#include "printf.h"

static int base;

// TX FUNCTIONS
void uart16550_txwait() {
  while (!uart16550_txready())
    ;
}

char uart16550_txready() {
  uint8_t status = 0;
  status = *((volatile uint8_t *)(base + 5));
  return (status & (0x01 << 6));
}

void uart16550_putc(char c) {
  uart16550_txwait();
  *((volatile uint8_t *)(base)) = c;
}

// RX FUNCTIONS
void uart16550_rxwait() {
  while (!uart16550_rxready())
    ;
}

char uart16550_rxready() {
  uint8_t status = 0;
  status = *((volatile uint8_t *)(base + 5));
  return (status & (0x01));
}

char uart16550_getc() {
  uint8_t rvalue;
  uart16550_rxwait();
  rvalue = *((volatile uint8_t *)(base));
  return rvalue;
}

// UART basic functions
void uart16550_init(int base_address, uint16_t div) {
  // capture base address for good
  base = base_address;

  // Set the Line Control Register to the desired line control parameters.
  // Set bit 7 to ‘1’ to allow access to the Divisor Latches.
  uint8_t lcr = 0;
  lcr = *((volatile uint8_t *)(base + 3));
  lcr = (lcr | 0x80);
  *((volatile uint8_t *)(base + 3)) = lcr;

  // Set the Divisor Latches, MSB first, LSB next.
  uint8_t *dl = (uint8_t *)&div;
  *((volatile uint8_t *)(base + 1)) = *(dl + 1);
  *((volatile uint8_t *)(base)) = *(dl);

  // Set bit 7 of LCR to ‘0’ to disable access to Divisor Latches.
  // At this time the transmission engine starts working and data can be sent
  // and received.
  lcr = (lcr & 0x7F);
  *((volatile uint8_t *)(base + 3)) = lcr;

  // Set the FIFO trigger level. Generally, higher trigger level values produce
  // less interrupt to the system, so setting it to 14 bytes is recommended if
  // the system responds fast enough.
  *((volatile uint8_t *)(base + 2)) = 0xC0;

  // Enable desired interrupts by setting appropriate bits in the Interrupt
  // Enable register.
  *((volatile uint8_t *)(base + 1)) = 0x03;
}

// Change UART base
int uart16550_base(int base_address) {
  int previous = base;
  base = base_address;
  return previous;
}

void uart16550_finish() {
  uart16550_putc(EOT);
  uart16550_txwait();
}

// Print string, excluding end of string (0)
void uart16550_puts(const char *s) {
  while (*s)
    uart16550_putc(*s++);
}

// Sends the name of the file to use, including end of string (0)
void uart16550_sendstr(char *name) {
  int i = 0;
  do
    uart16550_putc(name[i]);
  while (name[i++]);
}

// Receives file into mem
int uart16550_recvfile(char *file_name, char *mem) {

  uart16550_puts(UART_PROGNAME);
  uart16550_puts(": requesting to receive file\n");

  // send file receive request
  uart16550_putc(FRX);

  // clear input buffer
  while (uart16550_rxready())
    uart16550_getc();

  // send file name
  uart16550_sendstr(file_name);

  // receive file size
  int file_size = (unsigned int)uart16550_getc();
  file_size |= ((unsigned int)uart16550_getc()) << 8;
  file_size |= ((unsigned int)uart16550_getc()) << 16;
  file_size |= ((unsigned int)uart16550_getc()) << 24;

  // allocate space for file if file pointer not initialized
  if (mem == NULL) {
    mem = (char *)malloc(file_size);
    if (mem == NULL) {
      uart16550_puts(UART_PROGNAME);
      uart16550_puts("Error: malloc failed");
    }
  }

  // send ACK before receiving file
  uart16550_putc(ACK);

  // write file to memory
  for (int i = 0; i < file_size; i++) {
    mem[i] = uart16550_getc();
  }

  uart16550_puts(UART_PROGNAME);
  uart16550_puts(": file received\n");

  return file_size;
}

// Sends mem contents to a file
void uart16550_sendfile(char *file_name, int file_size, char *mem) {

  uart16550_puts(UART_PROGNAME);
  uart16550_puts(": requesting to send file\n");

  // send file transmit command
  uart16550_putc(FTX);

  // send file name
  uart16550_sendstr(file_name);

  // send file size
  uart16550_putc((char)(file_size & 0x0ff));
  uart16550_putc((char)((file_size & 0x0ff00) >> 8));
  uart16550_putc((char)((file_size & 0x0ff0000) >> 16));
  uart16550_putc((char)((file_size & 0x0ff000000) >> 24));

  // send file contents
  for (int i = 0; i < file_size; i++)
    uart16550_putc(mem[i]);

  uart16550_puts(UART_PROGNAME);
  uart16550_puts(": file sent\n");
}
