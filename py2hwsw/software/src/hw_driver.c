/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdint.h>


// Core Setters and Getters
void iob_write(uint32_t addr, uint32_t addr_w, uint32_t value) {
  if (addr_w > 16)
    (*((volatile uint32_t *) addr) = (value));
  else if (addr_w > 8)
    (*((volatile uint16_t *) addr) = (value));
  else
    (*((volatile uint8_t *) addr) = (value));
}

uint32_t iob_read(uint32_t addr, uint32_t addr_w) {
  if (addr_w > 16)
    return (uint32_t)(*((volatile uint32_t *) addr));
  else if (addr_w > 8)
    return (uint32_t)(*((volatile uint16_t *) addr));
  else
    return (uint32_t)(*((volatile uint8_t *) addr));
}
