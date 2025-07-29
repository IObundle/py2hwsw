# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass


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

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(conf_dict):
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
