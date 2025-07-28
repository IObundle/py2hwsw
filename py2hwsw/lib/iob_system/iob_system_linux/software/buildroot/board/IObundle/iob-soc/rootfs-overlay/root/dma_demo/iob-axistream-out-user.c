#include "iob-axistream-out-user.h"

int iob_axis_out_reset() {
  if (iob_sysfs_write_file(IOB_AXISTREAM_OUT_SYSFILE_SOFT_RESET, 1) == -1) {
    return -1;
  }
  if (iob_sysfs_write_file(IOB_AXISTREAM_OUT_SYSFILE_SOFT_RESET, 0) == -1) {
    return -1;
  }
  return 0;
}

uint32_t iob_axis_write(uint32_t value) {
  int ret = 0;
  uint32_t full = 0;

  ret = iob_sysfs_read_file(IOB_AXISTREAM_OUT_SYSFILE_FIFO_FULL, &full);
  if ((ret == -1) || (full == 1)) {
    return 0;
  } else {
    if (iob_sysfs_write_file(IOB_AXISTREAM_OUT_SYSFILE_DATA, value) == -1) {
      return 0;
    }
  }
  return 1;
}
