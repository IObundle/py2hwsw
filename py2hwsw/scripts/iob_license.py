# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from datetime import date
import importlib

from iob_base import fail_with_msg


from api_base import internal_api_class


@internal_api_class
@dataclass
class iob_license:
    """Class that represents a license attribute"""


def update_license(core, *args, **kwargs):
    """Updates existing core license with new attributes
    param core: core object
    param kwargs: license arguments
    """
    for k, v in kwargs.items():
        if k not in dir(iob_license):
            fail_with_msg(f"Unknown license attribute: {k}")
        setattr(core.license, k, v)


#
# API methods
#


def license_from_dict(license_dict):
    api_iob_license = importlib.import_module("user_api.api").iob_license
    return api_iob_license(**license_dict)


def license_from_text(license_text):
    api_iob_license = importlib.import_module("user_api.api").iob_license
    license_dict = {}
    # TODO: parse short notation text
    return api_iob_license(**license_dict)
