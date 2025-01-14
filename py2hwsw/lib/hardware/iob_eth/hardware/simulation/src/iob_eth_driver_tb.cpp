#include "iob_eth_driver_tb.h"
#include "iob_eth_defines_verilator.h"

static FILE *eth2soc_fd;
static FILE *soc2eth_fd;

static void cpu_initeth(iob_native_t *eth_if);
static void relay_frame_file_2_eth(iob_native_t *eth_if);
static void relay_frame_eth_2_file(int frame_size, iob_native_t *eth_if);

// Call this function once at start up
void eth_setup(iob_native_t *eth_if) {
  // init cpu bus signals
  *(eth_if->iob_valid) = 0;
  *(eth_if->iob_wstrb) = 0;

  // configure eth
  cpu_initeth(eth_if);

  while ((eth2soc_fd = fopen("./eth2soc", "rb")) == NULL)
    ;
  fclose(eth2soc_fd);
  soc2eth_fd = fopen("./soc2eth", "wb");
}

// Call this function in main loop to keep relaying frames form file to core and
// vice versa
void eth_relay_frames(iob_native_t *eth_if) {
  int rx_nbytes_reg = 0;

  // Relay ethernet frames from core to file
  rx_nbytes_reg = IOB_ETH_GET_RX_NBYTES(eth_if);
  if (rx_nbytes_reg) {
    // VL_PRINTF("$eth2file\n");  // DEBUG
    relay_frame_eth_2_file(rx_nbytes_reg, eth_if);
    // VL_PRINTF("$eth2file_done\n");  // DEBUG
  }
  // Relay ethernet frames from file to core
  if (eth_tx_ready(0, eth_if)) {
    // Try to open file
    eth2soc_fd = fopen("./eth2soc", "rb");
    if (!eth2soc_fd) {
      // wait 1 ms and try again
      usleep(1000);
      eth2soc_fd = fopen("./eth2soc", "rb");
      if (!eth2soc_fd) {
        fclose(soc2eth_fd);
        exit(1);
      }
    }
    // Read file contents
    relay_frame_file_2_eth(eth_if);
  }
}

static void relay_frame_file_2_eth(iob_native_t *eth_if) {
  unsigned char size_l, size_h, frame_byte;
  unsigned short int frame_size;
  unsigned int i, n;

  // Read frame size (2 bytes)
  n = fscanf(eth2soc_fd, "%c%c", &size_l, &size_h);
  // Continue if size read successfully
  if (n == 2) {
    frame_size = (size_h << 8) | size_l;
    // VL_PRINTF("$file2eth received %d bytes.\n", frame_size);  // DEBUG
    //  wait for ready
    while (!eth_tx_ready(0, eth_if))
      ;
    // set frame size
    eth_set_payload_size(0, frame_size, eth_if);
    // Set ready bit
    eth_set_ready(0, 1, eth_if);

    // Read RAW frame from binary encoded file, byte by byte
    for (i = 0; i < frame_size; i = i) {
      n = fscanf(eth2soc_fd, "%c", &frame_byte);
      if (n > 0) {
        IOB_ETH_SET_FRAME_WORD(frame_byte, eth_if);
        i = i + 1;
      }
    }
    fclose(eth2soc_fd);
    // Delete frame from file
    eth2soc_fd = fopen("./eth2soc", "wb");
    // VL_PRINTF("$file2eth_done\n");  // DEBUG
  } // n != 0
  fclose(eth2soc_fd);
}

static void relay_frame_eth_2_file(int frame_size, iob_native_t *eth_if) {
  char frame_byte;
  unsigned int i;

  // Write two bytes with frame size
  fprintf(soc2eth_fd, "%c%c", frame_size & 0xff, (frame_size >> 8) & 0x07);

  // Read frame bytes from core and write to file
  for (i = 0; i < frame_size; i = i + 1) {
    frame_byte = IOB_ETH_GET_FRAME_WORD(eth_if);
    fprintf(soc2eth_fd, "%c", frame_byte);
  }
  fflush(soc2eth_fd);

  // Wait for BD status update (via ready/empty bit)
  while (!eth_rx_ready(64, eth_if))
    ;

  // Check bad CRC
  if (eth_bad_crc(64, eth_if))
    VL_PRINTF("Bad CRC!\n");

  // Mark empty to allow receive next frame
  eth_set_empty(64, 1, eth_if);
}

static void cpu_initeth(iob_native_t *eth_if) {
  eth_reset_bd_memory(eth_if);

  /**** Configure receiver *****/
  // Mark empty; Set as last descriptor; Enable interrupt.
  eth_set_empty(64, 1, eth_if);
  eth_set_wr(64, 1, eth_if);
  eth_set_interrupt(64, 1, eth_if);

  // Enable reception
  eth_receive(1, eth_if);

  /**** Configure transmitter *****/
  // Enable CRC and PAD; Set as last descriptor; Enable interrupt.
  eth_set_crc(0, 1, eth_if);
  eth_set_pad(0, 1, eth_if);
  eth_set_wr(0, 1, eth_if);
  eth_set_interrupt(0, 1, eth_if);

  // enable transmission
  eth_send(1, eth_if);
}
