# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os

interfaces = {
    "iob": [
        ("valid", "output", 1),
        ("addr", "output", "ADDR_W", 32),
        ("wdata", "output", "DATA_W", 32),
        ("wstrb", "output", "DATA_W / 8", 4),
        ("rvalid", "input", 1),
        ("rdata", "input", "DATA_W", 32),
        ("ready", "input", 1),
    ],
    "axil": [
        ("awaddr", "output", "ADDR_W", 32),
        # ("awprot", "output", "PROT_W", 3),
        ("awvalid", "output", 1),
        ("awready", "input", 1),
        ("wdata", "output", "DATA_W", 32),
        ("wstrb", "output", "DATA_W / 8", 4),
        ("wvalid", "output", 1),
        ("wready", "input", 1),
        ("bresp", "input", "RESP_W", 2),
        ("bvalid", "input", 1),
        ("bready", "output", 1),
        ("araddr", "output", "ADDR_W", 32),
        # ("arprot", "output", "PROT_W", 3),
        ("arvalid", "output", 1),
        ("arready", "input", 1),
        ("rdata", "input", "DATA_W", 32),
        ("rresp", "input", "RESP_W", 2),
        ("rvalid", "input", 1),
        ("rready", "output", 1),
    ],
    "axi": [
        ("awaddr", "output", "ADDR_W", 32),
        # ("awprot", "output", "PROT_W", 3),
        ("awvalid", "output", 1),
        ("awready", "input", 1),
        ("wdata", "output", "DATA_W", 32),
        ("wstrb", "output", "DATA_W / 8", 4),
        ("wvalid", "output", 1),
        ("wready", "input", 1),
        ("bresp", "input", "RESP_W", 2),
        ("bvalid", "input", 1),
        ("bready", "output", 1),
        ("araddr", "output", "ADDR_W", 32),
        # ("arprot", "output", "PROT_W", 3),
        ("arvalid", "output", 1),
        ("arready", "input", 1),
        ("rdata", "input", "DATA_W", 32),
        ("rresp", "input", "RESP_W", 2),
        ("rvalid", "input", 1),
        ("rready", "output", 1),
        ("awid", "output", "ID_W", 1),
        ("awlen", "output", "LEN_W", 8),
        ("awsize", "output", "SIZE_W", 3),
        ("awburst", "output", "BURST_W", 2),
        ("awlock", "output", "LOCK_W", 2),
        ("awcache", "output", "CACHE_W", 4),
        ("awqos", "output", "QOS_W", 4),
        ("wlast", "output", 1),
        ("bid", "input", "ID_W", 1),
        ("arid", "output", "ID_W", 1),
        ("arlen", "output", "LEN_W", 8),
        ("arsize", "output", "SIZE_W", 3),
        ("arburst", "output", "BURST_W", 2),
        ("arlock", "output", "LOCK_W", 2),
        ("arcache", "output", "CACHE_W", 4),
        ("arqos", "output", "QOS_W", 4),
        ("rid", "input", "ID_W", 1),
        ("rlast", "input", 1),
    ],
}


def setup(py_params_dict):
    """Core to translate addresses to access configurable memory zones.
    Use verilog parameters to define widths of each bus.
    :param str interface: Type of interface for buses.
    :param str name: Name of the generated verilog core.
    :param list memory_zones: List of tuples describing each memory zone and offset to add for translation.
    """
    INTERFACE = py_params_dict.get("interface", "axi")
    NAME = py_params_dict.get("name", f"iob_{INTERFACE}_address_translator")
    MEMORY_ZONES = py_params_dict.get(
        "memory_zones",
        [
            # (Initial zone address, Last zone address (inclusive), Offset to add (for translation))
        ],
    )
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        MEMORY_ZONES = [
            # (Initial zone address, Last zone address (inclusive), Offset to add (for translation))
            (0x0, 0xFFFF, 0xFF),  # Example zone
        ]
    assert MEMORY_ZONES, f"""
{os.path.basename(__file__)} error:
No memory zones defined for address translation!
Memory zones must be configured via the 'memory_zones' python parameter.
Memory zone tuple syntax: (Initial zone address, Last zone address (inclusive), Offset to add (for translation))
"""

    verilog_snippet = ""
    parameter_names = []
    verilog_parameters = []
    interface_parameters = {}

    #
    # Create verilog parameters
    #
    for wire in interfaces[INTERFACE]:
        name = wire[0]
        width = wire[2]
        default_width = wire[2] if type(width) is int else wire[3]

        # Only create verilog parameters for strings that represent widths
        if type(width) is int or not width.endswith("_W"):
            continue

        # Don't create a duplicate parameters
        if width in parameter_names:
            continue
        parameter_names.append(width)

        # Set verilog parameters
        verilog_parameters += [
            {
                "name": width,
                "type": "P",
                "val": default_width,
                "min": "1",
                "max": "32",
                "descr": f"{width[:-2]} bus width",
            },
        ]
        # Set parameters for generation of the interface
        interface_parameters[width] = width

    #
    # Connect interfaces
    #
    for wire in interfaces[INTERFACE]:
        name = wire[0]
        # Skip address wire
        if "addr" in name:
            continue
        # Connect both interfaces
        verilog_snippet += f"""\
   assign {INTERFACE}_{name}_o = {INTERFACE}_{name}_i;
"""

    #
    # Translate addresses to configurable memory zones
    #
    translation_snippet_body = "      "
    for zone in MEMORY_ZONES:
        zone_start, zone_end, offset = zone
        translation_snippet_body += f"""\
if (wire_name_i >= 'h{zone_start:x} && wire_name_i <= 'h{zone_end:x}) begin
         wire_name_reg = wire_name_i + 'h{offset:x}; // wire_name_i is in the range 0x{zone_start:x} to 0x{zone_end:x}
      end else \
"""

    translation_snippet_body += """\
begin
         wire_name_reg = wire_name_i; // Default case
      end
"""

    for wire in interfaces[INTERFACE]:
        name = INTERFACE + "_" + wire[0]
        if "addr" not in name:
            continue
        verilog_snippet += f"""
   // Translate {name} wire
   reg [ADDR_W-1:0] {name}_reg;
   assign {name}_o = {name}_reg;
   always @(*) begin
{translation_snippet_body.replace("wire_name", name)}
   end
"""

    #
    # Core attributes dictionary
    #
    attributes_dict = {
        "name": NAME,
        "generate_hw": True,
        "confs": verilog_parameters,
        "ports": [
            {
                "name": "subordinate_s",
                "descr": "Subordinate interface (connects to manager)",
                "wires": {
                    "type": INTERFACE,
                    **interface_parameters,
                },
            },
            {
                "name": "manager_m",
                "descr": "Manager interface (connects to subordinate)",
                "wires": {
                    "type": INTERFACE,
                    **interface_parameters,
                },
            },
        ],
        "snippets": [{"verilog_code": verilog_snippet}],
    }

    return attributes_dict
