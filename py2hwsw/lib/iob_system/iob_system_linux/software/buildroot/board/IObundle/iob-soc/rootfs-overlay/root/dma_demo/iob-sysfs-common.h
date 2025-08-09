/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

/* iob-sysfs-common.h: common functions for SysFS access */

int iob_sysfs_read_file(const char *filename, uint32_t *read_value);
int iob_sysfs_write_file(const char *filename, uint32_t write_value);
int iob_sysfs_print_version(const char *filename);
char *iob_sysfs_gen_fname(char *filename, char *class_path, int minor,
                          char *reg);
