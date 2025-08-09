/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdint.h>
#include <stdio.h>

#include "iob-sysfs-common.h"
/* IOb-axistream-out header automatically generated from:
 * /path/to/iob-linux/scripts/drivers.py iob_axistream_out
 * contains:
 * - sysfs file paths
 * - Register address and width definitions
 */
#include "iob_axistream_out.h"

int iob_axis_out_reset();
uint32_t iob_axis_write(uint32_t value);
