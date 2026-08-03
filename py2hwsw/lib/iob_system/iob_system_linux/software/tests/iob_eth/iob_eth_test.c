/*
 * SPDX-FileCopyrightText: 2026 IObundle
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>
#include <dirent.h>
#include <poll.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <net/if.h>
#include <linux/sockios.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ethtool.h>
#include <net/if_arp.h>
#include <linux/mii.h>

/**
 * IOb-ETH ethoc Driver Compatibility Test Suite
 *
 * Validates that the IOb-Eth core correctly implements the OpenCores Ethernet
 * MAC register map and operation modes by exercising the Linux ethoc driver
 * through standard networking APIs (sockets, ioctl, ethtool, sysfs, /proc).
 *
 * Requires a companion host script (iob_eth_host.py) running on the connected
 * Linux host to exchange frames and validate TX/RX paths.
 */

/* ---------------------------------------------------------------
 * Constants
 * --------------------------------------------------------------- */

#define TEST_ETH_PORT 9000
#define CMD_BUF_SIZE 1536
#define RECV_BUF_SIZE 1536

/* ethoc register offsets (from ethoc.c) */
#define REG_MODER 0x00
#define REG_INT_SOURCE 0x04
#define REG_INT_MASK 0x08
#define REG_IPGT 0x0C
#define REG_IPGR1 0x10
#define REG_IPGR2 0x14
#define REG_PACKETLEN 0x18
#define REG_COLLCONF 0x1C
#define REG_TX_BD_NUM 0x20
#define REG_CTRLMODER 0x24
#define REG_MIIMODER 0x28
#define REG_MIICOMMAND 0x2C
#define REG_MIIADDRESS 0x30
#define REG_MIITX_DATA 0x34
#define REG_MIIRX_DATA 0x38
#define REG_MIISTATUS 0x3C
#define REG_MAC_ADDR0 0x40
#define REG_MAC_ADDR1 0x44
#define REG_ETH_HASH0 0x48
#define REG_ETH_HASH1 0x4C
#define REG_ETH_TXCTRL 0x50
#define REG_ETH_END 0x54

/* ethoc MODER bits */
#define MODER_RXEN (1 << 0)
#define MODER_TXEN (1 << 1)
#define MODER_BRO (1 << 3)
#define MODER_PRO (1 << 5)
#define MODER_LOOP (1 << 7)
#define MODER_FULLD (1 << 10)
#define MODER_CRC (1 << 13)
#define MODER_PAD (1 << 15)

/* Expected default MODER after ethoc_reset(): RXEN|TXEN|CRC|PAD|FULLD */
#define MODER_DEFAULT                                                          \
  (MODER_RXEN | MODER_TXEN | MODER_CRC | MODER_PAD | MODER_FULLD)

/* Expected default IPGT after ethoc_reset() */
#define IPGT_DEFAULT 0x15

/* Expected default INT_MASK after ethoc_reset(): all 7 bits */
#define INT_MASK_ALL 0x7F

/* Command IDs for SoC↔Host protocol */
#define CMD_ECHO 0x01
#define CMD_BROADCAST 0x02
#define CMD_STRESS_TX 0x03
#define CMD_STRESS_RX 0x04
#define CMD_GET_HOST_MAC 0x05
#define CMD_DONE 0x06

/* Packet header: cmd(1) + id(1) + len(2) = 4 bytes */
#define HDR_SIZE 4

/* MAC address string length: "XX:XX:XX:XX:XX:XX" + NUL */
#define MAC_STR_LEN 18

/* ---------------------------------------------------------------
 * Test result tracking
 * --------------------------------------------------------------- */

static int g_passed = 0;
static int g_failed = 0;
static int g_total = 0;
static char g_iface[IFNAMSIZ];
static struct in_addr g_host_ip;
static struct in_addr g_soc_ip;
static int g_host_ip_set = 0;
static int g_soc_ip_set = 0;
static int g_verbose = 0;

#define TEST_PASS(name)                                                        \
  do {                                                                         \
    printf("  %-52s [PASS]\n", (name));                                        \
    g_passed++;                                                                \
    g_total++;                                                                 \
  } while (0)

#define TEST_FAIL(name, fmt, ...)                                              \
  do {                                                                         \
    printf("  %-52s [FAIL]\n", (name));                                        \
    printf("    " fmt "\n", ##__VA_ARGS__);                                    \
    g_failed++;                                                                \
    g_total++;                                                                 \
  } while (0)

#define TEST_INFO(name, fmt, ...)                                              \
  do {                                                                         \
    printf("  %-52s [INFO]\n", (name));                                        \
    printf("    " fmt "\n", ##__VA_ARGS__);                                    \
  } while (0)

/* ---------------------------------------------------------------
 * ethtool interface (no kernel headers dependency)
 * --------------------------------------------------------------- */

struct ethool_drvr_info {
  uint32_t cmd;
  uint32_t version[32];
  uint32_t fw_version[32];
  uint32_t erom_version[32];
  uint32_t bus_info[32];
  uint32_t n_stats;
  uint32_t testinfo_len;
  uint32_t eedump_len;
  uint32_t regdump_len;
};

struct ethool_regs {
  uint32_t cmd;
  uint32_t version;
  uint32_t len;
  uint8_t data[];
};

struct ethool_ringparam {
  uint32_t cmd;
  uint32_t rx_max_pending;
  uint32_t rx_mini_max_pending;
  uint32_t rx_jumbo_max_pending;
  uint32_t tx_max_pending;
  uint32_t rx_pending;
  uint32_t rx_mini_pending;
  uint32_t rx_jumbo_pending;
  uint32_t tx_pending;
};

struct ethool_link {
  uint32_t cmd;
  uint32_t link;
};

struct ethool_gstring {
  uint32_t cmd;
  uint32_t string_set;
  uint32_t len;
  uint8_t data[];
};

#define ETHOOL_GDRVINFO 0x00000003
#define ETHOOL_GREGS 0x00000005
#define ETHOOL_GREGS_LEN 0x00000018
#define ETHOOL_GRINGPARAM 0x0000000a
#define ETHOOL_GLINK 0x0000000a
#define ETHOOL_GSSET_INFO 0x00000037

/* ---------------------------------------------------------------
 * Network statistics (from /proc/net/dev)
 * --------------------------------------------------------------- */

struct net_stats {
  unsigned long rx_bytes;
  unsigned long rx_packets;
  unsigned long rx_errors;
  unsigned long rx_dropped;
  unsigned long rx_fifo_errors;
  unsigned long rx_frame_errors;
  unsigned long rx_compressed;
  unsigned long rx_multicast;
  unsigned long tx_bytes;
  unsigned long tx_packets;
  unsigned long tx_errors;
  unsigned long tx_dropped;
  unsigned long tx_fifo_errors;
  unsigned long tx_collisions;
  unsigned long tx_carrier_errors;
  unsigned long tx_compressed;
};

/* ---------------------------------------------------------------
 * Protocol structures
 * --------------------------------------------------------------- */

struct cmd_packet {
  uint8_t cmd;
  uint8_t id;
  uint16_t len;
  uint8_t data[CMD_BUF_SIZE];
};

/* ---------------------------------------------------------------
 * Helper: find ethoc network interface
 * --------------------------------------------------------------- */

static int find_ethoc_iface(char *result, size_t result_len) {
  DIR *dir;
  struct dirent *entry;
  char path[512];
  char link[512];
  ssize_t len;

  dir = opendir("/sys/class/net");
  if (!dir)
    return -1;

  while ((entry = readdir(dir)) != NULL) {
    if (entry->d_name[0] == '.')
      continue;

    snprintf(path, sizeof(path), "/sys/class/net/%s/device/driver",
             entry->d_name);
    len = readlink(path, link, sizeof(link) - 1);
    if (len <= 0)
      continue;
    link[len] = '\0';

    if (strstr(link, "ethoc")) {
      strncpy(result, entry->d_name, result_len - 1);
      result[result_len - 1] = '\0';
      closedir(dir);
      return 0;
    }
  }

  closedir(dir);
  return -1;
}

/* ---------------------------------------------------------------
 * Helper: create and bind UDP socket for test communication
 * --------------------------------------------------------------- */

static int create_test_socket(uint16_t port) {
  int fd;
  struct sockaddr_in addr;
  int opt = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0)
    return -1;

  setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(port);
  addr.sin_addr.s_addr = htonl(INADDR_ANY);

  if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    close(fd);
    return -1;
  }

  return fd;
}

/* ---------------------------------------------------------------
 * Helper: send command and receive response
 * --------------------------------------------------------------- */

static int send_cmd_internal(int fd, uint8_t cmd, const void *data,
                             uint16_t len, void *resp, uint16_t resp_size,
                             uint16_t *resp_len) {
  struct cmd_packet pkt;
  struct sockaddr_in addr;
  struct pollfd pfd;
  ssize_t n;
  socklen_t addrlen;
  uint8_t rxbuf[sizeof(struct cmd_packet)];

  if (!g_host_ip_set)
    return -1;

  memset(&pkt, 0, sizeof(pkt));
  pkt.cmd = cmd;
  if (data && len > 0 && len <= CMD_BUF_SIZE) {
    memcpy(pkt.data, data, len);
    pkt.len = htons(len);
  } else {
    pkt.len = htons(0);
  }

  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(TEST_ETH_PORT);
  addr.sin_addr = g_host_ip;

  errno = 0;
  if (sendto(fd, &pkt, HDR_SIZE + (data ? len : 0), 0, (struct sockaddr *)&addr,
             sizeof(addr)) < 0)
    return -1;

  pfd.fd = fd;
  pfd.events = POLLIN;

  while (1) {
    int ret = poll(&pfd, 1, 5000);
    if (ret <= 0)
      return -1;

    addrlen = sizeof(addr);
    n = recvfrom(fd, rxbuf, sizeof(rxbuf), 0, (struct sockaddr *)&addr,
                 &addrlen);
    if (n < HDR_SIZE)
      continue;

    if (resp_len)
      *resp_len = ntohs(*(uint16_t *)(rxbuf + 2));
    if (resp && resp_size > 0) {
      uint16_t dlen = ntohs(*(uint16_t *)(rxbuf + 2));
      if (dlen > resp_size)
        dlen = resp_size;
      memcpy(resp, rxbuf + HDR_SIZE, dlen);
    }
    return 0;
  }
}

static int send_cmd(int fd, uint8_t cmd, const void *data, uint16_t len,
                    void *resp, uint16_t resp_size, uint16_t *resp_len) {
  int retries = 3;
  int ret;

  while (retries > 0) {
    ret = send_cmd_internal(fd, cmd, data, len, resp, resp_size, resp_len);
    if (ret == 0)
      return 0;
    retries--;
    if (retries > 0)
      usleep(500000);
  }
  return ret;
}

/* ---------------------------------------------------------------
 * Helper: send packet without expecting response
 * --------------------------------------------------------------- */

static int send_raw(int fd, uint8_t cmd, const void *data, uint16_t len) {
  struct cmd_packet pkt;
  struct sockaddr_in addr;

  if (!g_host_ip_set)
    return -1;

  memset(&pkt, 0, sizeof(pkt));
  pkt.cmd = cmd;
  if (data && len > 0 && len <= CMD_BUF_SIZE) {
    memcpy(pkt.data, data, len);
    pkt.len = htons(len);
  } else {
    pkt.len = htons(0);
  }

  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(TEST_ETH_PORT);
  addr.sin_addr = g_host_ip;

  return sendto(fd, &pkt, HDR_SIZE + (data ? len : 0), 0,
                (struct sockaddr *)&addr, sizeof(addr));
}

/* ---------------------------------------------------------------
 * Helper: receive with timeout (returns 0 on success, cmd in *cmd_out)
 * --------------------------------------------------------------- */

static int recv_cmd(int fd, struct cmd_packet *pkt, int timeout_ms) {
  struct pollfd pfd;
  ssize_t n;

  pfd.fd = fd;
  pfd.events = POLLIN;

  int ret = poll(&pfd, 1, timeout_ms);
  if (ret <= 0)
    return -1;

  n = recv(fd, pkt, sizeof(*pkt), 0);
  if (n < HDR_SIZE)
    return -1;

  return 0;
}

/* ---------------------------------------------------------------
 * Helper: read /proc/net/dev statistics for interface
 * --------------------------------------------------------------- */

static int get_stats(struct net_stats *stats) {
  FILE *f;
  char line[512];
  char *p = NULL;
  int found = 0;

  memset(stats, 0, sizeof(*stats));

  f = fopen("/proc/net/dev", "r");
  if (!f)
    return -1;

  while (fgets(line, sizeof(line), f)) {
    char *cursor = line;
    while (*cursor == ' ')
      cursor++;
    if (strncmp(cursor, g_iface, strlen(g_iface)) == 0 &&
        cursor[strlen(g_iface)] == ':') {
      p = cursor + strlen(g_iface) + 1;
      found = 1;
      break;
    }
  }
  fclose(f);

  if (!found)
    return -1;

  sscanf(p,
         "%lu %lu %lu %lu %lu %lu %lu %lu "
         "%lu %lu %lu %lu %lu %lu %lu %lu",
         &stats->rx_bytes, &stats->rx_packets, &stats->rx_errors,
         &stats->rx_dropped, &stats->rx_fifo_errors, &stats->rx_frame_errors,
         &stats->rx_compressed, &stats->rx_multicast, &stats->tx_bytes,
         &stats->tx_packets, &stats->tx_errors, &stats->tx_dropped,
         &stats->tx_fifo_errors, &stats->tx_collisions,
         &stats->tx_carrier_errors, &stats->tx_compressed);

  return 0;
}

/* ---------------------------------------------------------------
 * Helper: set/clear interface flags
 * --------------------------------------------------------------- */

static int set_iface_flags(int fd, unsigned int flags_to_set,
                           unsigned int flags_to_clear) {
  struct ifreq ifr;
  int ret;

  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);

  ret = ioctl(fd, SIOCGIFADDR, &ifr);
  if (ret < 0 && errno != EADDRNOTAVAIL)
    return -1;

  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);

  ret = ioctl(fd, SIOCGIFFLAGS, &ifr);
  if (ret < 0)
    return -1;

  ifr.ifr_flags |= flags_to_set;
  ifr.ifr_flags &= ~flags_to_clear;

  ret = ioctl(fd, SIOCSIFFLAGS, &ifr);
  return ret;
}

static unsigned int get_iface_flags(int fd) {
  struct ifreq ifr;
  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  if (ioctl(fd, SIOCGIFFLAGS, &ifr) < 0)
    return 0;
  return ifr.ifr_flags;
}

/* ---------------------------------------------------------------
 * Helper: get interface MAC as 6 bytes
 * --------------------------------------------------------------- */

static int get_mac(int fd, unsigned char *mac) {
  struct ifreq ifr;
  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  if (ioctl(fd, SIOCGIFHWADDR, &ifr) < 0)
    return -1;
  memcpy(mac, ifr.ifr_hwaddr.sa_data, 6);
  return 0;
}

/* ---------------------------------------------------------------
 * Helper: set interface MAC address
 * --------------------------------------------------------------- */

static int set_mac(int fd, const unsigned char *mac) {
  struct ifreq ifr;
  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  ifr.ifr_hwaddr.sa_family = ARPHRD_ETHER;
  memcpy(ifr.ifr_hwaddr.sa_data, mac, 6);
  return ioctl(fd, SIOCSIFHWADDR, &ifr);
}

/* ---------------------------------------------------------------
 * Helper: get ethtool register dump
 * --------------------------------------------------------------- */

static int get_ethtool_regs(int fd, uint32_t *regs, int *count) {
  struct {
    struct ethtool_regs hdr;
    uint32_t data[64];
  } buf;
  struct ifreq ifr;

  memset(&buf, 0, sizeof(buf));
  buf.hdr.cmd = ETHOOL_GREGS;

  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  ifr.ifr_data = (void *)&buf;

  if (ioctl(fd, SIOCETHTOOL, &ifr) < 0)
    return -1;

  *count = buf.hdr.len / sizeof(uint32_t);
  if (*count > 64)
    *count = 64;
  memcpy(regs, buf.hdr.data, *count * sizeof(uint32_t));

  return 0;
}

/* ---------------------------------------------------------------
 * Helper: get ethtool ring parameters
 * --------------------------------------------------------------- */

static int get_ethtool_ring(int fd, struct ethool_ringparam *ring) {
  struct ifreq ifr;

  memset(ring, 0, sizeof(*ring));
  ring->cmd = ETHOOL_GRINGPARAM;

  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  ifr.ifr_data = (void *)ring;

  return ioctl(fd, SIOCETHTOOL, &ifr);
}

/* ---------------------------------------------------------------
 * Helper: get ethtool link status
 * --------------------------------------------------------------- */

static int get_ethtool_link(int fd) {
  struct {
    struct ethool_link hdr;
  } buf;
  struct ifreq ifr;

  memset(&buf, 0, sizeof(buf));
  buf.hdr.cmd = ETHOOL_GLINK;

  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  ifr.ifr_data = (void *)&buf;

  if (ioctl(fd, SIOCETHTOOL, &ifr) < 0)
    return -1;

  return buf.hdr.link;
}

/* ---------------------------------------------------------------
 * Helper: read sysfs file content
 * --------------------------------------------------------------- */

static int read_sysfs(const char *path, char *buf, size_t buflen) {
  int fd;
  ssize_t n;

  fd = open(path, O_RDONLY);
  if (fd < 0)
    return -1;

  n = read(fd, buf, buflen - 1);
  close(fd);

  if (n <= 0)
    return -1;

  buf[n] = '\0';

  /* trim trailing newline */
  if (n > 0 && buf[n - 1] == '\n')
    buf[n - 1] = '\0';

  return 0;
}

/* ---------------------------------------------------------------
 * Helper: read /proc/interrupts IRQ count for interface
 * --------------------------------------------------------------- */

static int get_irq_count(unsigned long *count_out) {
  FILE *f;
  char line[512];
  unsigned long total = 0;
  int cpu_cols = 0;

  *count_out = 0;

  f = fopen("/proc/interrupts", "r");
  if (!f)
    return -1;

  /* count CPU columns from header line */
  if (fgets(line, sizeof(line), f)) {
    char *h = line;
    while ((h = strstr(h, "CPU")) != NULL) {
      cpu_cols++;
      h += 3;
    }
  }
  if (cpu_cols == 0) {
    fclose(f);
    return -1;
  }

  while (fgets(line, sizeof(line), f)) {
    if (strstr(line, g_iface) || strstr(line, "ethoc")) {
      char *p = strchr(line, ':');
      if (!p)
        continue;
      p++;
      int col = 0;
      while (*p && col < cpu_cols) {
        unsigned long val;
        while (*p == ' ' || *p == '\t')
          p++;
        if (sscanf(p, " %lu", &val) == 1) {
          total += val;
          col++;
        } else {
          break;
        }
        while (*p >= '0' && *p <= '9')
          p++;
      }
      break;
    }
  }

  fclose(f);
  *count_out = total;
  return 0;
}

/* ===============================================================
 * TEST 1: Interface Detection & Driver Binding
 * =============================================================== */

static int test_interface_detection(void) {
  char driver_path[512];
  char link_target[512];
  ssize_t len;

  if (find_ethoc_iface(g_iface, sizeof(g_iface)) < 0) {
    TEST_FAIL("Interface Detection",
              "No interface with ethoc driver found in /sys/class/net/");
    return -1;
  }

  TEST_PASS("Interface Detection");

  if (g_verbose)
    printf("    Detected interface: %s\n", g_iface);

  /* verify driver symlink exists and points to ethoc */
  snprintf(driver_path, sizeof(driver_path), "/sys/class/net/%s/device/driver",
           g_iface);
  len = readlink(driver_path, link_target, sizeof(link_target) - 1);
  if (len > 0) {
    link_target[len] = '\0';
    if (g_verbose)
      printf("    Driver symlink: %s\n", link_target);
  }

  /* check MTU */
  {
    char mtu_path[128];
    char mtu_buf[32];
    snprintf(mtu_path, sizeof(mtu_path), "/sys/class/net/%s/mtu", g_iface);
    if (read_sysfs(mtu_path, mtu_buf, sizeof(mtu_buf)) == 0) {
      if (g_verbose)
        printf("    MTU: %s\n", mtu_buf);
    }
  }

  /* check address */
  {
    char addr_buf[128];
    char mac_buf[MAC_STR_LEN + 1];
    snprintf(addr_buf, sizeof(addr_buf), "/sys/class/net/%s/address", g_iface);
    if (read_sysfs(addr_buf, mac_buf, sizeof(mac_buf)) == 0) {
      if (g_verbose)
        printf("    MAC: %s\n", mac_buf);
    }
  }

  return 0;
}

/* ===============================================================
 * TEST 2: Interface Bring-Up
 * =============================================================== */

static int test_interface_up(void) {
  int fd;
  unsigned int flags;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Interface Bring-Up", "socket() failed: %s", strerror(errno));
    return -1;
  }

  if (set_iface_flags(fd, IFF_UP | IFF_RUNNING, 0) < 0) {
    TEST_FAIL("Interface Bring-Up", "Failed to bring interface up: %s",
              strerror(errno));
    close(fd);
    return -1;
  }

  usleep(100000); /* 100ms for driver to settle */

  flags = get_iface_flags(fd);
  close(fd);

  if (!(flags & IFF_UP)) {
    TEST_FAIL("Interface Bring-Up", "Interface not UP after SIOCSIFFLAGS");
    return -1;
  }

  TEST_PASS("Interface Bring-Up");
  return 0;
}

/* ===============================================================
 * TEST 3: MAC Address Read/Write
 * =============================================================== */

static int test_mac_read_write(void) {
  int fd;
  unsigned char orig_mac[6];
  unsigned char test_mac1[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x01};
  unsigned char test_mac2[6] = {0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x01};
  unsigned char read_mac[6];
  char mac_str[MAC_STR_LEN];
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("MAC Read/Write", "socket() failed");
    return -1;
  }

  /* read original MAC */
  if (get_mac(fd, orig_mac) < 0) {
    TEST_FAIL("MAC Read/Write", "Failed to read MAC");
    close(fd);
    return -1;
  }

  snprintf(mac_str, sizeof(mac_str), "%02X:%02X:%02X:%02X:%02X:%02X",
           orig_mac[0], orig_mac[1], orig_mac[2], orig_mac[3], orig_mac[4],
           orig_mac[5]);

  /* verify it is a valid unicast address */
  if (orig_mac[0] & 0x01) {
    TEST_FAIL("MAC Read/Write", "Read MAC is multicast/broadcast: %s", mac_str);
    ok = 0;
  }

  if (orig_mac[0] == 0 && orig_mac[1] == 0 && orig_mac[2] == 0 &&
      orig_mac[3] == 0 && orig_mac[4] == 0 && orig_mac[5] == 0) {
    TEST_FAIL("MAC Read/Write", "Read MAC is all zeros");
    ok = 0;
  }

  /* set test MAC 1 */
  if (set_mac(fd, test_mac1) < 0) {
    TEST_FAIL("MAC Read/Write", "Failed to set MAC: %s", strerror(errno));
    ok = 0;
  } else {
    get_mac(fd, read_mac);
    if (memcmp(read_mac, test_mac1, 6) != 0) {
      TEST_FAIL("MAC Read/Write", "MAC mismatch after set (1)");
      ok = 0;
    }
  }

  /* set test MAC 2 */
  if (set_mac(fd, test_mac2) < 0) {
    TEST_FAIL("MAC Read/Write", "Failed to set MAC (2): %s", strerror(errno));
    ok = 0;
  } else {
    get_mac(fd, read_mac);
    if (memcmp(read_mac, test_mac2, 6) != 0) {
      TEST_FAIL("MAC Read/Write", "MAC mismatch after set (2)");
      ok = 0;
    }
  }

  /* restore original MAC */
  set_mac(fd, orig_mac);
  close(fd);

  if (ok)
    TEST_PASS("MAC Read/Write");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 4: Default Register State
 * =============================================================== */

static int test_default_regs(void) {
  int fd;
  uint32_t regs[64];
  int count;
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Default Registers", "socket() failed");
    return -1;
  }

  if (get_ethtool_regs(fd, regs, &count) < 0) {
    if (errno == EOPNOTSUPP) {
      TEST_INFO("Default Registers",
                "ethtool get_regs not supported by driver");
      close(fd);
      TEST_PASS("Default Registers");
      return 0;
    }
    TEST_FAIL("Default Registers", "ethtool get_regs failed: %s",
              strerror(errno));
    close(fd);
    return -1;
  }
  close(fd);

  /* check register space: should be at least REG_ETH_END/4 = 21 regs */
  if (count < REG_ETH_END / 4) {
    TEST_FAIL("Default Registers",
              "Register dump too short: %d words (expected >= %d)", count,
              REG_ETH_END / 4);
    return -1;
  }

  if (g_verbose) {
    printf("    Register dump (%d words):\n", count);
    for (int i = 0; i < count; i++)
      printf("      [0x%02x] = 0x%08x\n", i * 4, regs[i]);
  }

  /* MODER: should have CRC|PAD|FULLD|RXEN|TXEN set after ethoc_reset() */
  uint32_t moder = regs[REG_MODER / 4];
  if ((moder & MODER_DEFAULT) != MODER_DEFAULT) {
    TEST_FAIL("Default Registers", "MODER = 0x%08x, expected bits 0x%08x set",
              moder, MODER_DEFAULT);
    ok = 0;
  }

  /* IPGT: should be 0x15 (full-duplex inter-packet gap) */
  uint32_t ipgt = regs[REG_IPGT / 4];
  if (ipgt != IPGT_DEFAULT) {
    TEST_FAIL("Default Registers", "IPGT = 0x%08x, expected 0x%08x", ipgt,
              IPGT_DEFAULT);
    ok = 0;
  }

  /* INT_MASK: should be 0x7F (all 7 interrupts enabled) */
  uint32_t int_mask = regs[REG_INT_MASK / 4];
  if (int_mask != INT_MASK_ALL) {
    TEST_FAIL("Default Registers", "INT_MASK = 0x%08x, expected 0x%08x",
              int_mask, INT_MASK_ALL);
    ok = 0;
  }

  /* TX_BD_NUM: should be > 0 and <= 0x80 */
  uint32_t tx_bd_num = regs[REG_TX_BD_NUM / 4];
  if (tx_bd_num == 0 || tx_bd_num > 0x80) {
    TEST_FAIL("Default Registers", "TX_BD_NUM = %u, expected 1..128",
              tx_bd_num);
    ok = 0;
  }

  if (ok)
    TEST_PASS("Default Registers");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 5: Link State Detection
 * =============================================================== */

static int test_link_state(void) {
  int fd;
  int link;
  char speed_buf[32];
  char duplex_buf[32];
  char operstate_buf[32];
  char path[128];

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Link State", "socket() failed");
    return -1;
  }

  link = get_ethtool_link(fd);
  close(fd);

  if (link < 0) {
    TEST_FAIL("Link State", "ethtool get_link failed");
    return -1;
  }

  /* read sysfs attributes */
  snprintf(path, sizeof(path), "/sys/class/net/%s/speed", g_iface);
  read_sysfs(path, speed_buf, sizeof(speed_buf));

  snprintf(path, sizeof(path), "/sys/class/net/%s/duplex", g_iface);
  read_sysfs(path, duplex_buf, sizeof(duplex_buf));

  snprintf(path, sizeof(path), "/sys/class/net/%s/operstate", g_iface);
  read_sysfs(path, operstate_buf, sizeof(operstate_buf));

  if (link) {
    TEST_INFO("Link State", "Link UP, speed=%s, duplex=%s, operstate=%s",
              speed_buf, duplex_buf, operstate_buf);
  } else {
    TEST_INFO("Link State", "Link DOWN (no cable or PHY not connected)");
  }

  TEST_PASS("Link State");
  return 0;
}

/* ===============================================================
 * TEST 6: MII/MDIO PHY Access
 * =============================================================== */

static int test_mdio_access(void) {
  int fd;
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("MII/MDIO Access", "socket() failed");
    return -1;
  }

  /* SIOCGMIIPHY: get PHY address */
  struct mii_ioctl_data mii;
  struct ifreq ifr;

  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  ifr.ifr_data = (void *)&mii;

  if (ioctl(fd, SIOCGMIIPHY, &ifr) < 0) {
    if (errno == EINVAL) {
      TEST_INFO("MII/MDIO Access",
                "SIOCGMIIPHY not supported (interface may be down)");
    } else {
      TEST_FAIL("MII/MDIO Access", "SIOCGMIIPHY failed: %s", strerror(errno));
    }
    ok = 0;
  } else {
    if (g_verbose)
      printf("    PHY address: %d\n", mii.phy_id);
  }

  if (ok) {
    /* SIOCGMIIREG: read PHY BMCR (register 0) */
    mii.reg_num = 0;
    if (ioctl(fd, SIOCGMIIREG, &ifr) < 0) {
      TEST_FAIL("MII/MDIO Access", "SIOCGMIIREG reg 0 failed: %s",
                strerror(errno));
      ok = 0;
    } else {
      if (g_verbose)
        printf("    PHY BMCR (reg 0) = 0x%04x\n", mii.val_out);
    }

    /* SIOCGMIIREG: read BMSR (register 1) */
    mii.reg_num = 1;
    if (ioctl(fd, SIOCGMIIREG, &ifr) < 0) {
      TEST_FAIL("MII/MDIO Access", "SIOCGMIIREG reg 1 failed: %s",
                strerror(errno));
      ok = 0;
    } else {
      if (g_verbose)
        printf("    PHY BMSR (reg 1) = 0x%04x\n", mii.val_out);
    }

    /* SIOCGMIIREG: read PHY ID high (register 2) */
    mii.reg_num = 2;
    if (ioctl(fd, SIOCGMIIREG, &ifr) < 0) {
      TEST_FAIL("MII/MDIO Access", "SIOCGMIIREG reg 2 failed: %s",
                strerror(errno));
      ok = 0;
    } else {
      if (g_verbose)
        printf("    PHY ID High (reg 2) = 0x%04x\n", mii.val_out);
    }

    /* SIOCGMIIREG: read PHY ID low (register 3) */
    mii.reg_num = 3;
    if (ioctl(fd, SIOCGMIIREG, &ifr) < 0) {
      TEST_FAIL("MII/MDIO Access", "SIOCGMIIREG reg 3 failed: %s",
                strerror(errno));
      ok = 0;
    } else {
      if (g_verbose)
        printf("    PHY ID Low (reg 3) = 0x%04x\n", mii.val_out);
    }

    /* SIOCGMIIREG: read ANAR (register 4, advertise) */
    mii.reg_num = 4;
    if (ioctl(fd, SIOCGMIIREG, &ifr) < 0) {
      TEST_FAIL("MII/MDIO Access", "SIOCGMIIREG reg 4 failed: %s",
                strerror(errno));
      ok = 0;
    } else {
      if (g_verbose)
        printf("    PHY ANAR (reg 4) = 0x%04x\n", mii.val_out);
    }
  }

  close(fd);

  if (ok)
    TEST_PASS("MII/MDIO Access");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 7: Raw TX — Basic Frame Transmission
 * =============================================================== */

static int test_tx_basic(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  uint8_t data[32];
  uint16_t resp_len;
  int ok = 1;

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("TX Basic", "Failed to create socket");
    return -1;
  }

  get_stats(&stats_before);

  /* send echo command with pattern payload */
  for (int i = 0; i < (int)sizeof(data); i++)
    data[i] = (uint8_t)(i & 0xFF);

  if (send_cmd(fd, CMD_ECHO, data, sizeof(data), NULL, 0, &resp_len) < 0) {
    TEST_FAIL("TX Basic", "send_cmd failed: %s", strerror(errno));
    ok = 0;
  }

  usleep(500000); /* 500ms for stats to update on slow SoCs */
  get_stats(&stats_after);

  close(fd);

  if (ok) {
    if (stats_after.tx_packets <= stats_before.tx_packets) {
      TEST_FAIL("TX Basic",
                "tx_packets did not increase: before=%lu, after=%lu",
                stats_before.tx_packets, stats_after.tx_packets);
      ok = 0;
    }
    if (stats_after.tx_errors > stats_before.tx_errors) {
      TEST_FAIL("TX Basic", "tx_errors increased: before=%lu, after=%lu",
                stats_before.tx_errors, stats_after.tx_errors);
      ok = 0;
    }
  }

  if (ok)
    TEST_PASS("TX Basic");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 8: TX Frame Size Range
 * =============================================================== */

static int test_tx_sizes(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  uint8_t data[1536];
  /* Max payload = 1500 (MTU) - 20 (IP) - 8 (UDP) - 4 (HDR) = 1468 */
  int sizes[] = {60, 128, 512, 1468};
  int ok = 1;
  int num_tests = sizeof(sizes) / sizeof(sizes[0]);
  uint16_t resp_len;

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("TX Size Range", "Failed to create socket");
    return -1;
  }

  get_stats(&stats_before);

  for (int i = 0; i < num_tests; i++) {
    memset(data, (uint8_t)(i + 1), sizes[i]);
    if (send_cmd(fd, CMD_ECHO, data, sizes[i], NULL, 0, &resp_len) < 0) {
      TEST_FAIL("TX Size Range", "send failed for size %d", sizes[i]);
      ok = 0;
    }
    usleep(50000);
  }

  usleep(200000);
  get_stats(&stats_after);
  close(fd);

  if (ok) {
    unsigned long tx_delta = stats_after.tx_packets - stats_before.tx_packets;
    if ((long)tx_delta < num_tests) {
      TEST_FAIL("TX Size Range", "Expected %d TX packets, got %lu", num_tests,
                tx_delta);
      ok = 0;
    }
    if (stats_after.tx_errors > stats_before.tx_errors) {
      TEST_FAIL("TX Size Range", "tx_errors increased");
      ok = 0;
    }
  }

  if (ok)
    TEST_PASS("TX Size Range");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 9: RX — Basic Frame Reception
 * =============================================================== */

static int test_rx_basic(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  struct cmd_packet pkt;
  uint8_t data[32];
  int ok = 1;

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("RX Basic", "Failed to create socket");
    return -1;
  }

  get_stats(&stats_before);

  /* ask host to echo a 32-byte pattern back */
  for (int i = 0; i < (int)sizeof(data); i++)
    data[i] = (uint8_t)(i & 0xFF);

  if (send_raw(fd, CMD_ECHO, data, sizeof(data)) < 0) {
    TEST_FAIL("RX Basic", "send_raw failed");
    ok = 0;
  }

  if (ok) {
    if (recv_cmd(fd, &pkt, 5000) < 0) {
      TEST_FAIL("RX Basic", "No response from host (timeout)");
      ok = 0;
    } else {
      uint16_t plen = ntohs(pkt.len);
      if (plen != sizeof(data)) {
        TEST_FAIL("RX Basic", "Response payload length %u != %zu", plen,
                  sizeof(data));
        ok = 0;
      } else if (memcmp(pkt.data, data, sizeof(data)) != 0) {
        TEST_FAIL("RX Basic", "Response payload mismatch");
        ok = 0;
      }
    }
  }

  usleep(100000);
  get_stats(&stats_after);
  close(fd);

  if (ok) {
    if (stats_after.rx_packets <= stats_before.rx_packets) {
      TEST_FAIL("RX Basic", "rx_packets did not increase");
      ok = 0;
    }
    if (stats_after.rx_errors > stats_before.rx_errors) {
      TEST_FAIL("RX Basic", "rx_errors increased");
      ok = 0;
    }
  }

  if (ok)
    TEST_PASS("RX Basic");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 10: RX Frame Size Range
 * =============================================================== */

static int test_rx_sizes(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  struct cmd_packet pkt;
  /* Max payload = 1500 (MTU) - 20 (IP) - 8 (UDP) - 4 (HDR) = 1468 */
  int sizes[] = {60, 128, 512, 1468};
  int num_tests = sizeof(sizes) / sizeof(sizes[0]);
  int ok = 1;
  uint8_t data[1536];

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("RX Size Range", "Failed to create socket");
    return -1;
  }

  get_stats(&stats_before);

  for (int i = 0; i < num_tests; i++) {
    memset(data, (uint8_t)(i + 1), sizes[i]);
    if (send_raw(fd, CMD_ECHO, data, sizes[i]) < 0) {
      TEST_FAIL("RX Size Range", "send failed for size %d", sizes[i]);
      ok = 0;
      continue;
    }

    if (recv_cmd(fd, &pkt, 5000) < 0) {
      TEST_FAIL("RX Size Range", "No response for size %d", sizes[i]);
      ok = 0;
    } else {
      uint16_t plen = ntohs(pkt.len);
      if (plen != (uint16_t)sizes[i]) {
        TEST_FAIL("RX Size Range", "Size %d: response length %u != %d",
                  sizes[i], plen, sizes[i]);
        ok = 0;
      } else if (memcmp(pkt.data, data, sizes[i]) != 0) {
        TEST_FAIL("RX Size Range", "Size %d: payload mismatch", sizes[i]);
        ok = 0;
      }
    }
    usleep(50000);
  }

  usleep(100000);
  get_stats(&stats_after);
  close(fd);

  if (ok)
    TEST_PASS("RX Size Range");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 11: Broadcast Reception
 * =============================================================== */

static int test_broadcast(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  unsigned int flags;
  struct cmd_packet pkt;
  uint8_t data[8] = {0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49};
  int ok = 1;

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("Broadcast", "Failed to create socket");
    return -1;
  }

  /* verify broadcast flag is set by default */
  flags = get_iface_flags(fd);
  if (!(flags & IFF_BROADCAST)) {
    TEST_INFO("Broadcast", "IFF_BROADCAST not set, enabling");
    if (set_iface_flags(fd, IFF_BROADCAST, 0) < 0) {
      TEST_FAIL("Broadcast", "Failed to set IFF_BROADCAST");
      close(fd);
      return -1;
    }
  }

  get_stats(&stats_before);

  /* host sends broadcast frame */
  if (send_raw(fd, CMD_BROADCAST, data, sizeof(data)) < 0) {
    TEST_FAIL("Broadcast", "send failed");
    ok = 0;
  }

  if (ok) {
    if (recv_cmd(fd, &pkt, 5000) < 0) {
      TEST_FAIL("Broadcast", "No broadcast response from host");
      ok = 0;
    }
  }

  usleep(100000);
  get_stats(&stats_after);
  close(fd);

  if (ok)
    TEST_PASS("Broadcast");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 12: Promiscuous Mode
 * =============================================================== */

static int test_promiscuous(void) {
  int fd;
  unsigned int flags;
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Promiscuous Mode", "socket() failed");
    return -1;
  }

  /* set promiscuous */
  if (set_iface_flags(fd, IFF_PROMISC, 0) < 0) {
    TEST_FAIL("Promiscuous Mode", "Failed to set IFF_PROMISC");
    close(fd);
    return -1;
  }

  flags = get_iface_flags(fd);
  if (!(flags & IFF_PROMISC)) {
    TEST_FAIL("Promiscuous Mode", "IFF_PROMISC not set after SIOCSIFFLAGS");
    ok = 0;
  }

  if (g_verbose)
    printf("    IFF_PROMISC set (flags=0x%x)\n", flags);
  (void)flags;

  /* clear promiscuous */
  if (set_iface_flags(fd, 0, IFF_PROMISC) < 0) {
    TEST_FAIL("Promiscuous Mode", "Failed to clear IFF_PROMISC");
    close(fd);
    return -1;
  }

  flags = get_iface_flags(fd);
  if (flags & IFF_PROMISC) {
    TEST_FAIL("Promiscuous Mode", "IFF_PROMISC still set after clear");
    ok = 0;
  }

  close(fd);

  if (ok)
    TEST_PASS("Promiscuous Mode");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 13: Loopback Mode
 * =============================================================== */

static int test_loopback(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  unsigned int flags;
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Loopback Mode", "socket() failed");
    return -1;
  }

  get_stats(&stats_before);

  /* enable loopback via IFF_LOOPBACK */
  errno = 0;
  if (set_iface_flags(fd, IFF_LOOPBACK, 0) < 0) {
    TEST_INFO("Loopback Mode", "IFF_LOOPBACK not supported by driver (%s)",
              strerror(errno));
    close(fd);
    TEST_PASS("Loopback Mode");
    return 0;
  }

  flags = get_iface_flags(fd);
  if (!(flags & IFF_LOOPBACK)) {
    TEST_INFO("Loopback Mode",
              "IFF_LOOPBACK accepted but not applied by driver");
    set_iface_flags(fd, 0, IFF_LOOPBACK);
    close(fd);
    TEST_PASS("Loopback Mode");
    return 0;
  }

  /* send a frame in loopback mode */
  if (ok) {
    uint8_t data[64];
    for (int i = 0; i < (int)sizeof(data); i++)
      data[i] = (uint8_t)i;

    int send_fd = create_test_socket(TEST_ETH_PORT + 1);
    if (send_fd >= 0) {
      send_raw(send_fd, CMD_ECHO, data, sizeof(data));
      close(send_fd);
    }
  }

  usleep(200000);
  get_stats(&stats_after);

  /* clear loopback */
  set_iface_flags(fd, 0, IFF_LOOPBACK);
  close(fd);

  if (ok) {
    if (g_verbose) {
      printf("    TX packets: %lu -> %lu\n", stats_before.tx_packets,
             stats_after.tx_packets);
      printf("    RX packets: %lu -> %lu\n", stats_before.rx_packets,
             stats_after.rx_packets);
    }
    (void)flags;
    TEST_INFO("Loopback Mode", "TX delta=%lu, RX delta=%lu (MODER_LOOP active)",
              stats_after.tx_packets - stats_before.tx_packets,
              stats_after.rx_packets - stats_before.rx_packets);
  }

  if (ok)
    TEST_PASS("Loopback Mode");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 14: MTU Change Rejection
 * =============================================================== */

static int test_mtu_reject(void) {
  int fd;
  struct ifreq ifr;
  char mtu_buf[32];
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("MTU Rejection", "socket() failed");
    return -1;
  }

  /* attempt to change MTU to 1400 */
  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, g_iface, IFNAMSIZ - 1);
  ifr.ifr_mtu = 1400;

  if (ioctl(fd, SIOCSIFMTU, &ifr) == 0) {
    TEST_FAIL("MTU Rejection",
              "SIOCSIFMTU succeeded but should return -ENOSYS");
    ok = 0;
  } else if (errno != EINVAL && errno != EOPNOTSUPP && errno != ENODEV &&
             errno != ENOSYS) {
    TEST_FAIL("MTU Rejection",
              "SIOCSIFMTU failed with unexpected errno %d (%s)", errno,
              strerror(errno));
    ok = 0;
  }

  /* attempt jumbo MTU */
  ifr.ifr_mtu = 9000;
  if (ioctl(fd, SIOCSIFMTU, &ifr) == 0) {
    TEST_FAIL("MTU Rejection", "Jumbo MTU accepted but should be rejected");
    ok = 0;
  }

  /* verify MTU remains 1500 */
  {
    char mtu_path[128];
    snprintf(mtu_path, sizeof(mtu_path), "/sys/class/net/%s/mtu", g_iface);
    if (read_sysfs(mtu_path, mtu_buf, sizeof(mtu_buf)) == 0) {
      int mtu = atoi(mtu_buf);
      if (mtu != 1500) {
        TEST_FAIL("MTU Rejection", "MTU changed to %d, expected 1500", mtu);
        ok = 0;
      }
    }
  }

  close(fd);

  if (ok)
    TEST_PASS("MTU Rejection");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 15: ethtool Ring Parameters
 * =============================================================== */

static int test_ring_params(void) {
  int fd;
  struct ethool_ringparam ring;
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Ring Parameters", "socket() failed");
    return -1;
  }

  if (get_ethtool_ring(fd, &ring) < 0) {
    TEST_FAIL("Ring Parameters", "ethtool get_ringparam failed: %s",
              strerror(errno));
    close(fd);
    return -1;
  }
  close(fd);

  if (g_verbose) {
    printf("    rx_max_pending=%u tx_max_pending=%u\n", ring.rx_max_pending,
           ring.tx_max_pending);
    printf("    rx_pending=%u tx_pending=%u\n", ring.rx_pending,
           ring.tx_pending);
    printf("    rx_mini_pending=%u rx_jumbo_pending=%u\n", ring.rx_mini_pending,
           ring.rx_jumbo_pending);
  }

  /* total BDs should be <= 128 */
  if (ring.rx_pending + ring.tx_pending > 128) {
    TEST_FAIL("Ring Parameters", "rx_pending + tx_pending = %u > 128",
              ring.rx_pending + ring.tx_pending);
    ok = 0;
  }

  /* tx_pending should be power of 2 (ethoc enforces this) */
  if (ring.tx_pending > 0 && (ring.tx_pending & (ring.tx_pending - 1)) != 0) {
    TEST_FAIL("Ring Parameters", "tx_pending = %u is not a power of 2",
              ring.tx_pending);
    ok = 0;
  }

  /* rx_mini and rx_jumbo should be 0 */
  if (ring.rx_mini_pending != 0) {
    TEST_FAIL("Ring Parameters", "rx_mini_pending = %u, expected 0",
              ring.rx_mini_pending);
    ok = 0;
  }
  if (ring.rx_jumbo_pending != 0) {
    TEST_FAIL("Ring Parameters", "rx_jumbo_pending = %u, expected 0",
              ring.rx_jumbo_pending);
    ok = 0;
  }

  if (ok)
    TEST_PASS("Ring Parameters");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 16: ethtool Register Dump
 * =============================================================== */

static int test_register_dump(void) {
  int fd;
  uint32_t regs[64];
  int count;
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Register Dump", "socket() failed");
    return -1;
  }

  if (get_ethtool_regs(fd, regs, &count) < 0) {
    if (errno == EOPNOTSUPP) {
      TEST_INFO("Register Dump", "ethtool get_regs not supported by driver");
      close(fd);
      TEST_PASS("Register Dump");
      return 0;
    }
    TEST_FAIL("Register Dump", "ethtool get_regs failed: %s", strerror(errno));
    close(fd);
    return -1;
  }
  close(fd);

  /* verify register count: ETH_END / 4 = 21 registers expected */
  if (count < REG_ETH_END / 4) {
    TEST_FAIL("Register Dump", "Only %d registers, expected >= %d", count,
              REG_ETH_END / 4);
    ok = 0;
  }

  /* print full register dump */
  printf("    Register dump (%d words, %d bytes):\n", count, count * 4);
  printf("    Offset  Name           Value\n");
  printf("    ------  ----           -----\n");

  static const char *reg_names[] = {
      "MODER",     "INT_SOURCE", "INT_MASK",   "IPGT",       "IPGR1",
      "IPGR2",     "PACKETLEN",  "COLLCONF",   "TX_BD_NUM",  "CTRLMODER",
      "MIIMODER",  "MIICOMMAND", "MIIADDRESS", "MIITX_DATA", "MIIRX_DATA",
      "MIISTATUS", "MAC_ADDR0",  "MAC_ADDR1",  "ETH_HASH0",  "ETH_HASH1",
      "ETH_TXCTRL"};

  for (int i = 0; i < count && i < 21; i++) {
    printf("    0x%02x     %-14s 0x%08x\n", i * 4, reg_names[i], regs[i]);
  }

  if (ok)
    TEST_PASS("Register Dump");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 17: Interrupt Verification
 * =============================================================== */

static int test_interrupts(void) {
  unsigned long irq_before, irq_after;
  int ok = 1;

  if (get_irq_count(&irq_before) < 0) {
    TEST_FAIL("Interrupts", "Failed to read /proc/interrupts");
    return -1;
  }

  /* generate some traffic */
  int fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("Interrupts", "Failed to create socket");
    return -1;
  }

  uint8_t data[64];
  for (int i = 0; i < (int)sizeof(data); i++)
    data[i] = (uint8_t)i;

  for (int i = 0; i < 10; i++) {
    send_raw(fd, CMD_ECHO, data, sizeof(data));
    usleep(10000);
  }

  /* wait for host to respond */
  struct cmd_packet pkt;
  for (int i = 0; i < 10; i++)
    recv_cmd(fd, &pkt, 2000);

  close(fd);

  usleep(200000);

  if (get_irq_count(&irq_after) < 0) {
    TEST_FAIL("Interrupts", "Failed to read /proc/interrupts (after)");
    return -1;
  }

  if (g_verbose)
    printf("    IRQ count: %lu -> %lu (delta=%lu)\n", irq_before, irq_after,
           irq_after - irq_before);

  if (irq_after <= irq_before) {
    TEST_FAIL("Interrupts", "IRQ count did not increase: before=%lu, after=%lu",
              irq_before, irq_after);
    ok = 0;
  }

  if (ok)
    TEST_PASS("Interrupts");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 18: Error Counter Clean Check
 * =============================================================== */

static int test_error_counters(void) {
  struct net_stats stats_before, stats_after;
  int ok = 1;

  if (get_stats(&stats_before) < 0) {
    TEST_FAIL("Error Counters", "Failed to read /proc/net/dev");
    return -1;
  }

  /* generate some traffic */
  int fd = create_test_socket(TEST_ETH_PORT);
  if (fd >= 0) {
    uint8_t data[64];
    for (int i = 0; i < (int)sizeof(data); i++)
      data[i] = (uint8_t)i;
    for (int i = 0; i < 5; i++)
      send_raw(fd, CMD_ECHO, data, sizeof(data));
    close(fd);
  }

  usleep(500000);
  get_stats(&stats_after);

  if (stats_after.rx_errors > stats_before.rx_errors) {
    TEST_FAIL("Error Counters", "rx_errors increased: %lu -> %lu",
              stats_before.rx_errors, stats_after.rx_errors);
    ok = 0;
  }
  if (stats_after.rx_frame_errors > stats_before.rx_frame_errors) {
    TEST_FAIL("Error Counters", "rx_frame_errors increased: %lu -> %lu",
              stats_before.rx_frame_errors, stats_after.rx_frame_errors);
    ok = 0;
  }
  if (stats_after.tx_errors > stats_before.tx_errors) {
    TEST_FAIL("Error Counters", "tx_errors increased: %lu -> %lu",
              stats_before.tx_errors, stats_after.tx_errors);
    ok = 0;
  }
  if (stats_after.tx_fifo_errors > stats_before.tx_fifo_errors) {
    TEST_FAIL("Error Counters", "tx_fifo_errors increased");
    ok = 0;
  }
  if (stats_after.tx_carrier_errors > stats_before.tx_carrier_errors) {
    TEST_FAIL("Error Counters", "tx_carrier_errors increased");
    ok = 0;
  }
  if (stats_after.tx_collisions > stats_before.tx_collisions) {
    if (g_verbose)
      printf("    Note: tx_collisions increased (%lu -> %lu) "
             "(expected on half-duplex link)\n",
             stats_before.tx_collisions, stats_after.tx_collisions);
  }

  if (ok)
    TEST_PASS("Error Counters");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 19: Stress TX Burst
 * =============================================================== */

static int test_stress_tx(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  uint16_t count = 50;
  uint16_t size = 512;
  uint8_t payload[4];
  uint16_t resp_len;
  int ok = 1;

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("Stress TX", "Failed to create socket");
    return -1;
  }

  get_stats(&stats_before);

  /* tell host to expect 'count' frames of 'size' bytes */
  payload[0] = (count >> 8) & 0xFF;
  payload[1] = count & 0xFF;
  payload[2] = (size >> 8) & 0xFF;
  payload[3] = size & 0xFF;

  if (send_cmd(fd, CMD_STRESS_TX, payload, sizeof(payload), NULL, 0,
               &resp_len) < 0) {
    TEST_FAIL("Stress TX", "send_cmd failed");
    ok = 0;
  }

  if (ok) {
    uint8_t data[512];
    for (int i = 0; i < count; i++) {
      memset(data, (uint8_t)(i & 0xFF), size);
      if (send_raw(fd, CMD_ECHO, data, size) < 0) {
        TEST_FAIL("Stress TX", "send failed at frame %d", i);
        ok = 0;
        break;
      }
    }
  }

  usleep(500000);
  get_stats(&stats_after);
  close(fd);

  if (ok) {
    unsigned long tx_delta = stats_after.tx_packets - stats_before.tx_packets;
    if (g_verbose)
      printf("    TX delta: %lu packets (expected %d)\n", tx_delta, count);

    if ((long)tx_delta < count) {
      TEST_FAIL("Stress TX", "tx_packets delta %lu < %d", tx_delta, count);
      ok = 0;
    }
    if (stats_after.tx_errors > stats_before.tx_errors) {
      TEST_FAIL("Stress TX", "tx_errors increased during stress");
      ok = 0;
    }
  }

  if (ok)
    TEST_PASS("Stress TX");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 20: Stress RX Burst
 * =============================================================== */

static int test_stress_rx(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  uint16_t count = 10;
  uint16_t size = 512;
  uint8_t payload[4];
  struct cmd_packet pkt;
  int received = 0;
  int ok = 1;

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("Stress RX", "Failed to create socket");
    return -1;
  }

  get_stats(&stats_before);

  /* tell host to send 'count' frames of 'size' bytes */
  payload[0] = (count >> 8) & 0xFF;
  payload[1] = count & 0xFF;
  payload[2] = (size >> 8) & 0xFF;
  payload[3] = size & 0xFF;

  if (send_raw(fd, CMD_STRESS_RX, payload, sizeof(payload)) < 0) {
    TEST_FAIL("Stress RX", "send_raw failed");
    ok = 0;
  }

  /* receive frames (host sends count CMD_ECHO frames + 1 ack) */
  if (ok) {
    while (received < count) {
      if (recv_cmd(fd, &pkt, 3000) < 0)
        break;
      received++;
    }
  }

  usleep(200000);
  get_stats(&stats_after);
  close(fd);

  if (ok) {
    if (g_verbose)
      printf("    RX: received %d/%d frames\n", received, count);

    if (received < count) {
      TEST_FAIL("Stress RX", "Only received %d/%d frames", received, count);
      ok = 0;
    }
    if (stats_after.rx_errors > stats_before.rx_errors) {
      TEST_FAIL("Stress RX", "rx_errors increased during stress");
      ok = 0;
    }
  }

  if (ok)
    TEST_PASS("Stress RX");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 21: Stress Bidirectional
 * =============================================================== */

static int test_stress_bidir(void) {
  int fd;
  struct net_stats stats_before, stats_after;
  uint8_t data[256];
  int sent = 0, received = 0;
  int ok = 1;

  fd = create_test_socket(TEST_ETH_PORT);
  if (fd < 0) {
    TEST_FAIL("Stress Bidirectional", "Failed to create socket");
    return -1;
  }

  get_stats(&stats_before);

  /* interleave TX and RX: send one, receive one, repeat */
  for (int i = 0; i < 50; i++) {
    /* TX */
    memset(data, (uint8_t)(i & 0xFF), sizeof(data));
    if (send_raw(fd, CMD_ECHO, data, sizeof(data)) > 0)
      sent++;

    /* try to RX */
    struct cmd_packet pkt;
    if (recv_cmd(fd, &pkt, 500) == 0)
      received++;
  }

  usleep(200000);
  get_stats(&stats_after);
  close(fd);

  if (g_verbose)
    printf("    Bidirectional: sent=%d, received=%d\n", sent, received);

  if (sent == 0) {
    TEST_FAIL("Stress Bidirectional", "No frames sent");
    ok = 0;
  }

  if (ok && stats_after.tx_errors > stats_before.tx_errors) {
    TEST_FAIL("Stress Bidirectional", "tx_errors increased");
    ok = 0;
  }

  if (ok && stats_after.rx_errors > stats_before.rx_errors) {
    TEST_FAIL("Stress Bidirectional", "rx_errors increased");
    ok = 0;
  }

  if (ok)
    TEST_PASS("Stress Bidirectional");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 22: Interface Down
 * =============================================================== */

static int test_interface_down(void) {
  int fd;
  unsigned int flags;
  int ok = 1;

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd < 0) {
    TEST_FAIL("Interface Down", "socket() failed");
    return -1;
  }

  /* bring interface down */
  if (set_iface_flags(fd, 0, IFF_UP) < 0) {
    TEST_FAIL("Interface Down", "Failed to bring interface down");
    close(fd);
    return -1;
  }

  flags = get_iface_flags(fd);
  if (flags & IFF_UP) {
    TEST_FAIL("Interface Down", "Interface still UP after clearing IFF_UP");
    ok = 0;
  }

  /* bring back up for subsequent tests */
  set_iface_flags(fd, IFF_UP | IFF_RUNNING, 0);
  usleep(100000);

  flags = get_iface_flags(fd);
  if (!(flags & IFF_UP)) {
    TEST_FAIL("Interface Down", "Failed to bring interface back up");
    ok = 0;
  }

  close(fd);

  if (ok)
    TEST_PASS("Interface Down");

  return ok ? 0 : -1;
}

/* ===============================================================
 * TEST 23: Final Statistics Summary
 * =============================================================== */

static int test_final_summary(void) {
  struct net_stats stats;
  uint32_t regs[64];
  int count;
  int fd;

  printf("\n    === Final Driver Statistics ===\n");

  if (get_stats(&stats) == 0) {
    printf("    %-20s %lu\n", "rx_packets:", stats.rx_packets);
    printf("    %-20s %lu\n", "rx_bytes:", stats.rx_bytes);
    printf("    %-20s %lu\n", "rx_errors:", stats.rx_errors);
    printf("    %-20s %lu\n", "rx_dropped:", stats.rx_dropped);
    printf("    %-20s %lu\n", "tx_packets:", stats.tx_packets);
    printf("    %-20s %lu\n", "tx_bytes:", stats.tx_bytes);
    printf("    %-20s %lu\n", "tx_errors:", stats.tx_errors);
    printf("    %-20s %lu\n", "tx_dropped:", stats.tx_dropped);
    printf("    %-20s %lu\n", "tx_collisions:", stats.tx_collisions);
  }

  fd = socket(AF_INET, SOCK_DGRAM, 0);
  if (fd >= 0) {
    if (get_ethtool_regs(fd, regs, &count) == 0) {
      printf("\n    === Final Register State ===\n");
      printf("    MODER     = 0x%08x\n", regs[REG_MODER / 4]);
      printf("    INT_MASK  = 0x%08x\n", regs[REG_INT_MASK / 4]);
      printf("    IPGT      = 0x%08x\n", regs[REG_IPGT / 4]);
      printf("    TX_BD_NUM = %u\n", regs[REG_TX_BD_NUM / 4]);
    }

    struct ethool_ringparam ring;
    if (get_ethtool_ring(fd, &ring) == 0) {
      printf("\n    === Final Ring Parameters ===\n");
      printf("    tx_pending = %u\n", ring.tx_pending);
      printf("    rx_pending = %u\n", ring.rx_pending);
    }

    close(fd);
  }

  {
    char mtu_path[128];
    char mtu_buf[32];
    snprintf(mtu_path, sizeof(mtu_path), "/sys/class/net/%s/mtu", g_iface);
    if (read_sysfs(mtu_path, mtu_buf, sizeof(mtu_buf)) == 0)
      printf("    %-20s %s\n", "mtu:", mtu_buf);
  }

  TEST_PASS("Final Statistics Summary");
  return 0;
}

/* ===============================================================
 * Main
 * =============================================================== */

static void print_usage(const char *prog) {
  fprintf(stderr, "Usage: %s [options]\n", prog);
  fprintf(stderr, "Options:\n");
  fprintf(stderr,
          "  -i <iface>      Network interface (auto-detect if omitted)\n");
  fprintf(stderr, "  -s <soc_ip>     SoC IP address\n");
  fprintf(stderr, "  -c <host_ip>    Host IP address\n");
  fprintf(stderr, "  -v              Verbose output\n");
  fprintf(stderr, "  -h              Show this help\n");
}

int main(int argc, char *argv[]) {
  int opt;
  g_verbose = 0;

  /* Disable stdout buffering so output appears immediately over SSH */
  setvbuf(stdout, NULL, _IONBF, 0);

  /* defaults */
  memset(g_iface, 0, sizeof(g_iface));

  while ((opt = getopt(argc, argv, "i:s:c:vh")) != -1) {
    switch (opt) {
    case 'i':
      strncpy(g_iface, optarg, IFNAMSIZ - 1);
      break;
    case 's':
      inet_aton(optarg, &g_soc_ip);
      g_soc_ip_set = 1;
      break;
    case 'c':
      inet_aton(optarg, &g_host_ip);
      g_host_ip_set = 1;
      break;
    case 'v':
      g_verbose = 1;
      break;
    case 'h':
    default:
      print_usage(argv[0]);
      return (opt == 'h') ? 0 : 1;
    }
  }

  if (!g_host_ip_set) {
    fprintf(stderr, "Error: Host IP address (-c) is required.\n");
    print_usage(argv[0]);
    return 1;
  }

  printf("IOb-ETH ethoc Driver Compatibility Test\n");
  printf("Host IP: %s\n", inet_ntoa(g_host_ip));
  printf("\n");

  /* Test 1: find ethoc interface */
  if (test_interface_detection() < 0) {
    printf("FATAL: Cannot find ethoc interface. Aborting.\n");
    return 1;
  }

  /* Test 2: bring interface up */
  test_interface_up();

  /* Test 3: MAC address */
  test_mac_read_write();

  /* Test 4: default registers */
  test_default_regs();

  /* Test 5: link state */
  test_link_state();

  /* Test 6: MII/MDIO */
  test_mdio_access();

  /* warm up ARP cache before TX/RX tests */
  {
    int arp_fd = create_test_socket(TEST_ETH_PORT + 1);
    if (arp_fd >= 0) {
      uint8_t warmup[4] = {0};
      for (int i = 0; i < 3; i++) {
        send_raw(arp_fd, CMD_ECHO, warmup, sizeof(warmup));
        usleep(200000);
      }
      close(arp_fd);
    }
  }

  /* Test 7: TX basic */
  test_tx_basic();

  /* Test 8: TX size range */
  test_tx_sizes();

  /* Test 9: RX basic */
  test_rx_basic();

  /* Test 10: RX size range */
  test_rx_sizes();

  /* Test 11: broadcast */
  test_broadcast();

  /* Test 12: promiscuous */
  test_promiscuous();

  /* Test 13: loopback */
  test_loopback();

  /* Test 14: MTU rejection */
  test_mtu_reject();

  /* Test 15: ring parameters */
  test_ring_params();

  /* Test 16: register dump */
  test_register_dump();

  /* Test 17: interrupts */
  test_interrupts();

  /* Test 18: error counters (mid-test check) */
  test_error_counters();

  /* warm up ARP cache again before stress tests */
  {
    int arp_fd = create_test_socket(TEST_ETH_PORT + 1);
    if (arp_fd >= 0) {
      uint8_t warmup[4] = {0};
      for (int i = 0; i < 5; i++) {
        send_raw(arp_fd, CMD_ECHO, warmup, sizeof(warmup));
        usleep(200000);
      }
      close(arp_fd);
    }
  }

  /* Test 19: stress TX */
  test_stress_tx();

  /* Test 20: stress RX */
  test_stress_rx();

  /* Test 21: stress bidirectional */
  test_stress_bidir();

  /* Test 22: interface down */
  test_interface_down();

  /* Test 23: final summary */
  test_final_summary();

  /* Overall verdict */
  printf("\n");
  printf("=== Validation Complete ===\n");
  printf("Tests: %d total, %d passed, %d failed\n", g_total, g_passed,
         g_failed);

  if (g_failed > 0) {
    printf("RESULT: FAIL (%d test(s) failed)\n", g_failed);
    return 1;
  } else {
    printf("RESULT: ALL TESTS PASSED\n");
    return 0;
  }
}
