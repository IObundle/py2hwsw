/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "iob_timer.h"

int main(int argc, char *argv[]) {
  printf("[User] IOb-Timer application\n");

  timer_init(0);

  printf("[User] Version: 0x%x\n", iob_timer_csrs_get_version());

  // read current timer count
  uint64_t elapsed = timer_get_count();
  printf("\nExecution time: %llu clock cycles\n", elapsed);

  return EXIT_SUCCESS;
}
