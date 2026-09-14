# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


def setup(py_params_dict):
    """IOb bus error responder for unmapped slave slots.

    Used by IOb bus splits (iob_split) to answer transactions that target
    unmapped addresses. It mirrors the timing of a real IOb CSR (registered
    ready/rvalid one cycle after valid), so the bus split finishes the
    transaction instead of hanging forever.

    Responds with ready for writes and with rvalid (zero data) for reads.
    """

    attributes_dict = {
        "generate_hw": True,
        #
        # IOb Parameters
        #
        "confs": [
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "64",
                "descr": "IOb address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "8",
                "max": "1024",
                "descr": "IOb data bus width",
            },
        ],
        #
        # Ports
        #
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable, async and synchronous reset",
            },
            {
                "name": "s_s",
                "descr": "Subordinate IOb interface",
                "signals": {
                    "type": "iob",
                    "prefix": "s_",
                    "DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                },
            },
        ],
        #
        # Snippets
        #
        "snippets": [
            {
                "verilog_code": f"""
   // Capture the valid transaction and respond one cycle later so the bus
   // split FSM completes the transaction instead of hanging. This mirrors
   // the timing of a real IOb CSR (registered ready/rvalid).
   reg req_r;
   reg wstrb_r;

   always @(posedge clk_i) begin
      if (rst_i) begin
         req_r   <= 1'b0;
         wstrb_r <= 1'b0;
      end else begin
         req_r   <= s_iob_valid_i;
         wstrb_r <= s_iob_wstrb_i;
      end
   end

   assign s_iob_ready_o  = req_r;
   assign s_iob_rvalid_o = req_r & ~wstrb_r;
   assign s_iob_rdata_o  = {{DATA_W{{1'b0}}}};
""",
            },
        ],
    }

    return attributes_dict
