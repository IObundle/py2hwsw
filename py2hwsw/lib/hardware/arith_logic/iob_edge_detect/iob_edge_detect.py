# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "EDGE_TYPE",
                "descr": "Edge detection type. Options: "rising", "falling", "both"",
                "type": "P",
                "val": '"rising"',
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "OUT_TYPE",
                "descr": "Output type. Options: "step", "pulse"",
                "type": "P",
                "val": '"step"',
                "min": "NA",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "bit_i",
                "descr": "",
                "signals": [
                    {"name": "bit_i", "width": 1},
                ],
            },
            {
                "name": "detected_o",
                "descr": "",
                "signals": [
                    {"name": "detected_o", "width": 1},
                ],
            },
        ],
        "wires": [
            {
                "name": "bit_int",
                "descr": "Internal bit wire",
                "signals": [
                    {"name": "bit_int", "width": "1", "descr": "Internal bit signal"},
                ],
            },
            {
                "name": "bit_int_q",
                "descr": "Internal bit wire with delay",
                "signals": [
                    {
                        "name": "bit_int_q",
                        "width": "1",
                        "descr": "Internal bit signal with delay",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instantiate": False,
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": r"""
                generate
    if (EDGE_TYPE == "falling") begin : gen_falling
      assign bit_int = ~bit_i;
      iob_reg_car #(
          .DATA_W (1),
          .RST_VAL(1'b0)
      ) bit_reg (
          `include "iob_edge_detect_iob_clk_s_s_portmap.vs"
          .data_i(bit_int),
          .data_o(bit_int_q)
      );

    end else begin : gen_default_rising
      assign bit_int = bit_i;

      iob_reg_car #(
          .DATA_W (1),
          .RST_VAL(1'b1)
      ) bit_reg (
          `include "iob_edge_detect_iob_clk_s_s_portmap.vs"
          .data_i(bit_int),
          .data_o(bit_int_q)
      );
    end
  endgenerate

  generate
    if (OUT_TYPE == "pulse") begin : gen_pulse
      assign detected_o = bit_int & ~bit_int_q;
    end else begin : gen_step
      wire detected_prev;
      iob_reg_car #(
          .DATA_W(1)
      ) detected_reg (
          `include "iob_edge_detect_iob_clk_s_s_portmap.vs"
          .data_i(detected_o),
          .data_o(detected_prev)
      );
      assign detected_o = detected_prev | (bit_int & ~bit_int_q);
    end
  endgenerate
                """
            }
        ],
    }

    return attributes_dict
