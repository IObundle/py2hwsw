# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

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
        ("awprot", "output", "PROT_W", 3),
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
        ("arprot", "output", "PROT_W", 3),
        ("arvalid", "output", 1),
        ("arready", "input", 1),
        ("rdata", "input", "DATA_W", 32),
        ("rresp", "input", "RESP_W", 2),
        ("rvalid", "input", 1),
        ("rready", "output", 1),
    ],
    "axi": [
        ("awaddr", "output", "ADDR_W", 32),
        ("awprot", "output", "PROT_W", 3),
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
        ("arprot", "output", "PROT_W", 3),
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
    assert MEMORY_ZONES, """
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
    for signal in interfaces[INTERFACE]:
        name = signal[0]
        width = signal[2]
        default_width = signal[2] if type(width) is int else signal[3]

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
        # Set parameters for if_gen generation of the interface
        interface_parameters[width] = width

    #
    # Connect interfaces
    #
    for signal in interfaces[INTERFACE]:
        name = signal[0]
        # Skip address signal
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
if (signal_name_i >= 'h{zone_start:x} && signal_name_i <= 'h{zone_end:x}) begin
         signal_name_reg = signal_name_i + 'h{offset:x}; // signal_name_i is in the range 0x{zone_start:x} to 0x{zone_end:x}
      end else \
"""

    translation_snippet_body += """\
begin
         signal_name_reg = signal_name_i; // Default case
      end
"""

    for signal in interfaces[INTERFACE]:
        name = INTERFACE + "_" + signal[0]
        if "addr" not in name:
            continue
        verilog_snippet += f"""
   // Translate {name} signal
   reg [ADDR_W-1:0] {name}_reg;
   assign {name}_o = {name}_reg;
   always @(*) begin
{translation_snippet_body.replace("signal_name", name)}
   end
"""

    #
    # Core attributes dictionary
    #
    attributes_dict = {
        "name": NAME,
        "generate_hw": True,
        "version": "0.1",
        "confs": verilog_parameters,
        "ports": [
            {
                "name": "slave_s",
                "descr": "Slave interface (connects to master)",
                "signals": {
                    "type": INTERFACE,
                    **interface_parameters,
                },
            },
            {
                "name": "master_m",
                "descr": "Master interface (connects to slave)",
                "signals": {
                    "type": INTERFACE,
                    **interface_parameters,
                },
            },
        ],
        "snippets": [{"verilog_code": verilog_snippet}],
    }

    return attributes_dict
