#include "iob_eth.h"
#include "iob_eth_defines.h"
#include "printf.h"

// Frame template (includes every field of the frame before the payload)
static char TEMPLATE[TEMPLATE_LEN];

// Function to clear cache
static void (*clear_cache)(void);
// Functions to alloc and clear memory
static void *(*mem_alloc)(size_t) = &malloc;
static void (*mem_free)(void *) = &free;

/*******************************************/
/********** AUXILIAR FUNCTIONS *************/
/*******************************************/

/* read integer value
 * return number of bytes read */
static int get_int(char *ptr, unsigned int *i_val) {
  *i_val = (unsigned char)ptr[3];
  *i_val <<= 8;
  *i_val += (unsigned char)ptr[2];
  *i_val <<= 8;
  *i_val += (unsigned char)ptr[1];
  *i_val <<= 8;
  *i_val += (unsigned char)ptr[0];
  return sizeof(int);
}

/* write integer value to ptr position */
static void set_int(char *ptr, unsigned int i_val) {
  ptr[0] = i_val & 0xFF;
  i_val >>= 8;
  ptr[1] = i_val & 0xFF;
  i_val >>= 8;
  ptr[2] = i_val & 0xFF;
  i_val >>= 8;
  ptr[3] = i_val & 0xFF;
  return;
}

static void print_buffer(char *buffer, int size) {
  if (buffer == NULL || size < 1) {
    printf("DEBUG print buffer: invalid inputs\n");
    return;
  }
  int i = 0, ch = 0;
  char HexTable[17] = "0123456789abcdef";
  printf("\tDEBUG: Buffer:");
  for (i = 0; i < size; i++) {
    ch = (int)((unsigned char)buffer[i]);
    printf("%c%c ", HexTable[ch >> 4], HexTable[ch & 0xF]);
  }
  printf("\n\n");
  return;
}

/*******************************************/
/*********** ETHERNET DRIVERS **************/
/*******************************************/

void eth_init(int base_address, void (*clear_cache_func)(void)) {
  eth_init_clear_cache(clear_cache_func);
#ifdef LOOPBACK
  eth_init_mac(base_address, ETH_MAC_ADDR, ETH_MAC_ADDR);
#else
  eth_init_mac(base_address, ETH_MAC_ADDR, ETH_RMAC_ADDR);
#endif
  eth_reset_bd_memory();
}

void eth_init_clear_cache(void (*clear_cache_func)(void)) {
  clear_cache = clear_cache_func;
}

// Use custom memory allocator
void eth_init_mem_alloc(void *(*mem_alloc_func)(size_t),
                        void (*mem_free_func)(void *)) {
  mem_alloc = mem_alloc_func;
  mem_free = mem_free_func;
}

void eth_init_mac(int base_address, uint64_t mac_addr, uint64_t dest_mac_addr) {
  int i, ret;

  // set base address
  IOB_ETH_INIT_BASEADDR(base_address);

  // dest mac address
  for (i = 0; i < IOB_ETH_MAC_ADDR_LEN; i++) {
    TEMPLATE[MAC_DEST_PTR + i] = dest_mac_addr >> 40;
    dest_mac_addr = dest_mac_addr << 8;
  }

  // source mac address
  for (i = 0; i < IOB_ETH_MAC_ADDR_LEN; i++) {
    TEMPLATE[MAC_SRC_PTR + i] = mac_addr >> 40;
    mac_addr = mac_addr << 8;
  }

#ifdef ETH_DEBUG_PRINT
  printf("\nSender: ");
  for (i = 0; i < IOB_ETH_MAC_ADDR_LEN; i++) {
    printf("%02x ", (unsigned char)TEMPLATE[MAC_SRC_PTR + i]);
  }
  printf("\nDest: ");
  for (i = 0; i < IOB_ETH_MAC_ADDR_LEN; i++) {
    printf("%02x ", (unsigned char)TEMPLATE[MAC_DEST_PTR + i]);
  }
  printf("\n");
#endif

  // eth type
  TEMPLATE[ETH_TYPE_PTR] = ETH_TYPE_H;
  TEMPLATE[ETH_TYPE_PTR + 1] = ETH_TYPE_L;

  // reset core
  // IOB_ETH_SET_SOFTRST(1);
  // IOB_ETH_SET_SOFTRST(0);

  //// wait for PHY to produce rx clock
  // while (!((IOB_ETH_GET_STATUS() >> 3) & 1));

  //#ifdef ETH_DEBUG_PRINT
  // printf("Ethernet RX clock detected\n");
  //#endif

  //// wait for PLL to lock and produce tx clock
  // while (!((IOB_ETH_GET_STATUS() >> 15) & 1));

  //#ifdef ETH_DEBUG_PRINT
  // printf("Ethernet TX PLL locked\n");
  //#endif

  //// set initial payload size to Ethernet minimum excluding FCS
  // IOB_ETH_SET_TX_NBYTES(46);

  //// check processor interface
  //// write dummy register
  // IOB_ETH_SET_DUMMY_W(0xDEADBEEF);

  //// read and check result
  // if (IOB_ETH_GET_DUMMY_R() != 0xDEADBEEF) {
  //   printf("Ethernet Init failed\n");
  // } else {
  //   printf("Ethernet Core Initialized\n");
  // }
}

// Reset buffer descriptor memory
void eth_reset_bd_memory() {
  // Reset 128 buffer descriptors (64 bits each)
  for (int i = 0; i < 256; i++) {
    IOB_ETH_SET_BD(0x00000000, i);
  }
}

// Get payload size from given buffer descriptor
unsigned short int eth_get_payload_size(unsigned int idx) {
  return IOB_ETH_GET_BD(idx << 1) >> 16;
}

// Set payload size in given buffer descriptor
void eth_set_payload_size(unsigned int idx, unsigned int size) {
  IOB_ETH_SET_BD((IOB_ETH_GET_BD(idx << 1) & 0x0000ffff) | size << 16,
                 idx << 1);
}

void eth_send_frame(char *data, unsigned int size) {
  int i;

  // wait for ready
  while (!eth_tx_ready(0))
    ;

  // Alloc memory for frame
  char *frame_ptr = (char *)(*mem_alloc)(TEMPLATE_LEN + size);

  // Copy template to frame
  for (i = 0; i < TEMPLATE_LEN; i++)
    frame_ptr[i] = TEMPLATE[i];

  // Copy payload to frame
  for (i = 0; i < size; i++)
    frame_ptr[i + TEMPLATE_LEN] = data[i];

  /* Buffer descriptor configuration */

  // set frame pointer
  eth_set_ptr(0, frame_ptr);
  // set frame size
  eth_set_payload_size(0, TEMPLATE_LEN + size);

  // Set ready bit; Enable CRC and PAD; Set as last descriptor; Enable
  // interrupt.
  eth_set_ready(0, 1);
  eth_set_crc(0, 1);
  eth_set_pad(0, 1);
  eth_set_wr(0, 1);
  eth_set_interrupt(0, 1);

  // start sending
  eth_send(1);

  // wait for ready
  while (!eth_tx_ready(0))
    ;

  // Disable transmission and free memory
  eth_send(0);
  (*mem_free)(frame_ptr);

  return;
}

int eth_rcv_frame(char *data_rcv, unsigned int size, int timeout) {
  int i;
  int cnt = timeout;
  int ignore;

  // Alloc memory for frame
  volatile char *frame_ptr =
      (volatile char *)(*mem_alloc)(HDR_LEN + ETH_NBYTES + 4);

  // Copy template to frame
  // for (i=0; i < TEMPLATE_LEN; i++)
  //  frame_ptr[i] = TEMPLATE[i];

  do {
    // set frame pointer
    eth_set_ptr(64, frame_ptr);

    // Mark empty; Set as last descriptor; Enable interrupt.
    eth_set_empty(64, 1);
    eth_set_wr(64, 1);
    eth_set_interrupt(64, 1);

    // Enable reception
    eth_receive(1);

    // wait until data received
    while (!eth_rx_ready(64)) {
      timeout--;
      if (!timeout) {
        eth_receive(0);
        (*mem_free)((char *)frame_ptr);
        return ETH_NO_DATA;
      }
    }

    if (eth_bad_crc(64)) {
      eth_receive(0);
      (*mem_free)((char *)frame_ptr);
      printf("Bad CRC\n");
      return ETH_INVALID_CRC;
    }

    // Disable reception
    eth_receive(0);

    // Clear cache
    (*clear_cache)();

    // Check destination MAC address to see if should ignore frame
    ignore = 0;
    for (i = 0; i < IOB_ETH_MAC_ADDR_LEN; i++)
      if (TEMPLATE[MAC_SRC_PTR + i] != frame_ptr[MAC_DEST_PTR + i]) {
        ignore = 1;
        break;
      }

  } while (ignore);

  // Copy payload to return array
  for (i = 0; i < size; i++) {
    data_rcv[i] = frame_ptr[i + TEMPLATE_LEN];
  }

  (*mem_free)((char *)frame_ptr);

  return ETH_DATA_RCV;
}

#define MAX(A, B) ((A) > (B) ? (A) : (B))

static unsigned int rcv_timeout = 500000;
static char buffer[ETH_NBYTES + HDR_LEN];

void eth_set_receive_timeout(unsigned int timeout) { rcv_timeout = timeout; }

static void SyncAckFirst() {
  while (1) {
    // Send frame
    eth_send_frame(
        buffer,
        ETH_MINIMUM_NBYTES); // Do not care what we send, any frame is the ack

    // Wait to receive ack
    if (eth_rcv_frame(buffer, ETH_MINIMUM_NBYTES, rcv_timeout) == ETH_DATA_RCV)
      break;
  }
}

static void SyncAckLast() {
  // Wait to receive frame
  while (1) {
    // Wait to receive ack
    if (eth_rcv_frame(buffer, ETH_MINIMUM_NBYTES, rcv_timeout) == ETH_DATA_RCV)
      break;
  }

  eth_send_frame(
      buffer,
      ETH_MINIMUM_NBYTES); // Do not care what we send, any frame is the ack
}

static unsigned int eth_rcv_file_impl(char *data, int size) {
  int num_frames = ((size - 1) / ETH_NBYTES) + 1;
  unsigned int bytes_to_receive;
  unsigned int count_bytes = 0;
  int i, j;

  // Loop to receive intermediate data frames
  for (j = 0; j < num_frames; j++) {

    // check if it is last packet (has less data that full payload size)
    if (j == (num_frames - 1))
      bytes_to_receive = size - count_bytes;
    else
      bytes_to_receive = ETH_NBYTES;

    // wait to receive frame
    while (eth_rcv_frame(&data[count_bytes], bytes_to_receive, rcv_timeout))
      ;

    // send data back as ack
    eth_send_frame(&data[count_bytes],
                   MAX(bytes_to_receive, ETH_MINIMUM_NBYTES));

    // update byte counter
    count_bytes += bytes_to_receive;
  }

  return count_bytes;
}

static unsigned int eth_send_file_impl(char *data, int size) {
  int num_frames = ((size - 1) / ETH_NBYTES) + 1;
  unsigned int bytes_to_send;
  unsigned int count_bytes = 0;
  unsigned int error_bytes = 0;
  int i, j;

  // Loop to send data
  for (j = 0; j < num_frames; j++) {

    // check if it is last packet (has less data that full payload size)
    if (j == (num_frames - 1))
      bytes_to_send = size - count_bytes;
    else
      bytes_to_send = ETH_NBYTES;

    // send frame
    eth_send_frame(&data[count_bytes], MAX(bytes_to_send, ETH_MINIMUM_NBYTES));

    // wait to receive frame as ack
    while (eth_rcv_frame(buffer, bytes_to_send, rcv_timeout))
      ;

    for (int i = 0; i < bytes_to_send; i++) {
      if (buffer[i] != data[count_bytes + i]) {
        error_bytes += 1;
        // printf("Error byte %d: %x %x\n",i,buffer[i], data[count_bytes + i]);
        // //DEBUG
      }
    }

    // update byte counter
    count_bytes += bytes_to_send;
  }

  printf("File transmitted with %d errors...\n", error_bytes);

  return count_bytes;
}

unsigned int eth_rcv_file(char *data, int size) {

  SyncAckLast();

  return eth_rcv_file_impl(data, size);
}

unsigned int eth_send_file(char *data, int size) {

  SyncAckFirst();

  return eth_send_file_impl(data, size);
}

unsigned int eth_rcv_variable_file(char *data) {
  unsigned int size = 0;

  SyncAckLast();

  // Receive file size
  while (eth_rcv_frame(buffer, ETH_MINIMUM_NBYTES, rcv_timeout))
    ;

  // Send data back as ack
  eth_send_frame(buffer, ETH_MINIMUM_NBYTES);
  get_int(buffer, &size);

  return eth_rcv_file_impl(data, size);
}

unsigned int eth_send_variable_file(char *data, int size) {

  SyncAckFirst();

  // Send size
  set_int(buffer, size);
  eth_send_frame(buffer, ETH_MINIMUM_NBYTES);

  // Wait for ack
  while (eth_rcv_frame(buffer, ETH_MINIMUM_NBYTES, rcv_timeout))
    ;

  // Transfer file
  return eth_send_file_impl(data, size);
}

void eth_wait_phy_rst() {
  while (IOB_ETH_GET_PHY_RST_VAL())
    ;
}

void eth_print_status(void) {
  printf("tx_ready = %x\n", eth_tx_ready(0));
  printf("rx_ready = %x\n", eth_rx_ready(0));
  printf("Bad CRC = %x\n", eth_bad_crc(0));
}
