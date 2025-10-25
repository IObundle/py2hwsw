# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def export_core(core):
    core_file_content = f"""\
CAPI=2:

name: {core.name}
version: {core.version}

filesets:
  rtl:
    files:
      - hardware/src/*.v
    file_type: verilog
  sim:
    files:
      - hardware/simulation/src/*.v
    file_type: verilog

targets:
  default:
    filesets:
      - rtl
  sim:
    filesets:
      - rtl
      - sim
"""

    os.makedirs("fusesoc", exist_ok=True)
    # Write the core description to the .core file
    core_file_path = f"fusesoc/{core.name}.core"
    with open(core_file_path, "w") as f:
        f.write(core_file_content)

    print(f"FuseSoC core file generated at: {core_file_path}")
