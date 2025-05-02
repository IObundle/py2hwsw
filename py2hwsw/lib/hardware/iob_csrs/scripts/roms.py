# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from csr_classes import fail_with_msg


def find_and_update_rom_csrs(csrs_dict, attributes_dict):
    """Given a dictionary of CSRs, find the ROM CSRs group and update the dictionary
    accordingly.
    User should provide a CSR of type "ROM". This CSR will be replaced by rom_csrs.
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add rom instance, wires and ports.
    """
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            if csr.get("type", "") == "ROM":
                csr_ref = csr
                break

        if not csr_ref:
            continue

        if "W" in csr_ref["mode"]:
            fail_with_msg(f"Unsupported mode '{csr_ref['mode']}' for ROM.", ValueError)

        # Replace original csr with "NOAUTO" type
        csr_ref["type"] = "NOAUTO"
        # Don't generate standard ports for this CSR.
        # It will be internal to the CSRs module, and have a custom port generated later.
        csr_ref["internal_use"] = True

        create_rom_instance(attributes_dict, csr_ref)


def create_rom_instance(attributes_dict, csr_ref):
    """Add ROM instance, wires and ports to given attributes_dict, based on rom description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add rom instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with rom information.
    """
    rom_name = csr_ref["name"]
    rom_addr_w = csr_ref["log2n_items"]

    #
    # ROM Ports
    #
    attributes_dict["ports"].append(
        # Create standard external memory port for ROM with if_gen.py
        {
            "name": f"{rom_name}_bus_m",
            "descr": f"External {rom_name} ROM signals.",
            "signals": {
                "type": "rom_sp",
                "prefix": f"{rom_name}_",
                "ADDR_W": rom_addr_w,
                "DATA_W": "DATA_W",
            },
        }
    )
    #
    # ROM Wires
    #
    attributes_dict["wires"] += [
        {
            "name": f"{rom_name}_rvalid_data_i",
            "descr": "Register input",
            "signals": [
                {"name": f"{rom_name}_ren"},
            ],
        },
        {
            "name": f"{rom_name}_rvalid_data_o",
            "descr": "Register output",
            "signals": [
                {"name": f"{rom_name}_rvalid"},
            ],
        },
    ]
    #
    # Blocks
    #
    attributes_dict["subblocks"].append(
        {
            "core_name": "iob_reg",
            "instance_name": f"{rom_name}_rvalid_r",
            "instance_description": f"{rom_name} rvalid register",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": "1'b0",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "data_i": f"{rom_name}_rvalid_data_i",
                "data_o": f"{rom_name}_rvalid_data_o",
            },
        },
    )
    #
    # Snippets
    #
    attributes_dict["snippets"].append(
        {
            "verilog_code": f"""
// Connect ROM to external memory signals
   assign {rom_name}_clk_o = clk_i;
   assign {rom_name}_en_o   = {rom_name}_ren;
   assign {rom_name}_addr_o = {rom_name}_raddr;
   assign {rom_name}_rdata   = {rom_name}_r_data_i;
   assign {rom_name}_ready  = 1'b1;  // ROM is always ready
""",
        }
    )
