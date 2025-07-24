#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

core_dictionary = {
    "generate_hw": True,
    "confs": [
        """
            W -t P -v 1 -m 1 -M 32
            -d 'Ports width'
            """
    ],
    "ports": [
        """
            a_i -s a_i:W
            -d 'Input port a'

            b_i -s b_i:W
            -d 'Input port b'

            c_i -s c_i:W
            -d 'Input port c'

            d_i -s d_i:W
            -d 'Input port d'

            y_o -s y_o:W
            -d 'Output port y'
        """
    ],
    "buses": [
        """
            and_ab_out -s aab:W
            -d 'and ab output'

            and_cd_out -s cad:W
            -d 'and cd output'

            or_out -s oab:1
            -d 'or output'
            """,
    ],
    "subblocks": [
        """
            iob_and iob_and_ab -p W:W -c
            a_i:a_i
            b_i:b_i
            y_o:and_ab_out
            -d 'First and gate'

            iob_and io_and_cd -p W:W -c
            a_i:c_i
            b_i:d_i
            y_o:and_cd_out
            -d 'Second and gate'

            iob_or iob_or_abcd -p W:W -c
            a_i:and_ab_out
            b_i:and_cd_out
            y_o:or_out
            -d 'Or gate'

            iob_inv iob_inv_out -p W:W -c
            a_i:or_out
            y_o:y_o
            -d 'Inverter'
            """,
    ],
    "superblocks": [
        # Tester
        {
            "core_name": "iob_aoi_tester",
            "name": "iob_tester",
            "dest_dir": "tester",
        },
    ],
}


class iob_aoi_short(iob_core):
    def __init__(self, width=None):
        if width:
            core_dictionary["confs"][0]["value"] = str(width)
        print("iob_aoi constructor called.")
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_aoi_short_obj = iob_aoi_short(width=1)
    iob_aoi_short_obj.generate_build_dir()
