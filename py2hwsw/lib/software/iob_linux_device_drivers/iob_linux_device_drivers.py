# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

"""Py2HWSW software module to generate Linux device drivers for the issuer core"""

import sys
import os

# Add scripts folder to python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from create_peripheral_device_drivers import generate_device_drivers


def setup(py_params_dict):

    assert (
        "issuer" in py_params_dict
    ), "Missing issuer core for Linux device drivers modules."

    assert (
        "build_dir" in py_params_dict
    ), "Missing build directory for Linux device drivers modules."

    linux_drivers_path = os.path.join(
        py_params_dict["build_dir"], "software/linux_drivers"
    )
    generate_device_drivers(linux_drivers_path, py_params_dict["issuer"])

    attributes_dict = {
        "generate_hw": False,
        "instantiate": False,
    }

    return attributes_dict
