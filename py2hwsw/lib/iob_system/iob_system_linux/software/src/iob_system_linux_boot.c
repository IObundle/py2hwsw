#include "bsp.h"
#include "clint.h"
#include "iob-eth.h"
#include "iob-spi.h"
#include "iob-spidefs.h"
#include "iob-spiplatform.h"
#include "iob-uart16550.h"
#include "iob_system_linux_conf.h"
#include "iob_system_linux_periphs.h"
#include "iob_system_linux_system.h"
#include "printf.h"
#include <stdio.h>
#include <string.h>

#define PROGNAME "IOb-Bootloader"

#define DC1 17 // Device Control 1 (used to indicate end of bootloader)
#define EXT_MEM 0x80000000

#define FLASH_FILE_SIZE_OFFSET 0x0   // sector 0, subsector 0
#define FLASH_FIRMWARE_OFFSET 0x1000 // sector 0, subsector 1

// Ethernet utility functions
// NOTE: These functions are not compatible with malloc() and free().
//      These are specifically made for use with the current iob-eth.c drivers.
//      (These assume that there is only one block allocated at a time)
//      It allocates a block with required size at the end of the external
//      memory region.
static void *mem_alloc(size_t size) {
  return (void *)(EXT_MEM | (1 << IOB_SYSTEM_LINUX_MEM_ADDR_W)) - size;
}
static void mem_free(void *ptr) {}

void clear_cache() {
  // Delay to ensure all data is written to memory
  for (unsigned int i = 0; i < 10; i++)
    asm volatile("nop");
  // Flush VexRiscv CPU internal cache
  asm volatile(".word 0x500F" ::: "memory");
}

// Send signal by uart to receive file by ethernet
uint32_t uart_recvfile_ethernet(char *file_name) {
  uart16550_puts(UART_PROGNAME);
  uart16550_puts(": requesting to receive file by ethernet\n");

  // send file receive by ethernet request
  uart16550_putc(0x13);

  // send file name (including end of string)
  uart16550_puts(file_name);
  uart16550_putc(0);

  // receive file size
  uint32_t file_size = uart16550_getc();
  file_size |= ((uint32_t)uart16550_getc()) << 8;
  file_size |= ((uint32_t)uart16550_getc()) << 16;
  file_size |= ((uint32_t)uart16550_getc()) << 24;

  // send ACK before receiving file
  uart16550_putc(ACK);

  return file_size;
}

int compute_mem_load_txt(char file_name_array[4][50],
                         long int file_address_array[4], char *file_start_addr,
                         uint32_t file_size) {
  int state = 0;
  int file_name_count = 0;
  int file_count = 0;
  char hexChar = 0;
  int hexDecimal = 0;
  int i = 0;
  for (i = 0; i < file_size; i++) {
    hexChar = *(file_start_addr + i);
    // uart16550_puts(&hexChar); /* Used for debugging. */
    if (state == 0) {
      if (hexChar == ' ') {
        file_name_array[file_count][file_name_count] = '\0';
        file_name_count = 0;
        file_address_array[file_count] = 0;
        file_count = file_count + 1;
        state = 1;
      } else {
        file_name_array[file_count][file_name_count] = hexChar;
        file_name_count = file_name_count + 1;
      }
    } else if (state == 1) {
      if (hexChar == '\n') {
        state = 0;
      } else {
        if ('0' <= hexChar && hexChar <= '9') {
          hexDecimal = hexChar - '0';
        } else if ('a' <= hexChar && hexChar <= 'f') {
          hexDecimal = 10 + hexChar - 'a';
        } else if ('A' <= hexChar && hexChar <= 'F') {
          hexDecimal = 10 + hexChar - 'A';
        } else {
          uart16550_puts(PROGNAME);
          uart16550_puts(": invalid hexadecimal character.\n");
        }
        file_address_array[file_count - 1] =
            file_address_array[file_count - 1] * 16 + hexDecimal;
      }
    }
  }

  return file_count;
}

void console_get_files(int file_count, long int file_address_array[4],
                       char *file_start_addr, char file_name_array[4][50],
                       int file_sizes[4]) {
  int i = 0;
  char *file_addr = NULL;
  for (i = 0; i < file_count; i++) {
    file_addr = (char *)(file_start_addr + file_address_array[i]);
    // Receive data from console via Ethernet
    file_sizes[i] = uart_recvfile_ethernet(file_name_array[i]);
    eth_rcv_file(file_addr, file_sizes[i]);
  }
}

void program_flash(int file_count, long int file_address_array[4],
                   char *file_start_addr, int file_sizes[4]) {
  int i = 0;
  unsigned int flash_addr = 0x0;
  char *prog_data = NULL;
  int next_subsector = 0;

  // erase SPI Flash
  flash_addr = FLASH_FILE_SIZE_OFFSET;
  spiflash_erase_address_range(flash_addr, 4 * file_count);

  // store file sizes
  prog_data = (char *)file_sizes;
  spiflash_memProgram(prog_data, 4 * file_count, flash_addr);

  for (i = 0; i < file_count; i++) {
    flash_addr = FLASH_FIRMWARE_OFFSET + (next_subsector * SUBSECTOR_SIZE);
    prog_data = file_start_addr + file_address_array[i];
    spiflash_erase_address_range(flash_addr, file_sizes[i]);
    printf("Program %d: addr: %p\tflash: %x\tsize: %d\n", i, prog_data,
           flash_addr, file_sizes[i]);
    spiflash_memProgram(prog_data, file_sizes[i], flash_addr);
    printf("Program %d: complete\n", i);
    next_subsector += (((file_sizes[i] + SUBSECTOR_SIZE - 1) / SUBSECTOR_SIZE));
  }
}

void read_flash(int file_count, long int file_address_array[4],
                char *file_start_addr) {
  int i = 0;
  int sample = 0;
  unsigned int *read_array = NULL;
  unsigned int spi_data = 0;
  unsigned int flash_file_start = 0;
  int read_cnt = 0, read_total = 0;
  int file_sizes[4] = {0};
  int next_subsector = 0;

  // get file sizes
  for (sample = 0; sample < 4 * file_count; sample = sample + 4) {
    file_sizes[sample >> 2] = spiflash_readmem(FLASH_FILE_SIZE_OFFSET + sample);
  }

  for (i = 0; i < file_count; i++) {
    read_array = (unsigned int *)(file_start_addr + file_address_array[i]);
    flash_file_start =
        FLASH_FIRMWARE_OFFSET + (next_subsector * SUBSECTOR_SIZE);
    read_total = file_sizes[i] / 4;
    read_cnt = 0;

    printf("Read %d: flash: %x\tmem: %p\tsize: %d\n", i, flash_file_start,
           read_array, file_sizes[i]);
    for (sample = 0; sample < file_sizes[i]; sample = sample + 4) {
      read_array[sample >> 2] = spiflash_readmem(flash_file_start + sample);
      // progress every 10%
      if (read_cnt % (read_total / 10) == 0) {
        printf("\tRead %d: %d%%\n", i, read_cnt * 100 / read_total);
      }
      read_cnt++;
    }
    next_subsector += (((file_sizes[i] + SUBSECTOR_SIZE - 1) / SUBSECTOR_SIZE));
  }
}

int main() {
  int run_linux = 0;
  int file_size;
  char *prog_start_addr;

  // init uart
  uart16550_init(UART0_BASE, FREQ / (16 * BAUD));

  // connect with console
  do {
    if (uart16550_txready())
      uart16550_putc((char)ENQ);
  } while (!uart16550_rxready());

  // welcome message
  uart16550_puts(PROGNAME);
  uart16550_puts(": connected!\n");

  uart16550_puts(PROGNAME);
  uart16550_puts(": DDR in use and program runs from DDR\n");

  // address to copy firmware to
  prog_start_addr = (char *)(EXT_MEM);

  while (uart16550_getc() != ACK) {
    uart16550_puts(PROGNAME);
    uart16550_puts(": Waiting for Console ACK.\n");
  }

#ifndef IOB_SYSTEM_LINUX_INIT_MEM
  // Init ethernet and printf (for ethernet)
  printf_init(&uart16550_putc);

  eth_init(ETH0_BASE, &clear_cache);
  // Use custom memory alloc/free functions to ensure it allocates in external
  // memory
  eth_init_mem_alloc(&mem_alloc, &mem_free);
  // Wait for PHY reset to finish
  eth_wait_phy_rst();

  char boot_flow[20] = {0};

  file_size = uart16550_recvfile("boot.flow", boot_flow);
  if (file_size > 20) {
    printf("Error: boot.flow file size is too large\n");
    return -1;
  }

  file_size =
      uart16550_recvfile("../iob_system_linux_mem.config", prog_start_addr);

  // compute_mem_load_txt
  char file_name_array[4][50];
  long int file_address_array[4];
  int file_sizes[4] = {0};
  int file_count = compute_mem_load_txt(file_name_array, file_address_array,
                                        prog_start_addr, file_size);

  if (!strcmp(boot_flow, "CONSOLE_TO_FLASH")) {
    uart16550_puts(PROGNAME);
    uart16550_puts(": CONSOLE_TO_FLASH\n");
    // init spi flash controller
    spiflash_init(SPI0_BASE);
    // Read files from console
    console_get_files(file_count, file_address_array, prog_start_addr,
                      file_name_array, file_sizes);
    program_flash(file_count, file_address_array, prog_start_addr, file_sizes);
  } else if (!strcmp(boot_flow, "FLASH_TO_EXTMEM")) {
    uart16550_puts(PROGNAME);
    uart16550_puts(": FLASH_TO_EXTMEM\n");
    // init spi flash controller
    spiflash_init(SPI0_BASE);
    read_flash(file_count, file_address_array, prog_start_addr);
  } else {
    uart16550_puts(PROGNAME);
    uart16550_puts(": CONSOLE_TO_EXTMEM\n");
    // Read files from console to external memory
    console_get_files(file_count, file_address_array, prog_start_addr,
                      file_name_array, file_sizes);
  }

  // Check if running Linux
  for (int i = 0; i < file_count; i++) {
    if (!strcmp(file_name_array[i], "rootfs.cpio.gz")) {
#ifdef SIMULATION
      // Running Linux: setup required dependencies
      uart16550_sendfile("test.log", 12, "Test passed!");
      uart16550_putc((char)DC1);
#endif
      run_linux = 1;
      break;
    }
  }
#else // INIT_MEM = 1
#ifdef IOB_SYSTEM_LINUX_RUN_LINUX
  // Running Linux: setup required dependencies
  uart16550_sendfile("test.log", 12, "Test passed!");
  uart16550_putc((char)DC1);
#endif
#endif

  // Clear CPU registers, to not pass arguments to the next
  asm volatile("li a0,0");
  asm volatile("li a1,0");
  asm volatile("li a2,0");
  asm volatile("li a3,0");
  asm volatile("li a4,0");
  asm volatile("li a5,0");
  asm volatile("li a6,0");
  asm volatile("li a7,0");

  // run firmware
  uart16550_puts(PROGNAME);
  uart16550_puts(": Restart CPU to run user program...\n");
  uart16550_txwait();

#ifndef SIMULATION
  // Terminate console if running Linux on FPGA
  if (run_linux)
    uart16550_finish();
#endif
}
