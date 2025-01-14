#!/bin/bash
source /opt/ic_tools/init/init-xcelium1903-hf013
xmvlog $CFLAGS $VSRC
xmelab $EFLAGS worklib.iob_eth_tb:module
xmsim  $SFLAGS worklib.iob_eth_tb:module
