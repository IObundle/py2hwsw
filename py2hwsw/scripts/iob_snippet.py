# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from iob_base import assert_attributes
import importlib


from api_base import api_class


@api_class
@dataclass
class iob_snippet:
    """Class to represent a Verilog snippet in an iob module"""


def create_snippet(core, *args, **kwargs):
    """Create a Verilog snippet to insert in given core."""
    # Ensure 'snippets' list exists
    core.set_default_attribute("snippets", [])
    assert_attributes(
        iob_snippet,
        kwargs,
        error_msg=f"Invalid {kwargs.get('name', '')} snippet attribute '[arg]'!",
    )
    snippet = iob_snippet(*args, **kwargs)
    core.snippets.append(snippet)


#
# API methods
#


def snippet_from_dict(snippet_dict):
    api_iob_snippet = importlib.import_module("user_api.api").api_iob_snippet
    return api_iob_snippet(**snippet_dict)


def snippet_from_text(snippet_text):
    api_iob_snippet = importlib.import_module("user_api.api").api_iob_snippet
    snippet_dict = {}
    # TODO: parse short notation text
    return api_iob_snippet(**snippet_dict)
