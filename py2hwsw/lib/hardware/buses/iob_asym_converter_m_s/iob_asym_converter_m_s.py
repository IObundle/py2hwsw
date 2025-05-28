# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            # Parameters
            {
                "name": "M_DATA_W",
                "descr": "Manager interface data width",
                "type": "P",
                "val": 21,
                "min": 1,
                "max": "NA",
            },
            {
                "name": "S_DATA_W",
                "descr": "Subordinate interface data width",
                "type": "P",
                "val": 21,
                "min": 1,
                "max": "NA",
            },
            {
                "name": "ADDR_W",
                "descr": "Higest ADDR_W (the one with lower DATA_W).",
                "type": "P",
                "val": 3,
                "min": 1,
                "max": "NA",
            },
            # Derived parameters
            # determine W_ADDR_W and R_ADDR_W
            {"name": "MAXDATA_W", "type": "D", "val": "iob_max(W_DATA_W, R_DATA_W)"},
            {"name": "MINDATA_W", "type": "D", "val": "iob_min(W_DATA_W, R_DATA_W)"},
            {"name": "R", "type": "D", "val": "MAXDATA_W / MINDATA_W"},
            {
                "name": "MINADDR_W",
                "type": "D",
                "val": "ADDR_W - $clog2(R)",
                "descr": "Lowest ADDR_W (the one with higher DATA_W).",
            },
            {
                "name": "M_ADDR_W",
                "type": "D",
                "val": "(M_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
            },
            {
                "name": "S_ADDR_W",
                "type": "D",
                "val": "(S_DATA_W == MAXDATA_W) ? MINADDR_W : ADDR_W",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {
                    "type": "iob_clk",
                },
            },
            {
                "name": "m_io",
                "descr": "Manager interface",
                "signals": [
                    {"name": "m_en_o", "width": 1},
                    {"name": "m_wstrb_o", "width": "M_DATA_W/8"},
                    {"name": "m_addr_o", "width": "M_ADDR_W"},
                    {"name": "m_d_o", "width": "M_DATA_W"},
                    {"name": "m_d_i", "width": "M_DATA_W"},
                ],
            },
            {
                "name": "s_io",
                "descr": "Subordinate interface",
                "signals": [
                    {"name": "s_en_i", "width": 1},
                    {"name": "s_wstrb_i", "width": "S_DATA_W/8"},
                    {"name": "s_addr_i", "width": "S_ADDR_W"},
                    {"name": "s_d_i", "width": "S_DATA_W"},
                    {"name": "s_d_o", "width": "S_DATA_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_functions",
                "instance_description": "Functions used for math calculations in derived parameters.",
                "instantiate": False,
            },
        ],
        # TODO: Instantiate iob_regs of FSM in g_subordinate_larger_dat
        "snippets": [
            {
                "verilog_code": """
   generate
      if (M_DATA_W >= S_DATA_W) begin : g_manager_larger_dat
         // Manager has larger data width.
         // Converter can use purely combinatorial logic (works with regarrays).
         integer align_bits = (s_addr_i%R) * (M_DATA_W/R);
         assign m_en_o = s_en_i;
         assign m_wstrb_o = s_wstrb_i<<(align_bits/8);
         assign m_addr_o = s_addr_i/R;
         assign m_d_o = (s_d_i<<align_bits) | M_DATA_W'd0;
         assign s_d_o = m_d_i[align_bits+:S_DATA_W];
      end else begin : g_subordinate_larger_dat
         // Subordinate has larger data width.
         // Logic must perform multiple steps to fill word sent/received in subordinate interface (not useful for regarrays since output will be registered).

         //FSM states
         localparam IDLE = 'd0;
         localparam WRITE_WORD = 'd1;
         localparam READ_WORD = 'd2;

         always @* begin
            state_nxt = state;
            word_count_nxt = word_count;

            case(state)
                IDLE: begin // Idle state
                    if (s_en_i != 0) begin // If there's data to process
                        // FIXME: We probably need a ready (and/or rvalid) signal to tell the manager when the transaction completes
                        if (|s_wstrb_i != 0) // Write to manager
                            state_nxt = WRITE_WORD;
                        else // Read from manager
                            state_nxt = READ_WORD;
                    end
                end
                WRITE_WORD: begin // Extract word from subordinate and write to manager
                    // FIXME: 
                     assign m_wstrb_o = s_wstrb_i<<(align_bits/8);
                     assign m_addr_o = s_addr_i/R;
                     assign m_d_o = (s_d_i<<align_bits) | M_DATA_W'd0;
                     if not all_subordinate_words_sent:
                        word_count_nxt = word_count + 1;
                     else:
                        // Transaction complete. Sent all data from subordinate word to manager.
                        state_nxt = IDLE;
                end
                READ_WORD: begin // Read word from subordinate and fill it in manager
                    // FIXME: 
                     assign m_wstrb_o = 'd0;
                     assign m_addr_o = s_addr_i*R + word_count;
                     assign m_d_o = 'd0;
                     assign s_d_o = m_d_i[align_bits+:S_DATA_W];
                     if not subordinate_word not yet filled:
                        word_count_nxt = word_count + 1;
                     else:
                        // Transaction complete. Subordinate word is filled with data from manager.
                        state_nxt = IDLE;
                end
            endcase
         end
      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
