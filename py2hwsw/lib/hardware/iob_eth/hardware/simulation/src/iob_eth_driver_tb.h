#ifndef H_IOB_ETH_DRIVER_TB_H
#define H_IOB_ETH_DRIVER_TB_H

#include "iob_tasks.h"

void eth_setup(iob_native_t *eth_if);
void eth_relay_frames(iob_native_t *eth_if);

#endif // H_IOB_ETH_DRIVER_TB_H
