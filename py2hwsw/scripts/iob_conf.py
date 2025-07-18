# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import fail_with_msg, parse_short_notation_text
from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_conf")
@dataclass
class iob_conf:
    """Py2HWSW's internal implementation of 'iob_conf' API class."""

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Every conf must have a name!")
        if self.kind not in ["P", "M", "C", "D"]:
            fail_with_msg(
                f"Conf '{self.name}' type must be either P (Parameter), M (Macro), C (Constant) or D (Derived Parameter)!"
            )

        try:
            value = int(self.value)
            min_value = int(self.min_value)
            max_value = int(self.max_value)
            if value < min_value or value > max_value:
                fail_with_msg(
                    f"Conf '{self.name}' value '{value}' must be between {min_value} and {max_value}!"
                )
        except ValueError:
            pass


#
# API methods
#


def conf_from_dict(conf_dict):
    return iob_conf(**conf_dict)


def conf_text2dict(conf_text: str) -> dict:
    # parse conf text into a dictionary
    conf_text_flags = [
        "name",
        ["-t", {"dest": "kind"}],
        ["-v", {"dest": "value"}],
        ["-m", {"dest": "min_value"}],
        ["-M", {"dest": "max_value"}],
        ["-d", {"dest": "descr", "nargs": "?"}],
        ["-doc", {"dest": "doc_only", "action": "store_true"}],
    ]
    return parse_short_notation_text(conf_text, conf_text_flags)


def conf_from_text(conf_text: str) -> iob_conf:
    return conf_from_dict(conf_text2dict(conf_text))
