# Tutorial: Add New Device Driver

This tutorial presents the steps required to create simple linux character device drivers for a device and use them in IOb-System-Linux.

The [IOb-SPI](https://github.com/IObundle/iob-spi) device is used as an example.

See [this commit](https://github.com/IObundle/iob-spi/commit/dce9c93f1202da96d3570f88e31b9409afb43419) for the full SPI linux driver implementation.

To follow this tutorial, clone the [iob-linux](https://github.com/IObundle/iob-linux) repository.

## 1. Create device drivers

On the device repository create a `software/linux` directory with the following files:

```bash
software/
├── linux
│   ├── drivers
│   │   ├── driver.mk
│   │   └── iob_spi_main.c
│   ├── iob_spi.dts
│   └── Readme.md
```

1.1. Create compilation makefile segment

`software/linux/drivers/driver.mk`

```make
iob_spi_master-objs := iob_spi_main.o iob_class/iob_class_utils.o
```

1.2. Create main driver file

`software/linux/drivers/iob_spi_main.c`

Copy the [SPI driver source](https://github.com/IObundle/iob-spi/blob/main/software/linux/drivers/iob_spi_main.c) to use it as a template for the new driver.

```bash
cp iob-spi/software/linux/drivers/iob_spi_main.c <new_core_name>/software/linux/drivers/<new_core_name>_main.c
```

Replace `<new_core_name>` with the new device name.

1.2.1. Rename the functions to the particular device

Use the following commands to rename the functions from the template:

```bash
NEW_CORE_NAME=<new_core_name>
sed -i "s/IOB_SPI_MASTER/${NEW_CORE_NAME}/g" ${NEW_CORE_NAME}/software/linux/drivers/${NEW_CORE_NAME}_main.c
sed -i "s/iob_spi_master/${NEW_CORE_NAME}/g" ${NEW_CORE_NAME}/software/linux/drivers/${NEW_CORE_NAME}_main.c
sed -i "s/iob_spi/${NEW_CORE_NAME}/g" ${NEW_CORE_NAME}/software/linux/drivers/${NEW_CORE_NAME}_main.c
sed -i "s/spi/${NEW_CORE_NAME}/g" ${NEW_CORE_NAME}/software/linux/drivers/${NEW_CORE_NAME}_main.c
```

Replace `<new_core_name>` with the new device name.

1.2.2. Update read function

Update the `iob_spi_read()` function implementation according with the read registers of the device. SPI has the `FL_READY`, `FL_DATAOUT`  and `VERSION` (implicit) read registers:

```C
static ssize_t iob_spi_read(struct file *file, char __user *buf, size_t count,
                             loff_t *ppos) {
  // (...)

  /* read value from register */
  switch (*ppos) {
  // Add one case for each Read software register
  case IOB_SPI_MASTER_FL_READY_ADDR:
    value =
        iob_data_read_reg(iob_spi_data->regbase, IOB_SPI_MASTER_FL_READY_ADDR,
                          IOB_SPI_MASTER_FL_READY_W);
    size = (IOB_SPI_MASTER_FL_READY_W >> 3); // bit to bytes
    pr_info("[Driver] %s: Read FL_READY: 0x%x\n", IOB_SPI_MASTER_DRIVER_NAME,
            value);
    break;
  case IOB_SPI_MASTER_FL_DATAOUT_ADDR:
    value =
        iob_data_read_reg(iob_spi_data->regbase, IOB_SPI_MASTER_FL_DATAOUT_ADDR,
                          IOB_SPI_MASTER_FL_DATAOUT_W);
    size = (IOB_SPI_MASTER_FL_DATAOUT_W >> 3); // bit to bytes
    pr_info("[Driver] %s: Read FL_DATAOUT: 0x%x\n", IOB_SPI_MASTER_DRIVER_NAME,
            value);
    break;
  // NOTE: version software register is implicit and always added
  case IOB_SPI_MASTER_VERSION_ADDR:
    value = iob_data_read_reg(iob_spi_data->regbase, IOB_SPI_MASTER_VERSION_ADDR,
                              IOB_SPI_MASTER_VERSION_W);
    size = (IOB_SPI_MASTER_VERSION_W >> 3); // bit to bytes
    pr_info("[Driver] %s: Read version 0x%x\n", IOB_SPI_MASTER_DRIVER_NAME, value);
    break;
  default:
    // invalid address - no bytes read
    return 0;
  }

  // (...)
}
```

1.2.3. Update write function

Update the `iob_spi_write()` function implementation according with the write registers of the device. SPI had the `FL_RESET`, `FL_DATAIN`, `FL_ADDRESS`, `FL_COMMAND`, `FL_COMMANDTP` and `FL_VALIDFLG` write registers:

```C
static ssize_t iob_spi_write(struct file *file, const char __user *buf,
                              size_t count, loff_t *ppos) {
  // (...)

  switch (*ppos) {
  // Add one case for each Write software register
  case IOB_SPI_MASTER_FL_RESET_ADDR:
    size = (IOB_SPI_MASTER_FL_RESET_W >> 3); // bit to bytes
    if (read_user_data(buf, size, &value))
      return -EFAULT;
    iob_data_write_reg(iob_spi_data->regbase, value,
                       IOB_SPI_MASTER_FL_RESET_ADDR,
                       IOB_SPI_MASTER_FL_RESET_W);
    pr_info("[Driver] %s: FL_RESET iob_spi: 0x%x\n",
            IOB_SPI_MASTER_DRIVER_NAME, value);
    break;
  case IOB_SPI_MASTER_FL_DATAIN_ADDR:
    // FL_DATAIN access implementation
    break;
  case IOB_SPI_MASTER_FL_ADDRESS_ADDR:
    // FL_ADDRESS access implementation
    break;
  case IOB_SPI_MASTER_FL_COMMAND_ADDR:
    // FL_COMMAND access implementation
    break;
  case IOB_SPI_MASTER_FL_COMMANDTP_ADDR:
    // FL_COMMANDTP access implementation
    break;
  case IOB_SPI_MASTER_FL_VALIDFLG_ADDR:
    // FL_VALIDFLG access implementation
    break;
  default:
      pr_info("[Driver] %s: Invalid write address 0x%x\n", IOB_SPI_MASTER_DRIVER_NAME,
              (unsigned int)*ppos);
      // invalid address - no bytes written
      return 0;
  }

  return count;
}
```

1.2.4. Verify device `compatible` field

Notice the string used in the `struct of_device_id`. This string must match the `compatible` field in the device tree to associate the hardware device with the correct driver.

```C
static const struct of_device_id of_iob_spi_match[] = {
    {.compatible = "iobundle,spi0"},
    {},
};
```

1.3. Generate driver header files

Generate `iob_spi_master.h` and `iob_spi_master_sysfs_multi.h` header files with the [`drivers.py`](https://github.com/IObundle/iob-linux/blob/main/scripts/drivers.py) script:

```bash
python3 ./path/to/iob-linux/scripts/drivers.py iob_spi_master -o [output_dir]
```

The `output_dir` should be a directory that is included by the linux user space software.

These headers are commonly placed in the Linux root filesystem along with the user space software that uses them.

For example, for the `dma_demo` program, the sources are placed in the following location:

`software/buildroot/board/IObundle/iob-soc/rootfs-overlay/root/dma_demo/`

## 2. Update the Linux Device Tree

Include the device node in the Linux Device Tree.

`software/linux/iob_spi.dts`

The `compatible` string must match with the `compatible` field in the driver source.

```
// SPDX-License-Identifier: (GPL-2.0 OR MIT)
/* Copyright (c) 2024 IObundle */

/dts-v1/;

/ {
    #address-cells = <1>;
    #size-cells = <1>;
    model = "IOb-SoC, VexRiscv";
    compatible = "IOb-SoC, VexRiscv";
    // CPU
    // Memory
    // Choosen
    soc {
        #address-cells = <1>;
        #size-cells = <1>;
        compatible = "iobundle,iob-soc", "simple-bus";
        ranges;

        // Other SOC peripherals go here

        // Add this Node to device tree
        SPI0: spi@/*SPI0_ADDR_MACRO*/ {
            compatible = "iobundle,spi0";
            reg = <0x/*SPI0_ADDR_MACRO*/ 0x100>;
        };

    };
};
```

The `size-cells` field (`0x100`) of the following device tree line must updated to match the size of the device register address space.

```
            reg = <0x/*SPI0_ADDR_MACRO*/ 0x100>;
```

## 3. Compile kernel, driver module, and add to rootfs

3.1. Compile Linux kernel

A compiled kernel is required to be able to later build the driver module.

```bash
cd /path/to/iob-linux
make build-linux-kernel
```

3.2. Compile driver module

Copy device driver files to the [`iob-linux/software/drivers`](https://github.com/IObundle/iob-linux/tree/main/software/drivers) folder.

```bash
cp /path/to/device/repo/software/linux/drivers/* /path/to/iob-linux/software/drivers/
```

Run the `make all` target.

```bash
cd /path/to/iob-linux/software/drivers
make all
```

3.3. Add module files to buildroot (optional)

To add the built driver modules to the Linux root filesystem, move the modules to a folder inside the buildroot filesystem.
For the SPI driver example, the module is placed in the `drivers` folder of the rootfs.

```bash
cd /path/to/iob-linux
mkdir software/buildroot/board/IObundle/iob-soc/rootfs-overlay/drivers
cp software/drivers/* software/buildroot/board/IObundle/iob-soc/rootfs-overlay/drivers/
```

Re-build buildroot:

```bash
make build-buildroot
```

## 4. Load module in linux

After booting into linux, use the `insmod` command to load the new driver modules:

```bash
# inside linux console
insmod /path/to/driver.ko
# iob-spi example:
insmod /drivers/iob_spi_master.ko
```
