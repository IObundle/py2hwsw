# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# annotations path
CUSTOM_COVERAGE_FLAGS=cov_annotated
CUSTOM_COVERAGE_FLAGS+=-E iob_uut.v
CUSTOM_COVERAGE_FLAGS+=--waive uart_coverage.waiver
CUSTOM_COVERAGE_FLAGS+=--waived-tag
CUSTOM_COVERAGE_FLAGS+=-o uart_coverage.rpt
