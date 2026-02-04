# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def csr_type(n_bits):
    type_dict = {8: "uint8_t", 16: "uint16_t", 32: "uint32_t"}
    try:
        n_bits = int(n_bits)

        for type_try in type_dict:
            if n_bits <= type_try:
                return type_dict[type_try]
    except:
        pass

    # If its not an integer, or its too big, default to 32
    # NOTE: Ideally, we should try to evaluate verilog parameters contained in n_bits.
    #       The best solution would be to obatin the evaluated value from the iob_csrs module directly.
    #       But currently py2hwsw does not have an easy mechanism to do that.
    return "uint32_t"
