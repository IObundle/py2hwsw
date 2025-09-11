# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT
import os
import shutil
import stat


def setup(py_params_dict):
    # Copy iob_cov_analyze.py to BUILD_DIR scripts
    src = os.path.join(os.path.dirname(__file__), "./src/iob_cov_analyze.py")
    dst = os.path.join(py_params_dict["build_dir"], "scripts/iob_cov_analyze.py")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    # Hack for Nix: Files copied from Nix's py2hwsw package do not contain write permissions
    os.chmod(dst, os.stat(dst).st_mode + stat.S_IEXEC | stat.S_IXGRP)

    attributes_dict = {
        "generate_hw": False,
        "instantiate": False,
    }

    return attributes_dict
