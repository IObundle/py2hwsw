/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

#include "iob-sysfs-common.h"
/* IOb-DMA header automatically generated from:
 * /path/to/iob-linux/scripts/drivers.py iob_dma
 * contains:
 * - sysfs file paths
 * - Register address and width definitions
 */
#include "iob_dma.h"

int dma_start_transfer(uint32_t *base_addr, uint32_t size, int direction,
                       uint16_t interface_number);
uint8_t dma_transfer_ready();
