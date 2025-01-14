/* PC Emulation of ETHERNET peripheral */

#include <fcntl.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include "iob-eth.h"
#include "iob_eth_conf.h"
#include "iob_eth_csrs.h"

#define BUFFER_SIZE 2048
#define SOCKET_NAME "/tmp/tmpLocalSocket"

static int data_socket = -1;
static int connection_socket = -1;

/* dest mac | src mac | eth type*/
static char TX_FRAME[14];

static char send_buffer[BUFFER_SIZE];
static char rcv_buffer[BUFFER_SIZE];
static char rcv_buffer_int[BUFFER_SIZE];
static int rcv_size_reg = 0;
static uint16_t tx_nbytes_reg = 0;
static uint32_t dummy_reg = 0;

struct tx_bd {
  bool cs : 1;      // Carrier sense lost
  bool df : 1;      // Defer indication
  bool lc : 1;      // Late collision
  bool rl : 1;      // Retransmission limit
  uint8_t rtry : 4; // Retry count
  bool ur : 1;      // Underrun
  uint8_t reserved0 : 2;
  bool crc : 1;      // CRC enable
  bool pad : 1;      // Pad enable
  bool wr : 1;       // Wrap
  bool irq : 1;      // Interrupt Request Enable
  bool rd : 1;       // Ready for transmission
  uint16_t len : 16; // Frame length to be transmitted
  void *ptr;         // Transmit pointer
};
struct rx_bd {
  bool lc : 1;  // Late collision
  bool crc : 1; // CRC error
  bool sf : 1;  // Short frame
  bool tl : 1;  // Too Long
  bool dn : 1;  // Dribble Nibble
  bool is : 1;  // Invalid symbol
  bool or : 1;  // Overrun
  bool m : 1;   // Miss;
  bool cf : 1;  // Control Frame
  uint8_t reserved0 : 4;
  bool wr : 1;       // Wrap
  bool irq : 1;      // Interrupt Request Enable
  bool e : 1;        // Empty (ready to receive)
  uint16_t len : 16; // Received frame length
  char *ptr;         // Receive pointer
};
union bd {
  uint32_t val[2];
  struct tx_bd tx;
  struct rx_bd rx;
};

// BD memory
static union bd bd_list[1 << IOB_ETH_BD_NUM_LOG2];

/*****************************
 * Registers
 ****************************/

static union {
  uint32_t val;
  struct {
    bool rxen : 1;
    bool txen : 1;
    bool nopre : 1;
    bool bro : 1;
    bool iam : 1;
    bool pro : 1;
    bool ifg : 1;
    bool loopbck : 1;
    bool nobckof : 1;
    bool exdfren : 1;
    bool fulld : 1;
    bool reserved0 : 1;
    bool dlycrcen : 1;
    bool crcen : 1;
    bool hugen : 1;
    bool pad : 1;
    bool recsmall : 1;
    uint16_t reserved1 : 15;
  } fields;
} moder = {0x00a0};

// int_source
// int_mask
// ipgt
// ipgr1
// ipgr2
// packetlen
// collconf

static uint8_t tx_bd_num = 0x40;

// ctrlmoder
// miimoder
// miicommand
// miiaddress
// miitx_data
// miirx_data
// miistatus
// mac_addr0
// mac_addr1
// hash0
// hash1
// txctrl

static int base;

/*****************************
 * PC emulation functions
 ****************************/

/* Reset AF_UNIX Socket
 */
static void reset_socket() {
  struct sockaddr_un name;
  int ret = 0;

  /* remove socket if it exists*/
  unlink(SOCKET_NAME);

  /*create socket to receive connections */
  // TODO: Use SOCK_RAW instead of AF_UNIX
  connection_socket = socket(AF_UNIX, SOCK_SEQPACKET, 0);
  /* check for errors */
  if (connection_socket == -1) {
    perror("Failed to create socket");
    exit(EXIT_FAILURE);
  }
  /*clear structure*/
  memset(&name, 0, sizeof(struct sockaddr_un));

  /*bind socket*/
  name.sun_family = AF_UNIX;
  strncpy(name.sun_path, SOCKET_NAME, sizeof(name.sun_path) - 1);

  ret = bind(connection_socket, (const struct sockaddr *)&name,
             sizeof(struct sockaddr_un));
  /* check for errors */
  if (ret == -1) {
    printf("Failed to bind socket");
    exit(EXIT_FAILURE);
  }

  /* wait for eth_comm connections */
  ret = listen(connection_socket, 1);
  /* check for errors */
  if (ret == -1) {
    printf("Error in listen");
    exit(EXIT_FAILURE);
  }
  printf("Waiting for client connection...\n");

  // /* accept connection */
  // data_socket = accept(connection_socket, NULL, NULL);
  // /* check for errors */
  // if(data_socket == -1){
  //     printf("Failed to accept connection\n");
  //     exit(EXIT_FAILURE);
  // }
  return;
}

static unsigned int current_tx_bd = 0;
static unsigned int current_rx_bd = 0x40; // Default equals to tx_bd_num

/* pc emulation functions
 * this AF_UNIX socket is used to emulate the ethernet communication
 * a Raw Ethernet Frame has the following fields:
 * [ Preamble | SFD | DST MAC | SRC MAC | ETH Type | Payload Data | CRC
 * (implicit) ] but the pc-emul version only sends and receives: [ DST MAC | SRC
 * MAC | ETH Type | Payload Data | CRC (implicit) ] (the preamble and SDF bytes
 * are not transfered)
 */
static void send_frame() {
  // write data to socket
  int wret = -1;
  // by default try to write data
  wret = send(data_socket, bd_list[current_tx_bd].tx.ptr,
              bd_list[current_tx_bd].tx.len, MSG_NOSIGNAL);
  return;
}

static void send_frames() {
  // Run through TX BDs, starting from latest that wasn't sent
  for (int i = current_tx_bd; i < tx_bd_num; i++) {
    current_tx_bd = i;
    // Check ready bit
    if (!bd_list[i].tx.rd) {
      printf("Debug: Tx bd %d is not yet ready for transmission.\n", i);
      return;
    }

    send_frame();
    bd_list[i].tx.rd = 0;

    // Check WR bit
    if (bd_list[i].tx.wr)
      break;
  }
  current_tx_bd = 0;
}

static void receive_frame() {
  // Emulate rx_ready() behaviour to receive data
  int ret = -1;
  ret = recv(data_socket, bd_list[current_rx_bd].rx.ptr, 1 << IOB_ETH_BUFFER_W,
             MSG_DONTWAIT);
  if (ret < 1) {
    bd_list[current_rx_bd].rx.crc = 1;
    bd_list[current_rx_bd].rx.len = 0;
    printf("Error in eth receive_frame!\n");
  } else {
    bd_list[current_rx_bd].rx.crc = 0;
    bd_list[current_rx_bd].rx.len = ret;
  }
}

static void receive_frames() {
  // Run through RX BDs, starting from latest that wasn't received
  for (int i = current_rx_bd; i < (1 << IOB_ETH_BD_NUM_LOG2); i++) {
    current_rx_bd = i;
    // Check ready bit
    if (!bd_list[i].rx.e) {
      printf("Debug: Rx bd %d is not yet ready for reception (not empyt).\n",
             i);
      return;
    }

    receive_frame();
    bd_list[i].rx.e = 0;

    // Check WR bit
    if (bd_list[i].rx.wr)
      break;
  }
  current_rx_bd = tx_bd_num;
}

static void try_send() {
  if (moder.fields.txen && bd_list[current_tx_bd].tx.rd)
    send_frames();
}

static void try_receive() {
  if (moder.fields.rxen && bd_list[current_rx_bd].rx.e)
    receive_frames();
}

/*****************************
 * csrs functions
 ****************************/

void IOB_ETH_INIT_BASEADDR(uint32_t addr) {
  base = addr;
  reset_socket();
  return;
}

// Core Setters and Getters
void IOB_ETH_SET_MODER(uint32_t value) {
  moder.val = value;
  // User may have enabled transfer
  try_send();
  try_receive();
}

uint32_t IOB_ETH_GET_MODER() { return moder.val; }

void IOB_ETH_SET_INT_SOURCE(uint32_t value) {}

uint32_t IOB_ETH_GET_INT_SOURCE() { return 0; }

void IOB_ETH_SET_INT_MASK(uint32_t value) {}

uint32_t IOB_ETH_GET_INT_MASK() { return 0; }

void IOB_ETH_SET_IPGT(uint32_t value) {}

uint32_t IOB_ETH_GET_IPGT() { return 0; }

void IOB_ETH_SET_IPGR1(uint32_t value) {}

uint32_t IOB_ETH_GET_IPGR1() { return 0; }

void IOB_ETH_SET_IPGR2(uint32_t value) {}

uint32_t IOB_ETH_GET_IPGR2() { return 0; }

void IOB_ETH_SET_PACKETLEN(uint32_t value) {}

uint32_t IOB_ETH_GET_PACKETLEN() { return 0; }

void IOB_ETH_SET_COLLCONF(uint32_t value) {}

uint32_t IOB_ETH_GET_COLLCONF() { return 0; }

void IOB_ETH_SET_TX_BD_NUM(uint32_t value) { tx_bd_num = (uint8_t)value; }

uint32_t IOB_ETH_GET_TX_BD_NUM() { return tx_bd_num; }

void IOB_ETH_SET_CTRLMODER(uint32_t value) {}

uint32_t IOB_ETH_GET_CTRLMODER() { return 0; }

void IOB_ETH_SET_MIIMODER(uint32_t value) {}

uint32_t IOB_ETH_GET_MIIMODER() { return 0; }

void IOB_ETH_SET_MIICOMMAND(uint32_t value) {}

uint32_t IOB_ETH_GET_MIICOMMAND() { return 0; }

void IOB_ETH_SET_MIIADDRESS(uint32_t value) {}

uint32_t IOB_ETH_GET_MIIADDRESS() { return 0; }

void IOB_ETH_SET_MIITX_DATA(uint32_t value) {}

uint32_t IOB_ETH_GET_MIITX_DATA() { return 0; }

void IOB_ETH_SET_MIIRX_DATA(uint32_t value) {}

uint32_t IOB_ETH_GET_MIIRX_DATA() { return 0; }

void IOB_ETH_SET_MIISTATUS(uint32_t value) {}

uint32_t IOB_ETH_GET_MIISTATUS() { return 0; }

void IOB_ETH_SET_MAC_ADDR0(uint32_t value) {}

uint32_t IOB_ETH_GET_MAC_ADDR0() { return 0; }

void IOB_ETH_SET_MAC_ADDR1(uint32_t value) {}

uint32_t IOB_ETH_GET_MAC_ADDR1() { return 0; }

void IOB_ETH_SET_ETH_HASH0_ADR(uint32_t value) {}

uint32_t IOB_ETH_GET_ETH_HASH0_ADR() { return 0; }

void IOB_ETH_SET_ETH_HASH1_ADR(uint32_t value) {}

uint32_t IOB_ETH_GET_ETH_HASH1_ADR() { return 0; }

void IOB_ETH_SET_ETH_TXCTRL(uint32_t value) {}

uint32_t IOB_ETH_GET_ETH_TXCTRL() { return 0; }

// No DMA interface
uint8_t IOB_ETH_GET_TX_BD_CNT() { return 0; }

uint8_t IOB_ETH_GET_RX_BD_CNT() { return 0; }

uint32_t IOB_ETH_GET_TX_WORD_CNT() { return 0; }

uint32_t IOB_ETH_GET_RX_WORD_CNT() { return 0; }

void IOB_ETH_SET_FRAME_WORD(uint32_t value) {}

uint32_t IOB_ETH_GET_FRAME_WORD() { return 0; }

uint8_t IOB_ETH_GET_PHY_RST_VAL() { return 0; }

// Buffer descriptors
void IOB_ETH_SET_BD(uint32_t value, int addr) {
  bd_list[addr >> 1].val[addr & 1] = value;
  // User may have changed ready bits
  if ((addr >> 1) < tx_bd_num)
    try_send();
  else
    try_receive();
}

uint32_t IOB_ETH_GET_BD(int addr) { return bd_list[addr >> 1].val[addr & 1]; }

uint16_t IOB_ETH_GET_VERSION() { return IOB_ETH_VERSION; }
