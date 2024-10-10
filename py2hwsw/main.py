# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def main():
    # This file is just a wrapper for py2hwsw.py
    import os
    import sys
    import py2hwsw

    py2hwsw_path = os.path.dirname(py2hwsw.__file__) + "/scripts/py2hwsw.py"

    args = ""
    for arg in sys.argv[1:]:
        args += arg + " "

    os.system('python3 "' + py2hwsw_path + '" ' + args)
