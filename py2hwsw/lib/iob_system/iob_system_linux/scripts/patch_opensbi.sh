#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# Patch OpenSBI fw_base.S to disable CLEAR_MDT for VexRiscv cores.
# This script is invoked from sw_build.mk before the OpenSBI build.

set -euo pipefail

# Determine the OpenSBI fw_base.S path relative to the repository root.
# ROOT_DIR points to the project root (one level above this script).
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
FW_BASE="${ROOT_DIR}/submodules/iob_linux/submodules/OpenSBI/firmware/fw_base.S"

if [[ -f "$FW_BASE" ]]; then
  echo "Patching $FW_BASE to comment out CLEAR_MDT calls..."
  # Replace lines that contain exactly a TAB followed by 'CLEAR_MDT t0' with a commented version.
  # Use sed to prepend '# ' to the line.
  sed -i '/^\tCLEAR_MDT t0$/ s/^/# /' "$FW_BASE"
else
  echo "Error: $FW_BASE not found" >&2
  exit 1
fi
