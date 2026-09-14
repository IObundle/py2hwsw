/*
 * SPDX-License-Identifier: BSD-2-Clause
 *
 * SPDX-FileCopyrightText: 2019 Western Digital Corporation or its affiliates.
 * SPDX-FileCopyrightText: 2026 IObundle
 */

#include <sbi/riscv_asm.h>
#include <sbi/riscv_encoding.h>
#include <sbi/riscv_io.h>
#include <sbi/sbi_console.h>
#include <sbi/sbi_const.h>
#include <sbi/sbi_hart.h>
#include <sbi/sbi_platform.h>

/*
 * Include these files as needed.
 * See config.mk PLATFORM_xxx configuration parameters.
 */
#include <sbi_utils/fdt/fdt_fixup.h>
#include <sbi_utils/fdt/fdt_helper.h>
#include <sbi_utils/ipi/aclint_mswi.h>
#include <sbi_utils/irqchip/plic.h>
#include <sbi_utils/serial/uart8250.h>
#include <sbi_utils/timer/aclint_mtimer.h>

// clang-format off
#define IOB_SYSTEM_LINUX_PLIC_ADDR 0x/*PLIC0_BASE_MACRO*/
#define IOB_SYSTEM_LINUX_PLIC_NUM_SOURCES 31
#define IOB_SYSTEM_LINUX_HART_COUNT 1
#define IOB_SYSTEM_LINUX_CLINT_ADDR 0x/*CLINT0_BASE_MACRO*/
#define IOB_SYSTEM_LINUX_ACLINT_MTIMER_FREQ /*FREQ_MACRO*/
#define IOB_SYSTEM_LINUX_ACLINT_MSWI_ADDR (IOB_SYSTEM_LINUX_CLINT_ADDR + CLINT_MSWI_OFFSET)
#define IOB_SYSTEM_LINUX_ACLINT_MTIMER_ADDR (IOB_SYSTEM_LINUX_CLINT_ADDR + CLINT_MTIMER_OFFSET)
#define IOB_SYSTEM_LINUX_UART_ADDR 0x/*UART0_BASE_MACRO*/
#define IOB_SYSTEM_LINUX_UART_INPUT_FREQ /*FREQ_MACRO*/
#define IOB_SYSTEM_LINUX_UART_BAUDRATE /*BAUD_MACRO*/
#define IOB_SYSTEM_LINUX_UART_REG_SHIFT 0
#define IOB_SYSTEM_LINUX_UART_REG_WIDTH 1
#define IOB_SYSTEM_LINUX_UART_REG_OFFSET 0
// clang-format on

static struct platform_uart_data uart = {
    IOB_SYSTEM_LINUX_UART_ADDR,      IOB_SYSTEM_LINUX_UART_INPUT_FREQ,
    IOB_SYSTEM_LINUX_UART_BAUDRATE,  IOB_SYSTEM_LINUX_UART_REG_SHIFT,
    IOB_SYSTEM_LINUX_UART_REG_WIDTH, IOB_SYSTEM_LINUX_UART_REG_OFFSET};

static struct plic_data plic = {
    .addr = IOB_SYSTEM_LINUX_PLIC_ADDR,
    .num_src = IOB_SYSTEM_LINUX_PLIC_NUM_SOURCES,
    .context_map =
        {
            [0] = {0, 1},
        },
};

static struct aclint_mswi_data mswi = {
    .addr = IOB_SYSTEM_LINUX_ACLINT_MSWI_ADDR,
    .size = ACLINT_MSWI_SIZE,
    .first_hartid = 0,
    .hart_count = IOB_SYSTEM_LINUX_HART_COUNT,
};

static struct aclint_mtimer_data mtimer = {
    .mtime_freq = IOB_SYSTEM_LINUX_ACLINT_MTIMER_FREQ,
    .mtime_addr =
        IOB_SYSTEM_LINUX_ACLINT_MTIMER_ADDR + ACLINT_DEFAULT_MTIME_OFFSET,
    .mtime_size = ACLINT_DEFAULT_MTIME_SIZE,
    .mtimecmp_addr =
        IOB_SYSTEM_LINUX_ACLINT_MTIMER_ADDR + ACLINT_DEFAULT_MTIMECMP_OFFSET,
    .mtimecmp_size = ACLINT_DEFAULT_MTIMECMP_SIZE,
    .first_hartid = 0,
    .hart_count = IOB_SYSTEM_LINUX_HART_COUNT,
    .has_64bit_mmio = true,
};

/*
 * Platform early initialization.
 */
static int iob_system_linux_early_init(bool cold_boot) {
  const void *fdt;
  struct platform_uart_data uart_data;
  struct plic_data plic_data;
  unsigned long aclint_freq;
  uint64_t clint_addr;
  int rc;

  if (!cold_boot)
    return 0;

  /*
   * Initialize UART as early as possible so sbi_printf works.
   * This must be done after sbi_domain_init (which happens before early_init).
   */
  rc = uart8250_init(uart.addr, uart.freq, uart.baud, uart.reg_shift,
                     uart.reg_io_width, uart.reg_offset, 0);
  if (rc)
    return rc;

  fdt = fdt_get_address();
  if (fdt) {
    // Note: instead of this, we could use OpenSBI helper functions, like
    // serial_uart8250_init() from
    // OpenSBI/lib/utils/serial/fdt_serial_uart8250.c
    rc = fdt_parse_uart8250(fdt, &uart_data, "ns16550a");
    if (!rc) {
      if (uart_data.addr)
        uart.addr = uart_data.addr;
      if (uart_data.freq)
        uart.freq = uart_data.freq;
      if (uart_data.baud)
        uart.baud = uart_data.baud;
      if (uart_data.reg_shift)
        uart.reg_shift = uart_data.reg_shift;
      if (uart_data.reg_io_width)
        uart.reg_io_width = uart_data.reg_io_width;
      if (uart_data.reg_offset)
        uart.reg_offset = uart_data.reg_offset;

      /* Re-initialize UART with FDT data if found */
      uart8250_init(uart.addr, uart.freq, uart.baud, uart.reg_shift,
                    uart.reg_io_width, uart.reg_offset, 0);
    }

    rc = fdt_parse_plic(fdt, &plic_data, "riscv,plic0");
    if (!rc) {
      plic.unique_id = plic_data.unique_id;
      if (plic_data.addr)
        plic.addr = plic_data.addr;
      if (plic_data.size)
        plic.size = plic_data.size;
      if (plic_data.num_src)
        plic.num_src = plic_data.num_src;
    }

    rc = fdt_parse_timebase_frequency(fdt, &aclint_freq);
    if (!rc && aclint_freq)
      mtimer.mtime_freq = aclint_freq;

    rc = fdt_parse_compat_addr(fdt, &clint_addr, "riscv,clint0");
    if (!rc && clint_addr) {
      mswi.addr = clint_addr;
      mtimer.mtime_addr =
          clint_addr + CLINT_MTIMER_OFFSET + ACLINT_DEFAULT_MTIME_OFFSET;
      mtimer.mtimecmp_addr =
          clint_addr + CLINT_MTIMER_OFFSET + ACLINT_DEFAULT_MTIMECMP_OFFSET;
    }
  }

  return aclint_mswi_cold_init(&mswi);
}

/*
 * Platform final initialization.
 */
static int iob_system_linux_final_init(bool cold_boot) {
  void *fdt;

  if (!cold_boot)
    return 0;

  fdt = fdt_get_address_rw();
  fdt_fixups(fdt);

  return 0;
}

/*
 * Enable SBI HART extensions (e.g. zicbom) reported by the CPU
 * device-tree node ("riscv,isa"/"riscv,isa-extensions"). This must run
 * before hart feature detection so that OpenSBI can program the
 * corresponding menvcfg bits (CBIE/CBCFE for Zicbom) for lower
 * privilege levels.
 */
static int iob_system_linux_extensions_init(bool cold_boot) {
  if (!cold_boot)
    return 0;

  return fdt_parse_isa_extensions_all_harts(fdt_get_address());
}

/*
 * Initialize the iob_system_linux interrupt controller during cold boot.
 */
static int iob_system_linux_irqchip_init(void) {
  /* Example if the generic PLIC driver is used */
  return plic_cold_irqchip_init(&plic);
}

/*
 * Initialize iob_system_linux timer during cold boot.
 */
static int iob_system_linux_timer_init(void) {
  /* Example if the generic ACLINT driver is used */
  return aclint_mtimer_cold_init(&mtimer, NULL);
}

/*
 * Platform descriptor.
 */
const struct sbi_platform_operations platform_ops = {
    .early_init = iob_system_linux_early_init,
    .final_init = iob_system_linux_final_init,
    .extensions_init = iob_system_linux_extensions_init,
    .irqchip_init = iob_system_linux_irqchip_init,
    .timer_init = iob_system_linux_timer_init};
const struct sbi_platform platform = {
    .opensbi_version = OPENSBI_VERSION,
    .platform_version = SBI_PLATFORM_VERSION(0x0, 0x01),
    .name = "iob_system_linux",
    .features = SBI_PLATFORM_DEFAULT_FEATURES,
    .hart_count = IOB_SYSTEM_LINUX_HART_COUNT,
    .hart_stack_size = SBI_PLATFORM_DEFAULT_HART_STACK_SIZE,
    .heap_size = SBI_PLATFORM_DEFAULT_HEAP_SIZE(IOB_SYSTEM_LINUX_HART_COUNT),
    .platform_ops_addr = (unsigned long)&platform_ops};
