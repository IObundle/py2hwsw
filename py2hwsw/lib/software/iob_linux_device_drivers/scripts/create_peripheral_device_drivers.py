import os
import string

from math import ceil


def create_dts_file(path, peripheral):
    """Create device tree file with demo on how to include the peripheral in the device tree"""
    content = f"""// SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
//
// SPDX-License-Identifier: {peripheral['spdx_license']}


/dts-v1/;

/ {{
    #address-cells = <1>;
    #size-cells = <1>;
    model = \"IOb-SoC, VexRiscv\";
    compatible = \"IOb-SoC, VexRiscv\";
    // CPU
    // Memory
    // Choosen
    soc {{
        #address-cells = <1>;
        #size-cells = <1>;
        compatible = \"iobundle,iob-soc\", \"simple-bus\";
        ranges;

        // Other SOC peripherals go here

        // Add this Node to device tree
        {peripheral['instance_name'].upper()}: {peripheral['name']}@/*{peripheral['instance_name'].upper()}_ADDR_MACRO*/ {{
            compatible = \"{peripheral['compatible_str']}\";
            reg = <0x/*{peripheral['instance_name'].upper()}_ADDR_MACRO*/ 0x100>;
        }};

    }};
}};"""
    with open(os.path.join(path, f"{peripheral['name']}.dts"), "w") as f:
        f.write(content)


def create_readme_file(path, peripheral):
    """Create README with directory structure and file descriptions of generated device driver files"""
    content = f"""<!--
SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}

SPDX-License-Identifier: {peripheral['spdx_license']}
-->

# {peripheral['upper_name']} Linux Kernel Drivers
- Structure:
    - `drivers/`: directory with linux kernel module drivers for {peripheral['name']}
        - `{peripheral['name']}_main.c`: driver source
        - `{peripheral['name']}_driver_files.h` and `{peripheral['name']}_sysfs.h`: header files
        - `driver.mk`: makefile segment with `{peripheral['name']}-obj:` target for driver
          compilation
    - `user/`: directory with user application example that uses {peripheral['name']}
      drivers
        - `{peripheral['name']}_user.c`: example user application that uses {peripheral['name']}
          drivers
        - `Makefile`: user application compilation targets
    - `{peripheral['name']}.dts`: device tree template with {peripheral['name']} node
        - manually add the `{peripheral['name']}` node to the system device tree so the
          {peripheral['name']} is recognized by the linux kernel
"""
    with open(os.path.join(path, "README.md"), "w") as f:
        f.write(content)


def create_driver_mk_file(path, peripheral):
    """Create Makefile segment for driver compilation"""
    content = f"""# SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
#
# SPDX-License-Identifier: {peripheral['spdx_license']}

{peripheral['name']}-objs := {peripheral['name']}_main.o iob_class/iob_class_utils.o
"""
    with open(os.path.join(path, "driver.mk"), "w") as f:
        f.write(content)


# Remove registers with address ranges from list
def filter_csrs_list(csrs_list):
    filtered_csrs_list = [i for i in csrs_list if i.get("log2n_items", 0) == 0]
    return filtered_csrs_list


def bceil(n, log2base):
    base = int(2**log2base)
    # n = eval_param_expression_from_config(n, self.config, "max")
    # print(f"{n} of {type(n)} and {base}")
    if n % base == 0:
        return n
    else:
        return int(base * ceil(n / base))


def deterministic_magic(name: str) -> str:
    """
    Return a single printable ASCII character to use as an ioctl magic
    number, derived deterministically from *name*.

    The algorithm:
    1. Sum the Unicode code points of all characters in *name*.
    2. Reduce the sum modulo the number of allowed characters.
    3. Pick the character at that index.

    The allowed set excludes letters and digits (they’re often used by
    other drivers) and contains the printable range 0x20‑0x7E.
    """
    # printable characters from space (0x20) to tilde (0x7E)
    printable = [
        ch
        for ch in (chr(i) for i in range(0x20, 0x7F))
        if ch not in string.ascii_letters + string.digits
    ]

    total = sum(ord(c) for c in name)
    idx = total % len(printable)
    return printable[idx]


def generate_ioctl_defines(name, csrs):
    """Define IOCTL commands for each CSR"""
    content = ""
    # define "ioctl name" __IOX("magic number","command number","argument type")
    # define WR_VALUE _IOW('a','a',int32_t*)
    # define RD_VALUE _IOR('a','b',int32_t*)
    # define RW_VALUE _IOWR('a','b',int32_t*)
    IOCTL_MAGIC = deterministic_magic(name)
    i = 0
    for csr in csrs:
        CSR_NAME = csr["name"].upper()
        if "W" in csr["mode"]:
            content += f"""\
#define WR_{CSR_NAME} _IOW('{IOCTL_MAGIC}',{i},int32_t*)
"""
            i += 1
        if "R" in csr["mode"]:
            content += f"""\
#define RD_{CSR_NAME} _IOR('{IOCTL_MAGIC}',{i},int32_t*)
"""
            i += 1
    return content


###############################################
#                                             #
#       Interface specific functions          #
#                                             #
###############################################

#
# /dev/ interface
#


def create_dev_user_csrs_source(path, peripheral):
    """Create user-space C file to interact with the driver"""
    content = (
        f"""
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "{peripheral['name']}.h"
"""
        + """\

uint32_t read_reg(int fd, uint32_t addr, uint32_t nbits, uint32_t *value) {
  ssize_t ret = -1;

  if (fd == 0) {
    perror("[User] Invalid file descriptor");
    return -1;
  }

  // Point to register address
  if (lseek(fd, addr, SEEK_SET) == -1) {
    perror("[User] Failed to seek to register");
    return -1;
  }

  // Read value from device
  switch (nbits) {
  case 8:
    uint8_t value8 = 0;
    ret = read(fd, &value8, sizeof(value8));
    if (ret == -1) {
      perror("[User] Failed to read from device");
    }
    *value = (uint32_t)value8;
    break;
  case 16:
    uint16_t value16 = 0;
    ret = read(fd, &value16, sizeof(value16));
    if (ret == -1) {
      perror("[User] Failed to read from device");
    }
    *value = (uint32_t)value16;
    break;
  case 32:
    uint32_t value32 = 0;
    ret = read(fd, &value32, sizeof(value32));
    if (ret == -1) {
      perror("[User] Failed to read from device");
    }
    *value = (uint32_t)value32;
    break;
  default:
    // unsupported nbits
    ret = -1;
    *value = 0;
    perror("[User] Unsupported nbits");
    break;
  }

  return ret;
}

uint32_t write_reg(int fd, uint32_t addr, uint32_t nbits, uint32_t value) {
  ssize_t ret = -1;

  if (fd == 0) {
    perror("[User] Invalid file descriptor");
    return -1;
  }

  // Point to register address
  if (lseek(fd, addr, SEEK_SET) == -1) {
    perror("[User] Failed to seek to register");
    return -1;
  }

  // Write value to device
  switch (nbits) {
  case 8:
    uint8_t value8 = (uint8_t)value;
    ret = write(fd, &value8, sizeof(value8));
    if (ret == -1) {
      perror("[User] Failed to write to device");
    }
    break;
  case 16:
    uint16_t value16 = (uint16_t)value;
    ret = write(fd, &value16, sizeof(value16));
    if (ret == -1) {
      perror("[User] Failed to write to device");
    }
    break;
  case 32:
    ret = write(fd, &value, sizeof(value));
    if (ret == -1) {
      perror("[User] Failed to write to device");
    }
    break;
  default:
    break;
  }

  return ret;
}

"""
        + f"""\
int fd = 0;

void {peripheral['name']}_csrs_init_baseaddr(uint32_t addr) {{
  fd = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
  if (fd == -1) {{
    perror("[User] Failed to open the device file");
  }}
}}

// Core Setters and Getters
"""
    )

    for csr in peripheral["csrs"]:
        CSR_NAME = csr["name"].upper()
        if int(csr["n_bits"]) <= 8:
            data_type = "uint8_t"
        elif int(csr["n_bits"]) <= 16:
            data_type = "uint16_t"
        else:
            data_type = "uint32_t"
        if "W" in csr["mode"]:
            content += f"""\
void {peripheral['name']}_csrs_set_{csr['name']}({data_type} value) {{
  write_reg(fd, {peripheral['upper_name']}_{CSR_NAME}_ADDR, {peripheral['upper_name']}_{CSR_NAME}_W, value);
}}
"""
        if "R" in csr["mode"]:
            content += f"""\
{data_type} {peripheral['name']}_csrs_get_{csr['name']}() {{
  uint32_t return_value;
  read_reg(fd, {peripheral['upper_name']}_{CSR_NAME}_ADDR, {peripheral['upper_name']}_{CSR_NAME}_W, &return_value);
  return ({data_type})return_value;
}}
"""

    with open(os.path.join(path, f"{peripheral['name']}_dev_csrs.c"), "w") as f:
        f.write(content)


#
# IOCTL
#


def create_ioctl_user_csrs_source(path, peripheral):
    """Create user-space C file to interact with the driver"""
    content = f"""
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>

#include "{peripheral['name']}.h"

"""

    # Define IOCTL commands for each CSR
    content += generate_ioctl_defines(peripheral["name"], peripheral["csrs"])

    content += f"""\
int fd = 0;

void {peripheral['name']}_csrs_init_baseaddr(uint32_t addr) {{
  fd = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
  if (fd == -1) {{
    perror("[User] Failed to open the device file");
  }}
}}

// Core Setters and Getters
"""
    for csr in peripheral["csrs"]:
        CSR_NAME = csr["name"].upper()
        if int(csr["n_bits"]) <= 8:
            data_type = "uint8_t"
        elif int(csr["n_bits"]) <= 16:
            data_type = "uint16_t"
        else:
            data_type = "uint32_t"
        if "W" in csr["mode"]:
            content += f"""\
    void {peripheral['name']}_csrs_set_{csr['name']}({data_type} value) {{
      ioctl(fd, WR_{CSR_NAME}, (int32_t*) &value);
    }}
    """
        if "R" in csr["mode"]:
            content += f"""\
    {data_type} {peripheral['name']}_csrs_get_{csr['name']}() {{
      uint32_t return_value;
      ioctl(fd, RD_{CSR_NAME}, (int32_t*) &return_value);
      return ({data_type})return_value;
    }}
    """

    with open(os.path.join(path, f"{peripheral['name']}_ioctl_csrs.c"), "w") as f:
        f.write(content)


#
# Sysfs interface
#


def create_sysfs_driver_header_file(path, peripheral, multi=False):
    """Generate <peripheral_name>_sysfs.h header"""
    # multi: generate sysfs_header for multiple hardware device support
    # NOTE: assumes struct iob_data* in dev->platform_data
    csrs_list = filter_csrs_list(peripheral["csrs"])
    top = peripheral["name"]
    TOP = peripheral["upper_name"]

    if multi:
        fswhdr = open(os.path.join(path, f"{top}_sysfs_multi.h"), "w")
    else:
        fswhdr = open(os.path.join(path, f"{top}_sysfs.h"), "w")

    fswhdr.write("/* This file was automatically generated by:\n")
    fswhdr.write(
        " * `create_sysfs_driver_header_file` method of `create_peripheral_device_drivers.py`\n"
    )
    fswhdr.write(" */\n\n")

    core_prefix = peripheral["upper_name"]

    fswhdr.write(f"#ifndef H_{core_prefix}_SYSFS_H\n")
    fswhdr.write(f"#define H_{core_prefix}_SYSFS_H\n\n")

    # sysfs show / store functions
    fswhdr.write("// Sysfs show/store functions\n")
    fswhdr.write(
        "static ssize_t sysfs_enosys_show(struct device *dev, struct device_attribute *attr, char *buf) {\n"
    )
    fswhdr.write("\treturn -ENOSYS;\n")
    fswhdr.write("}\n\n")
    fswhdr.write(
        "static ssize_t sysfs_enosys_store(struct device *dev, struct device_attribute *attr, const char __user *buf, size_t count) {\n"
    )
    fswhdr.write("\treturn -ENOSYS;\n")
    fswhdr.write("}\n\n")

    for csr in csrs_list:
        CSR_NAME = csr["name"].upper()
        csr_name = csr["name"]
        if "W" in csr["mode"]:
            # top, csr_name
            fswhdr.write(
                f"static ssize_t sysfs_{csr_name}_store(struct device *dev, struct device_attribute *attr, const char __user *buf, size_t count) {{\n"
            )
            fswhdr.write("\tu32 value = 0;\n")
            if multi:
                fswhdr.write(
                    f"\tstruct iob_data *{top}_data = (struct iob_data*) dev->platform_data;\n"
                )
            fswhdr.write(f"\tif (!mutex_trylock(&{top}_mutex)) {{\n")
            fswhdr.write('\t\tpr_info("Another process is accessing the device\\n");\n')
            fswhdr.write("\t\treturn -EBUSY;\n")
            fswhdr.write("\t}\n")
            fswhdr.write('\tsscanf(buf, "%u", &value);\n')
            if multi:
                fswhdr.write(
                    f"\tiob_data_write_reg({top}_data->regbase, value, {TOP}_CSRS_{CSR_NAME}_ADDR, {TOP}_CSRS_{CSR_NAME}_W);\n"
                )
            else:
                fswhdr.write(
                    f"\tiob_data_write_reg({top}_data.regbase, value, {TOP}_CSRS_{CSR_NAME}_ADDR, {TOP}_CSRS_{CSR_NAME}_W);\n"
                )
            fswhdr.write(f"\tmutex_unlock(&{top}_mutex);\n")
            fswhdr.write(f'\tpr_info("[{top}] Sysfs - Write: 0x%x\\n", value);\n')
            fswhdr.write("\treturn count;\n")
            fswhdr.write("}\n\n")
        elif "R" in csr["mode"]:
            # show function
            fswhdr.write(
                f"static ssize_t sysfs_{csr_name}_show(struct device *dev, struct device_attribute *attr, char *buf) {{\n"
            )
            if multi:
                fswhdr.write(
                    f"\tstruct iob_data *{top}_data = (struct iob_data*) dev->platform_data;\n"
                )
                fswhdr.write(
                    f"\tu32 value = iob_data_read_reg({top}_data->regbase, {TOP}_CSRS_{CSR_NAME}_ADDR, {TOP}_CSRS_{CSR_NAME}_W);\n"
                )
            else:
                fswhdr.write(
                    f"\tu32 value = iob_data_read_reg({top}_data.regbase, {TOP}_CSRS_{CSR_NAME}_ADDR, {TOP}_CSRS_{CSR_NAME}_W);\n"
                )
            fswhdr.write(f'\tpr_info("[{top}] Sysfs - Read: 0x%x\\n", value);\n')
            fswhdr.write('\treturn sprintf(buf, "%u", value);\n')
            fswhdr.write("}\n\n")

    # DEVICE_ATTR(name, 0600, sysfs_show, sysfs_store)
    fswhdr.write("// Device attributes\n")
    for csr in csrs_list:
        # attr name and permissions
        reg_name = csr["name"]
        fswhdr.write(f"DEVICE_ATTR({reg_name}, 0600,")

        # sysfs show function
        if "R" in csr["mode"]:
            fswhdr.write(f" sysfs_{reg_name}_show,")
        else:
            fswhdr.write(" sysfs_enosys_show,")

        # sysfs store function
        if "W" in csr["mode"]:
            fswhdr.write(f" sysfs_{reg_name}_store);\n")
        else:
            fswhdr.write(" sysfs_enosys_store);\n")

    fswhdr.write("\n")

    # probe / remove functions
    fswhdr.write("// Probe / Remove functions\n")
    fswhdr.write(
        f"static int {top}_create_device_attr_files(struct device *device) {{\n"
    )
    fswhdr.write("\tint ret = 0;\n")
    for csr in csrs_list:
        fswhdr.write(f"\tret |= device_create_file(device, &dev_attr_{csr['name']});\n")
    fswhdr.write("\treturn ret;\n")
    fswhdr.write("}\n\n")

    fswhdr.write(
        f"static void {top}_remove_device_attr_files(struct iob_data *{top}_data) {{\n"
    )
    for csr in csrs_list:
        fswhdr.write(
            f"\tdevice_remove_file({top}_data->device, &dev_attr_{csr['name']});\n"
        )
    fswhdr.write(f"\tdevice_destroy({top}_data->class, {top}_data->devnum);\n")
    fswhdr.write("\treturn;\n")
    fswhdr.write("}\n")

    fswhdr.write(f"\n#endif // H_{core_prefix}_SYSFS_H\n")
    fswhdr.close()


#
# Common
#


def create_driver_header_file_list(path, peripheral):
    """Generate <peripheral_name>_driver_files.h header"""
    fswhdr = open(os.path.join(path, f"{peripheral['name']}_driver_files.h"), "w")

    fswhdr.write("/* This file was automatically generated by:\n")
    fswhdr.write(
        " * `create_driver_header_file_list` method of `create_peripheral_device_drivers.py`\n"
    )
    fswhdr.write(" */\n\n")

    top = peripheral["name"]
    core_prefix = peripheral["upper_name"]

    fswhdr.write(f"#ifndef H_{core_prefix}_DRIVER_FILES_H\n")
    fswhdr.write(f"#define H_{core_prefix}_DRIVER_FILES_H\n\n")
    fswhdr.write(f'#define {core_prefix}_DRIVER_NAME "{top}"\n')
    fswhdr.write(f'#define {core_prefix}_DRIVER_CLASS "{top}"\n')
    fswhdr.write(f'#define {core_prefix}_DEVICE_FILE "/dev/{top}"\n')
    fswhdr.write(
        f'#define {core_prefix}_DEVICE_CLASS "/sys/class/" {core_prefix}_DRIVER_CLASS "/" {core_prefix}_DRIVER_NAME\n\n'
    )

    for csr in peripheral["csrs"]:
        CSR_NAME = csr["name"].upper()
        fswhdr.write(
            f'#define {core_prefix}_SYSFILE_{CSR_NAME} {core_prefix}_DEVICE_CLASS "/{csr["name"].lower()}"\n'
        )
    fswhdr.write("\n")

    fswhdr.write(f'#include "{top}_csrs_conf.h"\n')

    fswhdr.write(f"\n#endif // H_{core_prefix}_DRIVER_FILES_H\n")

    fswhdr.close()


def create_driver_main_file(path, peripheral):
    """Create the driver's kernel source"""
    content = f"""/*
 * SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
 *
 * SPDX-License-Identifier: {peripheral['spdx_license']}
 */

/* {peripheral['name']}_main.c: driver for {peripheral['name']}
 * using device platform. No hardcoded hardware address:
 * 1. load driver: insmod {peripheral['name']}.ko
 * 2. run user app: ./user/user
 */

#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/io.h>
#include <linux/ioport.h>
#include <linux/kernel.h>
#include <linux/mod_devicetable.h>
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/uaccess.h>

#include <linux/ioctl.h>

"""
    # Define IOCTL commands for each CSR
    content += generate_ioctl_defines(peripheral["name"], peripheral["csrs"])
    content += f"""

#include "iob_class/iob_class_utils.h"
#include "{peripheral['name']}_driver_files.h"

static int {peripheral['name']}_probe(struct platform_device *);
static int {peripheral['name']}_remove(struct platform_device *);

static ssize_t {peripheral['name']}_read(struct file *, char __user *, size_t, loff_t *);
static ssize_t {peripheral['name']}_write(struct file *, const char __user *, size_t,
                               loff_t *);
static loff_t {peripheral['name']}_llseek(struct file *, loff_t, int);
static int {peripheral['name']}_open(struct inode *, struct file *);
static int {peripheral['name']}_release(struct inode *, struct file *);

static struct iob_data {peripheral['name']}_data = {{0}};
DEFINE_MUTEX({peripheral['name']}_mutex);

#include "{peripheral['name']}_sysfs.h"

static const struct file_operations {peripheral['name']}_fops = {{
    .owner = THIS_MODULE,
    .write = {peripheral['name']}_write,
    .read = {peripheral['name']}_read,
    .llseek = {peripheral['name']}_llseek,
    .unlocked_ioctl = {peripheral['name']}_ioctl,
    .open = {peripheral['name']}_open,
    .release = {peripheral['name']}_release,
}};

static const struct of_device_id of_{peripheral['name']}_match[] = {{
    {{.compatible = "{peripheral['compatible_str']}"}},
    {{}},
}};

static struct platform_driver {peripheral['name']}_driver = {{
    .driver =
        {{
            .name = "{peripheral['name']}",
            .owner = THIS_MODULE,
            .of_match_table = of_{peripheral['name']}_match,
        }},
    .probe = {peripheral['name']}_probe,
    .remove = {peripheral['name']}_remove,
}};

//
// Module init and exit functions
//
static int {peripheral['name']}_probe(struct platform_device *pdev) {{
  struct resource *res;
  int result = 0;

  if ({peripheral['name']}_data.device != NULL) {{
    pr_err("[Driver] %s: No more devices allowed!\\n", {peripheral['upper_name']}_DRIVER_NAME);

    return -ENODEV;
  }}

  pr_info("[Driver] %s: probing.\\n", {peripheral['upper_name']}_DRIVER_NAME);

  // Get the I/O region base address
  res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
  if (!res) {{
    pr_err("[Driver]: Failed to get I/O resource!\\n");
    result = -ENODEV;
    goto r_get_resource;
  }}

  // Request and map the I/O region
  {peripheral['name']}_data.regbase = devm_ioremap_resource(&pdev->dev, res);
  if (IS_ERR({peripheral['name']}_data.regbase)) {{
    result = PTR_ERR({peripheral['name']}_data.regbase);
    goto r_ioremmap;
  }}
  {peripheral['name']}_data.regsize = resource_size(res);

  // Alocate char device
  result =
      alloc_chrdev_region(&{peripheral['name']}_data.devnum, 0, 1, {peripheral['upper_name']}_DRIVER_NAME);
  if (result) {{
    pr_err("%s: Failed to allocate device number!\\n", {peripheral['upper_name']}_DRIVER_NAME);
    goto r_alloc_region;
  }}

  cdev_init(&{peripheral['name']}_data.cdev, &{peripheral['name']}_fops);

  result = cdev_add(&{peripheral['name']}_data.cdev, {peripheral['name']}_data.devnum, 1);
  if (result) {{
    pr_err("%s: Char device registration failed!\\n", {peripheral['upper_name']}_DRIVER_NAME);
    goto r_cdev_add;
  }}

  // Create device class // todo: make a dummy driver just to create and own the
  // class: https://stackoverflow.com/a/16365027/8228163
  if (({peripheral['name']}_data.class =
           class_create(THIS_MODULE, {peripheral['upper_name']}_DRIVER_CLASS)) == NULL) {{
    printk("Device class can not be created!\\n");
    goto r_class;
  }}

  // Create device file
  {peripheral['name']}_data.device =
      device_create({peripheral['name']}_data.class, NULL, {peripheral['name']}_data.devnum, NULL,
                    {peripheral['upper_name']}_DRIVER_NAME);
  if ({peripheral['name']}_data.device == NULL) {{
    printk("Can not create device file!\\n");
    goto r_device;
  }}

  result = {peripheral['name']}_create_device_attr_files({peripheral['name']}_data.device);
  if (result) {{
    pr_err("Cannot create device attribute file......\\n");
    goto r_dev_file;
  }}

  dev_info(&pdev->dev, "initialized.\\n");
  goto r_ok;

r_dev_file:
  {peripheral['name']}_remove_device_attr_files(&{peripheral['name']}_data);
r_device:
  class_destroy({peripheral['name']}_data.class);
r_class:
  cdev_del(&{peripheral['name']}_data.cdev);
r_cdev_add:
  unregister_chrdev_region({peripheral['name']}_data.devnum, 1);
r_alloc_region:
  // iounmap is managed by devm
r_ioremmap:
r_get_resource:
r_ok:

  return result;
}}

static int {peripheral['name']}_remove(struct platform_device *pdev) {{
  {peripheral['name']}_remove_device_attr_files(&{peripheral['name']}_data);
  class_destroy({peripheral['name']}_data.class);
  cdev_del(&{peripheral['name']}_data.cdev);
  unregister_chrdev_region({peripheral['name']}_data.devnum, 1);
  // Note: no need for iounmap, since we are using devm_ioremap_resource()

  dev_info(&pdev->dev, "exiting.\\n");

  return 0;
}}

static int __init test_counter_init(void) {{
  pr_info("[Driver] %s: initializing.\\n", {peripheral['upper_name']}_DRIVER_NAME);

  return platform_driver_register(&{peripheral['name']}_driver);
}}

static void __exit test_counter_exit(void) {{
  pr_info("[Driver] %s: exiting.\\n", {peripheral['upper_name']}_DRIVER_NAME);
  platform_driver_unregister(&{peripheral['name']}_driver);
}}

//
// File operations
//

static int {peripheral['name']}_open(struct inode *inode, struct file *file) {{
  pr_info("[Driver] {peripheral['name']} device opened\\n");

  if (!mutex_trylock(&{peripheral['name']}_mutex)) {{
    pr_info("Another process is accessing the device\\n");

    return -EBUSY;
  }}

  return 0;
}}

static int {peripheral['name']}_release(struct inode *inode, struct file *file) {{
  pr_info("[Driver] {peripheral['name']} device closed\\n");

  mutex_unlock(&{peripheral['name']}_mutex);

  return 0;
}}

static ssize_t {peripheral['name']}_read(struct file *file, char __user *buf, size_t count,
                              loff_t *ppos) {{
  int size = 0;
  u32 value = 0;

  /* read value from register */
  switch (*ppos) {{
"""
    # Create read code for each CSR
    for csr in peripheral["csrs"]:
        if "R" not in csr["mode"]:
            continue
        CSR_NAME = csr["name"].upper()
        content += f"""\
  case {peripheral['upper_name']}_CSRS_{CSR_NAME}_ADDR:
    value = iob_data_read_reg({peripheral['name']}_data.regbase, {peripheral['upper_name']}_CSRS_{CSR_NAME}_ADDR,
                              {peripheral['upper_name']}_CSRS_{CSR_NAME}_W);
    size = ({peripheral['upper_name']}_CSRS_{CSR_NAME}_W >> 3); // bit to bytes
    pr_info("[Driver] Read {csr['name']} CSR!\\n");
    break;
"""

    content += f"""\
  default:
    // invalid address - no bytes read
    return 0;
  }}

  // Read min between count and REG_SIZE
  if (size > count)
    size = count;

  if (copy_to_user(buf, &value, size))
    return -EFAULT;

  return count;
}}

static ssize_t {peripheral['name']}_write(struct file *file, const char __user *buf,
                               size_t count, loff_t *ppos) {{
  int size = 0;
  u32 value = 0;

  switch (*ppos) {{
"""
    # Create write code for each CSR
    for csr in peripheral["csrs"]:
        if "W" not in csr["mode"]:
            continue
        CSR_NAME = csr["name"].upper()
        content += f"""\
  case {peripheral['upper_name']}_CSRS_{CSR_NAME}_ADDR:
    size = ({peripheral['upper_name']}_CSRS_{CSR_NAME}_W >> 3); // bit to bytes
    if (read_user_data(buf, size, &value))
      return -EFAULT;
    iob_data_write_reg({peripheral['name']}_data.regbase, value, {peripheral['upper_name']}_CSRS_{CSR_NAME}_ADDR,
                       {peripheral['upper_name']}_CSRS_{CSR_NAME}_W);
    pr_info("[Driver] {csr['name']} {peripheral['name']}: 0x%x\\n", value);
    break;
"""

    content += f"""\
  default:
    pr_info("[Driver] Invalid write address 0x%x\\n", (unsigned int)*ppos);
    // invalid address - no bytes written
    return 0;
  }}

  return count;
}}

/* Custom lseek function
 * check: lseek(2) man page for whence modes
 */
static loff_t {peripheral['name']}_llseek(struct file *filp, loff_t offset, int whence) {{
  loff_t new_pos = -1;

  switch (whence) {{
  case SEEK_SET:
    new_pos = offset;
    break;
  case SEEK_CUR:
    new_pos = filp->f_pos + offset;
    break;
  case SEEK_END:
    new_pos = (1 << {peripheral['upper_name']}_CSRS_ADDR_W) + offset;
    break;
  default:
    return -EINVAL;
  }}

  // Check for valid bounds
  if (new_pos < 0 || new_pos > {peripheral['name']}_data.regsize) {{
    return -EINVAL;
  }}

  // Update file position
  filp->f_pos = new_pos;

  return new_pos;
}}

/* IOCTL function
 * This function will be called when we write IOCTL on the Device file
 */
 static long {peripheral['name']}_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{{
  int size = 0;
  u32 value = 0;

         switch(cmd) {{
"""
    # Create code for each CSR
    for csr in peripheral["csrs"]:
        CSR_NAME = csr["name"].upper()
        if "W" in csr["mode"]:
            content += f"""\
                case WR_{CSR_NAME}:
                        size = ({peripheral['upper_name']}_CSRS_{CSR_NAME}_W >> 3); // bit to bytes
                        if (read_user_data((int32_t*) arg, size, &value))
                          return -EFAULT;
                        iob_data_write_reg({peripheral['name']}_data.regbase, value, {peripheral['upper_name']}_CSRS_{CSR_NAME}_ADDR,
                                           {peripheral['upper_name']}_CSRS_{CSR_NAME}_W);
                        pr_info("[Driver] {csr['name']} {peripheral['name']}: 0x%x\\n", value);

                        break;
"""
        if "R" in csr["mode"]:
            content += f"""\
                case RD_{CSR_NAME}:
                        value = iob_data_read_reg({peripheral['name']}_data.regbase, {peripheral['upper_name']}_CSRS_{CSR_NAME}_ADDR,
                                                  {peripheral['upper_name']}_CSRS_{CSR_NAME}_W);
                        size = ({peripheral['upper_name']}_CSRS_{CSR_NAME}_W >> 3); // bit to bytes
                        pr_info("[Driver] Read {csr['name']} CSR!\\n");

                        if (copy_to_user((int32_t*) arg, &value, size))
                          return -EFAULT;

                        break;
"""

    content += f"""\
                default:
                        pr_info("[Driver] Invalid IOCTL command 0x%x\\n", cmd);
                        break;
        }}
        return 0;
}}

module_init(test_counter_init);
module_exit(test_counter_exit);

MODULE_LICENSE("{peripheral['license']}");
MODULE_AUTHOR("{peripheral['author']}");
MODULE_DESCRIPTION("{peripheral['description']}");
MODULE_VERSION("{peripheral['version']}");
"""
    with open(os.path.join(path, f"{peripheral['name']}_main.c"), "w") as f:
        f.write(content)


def create_sysfs_user_csrs_source(path, peripheral):
    """Create user-space C file to interact with the driver"""
    content = f"""/*
 * SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
 *
 * SPDX-License-Identifier: {peripheral['spdx_license']}
 */

#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "{peripheral['name']}_driver_files.h"

#include "{peripheral['name']}_csrs.h"

int sysfs_read_file(const char *filename, uint32_t *read_value) {{
  // Open file for read
  FILE *file = fopen(filename, "r");
  if (file == NULL) {{
    perror("[User] Failed to open the file");
    return -1;
  }}

  // Read uint32_t value from file in ASCII
  ssize_t ret = fscanf(file, "%u", read_value);
  if (ret == -1) {{
    perror("[User] Failed to read from file");
    fclose(file);
    return -1;
  }}

  fclose(file);

  return ret;
}}

int sysfs_write_file(const char *filename, uint32_t write_value) {{
  // Open file for write
  FILE *file = fopen(filename, "w");
  if (file == NULL) {{
    perror("[User] Failed to open the file");
    return -1;
  }}

  // Write uint32_t value to file in ASCII
  ssize_t ret = fprintf(file, "%u", write_value);
  if (ret == -1) {{
    perror("[User] Failed to write to file");
    fclose(file);
    return -1;
  }}

  fclose(file);

  return ret;
}}


void {peripheral['name']}_csrs_init_baseaddr(uint32_t addr) {{}}

// Core Setters and Getters
"""

    for csr in peripheral["csrs"]:
        CSR_NAME = csr["name"].upper()
        if int(csr["n_bits"]) <= 8:
            data_type = "uint8_t"
        elif int(csr["n_bits"]) <= 16:
            data_type = "uint16_t"
        else:
            data_type = "uint32_t"
        if "W" in csr["mode"]:
            content += f"""\
void {peripheral['name']}_csrs_set_{csr['name']}({data_type} value) {{
  sysfs_write_file({peripheral['upper_name']}_SYSFILE_{CSR_NAME}, value);
}}
"""
        if "R" in csr["mode"]:
            content += f"""\
{data_type} {peripheral['name']}_csrs_get_{csr['name']}() {{
  uint32_t return_value;
  sysfs_read_file({peripheral['upper_name']}_SYSFILE_{CSR_NAME}, &return_value);
  return ({data_type})return_value;
}}
"""

    with open(os.path.join(path, f"{peripheral['name']}_sysfs_csrs.c"), "w") as f:
        f.write(content)


def create_user_makefile(path, peripheral):
    """Create Makefile to build user application"""
    content = f"""# SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
#
# SPDX-License-Identifier: {peripheral['spdx_license']}

SRC = $(wildcard *.c)
SRC += $(wildcard ../../src/{peripheral['name']}.c)
HDR += ../drivers/{peripheral['name']}_driver_files.h
FLAGS = -Wall -Werror -O2
FLAGS += -static
FLAGS += -march=rv32imac
FLAGS += -mabi=ilp32
FLAGS += -I../drivers -I../../src
BIN = {peripheral['name']}_user
CC = riscv64-unknown-linux-gnu-gcc

all: $(BIN)

$(BIN): $(SRC) $(HDR)
	$(CC) $(FLAGS) $(INCLUDE) -o $(BIN) $(SRC)

clean:
	rm -rf $(BIN)
"""
    with open(os.path.join(path, "Makefile"), "w") as f:
        f.write(content)


#
# Main function
#


def generate_device_drivers(output_dir, peripheral):
    """Generate device driver files for a peripheral"""

    # Find 'iob_csrs' subblock
    for block in peripheral["subblocks"]:
        if block["core_name"] == "iob_csrs":
            csrs_subblock = block
            break
    else:
        print("Error: no iob_csrs subblock found")
        exit(1)

    # Create copy of csrs list
    csrs_list = list(csrs_subblock["csrs"])
    # Every peripheral has an implicit "version" CSR
    csrs_list.append(
        {
            "name": "version",
            "mode": "R",
            "n_bits": 16,
        }
    )

    # Peripheral information
    # TODO: Replace hardcoded by dynamic info.
    _peripheral = {
        "name": peripheral["name"],  # example: 'iob_timer'
        "instance_name": f"{peripheral['name'][4:]}0",  # example: 'timer0'
        "upper_name": peripheral["name"].upper(),
        "version": "0.81",
        "description": f"{peripheral['name']} Drivers",
        "author": "IObundle",
        "spdx_year": "2025",
        "spdx_license": "MIT",
        "license": "Dual MIT/GPL",
        "csrs": csrs_list,
    }
    _peripheral["compatible_str"] = f"iobundle,{_peripheral['instance_name']}"

    print("Generating device drivers for", _peripheral["name"], "in", output_dir)

    # Create directory structure
    os.makedirs(os.path.join(output_dir, "drivers"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "user"), exist_ok=True)

    # Create files
    create_dts_file(output_dir, _peripheral)
    create_readme_file(output_dir, _peripheral)
    create_driver_mk_file(os.path.join(output_dir, "drivers"), _peripheral)
    create_driver_header_file_list(os.path.join(output_dir, "drivers"), _peripheral)
    create_sysfs_driver_header_file(os.path.join(output_dir, "drivers"), _peripheral)
    create_driver_main_file(os.path.join(output_dir, "drivers"), _peripheral)
    create_sysfs_user_csrs_source(os.path.join(output_dir, "user"), _peripheral)
    create_dev_user_csrs_source(os.path.join(output_dir, "user"), _peripheral)
    create_ioctl_user_csrs_source(os.path.join(output_dir, "user"), _peripheral)
    create_user_makefile(os.path.join(output_dir, "user"), _peripheral)
