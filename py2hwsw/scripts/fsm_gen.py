#!/usr/bin/env python3


def generate_fsms(core):
    out_dir = core.build_dir + "/hardware/src"

    f_fsms = open(f"{out_dir}/{core.name}_fsms.vs", "w+")

    for fsm in core.fsms:
        f_fsms.write(fsm.verilog_code)
        f_fsms.write("\n")

    f_fsms.close()
