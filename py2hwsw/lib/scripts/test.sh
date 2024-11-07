#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

set -e

#find directories containing testbenches
TBS=`find ${LIB_DIR}/hardware | grep _tb.v | grep -v include`

FILTER_OUT_TBS=""
#for debug
#FILTER_OUT_TBS="iob_system_tb.v iob_uart_tb.v iob_div_subshift_tb.v iob_div_subshift_frac_tb.v iob_div_pipe_tb.v iob_and_tb.v iob_aoi_tb.v iob_csrs_demo_tb.v iob_pulse_gen_tb.v iob_ctls_tb.v iob_prio_enc_tb.v iob_shift_reg_tb.v iob_timer_tb.v iob_nco_tb.v iob_ram_t2p_be_tb.v iob_ram_2p_tb.v iob_ram_tdp_tb.v iob_ram_atdp_be_tb.v iob_ram_tdp_be_xil_tb.v iob_ram_2p_tb.v iob_ram_tdp_tb.v iob_ram_atdp_be_tb.v iob_ram_t2p_tb.v iob_ram_sp_se_tb.v iob_ram_sp_tb.v iob_ram_t2p_tiled_tb.v iob_ram_atdp_tb.v iob_ram_sp_be_tb.v iob_ram_tdp_be_tb.v iob_ram_at2p_tb.v iob_ram_tdp_tb.v iob_rom_sp_tb.v iob_rom_atdp_tb.v iob_regfile_sp_tb.v iob_rom_tdp_tb.v iob_rom_2p_tb.v iob_axis2axi_tb.v iob_fifo_async_tb.v iob_fifo_sync_tb.v"

TBS_FILTERED=""
for i in $TBS; do
    if ! echo $FILTER_OUT_TBS | grep -q `basename $i` ; then
        TBS_FILTERED+=" $i";
    fi
done

echo $TBS_FILTERED

#extract respective directories
for i in $TBS_FILTERED; do TB_DIRS+=" `dirname $i`" ; done

#extract respective modules - go back from MODULE/hardware/simulation/src
for i in $TB_DIRS; do MODULES+=" `basename $(builtin cd $i/../../..; pwd)`" ; done

#test first argument is "clean", run make clean for all modules and exit
if [ "$1" == "clean" ]; then
    for i in $MODULES; do 
        DEFAULT_BUILD_DIR=`py2hwsw $i print_build_dir`
        make clean CORE=$i BUILD_DIR=../../${DEFAULT_BUILD_DIR}
    done
    exit 0
fi

#test if first argument is test and run all tests
if [ "$1" == "test" ]; then
    for i in $MODULES; do
        echo -e "\n\033[1;33mTesting module '${i}'\033[0m"
        DEFAULT_BUILD_DIR=`py2hwsw $i print_build_dir`
        make -f ${LIB_DIR}/Makefile clean setup CORE=$i BUILD_DIR=../../${DEFAULT_BUILD_DIR}
        make -C ../../${DEFAULT_BUILD_DIR} sim-run
    done
    exit 0
fi

#test if first argument is "build" and run build for single module
if [ "$1" == "build" ]; then
    DEFAULT_BUILD_DIR=`py2hwsw $2 print_build_dir`
    make clean setup CORE=$2 BUILD_DIR=../../${DEFAULT_BUILD_DIR}
    make -C ../../${DEFAULT_BUILD_DIR} sim-build
    exit 0
fi

#run single test
DEFAULT_BUILD_DIR=`py2hwsw $1 print_build_dir`
make clean setup CORE=$1 BUILD_DIR=../../${DEFAULT_BUILD_DIR}
make -C ../../${DEFAULT_BUILD_DIR} sim-run VCD=$VCD
