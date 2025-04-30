/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_dma_csrs.h"
#include <stdio.h>

int iob_core_tb() {

  int failed = 0;

  // print welcome message
  printf("IOB DMA testbench\n");

  // print the reset message
  printf("Reset complete\n");

  unsigned int version;
  int i;
  // read version 20 times to burn time
  for (i = 0; i < 20; i++) {
    version = iob_dma_csrs_get_version();
  }
  printf("Version is %d\n", version);

  printf("DMA test complete.\n");
  return failed;
}
