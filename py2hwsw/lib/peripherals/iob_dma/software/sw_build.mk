# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

UTARGETS=tb
TB_INCLUDES=-I./src -I./simulation/src
TB_SRC=./src/iob_dma_csrs.c
TB_SRC+=./simulation/src/iob_axistream_in_csrs.c
TB_SRC+=./simulation/src/iob_axistream_out_csrs.c
TB_SRC+=./src/iob_dma.c
