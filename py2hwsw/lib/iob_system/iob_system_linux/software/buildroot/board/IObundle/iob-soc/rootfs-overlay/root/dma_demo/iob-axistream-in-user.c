#include "iob-axistream-in-user.h"

int iob_axis_in_reset() {
  if (iob_sysfs_write_file(IOB_AXISTREAM_IN_SYSFILE_SOFT_RESET, 1) == -1) {
    return -1;
  }
  if (iob_sysfs_write_file(IOB_AXISTREAM_IN_SYSFILE_SOFT_RESET, 0) == -1) {
    return -1;
  }
  return 0;
}

uint32_t iob_axis_read(uint32_t *value) {
  int ret = 0;
  uint32_t empty = 0;

  ret = iob_sysfs_read_file(IOB_AXISTREAM_IN_SYSFILE_FIFO_EMPTY, &empty);
  if ((ret == -1) || (empty == 1)) {
    return 0;
  } else {
    ret = iob_sysfs_read_file(IOB_AXISTREAM_IN_SYSFILE_DATA, value);
    if (ret == -1) {
      return 0;
    }
  }
  return 1;
}
