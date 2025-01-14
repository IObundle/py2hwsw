#include "iob-eth.h"
#include "iob-uart.h"
#include "periphs.h"
#include "printf.h"
#include "stdlib.h"
#include "system.h"

#define TEST_SIZE 2048

#define PAGE_ALIGN(val) ((val + 0xfff) & ~0xfff)

#ifdef SIM
#undef ETH_NBYTES
#define ETH_NBYTES 1024
#define ADDRESS 2048
#define ITERATIONS 1
#define TIMES 1
#endif

int main() {
  /* 1xTEST_SIZE (send data, 1x for send_file(), 1x for send_variable_file())
   * 1xTEST_SIZE (rcv_file())
   * 1xTEST_SIZE (rcv_variable_file())
   */
  char buffer[3 * TEST_SIZE] = {0};
  int i;
  int bufferAddress = 0;

  uart_init(UART_BASE, FREQ / BAUD);
  eth_init(ETHERNET_BASE);

  uart_puts("\nSuccessful Init\n");

#ifdef SIM
  printf("Size:%d:%x\n", ETH_NBYTES, ETH_NBYTES);

  buffer[0] = 0xef;
  buffer[1] = 0xfe;
  buffer[2] = 0xef;
  buffer[3] = 0xfe;
  for (int i = 4; i < ETH_NBYTES; i++) {
    buffer[i] = (char)(i / 4);
  }

  // Send frame containing test data
  eth_send_frame(buffer, ETH_NBYTES);

  int address = 0;
  for (int k = 0; k < ITERATIONS; k++) {
    printf("%d\n", (ETH_NBYTES - k));
    for (int i = 0; i < TIMES; i++) {
      while (eth_rcv_frame(&buffer[address], (ETH_NBYTES - k), 5000000))
        ; // Data in

      printf("%08x\n", &buffer[address]);
      for (int j = 0; j < 8; j++) {
        printf("%02x ", buffer[address + j]);
      }
      printf("\n");
      for (int j = 0; j < 8; j++) {
        printf("%02x ", buffer[address + (ETH_NBYTES - k) - 6 + j]);
      }
      printf("\n");

      eth_send_frame(&buffer[address], (ETH_NBYTES - k));
      address += ADDRESS + 1;
    }
  }
#else  // ifndef SIM
  printf("\nTesting send,send_variable,rcv and rcv_variable\n");
  printf("In another terminal, do \"make test-eth\" to perform the test\n");
  printf("\"make test-eth\" can also be run before running the firmware\n");
  printf("It should not matter which one is ran first\n");
  printf("For pc-emul, do \"make pc-test-eth\"\n\n");

  bufferAddress = 0;
  for (int i = 0; i < TEST_SIZE; i++) {
    buffer[bufferAddress + i] =
        (i % 4) + '0'; // Fill buffer with a repeating pattern of "0123"
  }

  printf("Testing send file\n");
  eth_send_file(&buffer[bufferAddress], TEST_SIZE);

  printf("Testing send variable file\n");
  eth_send_variable_file(&buffer[bufferAddress], TEST_SIZE);

  printf("Testing receive file\n");
  bufferAddress = PAGE_ALIGN(TEST_SIZE);
  eth_rcv_file(&buffer[bufferAddress], TEST_SIZE);

  printf("Testing receive variable file\n");
  bufferAddress = PAGE_ALIGN(TEST_SIZE * 2);
  int res = eth_rcv_variable_file(&buffer[bufferAddress]);

  if (res != TEST_SIZE) {
    printf("Error, the size of the file received is different\n");
    printf("Should be: %d but it is: %d\n", TEST_SIZE, res);
  }
#endif // ifdef SIM

  uart_puts("\nFinish\n");
  uart_puts("\nWaiting some time to finish\n");
  uart_finish();
}
