#include "iob_uart_csrs.h"

// Base Address
static int base;


// Core Setters and Getters
void iob_write (uint32_t addr, uint32_t addr_w, uint32_t value) {
  if (addr_w >16)
    (*((volatile uint32_t *)(base + addr)) = (value));
  else if (addr_w > 8)
    (*((volatile uint16_t *)(base + addr)) = (value));
  else
    (*((volatile uint8_t *)(base + addr)) = (value));}

uint32_t iob_read (uint32_t addr, uint32_t addr_w) {
  if (addr_w >16)
    return (uint32_t) (*((volatile uint32_t *)(base + addr)));
  else if (addr_w > 8)
    return (uint32_t) (*((volatile uint16_t *)(base + addr)));
  else
    return (uint32_t) (*((volatile uint8_t *)(base + addr));}
}

