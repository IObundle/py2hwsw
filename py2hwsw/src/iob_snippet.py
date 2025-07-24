# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass


@dataclass
class iob_snippet:
    """
    Class to represent a Verilog snippet in an iob module.

    Attributes:
        verilog_code (str): Verilog code string
    """

    verilog_code: str = ""

    pass

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_snippet_from_dict(snippet_dict):
        """
        Function to create iob_snippet object from dictionary attributes.

        Attributes:
            snippet_dict (dict): dictionary with values to initialize attributes of iob_snippet object.
                This dictionary supports the following keys corresponding to the iob_snippet attributes:
                - verilog_code -> iob_snippet.verilog_code

        Returns:
            iob_snippet: iob_snippet object
        """
        return iob_snippet(**snippet_dict)

    @staticmethod
    def snippet_text2dict(snippet_text):
        """Convert snippet short notation text to dictionary.
        Atributes:
            snippet_text (str): Short notation text. See `create_snippet_from_text` for format.

        Returns:
            dict: Dictionary with snippet attributes.
        """
        return {"verilog_code": snippet_text}

    @staticmethod
    def create_snippet_from_text(snippet_text):
        """
        Function to create iob_snippet object from short notation text.

        Attributes:
            snippet_text (str): Short notation text. Object attributes are specified using the following format:
                [snippet_text]

        Returns:
            iob_snippet: iob_snippet object
        """
        return __class__.create_snippet_from_dict(
            __class__.snippet_text2dict(snippet_text)
        )
