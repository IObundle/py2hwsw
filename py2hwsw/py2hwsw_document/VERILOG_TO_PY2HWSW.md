<!--
SPDX-FileCopyrightText: 2026 IObundle

SPDX-License-Identifier: GPL-3.0-only
-->

# Converting Verilog to py2hwsw

This guide covers how to translate Verilog modules into py2hwsw Python definitions,
and how to write py2hwsw modules from scratch.

---

## 1. Overview

py2hwsw is a Python framework that generates Verilog RTL (and supporting files) from
a Python `setup()` function that returns an `attributes_dict`.

### Module Hierarchy

```
iob_system          Top-level SoC (is_system=True)
  └─ iob_core       Reusable IP block (both iob_module + iob_instance)
       └─ iob_block Sub-module instance
            └─ iob_module  Describes Verilog body (ports, wires, snippets)
```

- **`iob_module`**: Describes a Verilog module's internals (ports, wires, logic).
- **`iob_instance`**: Describes how a module is instantiated (port connections, parameters).
- **`iob_core`**: Inherits both. The class you instantiate for each IP.
- **`iob_block`**: Helper that calls `get_core_obj()` to create sub-instances.

### The `setup()` Function

Every py2hwsw module defines a `setup(py_params_dict)` function that returns an
`attributes_dict` dictionary. This dictionary describes the module completely:

```python
def setup(py_params_dict):
    attributes_dict = {
        "name": "my_module",
        "generate_hw": True,  # or False for hand-written templates
        "confs": [...],       # Verilog parameters/macros
        "ports": [...],       # Module IO ports
        "wires": [...],       # Internal wires
        "subblocks": [...],   # Sub-module instances
        "snippets": [...],    # Raw Verilog code
    }
    return attributes_dict
```

### Two Generation Modes

| Mode | `generate_hw` | What happens |
|------|---------------|--------------|
| Auto-generate | `True` | py2hwsw writes the full `.v` file from the dict |
| Hand-written | `False` | Only `.vs` snippet files are generated; the `.v` is a hand-written template that includes them via `` `include `` |

Most peripherals use `generate_hw: True`. Complex modules with custom FSMs or
intricate logic use `False` and write the Verilog body by hand.

---

## 2. Minimal Module Template

```python
# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {"type": "iob_clk"},
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "data_i",
                "descr": "Data input",
                "signals": [
                    {"name": "data_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "data_o",
                "descr": "Data output",
                "signals": [
                    {"name": "data_o", "width": "DATA_W", "isvar": True},
                ],
            },
        ],
        "wires": [],
        "subblocks": [],
        "snippets": [
            {
                "verilog_code": """
    assign data_o = data_i;
""",
            },
        ],
    }
    return attributes_dict
```

---

## 3. Ports

Ports represent the module's IO. Each port has a **name** and a list of **signals**.

### Naming Rules (Enforced)

Every port name **must** end with one of:

| Suffix | Direction | Meaning |
|--------|-----------|---------|
| `_i` | input | All signals must have `direction="input"` |
| `_o` | output | All signals must have `direction="output"` |
| `_io` | inout | Must have at least one input and one output signal |
| `_s` | subordinate (slave) | Requires an `interface` |
| `_m` | manager (master) | Requires an `interface` |

### Port with Explicit Signals

```python
{
    "name": "config_i",
    "descr": "Configuration register input",
    "signals": [
        {"name": "mode_i", "width": 2, "descr": "Operating mode"},
        {"name": "enable_i", "width": 1, "descr": "Enable signal"},
    ],
}
```

### Port with a Single Signal (Shorthand)

```python
{
    "name": "interrupt_o",
    "signals": [
        {"name": "interrupt_o", "width": 1, "descr": "Interrupt output"},
    ],
}
```

### Clock Port (Standard Interface Shorthand)

The clock interface is the most common. Use the `iob_clk` interface type:

```python
{
    "name": "clk_en_rst_s",
    "signals": {"type": "iob_clk"},
    "descr": "Clock, clock enable and reset",
}
```

This auto-generates signals: `clk_i`, `cke_i`, `arst_i` (and optionally `rst_i`,
`en_i` depending on configuration). The port suffix `_s` indicates it is a
subordinate clock interface.

### Port with `isvar` (Register Output)

Use `"isvar": True` on output signals that are registered (generated as `reg`
instead of `wire`):

```python
{
    "name": "count_o",
    "signals": [
        {"name": "count_o", "width": 8, "isvar": True},
    ],
}
```

---

## 4. Wires

Wires are internal signals. They have **no direction suffix** in their name.

```python
"wires": [
    {
        "name": "counter",
        "descr": "Internal counter",
        "signals": [
            {"name": "counter", "width": 32},
        ],
    },
    {
        "name": "status",
        "descr": "Status register",
        "signals": [
            {"name": "status_rd", "width": 32},  # readable status
        ],
    },
],
```

### Signal Deduplication

If you declare a signal name in multiple wires, py2hwsw automatically replaces
duplicates with an `iob_signal_reference` (no duplicate `wire` declarations in
the Verilog output). The duplicate must have identical attributes.

### Wire Groups for Multi-Signal Interfaces

Wire groups bundle related signals:

```python
{
    "name": "timer_reg_interface",
    "descr": "Register interface to timer core",
    "signals": [
        {"name": "enable_wr"},
        {"name": "reset_wr"},
        {"name": "sample_wr"},
        {"name": "time_now"},
    ],
},
```

### Wires from Ports (Common Pattern)

A common pattern is to create internal wires that mirror external ports (with
the direction suffix stripped):

```python
import copy

for port in attributes_dict["ports"]:
    if port["name"].startswith("input") or port["name"].startswith("output"):
        wire = copy.deepcopy(port)
        wire["name"] = wire["name"][:-2]       # strip _i / _o suffix
        wire["signals"][0]["name"] = wire["signals"][0]["name"][:-2]
        attributes_dict["wires"].append(wire)
```

---

## 5. Configuration Parameters (`confs`)

Parameters and macros that appear in the Verilog `parameter` / `` `define `` sections.

### Types

| Type | Letter | Generates |
|------|--------|-----------|
| Parameter | `P` | `parameter NAME = VAL` |
| Macro | `M` | `` `define NAME VAL `` |
| Constant | `C` | `localparam NAME = VAL` |
| Derived | `D` | Auto-computed (e.g., `ADDR_W` from CSRs) |

### Example

```python
"confs": [
    {
        "name": "DATA_W",
        "type": "P",
        "val": "32",
        "min": "NA",
        "max": "NA",
        "descr": "Data bus width",
    },
    {
        "name": "PREAMBLE",
        "type": "M",
        "val": "8'h55",
        "min": "NA",
        "max": "NA",
        "descr": "Ethernet preamble value",
    },
],
```

### Reading Parameters in `setup()`

```python
N_INPUTS = int(py_params_dict.get("n_inputs", 1))
```

---

## 6. Snippets (Inline Verilog)

For `generate_hw: True` modules, snippets provide the Verilog logic body:

```python
"snippets": [
    {
        "verilog_code": """
    assign data_o = data_i & {DATA_W{enable_i}};
    assign status_rd = {31'd0, busy};
""",
    },
],
```

You can have multiple snippets. They are inserted in order into the generated `.v`.

### Dynamic Snippets

Build Verilog strings dynamically in Python:

```python
verilog_code = ""
for idx in range(N_INPUTS):
    verilog_code += f"""
    assign input_{idx}_o = input_port_{idx}_i[INPUT_GPIO_W-1:0];
"""
attributes_dict["snippets"] = [{"verilog_code": verilog_code}]
```

---

## 7. Subblocks (Module Instances)

Subblocks instantiate other py2hwsw cores inside your module.

### Basic Subblock

```python
"subblocks": [
    {
        "core": "iob_timer_core",      # Name of the .py module to instantiate
        "instance_name": "timer_inst",       # Verilog instance name
        "instance_description": "Timer core",
        "connect": {
            "clk_en_rst_s": "clk_en_rst_s",     # port -> wire mapping
            "interrupt_o": "interrupt_o",
        },
    },
],
```

### Subblock with Parameters

```python
{
    "core": "iob_fifo_sync",
    "instance_name": "data_fifo",
    "parameters": {
        "DATA_W": 8,
        "ADDR_W": "BUFFER_W",
    },
    "connect": {
        "clk_en_rst_s": "clk_en_rst_s",
        "data_i": "fifo_w_data",
        "data_o": "fifo_r_data",
    },
},
```

### The `connect` Dictionary

Maps **port names of the subblock** to **wire names of the parent**.

```python
"connect": {
    "<subblock_port>": "<parent_wire_or_port>",
    ...
}
```

- Both sides can be strings (port name -> wire name).
- You can connect to the parent's ports directly (e.g., `"clk_en_rst_s"`).
- `"control_if_m"` on `iob_csrs` is **auto-connected** -- you don't need to list it.
- Unused output ports can be connected to `"z"` to leave them unconnected.
- Signal remapping uses a tuple: `("port_name", ["src:dst", ...])`.

### Implicit Wire Creation

If the parent doesn't have a wire matching the connected port, py2hwsw
**automatically creates one** with the same signals as the port. This is
convenient but can lead to unexpected wire names.

---

## 8. iob_csrs (Register Definitions)

`iob_csrs` is the standard subblock for software-accessible registers. It
auto-generates the register file, the CSR bus port, and address decoding.

### Basic CSR Definition

```python
"subblocks": [
    {
        "core": "iob_csrs",
        "instance_name": "csrs",
        "instance_description": "Control/Status Registers",
        "csr_if": "iob",           # "iob", "axil", "wb", etc.
        "autoaddr": True,          # Auto-assign addresses (default True)
        "rw_overlap": False,       # Allow overlapping R/W addresses
        "csrs": [
            {
                "name": "my_reg",
                "descr": "My register",
                "mode": "W",        # "W", "R", "RW", or "NOAUTO"
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,   # 0 = single register, >0 = array
                "descr": "Description for docs",
            },
        ],
        "connect": {
            "clk_en_rst_s": "clk_en_rst_s",
            # 'control_if_m' is auto-connected
            "my_reg_o": "my_reg_wire",    # Output signal from CSRs -> wire
            "status_i": "status_wire",    # Input signal to CSRs <- wire
        },
    },
],
```

### CSR Modes

| Mode | Direction | Description |
|------|-----------|-------------|
| `"W"` | CSR -> core | Write-only. Generates `<name>_o` output signal. |
| `"R"` | core -> CSR | Read-only. Generates `<name>_i` input signal. |
| `"RW"` | Both | Generates both `_o` and `_i` signals. |
| `"NOAUTO"` | Both | Manual address assignment. Use for special registers. |

### NOAUTO Register Implementation

NOAUTO registers expose raw bus signals so you can implement custom register
behavior in snippets. The CSR block generates: `<name>_valid_wrrd`,
`<name>_wdata_wrrd`, `<name>_wstrb_wrrd`, `<name>_ready_wrrd`,
`<name>_rdata_wrrd`, `<name>_rvalid_wrrd`.

CSR register definition:

```python
{
    "name": "tx_bd_num",
    "mode": "RW",
    "n_bits": 32,
    "rst_val": 64,
    "addr": 32,
    "log2n_items": 0,
    "type": "NOAUTO",
},
```

Wire group (matching the raw bus signals):

```python
{
    "name": "tx_bd_num",
    "signals": [
        {"name": "tx_bd_num_valid_wrrd", "width": 1},
        {"name": "tx_bd_num_wdata_wrrd", "width": 32},
        {"name": "tx_bd_num_wstrb_wrrd", "width": 4},
        {"name": "tx_bd_num_ready_wrrd", "width": 1},
        {"name": "tx_bd_num_rdata_wrrd", "width": 32},
        {"name": "tx_bd_num_rvalid_wrrd", "width": 1},
    ],
},
```

Snippet implementing the register:

```verilog
reg [31:0] tx_bd_num_reg;
assign tx_bd_num_ready_wrrd  = 1'b1;
assign tx_bd_num_rdata_wrrd  = tx_bd_num_reg;

// Write logic
always @(posedge clk_i, posedge arst_i) begin
    if (arst_i)          tx_bd_num_reg <= 32'd64;
    else if (tx_bd_num_valid_wrrd && |tx_bd_num_wstrb_wrrd)
                         tx_bd_num_reg <= tx_bd_num_wdata_wrrd;
end

// Read-valid: one-cycle delayed (required by CSR bus FSM)
wire tx_bd_num_rvalid_nxt = tx_bd_num_valid_wrrd & ~(|tx_bd_num_wstrb_wrrd);
reg  tx_bd_num_rvalid_wrrd_reg;
always @(posedge clk_i, posedge arst_i) begin
    if (arst_i)          tx_bd_num_rvalid_wrrd_reg <= 1'b0;
    else if (cke_i)      tx_bd_num_rvalid_wrrd_reg <= tx_bd_num_rvalid_nxt;
end
assign tx_bd_num_rvalid_wrrd = tx_bd_num_rvalid_wrrd_reg;
```

**Important**: Always assign `ready_wrrd = 1` and implement `rvalid_wrrd` with
a one-cycle register. Without `rvalid`, read transactions hang the CSR bus FSM
in WAIT_RVALID forever.

### Register Groups

Group related registers for documentation:

```python
"csrs": [
    {
        "name": "control_group",
        "descr": "Control registers",
        "regs": [
            {"name": "enable", "mode": "W", "n_bits": 1, "rst_val": 0, "log2n_items": 0},
            {"name": "reset", "mode": "W", "n_bits": 1, "rst_val": 0, "log2n_items": 0},
        ],
    },
    {
        "name": "status_group",
        "descr": "Status registers",
        "regs": [
            {"name": "busy", "mode": "R", "n_bits": 1, "rst_val": 0, "log2n_items": 0},
            {"name": "data_low", "mode": "R", "n_bits": 32, "rst_val": 0, "log2n_items": 0},
        ],
    },
],
```

### What iob_csrs Auto-Generates

- A `control_if_m` port (manager bus interface, auto-connected to parent's CBUS).
- Per-register output/input ports named `<reg_name>_o` / `<reg_name>_i`.
- Address decoder, register file Verilog, and documentation.

### Register Signal Names

The CSR block generates ports based on register names:

- `"mode": "W"` register named `"enable"` -> port `enable_o` (output from CSRs)
- `"mode": "R"` register named `"status"` -> port `status_i` (input to CSRs)
- These ports connect to your internal wires via the `connect` dict.

### CSRs with Explicit Addresses

```python
{
    "name": "moder",
    "mode": "RW",
    "n_bits": 32,
    "rst_val": 40960,
    "addr": 0,             # Explicit byte address
    "log2n_items": 0,
},
```

---

## 9. Interfaces

Standard interfaces group related signals (bus protocols, memories, clocks) and
handle direction swapping for manager/subordinate connections automatically.

### Clock Interface (`iob_clk`)

Used in nearly every module:

```python
{
    "name": "clk_en_rst_s",
    "signals": {"type": "iob_clk"},
    "descr": "Clock, clock enable and reset",
}
```

Generates: `clk_i`, `cke_i`, `arst_i` (and optionally `rst_i`, `en_i`).

Configuration options for `iobClkInterface`:
- `has_cke` (default True) -- clock enable
- `has_arst` (default True) -- async reset
- `has_rst` (default False) -- sync reset
- `has_en` (default False) -- enable

```python
# Clock with sync reset, no async reset:
"signals": {"type": "iob_clk", "has_arst": False, "has_rst": True},
```

### IOb Bus Interface

Standard IOb bus for CSR access:

```python
# As a port (manager side):
{
    "name": "cbus_m",
    "signals": {
        "type": "iob",
        "ADDR_W": "ADDR_W",
        "DATA_W": "DATA_W",
    },
}

# As a port (subordinate side):
{
    "name": "cbus_s",
    "signals": {
        "type": "iob",
        "ADDR_W": "ADDR_W",
        "DATA_W": "DATA_W",
    },
}
```

Generates signals: `iob_valid_o`, `iob_addr_o`, `iob_wdata_o`, `iob_wstrb_o`,
`iob_rvalid_i`, `iob_rdata_i`, `iob_ready_i` (directions adjusted for `_s`/`_m`).

### AXI-Lite Interface

```python
{
    "name": "axil_m",
    "signals": {
        "type": "axil",
        "ADDR_W": "AXI_ADDR_W",
        "DATA_W": "AXI_DATA_W",
    },
}
```

Generates AXI-Lite signals: `axil_awaddr`, `axil_awvalid`, `axil_awready`,
`axil_wdata`, `axil_wstrb`, `axil_wvalid`, `axil_wready`, `axil_bresp`,
`axil_bvalid`, `axil_bready`, `axil_araddr`, `axil_arvalid`, `axil_arready`,
`axil_rdata`, `axil_rresp`, `axil_rvalid`, `axil_rready`.

Options: `has_read_if`, `has_write_if`, `has_prot`.

### AXI Full Interface

```python
{
    "name": "axi_m",
    "signals": {
        "type": "axi",
        "ID_W": "AXI_ID_W",
        "ADDR_W": "AXI_ADDR_W",
        "DATA_W": "AXI_DATA_W",
        "LEN_W": "AXI_LEN_W",
    },
}
```

### Memory Interfaces

Symmetric (both ports same width):

```python
{
    "name": "mem_a",
    "signals": {
        "type": "symMem",
        "genre": "ram_tdp",    # ram_sp, ram_2p, ram_tdp, rom_sp, etc.
        "ADDR_W": "ADDR_W",
        "DATA_W": "DATA_W",
    },
}
```

Asymmetric (different read/write widths):

```python
{
    "name": "mem_a",
    "signals": {
        "type": "asymMem",
        "genre": "ram_t2p",
        "ADDR_W": "ADDR_W",
        "W_DATA_W": "W_DATA_W",
        "R_DATA_W": "R_DATA_W",
    },
}
```

Available memory genres: `ram_sp`, `ram_2p`, `ram_tdp`, `ram_at2p`, `ram_atdp`,
`ram_t2p`, `ram_t2p_be`, `ram_sp_be`, `rom_sp`, `rom_2p`, `rom_tdp`, `rom_atdp`,
and more (see `interfaces.py`).

### Manager/Subordinate (`_s`/`_m`) Ports

When a port name ends in `_s` (subordinate/slave) or `_m` (manager/master), the
interface's `if_direction` is set automatically, and all signal directions are
swapped:

- `_m` port: signals keep their default direction (manager drives outputs).
- `_s` port: signal directions are reversed (subordinate receives as inputs).

```python
# RAM true dual port - subordinate side (port inside the RAM module):
{
    "name": "port_a_io",
    "signals": {
        "type": "symMem",
        "genre": "ram_tdp",
        "ADDR_W": "ADDR_W",
        "DATA_W": "DATA_W",
    },
}
```

### Available Interface Types

| Type | Class | Description |
|------|-------|-------------|
| `iob_clk` | `iobClkInterface` | Clock + optional cke/arst/rst/en |
| `iob` | `iobInterface` | IOb bus (valid/addr/wdata/wstrb/rvalid/rdata/ready) |
| `axil` | `AXILiteInterface` | AXI-Lite full (read + write channels) |
| `axil_read` | `AXILiteInterface` | AXI-Lite read only |
| `axil_write` | `AXILiteInterface` | AXI-Lite write only |
| `axi` | `AXIInterface` | AXI full |
| `symMem` | `symMemInterface` | Symmetric memory (RAM/ROM) |
| `asymMem` | `asymMemInterface` | Asymmetric memory |
| `wb` | `wishboneInterface` | Wishbone bus |
| `axis` | `AXIStreamInterface` | AXI Stream |
| `rs232` | RS232 | UART |
| `mii` | MII | Media Independent Interface |

---

## 10. `generate_hw: False` (Hand-Written Templates)

When your Verilog is too complex for snippets (custom FSMs, pipeline stages,
intricate combinational logic), use `generate_hw: False`. The `.py` file declares
ports/wires/subblocks (so they appear in documentation and auto-connect), but
the actual `.v` is written by hand.

### The `.py` File

```python
def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "ports": [
            {
                "name": "arst_i",
                "signals": [{"name": "arst_i", "width": 1}],
            },
            {
                "name": "fifo_o",
                "descr": "Byte push interface to data FIFO",
                "signals": [
                    {"name": "wr_o", "isvar": True, "width": 1},
                    {"name": "data_o", "isvar": True, "width": 8},
                ],
            },
            {
                "name": "mii_i",
                "signals": [
                    {"name": "rx_clk_i", "width": 1},
                    {"name": "rx_dv_i", "width": 1},
                    {"name": "rx_data_i", "width": 4},
                ],
            },
        ],
        "subblocks": [],
    }
    return attributes_dict
```

### The Hand-Written `.v` Template

Place the `.v` file in `setup_dir/hardware/src/<module_name>.v`. Use
`` `include `` directives to pull in auto-generated snippets:

```verilog
`timescale 1ns / 1ps

module my_module (
    // Ports declared by setup()
    `include "my_module_io.vs"
);

    // Wires declared by setup()
    `include "my_module_wires.vs"

    // Your custom Verilog logic here
    always @(posedge clk_i or posedge arst_i) begin
        if (arst_i)
            count <= 0;
        else if (cke_i)
            count <= count + 1;
    end

    // Sub-block instantiations
    `include "my_module_subblocks.vs"

endmodule
```

### Available `.vs` Include Files

| File | Content |
|------|---------|
| `<name>_io.vs` | Port declarations |
| `<name>_wires.vs` | Internal wire declarations |
| `<name>_params.vs` | Parameter declarations |
| `<name>_subblocks.vs` | Sub-module instantiations |
| `<name>_comb.vs` | Combinational logic (from `iob_comb`) |
| `<name>_fsm.vs` | FSM logic (from `iob_fsm`) |
| `<name>_snippets.vs` | Raw Verilog snippets |

### Post-Processing

When the top module runs `post_setup`, the `` `include `` directives are replaced
inline with the `.vs` file contents, and the `.vs` files are deleted. This happens
automatically during a real py2hwsw build.

---

## 11. Step-by-Step Conversion Walkthrough

Given a Verilog module, convert it to py2hwsw as follows:

### Step 1: Identify Ports

Parse the Verilog port list and note direction, width, and name:

```verilog
module my_module (
    input         clk_i,
    input         arst_i,
    input  [7:0]  data_i,
    output [7:0]  data_o,
    output        valid_o,
    input         ready_i
);
```

### Step 2: Group Signals into Ports

Group related signals into logical ports. Determine the port name suffix:

| Verilog | py2hwsw port name |
|---------|-------------------|
| `input clk_i` | Part of `clk_en_rst_s` (use `iob_clk` interface) |
| `input arst_i` | Part of `clk_en_rst_s` |
| `input [7:0] data_i` | `data_i` (suffix `_i` = input) |
| `output [7:0] data_o` | `data_o` (suffix `_o` = output, `isvar: True` for reg) |
| `output valid_o` | `valid_o` (suffix `_o`, `isvar: True`) |
| `input ready_i` | `ready_i` (suffix `_i`) |

### Step 3: Declare Confs

Identify Verilog parameters and map to `confs`:

```verilog
parameter DATA_W = 32;
```

becomes:

```python
{"name": "DATA_W", "type": "P", "val": "32", "min": "NA", "max": "NA", "descr": "..."}
```

### Step 4: Declare Internal Wires

Identify internal `wire`/`reg` declarations and map to `wires`:

```verilog
wire [31:0] counter;
reg  [7:0]  buffer;
```

becomes:

```python
"wires": [
    {"name": "counter", "signals": [{"name": "counter", "width": 32}]},
    {"name": "buffer", "signals": [{"name": "buffer", "width": 8, "isvar": True}]},
],
```

### Step 5: Translate Logic to Snippets

Convert `always`/`assign` blocks to snippet strings. Use conf names
(`DATA_W`) instead of literal values:

```verilog
// Verilog
always @(posedge clk_i or posedge arst_i) begin
    if (arst_i)
        counter <= 0;
    else if (cke_i)
        counter <= counter + 1;
end
assign data_o = buffer[DATA_W-1:0];
```

becomes:

```python
"snippets": [{
    "verilog_code": """
    always @(posedge clk_i or posedge arst_i) begin
        if (arst_i)
            counter <= 0;
        else if (cke_i)
            counter <= counter + 1;
    end
    assign data_o = buffer[DATA_W-1:0];
"""
}],
```

### Step 6: Identify Sub-Modules

Find instantiated modules and create `subblocks` entries:

```verilog
iob_reg #(.DATA_W(8)) buf_reg (
    .clk_i(clk_i),
    .data_i(data_i),
    .data_o(buffer)
);
```

becomes:

```python
"subblocks": [{
    "core": "iob_reg",
    "instance_name": "buf_reg",
    "parameters": {"DATA_W": 8},
    "connect": {
        "clk_en_rst_s": "clk_en_rst_s",
        "data_i": "data_i",
        "data_o": "buffer",
    },
}],
```

### Step 7: Decide `generate_hw`

- Simple logic, few always blocks -> `generate_hw: True` + snippets
- Complex FSM, pipeline, hand-optimized logic -> `generate_hw: False` + hand-written `.v`

---

## 12. Common Pitfalls

### Port Name Must Have Direction Suffix

```
ValueError: Port name 'my_signal' does not end with a valid direction suffix!
```

Fix: Rename to `my_signal_i`, `my_signal_o`, or `my_signal_io`.

### Signal Direction Must Match Port Direction

```
ValueError: Signal direction 'input' does not match port name 'my_signal_o'
```

An `_o` port cannot contain input signals. Use `_io` for mixed direction, or
split into separate ports.

### Signal Count Must Match in `connect_external`

```
ValueError: Port 'tx_io' has 4 signals but wire 'tx_bus' has 3 signals!
```

The wire must have the same number of signals as the port. Signal matching
happens by index when interfaces are not used.

### `width` Belongs on Signals, Not Wires

```python
# WRONG - raises "Invalid wire attribute 'width'":
{"name": "my_wire", "width": 8, "signals": [{"name": "my_signal"}]}

# CORRECT:
{"name": "my_wire", "signals": [{"name": "my_signal", "width": 8}]}
```

The `width` attribute goes on individual `iob_signal` dicts inside `signals`,
not on the `iob_wire` dict itself.

### `isvar` for Registered Outputs

If an output is driven by an `always` block (not an `assign`), you must set
`"isvar": True` on the signal. Otherwise py2hwsw generates `wire` instead of
`reg`, causing a Verilog compilation error.

### `control_if_m` Is Auto-Connected

When using `iob_csrs`, the `control_if_m` port is automatically connected to
the parent's CSR bus. Do not manually list it in `connect`.

### Unused Ports Connected to `"z"`

If a subblock has output ports you don't need, connect them to the string `"z"`
to leave them unconnected:

```python
"connect": {
    "w_level_o": "z",   # Leave FIFO level output unconnected
}
```

### `clk_en_rst_s` Is Required

Most subblocks expect a `clk_en_rst_s` port connection. Always include it
in your `connect` dict unless the subblock is purely combinational.

---

## 13. Reference Files

### py2hwsw Core Scripts

| File | Purpose |
|------|---------|
| `scripts/iob_core.py` | Main core class, `get_core_obj()`, `generate_build_dir()` |
| `scripts/iob_module.py` | Module descriptor (ports, wires, snippets, subblocks) |
| `scripts/iob_instance.py` | Instance descriptor (portmaps, parameters) |
| `scripts/iob_port.py` | Port definition with direction enforcement |
| `scripts/iob_wire.py` | Wire definition and deduplication |
| `scripts/iob_signal.py` | Atomic signal (name, width, direction, isvar) |
| `scripts/iob_portmap.py` | Port-to-wire connection logic |
| `scripts/iob_conf.py` | Configuration parameters (P/M/C/D) |
| `scripts/interfaces.py` | Standard interface definitions (iob_clk, iob, AXI, memory, etc.) |
| `scripts/verilog_gen.py` | Verilog file generation and `replace_includes()` |
| `scripts/io_gen.py` | Port `.vs` snippet generation |
| `scripts/wire_gen.py` | Wire `.vs` snippet generation |
| `scripts/block_gen.py` | Subblock instantiation `.vs` generation |
| `scripts/snippet_gen.py` | Snippet `.vs` generation |

### Example Modules (by complexity)

| Module | Path | Mode | Demonstrates |
|--------|------|------|--------------|
| `iob_reg` | `lib/hardware/registers/iob_reg/` | `True` | Minimal register, dynamic snippets |
| `iob_gpio` | `lib/peripherals/iob_gpio/` | `True` | Dynamic ports, CSRs, generate |
| `iob_timer` | `lib/peripherals/iob_timer/` | `True` | CSRs with R/W regs, subblocks |
| `iob_uart` | `lib/peripherals/iob_uart/` | `True` | CLI-style syntax, sw_modules |
| `iob_eth` | `lib/iob_system/submodules/iob_eth/` | `True` | Complex SoC peripheral, AXI, FIFOs, hand-written sub-templates |
| `iob_eth_tx` | `.../iob_eth/hardware/modules/iob_eth_tx/` | `False` | Hand-written template with `.vs` includes |
| `iob_eth_rx` | `.../iob_eth/hardware/modules/iob_eth_rx/` | `False` | Hand-written template, `_io` port |
| `iob_eth_dt` | `.../iob_eth/hardware/modules/iob_eth_dt/` | `False` | Hand-written template, multi-interface |
| `iob_eth_logic` | `.../iob_eth/hardware/modules/iob_eth_logic/` | `False` | Hand-written template with snippets |
