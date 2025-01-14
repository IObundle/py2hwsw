// driver functions
#include "stdint.h"
#include <stdlib.h>

void eth_init(int base_address, void (*clear_cache_func)(void));

void eth_init_clear_cache(void (*clear_cache_func)(void));

void eth_init_mem_alloc(void *(*mem_alloc_func)(size_t),
                        void (*mem_free_func)(void *));

void eth_init_mac(int base_address, uint64_t mac_addr, uint64_t dest_mac_addr);

void eth_reset_bd_memory();

unsigned short int eth_get_payload_size(unsigned int idx);

void eth_set_payload_size(unsigned int idx, unsigned int size);

// Care when using this function directly, too small a size or too large might
// not work (frame does not get sent)
void eth_send_frame(char *data_to_send, unsigned int size);

/* Function name: eth_rcv_frame
 * Inputs:
 * 	- data_rcv: char array where data received will be saved
 * 	- size: number of bytes to be received
 * 	- timeout: number of cycles (approximately) in which the data should be
 * received Output:
 * 	- Return -1 if timeout occurs (no data received), or 0 if data is
 * 	successfully received
 */
int eth_rcv_frame(char *data_rcv, unsigned int size, int timeout);

void eth_set_receive_timeout(unsigned int timeout);

unsigned int eth_rcv_file(char *data, int size);

unsigned int eth_send_file(char *data, int size);

unsigned int eth_rcv_variable_file(char *data);

unsigned int eth_send_variable_file(char *data, int size);

void eth_wait_phy_rst();

void eth_print_status(void);
