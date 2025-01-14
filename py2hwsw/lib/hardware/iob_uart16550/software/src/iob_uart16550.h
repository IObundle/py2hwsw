#include <stdlib.h>
#include <stdarg.h>
#include <stdint.h>

#define UART_PROGNAME "IOb-UART"

// UART commands
#define STX 2 // start text
#define ETX 3 // end text
#define EOT 4 // end of transission
#define ENQ 5 // enquiry
#define ACK 6 // acklowledge
#define FTX 7 // transmit file
#define FRX 8 // receive file

// UART functions

// Reset UART and set the division factor
void uart16550_init(int base_address, uint16_t div);

// Change UART base, returns previous base
int uart16550_base(int base_address);

// Close transmission
void uart16550_finish();

// TX FUNCTIONS
// Check if tx is ready
char uart16550_txready();
// Wait for tx to be ready
void uart16550_txwait();

// RX FUNCTIONS
// Check if rx is ready
char uart16550_rxready();
// Wait for rx to be ready
void uart16550_rxwait();

// Print char
void uart16550_putc(char c);

// Print string
void uart16550_puts(const char *s);

// Send file
void uart16550_sendfile(char *file_name, int file_size, char *mem);

// Get char
char uart16550_getc();

// Receive file
int uart16550_recvfile(char *file_name, char *mem);
