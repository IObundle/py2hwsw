# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


def setup(py_params_dict):
    """AXI4 subordinate that terminates every transaction with a DECERR
    response.

    Used by AXI interconnects (iob_axi_split) to answer requests that target
    unmapped addresses. Without it, an unmapped request is left unanswered and
    the requesting manager stalls forever (silent deadlock), which can freeze
    the whole SoC (e.g. a CPU speculative fetch into an unmapped region).
    """

    attributes_dict = {
        "generate_hw": True,
        #
        # AXI Parameters
        #
        "confs": [
            {
                "name": "ID_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "AXI ID bus width",
            },
            {
                "name": "LEN_W",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "32",
                "descr": "AXI LEN bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "64",
                "descr": "AXI address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "8",
                "max": "1024",
                "descr": "AXI data bus width",
            },
            {
                "name": "SIZE_W",
                "type": "P",
                "val": "3",
                "min": "1",
                "max": "8",
                "descr": "AXI size bus width",
            },
            {
                "name": "BURST_W",
                "type": "P",
                "val": "2",
                "min": "1",
                "max": "8",
                "descr": "AXI burst bus width",
            },
            {
                "name": "LOCK_W",
                "type": "P",
                "val": "2",
                "min": "1",
                "max": "8",
                "descr": "AXI lock bus width",
            },
            {
                "name": "CACHE_W",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "8",
                "descr": "AXI cache bus width",
            },
            {
                "name": "QOS_W",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "8",
                "descr": "AXI qos bus width",
            },
            {
                "name": "RESP_W",
                "type": "P",
                "val": "2",
                "min": "1",
                "max": "8",
                "descr": "AXI response bus width",
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
                "descr": "Subordinate AXI interface",
                "signals": {
                    "type": "axi",
                    "prefix": "s_",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                    "ID_W": "ID_W",
                    "SIZE_W": "SIZE_W",
                    "BURST_W": "BURST_W",
                    "LOCK_W": "LOCK_W",
                    "CACHE_W": "CACHE_W",
                    "QOS_W": "QOS_W",
                    "RESP_W": "RESP_W",
                    "LEN_W": "LEN_W",
                },
            },
        ],
        #
        # Snippets
        #
        "snippets": [
            {
                "verilog_code": f"""
   // DECERR (decode error) response value: all response bits set.
   localparam [RESP_W-1:0] DECERR_RESP = {{RESP_W{{1'b1}}}};

   //
   // Read
   //
   // Accept a single AR at a time and respond with a full burst of
   // DECERR beats (arlen+1 beats, rlast on the final beat) so the
   // master's read transaction completes spec-compliantly instead
   // of stalling on early burst termination.
   reg             rd_busy;
   reg [ ID_W-1:0] rd_id;
   reg [LEN_W-1:0] rd_cnt_r;

   always @(posedge clk_i) begin
      if (rst_i) begin
         rd_busy   <= 1'b0;
         rd_id     <= {{ID_W{{1'b0}}}};
         rd_cnt_r  <= {{LEN_W{{1'b0}}}};
      end else begin
         if (s_axi_arvalid_i & s_axi_arready_o) begin
            rd_busy  <= 1'b1;
            rd_id    <= s_axi_arid_i;
            rd_cnt_r <= s_axi_arlen_i;
         end else if (s_axi_rvalid_o & s_axi_rready_i) begin
            if (rd_cnt_r == 0) begin
               rd_busy  <= 1'b0;
               rd_cnt_r <= {{LEN_W{{1'b0}}}};
            end else begin
               rd_cnt_r <= rd_cnt_r - 1'b1;
            end
         end
      end
   end

   assign s_axi_arready_o = ~rd_busy;
   assign s_axi_rvalid_o  = rd_busy;
   assign s_axi_rid_o     = rd_id;
   assign s_axi_rdata_o   = {{DATA_W{{1'b0}}}};
   assign s_axi_rresp_o   = DECERR_RESP;
   assign s_axi_rlast_o   = (rd_cnt_r == 0) & rd_busy;

   //
   // Write channel
   //
   // Accept a single AW at a time, absorb all beats of its W burst, then
   // respond with a DECERR B.
   reg             wr_busy;
   reg             wr_last_seen;
   reg [ID_W-1:0] wr_id;

   always @(posedge clk_i) begin
      if (rst_i) begin
         wr_busy      <= 1'b0;
         wr_last_seen <= 1'b0;
         wr_id        <= {{ID_W{{1'b0}}}};
      end else begin
         if (s_axi_awvalid_i & s_axi_awready_o) begin
            wr_busy <= 1'b1;
            wr_id   <= s_axi_awid_i;
         end

         if (s_axi_wvalid_i & s_axi_wready_o & s_axi_wlast_i) begin
            wr_last_seen <= 1'b1;
         end

         if (s_axi_bvalid_o & s_axi_bready_i) begin
            wr_busy      <= 1'b0;
            wr_last_seen <= 1'b0;
         end
      end
   end

   assign s_axi_awready_o = ~wr_busy;
   assign s_axi_wready_o  = wr_busy;
   assign s_axi_bvalid_o  = wr_busy & wr_last_seen;
   assign s_axi_bid_o     = wr_id;
   assign s_axi_bresp_o   = DECERR_RESP;
""",
            },
        ],
    }

    return attributes_dict
