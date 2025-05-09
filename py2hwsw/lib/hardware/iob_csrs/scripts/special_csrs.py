# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from csr_classes import fail_with_msg


def find_and_update_autoclear_csrs(csrs_dict, attributes_dict):
    """Auto-clear CSR: Same signals as NOAUTO, but already includes internal register that gets cleared automatically on ready/rready.
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add autoclear instance, wires and ports.
    """
    # Autoclear register for NOAUTO. If cpu writes 1 to it, it will be autocleared when core returns ready (reads value from it). IPxact should have an attribute for this.
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            if csr.get("type", "") == "NOAUTO" and csr.pop("autoclear", False):
                csr_ref = csr

                # Don't generate standard ports for this CSR.
                # It will be internal to the CSRs module, and have a custom port generated later.
                csr_ref["internal_use"] = True
                csr_ref["volatile"] = True

                # Create field if it doesn't exist
                if not csr_ref.get("fields", []):
                    csr_ref["fields"] = [
                        {
                            "name": csr_ref["name"],
                            "mode": csr_ref["mode"],
                            "base_bit": 0,
                            "width": csr_ref["n_bits"],
                            "volatile": True,
                            "rst_val": 0,
                        }
                    ]
                # Set correct read/write action for field of autoclear csrs
                if "W" in csr_ref["mode"]:
                    csr_ref["fields"][0]["write_action"] = "clear"
                if "R" in csr_ref["mode"]:
                    csr_ref["fields"][0]["read_action"] = "clear"

                create_autoclear_instance(attributes_dict, csr_ref)


def create_autoclear_instance(attributes_dict, csr_ref):
    """Add AUTOCLEAR instance, wires and ports to given attributes_dict, based on autoclear description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add autoclear instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with autoclear information.
    """
    name = csr_ref["name"]
    descr = csr_ref["descr"]
    mode = csr_ref["mode"]
    width = csr_ref["n_bits"]
    port_signals = []
    snippet = ""
    if "R" in mode:
        port_signals += [
            {"name": f"{name}_valid_o", "width": 1},
            {"name": f"{name}_addr_o", "width": 1},
            {"name": f"{name}_rvalid_i", "width": 1},
            {"name": f"{name}_rdata_i", "width": width},
            {"name": f"{name}_ready_i", "width": 1},
            {"name": f"{name}_rready_o", "width": 1},
        ]
        snippet += f"""
   // Should these signals be registered?
   assign {name}_valid_o = {name}_valid;
   assign {name}_addr_o = {name}_addr;
   // assign {name}_rdata = {name}_rdata_i;
   assign {name}_ready = {name}_ready_i;

   // Always ready to receive new value from core
   assign {name}_rready_o = 1'b1;
   // Always ready to send value value to CPU
   assign {name}_rvalid = 1'b1;

   // Set rdata from core
   assign {name}_en = {name}_rvalid_i;
   // Auto-clear when CPU reads
   assign {name}_rst = {name}_rready;
"""
    if "W" in mode:
        port_signals += [
            {"name": f"{name}_valid_o", "width": 1},
            {"name": f"{name}_addr_o", "width": 1},
            {"name": f"{name}_wdata_o", "width": width},
            {"name": f"{name}_wstrb_o", "width": f"{width}/8"},
            {"name": f"{name}_ready_i", "width": 1},
        ]
        snippet += f"""
   // Should these signals be registered?
   assign {name}_valid_o = {name}_valid;
   assign {name}_addr_o = {name}_addr;
   // assign {name}_wdata_o = {name}_wdata;
   assign {name}_wstrb_o = {name}_wstrb;

   // Always ready to receive new value from CPU
   assign {name}_ready = 1'b1;

   // Set wdata from CPU
   assign {name}_en = {name}_valid & |{name}_wstrb;
   // Auto-clear when core reads
   assign {name}_rst = {name}_ready_i;
"""

    #
    # Ports
    #
    attributes_dict["ports"].append(
        # Create normal port, as if it were of type "NOAUTO"
        {
            "name": f"{name}_io",
            "descr": descr,
            "signals": port_signals,
        }
    )
    #
    # Wires
    #
    attributes_dict["wires"] += [
        {
            "name": f"{name}_en_rst",
            "descr": "",
            "signals": [
                {"name": f"{name}_en", "width": 1},
                {"name": f"{name}_rst", "width": 1},
            ],
        },
    ]
    if "R" in mode:
        attributes_dict["wires"] += [
            {
                "name": f"{name}_data_i",
                "descr": "",
                "signals": [
                    {"name": f"{name}_rdata_i"},  # From core
                ],
            },
            {
                "name": f"{name}_data_o",
                "descr": "",
                "signals": [
                    {"name": f"{name}_rdata"},  # To CPU
                ],
            },
        ]
    if "W" in mode:
        attributes_dict["wires"] += [
            {
                "name": f"{name}_data_i",
                "descr": "",
                "signals": [
                    {"name": f"{name}_wdata"},  # From CPU
                ],
            },
            {
                "name": f"{name}_data_o",
                "descr": "",
                "signals": [
                    {"name": f"{name}_wdata_o"},  # To core
                ],
            },
        ]
    #
    # Subblocks
    #
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_reg",
            "instance_name": f"iob_reg_{name}",
            "instance_description": f"{name} autoclear csr",
            "parameters": {
                "DATA_W": width,
                "RST_VAL": f"{{{width}{{1'b0}}}}",
            },
            "port_params": {"clk_en_rst_s": "c_a_r_e"},
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        f"en_i:{name}_en",
                        f"rst_i:{name}_rst",
                    ],
                ),
                "data_i": f"{name}_data_i",
                "data_o": f"{name}_data_o",
            },
        },
    ]
    #
    # Snippets
    #
    attributes_dict["snippets"].append({"verilog_code": snippet})
