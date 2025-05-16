# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

UTARGETS=tb
TB_INCLUDES=-I./src -I./simulation/src
CSRS=./src/iob_dma_csrs.c
CSRS+=./simulation/src/iob_axistream_in_csrs.c
CSRS+=./simulation/src/iob_axistream_out_csrs.c
CSRS+=./src/iob_dma.c
