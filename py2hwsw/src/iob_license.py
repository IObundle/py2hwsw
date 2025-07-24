# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from datetime import date

from iob_base import fail_with_msg, parse_short_notation_text


@dataclass
class iob_license:
    """
    Class that represents a license attribute.

    Attributes:
        name (str): Name of the license.
        year (int): Year of the license.
        author (str): Author of the license.
    """

    name: str = "MIT"
    year: int = date.today().year
    author: str = "IObundle, Lda"

    @staticmethod
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
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(license_dict):
        """
        Function to create iob_license object from dictionary attributes.

        Attributes:
            license_dict (dict): dictionary with values to initialize attributes of iob_license object.
                This dictionary supports the following keys corresponding to the iob_license attributes:
                - name -> iob_license.name
                - year -> iob_license.year
                - author -> iob_license.author

        Returns:
            iob_license: iob_license object
        """
        return iob_license(**license_dict)

    @staticmethod
    def license_text2dict(license_text):
        """Convert license short notation text to dictionary.
        Atributes:
            license_text (str): Short notation text. See `create_from_text` for format.

        Returns:
            dict: Dictionary with license attributes.
        """
        license_flags = [
            "name",
            ["-y", {"dest": "year", "type": int}],
            ["-a", {"dest": "author"}],
        ]
        return parse_short_notation_text(license_text, license_flags)

    @staticmethod
    def create_from_text(license_text):
        """
        Function to create iob_license object from short notation text.

        Attributes:
            license_text (str): Short notation text. Object attributes are specified using the following format:
                [name] [-y year] [-a author]
                Example:
                    MIT -y 2025 -a 'IObundle, Lda'

        Returns:
            iob_license: iob_license object
        """
        return __class__.create_from_dict(__class__.license_text2dict(license_text))
