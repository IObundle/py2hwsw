# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from csr_classes import fail_with_msg


def find_and_update_autoclear_csrs(csrs_dict, attributes_dict):
    """Given a dictionary of CSRs, find the AUTOCLEAR CSR and update the dictionar accordingly.
    User should provide a CSR of type "AUTOCLEAR".
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add autoclear instance, wires and ports.
    """
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            if csr.get("type", "") == "NOAUTO" and csr.get("autoclear", False):
                csr_ref = csr
                break

        if not csr_ref:
            continue

        # Don't generate standard ports for this CSR.
        # It will be internal to the CSRs module, and have a custom port generated later.
        csr_ref["internal_use"] = True
        csr_ref["volatile"] = True

        # Create field if it doesn't exist
        if not csr_ref.get("fields", []):
            csr_ref["fields"] = [
                {"name": csr_ref["name"], "base_bit": 0, "width": csr_ref["n_bits"]}
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
    port_suffix = "_"
    port_signals = []
    snippet = ""
    if "R" in mode:
        port_suffix += "i"
        port_signals += [
            {"name": f"{name}_rdata_i", "width": width},
            # TODO: other noauto wires
        ]
        snippet += f"""
   assign {name}_rdata = {name}_rdata_i;
"""
    if "W" in mode:
        port_suffix += "o"
        port_signals += [
            {"name": f"{name}_wdata_o", "width": width},
            # TODO: other noauto wires
        ]
        snippet += f"""
   assign {name}_wdata = {name}_wdata_o;
"""

    #
    # Ports
    #
    attributes_dict["ports"].append(
        # Create normal port, as if it were of type "REG"
        {
            "name": f"{name}{port_suffix}",
            "descr": descr,
            "signals": port_signals,
        }
    )
    #
    # Snippets
    #
    attributes_dict["snippets"].append({"verilog_code": snippet})
