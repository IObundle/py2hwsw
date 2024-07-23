#!/usr/bin/env python3


def generate_combs(core):
    out_dir = core.build_dir + "/hardware/src"

    f_combs = open(f"{out_dir}/{core.name}_combs.vs", "w+")

    for comb in core.combs:
        f_combs.write(comb.verilog_code)
        f_combs.write("\n")

    f_combs.close()
