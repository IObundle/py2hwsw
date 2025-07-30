#include <stdint.h>
#include <stdio.h>

#include "iob-sysfs-common.h"
/* IOb-axistream-in header automatically generated from:
 * /path/to/iob-linux/scripts/drivers.py iob_axistream_in
 * contains:
 * - sysfs file paths
 * - Register address and width definitions
 */
#include "iob_axistream_in.h"

int iob_axis_in_reset();
uint32_t iob_axis_read(uint32_t *value);
