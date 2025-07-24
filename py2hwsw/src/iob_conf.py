# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from iob_base import fail_with_msg, parse_short_notation_text


@dataclass
class iob_conf:
    """
    Class to represent a configuration option.

    Attributes:
        name (str): Configuration identifier name.
        kind (str): Configuration type:
                    M: Verilog macro; the IP final user may redefine this macro, affecting all instances of the core.
                    C: Verilog derived or constant macro; the IP final user may not redefine this macro.
                    P: Verilog parameter; the IP final user may redefine this parameter for each instance of the core.
                    D: Verilog derived or constant parameter; the IP final user may not redefine this parameter.
                    L: Verilog local parameter; the IP final user may not redefine this parameter.
        value (str | int | bool): Configuration value.
        min_value (str | int): Minimum value supported by the configuration option (NA if not applicable).
        max_value (str | int): Maximum value supported by the configuration option (NA if not applicable).
        descr (str): Description of the configuration option.
        doc_only (bool): If enabled, configuration option will only appear in documentation. Not in the verilog code.
    """

    name: str = ""
    kind: str = "P"
    value: str | int | bool = ""
    min_value: str | int = "NA"
    max_value: str | int = "NA"
    descr: str = "Default description"
    doc_only: bool = False

    def validate_attributes(self):
        if not self.name:
            fail_with_msg("Every conf must have a name!")
        if self.kind not in ["P", "M", "C", "D", "L"]:
            fail_with_msg(
                f"Conf '{self.name}' type must be either P (Parameter), M (Macro), C (Constant), D (Derived Parameter), or L (Local Parameter)!"
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
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_conf_from_dict(conf_dict):
        """
        Function to create iob_conf object from dictionary attributes.

        Attributes:
            conf_dict (dict): dictionary with values to initialize attributes of iob_conf object.
                This dictionary supports the following keys corresponding to the iob_conf attributes:
                - name           -> iob_conf.name
                - kind           -> iob_conf.kind
                - value          -> iob_conf.value
                - min_value      -> iob_conf.min_value
                - max_value      -> iob_conf.max_value
                - descr          -> iob_conf.descr
                - doc_only       -> iob_conf.doc_only

        Returns:
            iob_conf: iob_conf object
        """
        return iob_conf(**conf_dict)

    @staticmethod
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

    @staticmethod
    def create_conf_from_text(conf_text):
        """
        Function to create iob_conf object from short notation text.

        Attributes:
            conf_text (str): Short notation text. Object attributes are specified using the following format:
                name [-t kind] [-v value] [-m min_value] [-M max_value] [-doc]
                [-d descr]
                Example:
                    DATA_W -t P -v 32 -m NA -M NA
                    -d 'Data bus width'

        Returns:
            iob_conf: iob_conf object
        """
        return __class__.create_conf_from_dict(__class__.conf_text2dict(conf_text))
