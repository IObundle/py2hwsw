# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
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
            {"name": "MAXDATA_W", "type": "D", "val": "iob_max(M_DATA_W, S_DATA_W)"},
            {"name": "MINDATA_W", "type": "D", "val": "iob_min(M_DATA_W, S_DATA_W)"},
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
                "wires": {
                    "type": "iob_clk",
                },
            },
            {
                "name": "m_io",
                "descr": "Manager interface",
                "wires": [
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
                "wires": [
                    {"name": "s_en_i", "width": 1},
                    {"name": "s_wstrb_i", "width": "S_DATA_W/8"},
                    {"name": "s_addr_i", "width": "S_ADDR_W"},
                    {"name": "s_d_i", "width": "S_DATA_W"},
                    {"name": "s_d_o", "width": "S_DATA_W"},
                    {"name": "s_ready_o", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_functions",
                "instance_description": "Functions used for math calculations in derived parameters.",
                "instantiate": False,
            },
            {
                "core_name": "iob_reg",
                "port_params": {"clk_en_rst_s": "c_a"},
                "instantiate": False,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   `include "iob_functions.vs"

   generate
      if (M_DATA_W >= S_DATA_W) begin : g_manager_larger_dat
         // Manager has larger data width.
         // Converter can use purely combinatorial logic (works with regarrays).
         integer align_bits = (s_addr_i%R) * (M_DATA_W/R);

         assign m_en_o = s_en_i;
         assign m_wstrb_o = s_wstrb_i<<(align_bits/8);
         assign m_addr_o = s_addr_i/R;
         assign m_d_o = (s_d_i<<align_bits) | {M_DATA_W{1'b0}};
         assign s_d_o = m_d_i[align_bits+:S_DATA_W];
         assign s_ready_o = 1;
      end else begin : g_subordinate_larger_dat
         // Subordinate has larger data width.
         // Logic must perform multiple steps to fill word sent/received in subordinate interface (not useful for regarrays since output will be registered).

         //FSM states
         localparam IDLE = 'd0;
         localparam WRITE_WORD = 'd1;
         localparam READ_WORD = 'd2;

         localparam M_WSTRB_W = M_DATA_W/8;

         reg [M_ADDR_W-1:0] current_manager_address;
         integer align_bits;

         // FSM regs
         wire [2-1:0] state;
         reg [2-1:0] state_nxt;
         wire [R:0] word_count;
         reg [R:0] word_count_nxt;

         // Create regs for ports
         reg [1-1:0] m_en_int;
         assign m_en_o = m_en_int;
         reg [(M_DATA_W/8)-1:0] m_wstrb_int;
         assign m_wstrb_o = m_wstrb_int;
         reg [M_ADDR_W-1:0] m_addr_int;
         assign m_addr_o = m_addr_int;
         reg [M_DATA_W-1:0] m_d_int;
         assign m_d_o = m_d_int;

         reg [S_DATA_W-1:0] s_d_int;
         assign s_d_o = s_d_int;
         reg [1-1:0] s_ready_int;
         assign s_ready_o = s_ready_int;


         always @* begin
            state_nxt = state;
            word_count_nxt = 'd0;

            m_en_int = 0;
            m_wstrb_int = 0;
            m_addr_int = 0;
            m_d_int = 0;

            s_d_int = 0;
            s_ready_int = 0;

            case(state)
                IDLE: begin // Idle state
                    if (s_en_i != 0) begin // If there's data to process
                        if (|s_wstrb_i != 0) // Write to manager
                            state_nxt = WRITE_WORD;
                        else // Read from manager
                            state_nxt = READ_WORD;
                    end
                end
                WRITE_WORD: begin // Extract word from subordinate and write to manager
                     current_manager_address = s_addr_i*R + word_count;
                     align_bits = (current_manager_address%R) * (S_DATA_W/R);

                     // Extract partial word of subordinate and send it to manager
                     m_en_int = 1;
                     m_wstrb_int = s_wstrb_i[align_bits/8+:M_WSTRB_W];
                     m_addr_int = current_manager_address;
                     m_d_int = s_d_i[align_bits+:M_DATA_W];

                     if (word_count < R-1) begin
                        word_count_nxt = word_count + 1;
                     end else begin
                        // Transaction complete. Sent all data from subordinate word to manager.
                        state_nxt = IDLE;
                        s_ready_int = 1;
                     end
                end
                READ_WORD: begin // Read word from subordinate and fill it in manager
                     current_manager_address = s_addr_i*R + word_count;
                     align_bits = (current_manager_address%R) * (S_DATA_W/R);

                     // Fill partial word of subordinate with data from manager
                     m_en_int = 1;
                     m_wstrb_int = 'd0;
                     m_addr_int = current_manager_address;
                     m_d_int = 'd0;
                     s_d_int[align_bits+:M_DATA_W] = m_d_i;

                     if (word_count < R-1) begin
                        word_count_nxt = word_count + 1;
                     end else begin
                        // Transaction complete. Subordinate word is filled with data from manager.
                        state_nxt = IDLE;
                        s_ready_int = 1;
                     end
                end
            endcase
         end

         // word count register
         iob_reg_ca #(
            .DATA_W (R+1),
            .RST_VAL('d0)
         ) word_count_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
            .clk_i (clk_i),
            .cke_i (cke_i),
            .arst_i(arst_i),
            // data_i port: Data input
            .data_i(word_count_nxt),
            // data_o port: Data output
            .data_o(word_count)
         );

         // state register
         iob_reg_ca #(
            .DATA_W (2),
            .RST_VAL(1'b0)
         ) state_reg (
            // clk_en_rst_s port: Clock, clock enable and reset
            .clk_i (clk_i),
            .cke_i (cke_i),
            .arst_i(arst_i),
            // data_i port: Data input
            .data_i(state_nxt),
            // data_o port: Data output
            .data_o(state)
         );

      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
