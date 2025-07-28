#include "iob-dma-user.h"

#define IOB_DMA_PAGE_SIZE 4096
/* Calculate memory map length
 * - size: number of 32-bit words to transfer
 *
 */
static size_t mmap_length(uint32_t size) {
  size_t mmap_length = 0;
  uint32_t page_mult =
      ((size << 2) + IOB_DMA_PAGE_SIZE - 1) / IOB_DMA_PAGE_SIZE;
  mmap_length = page_mult * IOB_DMA_PAGE_SIZE;
  return mmap_length;
}

/* DMA transfer:
 * - data_ptr: pointer to data for read or write according to [direction].
 * - size: ammount of 32-bit words to transfer
 * - direction: 0 = read from memory, 1 = write to memory
 * - interface_number: which AXI Stream interface to use
 *
 * returns 0 on success, -1 on error
 */
int dma_start_transfer(uint32_t *data_ptr, uint32_t size, int direction,
                       uint16_t interface_number) {
  int fd = 0;
  void *virt_addr = NULL;

  // open the device file
  fd = open(IOB_DMA_DEVICE_FILE, O_RDWR);
  if (fd < 0) {
    printf("Error opening device file: %s\n", IOB_DMA_DEVICE_FILE);
    return -1;
  }

  // NOTE: driver call to mmap() sets DMA physical base address
  // iob_sysfs_write_file(IOB_DMA_SYSFILE_BASE_ADDR, base_addr);
  virt_addr =
      mmap(NULL, mmap_length(size), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  if (virt_addr == MAP_FAILED) {
    printf("Error mapping memory\n");
    close(fd);
    return -1;
  }

  iob_sysfs_write_file(IOB_DMA_SYSFILE_DIRECTION, direction);
  iob_sysfs_write_file(IOB_DMA_SYSFILE_INTERFACE_NUM, interface_number);

  // MEM -> DEVICE transfers: copy user buffer to DMA memory
  if (direction == 0) {
    memcpy(virt_addr, data_ptr, size << 2);
  }

  // Setting the transfer size will begin the transfer
  iob_sysfs_write_file(IOB_DMA_SYSFILE_TRANSFER_SIZE, size);

  while (dma_transfer_ready() == 0) {
    // wait for transfer to complete
  }

  // DEVICE -> MEM transfers: copy DMA memory to user buffer
  if (direction == 1) {
    memcpy(data_ptr, virt_addr, size << 2);
  }

  close(fd);
  return 0;
}

// Check if DMA is ready for new transfer
uint8_t dma_transfer_ready() {
  uint32_t ready_r = 0;
  uint32_t ready_w = 0;
  iob_sysfs_read_file(IOB_DMA_SYSFILE_READY_R, &ready_r);
  iob_sysfs_read_file(IOB_DMA_SYSFILE_READY_W, &ready_w);
  return (ready_w && ready_r);
}
