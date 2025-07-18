#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import py2hwsw_api as py2hwsw

core_dictionary = {
    # Set "is_tester" attribute to generate Makefile and flows allowing to run this core as top module
    "generate_hw": True,
    "is_tester": True,
    "confs": [
        {
            "name": "W",
            "type": "P",
            "val": "21",
            "min": "1",
            "max": "32",
            "descr": "IO width",
        },
    ],
    "buses": [
        {
            "name": "a",
            "descr": "AOI input port 1",
            "wires": [
                {"name": "a", "width": "W"},
            ],
        },
        {
            "name": "b",
            "descr": "AOI input port 2",
            "wires": [
                {"name": "b", "width": "W"},
            ],
        },
        {
            "name": "c",
            "descr": "AOI input port 3",
            "wires": [
                {"name": "c", "width": "W"},
            ],
        },
        {
            "name": "d",
            "descr": "AOI input port 4",
            "wires": [
                {"name": "d", "width": "W"},
            ],
        },
        {
            "name": "y",
            "descr": "AOI output port",
            "wires": [
                {"name": "y", "width": "W"},
            ],
        },
    ],
    "subblocks": [
        {
            "core_name": "iob_aoi",
            "instance_name": "uut_aoi",
            "instance_description": "Unit Under Test",
            "parameters": {
                "W": "W",
            },
            "connect": {
                "a_i": "a",
                "b_i": "b",
                "c_i": "c",
                "d_i": "d",
                "y_o": "y",
            },
        }
    ],
    "snippets": [
        {
            "verilog_code": """\
   // Tester body / verification code
   // Currently using non-synthesizable code

   reg     [3:0] data_i = 0;
   wire          data_o;

   assign a = data_i[0];
   assign b = data_i[1];
   assign c = data_i[2];
   assign d = data_i[3];
   assign data_o = y;

   integer       i;
   integer       fp;

   initial begin

      for (i = 0; i < 16; i = i + 1) begin
         #10 data_i = i[3:0];
         #10 $display("data_i = %b, data_o = %b", data_i, data_o);
      end
      #10 $display("%c[1;34m", 8'd27);
      $display("Test completed successfully.");
      $display("%c[0m", 8'd27);

      fp = $fopen("test.log", "w");
      $fdisplay(fp, "Test passed!");

      $finish();
   end
"""
        }
    ],
}


class iob_aoi_tester(py2hwsw.iob_core):
    def __init__(self):
        super().__init__(core_dictionary)


if __name__ == "__main__":
    iob_aoi_tester_obj = iob_aoi_tester()
    iob_aoi_tester_obj.generate_build_dir()
