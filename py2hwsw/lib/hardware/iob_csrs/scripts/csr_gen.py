#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
# csr_gen.py: build Verilog control and status registers and software bare-metal driver
#
import copy
import sys
import os
from math import ceil, log, log2
from latex import write_table
import iob_colors
import re
from csr_classes import iob_csr, iob_csr_group


def convert_int(value):
    """Try to convert given str (or int) to int. Otherwise return as is."""
    if type(value) is int:
        return value

    try:
        return int(value)
    except ValueError:
        return value


def clog2(val):
    """Used by eval_param_expression"""
    return ceil(log2(val))


def eval_param_expression(param_expression, params_dict):
    """Given a mathematical string with parameters, replace every parameter by
    its numeric value and tries to evaluate the string.
    param_expression: string defining a math expression that may contain parameters
    params_dict: dictionary of parameters, where the key is the parameter name and the value is its value
    """
    if type(param_expression) is int:
        return param_expression
    else:
        original_expression = param_expression
        # Split string to separate parameters/macros from the rest
        split_expression = re.split(r"([^\w_])", param_expression)
        # Replace each parameter, following the reverse order of parameter list.
        # The reversed order allows replacing parameters recursively (parameters may
        # have values with parameters that came before).
        for param_name, param_value in reversed(params_dict.items()):
            # Replace every instance of this parameter by its value
            for idx, word in enumerate(split_expression):
                if word == param_name:
                    # Replace parameter/macro by its value
                    split_expression[idx] = str(param_value)
                    # Remove '`' char if it was a macro
                    if idx > 0 and split_expression[idx - 1] == "`":
                        split_expression[idx - 1] = ""
                    # resplit the string in case the parameter value contains other parameters
                    split_expression = re.split(r"([^\w_])", "".join(split_expression))
        # Join back the string
        param_expression = "".join(split_expression)
        # Evaluate $clog2 expressions
        param_expression = param_expression.replace("$clog2", "clog2")
        # Evaluate IOB_MAX and IOB_MIN expressions
        param_expression = param_expression.replace("iob_max", "max")
        param_expression = param_expression.replace("iob_min", "min")

        # Try to calculate string as it should only contain numeric values
        try:
            return eval(param_expression)
        except:
            sys.exit(
                f"Error: string '{original_expression}' evaluated to '{param_expression}' is not a numeric expression."
            )


def eval_param_expression_from_config(param_expression, confs, param_attribute):
    """Given a mathematical string with parameters, replace every parameter by its
    numeric value and tries to evaluate the string. The parameters are taken from the
    confs dictionary.
    param_expression: string defining a math expression that may contain parameters.
    confs: list of dictionaries, each of which describes a parameter and has attributes:
           'name', 'val' and 'max'.
    param_attribute: name of the attribute in the paramater that contains the value to
           replace in string given. Attribute names are: 'val', 'min, or 'max'.
    """
    # Create parameter dictionary with correct values to be replaced in string
    params_dict = {}
    for param in confs:
        params_dict[param["name"]] = param.get(param_attribute, None)

    return eval_param_expression(param_expression, params_dict)


class csr_gen:
    """Use a class for the entire module, as it may be imported multiple times, but
    must have instance variables (multiple cores/submodules have different registers)
    """

    def __init__(self):
        self.cpu_n_bytes = 4
        self.core_addr_w = None
        self.config = None

    @staticmethod
    def boffset(n, n_bytes):
        return 8 * (n % n_bytes)

    @staticmethod
    def bfloor(n, log2base):
        base = int(2**log2base)
        if n % base == 0:
            return n
        return base * int(n / base)

    @staticmethod
    def verilog_max(a, b):
        if a == b:
            return a
        try:
            # Assume a and b are int
            a = int(a)
            b = int(b)
            return a if a > b else b
        except ValueError:
            # a or b is a string
            return f"(({a} > {b}) ? {a} : {b})"

    def get_reg_table(self, csrs, rw_overlap, autoaddr, doc_conf):
        # Create doc table
        doc_table = []
        for csr_group in csrs:
            filtered_csr_group = copy.copy(csr_group)
            filtered_csr_group.regs = []
            for reg in csr_group.regs:
                # exclude registers without matching doc_conf
                # registers without 'doc_conf_list' are always included
                if reg.doc_conf_list and doc_conf not in reg.doc_conf_list:
                    continue
                filtered_csr_group.regs.append(reg)
            if filtered_csr_group.regs:
                doc_table.append(filtered_csr_group)

        # List all registers from doc_table
        reg_table = []
        for csr_group in doc_table:
            reg_table += csr_group.regs

        return self.compute_addr(reg_table, rw_overlap, autoaddr), copy.deepcopy(
            doc_table
        )

    def bceil(self, n, log2base):
        base = int(2**log2base)
        n = eval_param_expression_from_config(n, self.config, "max")
        # print(f"{n} of {type(n)} and {base}")
        if n % base == 0:
            return n
        else:
            return int(base * ceil(n / base))

    # Calculate numeric value of addr_w, replacing params by their max value
    def calc_addr_w(self, log2n_items, n_bytes):
        return int(
            ceil(
                eval_param_expression_from_config(log2n_items, self.config, "max")
                + log(n_bytes, 2)
            )
        )

    # Generate symbolic expression string to caluclate addr_w in verilog
    @staticmethod
    def calc_verilog_addr_w(log2n_items, n_bytes):
        n_bytes = int(n_bytes)
        try:
            # Assume log2n_items is int
            log2n_items = int(log2n_items)
            return log2n_items + ceil(log(n_bytes, 2))
        except ValueError:
            # log2n_items is a string
            if n_bytes == 1:
                return log2n_items
            else:
                return f"{log2n_items}+{ceil(log(n_bytes, 2))}"

    def gen_wr_reg(self, row):
        wires = []
        name = row.name
        rst_val = int(row.rst_val)
        n_bits = row.n_bits
        log2n_items = convert_int(row.log2n_items)
        n_bytes = self.bceil(n_bits, 3) / 8
        if n_bytes == 3:
            n_bytes = 4
        addr = row.addr
        addr_w = self.calc_verilog_addr_w(log2n_items, n_bytes)
        auto = row.type != "NOAUTO"
        suffix = "" if row.internal_use else "_o"
        suffix_i = "" if row.internal_use else "_i"
        optional_comment = row.optional_comment

        lines = ""
        lines += f"\n\n//NAME: {name};\n//MODE: {row.mode}; WIDTH: {n_bits}; RST_VAL: {rst_val}; ADDR: {addr}; SPACE (bytes): {2**self.calc_addr_w(log2n_items, n_bytes)} (max); TYPE: {row.type}. {optional_comment}\n\n"

        # compute wdata with only the needed bits
        wires.append(
            {
                "name": f"{name}_wdata",
                "descr": "",
                "signals": [
                    {"name": f"{name}_wdata", "width": self.verilog_max(n_bits, 1)},
                ],
            },
        )
        lines += f"    assign {name}_wdata = internal_iob_wdata[{self.boffset(addr,self.cpu_n_bytes)}+:{self.verilog_max(n_bits,1)}];\n"

        if auto:  # generate register
            # signal to indicate if the register is addressed
            lines += f"    wire {name}_addressed_w;\n"

            # test if addr and addr_w are int and substitute with their values
            if isinstance(addr, int) and isinstance(addr_w, int):
                lines += f"    assign {name}_addressed_w = (wstrb_addr >= ({addr})) && (wstrb_addr < {addr+2**addr_w});\n"
            else:
                lines += f"    assign {name}_addressed_w = (wstrb_addr >= ({addr})) && (wstrb_addr < ({addr}+(2**({addr_w}))));\n"

            n_items = 2 ** eval_param_expression_from_config(
                log2n_items, self.config, "max"
            )
            assert (
                n_items == 1
            ), "Regfiles (n_items > 1) cannot be generated with auto. This error is a bug, auto regfiles should be handled by previous scripts."
            assert (
                row.asym == 1
            ), f"Currently, REG with log2n_items == 0 do support asymetric interfaces. CSR: {name}"

            # fill remaining bits of reset value with 0s
            if isinstance(n_bits, str):
                if rst_val != 0:
                    # get number of bits needed to represent rst_val
                    rst_n_bits = ceil(log(rst_val + 1, 2))
                    zeros_filling = (
                        "{(" + str(n_bits) + "-" + str(rst_n_bits) + "){1'd0}}"
                    )
                    rst_val_str = (
                        "{"
                        + zeros_filling
                        + ","
                        + str(rst_n_bits)
                        + "'d"
                        + str(rst_val)
                        + "}"
                    )
                else:
                    rst_val_str = "{" + str(n_bits) + "{1'd0}}"
            else:
                rst_val_str = str(n_bits) + "'d" + str(rst_val)
            wires.append(
                {
                    "name": f"{name}_w_valid",
                    "descr": "",
                    "signals": [
                        {"name": f"{name}_w_valid", "width": 1},
                    ],
                },
            )
            lines += f"    assign {name}_w_valid = internal_iob_valid & (write_en & {name}_addressed_w);\n"

            if "R" in row.mode:
                # This is a "RW" CSR. Create logic to mux inputs and assign outputs of reg
                wires += [
                    {
                        "name": f"{name}_reg_en",
                        "descr": "",
                        "signals": [
                            {"name": f"{name}_reg_en", "width": 1},
                        ],
                    },
                    {
                        "name": f"{name}_reg_data",
                        "descr": "",
                        "signals": [
                            {
                                "name": f"{name}_reg_data",
                                "width": self.verilog_max(n_bits, 1),
                            },
                        ],
                    },
                ]

                lines += (
                    f"    assign {name}_rdata = {name}_rdata{suffix};\n"
                    f"    assign {name}_reg_en = {name}_w_valid | (|{name}_wstrb_i);\n"
                    f"    assign {name}_reg_data = {name}_w_valid ? {name}_wdata : {name}_wdata{suffix_i};\n"
                )

            # Create reg
            lines += (
                "    iob_reg_cae #(\n"
                f"      .DATA_W({n_bits}),\n"
                f"      .RST_VAL({rst_val_str})\n"
                f"    ) {name}_datareg_wr (\n"
                "      .clk_i  (clk_i),\n"
                "      .cke_i  (cke_i),\n"
                "      .arst_i (arst_i),\n"
            )
            if "R" in row.mode:  # inputs of "RW" CSR
                lines += (
                    f"      .en_i   ({name}_reg_en),\n"
                    f"      .data_i ({name}_reg_data),\n"
                )
            else:  # inputs of "W" CSR
                lines += (
                    f"      .en_i   ({name}_w_valid),\n"
                    f"      .data_i ({name}_wdata),\n"
                )
            lines += f"      .data_o ({name}_rdata{suffix})\n" "    );\n\n"
        else:  # not auto: compute valid
            # signal to indicate if the register is addressed
            lines += f"    wire {name}_addressed;\n"

            # test if addr and addr_w are int and substitute with their values
            # For non-auto, use normal address
            if isinstance(addr, int) and isinstance(addr_w, int):
                lines += f"    assign {name}_addressed = (internal_iob_addr_stable >= ({addr})) && (internal_iob_addr_stable < {addr+2**addr_w});\n"
            else:
                lines += f"    assign {name}_addressed = (internal_iob_addr_stable >= ({addr})) && (internal_iob_addr_stable < ({addr}+(2**({addr_w}))));\n"

            lines += f"   assign {name}_valid{suffix} = internal_iob_valid & {name}_addressed;\n"
            if type(log2n_items) is not int or log2n_items > 0:
                lines += f"   assign {name}_addr{suffix} = internal_iob_addr_stable - {addr};\n"
            lines += f"   assign {name}_wstrb{suffix} = internal_iob_wstrb;\n"
            if suffix:
                lines += f"    assign {name}_wdata{suffix} = {name}_wdata;\n"

        return lines, wires

    def gen_rd_reg(self, row):
        wires = []
        name = row.name
        rst_val = row.rst_val
        n_bits = row.n_bits
        log2n_items = convert_int(row.log2n_items)
        n_bytes = self.bceil(n_bits, 3) / 8
        if n_bytes == 3:
            n_bytes = 4
        addr = row.addr
        addr_w = self.calc_verilog_addr_w(log2n_items, n_bytes)
        auto = row.type != "NOAUTO"
        suffix = "" if row.internal_use else "_o"
        suffix_i = "" if row.internal_use else "_i"
        optional_comment = row.optional_comment

        lines = ""
        lines += f"\n\n//NAME: {name};\n//MODE: {row.mode}; WIDTH: {n_bits}; RST_VAL: {rst_val}; ADDR: {addr}; SPACE (bytes): {2**self.calc_addr_w(log2n_items,n_bytes)} (max); TYPE: {row.type}. {optional_comment}\n\n"

        if auto:
            # signal to indicate if the register is addressed
            lines += f"    wire {name}_addressed_r;\n"

            # test if addr and addr_w are int and substitute with their values
            # For (auto) REG, use special read strobe based on 'shift_amount'
            if isinstance(addr, int) and isinstance(addr_w, int):
                lines += f"    assign {name}_addressed_r = (internal_iob_addr_stable>>shift_amount >= ({addr}>>shift_amount)) && (internal_iob_addr_stable>>shift_amount < iob_max(1,{addr+2**addr_w}>>shift_amount));\n"
            else:
                lines += f"    assign {name}_addressed_r = (internal_iob_addr_stable>>shift_amount >= ({addr}>>shift_amount)) && (internal_iob_addr_stable>>shift_amount < iob_max(1,({addr}+(2**({addr_w})))>>shift_amount));\n"

            n_items = 2 ** eval_param_expression_from_config(
                log2n_items, self.config, "max"
            )
            assert (
                n_items == 1
            ), "Regfiles (n_items > 1) cannot be generated with auto. This error is a bug, auto regfiles should be handled by previous scripts."
            assert (
                row.asym == 1
            ), f"Currently, REG with log2n_items == 0 do support asymetric interfaces. CSR: {name}"

            # version is not a register, it is an internal constant
            if name == "version":
                return lines, wires

            # fill remaining bits of reset value with 0s
            if isinstance(n_bits, str):
                if rst_val != 0:
                    # get number of bits needed to represent rst_val
                    rst_n_bits = ceil(log(rst_val + 1, 2))
                    zeros_filling = (
                        "{(" + str(n_bits) + "-" + str(rst_n_bits) + "){1'd0}}"
                    )
                    rst_val_str = (
                        "{"
                        + zeros_filling
                        + ","
                        + str(rst_n_bits)
                        + "'d"
                        + str(rst_val)
                        + "}"
                    )
                else:
                    rst_val_str = "{" + str(n_bits) + "{1'd0}}"
            else:
                rst_val_str = str(n_bits) + "'d" + str(rst_val)
            wires += [
                {
                    "name": f"{name}_rdata",
                    "descr": "",
                    "signals": [
                        {"name": f"{name}_rdata", "width": self.verilog_max(n_bits, 1)},
                    ],
                },
            ]

            # Create reg only if this is not a "RW" CSR. For "RW" we reuse CSR created previously.
            if "W" not in row.mode:
                lines += "    iob_reg_ca #(\n"
                lines += f"      .DATA_W({n_bits}),\n"
                lines += f"      .RST_VAL({rst_val_str})\n"
                lines += f"    ) {name}_datareg_rd (\n"
                lines += "      .clk_i  (clk_i),\n"
                lines += "      .cke_i  (cke_i),\n"
                lines += "      .arst_i (arst_i),\n"
                lines += f"      .data_i ({name}_wdata{suffix_i}),\n"
                lines += f"      .data_o ({name}_rdata)\n"
                lines += "    );\n\n"
        else:  # not auto: output read enable
            # If CSR is also "W", then use same valid and addr as generated by "W", otherwise create a new one
            if "W" not in row.mode:
                # signal to indicate if the register is addressed
                lines += f"    wire {name}_addressed;\n"

                # test if addr and addr_w are int and substitute with their values
                # For non-auto, use normal address
                if isinstance(addr, int) and isinstance(addr_w, int):
                    lines += f"    assign {name}_addressed = (internal_iob_addr_stable >= ({addr})) && (internal_iob_addr_stable < {addr+2**addr_w});\n"
                else:
                    lines += f"    assign {name}_addressed = (internal_iob_addr_stable >= ({addr})) && (internal_iob_addr_stable < ({addr}+(2**({addr_w}))));\n"

                # Create new valid and addr signals
                lines += f"   assign {name}_valid{suffix} = internal_iob_valid & {name}_addressed & ~write_en;\n"
                if type(log2n_items) is not int or log2n_items > 0:
                    lines += f"   assign {name}_addr{suffix} = internal_iob_addr_stable - {addr};\n"

            lines += f"    assign {name}_rready{suffix} = internal_iob_rready;\n"

        return lines, wires

    # auxiliar read register case name
    def aux_read_reg_case_name(self, row):
        aux_read_reg_case_name = ""
        if "R" in row.mode:
            addr = row.addr
            n_bits = row.n_bits
            log2n_items = row.log2n_items
            n_bytes = int(self.bceil(n_bits, 3) / 8)
            if n_bytes == 3:
                n_bytes = 4
            addr_w = self.calc_addr_w(log2n_items, n_bytes)
            addr_w_base = max(log(self.cpu_n_bytes, 2), addr_w)
            aux_read_reg_case_name = f"iob_addr_i_{self.bfloor(addr, addr_w_base)}_{self.boffset(addr, self.cpu_n_bytes)}"
        return aux_read_reg_case_name

    # generate wires to connect instance in top module
    def gen_inst_wire(self, table, f):
        for row in table:
            name = row.name
            n_bits = row.n_bits
            auto = row.type != "NOAUTO"

            # version is not a register, it is an internal constant
            if name != "version":
                if "W" in row.mode:
                    if auto:
                        f.write(
                            f"    wire [{self.verilog_max(n_bits,1)}-1:0] {name}_wr;\n"
                        )
                    else:
                        f.write(
                            f"    wire [{self.verilog_max(n_bits,1)}-1:0] {name}_wdata_wr;\n"
                        )
                        f.write(f"    wire {name}_valid_wr;\n")
                        f.write(f"    wire {name}_ready_wr;\n")
                if "R" in row.mode:
                    if auto:
                        f.write(
                            f"    wire [{self.verilog_max(n_bits,1)}-1:0] {name}_rd;\n"
                        )
                    else:
                        f.write(
                            f"""
    wire [{self.verilog_max(n_bits,1)}-1:0] {name}_rdata_rd;
    wire {name}_rvalid_rd;
    wire {name}_valid_rd;
    wire {name}_rready_rd;
    wire {name}_ready_rd;
"""
                        )
        f.write("\n")

    # generate portmap for csrs instance in top module
    def gen_portmap(self, table, f):
        for row in table:
            name = row.name
            auto = row.type != "NOAUTO"

            # version is not a register, it is an internal constant
            if name != "version":
                if "W" in row.mode:
                    if auto:
                        f.write(f"    .{name}_o({name}_wr),\n")
                    else:
                        f.write(f"    .{name}_wdata_o({name}_wdata_wr),\n")
                        f.write(f"    .{name}_valid_o({name}_valid_wr),\n")
                        f.write(f"    .{name}_ready_i({name}_ready_wr),\n")
                if "R" in row.mode:
                    if auto:
                        f.write(f"    .{name}_i({name}_rd),\n")
                    else:
                        f.write(
                            f"""
    .{name}_rdata_i({name}_rdata_rd),
    .{name}_rvalid_i({name}_rvalid_rd),
    .{name}_rready_o({name}_rready_rd),
    .{name}_ren_o({name}_valid_rd),
    .{name}_ready_i({name}_ready_rd),
"""
                        )

    def gen_ports_wires(self, table):
        """Generate ports and internal wires for csrs instance."""
        ports = []
        wires = []
        snippet = ""
        for row in table:
            name = row.name
            auto = row.type != "NOAUTO"
            n_bits = row.n_bits
            log2n_items = convert_int(row.log2n_items)
            register_signals = []
            port_has_inputs = False
            port_has_outputs = False
            n_bits = convert_int(n_bits)
            # Figure out how many bits needed to select each byte in the CSR word,
            # and how many bits to address each byte in the entire CSR array
            if type(n_bits) is int:
                num_byte_sel_bits = (ceil(n_bits / 8) - 1).bit_length()
            else:
                num_byte_sel_bits = f"$clog2({n_bits}/8)"

            if (type(log2n_items) is int) and (type(n_bits) is int):
                internal_addr_w = log2n_items + num_byte_sel_bits
            else:
                internal_addr_w = f"{log2n_items}+{num_byte_sel_bits}"

            # version is not a register, it is an internal constant
            if name == "version":
                continue

            # Create ports signals for write CSR
            if "W" in row.mode:
                if auto:
                    register_signals.append(
                        {
                            "name": name + "_rdata_o",
                            "width": self.verilog_max(n_bits, 1),
                        }
                    )
                    port_has_outputs = True
                else:  # Not auto
                    register_signals += []
                    port_has_outputs = True
                    register_signals += [
                        {
                            "name": f"{name}_valid_o",
                            "width": 1,
                        },
                    ]
                    if type(log2n_items) is not int or log2n_items > 0:
                        register_signals += [
                            {
                                "name": f"{name}_addr_o",
                                "width": internal_addr_w,
                            },
                        ]
                    register_signals += [
                        {
                            "name": f"{name}_wdata_o",
                            "width": self.verilog_max(n_bits, 1),
                        },
                        {
                            "name": f"{name}_wstrb_o",
                            "width": self.verilog_max(f"{n_bits}/8", 1),
                        },
                        {
                            "name": f"{name}_ready_i",
                            "width": 1,
                        },
                    ]
                    port_has_inputs = True
                    port_has_outputs = True
            # Create ports signals for read CSR
            if "R" in row.mode:
                if auto:
                    register_signals.append(
                        {
                            "name": name + "_wdata_i",
                            "width": self.verilog_max(n_bits, 1),
                        }
                    )
                    # If CSR mode is "RW", then also include a wstrb signal (to mux input of single RW CSR)
                    if "W" in row.mode:
                        register_signals.append(
                            {
                                "name": name + "_wstrb_i",
                                "width": self.verilog_max(f"{n_bits}/8", 1),
                            }
                        )
                    port_has_inputs = True
                else:  # not auto
                    # Valid, addr, and ready are shared with "W" mode. Don't create them if they already exist.
                    if "W" not in row.mode:
                        register_signals += [
                            {
                                "name": f"{name}_valid_o",
                                "width": 1,
                            },
                        ]
                        if type(log2n_items) is not int or log2n_items > 0:
                            register_signals += [
                                {
                                    "name": f"{name}_addr_o",
                                    "width": internal_addr_w,
                                },
                            ]
                    register_signals += [
                        {
                            "name": f"{name}_rdata_i",
                            "width": self.verilog_max(n_bits, 1),
                        },
                        {
                            "name": f"{name}_rready_o",
                            "width": 1,
                        },
                    ]
                    if "W" not in row.mode:
                        register_signals += [
                            {
                                "name": f"{name}_ready_i",
                                "width": 1,
                            },
                        ]
                    register_signals += [
                        {
                            "name": f"{name}_rvalid_i",
                            "width": 1,
                        },
                    ]
                    port_has_inputs = True
                    port_has_outputs = True

            # Remove suffixes from signals if CSR is for 'internal_use'
            # and create internal wires instead of ports.
            if row.internal_use:
                for reg in register_signals:
                    reg["name"] = reg["name"][:-2]
                wires.append(
                    {
                        "name": name,
                        "descr": f"{name} register interface",
                        "signals": register_signals,
                    }
                )
            else:  # CSR is implemented externally. Create port.
                if port_has_inputs and port_has_outputs:
                    direction = "_io"
                elif port_has_inputs:
                    direction = "_i"
                else:
                    direction = "_o"
                ports.append(
                    {
                        "name": name + direction,
                        "descr": f"{name} register interface",
                        "signals": register_signals,
                    }
                )

        return ports, wires, snippet

    def get_csrs_inst_params(self, core_confs):
        """Return multi-line string with parameters for csrs instance"""
        param_list = [p for p in core_confs if p["type"] == "P"]
        if not param_list:
            return ""

        param_str = "#(\n"
        for idx, param in enumerate(param_list):
            comma = "," if idx < len(param_list) - 1 else ""
            param_str += f"    .{param['name']}({param['name']}){comma}\n"
        param_str += ") "
        return param_str

    def write_hwcode(self, table, core_attributes):
        """Generates and appends verilog code to core "snippets" list."""
        ports = []
        wires = []
        subblocks = []
        snippet = ""
        # check if all registers are auto and add rready_int if not
        all_auto = True
        all_reads_auto = True
        for row in table:
            if row.type == "NOAUTO":
                all_auto = False
                if "R" in row.mode:
                    all_reads_auto = False
                    break

        if not all_reads_auto:
            wires.append(
                {
                    "name": "rready_int",
                    "descr": "",
                    "signals": [
                        {"name": "rready_int", "width": 1, "isvar": True},
                    ],
                }
            )

        # TODO: These converters should be handled by a single universal converter as specified in: https://github.com/IObundle/py2hwsw/issues/259
        if core_attributes["csr_if"] == "iob":
            # "IOb" CSR_IF
            snippet += """
   assign internal_iob_valid = iob_valid_i;
   assign internal_iob_addr = iob_addr_i;
   assign internal_iob_wdata = iob_wdata_i;
   assign internal_iob_wstrb = iob_wstrb_i;
   assign internal_iob_rready = iob_rready_i;
   assign iob_rvalid_o = internal_iob_rvalid;
   assign iob_rdata_o = internal_iob_rdata;
   assign iob_ready_o = internal_iob_ready;
"""
        elif core_attributes["csr_if"] == "apb":
            # "APB" CSR_IF
            subblocks.append(
                {
                    "core_name": "iob_apb2iob",
                    "instance_name": "iob_apb2iob_coverter",
                    "instance_description": "Convert APB port into internal IOb interface",
                    "parameters": {
                        "APB_ADDR_W": "ADDR_W",
                        "APB_DATA_W": "DATA_W",
                    },
                    "connect": {
                        "clk_en_rst_s": "clk_en_rst_s",
                        "apb_s": "control_if_s",
                        "iob_m": "internal_iob",
                    },
                }
            )
        elif core_attributes["csr_if"] == "axil":
            # "AXI_Lite" CSR_IF
            subblocks.append(
                {
                    "core_name": "iob_axil2iob",
                    "instance_name": "iob_axil2iob_coverter",
                    "instance_description": "Convert AXI-Lite port into internal IOb interface",
                    "parameters": {
                        "AXIL_ADDR_W": "ADDR_W",
                        "AXIL_DATA_W": "DATA_W",
                    },
                    "connect": {
                        "clk_en_rst_s": "clk_en_rst_s",
                        "axil_s": "control_if_s",
                        "iob_m": "internal_iob",
                    },
                }
            )
        elif core_attributes["csr_if"] == "axi":
            # "AXI" CSR_IF
            subblocks.append(
                {
                    "core_name": "iob_axi2iob",
                    "instance_name": "iob_axi2iob_coverter",
                    "instance_description": "Convert AXI port into internal IOb interface",
                    "parameters": {
                        "ADDR_WIDTH": "ADDR_W",
                        "DATA_WIDTH": "DATA_W",
                        "AXI_ID_WIDTH": "AXI_ID_W",
                        "AXI_LEN_WIDTH": "AXI_LEN_W",
                    },
                    "connect": {
                        "clk_en_rst_s": "clk_en_rst_s",
                        "axi_s": (
                            "control_if_s",
                            [
                                "axi_awlock_i[0]",
                                "axi_arlock_i[0]",
                            ],
                        ),
                        "iob_m": "internal_iob",
                    },
                }
            )
        elif core_attributes["csr_if"] == "wb":
            # "wb" CSR_IF
            subblocks.append(
                {
                    "core_name": "iob_wishbone2iob",
                    "instance_name": "iob_wishbone2iob_coverter",
                    "instance_description": "Convert Wishbone port into internal IOb interface",
                    "parameters": {
                        "ADDR_W": "ADDR_W",
                        "DATA_W": "DATA_W",
                    },
                    "connect": {
                        "clk_en_rst_s": "clk_en_rst_s",
                        "wb_s": "control_if_s",
                        "iob_m": "internal_iob",
                    },
                }
            )

        for row in table:
            if "W" in row.mode:
                # compute write address based on write strobe (ignore LSBs)
                snippet += "    wire [ADDR_W-1:0] wstrb_addr;\n"
                snippet += "    assign wstrb_addr = `IOB_WORD_ADDR(internal_iob_addr_stable) + byte_offset;\n"
                break

        for row in table:
            if "R" in row.mode:
                # Create special read strobe for "REG" (auto) CSRs
                snippet += """
// Create a special readstrobe for "REG" (auto) CSRs.
// LSBs 0 = read full word; LSBs 1 = read byte; LSBs 2 = read half word; LSBs 3 = read byte.
   reg shift_amount;
   always @(*)
      case (internal_iob_addr_stable[1:0])
         // Access entire word
         2'b00: shift_amount = 2;
         // Access single byte
         2'b01: shift_amount = 0;
         // Access half word
         2'b10: shift_amount = 1;
         // Access single byte
         2'b11: shift_amount = 0;
         default: shift_amount = 0;
      endcase
"""
                break

        # insert write register logic
        for row in table:
            if "W" in row.mode:
                _snippet, _wires = self.gen_wr_reg(row)
                snippet += _snippet
                wires += _wires

        # insert read register logic
        for row in table:
            if "R" in row.mode:
                _snippet, _wires = self.gen_rd_reg(row)
                snippet += _snippet
                wires += _wires

        #
        # RESPONSE SWITCH
        #
        wires += [
            # iob_regs
            {
                "name": "iob_rvalid_out",
                "descr": "",
                "signals": [
                    {"name": "iob_rvalid_out", "width": 1},
                ],
            },
            {
                "name": "iob_rvalid_nxt",
                "descr": "",
                "signals": [
                    {
                        "name": "iob_rvalid_nxt",
                        "width": 1,
                        "isvar": True,
                        "isreg": True,
                    },
                ],
            },
            {
                "name": "iob_rdata_out",
                "descr": "",
                "signals": [
                    {"name": "iob_rdata_out", "width": 8 * self.cpu_n_bytes},
                ],
            },
            {
                "name": "iob_rdata_nxt",
                "descr": "",
                "signals": [
                    {
                        "name": "iob_rdata_nxt",
                        "width": 8 * self.cpu_n_bytes,
                        "isvar": True,
                        "isreg": True,
                    },
                ],
            },
            {
                "name": "iob_ready_out",
                "descr": "",
                "signals": [
                    {"name": "iob_ready_out", "width": 1},
                ],
            },
            {
                "name": "iob_ready_nxt",
                "descr": "",
                "signals": [
                    {"name": "iob_ready_nxt", "width": 1, "isvar": True, "isreg": True},
                ],
            },
        ]
        if not all_auto:
            wires += [
                {
                    "name": "rvalid_int",
                    "descr": "Rvalid signal of currently addressed CSR",
                    "signals": [
                        {"name": "rvalid_int", "width": 1, "isvar": True},
                    ],
                },
                {
                    "name": "ready_int",
                    "descr": "Ready signal of currently addressed CSR",
                    "signals": [
                        {"name": "ready_int", "width": 1, "isvar": True},
                    ],
                },
                {
                    "name": "auto_addressed",
                    "descr": "Flag if an auto-register is currently addressed",
                    "signals": [
                        {"name": "auto_addressed", "width": 1, "isvar": True},
                    ],
                },
            ]
        subblocks += [
            {
                "core_name": "iob_reg",
                "instance_name": "rvalid_reg",
                "instance_description": "rvalid register",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": "1'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "iob_rvalid_nxt",
                    "data_o": "iob_rvalid_out",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "rdata_reg",
                "instance_description": "rdata register",
                "parameters": {
                    "DATA_W": 8 * self.cpu_n_bytes,
                    "RST_VAL": f"{8 * self.cpu_n_bytes}'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "iob_rdata_nxt",
                    "data_o": "iob_rdata_out",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "ready_reg",
                "instance_description": "ready register",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": "1'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "iob_ready_nxt",
                    "data_o": "iob_ready_out",
                },
            },
        ]

        # auxiliar read register cases
        for row in table:
            if "R" in row.mode:
                aux_read_reg = self.aux_read_reg_case_name(row)
                if aux_read_reg:
                    wires.append(
                        {
                            "name": aux_read_reg,
                            "descr": "",
                            "signals": [
                                {"name": aux_read_reg, "width": 1, "isvar": True},
                            ],
                        },
                    )

        # Create byte aligned wires
        for row in table:
            name = row.name
            auto = row.type != "NOAUTO"
            suffix = "" if row.internal_use else "_i"
            n_bits = row.n_bits
            n_bytes = int(self.bceil(n_bits, 3) / 8)
            if n_bytes == 3:
                n_bytes = 4
            if "R" in row.mode:
                if name == "version":
                    pass
                elif auto:
                    snippet += f"wire [{8*n_bytes-1}:0] byte_aligned_{name};\n"
                    snippet += f"assign byte_aligned_{name} = {name}_rdata;\n"
                else:
                    snippet += f"wire [{8*n_bytes-1}:0] byte_aligned_{name}_rdata;\n"
                    snippet += (
                        f"assign byte_aligned_{name}_rdata = {name}_rdata{suffix};\n"
                    )

        # Response signals switch logic
        if all_auto:
            snippet += """
    //RESPONSE SWITCH

    assign internal_iob_rvalid = iob_rvalid_out;
    assign internal_iob_rdata = iob_rdata_out;
    assign internal_iob_ready = iob_ready_out;
"""
        else:  # Not all auto
            snippet += """
    //RESPONSE SWITCH

    // Don't register response signals if accessing non-auto CSR
    assign internal_iob_rvalid = auto_addressed ? iob_rvalid_out : rvalid_int;
    assign internal_iob_rdata = auto_addressed ? iob_rdata_out : iob_rdata_nxt;
    assign internal_iob_ready = auto_addressed ? iob_ready_out : ready_int;
"""

        snippet += f"""
    always @* begin
        iob_rdata_nxt = {8*self.cpu_n_bytes}'d0;
"""
        if not all_auto:
            snippet += f"""
        rvalid_int = 1'b1;
        ready_int = 1'b1;
        if (internal_iob_valid) begin
            auto_addressed = 1'b1;
        end
"""

        # read register response
        for row in table:
            name = row.name
            addr = row.addr
            n_bits = row.n_bits
            log2n_items = row.log2n_items
            n_bytes = int(self.bceil(n_bits, 3) / 8)
            if n_bytes == 3:
                n_bytes = 4
            addr_last = int(
                addr
                + (
                    (
                        2
                        ** eval_param_expression_from_config(
                            log2n_items, self.config, "max"
                        )
                    )
                )
                * n_bytes
            )
            addr_w = self.calc_addr_w(log2n_items, n_bytes)
            addr_w_base = max(log(self.cpu_n_bytes, 2), addr_w)
            auto = row.type != "NOAUTO"
            suffix = "" if row.internal_use else "_i"

            if "R" in row.mode:
                if auto:
                    snippet += f"        if({name}_addressed_r) "
                else:  # Not auto
                    snippet += f"        if({name}_addressed) "
                snippet += "begin\n"
                if name == "version":
                    rst_val = row.rst_val
                    snippet += f"            iob_rdata_nxt[{self.boffset(addr, self.cpu_n_bytes)}+:{8*n_bytes}] = {8*n_bytes}'h{rst_val}|{8*n_bytes}'d0;\n"
                elif auto:
                    snippet += f"            iob_rdata_nxt[{self.boffset(addr, self.cpu_n_bytes)}+:{8*n_bytes}] = byte_aligned_{name}|{8*n_bytes}'d0;\n"
                else:
                    snippet += f"""
            iob_rdata_nxt[{self.boffset(addr, self.cpu_n_bytes)}+:{8*n_bytes}] = byte_aligned_{name}_rdata|{8*n_bytes}'d0;
            rvalid_int = {name}_rvalid{suffix};
"""
                if not auto:
                    snippet += f"            ready_int = {name}_ready{suffix};\n"
                    snippet += (
                        "            if (internal_iob_valid & ~|internal_iob_wstrb) begin\n"
                        "                auto_addressed = 1'b0;\n"
                        "            end\n"
                    )
                snippet += "        end\n\n"

        # write register response
        for row in table:
            name = row.name
            addr = row.addr
            n_bits = row.n_bits
            log2n_items = row.log2n_items
            n_bytes = int(self.bceil(n_bits, 3) / 8)
            if n_bytes == 3:
                n_bytes = 4
            addr_w = self.calc_addr_w(log2n_items, n_bytes)
            auto = row.type != "NOAUTO"
            suffix = "" if row.internal_use else "_i"

            if "W" in row.mode:
                if not auto:
                    # get ready
                    snippet += f"        if((wstrb_addr >= {addr}) && (wstrb_addr < {addr + 2**addr_w})) begin\n"
                    snippet += f"            ready_int = {name}_ready{suffix};\n"
                    snippet += (
                        "            if (internal_iob_valid & |internal_iob_wstrb) begin\n"
                        "                auto_addressed = 1'b0;\n"
                        "            end\n"
                    )
                    snippet += "        end\n\n"

        snippet += """

        // ######  FSM  #############

        //FSM default values
        iob_ready_nxt = 1'b0;
        iob_rvalid_nxt = 1'b0;
        state_nxt = state;
"""
        if not all_reads_auto:
            snippet += """
        rready_int = 1'b0;
"""
        snippet += """

        //FSM state machine
        case(state)
            WAIT_REQ: begin
                if(internal_iob_valid & (!internal_iob_ready)) begin // Wait for a valid request
"""
        if not all_auto:
            snippet += """
                    iob_ready_nxt = ready_int;
"""
        else:
            snippet += """
                    iob_ready_nxt = 1'b1;
"""
        snippet += """
                    // If is read and ready, go to WAIT_RVALID
                    if (iob_ready_nxt && (!write_en)) begin
                        state_nxt = WAIT_RVALID;
                    end
                end
            end

            default: begin  // WAIT_RVALID
                if (internal_iob_rready & internal_iob_rvalid) begin // Transfer done
"""
        if not all_reads_auto:
            snippet += """
                    rready_int = 1'b1;
"""
        snippet += """
                    iob_rvalid_nxt = 1'b0;
                    state_nxt = WAIT_REQ;
                end else begin
"""
        if not all_reads_auto:
            snippet += """
                    iob_rvalid_nxt = rvalid_int;
"""
        else:
            snippet += """
                    iob_rvalid_nxt = 1'b1;
"""
        snippet += """
                end
            end
        endcase

    end //always @*
"""

        core_attributes["ports"] += ports
        core_attributes["wires"] += wires
        core_attributes["subblocks"] += subblocks
        core_attributes["snippets"] += [{"verilog_code": snippet}]

    def write_hwheader(self, table, out_dir, top):
        os.makedirs(out_dir, exist_ok=True)
        f_def = open(f"{out_dir}/{top}.vh", "w")
        f_def.write("//These macros may be dependent on instance parameters\n")
        f_def.write("//address macros\n")
        macro_prefix = f"{top}_".upper()
        f_def.write("//addresses\n")
        for row in table:
            name = row.name.upper()
            n_bits = row.n_bits
            n_bytes = self.bceil(n_bits, 3) / 8
            if n_bytes == 3:
                n_bytes = 4
            log2n_items = row.log2n_items
            f_def.write(f"`define {macro_prefix}{name}_ADDR {row.addr}\n")
            if eval_param_expression_from_config(log2n_items, self.config, "max") > 0:
                f_def.write(
                    f"`define {macro_prefix}{name}_ADDR_W {self.verilog_max(self.calc_verilog_addr_w(log2n_items,n_bytes),1)}\n"
                )
            f_def.write(
                f"`define {macro_prefix}{name}_W {self.verilog_max(n_bits,1)}\n\n"
            )
        f_def.close()

    # Get C type from csrs n_bytes
    # uses unsigned int types from C stdint library
    @staticmethod
    def csr_type(name, n_bytes):
        type_dict = {1: "uint8_t", 2: "uint16_t", 4: "uint32_t", 8: "uint64_t"}
        try:
            type_try = type_dict[n_bytes]
        except:
            print(
                f"{iob_colors.FAIL}register {name} has invalid number of bytes {n_bytes}.{iob_colors.ENDC}"
            )
            type_try = -1
        return type_try

    def write_swheader(self, table, out_dir, top):
        os.makedirs(out_dir, exist_ok=True)
        fswhdr = open(f"{out_dir}/{top}.h", "w")

        core_prefix = f"{top}_"
        core_prefix_upper = f"{top}_".upper()

        fswhdr.write(f"#ifndef H_{core_prefix_upper}CSRS_H\n")
        fswhdr.write(f"#define H_{core_prefix_upper}CSRS_H\n\n")

        doxygen_core = top.strip("_csrs")
        fswhdr.write(f"/** @file {top}.h\n")
        fswhdr.write(f" *  @brief Function prototypes for the {doxygen_core} core.\n")
        fswhdr.write(" *\n")
        fswhdr.write(
            " *  This file contains the function prototypes to access the Control and Status\n"
        )
        fswhdr.write(f" * Registers (CSRs) for the {doxygen_core} core.\n")
        fswhdr.write(" *\n")
        fswhdr.write(" *  This file is automatically generated by Py2HWSW\n")
        fswhdr.write(" */\n\n")

        fswhdr.write("#include <stdint.h>\n\n")

        fswhdr.write("//used address space width\n")

        addr_w_macro = f"{core_prefix_upper}CSRS_ADDR_W"
        fswhdr.write("/**\n")
        fswhdr.write(f" * @def {addr_w_macro}\n")
        fswhdr.write(" * @brief Used core address space width.\n")
        fswhdr.write(" *\n")
        fswhdr.write(
            " * This macro defines the required address width in bits to access all core\n"
        )
        fswhdr.write(" * CSRs.\n")
        fswhdr.write(" */\n")
        fswhdr.write(f"#define  {addr_w_macro} {self.core_addr_w}\n\n")

        fswhdr.write("//Addresses\n")

        for row in table:
            name = row.name.upper()
            if "W" in row.mode or "R" in row.mode:
                addr_macro = f"{core_prefix_upper}{name}_ADDR"
                fswhdr.write("/**\n")
                fswhdr.write(f" * @def {addr_macro}\n")
                fswhdr.write(f" * @brief {row.name} CSR address.\n")
                fswhdr.write(" */\n")
                fswhdr.write(f"#define {addr_macro} {row.addr}\n")

        fswhdr.write("\n//Data widths (bit)\n")

        for row in table:
            name = row.name.upper()
            n_bits = row.n_bits
            n_bytes = int(self.bceil(n_bits, 3) / 8)
            if n_bytes == 3:
                n_bytes = 4
            if "W" in row.mode or "R" in row.mode:
                width_macro = f"{core_prefix_upper}{name}_W"
                fswhdr.write("/**\n")
                fswhdr.write(f" * @def {width_macro}\n")
                fswhdr.write(f" * @brief {row.name} CSR Width.\n")
                fswhdr.write(" */\n")
                fswhdr.write(f"#define {width_macro} {n_bytes*8}\n")

        fswhdr.write("\n// Base Address\n")

        fswhdr.write("/**\n")
        fswhdr.write(" * @brief Set core base address.\n")
        fswhdr.write(" *\n")
        fswhdr.write(
            " * This function sets the base address for the core in the system. All other\n"
        )
        fswhdr.write(" * accesses are offset from this base address.\n")
        fswhdr.write(" *\n")
        fswhdr.write(" * @param addr Base address for core.\n")
        fswhdr.write(" */\n")
        fswhdr.write(f"void {core_prefix}init_baseaddr(uint32_t addr);\n")

        fswhdr.write("\n// IO read and write function prototypes\n")
        fswhdr.write("/**\n")
        fswhdr.write(" * @brief Write access function prototype.\n")
        fswhdr.write(" *\n")
        fswhdr.write(" * @param addr Address to write to.\n")
        fswhdr.write(" * @param data_w Data width in bits.\n")
        fswhdr.write(" * @param value Value to write.\n")
        fswhdr.write(" */\n")
        fswhdr.write(
            "void iob_write(uint32_t addr, uint32_t data_w, uint32_t value);\n"
        )

        fswhdr.write("/**\n")
        fswhdr.write(" * @brief Read access function prototype.\n")
        fswhdr.write(" *\n")
        fswhdr.write(" * @param addr Address to write to.\n")
        fswhdr.write(" * @param data_w Data width in bits.\n")
        fswhdr.write(" * @return uint32_t Read data value.\n")
        fswhdr.write(" */\n")
        fswhdr.write("uint32_t iob_read(uint32_t addr, uint32_t data_w);\n")

        fswhdr.write("\n// Core Setters and Getters\n")

        for row in table:
            name = row.name
            n_bits = row.n_bits
            log2n_items = row.log2n_items
            n_bytes = self.bceil(n_bits, 3) / 8
            if n_bytes == 3:
                n_bytes = 4
            addr_w = self.calc_addr_w(log2n_items, n_bytes)
            if "W" in row.mode:
                sw_type = self.csr_type(name, n_bytes)
                addr_arg = ""

                fswhdr.write("/**\n")
                fswhdr.write(f" * @brief Set {name} value.\n")
                fswhdr.write(f" * {row.descr}\n")
                fswhdr.write(f" * @param value {name} Value.\n")
                if addr_w / n_bytes > 1:
                    addr_arg = ", int addr"
                    fswhdr.write(f" * @param addr {name} array address.\n")
                fswhdr.write(" */\n")
                fswhdr.write(
                    f"void {core_prefix}set_{name}({sw_type} value{addr_arg});\n"
                )
            if "R" in row.mode:
                sw_type = self.csr_type(name, n_bytes)
                addr_arg = ""

                fswhdr.write("/**\n")
                fswhdr.write(f" * @brief Get {name} value.\n")
                fswhdr.write(f" * {row.descr}\n")
                if addr_w / n_bytes > 1:
                    addr_arg = "int addr"
                    fswhdr.write(f" * @param addr {name} array address.\n")
                fswhdr.write(f" * @return {sw_type} {name} value.\n")
                fswhdr.write(" */\n")
                fswhdr.write(f"{sw_type} {core_prefix}get_{name}({addr_arg});\n")

        fswhdr.write(f"\n#endif // H_{core_prefix_upper}_CSRS_H\n")

        fswhdr.close()

    def write_swcode(self, table, out_dir, top):
        os.makedirs(out_dir, exist_ok=True)
        fsw = open(f"{out_dir}/{top}.c", "w")
        core_prefix = f"{top}_"
        core_prefix_upper = core_prefix.upper()
        fsw.write(f'#include "{top}.h"\n\n')
        fsw.write("\n// Base Address\n")
        fsw.write("static uint32_t base;\n")
        fsw.write(f"void {core_prefix}init_baseaddr(uint32_t addr) {{\n")
        fsw.write("  base = addr;\n")
        fsw.write("}\n")

        fsw.write("\n// Core Setters and Getters\n")

        for row in table:
            name = row.name
            name_upper = row.name.upper()
            n_bits = row.n_bits
            log2n_items = row.log2n_items
            n_bytes = self.bceil(n_bits, 3) / 8
            if n_bytes == 3:
                n_bytes = 4
            addr_w = self.calc_addr_w(log2n_items, n_bytes)
            addr = f"base + {core_prefix_upper}{name_upper}_ADDR"
            sw_type = self.csr_type(name, n_bytes)

            # addr argument for regfiles
            addr_arg = ""
            addr_offset = ""
            if addr_w / n_bytes > 1:
                addr_arg = "int addr"
                # regfiles are addressed at each n_bits
                addr_offset = f"+(addr << {int(log2(n_bytes))})"

            if "W" in row.mode:
                waddr_arg = ""
                if addr_arg:
                    waddr_arg = f", {addr_arg}"
                fsw.write(
                    f"void {core_prefix}set_{name}({sw_type} value{waddr_arg}) {{\n"
                )
                fsw.write(
                    f"  iob_write({addr}{addr_offset}, {core_prefix_upper}{name_upper}_W, value);\n"
                )
                fsw.write("}\n\n")
            if "R" in row.mode:
                fsw.write(f"{sw_type} {core_prefix}get_{name}({addr_arg}) {{\n")
                fsw.write(
                    f"  return iob_read({addr}{addr_offset}, {core_prefix_upper}{name_upper}_W);\n"
                )
                fsw.write("}\n\n")
        fsw.close()

    # check if address is aligned
    @staticmethod
    def check_alignment(addr, addr_w):
        if addr % (2**addr_w) != 0:
            sys.exit(
                f"{iob_colors.FAIL}address {addr} with span {2**addr_w} is not aligned{iob_colors.ENDC}"
            )

    # check if address overlaps with previous
    @staticmethod
    def check_overlap(addr, addr_mode, read_addr, write_addr):
        if addr_mode == "R" and addr < read_addr:
            sys.exit(
                f"{iob_colors.FAIL}read address {addr} overlaps with previous addresses{iob_colors.ENDC}"
            )
        elif addr_mode == "W" and addr < write_addr:
            sys.exit(
                f"{iob_colors.FAIL}write address {addr} overlaps with previous addresses{iob_colors.ENDC}"
            )

    # check autoaddr configuration
    @staticmethod
    def check_autoaddr(autoaddr, row):
        is_version = row.name == "version"
        if is_version:
            # version has always automatic address
            return -1

        # invalid autoaddr + register addr configurations
        if autoaddr and row.addr > -1:
            sys.exit(
                f"{iob_colors.FAIL}Manual address in register named {row.name} while in auto address mode.{iob_colors.ENDC}"
            )
        if (not autoaddr) and row.addr < 0:
            sys.exit(
                f"{iob_colors.FAIL}Missing address in register named {row.name} while in manual address mode.{iob_colors.ENDC}"
            )

        if autoaddr:
            return -1
        else:
            return row.addr

    # compute address
    def compute_addr(self, table, rw_overlap, autoaddr):
        read_addr = 0
        write_addr = 0

        tmp = []

        for row in table:
            addr = self.check_autoaddr(autoaddr, row)
            addr_mode = row.mode
            n_bits = row.n_bits
            log2n_items = row.log2n_items
            n_bytes = self.bceil(n_bits, 3) / 8
            if n_bytes == 3:
                n_bytes = 4
            addr_w = self.calc_addr_w(log2n_items, n_bytes)
            if addr >= 0:  # manual address
                self.check_alignment(addr, addr_w)
                self.check_overlap(addr, addr_mode, read_addr, write_addr)
                addr_tmp = addr
            elif "R" in addr_mode:  # auto address
                read_addr = self.bceil(read_addr, addr_w)
                addr_tmp = read_addr
            elif "W" in addr_mode:
                write_addr = self.bceil(write_addr, addr_w)
                addr_tmp = write_addr
            else:
                sys.exit(
                    f"{iob_colors.FAIL}invalid address mode {addr_mode} for register named {row.name}{iob_colors.ENDC}"
                )

            if autoaddr and not rw_overlap:
                addr_tmp = max(read_addr, write_addr)

            # save address temporarily in list
            tmp.append(addr_tmp)

            # update addresses
            addr_tmp += 2**addr_w
            if "R" in addr_mode:
                read_addr = addr_tmp
            elif "W" in addr_mode:
                write_addr = addr_tmp
            if not rw_overlap:
                read_addr = addr_tmp
                write_addr = addr_tmp

        # update reg addresses
        for i in range(len(tmp)):
            table[i].addr = tmp[i]

        # update core address space size
        self.core_addr_w = int(ceil(log(max(read_addr, write_addr), 2)))

        return table

    # Generate csrs.tex file with list TeX tables of regs
    @staticmethod
    def generate_csrs_tex(doc_tables, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        csrs_file = open(f"{out_dir}/csrs.tex", "w")

        csrs_file.write(
            """
The software accessible registers of the core are described in the following
tables. The tables give information on the name, read/write capability, address, width in bits, and a textual description.
"""
        )

        for doc_conf, doc_table in doc_tables.items():
            csrs_file.write(f"\\subsubsection{{{doc_conf} Configuration}}")

            for csr_group in doc_table:
                csrs_file.write(
                    """
\\begin{xltabular}{\\textwidth}{|l|c|c|c|c|X|}

  \\hline
  \\rowcolor{iob-green}
  {\\bf Name} & {\\bf R/W} & {\\bf Addr} & {\\bf Width} & {\\bf Default} & {\\bf Description} \\\\ \\hline

  \\input """
                    + doc_conf
                    + f"_{csr_group.name}"
                    + """_csrs_tab

  \\caption{"""
                    + csr_group.descr.replace("_", "\\_")
                    + """}
\\end{xltabular}
\\label{"""
                    + doc_conf
                    + f"_{csr_group.name}"
                    + """_csrs_tab:is}
"""
                )

                if csr_group.doc_clearpage:
                    csrs_file.write("\\clearpage")

        csrs_file.close()

    # Generate TeX tables of registers
    # doc_tables: dictionary of doc_conf tables,
    #    each ['doc_conf'] key as respective doc_table only with valid registers
    # out_dir: output directory
    @classmethod
    def generate_regs_tex(self, doc_tables, out_dir):
        os.makedirs(out_dir, exist_ok=True)
        # Create csrs.tex file
        self.generate_csrs_tex(doc_tables, out_dir)

        for doc_conf, doc_table in doc_tables.items():
            for csr_group in doc_table:
                tex_table = []
                for reg in csr_group.regs:
                    tex_table.append(
                        [
                            reg.name.upper(),
                            reg.mode,
                            str(reg.addr),
                            str(reg.n_bits),
                            str(reg.rst_val),
                            reg.descr,
                        ]
                    )
                write_table(f"{out_dir}/{doc_conf}_{csr_group.name}_csrs", tex_table)
