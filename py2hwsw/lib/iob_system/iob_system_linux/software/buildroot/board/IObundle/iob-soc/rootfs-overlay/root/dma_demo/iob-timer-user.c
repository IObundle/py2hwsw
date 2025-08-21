/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob-timer-user.h"

int iob_timer_reset() {
  if (iob_sysfs_write_file(IOB_TIMER_SYSFILE_RESET, 1) == -1) {
    return -1;
  }
  if (iob_sysfs_write_file(IOB_TIMER_SYSFILE_RESET, 0) == -1) {
    return -1;
  }

  return 0;
}

int iob_timer_init() {
  if (iob_timer_reset()) {
    return -1;
  }

  if (iob_sysfs_write_file(IOB_TIMER_SYSFILE_ENABLE, 1) == -1) {
    return -1;
  }

  return 0;
}

int iob_timer_get_count(uint64_t *count) {
  uint32_t ret = -1;
  uint32_t data = 0;

  // Sample timer counter
  if (iob_sysfs_write_file(IOB_TIMER_SYSFILE_SAMPLE, 1) == -1) {
    return -1;
  }
  if (iob_sysfs_write_file(IOB_TIMER_SYSFILE_SAMPLE, 0) == -1) {
    return -1;
  }

  // Read sampled timer counter
  ret = iob_sysfs_read_file(IOB_TIMER_SYSFILE_DATA_HIGH, &data);
  if (ret == -1) {
    return -1;
  }
  *count = ((uint64_t)data) << IOB_TIMER_DATA_LOW_W;
  ret = iob_sysfs_read_file(IOB_TIMER_SYSFILE_DATA_LOW, &data);
  if (ret == -1) {
    return -1;
  }
  (*count) = (*count) | (uint64_t)data;

  return 0;
}

int iob_timer_test() {
  printf("[Tester|User] IOb-Timer test\n");

  if (iob_timer_init() == -1) {
    perror("[Tester|User] Failed to initialize timer");
    return -1;
  }

  if (iob_sysfs_print_version(IOB_TIMER_SYSFILE_VERSION) == -1) {
    perror("[Tester|User] Failed to print version");
    return -1;
  }

  // read current timer count
  uint64_t elapsed = 0;
  if (iob_timer_get_count(&elapsed)) {
    perror("[Tester|User] Failed to get count");
  }
  printf("\nExecution time: %llu clock cycles\n", elapsed);

  return 0;
}
