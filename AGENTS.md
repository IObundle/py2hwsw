# AGENTS.md

Py2HWSW: Python framework that generates lint-friendly Verilog, software drivers, and build trees for embedded HW/SW (RISC-V SoC) projects. GPL-3.0-only, REUSE-compliant.

## Environment

- Everything runs in a **nix-shell**. Enter it from `py2hwsw/lib/` (contains `default.nix`): `nix-shell` or `nix-shell --run "<cmd>"`. First entry downloads all deps (slow).
- Deps are pinned in `py2hwsw/lib/default.nix` (custom verilator 5.040, yosys, riscv-gnu-toolchain, verible, black, reuse, custom fusesoc).
- The shell adds `bin/` to PATH (provides `py2hwsw` CLI) and sets PYTHONPATH.
- Alt install: `pip install -e .` (setup.py); Docker image: `py2hwsw/docker/` (`make build` / `make run`).

## Commands (verify order: setup → build → test)

All from `py2hwsw/lib/` inside nix-shell unless noted:

```bash
# CI equivalent (full lib simulation suite)
nix-shell --run "make sim-test"

# Single core: generate build dir, then simulate
make setup CORE=iob_uart
make -C build sim-run                 # build dir name from: py2hwsw <core> print_build_dir

# Or one-shot single-module test (clean + setup + sim-run)
nix-shell --run "scripts/test.sh iob_uart"   # also: test.sh test | clean | build <mod>

# Simulators/boards
make sim-build CORE=iob_uart SIMULATOR=icarus   # icarus|verilator|vcs|questa|xcelium
make fpga-build CORE=iob_system BOARD=iob_aes_ku040_db_g

# FuseSoC export/test
make fusesoc-export CORE=iob_uart
nix-shell --run "py2hwsw --print_lib_cores"

# Docs (LaTeX): design spec PDF
make -C py2hwsw/lib py2-doc-build

# REUSE license lint (CI runs after sim-test)
nix-shell py2hwsw/lib --run "reuse lint"
```

CI (`.github/workflows/ci.yml`): checkout with `submodules: recursive`, `git clean -ffdx`, then `cd py2hwsw/lib && nix-shell --run "make sim-test"`, then `reuse lint`.

## Architecture

- **CLI**: `py2hwsw <core> [setup|clean|print_core|print_build_dir|print_core_version|print_core_dict|deliver|export_fusesoc] --build_dir <dir> --py_params 'k=v:k=v'`. Entry: `py2hwsw/scripts/py2hwsw.py`; core logic in `py2hwsw/scripts/iob_core.py`, `iob_base.py`.
- **Framework code** lives in `py2hwsw/scripts/` (verilog_gen, verilog_lint, verilog_format, setup_srcs, doc_gen, ipxact_gen, config_gen, …). Shared tool templates (sim/fpga/syn/lint makefiles) in `py2hwsw/hardware/`; copied into each generated build dir along with `py2hwsw/build.mk` (top Makefile of a build dir: `sim-*`, `fpga-*`, `lint-*`, `syn-*`, `doc-*`, `test` targets).
- **Library of cores** in `py2hwsw/lib/`:
  - `lib/hardware/**` – buses, memories, fifo, clocks_resets, arith_logic, basic_tests, altera/amd vendor wrappers, …
  - `lib/peripherals/**` – iob_uart, iob_gpio, iob_timer, iob_dma, …
  - `lib/iob_system/` – RISC-V SoC (`iob_system.py`) + CPU/cache/CLINT/PLIC git submodules under `submodules/` and `iob_system_linux/`
  - `lib/software/**` – C libs and Linux driver generators
- **A core** = a Python file `<core_name>.py` defining a class (subclass of `iob_core`). Located by name anywhere under `lib/`. Testbenches: `<core>/hardware/simulation/src/<core>_tb.v`. Tester variants live in `<core>_tester/` subdirs.
- **Verilog generation**: cores emit formatted (verible) and lint-checked (verible rules in `py2hwsw/scripts/verible-*.rules`) Verilog. Cores not in `CORES_READY_FOR_LINT` (lib/Makefile) are set up with `--no_verilog_lint`.
- Generated artifacts go to `build/` (or `BUILD_DIR`); `.gitignore` covers `__pycache__/` and `py2hwsw_generated_docs/`.

## Testing quirks

- No pytest/unit tests — "tests" = Verilog testbenches simulated via `scripts/test.sh` (finds `*_tb.v`, skips `submodules/` and `iob_system_linux` because icarus is too slow for it).
- `make sim-test` / `test.sh test` re-runs clean+setup per module (serial, can take a while).
- Full `test` target in a build dir = `sim-test fpga-test doc-test`; `dtest` adds `syn-test`.
- FPGA/board targets need hardware; use `board_server` targets for shared boards.

## Conventions & gotchas

- **License headers**: every source file needs an SPDX header (`SPDX-FileCopyrightText: 2026 IObundle` / `SPDX-License-Identifier: GPL-3.0-only`, except `./bin/py2hwsw` and submodule paths). Manage via `py2hwsw/scripts/manage_headers.py`; exclusions in `.ignore_file_headers`. CI enforces `reuse lint`. License texts: `py2hwsw/scripts/LICENSES/` (root `LICENSES` is a symlink).
- **Style**: Python → black; C/C++ → clang-format LLVM (`py2hwsw/.clang-format`); Verilog → verible (rules in `py2hwsw/scripts/`). Note: `lib/README.md` references `scripts/sw_format.py` / `make python-format` — that script does not exist; run `black` directly.
- **Git submodules**: `py2hwsw/lib/iob_system/submodules/*` and `iob_system_linux/submodules/*` are external repos — do not edit their contents. Clone with `--init --recursive`.
- **py_params format**: colon-separated `key=value` (argparse limitation), e.g. `--py_params 'cpu=iob_vexriscv:init_mem=1'`. Makefile maps common vars (`CPU`, `INIT_MEM`, `CSR_IF`, …) into `PY_PARAMS`.
- **Build-dir Makefile** differs from `lib/Makefile`: build-dir targets operate on the generated tree; always pass `CORE=`/`BUILD_DIR=` when using `lib/Makefile`.
- Docs: user guide sources in `py2hwsw/py2hwsw_document/`; per-core docs in each core's `document/`. `py2hwsw --py2hwsw_docs` scaffolds generated doc tree.
