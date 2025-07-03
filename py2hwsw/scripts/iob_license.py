# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from datetime import date

from iob_base import fail_with_msg


@dataclass
class iob_license:
    """Class that represents a license attribute"""

    # Identifier name for the license.
    name: str = "MIT"
    # Year of the license.
    year: int = date.today().year
    # Author of the license.
    author: str = "IObundle, Lda"


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
    return iob_license(**license_dict)


def license_from_text(license_text):
    license_dict = {}
    # TODO: parse short notation text
    return iob_license(**license_dict)
