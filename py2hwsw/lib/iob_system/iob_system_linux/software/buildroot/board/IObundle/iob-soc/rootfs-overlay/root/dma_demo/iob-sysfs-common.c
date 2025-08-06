/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob-sysfs-common.h"
#include <stdint.h>
#include <stdio.h>

int iob_sysfs_read_file(const char *filename, uint32_t *read_value) {
  // Open file for read
  FILE *file = fopen(filename, "r");
  if (file == NULL) {
    perror("[User] Failed to open the file");
    return -1;
  }

  // Read uint32_t value from file in ASCII
  ssize_t ret = fscanf(file, "%u", read_value);
  if (ret == -1) {
    perror("[User] Failed to read from file");
    fclose(file);
    return -1;
  }

  fclose(file);

  return ret;
}

int iob_sysfs_write_file(const char *filename, uint32_t write_value) {
  // Open file for write
  FILE *file = fopen(filename, "w");
  if (file == NULL) {
    perror("[User] Failed to open the file");
    return -1;
  }

  // Write uint32_t value to file in ASCII
  ssize_t ret = fprintf(file, "%u", write_value);
  if (ret == -1) {
    perror("[User] Failed to write to file");
    fclose(file);
    return -1;
  }

  fclose(file);

  return ret;
}

int iob_sysfs_print_version(const char *filename) {
  uint32_t ret = -1;
  uint32_t version = 0;

  ret = iob_sysfs_read_file(filename, &version);
  if (ret == -1) {
    return ret;
  }

  printf("[User] Version: 0x%x\n", version);
  return 0;
}

char *iob_sysfs_gen_fname(char *filename, char *class_path, int minor,
                          char *reg) {
  sprintf(filename, "%s%d/%s", class_path, minor, reg);
  return filename;
}
