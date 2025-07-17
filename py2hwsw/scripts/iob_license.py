# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import fail_with_msg, parse_short_notation_text

from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_license")
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
    return iob_license(**license_dict)


def license_text2dict(license_text):
    license_flags = [
        "name",
        ["-y", {"dest": "year"}],
        ["-a", {"dest": "author"}],
    ]
    return parse_short_notation_text(license_text, license_flags)


def license_from_text(license_text):
    return license_from_dict(license_text2dict(license_text))
