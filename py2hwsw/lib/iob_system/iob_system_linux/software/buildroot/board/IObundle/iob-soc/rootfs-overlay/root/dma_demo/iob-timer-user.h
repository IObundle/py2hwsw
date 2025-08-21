/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdint.h>
#include <stdio.h>

#include "iob-sysfs-common.h"
/* IOb-Timer header automatically generated from:
 * /path/to/iob-linux/scripts/drivers.py iob_timer
 * contains:
 * - sysfs file paths
 * - Register address and width definitions
 */
#include "iob_timer.h"

int iob_timer_reset();
int iob_timer_init();
int iob_timer_get_count(uint64_t *count);
int iob_timer_test();
