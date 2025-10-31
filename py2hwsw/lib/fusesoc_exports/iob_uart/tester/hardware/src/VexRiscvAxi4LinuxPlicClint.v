// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

// Generator : SpinalHDL v1.9.3    git head : 029104c77a54c53f1edda327a3bea333f7d65fd9
// Component : VexRiscvAxi4LinuxPlicClint
// Git hash  : 5ef1bc775fdbe942875dd7906f22aa98e6cffaaf

`timescale 1ns / 1ps

module VexRiscvAxi4LinuxPlicClint (
   input         clint_awvalid,
   output        clint_awready,
   input  [15:0] clint_awaddr,
   input  [ 2:0] clint_awprot,
   input         clint_wvalid,
   output        clint_wready,
   input  [31:0] clint_wdata,
   input  [ 3:0] clint_wstrb,
   output        clint_bvalid,
   input         clint_bready,
   output [ 1:0] clint_bresp,
   input         clint_arvalid,
   output        clint_arready,
   input  [15:0] clint_araddr,
   input  [ 2:0] clint_arprot,
   output        clint_rvalid,
   input         clint_rready,
   output [31:0] clint_rdata,
   output [ 1:0] clint_rresp,
   input         plic_awvalid,
   output        plic_awready,
   input  [21:0] plic_awaddr,
   input  [ 2:0] plic_awprot,
   input         plic_wvalid,
   output        plic_wready,
   input  [31:0] plic_wdata,
   input  [ 3:0] plic_wstrb,
   output        plic_bvalid,
   input         plic_bready,
   output [ 1:0] plic_bresp,
   input         plic_arvalid,
   output        plic_arready,
   input  [21:0] plic_araddr,
   input  [ 2:0] plic_arprot,
   output        plic_rvalid,
   input         plic_rready,
   output [31:0] plic_rdata,
   output [ 1:0] plic_rresp,
   input  [31:0] plicInterrupts,
   input  [31:0] externalResetVector,
   input  [31:0] ioStartAddr,
   input  [31:0] ioSize,
   output        iBusAxi_arvalid,
   input         iBusAxi_arready,
   output [31:0] iBusAxi_araddr,
   output [ 0:0] iBusAxi_arid,
   output [ 3:0] iBusAxi_arregion,
   output [ 7:0] iBusAxi_arlen,
   output [ 2:0] iBusAxi_arsize,
   output [ 1:0] iBusAxi_arburst,
   output [ 0:0] iBusAxi_arlock,
   output [ 3:0] iBusAxi_arcache,
   output [ 3:0] iBusAxi_arqos,
   output [ 2:0] iBusAxi_arprot,
   input         iBusAxi_rvalid,
   output        iBusAxi_rready,
   input  [31:0] iBusAxi_rdata,
   input  [ 0:0] iBusAxi_rid,
   input  [ 1:0] iBusAxi_rresp,
   input         iBusAxi_rlast,
   output        dBusAxi_awvalid,
   input         dBusAxi_awready,
   output [31:0] dBusAxi_awaddr,
   output [ 0:0] dBusAxi_awid,
   output [ 3:0] dBusAxi_awregion,
   output [ 7:0] dBusAxi_awlen,
   output [ 2:0] dBusAxi_awsize,
   output [ 1:0] dBusAxi_awburst,
   output [ 0:0] dBusAxi_awlock,
   output [ 3:0] dBusAxi_awcache,
   output [ 3:0] dBusAxi_awqos,
   output [ 2:0] dBusAxi_awprot,
   output        dBusAxi_wvalid,
   input         dBusAxi_wready,
   output [31:0] dBusAxi_wdata,
   output [ 3:0] dBusAxi_wstrb,
   output        dBusAxi_wlast,
   input         dBusAxi_bvalid,
   output        dBusAxi_bready,
   input  [ 0:0] dBusAxi_bid,
   input  [ 1:0] dBusAxi_bresp,
   output        dBusAxi_arvalid,
   input         dBusAxi_arready,
   output [31:0] dBusAxi_araddr,
   output [ 0:0] dBusAxi_arid,
   output [ 3:0] dBusAxi_arregion,
   output [ 7:0] dBusAxi_arlen,
   output [ 2:0] dBusAxi_arsize,
   output [ 1:0] dBusAxi_arburst,
   output [ 0:0] dBusAxi_arlock,
   output [ 3:0] dBusAxi_arcache,
   output [ 3:0] dBusAxi_arqos,
   output [ 2:0] dBusAxi_arprot,
   input         dBusAxi_rvalid,
   output        dBusAxi_rready,
   input  [31:0] dBusAxi_rdata,
   input  [ 0:0] dBusAxi_rid,
   input  [ 1:0] dBusAxi_rresp,
   input         dBusAxi_rlast,
   input         clk,
   input         reset
);
   localparam ShiftCtrlEnum_DISABLE_1 = 2'd0;
   localparam ShiftCtrlEnum_SLL_1 = 2'd1;
   localparam ShiftCtrlEnum_SRL_1 = 2'd2;
   localparam ShiftCtrlEnum_SRA_1 = 2'd3;
   localparam EnvCtrlEnum_NONE = 3'd0;
   localparam EnvCtrlEnum_XRET = 3'd1;
   localparam EnvCtrlEnum_WFI = 3'd2;
   localparam EnvCtrlEnum_ECALL = 3'd3;
   localparam EnvCtrlEnum_EBREAK = 3'd4;
   localparam BranchCtrlEnum_INC = 2'd0;
   localparam BranchCtrlEnum_B = 2'd1;
   localparam BranchCtrlEnum_JAL = 2'd2;
   localparam BranchCtrlEnum_JALR = 2'd3;
   localparam AluBitwiseCtrlEnum_XOR_1 = 2'd0;
   localparam AluBitwiseCtrlEnum_OR_1 = 2'd1;
   localparam AluBitwiseCtrlEnum_AND_1 = 2'd2;
   localparam Src2CtrlEnum_RS = 2'd0;
   localparam Src2CtrlEnum_IMI = 2'd1;
   localparam Src2CtrlEnum_IMS = 2'd2;
   localparam Src2CtrlEnum_PC = 2'd3;
   localparam AluCtrlEnum_ADD_SUB = 2'd0;
   localparam AluCtrlEnum_SLT_SLTU = 2'd1;
   localparam AluCtrlEnum_BITWISE = 2'd2;
   localparam Src1CtrlEnum_RS = 2'd0;
   localparam Src1CtrlEnum_IMU = 2'd1;
   localparam Src1CtrlEnum_PC_INCREMENT = 2'd2;
   localparam Src1CtrlEnum_URS1 = 2'd3;
   localparam MmuPlugin_shared_State_IDLE = 3'd0;
   localparam MmuPlugin_shared_State_L1_CMD = 3'd1;
   localparam MmuPlugin_shared_State_L1_RSP = 3'd2;
   localparam MmuPlugin_shared_State_L0_CMD = 3'd3;
   localparam MmuPlugin_shared_State_L0_RSP = 3'd4;

   wire [30:0] plicCtrl_io_sources;
   wire        IBusCachedPlugin_cache_io_flush;
   wire        IBusCachedPlugin_cache_io_cpu_prefetch_isValid;
   wire        IBusCachedPlugin_cache_io_cpu_fetch_isValid;
   wire        IBusCachedPlugin_cache_io_cpu_fetch_isStuck;
   wire        IBusCachedPlugin_cache_io_cpu_fetch_isRemoved;
   wire        IBusCachedPlugin_cache_io_cpu_decode_isValid;
   wire        IBusCachedPlugin_cache_io_cpu_decode_isStuck;
   wire        IBusCachedPlugin_cache_io_cpu_decode_isUser;
   reg         IBusCachedPlugin_cache_io_cpu_fill_valid;
   reg         dataCache_1_io_cpu_execute_isValid;
   reg  [31:0] dataCache_1_io_cpu_execute_address;
   reg         dataCache_1_io_cpu_execute_args_wr;
   reg  [ 1:0] dataCache_1_io_cpu_execute_args_size;
   reg         dataCache_1_io_cpu_execute_args_isLrsc;
   wire        dataCache_1_io_cpu_execute_args_amoCtrl_swap;
   wire [ 2:0] dataCache_1_io_cpu_execute_args_amoCtrl_alu;
   reg         dataCache_1_io_cpu_memory_isValid;
   wire [31:0] dataCache_1_io_cpu_memory_address;
   reg         dataCache_1_io_cpu_memory_mmuRsp_isIoAccess;
   reg         dataCache_1_io_cpu_writeBack_isValid;
   wire        dataCache_1_io_cpu_writeBack_isUser;
   wire [31:0] dataCache_1_io_cpu_writeBack_storeData;
   wire [31:0] dataCache_1_io_cpu_writeBack_address;
   wire        dataCache_1_io_cpu_writeBack_fence_SW;
   wire        dataCache_1_io_cpu_writeBack_fence_SR;
   wire        dataCache_1_io_cpu_writeBack_fence_SO;
   wire        dataCache_1_io_cpu_writeBack_fence_SI;
   wire        dataCache_1_io_cpu_writeBack_fence_PW;
   wire        dataCache_1_io_cpu_writeBack_fence_PR;
   wire        dataCache_1_io_cpu_writeBack_fence_PO;
   wire        dataCache_1_io_cpu_writeBack_fence_PI;
   wire [ 3:0] dataCache_1_io_cpu_writeBack_fence_FM;
   wire        dataCache_1_io_cpu_flush_valid;
   wire        dataCache_1_io_cpu_flush_payload_singleLine;
   wire [ 5:0] dataCache_1_io_cpu_flush_payload_lineId;
   reg  [31:0] _zz_RegFilePlugin_regFile_port0;
   reg  [31:0] _zz_RegFilePlugin_regFile_port1;
   wire        clintCtrl_io_bus_aw_ready;
   wire        clintCtrl_io_bus_w_ready;
   wire        clintCtrl_io_bus_b_valid;
   wire [ 1:0] clintCtrl_io_bus_b_payload_resp;
   wire        clintCtrl_io_bus_ar_ready;
   wire        clintCtrl_io_bus_r_valid;
   wire [31:0] clintCtrl_io_bus_r_payload_data;
   wire [ 1:0] clintCtrl_io_bus_r_payload_resp;
   wire [ 0:0] clintCtrl_io_timerInterrupt;
   wire [ 0:0] clintCtrl_io_softwareInterrupt;
   wire [63:0] clintCtrl_io_time;
   wire        plicCtrl_io_bus_aw_ready;
   wire        plicCtrl_io_bus_w_ready;
   wire        plicCtrl_io_bus_b_valid;
   wire [ 1:0] plicCtrl_io_bus_b_payload_resp;
   wire        plicCtrl_io_bus_ar_ready;
   wire        plicCtrl_io_bus_r_valid;
   wire [31:0] plicCtrl_io_bus_r_payload_data;
   wire [ 1:0] plicCtrl_io_bus_r_payload_resp;
   wire [ 1:0] plicCtrl_io_targets;
   wire        IBusCachedPlugin_cache_io_cpu_prefetch_haltIt;
   wire [31:0] IBusCachedPlugin_cache_io_cpu_fetch_data;
   wire [31:0] IBusCachedPlugin_cache_io_cpu_fetch_physicalAddress;
   wire        IBusCachedPlugin_cache_io_cpu_decode_error;
   wire        IBusCachedPlugin_cache_io_cpu_decode_mmuRefilling;
   wire        IBusCachedPlugin_cache_io_cpu_decode_mmuException;
   wire [31:0] IBusCachedPlugin_cache_io_cpu_decode_data;
   wire        IBusCachedPlugin_cache_io_cpu_decode_cacheMiss;
   wire [31:0] IBusCachedPlugin_cache_io_cpu_decode_physicalAddress;
   wire        IBusCachedPlugin_cache_io_mem_cmd_valid;
   wire [31:0] IBusCachedPlugin_cache_io_mem_cmd_payload_address;
   wire [ 2:0] IBusCachedPlugin_cache_io_mem_cmd_payload_size;
   wire        dataCache_1_io_cpu_execute_haltIt;
   wire        dataCache_1_io_cpu_execute_refilling;
   wire        dataCache_1_io_cpu_memory_isWrite;
   wire        dataCache_1_io_cpu_writeBack_haltIt;
   wire [31:0] dataCache_1_io_cpu_writeBack_data;
   wire        dataCache_1_io_cpu_writeBack_mmuException;
   wire        dataCache_1_io_cpu_writeBack_unalignedAccess;
   wire        dataCache_1_io_cpu_writeBack_accessError;
   wire        dataCache_1_io_cpu_writeBack_isWrite;
   wire        dataCache_1_io_cpu_writeBack_keepMemRspData;
   wire        dataCache_1_io_cpu_writeBack_exclusiveOk;
   wire        dataCache_1_io_cpu_flush_ready;
   wire        dataCache_1_io_cpu_redo;
   wire        dataCache_1_io_cpu_writesPending;
   wire        dataCache_1_io_mem_cmd_valid;
   wire        dataCache_1_io_mem_cmd_payload_wr;
   wire        dataCache_1_io_mem_cmd_payload_uncached;
   wire [31:0] dataCache_1_io_mem_cmd_payload_address;
   wire [31:0] dataCache_1_io_mem_cmd_payload_data;
   wire [ 3:0] dataCache_1_io_mem_cmd_payload_mask;
   wire [ 2:0] dataCache_1_io_mem_cmd_payload_size;
   wire        dataCache_1_io_mem_cmd_payload_last;
   wire [51:0] _zz_memory_MUL_LOW;
   wire [51:0] _zz_memory_MUL_LOW_1;
   wire [51:0] _zz_memory_MUL_LOW_2;
   wire [32:0] _zz_memory_MUL_LOW_3;
   wire [51:0] _zz_memory_MUL_LOW_4;
   wire [49:0] _zz_memory_MUL_LOW_5;
   wire [51:0] _zz_memory_MUL_LOW_6;
   wire [49:0] _zz_memory_MUL_LOW_7;
   wire [31:0] _zz_execute_SHIFT_RIGHT;
   wire [32:0] _zz_execute_SHIFT_RIGHT_1;
   wire [32:0] _zz_execute_SHIFT_RIGHT_2;
   wire [31:0] _zz_decode_FORMAL_PC_NEXT;
   wire [ 2:0] _zz_decode_FORMAL_PC_NEXT_1;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_1;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_2;
   wire        _zz_decode_LEGAL_INSTRUCTION_3;
   wire [ 0:0] _zz_decode_LEGAL_INSTRUCTION_4;
   wire [16:0] _zz_decode_LEGAL_INSTRUCTION_5;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_6;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_7;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_8;
   wire        _zz_decode_LEGAL_INSTRUCTION_9;
   wire [ 0:0] _zz_decode_LEGAL_INSTRUCTION_10;
   wire [10:0] _zz_decode_LEGAL_INSTRUCTION_11;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_12;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_13;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_14;
   wire        _zz_decode_LEGAL_INSTRUCTION_15;
   wire [ 0:0] _zz_decode_LEGAL_INSTRUCTION_16;
   wire [ 4:0] _zz_decode_LEGAL_INSTRUCTION_17;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_18;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_19;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_20;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_21;
   wire [31:0] _zz_decode_LEGAL_INSTRUCTION_22;
   wire [31:0] _zz_MmuPlugin_ioEndAddr;
   wire [ 3:0] _zz__zz_IBusCachedPlugin_jump_pcLoad_payload_1;
   reg  [31:0] _zz_IBusCachedPlugin_jump_pcLoad_payload_5;
   wire [ 1:0] _zz_IBusCachedPlugin_jump_pcLoad_payload_6;
   wire [31:0] _zz_IBusCachedPlugin_fetchPc_pc;
   wire [ 2:0] _zz_IBusCachedPlugin_fetchPc_pc_1;
   wire [31:0] _zz_IBusCachedPlugin_decodePc_pcPlus;
   wire [ 2:0] _zz_IBusCachedPlugin_decodePc_pcPlus_1;
   wire [31:0] _zz_IBusCachedPlugin_decompressor_decompressed_27;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_28;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_29;
   wire [ 6:0] _zz_IBusCachedPlugin_decompressor_decompressed_30;
   wire [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_31;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_32;
   wire [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_33;
   wire [11:0] _zz_IBusCachedPlugin_decompressor_decompressed_34;
   wire [11:0] _zz_IBusCachedPlugin_decompressor_decompressed_35;
   wire [25:0] _zz_io_cpu_flush_payload_lineId;
   wire [25:0] _zz_io_cpu_flush_payload_lineId_1;
   wire [ 2:0] _zz_DBusCachedPlugin_exceptionBus_payload_code;
   wire [ 2:0] _zz_DBusCachedPlugin_exceptionBus_payload_code_1;
   reg  [ 7:0] _zz_writeBack_DBusCachedPlugin_rspShifted;
   wire [ 1:0] _zz_writeBack_DBusCachedPlugin_rspShifted_1;
   reg  [ 7:0] _zz_writeBack_DBusCachedPlugin_rspShifted_2;
   wire [ 0:0] _zz_writeBack_DBusCachedPlugin_rspShifted_3;
   wire [ 0:0] _zz_writeBack_DBusCachedPlugin_rspRf;
   wire [ 9:0] _zz_MmuPlugin_ports_0_cacheHitsCalc;
   wire [ 9:0] _zz_MmuPlugin_ports_0_cacheHitsCalc_1;
   wire        _zz_MmuPlugin_ports_0_cacheHitsCalc_2;
   wire        _zz_MmuPlugin_ports_0_cacheHitsCalc_3;
   wire        _zz_MmuPlugin_ports_0_cacheHitsCalc_4;
   wire        _zz_MmuPlugin_ports_0_cacheHitsCalc_5;
   reg         _zz_MmuPlugin_ports_0_cacheLine_valid_4;
   reg         _zz_MmuPlugin_ports_0_cacheLine_exception;
   reg         _zz_MmuPlugin_ports_0_cacheLine_superPage;
   reg  [ 9:0] _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_0;
   reg  [ 9:0] _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_1;
   reg  [ 9:0] _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_0;
   reg  [ 9:0] _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_1;
   reg         _zz_MmuPlugin_ports_0_cacheLine_allowRead;
   reg         _zz_MmuPlugin_ports_0_cacheLine_allowWrite;
   reg         _zz_MmuPlugin_ports_0_cacheLine_allowExecute;
   reg         _zz_MmuPlugin_ports_0_cacheLine_allowUser;
   wire [ 1:0] _zz_MmuPlugin_ports_0_entryToReplace_valueNext;
   wire [ 0:0] _zz_MmuPlugin_ports_0_entryToReplace_valueNext_1;
   wire [ 9:0] _zz_MmuPlugin_ports_1_cacheHitsCalc;
   wire [ 9:0] _zz_MmuPlugin_ports_1_cacheHitsCalc_1;
   wire        _zz_MmuPlugin_ports_1_cacheHitsCalc_2;
   wire        _zz_MmuPlugin_ports_1_cacheHitsCalc_3;
   wire        _zz_MmuPlugin_ports_1_cacheHitsCalc_4;
   wire        _zz_MmuPlugin_ports_1_cacheHitsCalc_5;
   reg         _zz_MmuPlugin_ports_1_cacheLine_valid_4;
   reg         _zz_MmuPlugin_ports_1_cacheLine_exception;
   reg         _zz_MmuPlugin_ports_1_cacheLine_superPage;
   reg  [ 9:0] _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_0;
   reg  [ 9:0] _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_1;
   reg  [ 9:0] _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_0;
   reg  [ 9:0] _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_1;
   reg         _zz_MmuPlugin_ports_1_cacheLine_allowRead;
   reg         _zz_MmuPlugin_ports_1_cacheLine_allowWrite;
   reg         _zz_MmuPlugin_ports_1_cacheLine_allowExecute;
   reg         _zz_MmuPlugin_ports_1_cacheLine_allowUser;
   wire [ 1:0] _zz_MmuPlugin_ports_1_entryToReplace_valueNext;
   wire [ 0:0] _zz_MmuPlugin_ports_1_entryToReplace_valueNext_1;
   wire [ 1:0] _zz__zz_MmuPlugin_shared_refills_2;
   wire [31:0] _zz__zz_decode_IS_CSR;
   wire [31:0] _zz__zz_decode_IS_CSR_1;
   wire [31:0] _zz__zz_decode_IS_CSR_2;
   wire [31:0] _zz__zz_decode_IS_CSR_3;
   wire [31:0] _zz__zz_decode_IS_CSR_4;
   wire [31:0] _zz__zz_decode_IS_CSR_5;
   wire [ 0:0] _zz__zz_decode_IS_CSR_6;
   wire [31:0] _zz__zz_decode_IS_CSR_7;
   wire [ 0:0] _zz__zz_decode_IS_CSR_8;
   wire [31:0] _zz__zz_decode_IS_CSR_9;
   wire [ 1:0] _zz__zz_decode_IS_CSR_10;
   wire [31:0] _zz__zz_decode_IS_CSR_11;
   wire [31:0] _zz__zz_decode_IS_CSR_12;
   wire        _zz__zz_decode_IS_CSR_13;
   wire [31:0] _zz__zz_decode_IS_CSR_14;
   wire [31:0] _zz__zz_decode_IS_CSR_15;
   wire [ 0:0] _zz__zz_decode_IS_CSR_16;
   wire [29:0] _zz__zz_decode_IS_CSR_17;
   wire [ 0:0] _zz__zz_decode_IS_CSR_18;
   wire        _zz__zz_decode_IS_CSR_19;
   wire [ 0:0] _zz__zz_decode_IS_CSR_20;
   wire [31:0] _zz__zz_decode_IS_CSR_21;
   wire [26:0] _zz__zz_decode_IS_CSR_22;
   wire [31:0] _zz__zz_decode_IS_CSR_23;
   wire [31:0] _zz__zz_decode_IS_CSR_24;
   wire [ 0:0] _zz__zz_decode_IS_CSR_25;
   wire [ 0:0] _zz__zz_decode_IS_CSR_26;
   wire [ 0:0] _zz__zz_decode_IS_CSR_27;
   wire        _zz__zz_decode_IS_CSR_28;
   wire [31:0] _zz__zz_decode_IS_CSR_29;
   wire [ 0:0] _zz__zz_decode_IS_CSR_30;
   wire        _zz__zz_decode_IS_CSR_31;
   wire [21:0] _zz__zz_decode_IS_CSR_32;
   wire [ 0:0] _zz__zz_decode_IS_CSR_33;
   wire        _zz__zz_decode_IS_CSR_34;
   wire [31:0] _zz__zz_decode_IS_CSR_35;
   wire [ 0:0] _zz__zz_decode_IS_CSR_36;
   wire        _zz__zz_decode_IS_CSR_37;
   wire [ 0:0] _zz__zz_decode_IS_CSR_38;
   wire [31:0] _zz__zz_decode_IS_CSR_39;
   wire [ 1:0] _zz__zz_decode_IS_CSR_40;
   wire [31:0] _zz__zz_decode_IS_CSR_41;
   wire [31:0] _zz__zz_decode_IS_CSR_42;
   wire [31:0] _zz__zz_decode_IS_CSR_43;
   wire [31:0] _zz__zz_decode_IS_CSR_44;
   wire [17:0] _zz__zz_decode_IS_CSR_45;
   wire        _zz__zz_decode_IS_CSR_46;
   wire [ 0:0] _zz__zz_decode_IS_CSR_47;
   wire [31:0] _zz__zz_decode_IS_CSR_48;
   wire        _zz__zz_decode_IS_CSR_49;
   wire        _zz__zz_decode_IS_CSR_50;
   wire [31:0] _zz__zz_decode_IS_CSR_51;
   wire [ 0:0] _zz__zz_decode_IS_CSR_52;
   wire [31:0] _zz__zz_decode_IS_CSR_53;
   wire [31:0] _zz__zz_decode_IS_CSR_54;
   wire [ 3:0] _zz__zz_decode_IS_CSR_55;
   wire        _zz__zz_decode_IS_CSR_56;
   wire [31:0] _zz__zz_decode_IS_CSR_57;
   wire [ 0:0] _zz__zz_decode_IS_CSR_58;
   wire [ 1:0] _zz__zz_decode_IS_CSR_59;
   wire        _zz__zz_decode_IS_CSR_60;
   wire [31:0] _zz__zz_decode_IS_CSR_61;
   wire [ 0:0] _zz__zz_decode_IS_CSR_62;
   wire [ 0:0] _zz__zz_decode_IS_CSR_63;
   wire [31:0] _zz__zz_decode_IS_CSR_64;
   wire [31:0] _zz__zz_decode_IS_CSR_65;
   wire [ 1:0] _zz__zz_decode_IS_CSR_66;
   wire        _zz__zz_decode_IS_CSR_67;
   wire [31:0] _zz__zz_decode_IS_CSR_68;
   wire        _zz__zz_decode_IS_CSR_69;
   wire [31:0] _zz__zz_decode_IS_CSR_70;
   wire [13:0] _zz__zz_decode_IS_CSR_71;
   wire [ 4:0] _zz__zz_decode_IS_CSR_72;
   wire        _zz__zz_decode_IS_CSR_73;
   wire [31:0] _zz__zz_decode_IS_CSR_74;
   wire [ 0:0] _zz__zz_decode_IS_CSR_75;
   wire [31:0] _zz__zz_decode_IS_CSR_76;
   wire [31:0] _zz__zz_decode_IS_CSR_77;
   wire [ 2:0] _zz__zz_decode_IS_CSR_78;
   wire        _zz__zz_decode_IS_CSR_79;
   wire [31:0] _zz__zz_decode_IS_CSR_80;
   wire [ 0:0] _zz__zz_decode_IS_CSR_81;
   wire [31:0] _zz__zz_decode_IS_CSR_82;
   wire [31:0] _zz__zz_decode_IS_CSR_83;
   wire [ 0:0] _zz__zz_decode_IS_CSR_84;
   wire        _zz__zz_decode_IS_CSR_85;
   wire [ 0:0] _zz__zz_decode_IS_CSR_86;
   wire [ 3:0] _zz__zz_decode_IS_CSR_87;
   wire        _zz__zz_decode_IS_CSR_88;
   wire [31:0] _zz__zz_decode_IS_CSR_89;
   wire [ 0:0] _zz__zz_decode_IS_CSR_90;
   wire [31:0] _zz__zz_decode_IS_CSR_91;
   wire [31:0] _zz__zz_decode_IS_CSR_92;
   wire [ 1:0] _zz__zz_decode_IS_CSR_93;
   wire        _zz__zz_decode_IS_CSR_94;
   wire [31:0] _zz__zz_decode_IS_CSR_95;
   wire        _zz__zz_decode_IS_CSR_96;
   wire [31:0] _zz__zz_decode_IS_CSR_97;
   wire [ 0:0] _zz__zz_decode_IS_CSR_98;
   wire [ 6:0] _zz__zz_decode_IS_CSR_99;
   wire [ 0:0] _zz__zz_decode_IS_CSR_100;
   wire [31:0] _zz__zz_decode_IS_CSR_101;
   wire [31:0] _zz__zz_decode_IS_CSR_102;
   wire [ 4:0] _zz__zz_decode_IS_CSR_103;
   wire        _zz__zz_decode_IS_CSR_104;
   wire [31:0] _zz__zz_decode_IS_CSR_105;
   wire [ 0:0] _zz__zz_decode_IS_CSR_106;
   wire [31:0] _zz__zz_decode_IS_CSR_107;
   wire [31:0] _zz__zz_decode_IS_CSR_108;
   wire [ 2:0] _zz__zz_decode_IS_CSR_109;
   wire        _zz__zz_decode_IS_CSR_110;
   wire [ 0:0] _zz__zz_decode_IS_CSR_111;
   wire [ 0:0] _zz__zz_decode_IS_CSR_112;
   wire [31:0] _zz__zz_decode_IS_CSR_113;
   wire [10:0] _zz__zz_decode_IS_CSR_114;
   wire        _zz__zz_decode_IS_CSR_115;
   wire [ 0:0] _zz__zz_decode_IS_CSR_116;
   wire [ 0:0] _zz__zz_decode_IS_CSR_117;
   wire [31:0] _zz__zz_decode_IS_CSR_118;
   wire [31:0] _zz__zz_decode_IS_CSR_119;
   wire [ 0:0] _zz__zz_decode_IS_CSR_120;
   wire [ 1:0] _zz__zz_decode_IS_CSR_121;
   wire        _zz__zz_decode_IS_CSR_122;
   wire [31:0] _zz__zz_decode_IS_CSR_123;
   wire [ 8:0] _zz__zz_decode_IS_CSR_124;
   wire        _zz__zz_decode_IS_CSR_125;
   wire        _zz__zz_decode_IS_CSR_126;
   wire [31:0] _zz__zz_decode_IS_CSR_127;
   wire [ 0:0] _zz__zz_decode_IS_CSR_128;
   wire [ 0:0] _zz__zz_decode_IS_CSR_129;
   wire [31:0] _zz__zz_decode_IS_CSR_130;
   wire [31:0] _zz__zz_decode_IS_CSR_131;
   wire [ 6:0] _zz__zz_decode_IS_CSR_132;
   wire        _zz__zz_decode_IS_CSR_133;
   wire [ 0:0] _zz__zz_decode_IS_CSR_134;
   wire [31:0] _zz__zz_decode_IS_CSR_135;
   wire [ 4:0] _zz__zz_decode_IS_CSR_136;
   wire        _zz__zz_decode_IS_CSR_137;
   wire [31:0] _zz__zz_decode_IS_CSR_138;
   wire [ 0:0] _zz__zz_decode_IS_CSR_139;
   wire [31:0] _zz__zz_decode_IS_CSR_140;
   wire [31:0] _zz__zz_decode_IS_CSR_141;
   wire [ 1:0] _zz__zz_decode_IS_CSR_142;
   wire        _zz__zz_decode_IS_CSR_143;
   wire [ 0:0] _zz__zz_decode_IS_CSR_144;
   wire [ 1:0] _zz__zz_decode_IS_CSR_145;
   wire [31:0] _zz__zz_decode_IS_CSR_146;
   wire [31:0] _zz__zz_decode_IS_CSR_147;
   wire [ 4:0] _zz__zz_decode_IS_CSR_148;
   wire        _zz__zz_decode_IS_CSR_149;
   wire        _zz__zz_decode_IS_CSR_150;
   wire [31:0] _zz__zz_decode_IS_CSR_151;
   wire [ 0:0] _zz__zz_decode_IS_CSR_152;
   wire [31:0] _zz__zz_decode_IS_CSR_153;
   wire [31:0] _zz__zz_decode_IS_CSR_154;
   wire [ 0:0] _zz__zz_decode_IS_CSR_155;
   wire [31:0] _zz__zz_decode_IS_CSR_156;
   wire [31:0] _zz__zz_decode_IS_CSR_157;
   wire [ 0:0] _zz__zz_decode_IS_CSR_158;
   wire [ 0:0] _zz__zz_decode_IS_CSR_159;
   wire [ 1:0] _zz__zz_decode_IS_CSR_160;
   wire        _zz__zz_decode_IS_CSR_161;
   wire [ 2:0] _zz__zz_decode_IS_CSR_162;
   wire [ 1:0] _zz__zz_decode_IS_CSR_163;
   wire        _zz__zz_decode_IS_CSR_164;
   wire        _zz__zz_decode_IS_CSR_165;
   wire [ 0:0] _zz__zz_decode_IS_CSR_166;
   wire [ 0:0] _zz__zz_decode_IS_CSR_167;
   wire        _zz__zz_decode_IS_CSR_168;
   wire        _zz_RegFilePlugin_regFile_port;
   wire        _zz_decode_RegFilePlugin_rs1Data;
   wire        _zz_RegFilePlugin_regFile_port_1;
   wire        _zz_decode_RegFilePlugin_rs2Data;
   wire [ 0:0] _zz__zz_execute_REGFILE_WRITE_DATA;
   wire [ 2:0] _zz__zz_execute_SRC1;
   wire [ 4:0] _zz__zz_execute_SRC1_1;
   wire [11:0] _zz__zz_execute_SRC2_2;
   wire [31:0] _zz_execute_SrcPlugin_addSub;
   wire [31:0] _zz_execute_SrcPlugin_addSub_1;
   wire [31:0] _zz_execute_SrcPlugin_addSub_2;
   wire [31:0] _zz_execute_SrcPlugin_addSub_3;
   wire [31:0] _zz_execute_SrcPlugin_addSub_4;
   wire [65:0] _zz_writeBack_MulPlugin_result;
   wire [65:0] _zz_writeBack_MulPlugin_result_1;
   wire [31:0] _zz__zz_decode_RS2_2;
   wire [31:0] _zz__zz_decode_RS2_2_1;
   wire [ 5:0] _zz_memory_DivPlugin_div_counter_valueNext;
   wire [ 0:0] _zz_memory_DivPlugin_div_counter_valueNext_1;
   wire [32:0] _zz_memory_DivPlugin_div_stage_0_remainderMinusDenominator;
   wire [31:0] _zz_memory_DivPlugin_div_stage_0_outRemainder;
   wire [31:0] _zz_memory_DivPlugin_div_stage_0_outRemainder_1;
   wire [32:0] _zz_memory_DivPlugin_div_stage_0_outNumerator;
   wire [32:0] _zz_memory_DivPlugin_div_result_1;
   wire [32:0] _zz_memory_DivPlugin_div_result_2;
   wire [32:0] _zz_memory_DivPlugin_div_result_3;
   wire [32:0] _zz_memory_DivPlugin_div_result_4;
   wire [ 0:0] _zz_memory_DivPlugin_div_result_5;
   wire [32:0] _zz_memory_DivPlugin_rs1_2;
   wire [ 0:0] _zz_memory_DivPlugin_rs1_3;
   wire [31:0] _zz_memory_DivPlugin_rs2_1;
   wire [ 0:0] _zz_memory_DivPlugin_rs2_2;
   wire [19:0] _zz__zz_execute_BranchPlugin_branch_src2;
   wire [11:0] _zz__zz_execute_BranchPlugin_branch_src2_4;
   wire [ 1:0] _zz__zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1;
   wire [ 1:0] _zz__zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1_1;
   wire        _zz_when;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_35;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_36;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_37;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_38;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_39;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_40;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_41;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_42;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_43;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_44;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_45;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_46;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_47;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_48;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_49;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_50;
   wire [31:0] _zz_CsrPlugin_csrMapping_readDataInit_51;
   wire [ 3:0] _zz_dbus_axi_arw_payload_len;
   wire [51:0] memory_MUL_LOW;
   wire [31:0] execute_BRANCH_CALC;
   wire        execute_BRANCH_DO;
   wire [33:0] memory_MUL_HH;
   wire [33:0] execute_MUL_HH;
   wire [33:0] execute_MUL_HL;
   wire [33:0] execute_MUL_LH;
   wire [31:0] execute_MUL_LL;
   wire [31:0] execute_SHIFT_RIGHT;
   wire [31:0] execute_REGFILE_WRITE_DATA;
   wire [31:0] memory_MEMORY_STORE_DATA_RF;
   wire [31:0] execute_MEMORY_STORE_DATA_RF;
   wire        decode_CSR_READ_OPCODE;
   wire        decode_CSR_WRITE_OPCODE;
   wire        decode_SRC2_FORCE_ZERO;
   wire [ 2:0] _zz_memory_to_writeBack_ENV_CTRL;
   wire [ 2:0] _zz_memory_to_writeBack_ENV_CTRL_1;
   wire [ 2:0] _zz_execute_to_memory_ENV_CTRL;
   wire [ 2:0] _zz_execute_to_memory_ENV_CTRL_1;
   wire [ 2:0] decode_ENV_CTRL;
   wire [ 2:0] _zz_decode_ENV_CTRL;
   wire [ 2:0] _zz_decode_to_execute_ENV_CTRL;
   wire [ 2:0] _zz_decode_to_execute_ENV_CTRL_1;
   wire        decode_IS_CSR;
   wire [ 1:0] decode_BRANCH_CTRL;
   wire [ 1:0] _zz_decode_BRANCH_CTRL;
   wire [ 1:0] _zz_decode_to_execute_BRANCH_CTRL;
   wire [ 1:0] _zz_decode_to_execute_BRANCH_CTRL_1;
   wire        decode_IS_RS2_SIGNED;
   wire        decode_IS_RS1_SIGNED;
   wire        decode_IS_DIV;
   wire        memory_IS_MUL;
   wire        execute_IS_MUL;
   wire        decode_IS_MUL;
   wire [ 1:0] _zz_execute_to_memory_SHIFT_CTRL;
   wire [ 1:0] _zz_execute_to_memory_SHIFT_CTRL_1;
   wire [ 1:0] decode_SHIFT_CTRL;
   wire [ 1:0] _zz_decode_SHIFT_CTRL;
   wire [ 1:0] _zz_decode_to_execute_SHIFT_CTRL;
   wire [ 1:0] _zz_decode_to_execute_SHIFT_CTRL_1;
   wire [ 1:0] decode_ALU_BITWISE_CTRL;
   wire [ 1:0] _zz_decode_ALU_BITWISE_CTRL;
   wire [ 1:0] _zz_decode_to_execute_ALU_BITWISE_CTRL;
   wire [ 1:0] _zz_decode_to_execute_ALU_BITWISE_CTRL_1;
   wire        decode_SRC_LESS_UNSIGNED;
   wire        decode_IS_SFENCE_VMA2;
   wire        decode_MEMORY_MANAGMENT;
   wire        memory_MEMORY_LRSC;
   wire        memory_MEMORY_WR;
   wire        decode_MEMORY_WR;
   wire        execute_BYPASSABLE_MEMORY_STAGE;
   wire        decode_BYPASSABLE_MEMORY_STAGE;
   wire        decode_BYPASSABLE_EXECUTE_STAGE;
   wire [ 1:0] decode_SRC2_CTRL;
   wire [ 1:0] _zz_decode_SRC2_CTRL;
   wire [ 1:0] _zz_decode_to_execute_SRC2_CTRL;
   wire [ 1:0] _zz_decode_to_execute_SRC2_CTRL_1;
   wire [ 1:0] decode_ALU_CTRL;
   wire [ 1:0] _zz_decode_ALU_CTRL;
   wire [ 1:0] _zz_decode_to_execute_ALU_CTRL;
   wire [ 1:0] _zz_decode_to_execute_ALU_CTRL_1;
   wire [ 1:0] decode_SRC1_CTRL;
   wire [ 1:0] _zz_decode_SRC1_CTRL;
   wire [ 1:0] _zz_decode_to_execute_SRC1_CTRL;
   wire [ 1:0] _zz_decode_to_execute_SRC1_CTRL_1;
   wire        decode_RESCHEDULE_NEXT;
   wire        decode_MEMORY_FORCE_CONSTISTENCY;
   wire [31:0] writeBack_FORMAL_PC_NEXT;
   wire [31:0] memory_FORMAL_PC_NEXT;
   wire [31:0] execute_FORMAL_PC_NEXT;
   wire [31:0] decode_FORMAL_PC_NEXT;
   wire [31:0] memory_PC;
   wire        execute_CSR_READ_OPCODE;
   wire        execute_CSR_WRITE_OPCODE;
   wire        execute_IS_CSR;
   wire [ 2:0] memory_ENV_CTRL;
   wire [ 2:0] _zz_memory_ENV_CTRL;
   wire [ 2:0] execute_ENV_CTRL;
   wire [ 2:0] _zz_execute_ENV_CTRL;
   wire [ 2:0] writeBack_ENV_CTRL;
   wire [ 2:0] _zz_writeBack_ENV_CTRL;
   wire        execute_RESCHEDULE_NEXT;
   wire [31:0] memory_BRANCH_CALC;
   wire        memory_BRANCH_DO;
   wire [31:0] execute_PC;
   wire [ 1:0] execute_BRANCH_CTRL;
   wire [ 1:0] _zz_execute_BRANCH_CTRL;
   wire        decode_RS2_USE;
   wire        decode_RS1_USE;
   reg  [31:0] _zz_decode_RS2;
   wire        execute_REGFILE_WRITE_VALID;
   wire        execute_BYPASSABLE_EXECUTE_STAGE;
   wire        memory_REGFILE_WRITE_VALID;
   wire        memory_BYPASSABLE_MEMORY_STAGE;
   wire        writeBack_REGFILE_WRITE_VALID;
   reg  [31:0] decode_RS2;
   reg  [31:0] decode_RS1;
   wire        execute_IS_RS1_SIGNED;
   wire        execute_IS_DIV;
   wire        execute_IS_RS2_SIGNED;
   wire [31:0] memory_INSTRUCTION;
   wire        memory_IS_DIV;
   wire        writeBack_IS_MUL;
   wire [33:0] writeBack_MUL_HH;
   wire [51:0] writeBack_MUL_LOW;
   wire [33:0] memory_MUL_HL;
   wire [33:0] memory_MUL_LH;
   wire [31:0] memory_MUL_LL;
   wire [31:0] memory_SHIFT_RIGHT;
   reg  [31:0] _zz_decode_RS2_1;
   wire [ 1:0] memory_SHIFT_CTRL;
   wire [ 1:0] _zz_memory_SHIFT_CTRL;
   wire [ 1:0] execute_SHIFT_CTRL;
   wire [ 1:0] _zz_execute_SHIFT_CTRL;
   wire        execute_SRC_LESS_UNSIGNED;
   wire        execute_SRC2_FORCE_ZERO;
   wire        execute_SRC_USE_SUB_LESS;
   wire [31:0] _zz_execute_to_memory_PC;
   wire [ 1:0] execute_SRC2_CTRL;
   wire [ 1:0] _zz_execute_SRC2_CTRL;
   wire        execute_IS_RVC;
   wire [ 1:0] execute_SRC1_CTRL;
   wire [ 1:0] _zz_execute_SRC1_CTRL;
   wire        decode_SRC_USE_SUB_LESS;
   wire        decode_SRC_ADD_ZERO;
   wire [31:0] execute_SRC_ADD_SUB;
   wire        execute_SRC_LESS;
   wire [ 1:0] execute_ALU_CTRL;
   wire [ 1:0] _zz_execute_ALU_CTRL;
   wire [31:0] execute_SRC2;
   wire [31:0] execute_SRC1;
   wire [ 1:0] execute_ALU_BITWISE_CTRL;
   wire [ 1:0] _zz_execute_ALU_BITWISE_CTRL;
   wire [31:0] _zz_lastStageRegFileWrite_payload_address;
   wire        _zz_lastStageRegFileWrite_valid;
   reg         _zz_1;
   wire [31:0] decode_INSTRUCTION_ANTICIPATED;
   reg         decode_REGFILE_WRITE_VALID;
   wire        decode_LEGAL_INSTRUCTION;
   wire [ 2:0] _zz_decode_ENV_CTRL_1;
   wire [ 1:0] _zz_decode_BRANCH_CTRL_1;
   wire [ 1:0] _zz_decode_SHIFT_CTRL_1;
   wire [ 1:0] _zz_decode_ALU_BITWISE_CTRL_1;
   wire [ 1:0] _zz_decode_SRC2_CTRL_1;
   wire [ 1:0] _zz_decode_ALU_CTRL_1;
   wire [ 1:0] _zz_decode_SRC1_CTRL_1;
   wire        execute_IS_SFENCE_VMA2;
   wire        writeBack_IS_DBUS_SHARING;
   wire        execute_IS_DBUS_SHARING;
   wire        memory_IS_DBUS_SHARING;
   reg  [31:0] _zz_decode_RS2_2;
   wire        writeBack_MEMORY_LRSC;
   wire        writeBack_MEMORY_WR;
   wire [31:0] writeBack_MEMORY_STORE_DATA_RF;
   wire [31:0] writeBack_REGFILE_WRITE_DATA;
   wire        writeBack_MEMORY_ENABLE;
   wire [31:0] memory_REGFILE_WRITE_DATA;
   wire        memory_MEMORY_ENABLE;
   reg         execute_MEMORY_AMO;
   reg         execute_MEMORY_LRSC;
   wire        execute_MEMORY_FORCE_CONSTISTENCY;
   (* keep , syn_keep *)wire [31:0] execute_RS1  /* synthesis syn_keep = 1 */;
   wire        execute_MEMORY_MANAGMENT;
   (* keep , syn_keep *)wire [31:0] execute_RS2  /* synthesis syn_keep = 1 */;
   wire        execute_MEMORY_WR;
   wire [31:0] execute_SRC_ADD;
   wire        execute_MEMORY_ENABLE;
   wire [31:0] execute_INSTRUCTION;
   wire        decode_MEMORY_AMO;
   wire        decode_MEMORY_LRSC;
   reg         _zz_decode_MEMORY_FORCE_CONSTISTENCY;
   wire        decode_MEMORY_ENABLE;
   wire        decode_FLUSH_ALL;
   reg         IBusCachedPlugin_rsp_issueDetected_4;
   reg         IBusCachedPlugin_rsp_issueDetected_3;
   reg         IBusCachedPlugin_rsp_issueDetected_2;
   reg         IBusCachedPlugin_rsp_issueDetected_1;
   reg  [31:0] _zz_execute_to_memory_FORMAL_PC_NEXT;
   reg  [31:0] _zz_memory_to_writeBack_FORMAL_PC_NEXT;
   wire [31:0] decode_PC;
   wire [31:0] decode_INSTRUCTION;
   wire        decode_IS_RVC;
   wire [31:0] writeBack_PC;
   wire [31:0] writeBack_INSTRUCTION;
   reg         decode_arbitration_haltItself;
   reg         decode_arbitration_haltByOther;
   reg         decode_arbitration_removeIt;
   wire        decode_arbitration_flushIt;
   reg         decode_arbitration_flushNext;
   reg         decode_arbitration_isValid;
   wire        decode_arbitration_isStuck;
   wire        decode_arbitration_isStuckByOthers;
   wire        decode_arbitration_isFlushed;
   wire        decode_arbitration_isMoving;
   wire        decode_arbitration_isFiring;
   reg         execute_arbitration_haltItself;
   reg         execute_arbitration_haltByOther;
   reg         execute_arbitration_removeIt;
   wire        execute_arbitration_flushIt;
   reg         execute_arbitration_flushNext;
   reg         execute_arbitration_isValid;
   wire        execute_arbitration_isStuck;
   wire        execute_arbitration_isStuckByOthers;
   wire        execute_arbitration_isFlushed;
   wire        execute_arbitration_isMoving;
   wire        execute_arbitration_isFiring;
   reg         memory_arbitration_haltItself;
   wire        memory_arbitration_haltByOther;
   reg         memory_arbitration_removeIt;
   wire        memory_arbitration_flushIt;
   reg         memory_arbitration_flushNext;
   reg         memory_arbitration_isValid;
   wire        memory_arbitration_isStuck;
   wire        memory_arbitration_isStuckByOthers;
   wire        memory_arbitration_isFlushed;
   wire        memory_arbitration_isMoving;
   wire        memory_arbitration_isFiring;
   reg         writeBack_arbitration_haltItself;
   wire        writeBack_arbitration_haltByOther;
   reg         writeBack_arbitration_removeIt;
   reg         writeBack_arbitration_flushIt;
   reg         writeBack_arbitration_flushNext;
   reg         writeBack_arbitration_isValid;
   wire        writeBack_arbitration_isStuck;
   wire        writeBack_arbitration_isStuckByOthers;
   wire        writeBack_arbitration_isFlushed;
   wire        writeBack_arbitration_isMoving;
   wire        writeBack_arbitration_isFiring;
   wire [31:0] lastStageInstruction  /* verilator public */;
   wire [31:0] lastStagePc  /* verilator public */;
   wire        lastStageIsValid  /* verilator public */;
   wire        lastStageIsFiring  /* verilator public */;
   reg         IBusCachedPlugin_fetcherHalt;
   wire        IBusCachedPlugin_forceNoDecodeCond;
   reg         IBusCachedPlugin_incomingInstruction;
   wire        IBusCachedPlugin_pcValids_0;
   wire        IBusCachedPlugin_pcValids_1;
   wire        IBusCachedPlugin_pcValids_2;
   wire        IBusCachedPlugin_pcValids_3;
   reg         IBusCachedPlugin_decodeExceptionPort_valid;
   reg  [ 3:0] IBusCachedPlugin_decodeExceptionPort_payload_code;
   wire [31:0] IBusCachedPlugin_decodeExceptionPort_payload_badAddr;
   wire        IBusCachedPlugin_mmuBus_cmd_0_isValid;
   wire        IBusCachedPlugin_mmuBus_cmd_0_isStuck;
   wire [31:0] IBusCachedPlugin_mmuBus_cmd_0_virtualAddress;
   wire        IBusCachedPlugin_mmuBus_cmd_0_bypassTranslation;
   wire        IBusCachedPlugin_mmuBus_cmd_1_isValid;
   wire        IBusCachedPlugin_mmuBus_cmd_1_isStuck;
   wire [31:0] IBusCachedPlugin_mmuBus_cmd_1_virtualAddress;
   wire        IBusCachedPlugin_mmuBus_cmd_1_bypassTranslation;
   reg  [31:0] IBusCachedPlugin_mmuBus_rsp_physicalAddress;
   wire        IBusCachedPlugin_mmuBus_rsp_isIoAccess;
   reg         IBusCachedPlugin_mmuBus_rsp_isPaging;
   reg         IBusCachedPlugin_mmuBus_rsp_allowRead;
   reg         IBusCachedPlugin_mmuBus_rsp_allowWrite;
   reg         IBusCachedPlugin_mmuBus_rsp_allowExecute;
   reg         IBusCachedPlugin_mmuBus_rsp_exception;
   reg         IBusCachedPlugin_mmuBus_rsp_refilling;
   wire        IBusCachedPlugin_mmuBus_rsp_bypassTranslation;
   wire        IBusCachedPlugin_mmuBus_rsp_ways_0_sel;
   wire [31:0] IBusCachedPlugin_mmuBus_rsp_ways_0_physical;
   wire        IBusCachedPlugin_mmuBus_rsp_ways_1_sel;
   wire [31:0] IBusCachedPlugin_mmuBus_rsp_ways_1_physical;
   wire        IBusCachedPlugin_mmuBus_rsp_ways_2_sel;
   wire [31:0] IBusCachedPlugin_mmuBus_rsp_ways_2_physical;
   wire        IBusCachedPlugin_mmuBus_rsp_ways_3_sel;
   wire [31:0] IBusCachedPlugin_mmuBus_rsp_ways_3_physical;
   wire        IBusCachedPlugin_mmuBus_end;
   wire        IBusCachedPlugin_mmuBus_busy;
   wire        dBus_cmd_valid;
   wire        dBus_cmd_ready;
   wire        dBus_cmd_payload_wr;
   wire        dBus_cmd_payload_uncached;
   wire [31:0] dBus_cmd_payload_address;
   wire [31:0] dBus_cmd_payload_data;
   wire [ 3:0] dBus_cmd_payload_mask;
   wire [ 2:0] dBus_cmd_payload_size;
   wire        dBus_cmd_payload_last;
   wire        dBus_rsp_valid;
   wire        dBus_rsp_payload_last;
   wire [31:0] dBus_rsp_payload_data;
   wire        dBus_rsp_payload_error;
   wire        DBusCachedPlugin_mmuBus_cmd_0_isValid;
   wire        DBusCachedPlugin_mmuBus_cmd_0_isStuck;
   wire [31:0] DBusCachedPlugin_mmuBus_cmd_0_virtualAddress;
   reg         DBusCachedPlugin_mmuBus_cmd_0_bypassTranslation;
   wire        DBusCachedPlugin_mmuBus_cmd_1_isValid;
   wire        DBusCachedPlugin_mmuBus_cmd_1_isStuck;
   wire [31:0] DBusCachedPlugin_mmuBus_cmd_1_virtualAddress;
   reg         DBusCachedPlugin_mmuBus_cmd_1_bypassTranslation;
   reg  [31:0] DBusCachedPlugin_mmuBus_rsp_physicalAddress;
   wire        DBusCachedPlugin_mmuBus_rsp_isIoAccess;
   reg         DBusCachedPlugin_mmuBus_rsp_isPaging;
   reg         DBusCachedPlugin_mmuBus_rsp_allowRead;
   reg         DBusCachedPlugin_mmuBus_rsp_allowWrite;
   reg         DBusCachedPlugin_mmuBus_rsp_allowExecute;
   reg         DBusCachedPlugin_mmuBus_rsp_exception;
   reg         DBusCachedPlugin_mmuBus_rsp_refilling;
   wire        DBusCachedPlugin_mmuBus_rsp_bypassTranslation;
   wire        DBusCachedPlugin_mmuBus_rsp_ways_0_sel;
   wire [31:0] DBusCachedPlugin_mmuBus_rsp_ways_0_physical;
   wire        DBusCachedPlugin_mmuBus_rsp_ways_1_sel;
   wire [31:0] DBusCachedPlugin_mmuBus_rsp_ways_1_physical;
   wire        DBusCachedPlugin_mmuBus_rsp_ways_2_sel;
   wire [31:0] DBusCachedPlugin_mmuBus_rsp_ways_2_physical;
   wire        DBusCachedPlugin_mmuBus_rsp_ways_3_sel;
   wire [31:0] DBusCachedPlugin_mmuBus_rsp_ways_3_physical;
   wire        DBusCachedPlugin_mmuBus_end;
   wire        DBusCachedPlugin_mmuBus_busy;
   reg         DBusCachedPlugin_redoBranch_valid;
   wire [31:0] DBusCachedPlugin_redoBranch_payload;
   reg         DBusCachedPlugin_exceptionBus_valid;
   reg  [ 3:0] DBusCachedPlugin_exceptionBus_payload_code;
   wire [31:0] DBusCachedPlugin_exceptionBus_payload_badAddr;
   wire [31:0] MmuPlugin_ioEndAddr;
   reg         MmuPlugin_dBusAccess_cmd_valid;
   reg         MmuPlugin_dBusAccess_cmd_ready;
   reg  [31:0] MmuPlugin_dBusAccess_cmd_payload_address;
   wire [ 1:0] MmuPlugin_dBusAccess_cmd_payload_size;
   wire        MmuPlugin_dBusAccess_cmd_payload_write;
   wire [31:0] MmuPlugin_dBusAccess_cmd_payload_data;
   wire [ 3:0] MmuPlugin_dBusAccess_cmd_payload_writeMask;
   wire        MmuPlugin_dBusAccess_rsp_valid;
   wire [31:0] MmuPlugin_dBusAccess_rsp_payload_data;
   wire        MmuPlugin_dBusAccess_rsp_payload_error;
   wire        MmuPlugin_dBusAccess_rsp_payload_redo;
   wire        decodeExceptionPort_valid;
   wire [ 3:0] decodeExceptionPort_payload_code;
   wire [31:0] decodeExceptionPort_payload_badAddr;
   wire        BranchPlugin_jumpInterface_valid;
   wire [31:0] BranchPlugin_jumpInterface_payload;
   wire        BranchPlugin_inDebugNoFetchFlag;
   wire [31:0] CsrPlugin_csrMapping_readDataSignal;
   wire [31:0] CsrPlugin_csrMapping_readDataInit;
   wire [31:0] CsrPlugin_csrMapping_writeDataSignal;
   reg         CsrPlugin_csrMapping_allowCsrSignal;
   wire        CsrPlugin_csrMapping_hazardFree;
   reg         CsrPlugin_csrMapping_doForceFailCsr;
   reg         CsrPlugin_inWfi  /* verilator public */;
   wire        CsrPlugin_thirdPartyWake;
   reg         CsrPlugin_jumpInterface_valid;
   reg  [31:0] CsrPlugin_jumpInterface_payload;
   reg         CsrPlugin_redoInterface_valid;
   wire [31:0] CsrPlugin_redoInterface_payload;
   wire        CsrPlugin_exceptionPendings_0;
   wire        CsrPlugin_exceptionPendings_1;
   wire        CsrPlugin_exceptionPendings_2;
   wire        CsrPlugin_exceptionPendings_3;
   wire        timerInterrupt;
   wire        externalInterrupt;
   wire        softwareInterrupt;
   wire        externalInterruptS;
   wire        contextSwitching;
   reg  [ 1:0] CsrPlugin_privilege;
   wire        CsrPlugin_forceMachineWire;
   reg         CsrPlugin_selfException_valid;
   reg  [ 3:0] CsrPlugin_selfException_payload_code;
   wire [31:0] CsrPlugin_selfException_payload_badAddr;
   wire        CsrPlugin_allowInterrupts;
   wire        CsrPlugin_allowException;
   wire        CsrPlugin_allowEbreakException;
   wire [63:0] utime;
   reg         CsrPlugin_xretAwayFromMachine;
   wire        IBusCachedPlugin_externalFlush;
   wire        IBusCachedPlugin_jump_pcLoad_valid;
   wire [31:0] IBusCachedPlugin_jump_pcLoad_payload;
   wire [ 3:0] _zz_IBusCachedPlugin_jump_pcLoad_payload;
   wire [ 3:0] _zz_IBusCachedPlugin_jump_pcLoad_payload_1;
   wire        _zz_IBusCachedPlugin_jump_pcLoad_payload_2;
   wire        _zz_IBusCachedPlugin_jump_pcLoad_payload_3;
   wire        _zz_IBusCachedPlugin_jump_pcLoad_payload_4;
   wire        IBusCachedPlugin_fetchPc_output_valid;
   wire        IBusCachedPlugin_fetchPc_output_ready;
   wire [31:0] IBusCachedPlugin_fetchPc_output_payload;
   reg  [31:0] IBusCachedPlugin_fetchPc_pcReg  /* verilator public */;
   reg         IBusCachedPlugin_fetchPc_correction;
   reg         IBusCachedPlugin_fetchPc_correctionReg;
   wire        IBusCachedPlugin_fetchPc_output_fire;
   wire        IBusCachedPlugin_fetchPc_corrected;
   reg         IBusCachedPlugin_fetchPc_pcRegPropagate;
   reg         IBusCachedPlugin_fetchPc_booted;
   reg         IBusCachedPlugin_fetchPc_inc;
   wire        when_Fetcher_l133;
   wire        when_Fetcher_l133_1;
   reg  [31:0] IBusCachedPlugin_fetchPc_pc;
   wire        IBusCachedPlugin_fetchPc_redo_valid;
   reg  [31:0] IBusCachedPlugin_fetchPc_redo_payload;
   reg         IBusCachedPlugin_fetchPc_flushed;
   wire        when_Fetcher_l160;
   reg         IBusCachedPlugin_decodePc_flushed;
   reg  [31:0] IBusCachedPlugin_decodePc_pcReg  /* verilator public */;
   wire [31:0] IBusCachedPlugin_decodePc_pcPlus;
   wire        IBusCachedPlugin_decodePc_injectedDecode;
   wire        when_Fetcher_l182;
   wire        when_Fetcher_l194;
   reg         IBusCachedPlugin_iBusRsp_redoFetch;
   wire        IBusCachedPlugin_iBusRsp_stages_0_input_valid;
   wire        IBusCachedPlugin_iBusRsp_stages_0_input_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_stages_0_input_payload;
   wire        IBusCachedPlugin_iBusRsp_stages_0_output_valid;
   wire        IBusCachedPlugin_iBusRsp_stages_0_output_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_stages_0_output_payload;
   reg         IBusCachedPlugin_iBusRsp_stages_0_halt;
   wire        IBusCachedPlugin_iBusRsp_stages_1_input_valid;
   wire        IBusCachedPlugin_iBusRsp_stages_1_input_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_stages_1_input_payload;
   wire        IBusCachedPlugin_iBusRsp_stages_1_output_valid;
   wire        IBusCachedPlugin_iBusRsp_stages_1_output_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_stages_1_output_payload;
   wire        IBusCachedPlugin_iBusRsp_stages_1_halt;
   wire        IBusCachedPlugin_iBusRsp_stages_2_input_valid;
   wire        IBusCachedPlugin_iBusRsp_stages_2_input_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_stages_2_input_payload;
   wire        IBusCachedPlugin_iBusRsp_stages_2_output_valid;
   wire        IBusCachedPlugin_iBusRsp_stages_2_output_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_stages_2_output_payload;
   reg         IBusCachedPlugin_iBusRsp_stages_2_halt;
   wire        _zz_IBusCachedPlugin_iBusRsp_stages_0_input_ready;
   wire        _zz_IBusCachedPlugin_iBusRsp_stages_1_input_ready;
   wire        _zz_IBusCachedPlugin_iBusRsp_stages_2_input_ready;
   wire        IBusCachedPlugin_iBusRsp_flush;
   wire        _zz_IBusCachedPlugin_iBusRsp_stages_0_output_ready;
   wire        _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid;
   reg         _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid_1;
   wire        IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid;
   wire        IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_payload;
   reg         _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid;
   reg  [31:0] _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_payload;
   reg         IBusCachedPlugin_iBusRsp_readyForError;
   wire        IBusCachedPlugin_iBusRsp_output_valid;
   wire        IBusCachedPlugin_iBusRsp_output_ready;
   wire [31:0] IBusCachedPlugin_iBusRsp_output_payload_pc;
   wire        IBusCachedPlugin_iBusRsp_output_payload_rsp_error;
   wire [31:0] IBusCachedPlugin_iBusRsp_output_payload_rsp_inst;
   wire        IBusCachedPlugin_iBusRsp_output_payload_isRvc;
   wire        when_Fetcher_l242;
   wire        IBusCachedPlugin_decompressor_input_valid;
   wire        IBusCachedPlugin_decompressor_input_ready;
   wire [31:0] IBusCachedPlugin_decompressor_input_payload_pc;
   wire        IBusCachedPlugin_decompressor_input_payload_rsp_error;
   wire [31:0] IBusCachedPlugin_decompressor_input_payload_rsp_inst;
   wire        IBusCachedPlugin_decompressor_input_payload_isRvc;
   wire        IBusCachedPlugin_decompressor_output_valid;
   wire        IBusCachedPlugin_decompressor_output_ready;
   wire [31:0] IBusCachedPlugin_decompressor_output_payload_pc;
   wire        IBusCachedPlugin_decompressor_output_payload_rsp_error;
   wire [31:0] IBusCachedPlugin_decompressor_output_payload_rsp_inst;
   wire        IBusCachedPlugin_decompressor_output_payload_isRvc;
   wire        IBusCachedPlugin_decompressor_flushNext;
   wire        IBusCachedPlugin_decompressor_consumeCurrent;
   reg         IBusCachedPlugin_decompressor_bufferValid;
   reg  [15:0] IBusCachedPlugin_decompressor_bufferData;
   wire        IBusCachedPlugin_decompressor_isInputLowRvc;
   wire        IBusCachedPlugin_decompressor_isInputHighRvc;
   reg         IBusCachedPlugin_decompressor_throw2BytesReg;
   wire        IBusCachedPlugin_decompressor_throw2Bytes;
   wire        IBusCachedPlugin_decompressor_unaligned;
   reg         IBusCachedPlugin_decompressor_bufferValidLatch;
   reg         IBusCachedPlugin_decompressor_throw2BytesLatch;
   wire        IBusCachedPlugin_decompressor_bufferValidPatched;
   wire        IBusCachedPlugin_decompressor_throw2BytesPatched;
   wire [31:0] IBusCachedPlugin_decompressor_raw;
   wire        IBusCachedPlugin_decompressor_isRvc;
   wire [15:0] _zz_IBusCachedPlugin_decompressor_decompressed;
   reg  [31:0] IBusCachedPlugin_decompressor_decompressed;
   wire [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_1;
   wire [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_2;
   wire [11:0] _zz_IBusCachedPlugin_decompressor_decompressed_3;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_4;
   reg  [11:0] _zz_IBusCachedPlugin_decompressor_decompressed_5;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_6;
   reg  [ 9:0] _zz_IBusCachedPlugin_decompressor_decompressed_7;
   wire [20:0] _zz_IBusCachedPlugin_decompressor_decompressed_8;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_9;
   reg  [14:0] _zz_IBusCachedPlugin_decompressor_decompressed_10;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_11;
   reg  [ 2:0] _zz_IBusCachedPlugin_decompressor_decompressed_12;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_13;
   reg  [ 9:0] _zz_IBusCachedPlugin_decompressor_decompressed_14;
   wire [20:0] _zz_IBusCachedPlugin_decompressor_decompressed_15;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_16;
   reg  [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_17;
   wire [12:0] _zz_IBusCachedPlugin_decompressor_decompressed_18;
   wire [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_19;
   wire [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_20;
   wire [ 4:0] _zz_IBusCachedPlugin_decompressor_decompressed_21;
   wire [ 4:0] switch_Misc_l44;
   wire        when_Misc_l47;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_22;
   wire [ 1:0] switch_Misc_l227;
   wire [ 1:0] switch_Misc_l227_1;
   reg  [ 2:0] _zz_IBusCachedPlugin_decompressor_decompressed_23;
   reg  [ 2:0] _zz_IBusCachedPlugin_decompressor_decompressed_24;
   wire        _zz_IBusCachedPlugin_decompressor_decompressed_25;
   reg  [ 6:0] _zz_IBusCachedPlugin_decompressor_decompressed_26;
   wire        IBusCachedPlugin_decompressor_output_fire;
   wire        IBusCachedPlugin_decompressor_bufferFill;
   wire        when_Fetcher_l285;
   wire        when_Fetcher_l288;
   wire        when_Fetcher_l293;
   wire        IBusCachedPlugin_injector_decodeInput_valid;
   wire        IBusCachedPlugin_injector_decodeInput_ready;
   wire [31:0] IBusCachedPlugin_injector_decodeInput_payload_pc;
   wire        IBusCachedPlugin_injector_decodeInput_payload_rsp_error;
   wire [31:0] IBusCachedPlugin_injector_decodeInput_payload_rsp_inst;
   wire        IBusCachedPlugin_injector_decodeInput_payload_isRvc;
   reg         _zz_IBusCachedPlugin_injector_decodeInput_valid;
   reg  [31:0] _zz_IBusCachedPlugin_injector_decodeInput_payload_pc;
   reg         _zz_IBusCachedPlugin_injector_decodeInput_payload_rsp_error;
   reg  [31:0] _zz_IBusCachedPlugin_injector_decodeInput_payload_rsp_inst;
   reg         _zz_IBusCachedPlugin_injector_decodeInput_payload_isRvc;
   reg         IBusCachedPlugin_injector_nextPcCalc_valids_0;
   wire        when_Fetcher_l331;
   reg         IBusCachedPlugin_injector_nextPcCalc_valids_1;
   wire        when_Fetcher_l331_1;
   reg         IBusCachedPlugin_injector_nextPcCalc_valids_2;
   wire        when_Fetcher_l331_2;
   reg         IBusCachedPlugin_injector_nextPcCalc_valids_3;
   wire        when_Fetcher_l331_3;
   reg  [31:0] IBusCachedPlugin_injector_formal_rawInDecode;
   wire        iBus_cmd_valid;
   wire        iBus_cmd_ready;
   reg  [31:0] iBus_cmd_payload_address;
   wire [ 2:0] iBus_cmd_payload_size;
   wire        iBus_rsp_valid;
   wire [31:0] iBus_rsp_payload_data;
   wire        iBus_rsp_payload_error;
   reg  [31:0] IBusCachedPlugin_rspCounter;
   wire        IBusCachedPlugin_s0_tightlyCoupledHit;
   reg         IBusCachedPlugin_s1_tightlyCoupledHit;
   reg         IBusCachedPlugin_s2_tightlyCoupledHit;
   wire        IBusCachedPlugin_rsp_iBusRspOutputHalt;
   wire        IBusCachedPlugin_rsp_issueDetected;
   reg         IBusCachedPlugin_rsp_redoFetch;
   wire        when_IBusCachedPlugin_l245;
   wire        when_IBusCachedPlugin_l250;
   wire        when_IBusCachedPlugin_l256;
   wire        when_IBusCachedPlugin_l262;
   wire        when_IBusCachedPlugin_l273;
   reg  [31:0] DBusCachedPlugin_rspCounter;
   wire        when_DBusCachedPlugin_l343;
   wire        when_DBusCachedPlugin_l351;
   wire [ 1:0] execute_DBusCachedPlugin_size;
   reg  [31:0] _zz_execute_MEMORY_STORE_DATA_RF;
   wire        toplevel_dataCache_1_io_cpu_flush_isStall;
   wire        when_DBusCachedPlugin_l385;
   wire        when_DBusCachedPlugin_l401;
   wire        when_DBusCachedPlugin_l463;
   wire        when_DBusCachedPlugin_l524;
   wire        when_DBusCachedPlugin_l544;
   wire [31:0] writeBack_DBusCachedPlugin_rspData;
   wire [ 7:0] writeBack_DBusCachedPlugin_rspSplits_0;
   wire [ 7:0] writeBack_DBusCachedPlugin_rspSplits_1;
   wire [ 7:0] writeBack_DBusCachedPlugin_rspSplits_2;
   wire [ 7:0] writeBack_DBusCachedPlugin_rspSplits_3;
   reg  [31:0] writeBack_DBusCachedPlugin_rspShifted;
   reg  [31:0] writeBack_DBusCachedPlugin_rspRf;
   wire        when_DBusCachedPlugin_l561;
   wire [ 1:0] switch_Misc_l227_2;
   wire        _zz_writeBack_DBusCachedPlugin_rspFormated;
   reg  [31:0] _zz_writeBack_DBusCachedPlugin_rspFormated_1;
   wire        _zz_writeBack_DBusCachedPlugin_rspFormated_2;
   reg  [31:0] _zz_writeBack_DBusCachedPlugin_rspFormated_3;
   reg  [31:0] writeBack_DBusCachedPlugin_rspFormated;
   wire        when_DBusCachedPlugin_l571;
   reg         DBusCachedPlugin_forceDatapath;
   wire        when_DBusCachedPlugin_l595;
   wire        when_DBusCachedPlugin_l596;
   wire        MmuPlugin_dBusAccess_cmd_fire;
   reg         MmuPlugin_status_sum;
   reg         MmuPlugin_status_mxr;
   reg         MmuPlugin_status_mprv;
   reg         MmuPlugin_satp_mode;
   reg  [ 8:0] MmuPlugin_satp_asid;
   reg  [21:0] MmuPlugin_satp_ppn;
   reg         MmuPlugin_ports_0_cache_0_valid;
   reg         MmuPlugin_ports_0_cache_0_exception;
   reg         MmuPlugin_ports_0_cache_0_superPage;
   reg  [ 9:0] MmuPlugin_ports_0_cache_0_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_0_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_0_cache_0_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_0_physicalAddress_1;
   reg         MmuPlugin_ports_0_cache_0_allowRead;
   reg         MmuPlugin_ports_0_cache_0_allowWrite;
   reg         MmuPlugin_ports_0_cache_0_allowExecute;
   reg         MmuPlugin_ports_0_cache_0_allowUser;
   reg         MmuPlugin_ports_0_cache_1_valid;
   reg         MmuPlugin_ports_0_cache_1_exception;
   reg         MmuPlugin_ports_0_cache_1_superPage;
   reg  [ 9:0] MmuPlugin_ports_0_cache_1_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_1_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_0_cache_1_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_1_physicalAddress_1;
   reg         MmuPlugin_ports_0_cache_1_allowRead;
   reg         MmuPlugin_ports_0_cache_1_allowWrite;
   reg         MmuPlugin_ports_0_cache_1_allowExecute;
   reg         MmuPlugin_ports_0_cache_1_allowUser;
   reg         MmuPlugin_ports_0_cache_2_valid;
   reg         MmuPlugin_ports_0_cache_2_exception;
   reg         MmuPlugin_ports_0_cache_2_superPage;
   reg  [ 9:0] MmuPlugin_ports_0_cache_2_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_2_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_0_cache_2_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_2_physicalAddress_1;
   reg         MmuPlugin_ports_0_cache_2_allowRead;
   reg         MmuPlugin_ports_0_cache_2_allowWrite;
   reg         MmuPlugin_ports_0_cache_2_allowExecute;
   reg         MmuPlugin_ports_0_cache_2_allowUser;
   reg         MmuPlugin_ports_0_cache_3_valid;
   reg         MmuPlugin_ports_0_cache_3_exception;
   reg         MmuPlugin_ports_0_cache_3_superPage;
   reg  [ 9:0] MmuPlugin_ports_0_cache_3_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_3_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_0_cache_3_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_0_cache_3_physicalAddress_1;
   reg         MmuPlugin_ports_0_cache_3_allowRead;
   reg         MmuPlugin_ports_0_cache_3_allowWrite;
   reg         MmuPlugin_ports_0_cache_3_allowExecute;
   reg         MmuPlugin_ports_0_cache_3_allowUser;
   reg         MmuPlugin_ports_0_dirty;
   wire        when_MmuPlugin_l129;
   reg         MmuPlugin_ports_0_requireMmuLockupCalc;
   wire        when_MmuPlugin_l143;
   wire        when_MmuPlugin_l144;
   wire [ 3:0] MmuPlugin_ports_0_cacheHitsCalc;
   wire        when_MmuPlugin_l136;
   reg         MmuPlugin_ports_0_requireMmuLockup;
   wire        when_MmuPlugin_l136_1;
   reg  [ 3:0] MmuPlugin_ports_0_cacheHits;
   wire        MmuPlugin_ports_0_cacheHit;
   wire        _zz_MmuPlugin_ports_0_cacheLine_valid;
   wire        _zz_MmuPlugin_ports_0_cacheLine_valid_1;
   wire        _zz_MmuPlugin_ports_0_cacheLine_valid_2;
   wire [ 1:0] _zz_MmuPlugin_ports_0_cacheLine_valid_3;
   wire        MmuPlugin_ports_0_cacheLine_valid;
   wire        MmuPlugin_ports_0_cacheLine_exception;
   wire        MmuPlugin_ports_0_cacheLine_superPage;
   wire [ 9:0] MmuPlugin_ports_0_cacheLine_virtualAddress_0;
   wire [ 9:0] MmuPlugin_ports_0_cacheLine_virtualAddress_1;
   wire [ 9:0] MmuPlugin_ports_0_cacheLine_physicalAddress_0;
   wire [ 9:0] MmuPlugin_ports_0_cacheLine_physicalAddress_1;
   wire        MmuPlugin_ports_0_cacheLine_allowRead;
   wire        MmuPlugin_ports_0_cacheLine_allowWrite;
   wire        MmuPlugin_ports_0_cacheLine_allowExecute;
   wire        MmuPlugin_ports_0_cacheLine_allowUser;
   reg         MmuPlugin_ports_0_entryToReplace_willIncrement;
   wire        MmuPlugin_ports_0_entryToReplace_willClear;
   reg  [ 1:0] MmuPlugin_ports_0_entryToReplace_valueNext;
   reg  [ 1:0] MmuPlugin_ports_0_entryToReplace_value;
   wire        MmuPlugin_ports_0_entryToReplace_willOverflowIfInc;
   wire        MmuPlugin_ports_0_entryToReplace_willOverflow;
   reg         MmuPlugin_ports_1_cache_0_valid;
   reg         MmuPlugin_ports_1_cache_0_exception;
   reg         MmuPlugin_ports_1_cache_0_superPage;
   reg  [ 9:0] MmuPlugin_ports_1_cache_0_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_0_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_1_cache_0_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_0_physicalAddress_1;
   reg         MmuPlugin_ports_1_cache_0_allowRead;
   reg         MmuPlugin_ports_1_cache_0_allowWrite;
   reg         MmuPlugin_ports_1_cache_0_allowExecute;
   reg         MmuPlugin_ports_1_cache_0_allowUser;
   reg         MmuPlugin_ports_1_cache_1_valid;
   reg         MmuPlugin_ports_1_cache_1_exception;
   reg         MmuPlugin_ports_1_cache_1_superPage;
   reg  [ 9:0] MmuPlugin_ports_1_cache_1_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_1_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_1_cache_1_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_1_physicalAddress_1;
   reg         MmuPlugin_ports_1_cache_1_allowRead;
   reg         MmuPlugin_ports_1_cache_1_allowWrite;
   reg         MmuPlugin_ports_1_cache_1_allowExecute;
   reg         MmuPlugin_ports_1_cache_1_allowUser;
   reg         MmuPlugin_ports_1_cache_2_valid;
   reg         MmuPlugin_ports_1_cache_2_exception;
   reg         MmuPlugin_ports_1_cache_2_superPage;
   reg  [ 9:0] MmuPlugin_ports_1_cache_2_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_2_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_1_cache_2_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_2_physicalAddress_1;
   reg         MmuPlugin_ports_1_cache_2_allowRead;
   reg         MmuPlugin_ports_1_cache_2_allowWrite;
   reg         MmuPlugin_ports_1_cache_2_allowExecute;
   reg         MmuPlugin_ports_1_cache_2_allowUser;
   reg         MmuPlugin_ports_1_cache_3_valid;
   reg         MmuPlugin_ports_1_cache_3_exception;
   reg         MmuPlugin_ports_1_cache_3_superPage;
   reg  [ 9:0] MmuPlugin_ports_1_cache_3_virtualAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_3_virtualAddress_1;
   reg  [ 9:0] MmuPlugin_ports_1_cache_3_physicalAddress_0;
   reg  [ 9:0] MmuPlugin_ports_1_cache_3_physicalAddress_1;
   reg         MmuPlugin_ports_1_cache_3_allowRead;
   reg         MmuPlugin_ports_1_cache_3_allowWrite;
   reg         MmuPlugin_ports_1_cache_3_allowExecute;
   reg         MmuPlugin_ports_1_cache_3_allowUser;
   reg         MmuPlugin_ports_1_dirty;
   wire        when_MmuPlugin_l129_1;
   reg         MmuPlugin_ports_1_requireMmuLockupCalc;
   wire        when_MmuPlugin_l143_1;
   wire        when_MmuPlugin_l144_1;
   wire        when_MmuPlugin_l146;
   wire [ 3:0] MmuPlugin_ports_1_cacheHitsCalc;
   wire        when_MmuPlugin_l136_2;
   reg         MmuPlugin_ports_1_requireMmuLockup;
   wire        when_MmuPlugin_l136_3;
   reg  [ 3:0] MmuPlugin_ports_1_cacheHits;
   wire        MmuPlugin_ports_1_cacheHit;
   wire        _zz_MmuPlugin_ports_1_cacheLine_valid;
   wire        _zz_MmuPlugin_ports_1_cacheLine_valid_1;
   wire        _zz_MmuPlugin_ports_1_cacheLine_valid_2;
   wire [ 1:0] _zz_MmuPlugin_ports_1_cacheLine_valid_3;
   wire        MmuPlugin_ports_1_cacheLine_valid;
   wire        MmuPlugin_ports_1_cacheLine_exception;
   wire        MmuPlugin_ports_1_cacheLine_superPage;
   wire [ 9:0] MmuPlugin_ports_1_cacheLine_virtualAddress_0;
   wire [ 9:0] MmuPlugin_ports_1_cacheLine_virtualAddress_1;
   wire [ 9:0] MmuPlugin_ports_1_cacheLine_physicalAddress_0;
   wire [ 9:0] MmuPlugin_ports_1_cacheLine_physicalAddress_1;
   wire        MmuPlugin_ports_1_cacheLine_allowRead;
   wire        MmuPlugin_ports_1_cacheLine_allowWrite;
   wire        MmuPlugin_ports_1_cacheLine_allowExecute;
   wire        MmuPlugin_ports_1_cacheLine_allowUser;
   reg         MmuPlugin_ports_1_entryToReplace_willIncrement;
   wire        MmuPlugin_ports_1_entryToReplace_willClear;
   reg  [ 1:0] MmuPlugin_ports_1_entryToReplace_valueNext;
   reg  [ 1:0] MmuPlugin_ports_1_entryToReplace_value;
   wire        MmuPlugin_ports_1_entryToReplace_willOverflowIfInc;
   wire        MmuPlugin_ports_1_entryToReplace_willOverflow;
   reg  [ 2:0] MmuPlugin_shared_state_1;
   reg  [ 9:0] MmuPlugin_shared_vpn_0;
   reg  [ 9:0] MmuPlugin_shared_vpn_1;
   reg  [ 1:0] MmuPlugin_shared_portSortedOh;
   reg         MmuPlugin_shared_dBusRspStaged_valid;
   reg  [31:0] MmuPlugin_shared_dBusRspStaged_payload_data;
   reg         MmuPlugin_shared_dBusRspStaged_payload_error;
   reg         MmuPlugin_shared_dBusRspStaged_payload_redo;
   wire        MmuPlugin_shared_dBusRsp_pte_V;
   wire        MmuPlugin_shared_dBusRsp_pte_R;
   wire        MmuPlugin_shared_dBusRsp_pte_W;
   wire        MmuPlugin_shared_dBusRsp_pte_X;
   wire        MmuPlugin_shared_dBusRsp_pte_U;
   wire        MmuPlugin_shared_dBusRsp_pte_G;
   wire        MmuPlugin_shared_dBusRsp_pte_A;
   wire        MmuPlugin_shared_dBusRsp_pte_D;
   wire [ 1:0] MmuPlugin_shared_dBusRsp_pte_RSW;
   wire [ 9:0] MmuPlugin_shared_dBusRsp_pte_PPN0;
   wire [11:0] MmuPlugin_shared_dBusRsp_pte_PPN1;
   wire        MmuPlugin_shared_dBusRsp_exception;
   wire        MmuPlugin_shared_dBusRsp_leaf;
   wire        when_MmuPlugin_l234;
   reg         MmuPlugin_shared_pteBuffer_V;
   reg         MmuPlugin_shared_pteBuffer_R;
   reg         MmuPlugin_shared_pteBuffer_W;
   reg         MmuPlugin_shared_pteBuffer_X;
   reg         MmuPlugin_shared_pteBuffer_U;
   reg         MmuPlugin_shared_pteBuffer_G;
   reg         MmuPlugin_shared_pteBuffer_A;
   reg         MmuPlugin_shared_pteBuffer_D;
   reg  [ 1:0] MmuPlugin_shared_pteBuffer_RSW;
   reg  [ 9:0] MmuPlugin_shared_pteBuffer_PPN0;
   reg  [11:0] MmuPlugin_shared_pteBuffer_PPN1;
   wire [ 1:0] _zz_MmuPlugin_shared_refills;
   reg  [ 1:0] _zz_MmuPlugin_shared_refills_1;
   wire [ 1:0] MmuPlugin_shared_refills;
   wire [ 1:0] _zz_MmuPlugin_shared_refills_2;
   reg  [ 1:0] _zz_MmuPlugin_shared_refills_3;
   wire        when_MmuPlugin_l246;
   wire [31:0] _zz_MmuPlugin_shared_vpn_0;
   wire        when_MmuPlugin_l273;
   wire        when_MmuPlugin_l302;
   wire        when_MmuPlugin_l304;
   wire        when_MmuPlugin_l310;
   wire        when_MmuPlugin_l310_1;
   wire        when_MmuPlugin_l310_2;
   wire        when_MmuPlugin_l310_3;
   wire        when_MmuPlugin_l304_1;
   wire        when_MmuPlugin_l310_4;
   wire        when_MmuPlugin_l310_5;
   wire        when_MmuPlugin_l310_6;
   wire        when_MmuPlugin_l310_7;
   wire        when_MmuPlugin_l334;
   wire [36:0] _zz_decode_IS_CSR;
   wire        _zz_decode_IS_CSR_1;
   wire        _zz_decode_IS_CSR_2;
   wire        _zz_decode_IS_CSR_3;
   wire        _zz_decode_IS_CSR_4;
   wire        _zz_decode_IS_CSR_5;
   wire        _zz_decode_IS_CSR_6;
   wire        _zz_decode_IS_CSR_7;
   wire        _zz_decode_IS_CSR_8;
   wire        _zz_decode_IS_CSR_9;
   wire        _zz_decode_IS_CSR_10;
   wire [ 1:0] _zz_decode_SRC1_CTRL_2;
   wire [ 1:0] _zz_decode_ALU_CTRL_2;
   wire [ 1:0] _zz_decode_SRC2_CTRL_2;
   wire [ 1:0] _zz_decode_ALU_BITWISE_CTRL_2;
   wire [ 1:0] _zz_decode_SHIFT_CTRL_2;
   wire [ 1:0] _zz_decode_BRANCH_CTRL_2;
   wire [ 2:0] _zz_decode_ENV_CTRL_2;
   wire        when_RegFilePlugin_l63;
   wire [ 4:0] decode_RegFilePlugin_regFileReadAddress1;
   wire [ 4:0] decode_RegFilePlugin_regFileReadAddress2;
   wire [31:0] decode_RegFilePlugin_rs1Data;
   wire [31:0] decode_RegFilePlugin_rs2Data;
   reg         lastStageRegFileWrite_valid  /* verilator public */;
   reg  [ 4:0] lastStageRegFileWrite_payload_address  /* verilator public */;
   reg  [31:0] lastStageRegFileWrite_payload_data  /* verilator public */;
   reg         _zz_5;
   reg  [31:0] execute_IntAluPlugin_bitwise;
   reg  [31:0] _zz_execute_REGFILE_WRITE_DATA;
   reg  [31:0] _zz_execute_SRC1;
   wire        _zz_execute_SRC2;
   reg  [19:0] _zz_execute_SRC2_1;
   wire        _zz_execute_SRC2_2;
   reg  [19:0] _zz_execute_SRC2_3;
   reg  [31:0] _zz_execute_SRC2_4;
   reg  [31:0] execute_SrcPlugin_addSub;
   wire        execute_SrcPlugin_less;
   wire [ 4:0] execute_FullBarrelShifterPlugin_amplitude;
   reg  [31:0] _zz_execute_FullBarrelShifterPlugin_reversed;
   wire [31:0] execute_FullBarrelShifterPlugin_reversed;
   reg  [31:0] _zz_decode_RS2_3;
   reg         execute_MulPlugin_aSigned;
   reg         execute_MulPlugin_bSigned;
   wire [31:0] execute_MulPlugin_a;
   wire [31:0] execute_MulPlugin_b;
   wire [ 1:0] switch_MulPlugin_l87;
   wire [15:0] execute_MulPlugin_aULow;
   wire [15:0] execute_MulPlugin_bULow;
   wire [16:0] execute_MulPlugin_aSLow;
   wire [16:0] execute_MulPlugin_bSLow;
   wire [16:0] execute_MulPlugin_aHigh;
   wire [16:0] execute_MulPlugin_bHigh;
   wire [65:0] writeBack_MulPlugin_result;
   wire        when_MulPlugin_l147;
   wire [ 1:0] switch_MulPlugin_l148;
   reg  [32:0] memory_DivPlugin_rs1;
   reg  [31:0] memory_DivPlugin_rs2;
   reg  [64:0] memory_DivPlugin_accumulator;
   wire        memory_DivPlugin_frontendOk;
   reg         memory_DivPlugin_div_needRevert;
   reg         memory_DivPlugin_div_counter_willIncrement;
   reg         memory_DivPlugin_div_counter_willClear;
   reg  [ 5:0] memory_DivPlugin_div_counter_valueNext;
   reg  [ 5:0] memory_DivPlugin_div_counter_value;
   wire        memory_DivPlugin_div_counter_willOverflowIfInc;
   wire        memory_DivPlugin_div_counter_willOverflow;
   reg         memory_DivPlugin_div_done;
   wire        when_MulDivIterativePlugin_l126;
   wire        when_MulDivIterativePlugin_l126_1;
   reg  [31:0] memory_DivPlugin_div_result;
   wire        when_MulDivIterativePlugin_l128;
   wire        when_MulDivIterativePlugin_l129;
   wire        when_MulDivIterativePlugin_l132;
   wire [31:0] _zz_memory_DivPlugin_div_stage_0_remainderShifted;
   wire [32:0] memory_DivPlugin_div_stage_0_remainderShifted;
   wire [32:0] memory_DivPlugin_div_stage_0_remainderMinusDenominator;
   wire [31:0] memory_DivPlugin_div_stage_0_outRemainder;
   wire [31:0] memory_DivPlugin_div_stage_0_outNumerator;
   wire        when_MulDivIterativePlugin_l151;
   wire [31:0] _zz_memory_DivPlugin_div_result;
   wire        when_MulDivIterativePlugin_l162;
   wire        _zz_memory_DivPlugin_rs2;
   wire        _zz_memory_DivPlugin_rs1;
   reg  [32:0] _zz_memory_DivPlugin_rs1_1;
   reg         HazardSimplePlugin_src0Hazard;
   reg         HazardSimplePlugin_src1Hazard;
   wire        HazardSimplePlugin_writeBackWrites_valid;
   wire [ 4:0] HazardSimplePlugin_writeBackWrites_payload_address;
   wire [31:0] HazardSimplePlugin_writeBackWrites_payload_data;
   reg         HazardSimplePlugin_writeBackBuffer_valid;
   reg  [ 4:0] HazardSimplePlugin_writeBackBuffer_payload_address;
   reg  [31:0] HazardSimplePlugin_writeBackBuffer_payload_data;
   wire        HazardSimplePlugin_addr0Match;
   wire        HazardSimplePlugin_addr1Match;
   wire        when_HazardSimplePlugin_l47;
   wire        when_HazardSimplePlugin_l48;
   wire        when_HazardSimplePlugin_l51;
   wire        when_HazardSimplePlugin_l45;
   wire        when_HazardSimplePlugin_l57;
   wire        when_HazardSimplePlugin_l58;
   wire        when_HazardSimplePlugin_l48_1;
   wire        when_HazardSimplePlugin_l51_1;
   wire        when_HazardSimplePlugin_l45_1;
   wire        when_HazardSimplePlugin_l57_1;
   wire        when_HazardSimplePlugin_l58_1;
   wire        when_HazardSimplePlugin_l48_2;
   wire        when_HazardSimplePlugin_l51_2;
   wire        when_HazardSimplePlugin_l45_2;
   wire        when_HazardSimplePlugin_l57_2;
   wire        when_HazardSimplePlugin_l58_2;
   wire        when_HazardSimplePlugin_l105;
   wire        when_HazardSimplePlugin_l108;
   wire        when_HazardSimplePlugin_l113;
   wire        execute_BranchPlugin_eq;
   wire [ 2:0] switch_Misc_l227_3;
   reg         _zz_execute_BRANCH_DO;
   reg         _zz_execute_BRANCH_DO_1;
   wire [31:0] execute_BranchPlugin_branch_src1;
   wire        _zz_execute_BranchPlugin_branch_src2;
   reg  [10:0] _zz_execute_BranchPlugin_branch_src2_1;
   wire        _zz_execute_BranchPlugin_branch_src2_2;
   reg  [19:0] _zz_execute_BranchPlugin_branch_src2_3;
   wire        _zz_execute_BranchPlugin_branch_src2_4;
   reg  [18:0] _zz_execute_BranchPlugin_branch_src2_5;
   reg  [31:0] _zz_execute_BranchPlugin_branch_src2_6;
   wire [31:0] execute_BranchPlugin_branch_src2;
   wire [31:0] execute_BranchPlugin_branchAdder;
   reg  [ 1:0] _zz_CsrPlugin_privilege;
   wire [ 1:0] CsrPlugin_misa_base;
   wire [25:0] CsrPlugin_misa_extensions;
   wire [ 1:0] CsrPlugin_mtvec_mode;
   reg  [29:0] CsrPlugin_mtvec_base;
   reg  [31:0] CsrPlugin_mepc;
   reg         CsrPlugin_mstatus_MIE;
   reg         CsrPlugin_mstatus_MPIE;
   reg  [ 1:0] CsrPlugin_mstatus_MPP;
   reg         CsrPlugin_mip_MEIP;
   reg         CsrPlugin_mip_MTIP;
   reg         CsrPlugin_mip_MSIP;
   reg         CsrPlugin_mie_MEIE;
   reg         CsrPlugin_mie_MTIE;
   reg         CsrPlugin_mie_MSIE;
   reg  [31:0] CsrPlugin_mscratch;
   reg         CsrPlugin_mcause_interrupt;
   reg  [ 3:0] CsrPlugin_mcause_exceptionCode;
   reg  [31:0] CsrPlugin_mtval;
   reg  [63:0] CsrPlugin_mcycle;
   reg  [63:0] CsrPlugin_minstret;
   reg         CsrPlugin_medeleg_IAM;
   reg         CsrPlugin_medeleg_IAF;
   reg         CsrPlugin_medeleg_II;
   reg         CsrPlugin_medeleg_BP;
   reg         CsrPlugin_medeleg_LAM;
   reg         CsrPlugin_medeleg_LAF;
   reg         CsrPlugin_medeleg_SAM;
   reg         CsrPlugin_medeleg_SAF;
   reg         CsrPlugin_medeleg_EU;
   reg         CsrPlugin_medeleg_ES;
   reg         CsrPlugin_medeleg_IPF;
   reg         CsrPlugin_medeleg_LPF;
   reg         CsrPlugin_medeleg_SPF;
   reg         CsrPlugin_mideleg_ST;
   reg         CsrPlugin_mideleg_SE;
   reg         CsrPlugin_mideleg_SS;
   reg         CsrPlugin_mcounteren_IR;
   reg         CsrPlugin_mcounteren_TM;
   reg         CsrPlugin_mcounteren_CY;
   reg         CsrPlugin_scounteren_IR;
   reg         CsrPlugin_scounteren_TM;
   reg         CsrPlugin_scounteren_CY;
   reg         CsrPlugin_sstatus_SIE;
   reg         CsrPlugin_sstatus_SPIE;
   reg  [ 0:0] CsrPlugin_sstatus_SPP;
   reg         CsrPlugin_sip_SEIP_SOFT;
   reg         CsrPlugin_sip_SEIP_INPUT;
   wire        CsrPlugin_sip_SEIP_OR;
   reg         CsrPlugin_sip_STIP;
   reg         CsrPlugin_sip_SSIP;
   reg         CsrPlugin_sie_SEIE;
   reg         CsrPlugin_sie_STIE;
   reg         CsrPlugin_sie_SSIE;
   reg  [ 1:0] CsrPlugin_stvec_mode;
   reg  [29:0] CsrPlugin_stvec_base;
   reg  [31:0] CsrPlugin_sscratch;
   reg         CsrPlugin_scause_interrupt;
   reg  [ 3:0] CsrPlugin_scause_exceptionCode;
   reg  [31:0] CsrPlugin_stval;
   reg  [31:0] CsrPlugin_sepc;
   reg  [21:0] CsrPlugin_satp_PPN;
   reg  [ 8:0] CsrPlugin_satp_ASID;
   reg  [ 0:0] CsrPlugin_satp_MODE;
   reg         CsrPlugin_rescheduleLogic_rescheduleNext;
   wire        when_CsrPlugin_l1153;
   wire        _zz_when_CsrPlugin_l1302;
   wire        _zz_when_CsrPlugin_l1302_1;
   wire        _zz_when_CsrPlugin_l1302_2;
   wire        _zz_when_CsrPlugin_l1302_3;
   wire        _zz_when_CsrPlugin_l1302_4;
   wire        _zz_when_CsrPlugin_l1302_5;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValids_decode;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValids_execute;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValids_memory;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValids_writeBack;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_decode;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_execute;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_memory;
   reg         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_writeBack;
   reg  [ 3:0] CsrPlugin_exceptionPortCtrl_exceptionContext_code;
   reg  [31:0] CsrPlugin_exceptionPortCtrl_exceptionContext_badAddr;
   reg  [ 1:0] CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped;
   wire        when_CsrPlugin_l1216;
   wire        when_CsrPlugin_l1216_1;
   wire        when_CsrPlugin_l1216_2;
   wire        when_CsrPlugin_l1216_3;
   wire        when_CsrPlugin_l1216_4;
   wire        when_CsrPlugin_l1216_5;
   wire        when_CsrPlugin_l1216_6;
   wire        when_CsrPlugin_l1216_7;
   wire        when_CsrPlugin_l1216_8;
   wire        when_CsrPlugin_l1216_9;
   wire        when_CsrPlugin_l1216_10;
   wire        when_CsrPlugin_l1216_11;
   wire        when_CsrPlugin_l1216_12;
   wire [ 1:0] CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilege;
   wire [ 1:0] _zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code;
   wire        _zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1;
   wire        when_CsrPlugin_l1259;
   wire        when_CsrPlugin_l1259_1;
   wire        when_CsrPlugin_l1259_2;
   wire        when_CsrPlugin_l1259_3;
   wire        when_CsrPlugin_l1272;
   reg         CsrPlugin_interrupt_valid;
   reg  [ 3:0] CsrPlugin_interrupt_code  /* verilator public */;
   reg  [ 1:0] CsrPlugin_interrupt_targetPrivilege;
   wire        when_CsrPlugin_l1296;
   wire        when_CsrPlugin_l1296_1;
   wire        when_CsrPlugin_l1302;
   wire        when_CsrPlugin_l1302_1;
   wire        when_CsrPlugin_l1302_2;
   wire        when_CsrPlugin_l1302_3;
   wire        when_CsrPlugin_l1302_4;
   wire        when_CsrPlugin_l1302_5;
   wire        when_CsrPlugin_l1302_6;
   wire        when_CsrPlugin_l1302_7;
   wire        when_CsrPlugin_l1302_8;
   wire        CsrPlugin_exception;
   reg         CsrPlugin_lastStageWasWfi;
   reg         CsrPlugin_pipelineLiberator_pcValids_0;
   reg         CsrPlugin_pipelineLiberator_pcValids_1;
   reg         CsrPlugin_pipelineLiberator_pcValids_2;
   wire        CsrPlugin_pipelineLiberator_active;
   wire        when_CsrPlugin_l1335;
   wire        when_CsrPlugin_l1335_1;
   wire        when_CsrPlugin_l1335_2;
   wire        when_CsrPlugin_l1340;
   reg         CsrPlugin_pipelineLiberator_done;
   wire        when_CsrPlugin_l1346;
   wire        CsrPlugin_interruptJump  /* verilator public */;
   reg         CsrPlugin_hadException  /* verilator public */;
   reg  [ 1:0] CsrPlugin_targetPrivilege;
   reg  [ 3:0] CsrPlugin_trapCause;
   wire        CsrPlugin_trapCauseEbreakDebug;
   reg  [ 1:0] CsrPlugin_xtvec_mode;
   reg  [29:0] CsrPlugin_xtvec_base;
   wire        CsrPlugin_trapEnterDebug;
   wire        when_CsrPlugin_l1390;
   wire        when_CsrPlugin_l1398;
   wire        when_CsrPlugin_l1456;
   wire [ 1:0] switch_CsrPlugin_l1460;
   wire        when_CsrPlugin_l1468;
   reg         execute_CsrPlugin_wfiWake;
   wire        when_CsrPlugin_l1519;
   wire        when_CsrPlugin_l1521;
   wire        when_CsrPlugin_l1527;
   wire        execute_CsrPlugin_blockedBySideEffects;
   reg         execute_CsrPlugin_illegalAccess;
   reg         execute_CsrPlugin_illegalInstruction;
   wire        when_CsrPlugin_l1540;
   wire        when_CsrPlugin_l1547;
   wire        when_CsrPlugin_l1548;
   wire        when_CsrPlugin_l1555;
   wire        when_CsrPlugin_l1565;
   reg         execute_CsrPlugin_writeInstruction;
   reg         execute_CsrPlugin_readInstruction;
   wire        execute_CsrPlugin_writeEnable;
   wire        execute_CsrPlugin_readEnable;
   reg  [31:0] execute_CsrPlugin_readToWriteData;
   wire        switch_Misc_l227_4;
   reg  [31:0] _zz_CsrPlugin_csrMapping_writeDataSignal;
   wire        when_CsrPlugin_l1587;
   wire        when_CsrPlugin_l1591;
   wire [11:0] execute_CsrPlugin_csrAddress;
   wire        when_Pipeline_l124;
   reg  [31:0] decode_to_execute_PC;
   wire        when_Pipeline_l124_1;
   reg  [31:0] execute_to_memory_PC;
   wire        when_Pipeline_l124_2;
   reg  [31:0] memory_to_writeBack_PC;
   wire        when_Pipeline_l124_3;
   reg  [31:0] decode_to_execute_INSTRUCTION;
   wire        when_Pipeline_l124_4;
   reg  [31:0] execute_to_memory_INSTRUCTION;
   wire        when_Pipeline_l124_5;
   reg  [31:0] memory_to_writeBack_INSTRUCTION;
   wire        when_Pipeline_l124_6;
   reg         decode_to_execute_IS_RVC;
   wire        when_Pipeline_l124_7;
   reg  [31:0] decode_to_execute_FORMAL_PC_NEXT;
   wire        when_Pipeline_l124_8;
   reg  [31:0] execute_to_memory_FORMAL_PC_NEXT;
   wire        when_Pipeline_l124_9;
   reg  [31:0] memory_to_writeBack_FORMAL_PC_NEXT;
   wire        when_Pipeline_l124_10;
   reg         decode_to_execute_MEMORY_FORCE_CONSTISTENCY;
   wire        when_Pipeline_l124_11;
   reg         decode_to_execute_RESCHEDULE_NEXT;
   wire        when_Pipeline_l124_12;
   reg  [ 1:0] decode_to_execute_SRC1_CTRL;
   wire        when_Pipeline_l124_13;
   reg         decode_to_execute_SRC_USE_SUB_LESS;
   wire        when_Pipeline_l124_14;
   reg         decode_to_execute_MEMORY_ENABLE;
   wire        when_Pipeline_l124_15;
   reg         execute_to_memory_MEMORY_ENABLE;
   wire        when_Pipeline_l124_16;
   reg         memory_to_writeBack_MEMORY_ENABLE;
   wire        when_Pipeline_l124_17;
   reg  [ 1:0] decode_to_execute_ALU_CTRL;
   wire        when_Pipeline_l124_18;
   reg  [ 1:0] decode_to_execute_SRC2_CTRL;
   wire        when_Pipeline_l124_19;
   reg         decode_to_execute_REGFILE_WRITE_VALID;
   wire        when_Pipeline_l124_20;
   reg         execute_to_memory_REGFILE_WRITE_VALID;
   wire        when_Pipeline_l124_21;
   reg         memory_to_writeBack_REGFILE_WRITE_VALID;
   wire        when_Pipeline_l124_22;
   reg         decode_to_execute_BYPASSABLE_EXECUTE_STAGE;
   wire        when_Pipeline_l124_23;
   reg         decode_to_execute_BYPASSABLE_MEMORY_STAGE;
   wire        when_Pipeline_l124_24;
   reg         execute_to_memory_BYPASSABLE_MEMORY_STAGE;
   wire        when_Pipeline_l124_25;
   reg         decode_to_execute_MEMORY_WR;
   wire        when_Pipeline_l124_26;
   reg         execute_to_memory_MEMORY_WR;
   wire        when_Pipeline_l124_27;
   reg         memory_to_writeBack_MEMORY_WR;
   wire        when_Pipeline_l124_28;
   reg         decode_to_execute_MEMORY_LRSC;
   wire        when_Pipeline_l124_29;
   reg         execute_to_memory_MEMORY_LRSC;
   wire        when_Pipeline_l124_30;
   reg         memory_to_writeBack_MEMORY_LRSC;
   wire        when_Pipeline_l124_31;
   reg         decode_to_execute_MEMORY_AMO;
   wire        when_Pipeline_l124_32;
   reg         decode_to_execute_MEMORY_MANAGMENT;
   wire        when_Pipeline_l124_33;
   reg         decode_to_execute_IS_SFENCE_VMA2;
   wire        when_Pipeline_l124_34;
   reg         decode_to_execute_SRC_LESS_UNSIGNED;
   wire        when_Pipeline_l124_35;
   reg  [ 1:0] decode_to_execute_ALU_BITWISE_CTRL;
   wire        when_Pipeline_l124_36;
   reg  [ 1:0] decode_to_execute_SHIFT_CTRL;
   wire        when_Pipeline_l124_37;
   reg  [ 1:0] execute_to_memory_SHIFT_CTRL;
   wire        when_Pipeline_l124_38;
   reg         decode_to_execute_IS_MUL;
   wire        when_Pipeline_l124_39;
   reg         execute_to_memory_IS_MUL;
   wire        when_Pipeline_l124_40;
   reg         memory_to_writeBack_IS_MUL;
   wire        when_Pipeline_l124_41;
   reg         decode_to_execute_IS_DIV;
   wire        when_Pipeline_l124_42;
   reg         execute_to_memory_IS_DIV;
   wire        when_Pipeline_l124_43;
   reg         decode_to_execute_IS_RS1_SIGNED;
   wire        when_Pipeline_l124_44;
   reg         decode_to_execute_IS_RS2_SIGNED;
   wire        when_Pipeline_l124_45;
   reg  [ 1:0] decode_to_execute_BRANCH_CTRL;
   wire        when_Pipeline_l124_46;
   reg         decode_to_execute_IS_CSR;
   wire        when_Pipeline_l124_47;
   reg  [ 2:0] decode_to_execute_ENV_CTRL;
   wire        when_Pipeline_l124_48;
   reg  [ 2:0] execute_to_memory_ENV_CTRL;
   wire        when_Pipeline_l124_49;
   reg  [ 2:0] memory_to_writeBack_ENV_CTRL;
   wire        when_Pipeline_l124_50;
   reg  [31:0] decode_to_execute_RS1;
   wire        when_Pipeline_l124_51;
   reg  [31:0] decode_to_execute_RS2;
   wire        when_Pipeline_l124_52;
   reg         decode_to_execute_SRC2_FORCE_ZERO;
   wire        when_Pipeline_l124_53;
   reg         decode_to_execute_CSR_WRITE_OPCODE;
   wire        when_Pipeline_l124_54;
   reg         decode_to_execute_CSR_READ_OPCODE;
   wire        when_Pipeline_l124_55;
   reg  [31:0] execute_to_memory_MEMORY_STORE_DATA_RF;
   wire        when_Pipeline_l124_56;
   reg  [31:0] memory_to_writeBack_MEMORY_STORE_DATA_RF;
   wire        when_Pipeline_l124_57;
   reg         execute_to_memory_IS_DBUS_SHARING;
   wire        when_Pipeline_l124_58;
   reg         memory_to_writeBack_IS_DBUS_SHARING;
   wire        when_Pipeline_l124_59;
   reg  [31:0] execute_to_memory_REGFILE_WRITE_DATA;
   wire        when_Pipeline_l124_60;
   reg  [31:0] memory_to_writeBack_REGFILE_WRITE_DATA;
   wire        when_Pipeline_l124_61;
   reg  [31:0] execute_to_memory_SHIFT_RIGHT;
   wire        when_Pipeline_l124_62;
   reg  [31:0] execute_to_memory_MUL_LL;
   wire        when_Pipeline_l124_63;
   reg  [33:0] execute_to_memory_MUL_LH;
   wire        when_Pipeline_l124_64;
   reg  [33:0] execute_to_memory_MUL_HL;
   wire        when_Pipeline_l124_65;
   reg  [33:0] execute_to_memory_MUL_HH;
   wire        when_Pipeline_l124_66;
   reg  [33:0] memory_to_writeBack_MUL_HH;
   wire        when_Pipeline_l124_67;
   reg         execute_to_memory_BRANCH_DO;
   wire        when_Pipeline_l124_68;
   reg  [31:0] execute_to_memory_BRANCH_CALC;
   wire        when_Pipeline_l124_69;
   reg  [51:0] memory_to_writeBack_MUL_LOW;
   wire        when_Pipeline_l151;
   wire        when_Pipeline_l154;
   wire        when_Pipeline_l151_1;
   wire        when_Pipeline_l154_1;
   wire        when_Pipeline_l151_2;
   wire        when_Pipeline_l154_2;
   wire        when_CsrPlugin_l1669;
   reg         execute_CsrPlugin_csr_768;
   wire        when_CsrPlugin_l1669_1;
   reg         execute_CsrPlugin_csr_256;
   wire        when_CsrPlugin_l1669_2;
   reg         execute_CsrPlugin_csr_384;
   wire        when_CsrPlugin_l1669_3;
   reg         execute_CsrPlugin_csr_3857;
   wire        when_CsrPlugin_l1669_4;
   reg         execute_CsrPlugin_csr_3858;
   wire        when_CsrPlugin_l1669_5;
   reg         execute_CsrPlugin_csr_3859;
   wire        when_CsrPlugin_l1669_6;
   reg         execute_CsrPlugin_csr_3860;
   wire        when_CsrPlugin_l1669_7;
   reg         execute_CsrPlugin_csr_769;
   wire        when_CsrPlugin_l1669_8;
   reg         execute_CsrPlugin_csr_836;
   wire        when_CsrPlugin_l1669_9;
   reg         execute_CsrPlugin_csr_772;
   wire        when_CsrPlugin_l1669_10;
   reg         execute_CsrPlugin_csr_773;
   wire        when_CsrPlugin_l1669_11;
   reg         execute_CsrPlugin_csr_833;
   wire        when_CsrPlugin_l1669_12;
   reg         execute_CsrPlugin_csr_832;
   wire        when_CsrPlugin_l1669_13;
   reg         execute_CsrPlugin_csr_834;
   wire        when_CsrPlugin_l1669_14;
   reg         execute_CsrPlugin_csr_835;
   wire        when_CsrPlugin_l1669_15;
   reg         execute_CsrPlugin_csr_2816;
   wire        when_CsrPlugin_l1669_16;
   reg         execute_CsrPlugin_csr_2944;
   wire        when_CsrPlugin_l1669_17;
   reg         execute_CsrPlugin_csr_2818;
   wire        when_CsrPlugin_l1669_18;
   reg         execute_CsrPlugin_csr_2946;
   wire        when_CsrPlugin_l1669_19;
   reg         execute_CsrPlugin_csr_770;
   wire        when_CsrPlugin_l1669_20;
   reg         execute_CsrPlugin_csr_771;
   wire        when_CsrPlugin_l1669_21;
   reg         execute_CsrPlugin_csr_3072;
   wire        when_CsrPlugin_l1669_22;
   reg         execute_CsrPlugin_csr_3200;
   wire        when_CsrPlugin_l1669_23;
   reg         execute_CsrPlugin_csr_3074;
   wire        when_CsrPlugin_l1669_24;
   reg         execute_CsrPlugin_csr_3202;
   wire        when_CsrPlugin_l1669_25;
   reg         execute_CsrPlugin_csr_3073;
   wire        when_CsrPlugin_l1669_26;
   reg         execute_CsrPlugin_csr_3201;
   wire        when_CsrPlugin_l1669_27;
   reg         execute_CsrPlugin_csr_774;
   wire        when_CsrPlugin_l1669_28;
   reg         execute_CsrPlugin_csr_262;
   wire        when_CsrPlugin_l1669_29;
   reg         execute_CsrPlugin_csr_324;
   wire        when_CsrPlugin_l1669_30;
   reg         execute_CsrPlugin_csr_260;
   wire        when_CsrPlugin_l1669_31;
   reg         execute_CsrPlugin_csr_261;
   wire        when_CsrPlugin_l1669_32;
   reg         execute_CsrPlugin_csr_321;
   wire        when_CsrPlugin_l1669_33;
   reg         execute_CsrPlugin_csr_320;
   wire        when_CsrPlugin_l1669_34;
   reg         execute_CsrPlugin_csr_322;
   wire        when_CsrPlugin_l1669_35;
   reg         execute_CsrPlugin_csr_323;
   wire [ 1:0] switch_CsrPlugin_l1031;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_1;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_2;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_3;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_4;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_5;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_6;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_7;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_8;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_9;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_10;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_11;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_12;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_13;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_14;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_15;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_16;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_17;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_18;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_19;
   wire        when_CsrPlugin_l1076;
   wire        when_CsrPlugin_l1077;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_20;
   wire        when_CsrPlugin_l1076_1;
   wire        when_CsrPlugin_l1077_1;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_21;
   wire        when_CsrPlugin_l1076_2;
   wire        when_CsrPlugin_l1077_2;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_22;
   wire        when_CsrPlugin_l1076_3;
   wire        when_CsrPlugin_l1077_3;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_23;
   wire        when_CsrPlugin_l1076_4;
   wire        when_CsrPlugin_l1077_4;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_24;
   wire        when_CsrPlugin_l1076_5;
   wire        when_CsrPlugin_l1077_5;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_25;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_26;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_27;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_28;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_29;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_30;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_31;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_32;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_33;
   reg  [31:0] _zz_CsrPlugin_csrMapping_readDataInit_34;
   wire        when_CsrPlugin_l1702;
   wire [11:0] _zz_when_CsrPlugin_l1709;
   wire        when_CsrPlugin_l1709;
   reg         when_CsrPlugin_l1719;
   wire        when_CsrPlugin_l1717;
   wire        when_CsrPlugin_l1725;
   wire [ 0:0] _zz_iBusAxi_arid;
   wire [ 3:0] _zz_iBusAxi_arregion;
   wire        dbus_axi_arw_valid;
   wire        dbus_axi_arw_ready;
   wire [31:0] dbus_axi_arw_payload_addr;
   wire [ 7:0] dbus_axi_arw_payload_len;
   wire [ 2:0] dbus_axi_arw_payload_size;
   wire [ 3:0] dbus_axi_arw_payload_cache;
   wire [ 2:0] dbus_axi_arw_payload_prot;
   wire        dbus_axi_arw_payload_write;
   wire        dbus_axi_w_valid;
   wire        dbus_axi_w_ready;
   wire [31:0] dbus_axi_w_payload_data;
   wire [ 3:0] dbus_axi_w_payload_strb;
   wire        dbus_axi_w_payload_last;
   wire        dbus_axi_b_valid;
   wire        dbus_axi_b_ready;
   wire [ 1:0] dbus_axi_b_payload_resp;
   wire        dbus_axi_r_valid;
   wire        dbus_axi_r_ready;
   wire [31:0] dbus_axi_r_payload_data;
   wire [ 1:0] dbus_axi_r_payload_resp;
   wire        dbus_axi_r_payload_last;
   wire        dBus_cmd_fire;
   wire        when_Utils_l659;
   wire        dbus_axi_b_fire;
   reg         _zz_when_Utils_l687;
   reg         _zz_when_Utils_l687_1;
   reg  [ 2:0] _zz_dBus_cmd_ready;
   reg  [ 2:0] _zz_dBus_cmd_ready_1;
   wire        when_Utils_l687;
   wire        when_Utils_l689;
   wire        _zz_dBus_cmd_ready_2;
   wire        _zz_dbus_axi_arw_valid;
   reg         _zz_dBus_cmd_ready_3;
   wire        _zz_dbus_axi_arw_payload_write;
   wire        _zz_dbus_axi_w_payload_last;
   wire        _zz_dbus_axi_arw_valid_1;
   reg         _zz_when_Stream_l998;
   wire        _zz_dbus_axi_w_valid;
   reg         _zz_when_Stream_l998_1;
   reg         _zz_when_Stream_l998_2;
   reg         _zz_when_Stream_l998_3;
   wire        when_Stream_l998;
   wire        when_Stream_l998_1;
   wire        _zz_6;
   reg         _zz_7;
   reg         _zz_dbus_axi_arw_valid_2;
   wire        when_Stream_l439;
   reg         _zz_dbus_axi_w_valid_1;
   wire [ 0:0] _zz_dBusAxi_arid;
   wire [ 3:0] _zz_dBusAxi_arregion;
   wire [ 0:0] _zz_dBusAxi_awid;
   wire [ 3:0] _zz_dBusAxi_awregion;
`ifndef SYNTHESIS
   reg [47:0] _zz_memory_to_writeBack_ENV_CTRL_string;
   reg [47:0] _zz_memory_to_writeBack_ENV_CTRL_1_string;
   reg [47:0] _zz_execute_to_memory_ENV_CTRL_string;
   reg [47:0] _zz_execute_to_memory_ENV_CTRL_1_string;
   reg [47:0] decode_ENV_CTRL_string;
   reg [47:0] _zz_decode_ENV_CTRL_string;
   reg [47:0] _zz_decode_to_execute_ENV_CTRL_string;
   reg [47:0] _zz_decode_to_execute_ENV_CTRL_1_string;
   reg [31:0] decode_BRANCH_CTRL_string;
   reg [31:0] _zz_decode_BRANCH_CTRL_string;
   reg [31:0] _zz_decode_to_execute_BRANCH_CTRL_string;
   reg [31:0] _zz_decode_to_execute_BRANCH_CTRL_1_string;
   reg [71:0] _zz_execute_to_memory_SHIFT_CTRL_string;
   reg [71:0] _zz_execute_to_memory_SHIFT_CTRL_1_string;
   reg [71:0] decode_SHIFT_CTRL_string;
   reg [71:0] _zz_decode_SHIFT_CTRL_string;
   reg [71:0] _zz_decode_to_execute_SHIFT_CTRL_string;
   reg [71:0] _zz_decode_to_execute_SHIFT_CTRL_1_string;
   reg [39:0] decode_ALU_BITWISE_CTRL_string;
   reg [39:0] _zz_decode_ALU_BITWISE_CTRL_string;
   reg [39:0] _zz_decode_to_execute_ALU_BITWISE_CTRL_string;
   reg [39:0] _zz_decode_to_execute_ALU_BITWISE_CTRL_1_string;
   reg [23:0] decode_SRC2_CTRL_string;
   reg [23:0] _zz_decode_SRC2_CTRL_string;
   reg [23:0] _zz_decode_to_execute_SRC2_CTRL_string;
   reg [23:0] _zz_decode_to_execute_SRC2_CTRL_1_string;
   reg [63:0] decode_ALU_CTRL_string;
   reg [63:0] _zz_decode_ALU_CTRL_string;
   reg [63:0] _zz_decode_to_execute_ALU_CTRL_string;
   reg [63:0] _zz_decode_to_execute_ALU_CTRL_1_string;
   reg [95:0] decode_SRC1_CTRL_string;
   reg [95:0] _zz_decode_SRC1_CTRL_string;
   reg [95:0] _zz_decode_to_execute_SRC1_CTRL_string;
   reg [95:0] _zz_decode_to_execute_SRC1_CTRL_1_string;
   reg [47:0] memory_ENV_CTRL_string;
   reg [47:0] _zz_memory_ENV_CTRL_string;
   reg [47:0] execute_ENV_CTRL_string;
   reg [47:0] _zz_execute_ENV_CTRL_string;
   reg [47:0] writeBack_ENV_CTRL_string;
   reg [47:0] _zz_writeBack_ENV_CTRL_string;
   reg [31:0] execute_BRANCH_CTRL_string;
   reg [31:0] _zz_execute_BRANCH_CTRL_string;
   reg [71:0] memory_SHIFT_CTRL_string;
   reg [71:0] _zz_memory_SHIFT_CTRL_string;
   reg [71:0] execute_SHIFT_CTRL_string;
   reg [71:0] _zz_execute_SHIFT_CTRL_string;
   reg [23:0] execute_SRC2_CTRL_string;
   reg [23:0] _zz_execute_SRC2_CTRL_string;
   reg [95:0] execute_SRC1_CTRL_string;
   reg [95:0] _zz_execute_SRC1_CTRL_string;
   reg [63:0] execute_ALU_CTRL_string;
   reg [63:0] _zz_execute_ALU_CTRL_string;
   reg [39:0] execute_ALU_BITWISE_CTRL_string;
   reg [39:0] _zz_execute_ALU_BITWISE_CTRL_string;
   reg [47:0] _zz_decode_ENV_CTRL_1_string;
   reg [31:0] _zz_decode_BRANCH_CTRL_1_string;
   reg [71:0] _zz_decode_SHIFT_CTRL_1_string;
   reg [39:0] _zz_decode_ALU_BITWISE_CTRL_1_string;
   reg [23:0] _zz_decode_SRC2_CTRL_1_string;
   reg [63:0] _zz_decode_ALU_CTRL_1_string;
   reg [95:0] _zz_decode_SRC1_CTRL_1_string;
   reg [47:0] MmuPlugin_shared_state_1_string;
   reg [95:0] _zz_decode_SRC1_CTRL_2_string;
   reg [63:0] _zz_decode_ALU_CTRL_2_string;
   reg [23:0] _zz_decode_SRC2_CTRL_2_string;
   reg [39:0] _zz_decode_ALU_BITWISE_CTRL_2_string;
   reg [71:0] _zz_decode_SHIFT_CTRL_2_string;
   reg [31:0] _zz_decode_BRANCH_CTRL_2_string;
   reg [47:0] _zz_decode_ENV_CTRL_2_string;
   reg [95:0] decode_to_execute_SRC1_CTRL_string;
   reg [63:0] decode_to_execute_ALU_CTRL_string;
   reg [23:0] decode_to_execute_SRC2_CTRL_string;
   reg [39:0] decode_to_execute_ALU_BITWISE_CTRL_string;
   reg [71:0] decode_to_execute_SHIFT_CTRL_string;
   reg [71:0] execute_to_memory_SHIFT_CTRL_string;
   reg [31:0] decode_to_execute_BRANCH_CTRL_string;
   reg [47:0] decode_to_execute_ENV_CTRL_string;
   reg [47:0] execute_to_memory_ENV_CTRL_string;
   reg [47:0] memory_to_writeBack_ENV_CTRL_string;
`endif

   reg [31:0] RegFilePlugin_regFile[0:31]  /* verilator public */;

   assign _zz_when = ({decodeExceptionPort_valid,IBusCachedPlugin_decodeExceptionPort_valid} != 2'b00);
   assign _zz_memory_MUL_LOW = ($signed(_zz_memory_MUL_LOW_1) + $signed(_zz_memory_MUL_LOW_4));
   assign _zz_memory_MUL_LOW_1 = ($signed(52'h0000000000000) + $signed(_zz_memory_MUL_LOW_2));
   assign _zz_memory_MUL_LOW_3 = {1'b0, memory_MUL_LL};
   assign _zz_memory_MUL_LOW_2 = {{19{_zz_memory_MUL_LOW_3[32]}}, _zz_memory_MUL_LOW_3};
   assign _zz_memory_MUL_LOW_5 = ({16'd0, memory_MUL_LH} <<< 5'd16);
   assign _zz_memory_MUL_LOW_4 = {{2{_zz_memory_MUL_LOW_5[49]}}, _zz_memory_MUL_LOW_5};
   assign _zz_memory_MUL_LOW_7 = ({16'd0, memory_MUL_HL} <<< 5'd16);
   assign _zz_memory_MUL_LOW_6 = {{2{_zz_memory_MUL_LOW_7[49]}}, _zz_memory_MUL_LOW_7};
   assign _zz_execute_SHIFT_RIGHT_1 = ($signed(
       _zz_execute_SHIFT_RIGHT_2
   ) >>> execute_FullBarrelShifterPlugin_amplitude);
   assign _zz_execute_SHIFT_RIGHT = _zz_execute_SHIFT_RIGHT_1[31 : 0];
   assign _zz_execute_SHIFT_RIGHT_2 = {
      ((execute_SHIFT_CTRL == ShiftCtrlEnum_SRA_1) && execute_FullBarrelShifterPlugin_reversed[31]),
      execute_FullBarrelShifterPlugin_reversed
   };
   assign _zz_decode_FORMAL_PC_NEXT_1 = (decode_IS_RVC ? 3'b010 : 3'b100);
   assign _zz_decode_FORMAL_PC_NEXT = {29'd0, _zz_decode_FORMAL_PC_NEXT_1};
   assign _zz_MmuPlugin_ioEndAddr = (ioStartAddr + ioSize);
   assign _zz__zz_IBusCachedPlugin_jump_pcLoad_payload_1 = (_zz_IBusCachedPlugin_jump_pcLoad_payload - 4'b0001);
   assign _zz_IBusCachedPlugin_fetchPc_pc_1 = {IBusCachedPlugin_fetchPc_inc, 2'b00};
   assign _zz_IBusCachedPlugin_fetchPc_pc = {29'd0, _zz_IBusCachedPlugin_fetchPc_pc_1};
   assign _zz_IBusCachedPlugin_decodePc_pcPlus_1 = (decode_IS_RVC ? 3'b010 : 3'b100);
   assign _zz_IBusCachedPlugin_decodePc_pcPlus = {29'd0, _zz_IBusCachedPlugin_decodePc_pcPlus_1};
   assign _zz_IBusCachedPlugin_decompressor_decompressed_27 = {
      {
         _zz_IBusCachedPlugin_decompressor_decompressed_10,
         _zz_IBusCachedPlugin_decompressor_decompressed[6 : 2]
      },
      12'h000
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_34 = {
      {
         {4'b0000, _zz_IBusCachedPlugin_decompressor_decompressed[8 : 7]},
         _zz_IBusCachedPlugin_decompressor_decompressed[12 : 9]
      },
      2'b00
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_35 = {
      {
         {4'b0000, _zz_IBusCachedPlugin_decompressor_decompressed[8 : 7]},
         _zz_IBusCachedPlugin_decompressor_decompressed[12 : 9]
      },
      2'b00
   };
   assign _zz_io_cpu_flush_payload_lineId = _zz_io_cpu_flush_payload_lineId_1;
   assign _zz_io_cpu_flush_payload_lineId_1 = (execute_RS1 >>> 3'd6);
   assign _zz_DBusCachedPlugin_exceptionBus_payload_code = (writeBack_MEMORY_WR ? 3'b111 : 3'b101);
   assign _zz_DBusCachedPlugin_exceptionBus_payload_code_1 = (writeBack_MEMORY_WR ? 3'b110 : 3'b100);
   assign _zz_writeBack_DBusCachedPlugin_rspRf = (!dataCache_1_io_cpu_writeBack_exclusiveOk);
   assign _zz_MmuPlugin_ports_0_entryToReplace_valueNext_1 = MmuPlugin_ports_0_entryToReplace_willIncrement;
   assign _zz_MmuPlugin_ports_0_entryToReplace_valueNext = {
      1'd0, _zz_MmuPlugin_ports_0_entryToReplace_valueNext_1
   };
   assign _zz_MmuPlugin_ports_1_entryToReplace_valueNext_1 = MmuPlugin_ports_1_entryToReplace_willIncrement;
   assign _zz_MmuPlugin_ports_1_entryToReplace_valueNext = {
      1'd0, _zz_MmuPlugin_ports_1_entryToReplace_valueNext_1
   };
   assign _zz__zz_MmuPlugin_shared_refills_2 = (_zz_MmuPlugin_shared_refills_1 - 2'b01);
   assign _zz__zz_execute_REGFILE_WRITE_DATA = execute_SRC_LESS;
   assign _zz__zz_execute_SRC1 = (execute_IS_RVC ? 3'b010 : 3'b100);
   assign _zz__zz_execute_SRC1_1 = execute_INSTRUCTION[19 : 15];
   assign _zz__zz_execute_SRC2_2 = {execute_INSTRUCTION[31 : 25], execute_INSTRUCTION[11 : 7]};
   assign _zz_execute_SrcPlugin_addSub = ($signed(
       _zz_execute_SrcPlugin_addSub_1
   ) + $signed(
       _zz_execute_SrcPlugin_addSub_4
   ));
   assign _zz_execute_SrcPlugin_addSub_1 = ($signed(
       _zz_execute_SrcPlugin_addSub_2
   ) + $signed(
       _zz_execute_SrcPlugin_addSub_3
   ));
   assign _zz_execute_SrcPlugin_addSub_2 = execute_SRC1;
   assign _zz_execute_SrcPlugin_addSub_3 = (execute_SRC_USE_SUB_LESS ? (~ execute_SRC2) : execute_SRC2);
   assign _zz_execute_SrcPlugin_addSub_4 = (execute_SRC_USE_SUB_LESS ? 32'h00000001 : 32'h00000000);
   assign _zz_writeBack_MulPlugin_result = {{14{writeBack_MUL_LOW[51]}}, writeBack_MUL_LOW};
   assign _zz_writeBack_MulPlugin_result_1 = ({32'd0, writeBack_MUL_HH} <<< 6'd32);
   assign _zz__zz_decode_RS2_2 = writeBack_MUL_LOW[31 : 0];
   assign _zz__zz_decode_RS2_2_1 = writeBack_MulPlugin_result[63 : 32];
   assign _zz_memory_DivPlugin_div_counter_valueNext_1 = memory_DivPlugin_div_counter_willIncrement;
   assign _zz_memory_DivPlugin_div_counter_valueNext = {
      5'd0, _zz_memory_DivPlugin_div_counter_valueNext_1
   };
   assign _zz_memory_DivPlugin_div_stage_0_remainderMinusDenominator = {1'd0, memory_DivPlugin_rs2};
   assign _zz_memory_DivPlugin_div_stage_0_outRemainder = memory_DivPlugin_div_stage_0_remainderMinusDenominator[31:0];
   assign _zz_memory_DivPlugin_div_stage_0_outRemainder_1 = memory_DivPlugin_div_stage_0_remainderShifted[31:0];
   assign _zz_memory_DivPlugin_div_stage_0_outNumerator = {
      _zz_memory_DivPlugin_div_stage_0_remainderShifted,
      (!memory_DivPlugin_div_stage_0_remainderMinusDenominator[32])
   };
   assign _zz_memory_DivPlugin_div_result_1 = _zz_memory_DivPlugin_div_result_2;
   assign _zz_memory_DivPlugin_div_result_2 = _zz_memory_DivPlugin_div_result_3;
   assign _zz_memory_DivPlugin_div_result_3 = ({memory_DivPlugin_div_needRevert,(memory_DivPlugin_div_needRevert ? (~ _zz_memory_DivPlugin_div_result) : _zz_memory_DivPlugin_div_result)} + _zz_memory_DivPlugin_div_result_4);
   assign _zz_memory_DivPlugin_div_result_5 = memory_DivPlugin_div_needRevert;
   assign _zz_memory_DivPlugin_div_result_4 = {32'd0, _zz_memory_DivPlugin_div_result_5};
   assign _zz_memory_DivPlugin_rs1_3 = _zz_memory_DivPlugin_rs1;
   assign _zz_memory_DivPlugin_rs1_2 = {32'd0, _zz_memory_DivPlugin_rs1_3};
   assign _zz_memory_DivPlugin_rs2_2 = _zz_memory_DivPlugin_rs2;
   assign _zz_memory_DivPlugin_rs2_1 = {31'd0, _zz_memory_DivPlugin_rs2_2};
   assign _zz__zz_execute_BranchPlugin_branch_src2 = {
      {{execute_INSTRUCTION[31], execute_INSTRUCTION[19 : 12]}, execute_INSTRUCTION[20]},
      execute_INSTRUCTION[30 : 21]
   };
   assign _zz__zz_execute_BranchPlugin_branch_src2_4 = {
      {{execute_INSTRUCTION[31], execute_INSTRUCTION[7]}, execute_INSTRUCTION[30 : 25]},
      execute_INSTRUCTION[11 : 8]
   };
   assign _zz__zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1 = (_zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code & (~ _zz__zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1_1));
   assign _zz__zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1_1 = (_zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code - 2'b01);
   assign _zz_dbus_axi_arw_payload_len = ((dBus_cmd_payload_size == 3'b110) ? 4'b1111 : 4'b0000);
   assign _zz_decode_RegFilePlugin_rs1Data = 1'b1;
   assign _zz_decode_RegFilePlugin_rs2Data = 1'b1;
   assign _zz_IBusCachedPlugin_jump_pcLoad_payload_6 = {
      _zz_IBusCachedPlugin_jump_pcLoad_payload_4, _zz_IBusCachedPlugin_jump_pcLoad_payload_3
   };
   assign _zz_writeBack_DBusCachedPlugin_rspShifted_1 = dataCache_1_io_cpu_writeBack_address[1 : 0];
   assign _zz_writeBack_DBusCachedPlugin_rspShifted_3 = dataCache_1_io_cpu_writeBack_address[1 : 1];
   assign _zz_decode_LEGAL_INSTRUCTION = 32'h0000207f;
   assign _zz_decode_LEGAL_INSTRUCTION_1 = (decode_INSTRUCTION & 32'h0000407f);
   assign _zz_decode_LEGAL_INSTRUCTION_2 = 32'h00004063;
   assign _zz_decode_LEGAL_INSTRUCTION_3 = ((decode_INSTRUCTION & 32'h0000207f) == 32'h00002013);
   assign _zz_decode_LEGAL_INSTRUCTION_4 = ((decode_INSTRUCTION & 32'h0000107f) == 32'h00000013);
   assign _zz_decode_LEGAL_INSTRUCTION_5 = {
      ((decode_INSTRUCTION & 32'h0000603f) == 32'h00000023),
      {
         ((decode_INSTRUCTION & 32'h0000207f) == 32'h00000003),
         {
            ((decode_INSTRUCTION & _zz_decode_LEGAL_INSTRUCTION_6) == 32'h00000003),
            {
               (_zz_decode_LEGAL_INSTRUCTION_7 == _zz_decode_LEGAL_INSTRUCTION_8),
               {
                  _zz_decode_LEGAL_INSTRUCTION_9,
                  {_zz_decode_LEGAL_INSTRUCTION_10, _zz_decode_LEGAL_INSTRUCTION_11}
               }
            }
         }
      }
   };
   assign _zz_decode_LEGAL_INSTRUCTION_6 = 32'h0000505f;
   assign _zz_decode_LEGAL_INSTRUCTION_7 = (decode_INSTRUCTION & 32'h0000707b);
   assign _zz_decode_LEGAL_INSTRUCTION_8 = 32'h00000063;
   assign _zz_decode_LEGAL_INSTRUCTION_9 = ((decode_INSTRUCTION & 32'h0000607f) == 32'h0000000f);
   assign _zz_decode_LEGAL_INSTRUCTION_10 = ((decode_INSTRUCTION & 32'h1800707f) == 32'h0000202f);
   assign _zz_decode_LEGAL_INSTRUCTION_11 = {
      ((decode_INSTRUCTION & 32'hfc00007f) == 32'h00000033),
      {
         ((decode_INSTRUCTION & 32'he800707f) == 32'h0800202f),
         {
            ((decode_INSTRUCTION & _zz_decode_LEGAL_INSTRUCTION_12) == 32'h0000500f),
            {
               (_zz_decode_LEGAL_INSTRUCTION_13 == _zz_decode_LEGAL_INSTRUCTION_14),
               {
                  _zz_decode_LEGAL_INSTRUCTION_15,
                  {_zz_decode_LEGAL_INSTRUCTION_16, _zz_decode_LEGAL_INSTRUCTION_17}
               }
            }
         }
      }
   };
   assign _zz_decode_LEGAL_INSTRUCTION_12 = 32'h01f0707f;
   assign _zz_decode_LEGAL_INSTRUCTION_13 = (decode_INSTRUCTION & 32'hbe00705f);
   assign _zz_decode_LEGAL_INSTRUCTION_14 = 32'h00005013;
   assign _zz_decode_LEGAL_INSTRUCTION_15 = ((decode_INSTRUCTION & 32'hfe00305f) == 32'h00001013);
   assign _zz_decode_LEGAL_INSTRUCTION_16 = ((decode_INSTRUCTION & 32'hbe00707f) == 32'h00000033);
   assign _zz_decode_LEGAL_INSTRUCTION_17 = {
      ((decode_INSTRUCTION & 32'hf9f0707f) == 32'h1000202f),
      {
         ((decode_INSTRUCTION & 32'hfe007fff) == 32'h12000073),
         {
            ((decode_INSTRUCTION & _zz_decode_LEGAL_INSTRUCTION_18) == 32'h10200073),
            {
               (_zz_decode_LEGAL_INSTRUCTION_19 == _zz_decode_LEGAL_INSTRUCTION_20),
               (_zz_decode_LEGAL_INSTRUCTION_21 == _zz_decode_LEGAL_INSTRUCTION_22)
            }
         }
      }
   };
   assign _zz_decode_LEGAL_INSTRUCTION_18 = 32'hdfffffff;
   assign _zz_decode_LEGAL_INSTRUCTION_19 = (decode_INSTRUCTION & 32'hffefffff);
   assign _zz_decode_LEGAL_INSTRUCTION_20 = 32'h00000073;
   assign _zz_decode_LEGAL_INSTRUCTION_21 = (decode_INSTRUCTION & 32'hffffffff);
   assign _zz_decode_LEGAL_INSTRUCTION_22 = 32'h10500073;
   assign _zz_IBusCachedPlugin_decompressor_decompressed_28 = (_zz_IBusCachedPlugin_decompressor_decompressed[11 : 10] == 2'b01);
   assign _zz_IBusCachedPlugin_decompressor_decompressed_29 = ((_zz_IBusCachedPlugin_decompressor_decompressed[11 : 10] == 2'b11) && (_zz_IBusCachedPlugin_decompressor_decompressed[6 : 5] == 2'b00));
   assign _zz_IBusCachedPlugin_decompressor_decompressed_30 = 7'h00;
   assign _zz_IBusCachedPlugin_decompressor_decompressed_31 = _zz_IBusCachedPlugin_decompressor_decompressed[6 : 2];
   assign _zz_IBusCachedPlugin_decompressor_decompressed_32 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   assign _zz_IBusCachedPlugin_decompressor_decompressed_33 = _zz_IBusCachedPlugin_decompressor_decompressed[11 : 7];
   assign _zz_MmuPlugin_ports_0_cacheHitsCalc = IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22];
   assign _zz_MmuPlugin_ports_0_cacheHitsCalc_1 = IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12];
   assign _zz_MmuPlugin_ports_0_cacheHitsCalc_2 = (MmuPlugin_ports_0_cache_1_virtualAddress_1 == IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22]);
   assign _zz_MmuPlugin_ports_0_cacheHitsCalc_3 = (MmuPlugin_ports_0_cache_1_virtualAddress_0 == IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12]);
   assign _zz_MmuPlugin_ports_0_cacheHitsCalc_4 = (MmuPlugin_ports_0_cache_0_virtualAddress_1 == IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22]);
   assign _zz_MmuPlugin_ports_0_cacheHitsCalc_5 = (MmuPlugin_ports_0_cache_0_virtualAddress_0 == IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12]);
   assign _zz_MmuPlugin_ports_1_cacheHitsCalc = DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22];
   assign _zz_MmuPlugin_ports_1_cacheHitsCalc_1 = DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12];
   assign _zz_MmuPlugin_ports_1_cacheHitsCalc_2 = (MmuPlugin_ports_1_cache_1_virtualAddress_1 == DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22]);
   assign _zz_MmuPlugin_ports_1_cacheHitsCalc_3 = (MmuPlugin_ports_1_cache_1_virtualAddress_0 == DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12]);
   assign _zz_MmuPlugin_ports_1_cacheHitsCalc_4 = (MmuPlugin_ports_1_cache_0_virtualAddress_1 == DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22]);
   assign _zz_MmuPlugin_ports_1_cacheHitsCalc_5 = (MmuPlugin_ports_1_cache_0_virtualAddress_0 == DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12]);
   assign _zz__zz_decode_IS_CSR = (decode_INSTRUCTION & 32'h10103050);
   assign _zz__zz_decode_IS_CSR_1 = 32'h00000050;
   assign _zz__zz_decode_IS_CSR_2 = (decode_INSTRUCTION & 32'h12203050);
   assign _zz__zz_decode_IS_CSR_3 = 32'h10000050;
   assign _zz__zz_decode_IS_CSR_4 = (decode_INSTRUCTION & 32'h02103050);
   assign _zz__zz_decode_IS_CSR_5 = 32'h00000050;
   assign _zz__zz_decode_IS_CSR_6 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_7) == 32'h00001050);
   assign _zz__zz_decode_IS_CSR_8 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_9) == 32'h00002050);
   assign _zz__zz_decode_IS_CSR_10 = {
      _zz_decode_IS_CSR_4, (_zz__zz_decode_IS_CSR_11 == _zz__zz_decode_IS_CSR_12)
   };
   assign _zz__zz_decode_IS_CSR_13 = (|(_zz__zz_decode_IS_CSR_14 == _zz__zz_decode_IS_CSR_15));
   assign _zz__zz_decode_IS_CSR_16 = (|_zz_decode_IS_CSR_10);
   assign _zz__zz_decode_IS_CSR_17 = {
      (|_zz__zz_decode_IS_CSR_18),
      {_zz__zz_decode_IS_CSR_19, {_zz__zz_decode_IS_CSR_20, _zz__zz_decode_IS_CSR_22}}
   };
   assign _zz__zz_decode_IS_CSR_7 = 32'h00001050;
   assign _zz__zz_decode_IS_CSR_9 = 32'h00002050;
   assign _zz__zz_decode_IS_CSR_11 = (decode_INSTRUCTION & 32'h0000001c);
   assign _zz__zz_decode_IS_CSR_12 = 32'h00000004;
   assign _zz__zz_decode_IS_CSR_14 = (decode_INSTRUCTION & 32'h00000058);
   assign _zz__zz_decode_IS_CSR_15 = 32'h00000040;
   assign _zz__zz_decode_IS_CSR_18 = _zz_decode_IS_CSR_10;
   assign _zz__zz_decode_IS_CSR_19 = (|((decode_INSTRUCTION & 32'h02004064) == 32'h02004020));
   assign _zz__zz_decode_IS_CSR_20 = (|((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_21) == 32'h02000030));
   assign _zz__zz_decode_IS_CSR_22 = {
      (|(_zz__zz_decode_IS_CSR_23 == _zz__zz_decode_IS_CSR_24)),
      {
         (|{_zz__zz_decode_IS_CSR_25, _zz__zz_decode_IS_CSR_26}),
         {
            (|_zz__zz_decode_IS_CSR_27),
            {_zz__zz_decode_IS_CSR_28, {_zz__zz_decode_IS_CSR_30, _zz__zz_decode_IS_CSR_32}}
         }
      }
   };
   assign _zz__zz_decode_IS_CSR_21 = 32'h02004074;
   assign _zz__zz_decode_IS_CSR_23 = (decode_INSTRUCTION & 32'h02007054);
   assign _zz__zz_decode_IS_CSR_24 = 32'h00005010;
   assign _zz__zz_decode_IS_CSR_25 = ((decode_INSTRUCTION & 32'h40003054) == 32'h40001010);
   assign _zz__zz_decode_IS_CSR_26 = ((decode_INSTRUCTION & 32'h02007054) == 32'h00001010);
   assign _zz__zz_decode_IS_CSR_27 = ((decode_INSTRUCTION & 32'h00001000) == 32'h00001000);
   assign _zz__zz_decode_IS_CSR_28 = (|((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_29) == 32'h00002000));
   assign _zz__zz_decode_IS_CSR_30 = (|{_zz_decode_IS_CSR_9, _zz__zz_decode_IS_CSR_31});
   assign _zz__zz_decode_IS_CSR_32 = {
      (|_zz_decode_IS_CSR_2),
      {
         (|_zz__zz_decode_IS_CSR_33),
         {_zz__zz_decode_IS_CSR_34, {_zz__zz_decode_IS_CSR_36, _zz__zz_decode_IS_CSR_45}}
      }
   };
   assign _zz__zz_decode_IS_CSR_29 = 32'h00003000;
   assign _zz__zz_decode_IS_CSR_31 = ((decode_INSTRUCTION & 32'h00005000) == 32'h00001000);
   assign _zz__zz_decode_IS_CSR_33 = ((decode_INSTRUCTION & 32'h00004048) == 32'h00004008);
   assign _zz__zz_decode_IS_CSR_34 = (|((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_35) == 32'h00000024));
   assign _zz__zz_decode_IS_CSR_36 = (|{_zz__zz_decode_IS_CSR_37, {
      _zz__zz_decode_IS_CSR_38, _zz__zz_decode_IS_CSR_40
   }});
   assign _zz__zz_decode_IS_CSR_45 = {
      (|_zz__zz_decode_IS_CSR_46),
      {
         (|_zz__zz_decode_IS_CSR_47),
         {_zz__zz_decode_IS_CSR_49, {_zz__zz_decode_IS_CSR_62, _zz__zz_decode_IS_CSR_71}}
      }
   };
   assign _zz__zz_decode_IS_CSR_35 = 32'h00000064;
   assign _zz__zz_decode_IS_CSR_37 = ((decode_INSTRUCTION & 32'h00000034) == 32'h00000020);
   assign _zz__zz_decode_IS_CSR_38 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_39) == 32'h00000020);
   assign _zz__zz_decode_IS_CSR_40 = {
      (_zz__zz_decode_IS_CSR_41 == _zz__zz_decode_IS_CSR_42),
      (_zz__zz_decode_IS_CSR_43 == _zz__zz_decode_IS_CSR_44)
   };
   assign _zz__zz_decode_IS_CSR_46 = ((decode_INSTRUCTION & 32'h10000008) == 32'h00000008);
   assign _zz__zz_decode_IS_CSR_47 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_48) == 32'h10000008);
   assign _zz__zz_decode_IS_CSR_49 = (|{_zz__zz_decode_IS_CSR_50, {
      _zz__zz_decode_IS_CSR_52, _zz__zz_decode_IS_CSR_55
   }});
   assign _zz__zz_decode_IS_CSR_62 = (|{_zz__zz_decode_IS_CSR_63, _zz__zz_decode_IS_CSR_66});
   assign _zz__zz_decode_IS_CSR_71 = {
      (|_zz__zz_decode_IS_CSR_72),
      {_zz__zz_decode_IS_CSR_85, {_zz__zz_decode_IS_CSR_98, _zz__zz_decode_IS_CSR_114}}
   };
   assign _zz__zz_decode_IS_CSR_39 = 32'h00000064;
   assign _zz__zz_decode_IS_CSR_41 = (decode_INSTRUCTION & 32'h08000070);
   assign _zz__zz_decode_IS_CSR_42 = 32'h08000020;
   assign _zz__zz_decode_IS_CSR_43 = (decode_INSTRUCTION & 32'h10000070);
   assign _zz__zz_decode_IS_CSR_44 = 32'h00000020;
   assign _zz__zz_decode_IS_CSR_48 = 32'h10000008;
   assign _zz__zz_decode_IS_CSR_50 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_51) == 32'h00002040);
   assign _zz__zz_decode_IS_CSR_52 = (_zz__zz_decode_IS_CSR_53 == _zz__zz_decode_IS_CSR_54);
   assign _zz__zz_decode_IS_CSR_55 = {
      _zz__zz_decode_IS_CSR_56, {_zz__zz_decode_IS_CSR_58, _zz__zz_decode_IS_CSR_59}
   };
   assign _zz__zz_decode_IS_CSR_63 = (_zz__zz_decode_IS_CSR_64 == _zz__zz_decode_IS_CSR_65);
   assign _zz__zz_decode_IS_CSR_66 = {_zz__zz_decode_IS_CSR_67, _zz__zz_decode_IS_CSR_69};
   assign _zz__zz_decode_IS_CSR_72 = {
      _zz__zz_decode_IS_CSR_73, {_zz__zz_decode_IS_CSR_75, _zz__zz_decode_IS_CSR_78}
   };
   assign _zz__zz_decode_IS_CSR_85 = (|{_zz__zz_decode_IS_CSR_86, _zz__zz_decode_IS_CSR_87});
   assign _zz__zz_decode_IS_CSR_98 = (|_zz__zz_decode_IS_CSR_99);
   assign _zz__zz_decode_IS_CSR_114 = {
      _zz__zz_decode_IS_CSR_115, {_zz__zz_decode_IS_CSR_120, _zz__zz_decode_IS_CSR_124}
   };
   assign _zz__zz_decode_IS_CSR_51 = 32'h00002040;
   assign _zz__zz_decode_IS_CSR_53 = (decode_INSTRUCTION & 32'h00001040);
   assign _zz__zz_decode_IS_CSR_54 = 32'h00001040;
   assign _zz__zz_decode_IS_CSR_56 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_57) == 32'h00000040);
   assign _zz__zz_decode_IS_CSR_58 = _zz_decode_IS_CSR_9;
   assign _zz__zz_decode_IS_CSR_59 = {_zz_decode_IS_CSR_6, _zz__zz_decode_IS_CSR_60};
   assign _zz__zz_decode_IS_CSR_64 = (decode_INSTRUCTION & 32'h08000020);
   assign _zz__zz_decode_IS_CSR_65 = 32'h08000020;
   assign _zz__zz_decode_IS_CSR_67 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_68) == 32'h00000020);
   assign _zz__zz_decode_IS_CSR_69 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_70) == 32'h00000020);
   assign _zz__zz_decode_IS_CSR_73 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_74) == 32'h00000040);
   assign _zz__zz_decode_IS_CSR_75 = (_zz__zz_decode_IS_CSR_76 == _zz__zz_decode_IS_CSR_77);
   assign _zz__zz_decode_IS_CSR_78 = {
      _zz__zz_decode_IS_CSR_79, {_zz__zz_decode_IS_CSR_81, _zz__zz_decode_IS_CSR_84}
   };
   assign _zz__zz_decode_IS_CSR_86 = _zz_decode_IS_CSR_8;
   assign _zz__zz_decode_IS_CSR_87 = {
      _zz__zz_decode_IS_CSR_88, {_zz__zz_decode_IS_CSR_90, _zz__zz_decode_IS_CSR_93}
   };
   assign _zz__zz_decode_IS_CSR_99 = {
      _zz_decode_IS_CSR_4, {_zz__zz_decode_IS_CSR_100, _zz__zz_decode_IS_CSR_103}
   };
   assign _zz__zz_decode_IS_CSR_115 = (|{_zz__zz_decode_IS_CSR_116, _zz__zz_decode_IS_CSR_117});
   assign _zz__zz_decode_IS_CSR_120 = (|_zz__zz_decode_IS_CSR_121);
   assign _zz__zz_decode_IS_CSR_124 = {
      _zz__zz_decode_IS_CSR_125, {_zz__zz_decode_IS_CSR_128, _zz__zz_decode_IS_CSR_132}
   };
   assign _zz__zz_decode_IS_CSR_57 = 32'h00000050;
   assign _zz__zz_decode_IS_CSR_60 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_61) == 32'h00000040);
   assign _zz__zz_decode_IS_CSR_68 = 32'h10000020;
   assign _zz__zz_decode_IS_CSR_70 = 32'h00000028;
   assign _zz__zz_decode_IS_CSR_74 = 32'h00000040;
   assign _zz__zz_decode_IS_CSR_76 = (decode_INSTRUCTION & 32'h00004020);
   assign _zz__zz_decode_IS_CSR_77 = 32'h00004020;
   assign _zz__zz_decode_IS_CSR_79 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_80) == 32'h00000010);
   assign _zz__zz_decode_IS_CSR_81 = (_zz__zz_decode_IS_CSR_82 == _zz__zz_decode_IS_CSR_83);
   assign _zz__zz_decode_IS_CSR_84 = _zz_decode_IS_CSR_8;
   assign _zz__zz_decode_IS_CSR_88 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_89) == 32'h00002010);
   assign _zz__zz_decode_IS_CSR_90 = (_zz__zz_decode_IS_CSR_91 == _zz__zz_decode_IS_CSR_92);
   assign _zz__zz_decode_IS_CSR_93 = {_zz__zz_decode_IS_CSR_94, _zz__zz_decode_IS_CSR_96};
   assign _zz__zz_decode_IS_CSR_100 = (_zz__zz_decode_IS_CSR_101 == _zz__zz_decode_IS_CSR_102);
   assign _zz__zz_decode_IS_CSR_103 = {
      _zz__zz_decode_IS_CSR_104, {_zz__zz_decode_IS_CSR_106, _zz__zz_decode_IS_CSR_109}
   };
   assign _zz__zz_decode_IS_CSR_116 = _zz_decode_IS_CSR_7;
   assign _zz__zz_decode_IS_CSR_117 = (_zz__zz_decode_IS_CSR_118 == _zz__zz_decode_IS_CSR_119);
   assign _zz__zz_decode_IS_CSR_121 = {_zz_decode_IS_CSR_7, _zz__zz_decode_IS_CSR_122};
   assign _zz__zz_decode_IS_CSR_125 = (|_zz__zz_decode_IS_CSR_126);
   assign _zz__zz_decode_IS_CSR_128 = (|_zz__zz_decode_IS_CSR_129);
   assign _zz__zz_decode_IS_CSR_132 = {
      _zz__zz_decode_IS_CSR_133, {_zz__zz_decode_IS_CSR_144, _zz__zz_decode_IS_CSR_148}
   };
   assign _zz__zz_decode_IS_CSR_61 = 32'h02400040;
   assign _zz__zz_decode_IS_CSR_80 = 32'h00000030;
   assign _zz__zz_decode_IS_CSR_82 = (decode_INSTRUCTION & 32'h02000010);
   assign _zz__zz_decode_IS_CSR_83 = 32'h00000010;
   assign _zz__zz_decode_IS_CSR_89 = 32'h00002030;
   assign _zz__zz_decode_IS_CSR_91 = (decode_INSTRUCTION & 32'h00001030);
   assign _zz__zz_decode_IS_CSR_92 = 32'h00000010;
   assign _zz__zz_decode_IS_CSR_94 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_95) == 32'h00000020);
   assign _zz__zz_decode_IS_CSR_96 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_97) == 32'h00002020);
   assign _zz__zz_decode_IS_CSR_101 = (decode_INSTRUCTION & 32'h00001010);
   assign _zz__zz_decode_IS_CSR_102 = 32'h00001010;
   assign _zz__zz_decode_IS_CSR_104 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_105) == 32'h00002010);
   assign _zz__zz_decode_IS_CSR_106 = (_zz__zz_decode_IS_CSR_107 == _zz__zz_decode_IS_CSR_108);
   assign _zz__zz_decode_IS_CSR_109 = {
      _zz__zz_decode_IS_CSR_110, {_zz__zz_decode_IS_CSR_111, _zz__zz_decode_IS_CSR_112}
   };
   assign _zz__zz_decode_IS_CSR_118 = (decode_INSTRUCTION & 32'h00000070);
   assign _zz__zz_decode_IS_CSR_119 = 32'h00000020;
   assign _zz__zz_decode_IS_CSR_122 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_123) == 32'h00000000);
   assign _zz__zz_decode_IS_CSR_126 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_127) == 32'h00004010);
   assign _zz__zz_decode_IS_CSR_129 = (_zz__zz_decode_IS_CSR_130 == _zz__zz_decode_IS_CSR_131);
   assign _zz__zz_decode_IS_CSR_133 = (|{_zz__zz_decode_IS_CSR_134, _zz__zz_decode_IS_CSR_136});
   assign _zz__zz_decode_IS_CSR_144 = (|_zz__zz_decode_IS_CSR_145);
   assign _zz__zz_decode_IS_CSR_148 = {
      _zz__zz_decode_IS_CSR_149, {_zz__zz_decode_IS_CSR_158, _zz__zz_decode_IS_CSR_162}
   };
   assign _zz__zz_decode_IS_CSR_95 = 32'h02003020;
   assign _zz__zz_decode_IS_CSR_97 = 32'h02002068;
   assign _zz__zz_decode_IS_CSR_105 = 32'h00002010;
   assign _zz__zz_decode_IS_CSR_107 = (decode_INSTRUCTION & 32'h00002008);
   assign _zz__zz_decode_IS_CSR_108 = 32'h00002008;
   assign _zz__zz_decode_IS_CSR_110 = ((decode_INSTRUCTION & 32'h00000050) == 32'h00000010);
   assign _zz__zz_decode_IS_CSR_111 = _zz_decode_IS_CSR_8;
   assign _zz__zz_decode_IS_CSR_112 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_113) == 32'h00000000);
   assign _zz__zz_decode_IS_CSR_123 = 32'h00000020;
   assign _zz__zz_decode_IS_CSR_127 = 32'h00004014;
   assign _zz__zz_decode_IS_CSR_130 = (decode_INSTRUCTION & 32'h00006014);
   assign _zz__zz_decode_IS_CSR_131 = 32'h00002010;
   assign _zz__zz_decode_IS_CSR_134 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_135) == 32'h00000000);
   assign _zz__zz_decode_IS_CSR_136 = {
      _zz_decode_IS_CSR_6,
      {_zz__zz_decode_IS_CSR_137, {_zz__zz_decode_IS_CSR_139, _zz__zz_decode_IS_CSR_142}}
   };
   assign _zz__zz_decode_IS_CSR_145 = {
      _zz_decode_IS_CSR_5, (_zz__zz_decode_IS_CSR_146 == _zz__zz_decode_IS_CSR_147)
   };
   assign _zz__zz_decode_IS_CSR_149 = (|{_zz__zz_decode_IS_CSR_150, {
      _zz__zz_decode_IS_CSR_152, _zz__zz_decode_IS_CSR_155
   }});
   assign _zz__zz_decode_IS_CSR_158 = (|{_zz__zz_decode_IS_CSR_159, _zz__zz_decode_IS_CSR_160});
   assign _zz__zz_decode_IS_CSR_162 = {
      (|_zz__zz_decode_IS_CSR_163), {_zz__zz_decode_IS_CSR_165, _zz__zz_decode_IS_CSR_168}
   };
   assign _zz__zz_decode_IS_CSR_113 = 32'h00000028;
   assign _zz__zz_decode_IS_CSR_135 = 32'h00000044;
   assign _zz__zz_decode_IS_CSR_137 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_138) == 32'h00002000);
   assign _zz__zz_decode_IS_CSR_139 = (_zz__zz_decode_IS_CSR_140 == _zz__zz_decode_IS_CSR_141);
   assign _zz__zz_decode_IS_CSR_142 = {_zz__zz_decode_IS_CSR_143, _zz_decode_IS_CSR_5};
   assign _zz__zz_decode_IS_CSR_146 = (decode_INSTRUCTION & 32'h00000058);
   assign _zz__zz_decode_IS_CSR_147 = 32'h00000000;
   assign _zz__zz_decode_IS_CSR_150 = ((decode_INSTRUCTION & _zz__zz_decode_IS_CSR_151) == 32'h00000040);
   assign _zz__zz_decode_IS_CSR_152 = (_zz__zz_decode_IS_CSR_153 == _zz__zz_decode_IS_CSR_154);
   assign _zz__zz_decode_IS_CSR_155 = (_zz__zz_decode_IS_CSR_156 == _zz__zz_decode_IS_CSR_157);
   assign _zz__zz_decode_IS_CSR_159 = _zz_decode_IS_CSR_4;
   assign _zz__zz_decode_IS_CSR_160 = {_zz_decode_IS_CSR_3, _zz__zz_decode_IS_CSR_161};
   assign _zz__zz_decode_IS_CSR_163 = {_zz_decode_IS_CSR_3, _zz__zz_decode_IS_CSR_164};
   assign _zz__zz_decode_IS_CSR_165 = (|{_zz__zz_decode_IS_CSR_166, _zz__zz_decode_IS_CSR_167});
   assign _zz__zz_decode_IS_CSR_168 = (|_zz_decode_IS_CSR_1);
   assign _zz__zz_decode_IS_CSR_138 = 32'h00006004;
   assign _zz__zz_decode_IS_CSR_140 = (decode_INSTRUCTION & 32'h00005004);
   assign _zz__zz_decode_IS_CSR_141 = 32'h00001000;
   assign _zz__zz_decode_IS_CSR_143 = ((decode_INSTRUCTION & 32'h00004050) == 32'h00004000);
   assign _zz__zz_decode_IS_CSR_151 = 32'h00000044;
   assign _zz__zz_decode_IS_CSR_153 = (decode_INSTRUCTION & 32'h00002014);
   assign _zz__zz_decode_IS_CSR_154 = 32'h00002010;
   assign _zz__zz_decode_IS_CSR_156 = (decode_INSTRUCTION & 32'h40000034);
   assign _zz__zz_decode_IS_CSR_157 = 32'h40000030;
   assign _zz__zz_decode_IS_CSR_161 = ((decode_INSTRUCTION & 32'h00002014) == 32'h00000004);
   assign _zz__zz_decode_IS_CSR_164 = ((decode_INSTRUCTION & 32'h0000004c) == 32'h00000004);
   assign _zz__zz_decode_IS_CSR_166 = _zz_decode_IS_CSR_1;
   assign _zz__zz_decode_IS_CSR_167 = _zz_decode_IS_CSR_2;
   assign _zz_CsrPlugin_csrMapping_readDataInit_35 = (_zz_CsrPlugin_csrMapping_readDataInit | _zz_CsrPlugin_csrMapping_readDataInit_1);
   assign _zz_CsrPlugin_csrMapping_readDataInit_36 = (_zz_CsrPlugin_csrMapping_readDataInit_2 | _zz_CsrPlugin_csrMapping_readDataInit_3);
   assign _zz_CsrPlugin_csrMapping_readDataInit_37 = (_zz_CsrPlugin_csrMapping_readDataInit_4 | _zz_CsrPlugin_csrMapping_readDataInit_5);
   assign _zz_CsrPlugin_csrMapping_readDataInit_38 = (_zz_CsrPlugin_csrMapping_readDataInit_39 | _zz_CsrPlugin_csrMapping_readDataInit_6);
   assign _zz_CsrPlugin_csrMapping_readDataInit_40 = (_zz_CsrPlugin_csrMapping_readDataInit_7 | _zz_CsrPlugin_csrMapping_readDataInit_8);
   assign _zz_CsrPlugin_csrMapping_readDataInit_41 = (_zz_CsrPlugin_csrMapping_readDataInit_9 | _zz_CsrPlugin_csrMapping_readDataInit_10);
   assign _zz_CsrPlugin_csrMapping_readDataInit_42 = (_zz_CsrPlugin_csrMapping_readDataInit_11 | _zz_CsrPlugin_csrMapping_readDataInit_12);
   assign _zz_CsrPlugin_csrMapping_readDataInit_43 = (_zz_CsrPlugin_csrMapping_readDataInit_13 | _zz_CsrPlugin_csrMapping_readDataInit_14);
   assign _zz_CsrPlugin_csrMapping_readDataInit_44 = (_zz_CsrPlugin_csrMapping_readDataInit_15 | _zz_CsrPlugin_csrMapping_readDataInit_16);
   assign _zz_CsrPlugin_csrMapping_readDataInit_45 = (_zz_CsrPlugin_csrMapping_readDataInit_17 | _zz_CsrPlugin_csrMapping_readDataInit_18);
   assign _zz_CsrPlugin_csrMapping_readDataInit_46 = (_zz_CsrPlugin_csrMapping_readDataInit_19 | _zz_CsrPlugin_csrMapping_readDataInit_20);
   assign _zz_CsrPlugin_csrMapping_readDataInit_47 = (_zz_CsrPlugin_csrMapping_readDataInit_21 | _zz_CsrPlugin_csrMapping_readDataInit_22);
   assign _zz_CsrPlugin_csrMapping_readDataInit_48 = (_zz_CsrPlugin_csrMapping_readDataInit_23 | _zz_CsrPlugin_csrMapping_readDataInit_24);
   assign _zz_CsrPlugin_csrMapping_readDataInit_49 = (_zz_CsrPlugin_csrMapping_readDataInit_25 | _zz_CsrPlugin_csrMapping_readDataInit_26);
   assign _zz_CsrPlugin_csrMapping_readDataInit_50 = (_zz_CsrPlugin_csrMapping_readDataInit_27 | _zz_CsrPlugin_csrMapping_readDataInit_28);
   assign _zz_CsrPlugin_csrMapping_readDataInit_51 = (_zz_CsrPlugin_csrMapping_readDataInit_29 | _zz_CsrPlugin_csrMapping_readDataInit_30);
   assign _zz_CsrPlugin_csrMapping_readDataInit_39 = 32'h00000000;
   always @(posedge clk) begin
      if (_zz_decode_RegFilePlugin_rs1Data) begin
         _zz_RegFilePlugin_regFile_port0 <= RegFilePlugin_regFile[decode_RegFilePlugin_regFileReadAddress1];
      end
   end

   always @(posedge clk) begin
      if (_zz_decode_RegFilePlugin_rs2Data) begin
         _zz_RegFilePlugin_regFile_port1 <= RegFilePlugin_regFile[decode_RegFilePlugin_regFileReadAddress2];
      end
   end

   always @(posedge clk) begin
      if (_zz_1) begin
         RegFilePlugin_regFile[lastStageRegFileWrite_payload_address] <= lastStageRegFileWrite_payload_data;
      end
   end

   AxiLite4Clint clintCtrl (
      .io_bus_aw_valid       (clint_awvalid),                          //i
      .io_bus_aw_ready       (clintCtrl_io_bus_aw_ready),              //o
      .io_bus_aw_payload_addr(clint_awaddr[15:0]),                     //i
      .io_bus_aw_payload_prot(clint_awprot[2:0]),                      //i
      .io_bus_w_valid        (clint_wvalid),                           //i
      .io_bus_w_ready        (clintCtrl_io_bus_w_ready),               //o
      .io_bus_w_payload_data (clint_wdata[31:0]),                      //i
      .io_bus_w_payload_strb (clint_wstrb[3:0]),                       //i
      .io_bus_b_valid        (clintCtrl_io_bus_b_valid),               //o
      .io_bus_b_ready        (clint_bready),                           //i
      .io_bus_b_payload_resp (clintCtrl_io_bus_b_payload_resp[1:0]),   //o
      .io_bus_ar_valid       (clint_arvalid),                          //i
      .io_bus_ar_ready       (clintCtrl_io_bus_ar_ready),              //o
      .io_bus_ar_payload_addr(clint_araddr[15:0]),                     //i
      .io_bus_ar_payload_prot(clint_arprot[2:0]),                      //i
      .io_bus_r_valid        (clintCtrl_io_bus_r_valid),               //o
      .io_bus_r_ready        (clint_rready),                           //i
      .io_bus_r_payload_data (clintCtrl_io_bus_r_payload_data[31:0]),  //o
      .io_bus_r_payload_resp (clintCtrl_io_bus_r_payload_resp[1:0]),   //o
      .io_timerInterrupt     (clintCtrl_io_timerInterrupt),            //o
      .io_softwareInterrupt  (clintCtrl_io_softwareInterrupt),         //o
      .io_time               (clintCtrl_io_time[63:0]),                //o
      .clk                   (clk),                                    //i
      .reset                 (reset)                                   //i
   );
   AxiLite4Plic plicCtrl (
      .io_bus_aw_valid       (plic_awvalid),                          //i
      .io_bus_aw_ready       (plicCtrl_io_bus_aw_ready),              //o
      .io_bus_aw_payload_addr(plic_awaddr[21:0]),                     //i
      .io_bus_aw_payload_prot(plic_awprot[2:0]),                      //i
      .io_bus_w_valid        (plic_wvalid),                           //i
      .io_bus_w_ready        (plicCtrl_io_bus_w_ready),               //o
      .io_bus_w_payload_data (plic_wdata[31:0]),                      //i
      .io_bus_w_payload_strb (plic_wstrb[3:0]),                       //i
      .io_bus_b_valid        (plicCtrl_io_bus_b_valid),               //o
      .io_bus_b_ready        (plic_bready),                           //i
      .io_bus_b_payload_resp (plicCtrl_io_bus_b_payload_resp[1:0]),   //o
      .io_bus_ar_valid       (plic_arvalid),                          //i
      .io_bus_ar_ready       (plicCtrl_io_bus_ar_ready),              //o
      .io_bus_ar_payload_addr(plic_araddr[21:0]),                     //i
      .io_bus_ar_payload_prot(plic_arprot[2:0]),                      //i
      .io_bus_r_valid        (plicCtrl_io_bus_r_valid),               //o
      .io_bus_r_ready        (plic_rready),                           //i
      .io_bus_r_payload_data (plicCtrl_io_bus_r_payload_data[31:0]),  //o
      .io_bus_r_payload_resp (plicCtrl_io_bus_r_payload_resp[1:0]),   //o
      .io_sources            (plicCtrl_io_sources[30:0]),             //i
      .io_targets            (plicCtrl_io_targets[1:0]),              //o
      .clk                   (clk),                                   //i
      .reset                 (reset)                                  //i
   );
   InstructionCache IBusCachedPlugin_cache (
      .io_flush(IBusCachedPlugin_cache_io_flush),  //i
      .io_cpu_prefetch_isValid(IBusCachedPlugin_cache_io_cpu_prefetch_isValid),  //i
      .io_cpu_prefetch_haltIt(IBusCachedPlugin_cache_io_cpu_prefetch_haltIt),  //o
      .io_cpu_prefetch_pc(IBusCachedPlugin_iBusRsp_stages_0_input_payload[31:0]),  //i
      .io_cpu_fetch_isValid(IBusCachedPlugin_cache_io_cpu_fetch_isValid),  //i
      .io_cpu_fetch_isStuck(IBusCachedPlugin_cache_io_cpu_fetch_isStuck),  //i
      .io_cpu_fetch_isRemoved(IBusCachedPlugin_cache_io_cpu_fetch_isRemoved),  //i
      .io_cpu_fetch_pc(IBusCachedPlugin_iBusRsp_stages_1_input_payload[31:0]),  //i
      .io_cpu_fetch_data(IBusCachedPlugin_cache_io_cpu_fetch_data[31:0]),  //o
      .io_cpu_fetch_mmuRsp_physicalAddress(IBusCachedPlugin_mmuBus_rsp_physicalAddress[31:0]),  //i
      .io_cpu_fetch_mmuRsp_isIoAccess(IBusCachedPlugin_mmuBus_rsp_isIoAccess),  //i
      .io_cpu_fetch_mmuRsp_isPaging(IBusCachedPlugin_mmuBus_rsp_isPaging),  //i
      .io_cpu_fetch_mmuRsp_allowRead(IBusCachedPlugin_mmuBus_rsp_allowRead),  //i
      .io_cpu_fetch_mmuRsp_allowWrite(IBusCachedPlugin_mmuBus_rsp_allowWrite),  //i
      .io_cpu_fetch_mmuRsp_allowExecute(IBusCachedPlugin_mmuBus_rsp_allowExecute),  //i
      .io_cpu_fetch_mmuRsp_exception(IBusCachedPlugin_mmuBus_rsp_exception),  //i
      .io_cpu_fetch_mmuRsp_refilling(IBusCachedPlugin_mmuBus_rsp_refilling),  //i
      .io_cpu_fetch_mmuRsp_bypassTranslation(IBusCachedPlugin_mmuBus_rsp_bypassTranslation),  //i
      .io_cpu_fetch_mmuRsp_ways_0_sel(IBusCachedPlugin_mmuBus_rsp_ways_0_sel),  //i
      .io_cpu_fetch_mmuRsp_ways_0_physical(IBusCachedPlugin_mmuBus_rsp_ways_0_physical[31:0]),  //i
      .io_cpu_fetch_mmuRsp_ways_1_sel(IBusCachedPlugin_mmuBus_rsp_ways_1_sel),  //i
      .io_cpu_fetch_mmuRsp_ways_1_physical(IBusCachedPlugin_mmuBus_rsp_ways_1_physical[31:0]),  //i
      .io_cpu_fetch_mmuRsp_ways_2_sel(IBusCachedPlugin_mmuBus_rsp_ways_2_sel),  //i
      .io_cpu_fetch_mmuRsp_ways_2_physical(IBusCachedPlugin_mmuBus_rsp_ways_2_physical[31:0]),  //i
      .io_cpu_fetch_mmuRsp_ways_3_sel(IBusCachedPlugin_mmuBus_rsp_ways_3_sel),  //i
      .io_cpu_fetch_mmuRsp_ways_3_physical(IBusCachedPlugin_mmuBus_rsp_ways_3_physical[31:0]),  //i
      .io_cpu_fetch_physicalAddress(IBusCachedPlugin_cache_io_cpu_fetch_physicalAddress[31:0]),  //o
      .io_cpu_decode_isValid(IBusCachedPlugin_cache_io_cpu_decode_isValid),  //i
      .io_cpu_decode_isStuck(IBusCachedPlugin_cache_io_cpu_decode_isStuck),  //i
      .io_cpu_decode_pc(IBusCachedPlugin_iBusRsp_stages_2_input_payload[31:0]),  //i
      .io_cpu_decode_physicalAddress         (IBusCachedPlugin_cache_io_cpu_decode_physicalAddress[31:0]), //o
      .io_cpu_decode_data(IBusCachedPlugin_cache_io_cpu_decode_data[31:0]),  //o
      .io_cpu_decode_cacheMiss(IBusCachedPlugin_cache_io_cpu_decode_cacheMiss),  //o
      .io_cpu_decode_error(IBusCachedPlugin_cache_io_cpu_decode_error),  //o
      .io_cpu_decode_mmuRefilling(IBusCachedPlugin_cache_io_cpu_decode_mmuRefilling),  //o
      .io_cpu_decode_mmuException(IBusCachedPlugin_cache_io_cpu_decode_mmuException),  //o
      .io_cpu_decode_isUser(IBusCachedPlugin_cache_io_cpu_decode_isUser),  //i
      .io_cpu_fill_valid(IBusCachedPlugin_cache_io_cpu_fill_valid),  //i
      .io_cpu_fill_payload(IBusCachedPlugin_cache_io_cpu_decode_physicalAddress[31:0]),  //i
      .io_mem_cmd_valid(IBusCachedPlugin_cache_io_mem_cmd_valid),  //o
      .io_mem_cmd_ready(iBus_cmd_ready),  //i
      .io_mem_cmd_payload_address(IBusCachedPlugin_cache_io_mem_cmd_payload_address[31:0]),  //o
      .io_mem_cmd_payload_size(IBusCachedPlugin_cache_io_mem_cmd_payload_size[2:0]),  //o
      .io_mem_rsp_valid(iBus_rsp_valid),  //i
      .io_mem_rsp_payload_data(iBus_rsp_payload_data[31:0]),  //i
      .io_mem_rsp_payload_error(iBus_rsp_payload_error),  //i
      .clk(clk),  //i
      .reset(reset)  //i
   );
   DataCache dataCache_1 (
      .io_cpu_execute_isValid(dataCache_1_io_cpu_execute_isValid),  //i
      .io_cpu_execute_address(dataCache_1_io_cpu_execute_address[31:0]),  //i
      .io_cpu_execute_haltIt(dataCache_1_io_cpu_execute_haltIt),  //o
      .io_cpu_execute_args_wr(dataCache_1_io_cpu_execute_args_wr),  //i
      .io_cpu_execute_args_size(dataCache_1_io_cpu_execute_args_size[1:0]),  //i
      .io_cpu_execute_args_isLrsc(dataCache_1_io_cpu_execute_args_isLrsc),  //i
      .io_cpu_execute_args_isAmo(execute_MEMORY_AMO),  //i
      .io_cpu_execute_args_amoCtrl_swap(dataCache_1_io_cpu_execute_args_amoCtrl_swap),  //i
      .io_cpu_execute_args_amoCtrl_alu(dataCache_1_io_cpu_execute_args_amoCtrl_alu[2:0]),  //i
      .io_cpu_execute_args_totalyConsistent(execute_MEMORY_FORCE_CONSTISTENCY),  //i
      .io_cpu_execute_refilling(dataCache_1_io_cpu_execute_refilling),  //o
      .io_cpu_memory_isValid(dataCache_1_io_cpu_memory_isValid),  //i
      .io_cpu_memory_isStuck(memory_arbitration_isStuck),  //i
      .io_cpu_memory_isWrite(dataCache_1_io_cpu_memory_isWrite),  //o
      .io_cpu_memory_address(dataCache_1_io_cpu_memory_address[31:0]),  //i
      .io_cpu_memory_mmuRsp_physicalAddress(DBusCachedPlugin_mmuBus_rsp_physicalAddress[31:0]),  //i
      .io_cpu_memory_mmuRsp_isIoAccess(dataCache_1_io_cpu_memory_mmuRsp_isIoAccess),  //i
      .io_cpu_memory_mmuRsp_isPaging(DBusCachedPlugin_mmuBus_rsp_isPaging),  //i
      .io_cpu_memory_mmuRsp_allowRead(DBusCachedPlugin_mmuBus_rsp_allowRead),  //i
      .io_cpu_memory_mmuRsp_allowWrite(DBusCachedPlugin_mmuBus_rsp_allowWrite),  //i
      .io_cpu_memory_mmuRsp_allowExecute(DBusCachedPlugin_mmuBus_rsp_allowExecute),  //i
      .io_cpu_memory_mmuRsp_exception(DBusCachedPlugin_mmuBus_rsp_exception),  //i
      .io_cpu_memory_mmuRsp_refilling(DBusCachedPlugin_mmuBus_rsp_refilling),  //i
      .io_cpu_memory_mmuRsp_bypassTranslation(DBusCachedPlugin_mmuBus_rsp_bypassTranslation),  //i
      .io_cpu_memory_mmuRsp_ways_0_sel(DBusCachedPlugin_mmuBus_rsp_ways_0_sel),  //i
      .io_cpu_memory_mmuRsp_ways_0_physical(DBusCachedPlugin_mmuBus_rsp_ways_0_physical[31:0]),  //i
      .io_cpu_memory_mmuRsp_ways_1_sel(DBusCachedPlugin_mmuBus_rsp_ways_1_sel),  //i
      .io_cpu_memory_mmuRsp_ways_1_physical(DBusCachedPlugin_mmuBus_rsp_ways_1_physical[31:0]),  //i
      .io_cpu_memory_mmuRsp_ways_2_sel(DBusCachedPlugin_mmuBus_rsp_ways_2_sel),  //i
      .io_cpu_memory_mmuRsp_ways_2_physical(DBusCachedPlugin_mmuBus_rsp_ways_2_physical[31:0]),  //i
      .io_cpu_memory_mmuRsp_ways_3_sel(DBusCachedPlugin_mmuBus_rsp_ways_3_sel),  //i
      .io_cpu_memory_mmuRsp_ways_3_physical(DBusCachedPlugin_mmuBus_rsp_ways_3_physical[31:0]),  //i
      .io_cpu_writeBack_isValid(dataCache_1_io_cpu_writeBack_isValid),  //i
      .io_cpu_writeBack_isStuck(writeBack_arbitration_isStuck),  //i
      .io_cpu_writeBack_isFiring(writeBack_arbitration_isFiring),  //i
      .io_cpu_writeBack_isUser(dataCache_1_io_cpu_writeBack_isUser),  //i
      .io_cpu_writeBack_haltIt(dataCache_1_io_cpu_writeBack_haltIt),  //o
      .io_cpu_writeBack_isWrite(dataCache_1_io_cpu_writeBack_isWrite),  //o
      .io_cpu_writeBack_storeData(dataCache_1_io_cpu_writeBack_storeData[31:0]),  //i
      .io_cpu_writeBack_data(dataCache_1_io_cpu_writeBack_data[31:0]),  //o
      .io_cpu_writeBack_address(dataCache_1_io_cpu_writeBack_address[31:0]),  //i
      .io_cpu_writeBack_mmuException(dataCache_1_io_cpu_writeBack_mmuException),  //o
      .io_cpu_writeBack_unalignedAccess(dataCache_1_io_cpu_writeBack_unalignedAccess),  //o
      .io_cpu_writeBack_accessError(dataCache_1_io_cpu_writeBack_accessError),  //o
      .io_cpu_writeBack_keepMemRspData(dataCache_1_io_cpu_writeBack_keepMemRspData),  //o
      .io_cpu_writeBack_fence_SW(dataCache_1_io_cpu_writeBack_fence_SW),  //i
      .io_cpu_writeBack_fence_SR(dataCache_1_io_cpu_writeBack_fence_SR),  //i
      .io_cpu_writeBack_fence_SO(dataCache_1_io_cpu_writeBack_fence_SO),  //i
      .io_cpu_writeBack_fence_SI(dataCache_1_io_cpu_writeBack_fence_SI),  //i
      .io_cpu_writeBack_fence_PW(dataCache_1_io_cpu_writeBack_fence_PW),  //i
      .io_cpu_writeBack_fence_PR(dataCache_1_io_cpu_writeBack_fence_PR),  //i
      .io_cpu_writeBack_fence_PO(dataCache_1_io_cpu_writeBack_fence_PO),  //i
      .io_cpu_writeBack_fence_PI(dataCache_1_io_cpu_writeBack_fence_PI),  //i
      .io_cpu_writeBack_fence_FM(dataCache_1_io_cpu_writeBack_fence_FM[3:0]),  //i
      .io_cpu_writeBack_exclusiveOk(dataCache_1_io_cpu_writeBack_exclusiveOk),  //o
      .io_cpu_redo(dataCache_1_io_cpu_redo),  //o
      .io_cpu_flush_valid(dataCache_1_io_cpu_flush_valid),  //i
      .io_cpu_flush_ready(dataCache_1_io_cpu_flush_ready),  //o
      .io_cpu_flush_payload_singleLine(dataCache_1_io_cpu_flush_payload_singleLine),  //i
      .io_cpu_flush_payload_lineId(dataCache_1_io_cpu_flush_payload_lineId[5:0]),  //i
      .io_cpu_writesPending(dataCache_1_io_cpu_writesPending),  //o
      .io_mem_cmd_valid(dataCache_1_io_mem_cmd_valid),  //o
      .io_mem_cmd_ready(dBus_cmd_ready),  //i
      .io_mem_cmd_payload_wr(dataCache_1_io_mem_cmd_payload_wr),  //o
      .io_mem_cmd_payload_uncached(dataCache_1_io_mem_cmd_payload_uncached),  //o
      .io_mem_cmd_payload_address(dataCache_1_io_mem_cmd_payload_address[31:0]),  //o
      .io_mem_cmd_payload_data(dataCache_1_io_mem_cmd_payload_data[31:0]),  //o
      .io_mem_cmd_payload_mask(dataCache_1_io_mem_cmd_payload_mask[3:0]),  //o
      .io_mem_cmd_payload_size(dataCache_1_io_mem_cmd_payload_size[2:0]),  //o
      .io_mem_cmd_payload_last(dataCache_1_io_mem_cmd_payload_last),  //o
      .io_mem_rsp_valid(dBus_rsp_valid),  //i
      .io_mem_rsp_payload_last(dBus_rsp_payload_last),  //i
      .io_mem_rsp_payload_data(dBus_rsp_payload_data[31:0]),  //i
      .io_mem_rsp_payload_error(dBus_rsp_payload_error),  //i
      .clk(clk),  //i
      .reset(reset)  //i
   );
   always @(*) begin
      case (_zz_IBusCachedPlugin_jump_pcLoad_payload_6)
         2'b00:   _zz_IBusCachedPlugin_jump_pcLoad_payload_5 = DBusCachedPlugin_redoBranch_payload;
         2'b01:   _zz_IBusCachedPlugin_jump_pcLoad_payload_5 = CsrPlugin_jumpInterface_payload;
         2'b10:   _zz_IBusCachedPlugin_jump_pcLoad_payload_5 = BranchPlugin_jumpInterface_payload;
         default: _zz_IBusCachedPlugin_jump_pcLoad_payload_5 = CsrPlugin_redoInterface_payload;
      endcase
   end

   always @(*) begin
      case (_zz_writeBack_DBusCachedPlugin_rspShifted_1)
         2'b00: _zz_writeBack_DBusCachedPlugin_rspShifted = writeBack_DBusCachedPlugin_rspSplits_0;
         2'b01: _zz_writeBack_DBusCachedPlugin_rspShifted = writeBack_DBusCachedPlugin_rspSplits_1;
         2'b10: _zz_writeBack_DBusCachedPlugin_rspShifted = writeBack_DBusCachedPlugin_rspSplits_2;
         default:
         _zz_writeBack_DBusCachedPlugin_rspShifted = writeBack_DBusCachedPlugin_rspSplits_3;
      endcase
   end

   always @(*) begin
      case (_zz_writeBack_DBusCachedPlugin_rspShifted_3)
         1'b0: _zz_writeBack_DBusCachedPlugin_rspShifted_2 = writeBack_DBusCachedPlugin_rspSplits_1;
         default:
         _zz_writeBack_DBusCachedPlugin_rspShifted_2 = writeBack_DBusCachedPlugin_rspSplits_3;
      endcase
   end

   always @(*) begin
      case (_zz_MmuPlugin_ports_0_cacheLine_valid_3)
         2'b00: begin
            _zz_MmuPlugin_ports_0_cacheLine_valid_4 = MmuPlugin_ports_0_cache_0_valid;
            _zz_MmuPlugin_ports_0_cacheLine_exception = MmuPlugin_ports_0_cache_0_exception;
            _zz_MmuPlugin_ports_0_cacheLine_superPage = MmuPlugin_ports_0_cache_0_superPage;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_0 = MmuPlugin_ports_0_cache_0_virtualAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_1 = MmuPlugin_ports_0_cache_0_virtualAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_0 = MmuPlugin_ports_0_cache_0_physicalAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_1 = MmuPlugin_ports_0_cache_0_physicalAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_allowRead = MmuPlugin_ports_0_cache_0_allowRead;
            _zz_MmuPlugin_ports_0_cacheLine_allowWrite = MmuPlugin_ports_0_cache_0_allowWrite;
            _zz_MmuPlugin_ports_0_cacheLine_allowExecute = MmuPlugin_ports_0_cache_0_allowExecute;
            _zz_MmuPlugin_ports_0_cacheLine_allowUser = MmuPlugin_ports_0_cache_0_allowUser;
         end
         2'b01: begin
            _zz_MmuPlugin_ports_0_cacheLine_valid_4 = MmuPlugin_ports_0_cache_1_valid;
            _zz_MmuPlugin_ports_0_cacheLine_exception = MmuPlugin_ports_0_cache_1_exception;
            _zz_MmuPlugin_ports_0_cacheLine_superPage = MmuPlugin_ports_0_cache_1_superPage;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_0 = MmuPlugin_ports_0_cache_1_virtualAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_1 = MmuPlugin_ports_0_cache_1_virtualAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_0 = MmuPlugin_ports_0_cache_1_physicalAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_1 = MmuPlugin_ports_0_cache_1_physicalAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_allowRead = MmuPlugin_ports_0_cache_1_allowRead;
            _zz_MmuPlugin_ports_0_cacheLine_allowWrite = MmuPlugin_ports_0_cache_1_allowWrite;
            _zz_MmuPlugin_ports_0_cacheLine_allowExecute = MmuPlugin_ports_0_cache_1_allowExecute;
            _zz_MmuPlugin_ports_0_cacheLine_allowUser = MmuPlugin_ports_0_cache_1_allowUser;
         end
         2'b10: begin
            _zz_MmuPlugin_ports_0_cacheLine_valid_4 = MmuPlugin_ports_0_cache_2_valid;
            _zz_MmuPlugin_ports_0_cacheLine_exception = MmuPlugin_ports_0_cache_2_exception;
            _zz_MmuPlugin_ports_0_cacheLine_superPage = MmuPlugin_ports_0_cache_2_superPage;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_0 = MmuPlugin_ports_0_cache_2_virtualAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_1 = MmuPlugin_ports_0_cache_2_virtualAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_0 = MmuPlugin_ports_0_cache_2_physicalAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_1 = MmuPlugin_ports_0_cache_2_physicalAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_allowRead = MmuPlugin_ports_0_cache_2_allowRead;
            _zz_MmuPlugin_ports_0_cacheLine_allowWrite = MmuPlugin_ports_0_cache_2_allowWrite;
            _zz_MmuPlugin_ports_0_cacheLine_allowExecute = MmuPlugin_ports_0_cache_2_allowExecute;
            _zz_MmuPlugin_ports_0_cacheLine_allowUser = MmuPlugin_ports_0_cache_2_allowUser;
         end
         default: begin
            _zz_MmuPlugin_ports_0_cacheLine_valid_4 = MmuPlugin_ports_0_cache_3_valid;
            _zz_MmuPlugin_ports_0_cacheLine_exception = MmuPlugin_ports_0_cache_3_exception;
            _zz_MmuPlugin_ports_0_cacheLine_superPage = MmuPlugin_ports_0_cache_3_superPage;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_0 = MmuPlugin_ports_0_cache_3_virtualAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_1 = MmuPlugin_ports_0_cache_3_virtualAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_0 = MmuPlugin_ports_0_cache_3_physicalAddress_0;
            _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_1 = MmuPlugin_ports_0_cache_3_physicalAddress_1;
            _zz_MmuPlugin_ports_0_cacheLine_allowRead = MmuPlugin_ports_0_cache_3_allowRead;
            _zz_MmuPlugin_ports_0_cacheLine_allowWrite = MmuPlugin_ports_0_cache_3_allowWrite;
            _zz_MmuPlugin_ports_0_cacheLine_allowExecute = MmuPlugin_ports_0_cache_3_allowExecute;
            _zz_MmuPlugin_ports_0_cacheLine_allowUser = MmuPlugin_ports_0_cache_3_allowUser;
         end
      endcase
   end

   always @(*) begin
      case (_zz_MmuPlugin_ports_1_cacheLine_valid_3)
         2'b00: begin
            _zz_MmuPlugin_ports_1_cacheLine_valid_4 = MmuPlugin_ports_1_cache_0_valid;
            _zz_MmuPlugin_ports_1_cacheLine_exception = MmuPlugin_ports_1_cache_0_exception;
            _zz_MmuPlugin_ports_1_cacheLine_superPage = MmuPlugin_ports_1_cache_0_superPage;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_0 = MmuPlugin_ports_1_cache_0_virtualAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_1 = MmuPlugin_ports_1_cache_0_virtualAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_0 = MmuPlugin_ports_1_cache_0_physicalAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_1 = MmuPlugin_ports_1_cache_0_physicalAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_allowRead = MmuPlugin_ports_1_cache_0_allowRead;
            _zz_MmuPlugin_ports_1_cacheLine_allowWrite = MmuPlugin_ports_1_cache_0_allowWrite;
            _zz_MmuPlugin_ports_1_cacheLine_allowExecute = MmuPlugin_ports_1_cache_0_allowExecute;
            _zz_MmuPlugin_ports_1_cacheLine_allowUser = MmuPlugin_ports_1_cache_0_allowUser;
         end
         2'b01: begin
            _zz_MmuPlugin_ports_1_cacheLine_valid_4 = MmuPlugin_ports_1_cache_1_valid;
            _zz_MmuPlugin_ports_1_cacheLine_exception = MmuPlugin_ports_1_cache_1_exception;
            _zz_MmuPlugin_ports_1_cacheLine_superPage = MmuPlugin_ports_1_cache_1_superPage;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_0 = MmuPlugin_ports_1_cache_1_virtualAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_1 = MmuPlugin_ports_1_cache_1_virtualAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_0 = MmuPlugin_ports_1_cache_1_physicalAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_1 = MmuPlugin_ports_1_cache_1_physicalAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_allowRead = MmuPlugin_ports_1_cache_1_allowRead;
            _zz_MmuPlugin_ports_1_cacheLine_allowWrite = MmuPlugin_ports_1_cache_1_allowWrite;
            _zz_MmuPlugin_ports_1_cacheLine_allowExecute = MmuPlugin_ports_1_cache_1_allowExecute;
            _zz_MmuPlugin_ports_1_cacheLine_allowUser = MmuPlugin_ports_1_cache_1_allowUser;
         end
         2'b10: begin
            _zz_MmuPlugin_ports_1_cacheLine_valid_4 = MmuPlugin_ports_1_cache_2_valid;
            _zz_MmuPlugin_ports_1_cacheLine_exception = MmuPlugin_ports_1_cache_2_exception;
            _zz_MmuPlugin_ports_1_cacheLine_superPage = MmuPlugin_ports_1_cache_2_superPage;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_0 = MmuPlugin_ports_1_cache_2_virtualAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_1 = MmuPlugin_ports_1_cache_2_virtualAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_0 = MmuPlugin_ports_1_cache_2_physicalAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_1 = MmuPlugin_ports_1_cache_2_physicalAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_allowRead = MmuPlugin_ports_1_cache_2_allowRead;
            _zz_MmuPlugin_ports_1_cacheLine_allowWrite = MmuPlugin_ports_1_cache_2_allowWrite;
            _zz_MmuPlugin_ports_1_cacheLine_allowExecute = MmuPlugin_ports_1_cache_2_allowExecute;
            _zz_MmuPlugin_ports_1_cacheLine_allowUser = MmuPlugin_ports_1_cache_2_allowUser;
         end
         default: begin
            _zz_MmuPlugin_ports_1_cacheLine_valid_4 = MmuPlugin_ports_1_cache_3_valid;
            _zz_MmuPlugin_ports_1_cacheLine_exception = MmuPlugin_ports_1_cache_3_exception;
            _zz_MmuPlugin_ports_1_cacheLine_superPage = MmuPlugin_ports_1_cache_3_superPage;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_0 = MmuPlugin_ports_1_cache_3_virtualAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_1 = MmuPlugin_ports_1_cache_3_virtualAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_0 = MmuPlugin_ports_1_cache_3_physicalAddress_0;
            _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_1 = MmuPlugin_ports_1_cache_3_physicalAddress_1;
            _zz_MmuPlugin_ports_1_cacheLine_allowRead = MmuPlugin_ports_1_cache_3_allowRead;
            _zz_MmuPlugin_ports_1_cacheLine_allowWrite = MmuPlugin_ports_1_cache_3_allowWrite;
            _zz_MmuPlugin_ports_1_cacheLine_allowExecute = MmuPlugin_ports_1_cache_3_allowExecute;
            _zz_MmuPlugin_ports_1_cacheLine_allowUser = MmuPlugin_ports_1_cache_3_allowUser;
         end
      endcase
   end

`ifndef SYNTHESIS
   always @(*) begin
      case (_zz_memory_to_writeBack_ENV_CTRL)
         EnvCtrlEnum_NONE:   _zz_memory_to_writeBack_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_memory_to_writeBack_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_memory_to_writeBack_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_memory_to_writeBack_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_memory_to_writeBack_ENV_CTRL_string = "EBREAK";
         default:            _zz_memory_to_writeBack_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_memory_to_writeBack_ENV_CTRL_1)
         EnvCtrlEnum_NONE:   _zz_memory_to_writeBack_ENV_CTRL_1_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_memory_to_writeBack_ENV_CTRL_1_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_memory_to_writeBack_ENV_CTRL_1_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_memory_to_writeBack_ENV_CTRL_1_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_memory_to_writeBack_ENV_CTRL_1_string = "EBREAK";
         default:            _zz_memory_to_writeBack_ENV_CTRL_1_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_to_memory_ENV_CTRL)
         EnvCtrlEnum_NONE:   _zz_execute_to_memory_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_execute_to_memory_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_execute_to_memory_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_execute_to_memory_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_execute_to_memory_ENV_CTRL_string = "EBREAK";
         default:            _zz_execute_to_memory_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_to_memory_ENV_CTRL_1)
         EnvCtrlEnum_NONE:   _zz_execute_to_memory_ENV_CTRL_1_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_execute_to_memory_ENV_CTRL_1_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_execute_to_memory_ENV_CTRL_1_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_execute_to_memory_ENV_CTRL_1_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_execute_to_memory_ENV_CTRL_1_string = "EBREAK";
         default:            _zz_execute_to_memory_ENV_CTRL_1_string = "??????";
      endcase
   end
   always @(*) begin
      case (decode_ENV_CTRL)
         EnvCtrlEnum_NONE:   decode_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   decode_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    decode_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  decode_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: decode_ENV_CTRL_string = "EBREAK";
         default:            decode_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ENV_CTRL)
         EnvCtrlEnum_NONE:   _zz_decode_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_decode_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_decode_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_decode_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_decode_ENV_CTRL_string = "EBREAK";
         default:            _zz_decode_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_ENV_CTRL)
         EnvCtrlEnum_NONE:   _zz_decode_to_execute_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_decode_to_execute_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_decode_to_execute_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_decode_to_execute_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_decode_to_execute_ENV_CTRL_string = "EBREAK";
         default:            _zz_decode_to_execute_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_ENV_CTRL_1)
         EnvCtrlEnum_NONE:   _zz_decode_to_execute_ENV_CTRL_1_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_decode_to_execute_ENV_CTRL_1_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_decode_to_execute_ENV_CTRL_1_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_decode_to_execute_ENV_CTRL_1_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_decode_to_execute_ENV_CTRL_1_string = "EBREAK";
         default:            _zz_decode_to_execute_ENV_CTRL_1_string = "??????";
      endcase
   end
   always @(*) begin
      case (decode_BRANCH_CTRL)
         BranchCtrlEnum_INC:  decode_BRANCH_CTRL_string = "INC ";
         BranchCtrlEnum_B:    decode_BRANCH_CTRL_string = "B   ";
         BranchCtrlEnum_JAL:  decode_BRANCH_CTRL_string = "JAL ";
         BranchCtrlEnum_JALR: decode_BRANCH_CTRL_string = "JALR";
         default:             decode_BRANCH_CTRL_string = "????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_BRANCH_CTRL)
         BranchCtrlEnum_INC:  _zz_decode_BRANCH_CTRL_string = "INC ";
         BranchCtrlEnum_B:    _zz_decode_BRANCH_CTRL_string = "B   ";
         BranchCtrlEnum_JAL:  _zz_decode_BRANCH_CTRL_string = "JAL ";
         BranchCtrlEnum_JALR: _zz_decode_BRANCH_CTRL_string = "JALR";
         default:             _zz_decode_BRANCH_CTRL_string = "????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_BRANCH_CTRL)
         BranchCtrlEnum_INC:  _zz_decode_to_execute_BRANCH_CTRL_string = "INC ";
         BranchCtrlEnum_B:    _zz_decode_to_execute_BRANCH_CTRL_string = "B   ";
         BranchCtrlEnum_JAL:  _zz_decode_to_execute_BRANCH_CTRL_string = "JAL ";
         BranchCtrlEnum_JALR: _zz_decode_to_execute_BRANCH_CTRL_string = "JALR";
         default:             _zz_decode_to_execute_BRANCH_CTRL_string = "????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_BRANCH_CTRL_1)
         BranchCtrlEnum_INC:  _zz_decode_to_execute_BRANCH_CTRL_1_string = "INC ";
         BranchCtrlEnum_B:    _zz_decode_to_execute_BRANCH_CTRL_1_string = "B   ";
         BranchCtrlEnum_JAL:  _zz_decode_to_execute_BRANCH_CTRL_1_string = "JAL ";
         BranchCtrlEnum_JALR: _zz_decode_to_execute_BRANCH_CTRL_1_string = "JALR";
         default:             _zz_decode_to_execute_BRANCH_CTRL_1_string = "????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_to_memory_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: _zz_execute_to_memory_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_execute_to_memory_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_execute_to_memory_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_execute_to_memory_SHIFT_CTRL_string = "SRA_1    ";
         default:                 _zz_execute_to_memory_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_to_memory_SHIFT_CTRL_1)
         ShiftCtrlEnum_DISABLE_1: _zz_execute_to_memory_SHIFT_CTRL_1_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_execute_to_memory_SHIFT_CTRL_1_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_execute_to_memory_SHIFT_CTRL_1_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_execute_to_memory_SHIFT_CTRL_1_string = "SRA_1    ";
         default:                 _zz_execute_to_memory_SHIFT_CTRL_1_string = "?????????";
      endcase
   end
   always @(*) begin
      case (decode_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: decode_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     decode_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     decode_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     decode_SHIFT_CTRL_string = "SRA_1    ";
         default:                 decode_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: _zz_decode_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_decode_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_decode_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_decode_SHIFT_CTRL_string = "SRA_1    ";
         default:                 _zz_decode_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: _zz_decode_to_execute_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_decode_to_execute_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_decode_to_execute_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_decode_to_execute_SHIFT_CTRL_string = "SRA_1    ";
         default:                 _zz_decode_to_execute_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_SHIFT_CTRL_1)
         ShiftCtrlEnum_DISABLE_1: _zz_decode_to_execute_SHIFT_CTRL_1_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_decode_to_execute_SHIFT_CTRL_1_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_decode_to_execute_SHIFT_CTRL_1_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_decode_to_execute_SHIFT_CTRL_1_string = "SRA_1    ";
         default:                 _zz_decode_to_execute_SHIFT_CTRL_1_string = "?????????";
      endcase
   end
   always @(*) begin
      case (decode_ALU_BITWISE_CTRL)
         AluBitwiseCtrlEnum_XOR_1: decode_ALU_BITWISE_CTRL_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  decode_ALU_BITWISE_CTRL_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: decode_ALU_BITWISE_CTRL_string = "AND_1";
         default:                  decode_ALU_BITWISE_CTRL_string = "?????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ALU_BITWISE_CTRL)
         AluBitwiseCtrlEnum_XOR_1: _zz_decode_ALU_BITWISE_CTRL_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  _zz_decode_ALU_BITWISE_CTRL_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: _zz_decode_ALU_BITWISE_CTRL_string = "AND_1";
         default:                  _zz_decode_ALU_BITWISE_CTRL_string = "?????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_ALU_BITWISE_CTRL)
         AluBitwiseCtrlEnum_XOR_1: _zz_decode_to_execute_ALU_BITWISE_CTRL_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  _zz_decode_to_execute_ALU_BITWISE_CTRL_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: _zz_decode_to_execute_ALU_BITWISE_CTRL_string = "AND_1";
         default:                  _zz_decode_to_execute_ALU_BITWISE_CTRL_string = "?????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_ALU_BITWISE_CTRL_1)
         AluBitwiseCtrlEnum_XOR_1: _zz_decode_to_execute_ALU_BITWISE_CTRL_1_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  _zz_decode_to_execute_ALU_BITWISE_CTRL_1_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: _zz_decode_to_execute_ALU_BITWISE_CTRL_1_string = "AND_1";
         default:                  _zz_decode_to_execute_ALU_BITWISE_CTRL_1_string = "?????";
      endcase
   end
   always @(*) begin
      case (decode_SRC2_CTRL)
         Src2CtrlEnum_RS:  decode_SRC2_CTRL_string = "RS ";
         Src2CtrlEnum_IMI: decode_SRC2_CTRL_string = "IMI";
         Src2CtrlEnum_IMS: decode_SRC2_CTRL_string = "IMS";
         Src2CtrlEnum_PC:  decode_SRC2_CTRL_string = "PC ";
         default:          decode_SRC2_CTRL_string = "???";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SRC2_CTRL)
         Src2CtrlEnum_RS:  _zz_decode_SRC2_CTRL_string = "RS ";
         Src2CtrlEnum_IMI: _zz_decode_SRC2_CTRL_string = "IMI";
         Src2CtrlEnum_IMS: _zz_decode_SRC2_CTRL_string = "IMS";
         Src2CtrlEnum_PC:  _zz_decode_SRC2_CTRL_string = "PC ";
         default:          _zz_decode_SRC2_CTRL_string = "???";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_SRC2_CTRL)
         Src2CtrlEnum_RS:  _zz_decode_to_execute_SRC2_CTRL_string = "RS ";
         Src2CtrlEnum_IMI: _zz_decode_to_execute_SRC2_CTRL_string = "IMI";
         Src2CtrlEnum_IMS: _zz_decode_to_execute_SRC2_CTRL_string = "IMS";
         Src2CtrlEnum_PC:  _zz_decode_to_execute_SRC2_CTRL_string = "PC ";
         default:          _zz_decode_to_execute_SRC2_CTRL_string = "???";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_SRC2_CTRL_1)
         Src2CtrlEnum_RS:  _zz_decode_to_execute_SRC2_CTRL_1_string = "RS ";
         Src2CtrlEnum_IMI: _zz_decode_to_execute_SRC2_CTRL_1_string = "IMI";
         Src2CtrlEnum_IMS: _zz_decode_to_execute_SRC2_CTRL_1_string = "IMS";
         Src2CtrlEnum_PC:  _zz_decode_to_execute_SRC2_CTRL_1_string = "PC ";
         default:          _zz_decode_to_execute_SRC2_CTRL_1_string = "???";
      endcase
   end
   always @(*) begin
      case (decode_ALU_CTRL)
         AluCtrlEnum_ADD_SUB:  decode_ALU_CTRL_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: decode_ALU_CTRL_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  decode_ALU_CTRL_string = "BITWISE ";
         default:              decode_ALU_CTRL_string = "????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ALU_CTRL)
         AluCtrlEnum_ADD_SUB:  _zz_decode_ALU_CTRL_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: _zz_decode_ALU_CTRL_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  _zz_decode_ALU_CTRL_string = "BITWISE ";
         default:              _zz_decode_ALU_CTRL_string = "????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_ALU_CTRL)
         AluCtrlEnum_ADD_SUB:  _zz_decode_to_execute_ALU_CTRL_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: _zz_decode_to_execute_ALU_CTRL_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  _zz_decode_to_execute_ALU_CTRL_string = "BITWISE ";
         default:              _zz_decode_to_execute_ALU_CTRL_string = "????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_ALU_CTRL_1)
         AluCtrlEnum_ADD_SUB:  _zz_decode_to_execute_ALU_CTRL_1_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: _zz_decode_to_execute_ALU_CTRL_1_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  _zz_decode_to_execute_ALU_CTRL_1_string = "BITWISE ";
         default:              _zz_decode_to_execute_ALU_CTRL_1_string = "????????";
      endcase
   end
   always @(*) begin
      case (decode_SRC1_CTRL)
         Src1CtrlEnum_RS:           decode_SRC1_CTRL_string = "RS          ";
         Src1CtrlEnum_IMU:          decode_SRC1_CTRL_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: decode_SRC1_CTRL_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         decode_SRC1_CTRL_string = "URS1        ";
         default:                   decode_SRC1_CTRL_string = "????????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SRC1_CTRL)
         Src1CtrlEnum_RS:           _zz_decode_SRC1_CTRL_string = "RS          ";
         Src1CtrlEnum_IMU:          _zz_decode_SRC1_CTRL_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: _zz_decode_SRC1_CTRL_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         _zz_decode_SRC1_CTRL_string = "URS1        ";
         default:                   _zz_decode_SRC1_CTRL_string = "????????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_SRC1_CTRL)
         Src1CtrlEnum_RS:           _zz_decode_to_execute_SRC1_CTRL_string = "RS          ";
         Src1CtrlEnum_IMU:          _zz_decode_to_execute_SRC1_CTRL_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: _zz_decode_to_execute_SRC1_CTRL_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         _zz_decode_to_execute_SRC1_CTRL_string = "URS1        ";
         default:                   _zz_decode_to_execute_SRC1_CTRL_string = "????????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_to_execute_SRC1_CTRL_1)
         Src1CtrlEnum_RS:           _zz_decode_to_execute_SRC1_CTRL_1_string = "RS          ";
         Src1CtrlEnum_IMU:          _zz_decode_to_execute_SRC1_CTRL_1_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: _zz_decode_to_execute_SRC1_CTRL_1_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         _zz_decode_to_execute_SRC1_CTRL_1_string = "URS1        ";
         default:                   _zz_decode_to_execute_SRC1_CTRL_1_string = "????????????";
      endcase
   end
   always @(*) begin
      case (memory_ENV_CTRL)
         EnvCtrlEnum_NONE:   memory_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   memory_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    memory_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  memory_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: memory_ENV_CTRL_string = "EBREAK";
         default:            memory_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_memory_ENV_CTRL)
         EnvCtrlEnum_NONE:   _zz_memory_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_memory_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_memory_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_memory_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_memory_ENV_CTRL_string = "EBREAK";
         default:            _zz_memory_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (execute_ENV_CTRL)
         EnvCtrlEnum_NONE:   execute_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   execute_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    execute_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  execute_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: execute_ENV_CTRL_string = "EBREAK";
         default:            execute_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_ENV_CTRL)
         EnvCtrlEnum_NONE:   _zz_execute_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_execute_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_execute_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_execute_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_execute_ENV_CTRL_string = "EBREAK";
         default:            _zz_execute_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (writeBack_ENV_CTRL)
         EnvCtrlEnum_NONE:   writeBack_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   writeBack_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    writeBack_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  writeBack_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: writeBack_ENV_CTRL_string = "EBREAK";
         default:            writeBack_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_writeBack_ENV_CTRL)
         EnvCtrlEnum_NONE:   _zz_writeBack_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_writeBack_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_writeBack_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_writeBack_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_writeBack_ENV_CTRL_string = "EBREAK";
         default:            _zz_writeBack_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (execute_BRANCH_CTRL)
         BranchCtrlEnum_INC:  execute_BRANCH_CTRL_string = "INC ";
         BranchCtrlEnum_B:    execute_BRANCH_CTRL_string = "B   ";
         BranchCtrlEnum_JAL:  execute_BRANCH_CTRL_string = "JAL ";
         BranchCtrlEnum_JALR: execute_BRANCH_CTRL_string = "JALR";
         default:             execute_BRANCH_CTRL_string = "????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_BRANCH_CTRL)
         BranchCtrlEnum_INC:  _zz_execute_BRANCH_CTRL_string = "INC ";
         BranchCtrlEnum_B:    _zz_execute_BRANCH_CTRL_string = "B   ";
         BranchCtrlEnum_JAL:  _zz_execute_BRANCH_CTRL_string = "JAL ";
         BranchCtrlEnum_JALR: _zz_execute_BRANCH_CTRL_string = "JALR";
         default:             _zz_execute_BRANCH_CTRL_string = "????";
      endcase
   end
   always @(*) begin
      case (memory_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: memory_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     memory_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     memory_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     memory_SHIFT_CTRL_string = "SRA_1    ";
         default:                 memory_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_memory_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: _zz_memory_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_memory_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_memory_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_memory_SHIFT_CTRL_string = "SRA_1    ";
         default:                 _zz_memory_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (execute_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: execute_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     execute_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     execute_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     execute_SHIFT_CTRL_string = "SRA_1    ";
         default:                 execute_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: _zz_execute_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_execute_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_execute_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_execute_SHIFT_CTRL_string = "SRA_1    ";
         default:                 _zz_execute_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (execute_SRC2_CTRL)
         Src2CtrlEnum_RS:  execute_SRC2_CTRL_string = "RS ";
         Src2CtrlEnum_IMI: execute_SRC2_CTRL_string = "IMI";
         Src2CtrlEnum_IMS: execute_SRC2_CTRL_string = "IMS";
         Src2CtrlEnum_PC:  execute_SRC2_CTRL_string = "PC ";
         default:          execute_SRC2_CTRL_string = "???";
      endcase
   end
   always @(*) begin
      case (_zz_execute_SRC2_CTRL)
         Src2CtrlEnum_RS:  _zz_execute_SRC2_CTRL_string = "RS ";
         Src2CtrlEnum_IMI: _zz_execute_SRC2_CTRL_string = "IMI";
         Src2CtrlEnum_IMS: _zz_execute_SRC2_CTRL_string = "IMS";
         Src2CtrlEnum_PC:  _zz_execute_SRC2_CTRL_string = "PC ";
         default:          _zz_execute_SRC2_CTRL_string = "???";
      endcase
   end
   always @(*) begin
      case (execute_SRC1_CTRL)
         Src1CtrlEnum_RS:           execute_SRC1_CTRL_string = "RS          ";
         Src1CtrlEnum_IMU:          execute_SRC1_CTRL_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: execute_SRC1_CTRL_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         execute_SRC1_CTRL_string = "URS1        ";
         default:                   execute_SRC1_CTRL_string = "????????????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_SRC1_CTRL)
         Src1CtrlEnum_RS:           _zz_execute_SRC1_CTRL_string = "RS          ";
         Src1CtrlEnum_IMU:          _zz_execute_SRC1_CTRL_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: _zz_execute_SRC1_CTRL_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         _zz_execute_SRC1_CTRL_string = "URS1        ";
         default:                   _zz_execute_SRC1_CTRL_string = "????????????";
      endcase
   end
   always @(*) begin
      case (execute_ALU_CTRL)
         AluCtrlEnum_ADD_SUB:  execute_ALU_CTRL_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: execute_ALU_CTRL_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  execute_ALU_CTRL_string = "BITWISE ";
         default:              execute_ALU_CTRL_string = "????????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_ALU_CTRL)
         AluCtrlEnum_ADD_SUB:  _zz_execute_ALU_CTRL_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: _zz_execute_ALU_CTRL_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  _zz_execute_ALU_CTRL_string = "BITWISE ";
         default:              _zz_execute_ALU_CTRL_string = "????????";
      endcase
   end
   always @(*) begin
      case (execute_ALU_BITWISE_CTRL)
         AluBitwiseCtrlEnum_XOR_1: execute_ALU_BITWISE_CTRL_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  execute_ALU_BITWISE_CTRL_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: execute_ALU_BITWISE_CTRL_string = "AND_1";
         default:                  execute_ALU_BITWISE_CTRL_string = "?????";
      endcase
   end
   always @(*) begin
      case (_zz_execute_ALU_BITWISE_CTRL)
         AluBitwiseCtrlEnum_XOR_1: _zz_execute_ALU_BITWISE_CTRL_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  _zz_execute_ALU_BITWISE_CTRL_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: _zz_execute_ALU_BITWISE_CTRL_string = "AND_1";
         default:                  _zz_execute_ALU_BITWISE_CTRL_string = "?????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ENV_CTRL_1)
         EnvCtrlEnum_NONE:   _zz_decode_ENV_CTRL_1_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_decode_ENV_CTRL_1_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_decode_ENV_CTRL_1_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_decode_ENV_CTRL_1_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_decode_ENV_CTRL_1_string = "EBREAK";
         default:            _zz_decode_ENV_CTRL_1_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_BRANCH_CTRL_1)
         BranchCtrlEnum_INC:  _zz_decode_BRANCH_CTRL_1_string = "INC ";
         BranchCtrlEnum_B:    _zz_decode_BRANCH_CTRL_1_string = "B   ";
         BranchCtrlEnum_JAL:  _zz_decode_BRANCH_CTRL_1_string = "JAL ";
         BranchCtrlEnum_JALR: _zz_decode_BRANCH_CTRL_1_string = "JALR";
         default:             _zz_decode_BRANCH_CTRL_1_string = "????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SHIFT_CTRL_1)
         ShiftCtrlEnum_DISABLE_1: _zz_decode_SHIFT_CTRL_1_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_decode_SHIFT_CTRL_1_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_decode_SHIFT_CTRL_1_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_decode_SHIFT_CTRL_1_string = "SRA_1    ";
         default:                 _zz_decode_SHIFT_CTRL_1_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ALU_BITWISE_CTRL_1)
         AluBitwiseCtrlEnum_XOR_1: _zz_decode_ALU_BITWISE_CTRL_1_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  _zz_decode_ALU_BITWISE_CTRL_1_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: _zz_decode_ALU_BITWISE_CTRL_1_string = "AND_1";
         default:                  _zz_decode_ALU_BITWISE_CTRL_1_string = "?????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SRC2_CTRL_1)
         Src2CtrlEnum_RS:  _zz_decode_SRC2_CTRL_1_string = "RS ";
         Src2CtrlEnum_IMI: _zz_decode_SRC2_CTRL_1_string = "IMI";
         Src2CtrlEnum_IMS: _zz_decode_SRC2_CTRL_1_string = "IMS";
         Src2CtrlEnum_PC:  _zz_decode_SRC2_CTRL_1_string = "PC ";
         default:          _zz_decode_SRC2_CTRL_1_string = "???";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ALU_CTRL_1)
         AluCtrlEnum_ADD_SUB:  _zz_decode_ALU_CTRL_1_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: _zz_decode_ALU_CTRL_1_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  _zz_decode_ALU_CTRL_1_string = "BITWISE ";
         default:              _zz_decode_ALU_CTRL_1_string = "????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SRC1_CTRL_1)
         Src1CtrlEnum_RS:           _zz_decode_SRC1_CTRL_1_string = "RS          ";
         Src1CtrlEnum_IMU:          _zz_decode_SRC1_CTRL_1_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: _zz_decode_SRC1_CTRL_1_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         _zz_decode_SRC1_CTRL_1_string = "URS1        ";
         default:                   _zz_decode_SRC1_CTRL_1_string = "????????????";
      endcase
   end
   always @(*) begin
      case (MmuPlugin_shared_state_1)
         MmuPlugin_shared_State_IDLE:   MmuPlugin_shared_state_1_string = "IDLE  ";
         MmuPlugin_shared_State_L1_CMD: MmuPlugin_shared_state_1_string = "L1_CMD";
         MmuPlugin_shared_State_L1_RSP: MmuPlugin_shared_state_1_string = "L1_RSP";
         MmuPlugin_shared_State_L0_CMD: MmuPlugin_shared_state_1_string = "L0_CMD";
         MmuPlugin_shared_State_L0_RSP: MmuPlugin_shared_state_1_string = "L0_RSP";
         default:                       MmuPlugin_shared_state_1_string = "??????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SRC1_CTRL_2)
         Src1CtrlEnum_RS:           _zz_decode_SRC1_CTRL_2_string = "RS          ";
         Src1CtrlEnum_IMU:          _zz_decode_SRC1_CTRL_2_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: _zz_decode_SRC1_CTRL_2_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         _zz_decode_SRC1_CTRL_2_string = "URS1        ";
         default:                   _zz_decode_SRC1_CTRL_2_string = "????????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ALU_CTRL_2)
         AluCtrlEnum_ADD_SUB:  _zz_decode_ALU_CTRL_2_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: _zz_decode_ALU_CTRL_2_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  _zz_decode_ALU_CTRL_2_string = "BITWISE ";
         default:              _zz_decode_ALU_CTRL_2_string = "????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SRC2_CTRL_2)
         Src2CtrlEnum_RS:  _zz_decode_SRC2_CTRL_2_string = "RS ";
         Src2CtrlEnum_IMI: _zz_decode_SRC2_CTRL_2_string = "IMI";
         Src2CtrlEnum_IMS: _zz_decode_SRC2_CTRL_2_string = "IMS";
         Src2CtrlEnum_PC:  _zz_decode_SRC2_CTRL_2_string = "PC ";
         default:          _zz_decode_SRC2_CTRL_2_string = "???";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ALU_BITWISE_CTRL_2)
         AluBitwiseCtrlEnum_XOR_1: _zz_decode_ALU_BITWISE_CTRL_2_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  _zz_decode_ALU_BITWISE_CTRL_2_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: _zz_decode_ALU_BITWISE_CTRL_2_string = "AND_1";
         default:                  _zz_decode_ALU_BITWISE_CTRL_2_string = "?????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_SHIFT_CTRL_2)
         ShiftCtrlEnum_DISABLE_1: _zz_decode_SHIFT_CTRL_2_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     _zz_decode_SHIFT_CTRL_2_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     _zz_decode_SHIFT_CTRL_2_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     _zz_decode_SHIFT_CTRL_2_string = "SRA_1    ";
         default:                 _zz_decode_SHIFT_CTRL_2_string = "?????????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_BRANCH_CTRL_2)
         BranchCtrlEnum_INC:  _zz_decode_BRANCH_CTRL_2_string = "INC ";
         BranchCtrlEnum_B:    _zz_decode_BRANCH_CTRL_2_string = "B   ";
         BranchCtrlEnum_JAL:  _zz_decode_BRANCH_CTRL_2_string = "JAL ";
         BranchCtrlEnum_JALR: _zz_decode_BRANCH_CTRL_2_string = "JALR";
         default:             _zz_decode_BRANCH_CTRL_2_string = "????";
      endcase
   end
   always @(*) begin
      case (_zz_decode_ENV_CTRL_2)
         EnvCtrlEnum_NONE:   _zz_decode_ENV_CTRL_2_string = "NONE  ";
         EnvCtrlEnum_XRET:   _zz_decode_ENV_CTRL_2_string = "XRET  ";
         EnvCtrlEnum_WFI:    _zz_decode_ENV_CTRL_2_string = "WFI   ";
         EnvCtrlEnum_ECALL:  _zz_decode_ENV_CTRL_2_string = "ECALL ";
         EnvCtrlEnum_EBREAK: _zz_decode_ENV_CTRL_2_string = "EBREAK";
         default:            _zz_decode_ENV_CTRL_2_string = "??????";
      endcase
   end
   always @(*) begin
      case (decode_to_execute_SRC1_CTRL)
         Src1CtrlEnum_RS:           decode_to_execute_SRC1_CTRL_string = "RS          ";
         Src1CtrlEnum_IMU:          decode_to_execute_SRC1_CTRL_string = "IMU         ";
         Src1CtrlEnum_PC_INCREMENT: decode_to_execute_SRC1_CTRL_string = "PC_INCREMENT";
         Src1CtrlEnum_URS1:         decode_to_execute_SRC1_CTRL_string = "URS1        ";
         default:                   decode_to_execute_SRC1_CTRL_string = "????????????";
      endcase
   end
   always @(*) begin
      case (decode_to_execute_ALU_CTRL)
         AluCtrlEnum_ADD_SUB:  decode_to_execute_ALU_CTRL_string = "ADD_SUB ";
         AluCtrlEnum_SLT_SLTU: decode_to_execute_ALU_CTRL_string = "SLT_SLTU";
         AluCtrlEnum_BITWISE:  decode_to_execute_ALU_CTRL_string = "BITWISE ";
         default:              decode_to_execute_ALU_CTRL_string = "????????";
      endcase
   end
   always @(*) begin
      case (decode_to_execute_SRC2_CTRL)
         Src2CtrlEnum_RS:  decode_to_execute_SRC2_CTRL_string = "RS ";
         Src2CtrlEnum_IMI: decode_to_execute_SRC2_CTRL_string = "IMI";
         Src2CtrlEnum_IMS: decode_to_execute_SRC2_CTRL_string = "IMS";
         Src2CtrlEnum_PC:  decode_to_execute_SRC2_CTRL_string = "PC ";
         default:          decode_to_execute_SRC2_CTRL_string = "???";
      endcase
   end
   always @(*) begin
      case (decode_to_execute_ALU_BITWISE_CTRL)
         AluBitwiseCtrlEnum_XOR_1: decode_to_execute_ALU_BITWISE_CTRL_string = "XOR_1";
         AluBitwiseCtrlEnum_OR_1:  decode_to_execute_ALU_BITWISE_CTRL_string = "OR_1 ";
         AluBitwiseCtrlEnum_AND_1: decode_to_execute_ALU_BITWISE_CTRL_string = "AND_1";
         default:                  decode_to_execute_ALU_BITWISE_CTRL_string = "?????";
      endcase
   end
   always @(*) begin
      case (decode_to_execute_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: decode_to_execute_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     decode_to_execute_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     decode_to_execute_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     decode_to_execute_SHIFT_CTRL_string = "SRA_1    ";
         default:                 decode_to_execute_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (execute_to_memory_SHIFT_CTRL)
         ShiftCtrlEnum_DISABLE_1: execute_to_memory_SHIFT_CTRL_string = "DISABLE_1";
         ShiftCtrlEnum_SLL_1:     execute_to_memory_SHIFT_CTRL_string = "SLL_1    ";
         ShiftCtrlEnum_SRL_1:     execute_to_memory_SHIFT_CTRL_string = "SRL_1    ";
         ShiftCtrlEnum_SRA_1:     execute_to_memory_SHIFT_CTRL_string = "SRA_1    ";
         default:                 execute_to_memory_SHIFT_CTRL_string = "?????????";
      endcase
   end
   always @(*) begin
      case (decode_to_execute_BRANCH_CTRL)
         BranchCtrlEnum_INC:  decode_to_execute_BRANCH_CTRL_string = "INC ";
         BranchCtrlEnum_B:    decode_to_execute_BRANCH_CTRL_string = "B   ";
         BranchCtrlEnum_JAL:  decode_to_execute_BRANCH_CTRL_string = "JAL ";
         BranchCtrlEnum_JALR: decode_to_execute_BRANCH_CTRL_string = "JALR";
         default:             decode_to_execute_BRANCH_CTRL_string = "????";
      endcase
   end
   always @(*) begin
      case (decode_to_execute_ENV_CTRL)
         EnvCtrlEnum_NONE:   decode_to_execute_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   decode_to_execute_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    decode_to_execute_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  decode_to_execute_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: decode_to_execute_ENV_CTRL_string = "EBREAK";
         default:            decode_to_execute_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (execute_to_memory_ENV_CTRL)
         EnvCtrlEnum_NONE:   execute_to_memory_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   execute_to_memory_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    execute_to_memory_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  execute_to_memory_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: execute_to_memory_ENV_CTRL_string = "EBREAK";
         default:            execute_to_memory_ENV_CTRL_string = "??????";
      endcase
   end
   always @(*) begin
      case (memory_to_writeBack_ENV_CTRL)
         EnvCtrlEnum_NONE:   memory_to_writeBack_ENV_CTRL_string = "NONE  ";
         EnvCtrlEnum_XRET:   memory_to_writeBack_ENV_CTRL_string = "XRET  ";
         EnvCtrlEnum_WFI:    memory_to_writeBack_ENV_CTRL_string = "WFI   ";
         EnvCtrlEnum_ECALL:  memory_to_writeBack_ENV_CTRL_string = "ECALL ";
         EnvCtrlEnum_EBREAK: memory_to_writeBack_ENV_CTRL_string = "EBREAK";
         default:            memory_to_writeBack_ENV_CTRL_string = "??????";
      endcase
   end
`endif

   assign memory_MUL_LOW = ($signed(_zz_memory_MUL_LOW) + $signed(_zz_memory_MUL_LOW_6));
   assign execute_BRANCH_CALC = {execute_BranchPlugin_branchAdder[31 : 1], 1'b0};
   assign execute_BRANCH_DO = _zz_execute_BRANCH_DO_1;
   assign memory_MUL_HH = execute_to_memory_MUL_HH;
   assign execute_MUL_HH = ($signed(execute_MulPlugin_aHigh) * $signed(execute_MulPlugin_bHigh));
   assign execute_MUL_HL = ($signed(execute_MulPlugin_aHigh) * $signed(execute_MulPlugin_bSLow));
   assign execute_MUL_LH = ($signed(execute_MulPlugin_aSLow) * $signed(execute_MulPlugin_bHigh));
   assign execute_MUL_LL = (execute_MulPlugin_aULow * execute_MulPlugin_bULow);
   assign execute_SHIFT_RIGHT = _zz_execute_SHIFT_RIGHT;
   assign execute_REGFILE_WRITE_DATA = _zz_execute_REGFILE_WRITE_DATA;
   assign memory_MEMORY_STORE_DATA_RF = execute_to_memory_MEMORY_STORE_DATA_RF;
   assign execute_MEMORY_STORE_DATA_RF = _zz_execute_MEMORY_STORE_DATA_RF;
   assign decode_CSR_READ_OPCODE = (decode_INSTRUCTION[13 : 7] != 7'h20);
   assign decode_CSR_WRITE_OPCODE = (! (((decode_INSTRUCTION[14 : 13] == 2'b01) && (decode_INSTRUCTION[19 : 15] == 5'h00)) || ((decode_INSTRUCTION[14 : 13] == 2'b11) && (decode_INSTRUCTION[19 : 15] == 5'h00))));
   assign decode_SRC2_FORCE_ZERO = (decode_SRC_ADD_ZERO && (!decode_SRC_USE_SUB_LESS));
   assign _zz_memory_to_writeBack_ENV_CTRL = _zz_memory_to_writeBack_ENV_CTRL_1;
   assign _zz_execute_to_memory_ENV_CTRL = _zz_execute_to_memory_ENV_CTRL_1;
   assign decode_ENV_CTRL = _zz_decode_ENV_CTRL;
   assign _zz_decode_to_execute_ENV_CTRL = _zz_decode_to_execute_ENV_CTRL_1;
   assign decode_IS_CSR = _zz_decode_IS_CSR[33];
   assign decode_BRANCH_CTRL = _zz_decode_BRANCH_CTRL;
   assign _zz_decode_to_execute_BRANCH_CTRL = _zz_decode_to_execute_BRANCH_CTRL_1;
   assign decode_IS_RS2_SIGNED = _zz_decode_IS_CSR[30];
   assign decode_IS_RS1_SIGNED = _zz_decode_IS_CSR[29];
   assign decode_IS_DIV = _zz_decode_IS_CSR[28];
   assign memory_IS_MUL = execute_to_memory_IS_MUL;
   assign execute_IS_MUL = decode_to_execute_IS_MUL;
   assign decode_IS_MUL = _zz_decode_IS_CSR[27];
   assign _zz_execute_to_memory_SHIFT_CTRL = _zz_execute_to_memory_SHIFT_CTRL_1;
   assign decode_SHIFT_CTRL = _zz_decode_SHIFT_CTRL;
   assign _zz_decode_to_execute_SHIFT_CTRL = _zz_decode_to_execute_SHIFT_CTRL_1;
   assign decode_ALU_BITWISE_CTRL = _zz_decode_ALU_BITWISE_CTRL;
   assign _zz_decode_to_execute_ALU_BITWISE_CTRL = _zz_decode_to_execute_ALU_BITWISE_CTRL_1;
   assign decode_SRC_LESS_UNSIGNED = _zz_decode_IS_CSR[22];
   assign decode_IS_SFENCE_VMA2 = _zz_decode_IS_CSR[21];
   assign decode_MEMORY_MANAGMENT = _zz_decode_IS_CSR[20];
   assign memory_MEMORY_LRSC = execute_to_memory_MEMORY_LRSC;
   assign memory_MEMORY_WR = execute_to_memory_MEMORY_WR;
   assign decode_MEMORY_WR = _zz_decode_IS_CSR[14];
   assign execute_BYPASSABLE_MEMORY_STAGE = decode_to_execute_BYPASSABLE_MEMORY_STAGE;
   assign decode_BYPASSABLE_MEMORY_STAGE = _zz_decode_IS_CSR[13];
   assign decode_BYPASSABLE_EXECUTE_STAGE = _zz_decode_IS_CSR[12];
   assign decode_SRC2_CTRL = _zz_decode_SRC2_CTRL;
   assign _zz_decode_to_execute_SRC2_CTRL = _zz_decode_to_execute_SRC2_CTRL_1;
   assign decode_ALU_CTRL = _zz_decode_ALU_CTRL;
   assign _zz_decode_to_execute_ALU_CTRL = _zz_decode_to_execute_ALU_CTRL_1;
   assign decode_SRC1_CTRL = _zz_decode_SRC1_CTRL;
   assign _zz_decode_to_execute_SRC1_CTRL = _zz_decode_to_execute_SRC1_CTRL_1;
   assign decode_RESCHEDULE_NEXT = _zz_decode_IS_CSR[1];
   assign decode_MEMORY_FORCE_CONSTISTENCY = _zz_decode_MEMORY_FORCE_CONSTISTENCY;
   assign writeBack_FORMAL_PC_NEXT = memory_to_writeBack_FORMAL_PC_NEXT;
   assign memory_FORMAL_PC_NEXT = execute_to_memory_FORMAL_PC_NEXT;
   assign execute_FORMAL_PC_NEXT = decode_to_execute_FORMAL_PC_NEXT;
   assign decode_FORMAL_PC_NEXT = (decode_PC + _zz_decode_FORMAL_PC_NEXT);
   assign memory_PC = execute_to_memory_PC;
   assign execute_CSR_READ_OPCODE = decode_to_execute_CSR_READ_OPCODE;
   assign execute_CSR_WRITE_OPCODE = decode_to_execute_CSR_WRITE_OPCODE;
   assign execute_IS_CSR = decode_to_execute_IS_CSR;
   assign memory_ENV_CTRL = _zz_memory_ENV_CTRL;
   assign execute_ENV_CTRL = _zz_execute_ENV_CTRL;
   assign writeBack_ENV_CTRL = _zz_writeBack_ENV_CTRL;
   assign execute_RESCHEDULE_NEXT = decode_to_execute_RESCHEDULE_NEXT;
   assign memory_BRANCH_CALC = execute_to_memory_BRANCH_CALC;
   assign memory_BRANCH_DO = execute_to_memory_BRANCH_DO;
   assign execute_PC = decode_to_execute_PC;
   assign execute_BRANCH_CTRL = _zz_execute_BRANCH_CTRL;
   assign decode_RS2_USE = _zz_decode_IS_CSR[18];
   assign decode_RS1_USE = _zz_decode_IS_CSR[6];
   always @(*) begin
      _zz_decode_RS2 = execute_REGFILE_WRITE_DATA;
      if (when_CsrPlugin_l1587) begin
         _zz_decode_RS2 = CsrPlugin_csrMapping_readDataSignal;
      end
      if (DBusCachedPlugin_forceDatapath) begin
         _zz_decode_RS2 = MmuPlugin_dBusAccess_cmd_payload_address;
      end
   end

   assign execute_REGFILE_WRITE_VALID      = decode_to_execute_REGFILE_WRITE_VALID;
   assign execute_BYPASSABLE_EXECUTE_STAGE = decode_to_execute_BYPASSABLE_EXECUTE_STAGE;
   assign memory_REGFILE_WRITE_VALID       = execute_to_memory_REGFILE_WRITE_VALID;
   assign memory_BYPASSABLE_MEMORY_STAGE   = execute_to_memory_BYPASSABLE_MEMORY_STAGE;
   assign writeBack_REGFILE_WRITE_VALID    = memory_to_writeBack_REGFILE_WRITE_VALID;
   always @(*) begin
      decode_RS2 = decode_RegFilePlugin_rs2Data;
      if (HazardSimplePlugin_writeBackBuffer_valid) begin
         if (HazardSimplePlugin_addr1Match) begin
            decode_RS2 = HazardSimplePlugin_writeBackBuffer_payload_data;
         end
      end
      if (when_HazardSimplePlugin_l45) begin
         if (when_HazardSimplePlugin_l47) begin
            if (when_HazardSimplePlugin_l51) begin
               decode_RS2 = _zz_decode_RS2_2;
            end
         end
      end
      if (when_HazardSimplePlugin_l45_1) begin
         if (memory_BYPASSABLE_MEMORY_STAGE) begin
            if (when_HazardSimplePlugin_l51_1) begin
               decode_RS2 = _zz_decode_RS2_1;
            end
         end
      end
      if (when_HazardSimplePlugin_l45_2) begin
         if (execute_BYPASSABLE_EXECUTE_STAGE) begin
            if (when_HazardSimplePlugin_l51_2) begin
               decode_RS2 = _zz_decode_RS2;
            end
         end
      end
   end

   always @(*) begin
      decode_RS1 = decode_RegFilePlugin_rs1Data;
      if (HazardSimplePlugin_writeBackBuffer_valid) begin
         if (HazardSimplePlugin_addr0Match) begin
            decode_RS1 = HazardSimplePlugin_writeBackBuffer_payload_data;
         end
      end
      if (when_HazardSimplePlugin_l45) begin
         if (when_HazardSimplePlugin_l47) begin
            if (when_HazardSimplePlugin_l48) begin
               decode_RS1 = _zz_decode_RS2_2;
            end
         end
      end
      if (when_HazardSimplePlugin_l45_1) begin
         if (memory_BYPASSABLE_MEMORY_STAGE) begin
            if (when_HazardSimplePlugin_l48_1) begin
               decode_RS1 = _zz_decode_RS2_1;
            end
         end
      end
      if (when_HazardSimplePlugin_l45_2) begin
         if (execute_BYPASSABLE_EXECUTE_STAGE) begin
            if (when_HazardSimplePlugin_l48_2) begin
               decode_RS1 = _zz_decode_RS2;
            end
         end
      end
   end

   assign execute_IS_RS1_SIGNED = decode_to_execute_IS_RS1_SIGNED;
   assign execute_IS_DIV        = decode_to_execute_IS_DIV;
   assign execute_IS_RS2_SIGNED = decode_to_execute_IS_RS2_SIGNED;
   assign memory_INSTRUCTION    = execute_to_memory_INSTRUCTION;
   assign memory_IS_DIV         = execute_to_memory_IS_DIV;
   assign writeBack_IS_MUL      = memory_to_writeBack_IS_MUL;
   assign writeBack_MUL_HH      = memory_to_writeBack_MUL_HH;
   assign writeBack_MUL_LOW     = memory_to_writeBack_MUL_LOW;
   assign memory_MUL_HL         = execute_to_memory_MUL_HL;
   assign memory_MUL_LH         = execute_to_memory_MUL_LH;
   assign memory_MUL_LL         = execute_to_memory_MUL_LL;
   assign memory_SHIFT_RIGHT    = execute_to_memory_SHIFT_RIGHT;
   always @(*) begin
      _zz_decode_RS2_1 = memory_REGFILE_WRITE_DATA;
      if (memory_arbitration_isValid) begin
         case (memory_SHIFT_CTRL)
            ShiftCtrlEnum_SLL_1: begin
               _zz_decode_RS2_1 = _zz_decode_RS2_3;
            end
            ShiftCtrlEnum_SRL_1, ShiftCtrlEnum_SRA_1: begin
               _zz_decode_RS2_1 = memory_SHIFT_RIGHT;
            end
            default: begin
            end
         endcase
      end
      if (when_MulDivIterativePlugin_l128) begin
         _zz_decode_RS2_1 = memory_DivPlugin_div_result;
      end
   end

   assign memory_SHIFT_CTRL                         = _zz_memory_SHIFT_CTRL;
   assign execute_SHIFT_CTRL                        = _zz_execute_SHIFT_CTRL;
   assign execute_SRC_LESS_UNSIGNED                 = decode_to_execute_SRC_LESS_UNSIGNED;
   assign execute_SRC2_FORCE_ZERO                   = decode_to_execute_SRC2_FORCE_ZERO;
   assign execute_SRC_USE_SUB_LESS                  = decode_to_execute_SRC_USE_SUB_LESS;
   assign _zz_execute_to_memory_PC                  = execute_PC;
   assign execute_SRC2_CTRL                         = _zz_execute_SRC2_CTRL;
   assign execute_IS_RVC                            = decode_to_execute_IS_RVC;
   assign execute_SRC1_CTRL                         = _zz_execute_SRC1_CTRL;
   assign decode_SRC_USE_SUB_LESS                   = _zz_decode_IS_CSR[4];
   assign decode_SRC_ADD_ZERO                       = _zz_decode_IS_CSR[19];
   assign execute_SRC_ADD_SUB                       = execute_SrcPlugin_addSub;
   assign execute_SRC_LESS                          = execute_SrcPlugin_less;
   assign execute_ALU_CTRL                          = _zz_execute_ALU_CTRL;
   assign execute_SRC2                              = _zz_execute_SRC2_4;
   assign execute_SRC1                              = _zz_execute_SRC1;
   assign execute_ALU_BITWISE_CTRL                  = _zz_execute_ALU_BITWISE_CTRL;
   assign _zz_lastStageRegFileWrite_payload_address = writeBack_INSTRUCTION;
   assign _zz_lastStageRegFileWrite_valid           = writeBack_REGFILE_WRITE_VALID;
   always @(*) begin
      _zz_1 = 1'b0;
      if (lastStageRegFileWrite_valid) begin
         _zz_1 = 1'b1;
      end
   end

   assign decode_INSTRUCTION_ANTICIPATED = (decode_arbitration_isStuck ? decode_INSTRUCTION : IBusCachedPlugin_decompressor_output_payload_rsp_inst);
   always @(*) begin
      decode_REGFILE_WRITE_VALID = _zz_decode_IS_CSR[11];
      if (when_RegFilePlugin_l63) begin
         decode_REGFILE_WRITE_VALID = 1'b0;
      end
   end

   assign decode_LEGAL_INSTRUCTION = (|{((decode_INSTRUCTION & 32'h0000005f) == 32'h00000017), {
      ((decode_INSTRUCTION & 32'h0000007f) == 32'h0000006f),
      {
         ((decode_INSTRUCTION & 32'h0000107f) == 32'h00001073),
         {
            ((decode_INSTRUCTION & _zz_decode_LEGAL_INSTRUCTION) == 32'h00002073),
            {
               (_zz_decode_LEGAL_INSTRUCTION_1 == _zz_decode_LEGAL_INSTRUCTION_2),
               {
                  _zz_decode_LEGAL_INSTRUCTION_3,
                  {_zz_decode_LEGAL_INSTRUCTION_4, _zz_decode_LEGAL_INSTRUCTION_5}
               }
            }
         }
      }
   }});
   assign execute_IS_SFENCE_VMA2 = decode_to_execute_IS_SFENCE_VMA2;
   assign writeBack_IS_DBUS_SHARING = memory_to_writeBack_IS_DBUS_SHARING;
   assign execute_IS_DBUS_SHARING = MmuPlugin_dBusAccess_cmd_fire;
   assign memory_IS_DBUS_SHARING = execute_to_memory_IS_DBUS_SHARING;
   always @(*) begin
      _zz_decode_RS2_2 = writeBack_REGFILE_WRITE_DATA;
      if (when_DBusCachedPlugin_l571) begin
         _zz_decode_RS2_2 = writeBack_DBusCachedPlugin_rspFormated;
      end
      if (when_MulPlugin_l147) begin
         case (switch_MulPlugin_l148)
            2'b00: begin
               _zz_decode_RS2_2 = _zz__zz_decode_RS2_2;
            end
            default: begin
               _zz_decode_RS2_2 = _zz__zz_decode_RS2_2_1;
            end
         endcase
      end
   end

   assign writeBack_MEMORY_LRSC          = memory_to_writeBack_MEMORY_LRSC;
   assign writeBack_MEMORY_WR            = memory_to_writeBack_MEMORY_WR;
   assign writeBack_MEMORY_STORE_DATA_RF = memory_to_writeBack_MEMORY_STORE_DATA_RF;
   assign writeBack_REGFILE_WRITE_DATA   = memory_to_writeBack_REGFILE_WRITE_DATA;
   assign writeBack_MEMORY_ENABLE        = memory_to_writeBack_MEMORY_ENABLE;
   assign memory_REGFILE_WRITE_DATA      = execute_to_memory_REGFILE_WRITE_DATA;
   assign memory_MEMORY_ENABLE           = execute_to_memory_MEMORY_ENABLE;
   always @(*) begin
      execute_MEMORY_AMO = decode_to_execute_MEMORY_AMO;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            execute_MEMORY_AMO = 1'b0;
         end
      end
   end

   always @(*) begin
      execute_MEMORY_LRSC = decode_to_execute_MEMORY_LRSC;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            execute_MEMORY_LRSC = 1'b0;
         end
      end
   end

   assign execute_MEMORY_FORCE_CONSTISTENCY = decode_to_execute_MEMORY_FORCE_CONSTISTENCY;
   assign execute_RS1                       = decode_to_execute_RS1;
   assign execute_MEMORY_MANAGMENT          = decode_to_execute_MEMORY_MANAGMENT;
   assign execute_RS2                       = decode_to_execute_RS2;
   assign execute_MEMORY_WR                 = decode_to_execute_MEMORY_WR;
   assign execute_SRC_ADD                   = execute_SrcPlugin_addSub;
   assign execute_MEMORY_ENABLE             = decode_to_execute_MEMORY_ENABLE;
   assign execute_INSTRUCTION               = decode_to_execute_INSTRUCTION;
   assign decode_MEMORY_AMO                 = _zz_decode_IS_CSR[17];
   assign decode_MEMORY_LRSC                = _zz_decode_IS_CSR[16];
   assign decode_MEMORY_ENABLE              = _zz_decode_IS_CSR[5];
   assign decode_FLUSH_ALL                  = _zz_decode_IS_CSR[0];
   always @(*) begin
      IBusCachedPlugin_rsp_issueDetected_4 = IBusCachedPlugin_rsp_issueDetected_3;
      if (when_IBusCachedPlugin_l262) begin
         IBusCachedPlugin_rsp_issueDetected_4 = 1'b1;
      end
   end

   always @(*) begin
      IBusCachedPlugin_rsp_issueDetected_3 = IBusCachedPlugin_rsp_issueDetected_2;
      if (when_IBusCachedPlugin_l256) begin
         IBusCachedPlugin_rsp_issueDetected_3 = 1'b1;
      end
   end

   always @(*) begin
      IBusCachedPlugin_rsp_issueDetected_2 = IBusCachedPlugin_rsp_issueDetected_1;
      if (when_IBusCachedPlugin_l250) begin
         IBusCachedPlugin_rsp_issueDetected_2 = 1'b1;
      end
   end

   always @(*) begin
      IBusCachedPlugin_rsp_issueDetected_1 = IBusCachedPlugin_rsp_issueDetected;
      if (when_IBusCachedPlugin_l245) begin
         IBusCachedPlugin_rsp_issueDetected_1 = 1'b1;
      end
   end

   always @(*) begin
      _zz_execute_to_memory_FORMAL_PC_NEXT = execute_FORMAL_PC_NEXT;
      if (CsrPlugin_redoInterface_valid) begin
         _zz_execute_to_memory_FORMAL_PC_NEXT = CsrPlugin_redoInterface_payload;
      end
   end

   always @(*) begin
      _zz_memory_to_writeBack_FORMAL_PC_NEXT = memory_FORMAL_PC_NEXT;
      if (BranchPlugin_jumpInterface_valid) begin
         _zz_memory_to_writeBack_FORMAL_PC_NEXT = BranchPlugin_jumpInterface_payload;
      end
   end

   assign decode_PC             = IBusCachedPlugin_decodePc_pcReg;
   assign decode_INSTRUCTION    = IBusCachedPlugin_injector_decodeInput_payload_rsp_inst;
   assign decode_IS_RVC         = IBusCachedPlugin_injector_decodeInput_payload_isRvc;
   assign writeBack_PC          = memory_to_writeBack_PC;
   assign writeBack_INSTRUCTION = memory_to_writeBack_INSTRUCTION;
   always @(*) begin
      decode_arbitration_haltItself = 1'b0;
      if (when_DBusCachedPlugin_l343) begin
         decode_arbitration_haltItself = 1'b1;
      end
   end

   always @(*) begin
      decode_arbitration_haltByOther = 1'b0;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         decode_arbitration_haltByOther = 1'b1;
      end
      if (when_HazardSimplePlugin_l113) begin
         decode_arbitration_haltByOther = 1'b1;
      end
      if (CsrPlugin_rescheduleLogic_rescheduleNext) begin
         decode_arbitration_haltByOther = 1'b1;
      end
      if (CsrPlugin_pipelineLiberator_active) begin
         decode_arbitration_haltByOther = 1'b1;
      end
      if (when_CsrPlugin_l1527) begin
         decode_arbitration_haltByOther = 1'b1;
      end
   end

   always @(*) begin
      decode_arbitration_removeIt = 1'b0;
      if (_zz_when) begin
         decode_arbitration_removeIt = 1'b1;
      end
      if (decode_arbitration_isFlushed) begin
         decode_arbitration_removeIt = 1'b1;
      end
   end

   assign decode_arbitration_flushIt = 1'b0;
   always @(*) begin
      decode_arbitration_flushNext = 1'b0;
      if (_zz_when) begin
         decode_arbitration_flushNext = 1'b1;
      end
   end

   always @(*) begin
      execute_arbitration_haltItself = 1'b0;
      if (when_DBusCachedPlugin_l385) begin
         execute_arbitration_haltItself = 1'b1;
      end
      if (when_CsrPlugin_l1519) begin
         if (when_CsrPlugin_l1521) begin
            execute_arbitration_haltItself = 1'b1;
         end
      end
      if (when_CsrPlugin_l1591) begin
         if (execute_CsrPlugin_blockedBySideEffects) begin
            execute_arbitration_haltItself = 1'b1;
         end
      end
   end

   always @(*) begin
      execute_arbitration_haltByOther = 1'b0;
      if (when_DBusCachedPlugin_l401) begin
         execute_arbitration_haltByOther = 1'b1;
      end
   end

   always @(*) begin
      execute_arbitration_removeIt = 1'b0;
      if (CsrPlugin_selfException_valid) begin
         execute_arbitration_removeIt = 1'b1;
      end
      if (execute_arbitration_isFlushed) begin
         execute_arbitration_removeIt = 1'b1;
      end
   end

   assign execute_arbitration_flushIt = 1'b0;
   always @(*) begin
      execute_arbitration_flushNext = 1'b0;
      if (CsrPlugin_rescheduleLogic_rescheduleNext) begin
         execute_arbitration_flushNext = 1'b1;
      end
      if (CsrPlugin_selfException_valid) begin
         execute_arbitration_flushNext = 1'b1;
      end
   end

   always @(*) begin
      memory_arbitration_haltItself = 1'b0;
      if (when_MulDivIterativePlugin_l128) begin
         if (when_MulDivIterativePlugin_l129) begin
            memory_arbitration_haltItself = 1'b1;
         end
      end
   end

   assign memory_arbitration_haltByOther = 1'b0;
   always @(*) begin
      memory_arbitration_removeIt = 1'b0;
      if (memory_arbitration_isFlushed) begin
         memory_arbitration_removeIt = 1'b1;
      end
   end

   assign memory_arbitration_flushIt = 1'b0;
   always @(*) begin
      memory_arbitration_flushNext = 1'b0;
      if (BranchPlugin_jumpInterface_valid) begin
         memory_arbitration_flushNext = 1'b1;
      end
   end

   always @(*) begin
      writeBack_arbitration_haltItself = 1'b0;
      if (when_DBusCachedPlugin_l544) begin
         writeBack_arbitration_haltItself = 1'b1;
      end
   end

   assign writeBack_arbitration_haltByOther = 1'b0;
   always @(*) begin
      writeBack_arbitration_removeIt = 1'b0;
      if (DBusCachedPlugin_exceptionBus_valid) begin
         writeBack_arbitration_removeIt = 1'b1;
      end
      if (writeBack_arbitration_isFlushed) begin
         writeBack_arbitration_removeIt = 1'b1;
      end
   end

   always @(*) begin
      writeBack_arbitration_flushIt = 1'b0;
      if (DBusCachedPlugin_redoBranch_valid) begin
         writeBack_arbitration_flushIt = 1'b1;
      end
   end

   always @(*) begin
      writeBack_arbitration_flushNext = 1'b0;
      if (DBusCachedPlugin_redoBranch_valid) begin
         writeBack_arbitration_flushNext = 1'b1;
      end
      if (DBusCachedPlugin_exceptionBus_valid) begin
         writeBack_arbitration_flushNext = 1'b1;
      end
      if (when_CsrPlugin_l1390) begin
         writeBack_arbitration_flushNext = 1'b1;
      end
      if (when_CsrPlugin_l1456) begin
         writeBack_arbitration_flushNext = 1'b1;
      end
   end

   assign lastStageInstruction = writeBack_INSTRUCTION;
   assign lastStagePc          = writeBack_PC;
   assign lastStageIsValid     = writeBack_arbitration_isValid;
   assign lastStageIsFiring    = writeBack_arbitration_isFiring;
   assign clint_awready        = clintCtrl_io_bus_aw_ready;
   assign clint_wready         = clintCtrl_io_bus_w_ready;
   assign clint_bvalid         = clintCtrl_io_bus_b_valid;
   assign clint_bresp          = clintCtrl_io_bus_b_payload_resp;
   assign clint_arready        = clintCtrl_io_bus_ar_ready;
   assign clint_rvalid         = clintCtrl_io_bus_r_valid;
   assign clint_rdata          = clintCtrl_io_bus_r_payload_data;
   assign clint_rresp          = clintCtrl_io_bus_r_payload_resp;
   assign plic_awready         = plicCtrl_io_bus_aw_ready;
   assign plic_wready          = plicCtrl_io_bus_w_ready;
   assign plic_bvalid          = plicCtrl_io_bus_b_valid;
   assign plic_bresp           = plicCtrl_io_bus_b_payload_resp;
   assign plic_arready         = plicCtrl_io_bus_ar_ready;
   assign plic_rvalid          = plicCtrl_io_bus_r_valid;
   assign plic_rdata           = plicCtrl_io_bus_r_payload_data;
   assign plic_rresp           = plicCtrl_io_bus_r_payload_resp;
   assign plicCtrl_io_sources  = (plicInterrupts >>> 1'd1);
   always @(*) begin
      IBusCachedPlugin_fetcherHalt = 1'b0;
      if (when_CsrPlugin_l1272) begin
         IBusCachedPlugin_fetcherHalt = 1'b1;
      end
      if (when_CsrPlugin_l1390) begin
         IBusCachedPlugin_fetcherHalt = 1'b1;
      end
      if (when_CsrPlugin_l1456) begin
         IBusCachedPlugin_fetcherHalt = 1'b1;
      end
   end

   assign IBusCachedPlugin_forceNoDecodeCond = 1'b0;
   always @(*) begin
      IBusCachedPlugin_incomingInstruction = 1'b0;
      if (when_Fetcher_l242) begin
         IBusCachedPlugin_incomingInstruction = 1'b1;
      end
      if (IBusCachedPlugin_injector_decodeInput_valid) begin
         IBusCachedPlugin_incomingInstruction = 1'b1;
      end
   end

   assign MmuPlugin_ioEndAddr             = (_zz_MmuPlugin_ioEndAddr - 32'h00000001);
   assign BranchPlugin_inDebugNoFetchFlag = 1'b0;
   always @(*) begin
      CsrPlugin_csrMapping_allowCsrSignal = 1'b0;
      if (when_CsrPlugin_l1702) begin
         CsrPlugin_csrMapping_allowCsrSignal = 1'b1;
      end
      if (when_CsrPlugin_l1709) begin
         CsrPlugin_csrMapping_allowCsrSignal = 1'b1;
      end
   end

   always @(*) begin
      CsrPlugin_csrMapping_doForceFailCsr = 1'b0;
      if (execute_CsrPlugin_csr_3072) begin
         if (when_CsrPlugin_l1076) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
         if (when_CsrPlugin_l1077) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
      end
      if (execute_CsrPlugin_csr_3200) begin
         if (when_CsrPlugin_l1076_1) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
         if (when_CsrPlugin_l1077_1) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
      end
      if (execute_CsrPlugin_csr_3074) begin
         if (when_CsrPlugin_l1076_2) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
         if (when_CsrPlugin_l1077_2) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
      end
      if (execute_CsrPlugin_csr_3202) begin
         if (when_CsrPlugin_l1076_3) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
         if (when_CsrPlugin_l1077_3) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
      end
      if (execute_CsrPlugin_csr_3073) begin
         if (when_CsrPlugin_l1076_4) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
         if (when_CsrPlugin_l1077_4) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
      end
      if (execute_CsrPlugin_csr_3201) begin
         if (when_CsrPlugin_l1076_5) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
         if (when_CsrPlugin_l1077_5) begin
            CsrPlugin_csrMapping_doForceFailCsr = 1'b1;
         end
      end
   end

   assign CsrPlugin_csrMapping_readDataSignal = CsrPlugin_csrMapping_readDataInit;
   always @(*) begin
      CsrPlugin_inWfi = 1'b0;
      if (when_CsrPlugin_l1519) begin
         CsrPlugin_inWfi = 1'b1;
      end
   end

   assign CsrPlugin_thirdPartyWake = 1'b0;
   always @(*) begin
      CsrPlugin_jumpInterface_valid = 1'b0;
      if (when_CsrPlugin_l1390) begin
         CsrPlugin_jumpInterface_valid = 1'b1;
      end
      if (when_CsrPlugin_l1456) begin
         CsrPlugin_jumpInterface_valid = 1'b1;
      end
   end

   always @(*) begin
      CsrPlugin_jumpInterface_payload = 32'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
      if (when_CsrPlugin_l1390) begin
         CsrPlugin_jumpInterface_payload = {CsrPlugin_xtvec_base, 2'b00};
      end
      if (when_CsrPlugin_l1456) begin
         case (switch_CsrPlugin_l1460)
            2'b11: begin
               CsrPlugin_jumpInterface_payload = CsrPlugin_mepc;
            end
            2'b01: begin
               CsrPlugin_jumpInterface_payload = CsrPlugin_sepc;
            end
            default: begin
            end
         endcase
      end
   end

   assign CsrPlugin_forceMachineWire     = 1'b0;
   assign CsrPlugin_allowInterrupts      = 1'b1;
   assign CsrPlugin_allowException       = 1'b1;
   assign CsrPlugin_allowEbreakException = 1'b1;
   always @(*) begin
      CsrPlugin_xretAwayFromMachine = 1'b0;
      if (when_CsrPlugin_l1456) begin
         case (switch_CsrPlugin_l1460)
            2'b11: begin
               if (when_CsrPlugin_l1468) begin
                  CsrPlugin_xretAwayFromMachine = 1'b1;
               end
            end
            2'b01: begin
               CsrPlugin_xretAwayFromMachine = 1'b1;
            end
            default: begin
            end
         endcase
      end
   end

   assign IBusCachedPlugin_externalFlush = ({writeBack_arbitration_flushNext,{memory_arbitration_flushNext,{execute_arbitration_flushNext,decode_arbitration_flushNext}}} != 4'b0000);
   assign IBusCachedPlugin_jump_pcLoad_valid = ({CsrPlugin_redoInterface_valid,{CsrPlugin_jumpInterface_valid,{BranchPlugin_jumpInterface_valid,DBusCachedPlugin_redoBranch_valid}}} != 4'b0000);
   assign _zz_IBusCachedPlugin_jump_pcLoad_payload = {
      CsrPlugin_redoInterface_valid,
      {
         BranchPlugin_jumpInterface_valid,
         {CsrPlugin_jumpInterface_valid, DBusCachedPlugin_redoBranch_valid}
      }
   };
   assign _zz_IBusCachedPlugin_jump_pcLoad_payload_1 = (_zz_IBusCachedPlugin_jump_pcLoad_payload & (~ _zz__zz_IBusCachedPlugin_jump_pcLoad_payload_1));
   assign _zz_IBusCachedPlugin_jump_pcLoad_payload_2 = _zz_IBusCachedPlugin_jump_pcLoad_payload_1[3];
   assign _zz_IBusCachedPlugin_jump_pcLoad_payload_3 = (_zz_IBusCachedPlugin_jump_pcLoad_payload_1[1] || _zz_IBusCachedPlugin_jump_pcLoad_payload_2);
   assign _zz_IBusCachedPlugin_jump_pcLoad_payload_4 = (_zz_IBusCachedPlugin_jump_pcLoad_payload_1[2] || _zz_IBusCachedPlugin_jump_pcLoad_payload_2);
   assign IBusCachedPlugin_jump_pcLoad_payload = _zz_IBusCachedPlugin_jump_pcLoad_payload_5;
   always @(*) begin
      IBusCachedPlugin_fetchPc_correction = 1'b0;
      if (IBusCachedPlugin_fetchPc_redo_valid) begin
         IBusCachedPlugin_fetchPc_correction = 1'b1;
      end
      if (IBusCachedPlugin_jump_pcLoad_valid) begin
         IBusCachedPlugin_fetchPc_correction = 1'b1;
      end
   end

   assign IBusCachedPlugin_fetchPc_output_fire = (IBusCachedPlugin_fetchPc_output_valid && IBusCachedPlugin_fetchPc_output_ready);
   assign IBusCachedPlugin_fetchPc_corrected = (IBusCachedPlugin_fetchPc_correction || IBusCachedPlugin_fetchPc_correctionReg);
   always @(*) begin
      IBusCachedPlugin_fetchPc_pcRegPropagate = 1'b0;
      if (IBusCachedPlugin_iBusRsp_stages_1_input_ready) begin
         IBusCachedPlugin_fetchPc_pcRegPropagate = 1'b1;
      end
   end

   assign when_Fetcher_l133 = (IBusCachedPlugin_fetchPc_correction || IBusCachedPlugin_fetchPc_pcRegPropagate);
   assign when_Fetcher_l133_1 = ((! IBusCachedPlugin_fetchPc_output_valid) && IBusCachedPlugin_fetchPc_output_ready);
   always @(*) begin
      IBusCachedPlugin_fetchPc_pc = (IBusCachedPlugin_fetchPc_pcReg + _zz_IBusCachedPlugin_fetchPc_pc);
      if (IBusCachedPlugin_fetchPc_inc) begin
         IBusCachedPlugin_fetchPc_pc[1] = 1'b0;
      end
      if (IBusCachedPlugin_fetchPc_redo_valid) begin
         IBusCachedPlugin_fetchPc_pc = IBusCachedPlugin_fetchPc_redo_payload;
      end
      if (IBusCachedPlugin_jump_pcLoad_valid) begin
         IBusCachedPlugin_fetchPc_pc = IBusCachedPlugin_jump_pcLoad_payload;
      end
      IBusCachedPlugin_fetchPc_pc[0] = 1'b0;
   end

   always @(*) begin
      IBusCachedPlugin_fetchPc_flushed = 1'b0;
      if (IBusCachedPlugin_fetchPc_redo_valid) begin
         IBusCachedPlugin_fetchPc_flushed = 1'b1;
      end
      if (IBusCachedPlugin_jump_pcLoad_valid) begin
         IBusCachedPlugin_fetchPc_flushed = 1'b1;
      end
   end

   assign when_Fetcher_l160 = (IBusCachedPlugin_fetchPc_booted && ((IBusCachedPlugin_fetchPc_output_ready || IBusCachedPlugin_fetchPc_correction) || IBusCachedPlugin_fetchPc_pcRegPropagate));
   assign IBusCachedPlugin_fetchPc_output_valid = ((! IBusCachedPlugin_fetcherHalt) && IBusCachedPlugin_fetchPc_booted);
   assign IBusCachedPlugin_fetchPc_output_payload = IBusCachedPlugin_fetchPc_pc;
   always @(*) begin
      IBusCachedPlugin_decodePc_flushed = 1'b0;
      if (when_Fetcher_l194) begin
         IBusCachedPlugin_decodePc_flushed = 1'b1;
      end
   end

   assign IBusCachedPlugin_decodePc_pcPlus = (IBusCachedPlugin_decodePc_pcReg + _zz_IBusCachedPlugin_decodePc_pcPlus);
   assign IBusCachedPlugin_decodePc_injectedDecode = 1'b0;
   assign when_Fetcher_l182 = (decode_arbitration_isFiring && (! IBusCachedPlugin_decodePc_injectedDecode));
   assign when_Fetcher_l194 = (IBusCachedPlugin_jump_pcLoad_valid && ((! decode_arbitration_isStuck) || decode_arbitration_removeIt));
   always @(*) begin
      IBusCachedPlugin_iBusRsp_redoFetch = 1'b0;
      if (IBusCachedPlugin_rsp_redoFetch) begin
         IBusCachedPlugin_iBusRsp_redoFetch = 1'b1;
      end
   end

   assign IBusCachedPlugin_iBusRsp_stages_0_input_valid = IBusCachedPlugin_fetchPc_output_valid;
   assign IBusCachedPlugin_fetchPc_output_ready = IBusCachedPlugin_iBusRsp_stages_0_input_ready;
   assign IBusCachedPlugin_iBusRsp_stages_0_input_payload = IBusCachedPlugin_fetchPc_output_payload;
   always @(*) begin
      IBusCachedPlugin_iBusRsp_stages_0_halt = 1'b0;
      if (IBusCachedPlugin_cache_io_cpu_prefetch_haltIt) begin
         IBusCachedPlugin_iBusRsp_stages_0_halt = 1'b1;
      end
      if (IBusCachedPlugin_mmuBus_busy) begin
         IBusCachedPlugin_iBusRsp_stages_0_halt = 1'b1;
      end
   end

   assign _zz_IBusCachedPlugin_iBusRsp_stages_0_input_ready = (! IBusCachedPlugin_iBusRsp_stages_0_halt);
   assign IBusCachedPlugin_iBusRsp_stages_0_input_ready = (IBusCachedPlugin_iBusRsp_stages_0_output_ready && _zz_IBusCachedPlugin_iBusRsp_stages_0_input_ready);
   assign IBusCachedPlugin_iBusRsp_stages_0_output_valid = (IBusCachedPlugin_iBusRsp_stages_0_input_valid && _zz_IBusCachedPlugin_iBusRsp_stages_0_input_ready);
   assign IBusCachedPlugin_iBusRsp_stages_0_output_payload = IBusCachedPlugin_iBusRsp_stages_0_input_payload;
   assign IBusCachedPlugin_iBusRsp_stages_1_halt = 1'b0;
   assign _zz_IBusCachedPlugin_iBusRsp_stages_1_input_ready = (! IBusCachedPlugin_iBusRsp_stages_1_halt);
   assign IBusCachedPlugin_iBusRsp_stages_1_input_ready = (IBusCachedPlugin_iBusRsp_stages_1_output_ready && _zz_IBusCachedPlugin_iBusRsp_stages_1_input_ready);
   assign IBusCachedPlugin_iBusRsp_stages_1_output_valid = (IBusCachedPlugin_iBusRsp_stages_1_input_valid && _zz_IBusCachedPlugin_iBusRsp_stages_1_input_ready);
   assign IBusCachedPlugin_iBusRsp_stages_1_output_payload = IBusCachedPlugin_iBusRsp_stages_1_input_payload;
   always @(*) begin
      IBusCachedPlugin_iBusRsp_stages_2_halt = 1'b0;
      if (when_IBusCachedPlugin_l273) begin
         IBusCachedPlugin_iBusRsp_stages_2_halt = 1'b1;
      end
   end

   assign _zz_IBusCachedPlugin_iBusRsp_stages_2_input_ready = (! IBusCachedPlugin_iBusRsp_stages_2_halt);
   assign IBusCachedPlugin_iBusRsp_stages_2_input_ready = (IBusCachedPlugin_iBusRsp_stages_2_output_ready && _zz_IBusCachedPlugin_iBusRsp_stages_2_input_ready);
   assign IBusCachedPlugin_iBusRsp_stages_2_output_valid = (IBusCachedPlugin_iBusRsp_stages_2_input_valid && _zz_IBusCachedPlugin_iBusRsp_stages_2_input_ready);
   assign IBusCachedPlugin_iBusRsp_stages_2_output_payload = IBusCachedPlugin_iBusRsp_stages_2_input_payload;
   assign IBusCachedPlugin_fetchPc_redo_valid = IBusCachedPlugin_iBusRsp_redoFetch;
   always @(*) begin
      IBusCachedPlugin_fetchPc_redo_payload = IBusCachedPlugin_iBusRsp_stages_2_input_payload;
      if (IBusCachedPlugin_decompressor_throw2BytesReg) begin
         IBusCachedPlugin_fetchPc_redo_payload[1] = 1'b1;
      end
   end

   assign IBusCachedPlugin_iBusRsp_flush = (IBusCachedPlugin_externalFlush || IBusCachedPlugin_iBusRsp_redoFetch);
   assign IBusCachedPlugin_iBusRsp_stages_0_output_ready = _zz_IBusCachedPlugin_iBusRsp_stages_0_output_ready;
   assign _zz_IBusCachedPlugin_iBusRsp_stages_0_output_ready = ((1'b0 && (! _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid)) || IBusCachedPlugin_iBusRsp_stages_1_input_ready);
   assign _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid = _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid_1;
   assign IBusCachedPlugin_iBusRsp_stages_1_input_valid = _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid;
   assign IBusCachedPlugin_iBusRsp_stages_1_input_payload = IBusCachedPlugin_fetchPc_pcReg;
   assign IBusCachedPlugin_iBusRsp_stages_1_output_ready = ((1'b0 && (! IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid)) || IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_ready);
   assign IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid = _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid;
   assign IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_payload = _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_payload;
   assign IBusCachedPlugin_iBusRsp_stages_2_input_valid = IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid;
   assign IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_ready = IBusCachedPlugin_iBusRsp_stages_2_input_ready;
   assign IBusCachedPlugin_iBusRsp_stages_2_input_payload = IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_payload;
   always @(*) begin
      IBusCachedPlugin_iBusRsp_readyForError = 1'b1;
      if (IBusCachedPlugin_injector_decodeInput_valid) begin
         IBusCachedPlugin_iBusRsp_readyForError = 1'b0;
      end
   end

   assign when_Fetcher_l242 = (IBusCachedPlugin_iBusRsp_stages_1_input_valid || IBusCachedPlugin_iBusRsp_stages_2_input_valid);
   assign IBusCachedPlugin_decompressor_input_valid = (IBusCachedPlugin_iBusRsp_output_valid && (! IBusCachedPlugin_iBusRsp_redoFetch));
   assign IBusCachedPlugin_decompressor_input_payload_pc = IBusCachedPlugin_iBusRsp_output_payload_pc;
   assign IBusCachedPlugin_decompressor_input_payload_rsp_error = IBusCachedPlugin_iBusRsp_output_payload_rsp_error;
   assign IBusCachedPlugin_decompressor_input_payload_rsp_inst = IBusCachedPlugin_iBusRsp_output_payload_rsp_inst;
   assign IBusCachedPlugin_decompressor_input_payload_isRvc = IBusCachedPlugin_iBusRsp_output_payload_isRvc;
   assign IBusCachedPlugin_iBusRsp_output_ready = IBusCachedPlugin_decompressor_input_ready;
   assign IBusCachedPlugin_decompressor_flushNext = 1'b0;
   assign IBusCachedPlugin_decompressor_consumeCurrent = 1'b0;
   assign IBusCachedPlugin_decompressor_isInputLowRvc = (IBusCachedPlugin_decompressor_input_payload_rsp_inst[1 : 0] != 2'b11);
   assign IBusCachedPlugin_decompressor_isInputHighRvc = (IBusCachedPlugin_decompressor_input_payload_rsp_inst[17 : 16] != 2'b11);
   assign IBusCachedPlugin_decompressor_throw2Bytes = (IBusCachedPlugin_decompressor_throw2BytesReg || IBusCachedPlugin_decompressor_input_payload_pc[1]);
   assign IBusCachedPlugin_decompressor_unaligned = (IBusCachedPlugin_decompressor_throw2Bytes || IBusCachedPlugin_decompressor_bufferValid);
   assign IBusCachedPlugin_decompressor_bufferValidPatched = (IBusCachedPlugin_decompressor_input_valid ? IBusCachedPlugin_decompressor_bufferValid : IBusCachedPlugin_decompressor_bufferValidLatch);
   assign IBusCachedPlugin_decompressor_throw2BytesPatched = (IBusCachedPlugin_decompressor_input_valid ? IBusCachedPlugin_decompressor_throw2Bytes : IBusCachedPlugin_decompressor_throw2BytesLatch);
   assign IBusCachedPlugin_decompressor_raw = (IBusCachedPlugin_decompressor_bufferValidPatched ? {IBusCachedPlugin_decompressor_input_payload_rsp_inst[15 : 0],IBusCachedPlugin_decompressor_bufferData} : {IBusCachedPlugin_decompressor_input_payload_rsp_inst[31 : 16],(IBusCachedPlugin_decompressor_throw2BytesPatched ? IBusCachedPlugin_decompressor_input_payload_rsp_inst[31 : 16] : IBusCachedPlugin_decompressor_input_payload_rsp_inst[15 : 0])});
   assign IBusCachedPlugin_decompressor_isRvc = (IBusCachedPlugin_decompressor_raw[1 : 0] != 2'b11);
   assign _zz_IBusCachedPlugin_decompressor_decompressed = IBusCachedPlugin_decompressor_raw[15 : 0];
   always @(*) begin
      IBusCachedPlugin_decompressor_decompressed = 32'h00000000;
      case (switch_Misc_l44)
         5'h00: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           {
                              {
                                 {
                                    {2'b00, _zz_IBusCachedPlugin_decompressor_decompressed[10 : 7]},
                                    _zz_IBusCachedPlugin_decompressor_decompressed[12 : 11]
                                 },
                                 _zz_IBusCachedPlugin_decompressor_decompressed[5]
                              },
                              _zz_IBusCachedPlugin_decompressor_decompressed[6]
                           },
                           2'b00
                        },
                        5'h02
                     },
                     3'b000
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_2
               },
               7'h13
            };
            if (when_Misc_l47) begin
               IBusCachedPlugin_decompressor_decompressed = 32'h00000000;
            end
         end
         5'h02: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        _zz_IBusCachedPlugin_decompressor_decompressed_3,
                        _zz_IBusCachedPlugin_decompressor_decompressed_1
                     },
                     3'b010
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_2
               },
               7'h03
            };
         end
         5'h06: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           _zz_IBusCachedPlugin_decompressor_decompressed_3[11 : 5],
                           _zz_IBusCachedPlugin_decompressor_decompressed_2
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed_1
                     },
                     3'b010
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_3[4 : 0]
               },
               7'h23
            };
         end
         5'h08: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        _zz_IBusCachedPlugin_decompressor_decompressed_5,
                        _zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]
                     },
                     3'b000
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]
               },
               7'h13
            };
         end
         5'h09: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           _zz_IBusCachedPlugin_decompressor_decompressed_8[20],
                           _zz_IBusCachedPlugin_decompressor_decompressed_8[10 : 1]
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed_8[11]
                     },
                     _zz_IBusCachedPlugin_decompressor_decompressed_8[19 : 12]
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_20
               },
               7'h6f
            };
         end
         5'h0a: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {{_zz_IBusCachedPlugin_decompressor_decompressed_5, 5'h00}, 3'b000},
                  _zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]
               },
               7'h13
            };
         end
         5'h0b: begin
            IBusCachedPlugin_decompressor_decompressed = ((_zz_IBusCachedPlugin_decompressor_decompressed[11 : 7] == 5'h02) ? {{{{{{{{{_zz_IBusCachedPlugin_decompressor_decompressed_12,_zz_IBusCachedPlugin_decompressor_decompressed[4 : 3]},_zz_IBusCachedPlugin_decompressor_decompressed[5]},_zz_IBusCachedPlugin_decompressor_decompressed[2]},_zz_IBusCachedPlugin_decompressor_decompressed[6]},4'b0000},_zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]},3'b000},_zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]},7'h13} : {{_zz_IBusCachedPlugin_decompressor_decompressed_27[31 : 12],_zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]},7'h37});
         end
         5'h0c: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           ((_zz_IBusCachedPlugin_decompressor_decompressed[11 : 10] == 2'b10) ? _zz_IBusCachedPlugin_decompressor_decompressed_26 : {{1'b0,(_zz_IBusCachedPlugin_decompressor_decompressed_28 || _zz_IBusCachedPlugin_decompressor_decompressed_29)},5'h00}),
                           (((! _zz_IBusCachedPlugin_decompressor_decompressed[11]) || _zz_IBusCachedPlugin_decompressor_decompressed_22) ? _zz_IBusCachedPlugin_decompressor_decompressed[6 : 2] : _zz_IBusCachedPlugin_decompressor_decompressed_2)
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed_1
                     },
                     _zz_IBusCachedPlugin_decompressor_decompressed_24
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_1
               },
               (_zz_IBusCachedPlugin_decompressor_decompressed_22 ? 7'h13 : 7'h33)
            };
         end
         5'h0d: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           _zz_IBusCachedPlugin_decompressor_decompressed_15[20],
                           _zz_IBusCachedPlugin_decompressor_decompressed_15[10 : 1]
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed_15[11]
                     },
                     _zz_IBusCachedPlugin_decompressor_decompressed_15[19 : 12]
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_19
               },
               7'h6f
            };
         end
         5'h0e: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           {
                              {
                                 _zz_IBusCachedPlugin_decompressor_decompressed_18[12],
                                 _zz_IBusCachedPlugin_decompressor_decompressed_18[10 : 5]
                              },
                              _zz_IBusCachedPlugin_decompressor_decompressed_19
                           },
                           _zz_IBusCachedPlugin_decompressor_decompressed_1
                        },
                        3'b000
                     },
                     _zz_IBusCachedPlugin_decompressor_decompressed_18[4 : 1]
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_18[11]
               },
               7'h63
            };
         end
         5'h0f: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           {
                              {
                                 _zz_IBusCachedPlugin_decompressor_decompressed_18[12],
                                 _zz_IBusCachedPlugin_decompressor_decompressed_18[10 : 5]
                              },
                              _zz_IBusCachedPlugin_decompressor_decompressed_19
                           },
                           _zz_IBusCachedPlugin_decompressor_decompressed_1
                        },
                        3'b001
                     },
                     _zz_IBusCachedPlugin_decompressor_decompressed_18[4 : 1]
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_18[11]
               },
               7'h63
            };
         end
         5'h10: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {7'h00, _zz_IBusCachedPlugin_decompressor_decompressed[6 : 2]},
                        _zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]
                     },
                     3'b001
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]
               },
               7'h13
            };
         end
         5'h12: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           {
                              {
                                 {4'b0000, _zz_IBusCachedPlugin_decompressor_decompressed[3 : 2]},
                                 _zz_IBusCachedPlugin_decompressor_decompressed[12]
                              },
                              _zz_IBusCachedPlugin_decompressor_decompressed[6 : 4]
                           },
                           2'b00
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed_21
                     },
                     3'b010
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]
               },
               7'h03
            };
         end
         5'h14: begin
            IBusCachedPlugin_decompressor_decompressed = ((_zz_IBusCachedPlugin_decompressor_decompressed[12 : 2] == 11'h400) ? 32'h00100073 : ((_zz_IBusCachedPlugin_decompressor_decompressed[6 : 2] == 5'h00) ? {{{{12'h000,_zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]},3'b000},(_zz_IBusCachedPlugin_decompressor_decompressed[12] ? _zz_IBusCachedPlugin_decompressor_decompressed_20 : _zz_IBusCachedPlugin_decompressor_decompressed_19)},7'h67} : {{{{{_zz_IBusCachedPlugin_decompressor_decompressed_30,_zz_IBusCachedPlugin_decompressor_decompressed_31},(_zz_IBusCachedPlugin_decompressor_decompressed_32 ? _zz_IBusCachedPlugin_decompressor_decompressed_33 : _zz_IBusCachedPlugin_decompressor_decompressed_19)},3'b000},_zz_IBusCachedPlugin_decompressor_decompressed[11 : 7]},7'h33}));
         end
         5'h16: begin
            IBusCachedPlugin_decompressor_decompressed = {
               {
                  {
                     {
                        {
                           _zz_IBusCachedPlugin_decompressor_decompressed_34[11 : 5],
                           _zz_IBusCachedPlugin_decompressor_decompressed[6 : 2]
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed_21
                     },
                     3'b010
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed_35[4 : 0]
               },
               7'h23
            };
         end
         default: begin
         end
      endcase
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_1 = {
      2'b01, _zz_IBusCachedPlugin_decompressor_decompressed[9 : 7]
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_2 = {
      2'b01, _zz_IBusCachedPlugin_decompressor_decompressed[4 : 2]
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_3 = {
      {
         {
            {5'h00, _zz_IBusCachedPlugin_decompressor_decompressed[5]},
            _zz_IBusCachedPlugin_decompressor_decompressed[12 : 10]
         },
         _zz_IBusCachedPlugin_decompressor_decompressed[6]
      },
      2'b00
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_4 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   always @(*) begin
      _zz_IBusCachedPlugin_decompressor_decompressed_5[11] = _zz_IBusCachedPlugin_decompressor_decompressed_4;
      _zz_IBusCachedPlugin_decompressor_decompressed_5[10] = _zz_IBusCachedPlugin_decompressor_decompressed_4;
      _zz_IBusCachedPlugin_decompressor_decompressed_5[9] = _zz_IBusCachedPlugin_decompressor_decompressed_4;
      _zz_IBusCachedPlugin_decompressor_decompressed_5[8] = _zz_IBusCachedPlugin_decompressor_decompressed_4;
      _zz_IBusCachedPlugin_decompressor_decompressed_5[7] = _zz_IBusCachedPlugin_decompressor_decompressed_4;
      _zz_IBusCachedPlugin_decompressor_decompressed_5[6] = _zz_IBusCachedPlugin_decompressor_decompressed_4;
      _zz_IBusCachedPlugin_decompressor_decompressed_5[5] = _zz_IBusCachedPlugin_decompressor_decompressed_4;
      _zz_IBusCachedPlugin_decompressor_decompressed_5[4 : 0] = _zz_IBusCachedPlugin_decompressor_decompressed[6 : 2];
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_6 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   always @(*) begin
      _zz_IBusCachedPlugin_decompressor_decompressed_7[9] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[8] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[7] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[6] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[5] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[4] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[3] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[2] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[1] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
      _zz_IBusCachedPlugin_decompressor_decompressed_7[0] = _zz_IBusCachedPlugin_decompressor_decompressed_6;
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_8 = {
      {
         {
            {
               {
                  {
                     {
                        {
                           _zz_IBusCachedPlugin_decompressor_decompressed_7,
                           _zz_IBusCachedPlugin_decompressor_decompressed[8]
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed[10 : 9]
                     },
                     _zz_IBusCachedPlugin_decompressor_decompressed[6]
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed[7]
               },
               _zz_IBusCachedPlugin_decompressor_decompressed[2]
            },
            _zz_IBusCachedPlugin_decompressor_decompressed[11]
         },
         _zz_IBusCachedPlugin_decompressor_decompressed[5 : 3]
      },
      1'b0
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_9 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   always @(*) begin
      _zz_IBusCachedPlugin_decompressor_decompressed_10[14] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[13] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[12] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[11] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[10] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[9] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[8] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[7] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[6] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[5] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[4] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[3] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[2] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[1] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
      _zz_IBusCachedPlugin_decompressor_decompressed_10[0] = _zz_IBusCachedPlugin_decompressor_decompressed_9;
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_11 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   always @(*) begin
      _zz_IBusCachedPlugin_decompressor_decompressed_12[2] = _zz_IBusCachedPlugin_decompressor_decompressed_11;
      _zz_IBusCachedPlugin_decompressor_decompressed_12[1] = _zz_IBusCachedPlugin_decompressor_decompressed_11;
      _zz_IBusCachedPlugin_decompressor_decompressed_12[0] = _zz_IBusCachedPlugin_decompressor_decompressed_11;
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_13 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   always @(*) begin
      _zz_IBusCachedPlugin_decompressor_decompressed_14[9] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[8] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[7] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[6] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[5] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[4] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[3] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[2] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[1] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
      _zz_IBusCachedPlugin_decompressor_decompressed_14[0] = _zz_IBusCachedPlugin_decompressor_decompressed_13;
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_15 = {
      {
         {
            {
               {
                  {
                     {
                        {
                           _zz_IBusCachedPlugin_decompressor_decompressed_14,
                           _zz_IBusCachedPlugin_decompressor_decompressed[8]
                        },
                        _zz_IBusCachedPlugin_decompressor_decompressed[10 : 9]
                     },
                     _zz_IBusCachedPlugin_decompressor_decompressed[6]
                  },
                  _zz_IBusCachedPlugin_decompressor_decompressed[7]
               },
               _zz_IBusCachedPlugin_decompressor_decompressed[2]
            },
            _zz_IBusCachedPlugin_decompressor_decompressed[11]
         },
         _zz_IBusCachedPlugin_decompressor_decompressed[5 : 3]
      },
      1'b0
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_16 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   always @(*) begin
      _zz_IBusCachedPlugin_decompressor_decompressed_17[4] = _zz_IBusCachedPlugin_decompressor_decompressed_16;
      _zz_IBusCachedPlugin_decompressor_decompressed_17[3] = _zz_IBusCachedPlugin_decompressor_decompressed_16;
      _zz_IBusCachedPlugin_decompressor_decompressed_17[2] = _zz_IBusCachedPlugin_decompressor_decompressed_16;
      _zz_IBusCachedPlugin_decompressor_decompressed_17[1] = _zz_IBusCachedPlugin_decompressor_decompressed_16;
      _zz_IBusCachedPlugin_decompressor_decompressed_17[0] = _zz_IBusCachedPlugin_decompressor_decompressed_16;
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_18 = {
      {
         {
            {
               {
                  _zz_IBusCachedPlugin_decompressor_decompressed_17,
                  _zz_IBusCachedPlugin_decompressor_decompressed[6 : 5]
               },
               _zz_IBusCachedPlugin_decompressor_decompressed[2]
            },
            _zz_IBusCachedPlugin_decompressor_decompressed[11 : 10]
         },
         _zz_IBusCachedPlugin_decompressor_decompressed[4 : 3]
      },
      1'b0
   };
   assign _zz_IBusCachedPlugin_decompressor_decompressed_19 = 5'h00;
   assign _zz_IBusCachedPlugin_decompressor_decompressed_20 = 5'h01;
   assign _zz_IBusCachedPlugin_decompressor_decompressed_21 = 5'h02;
   assign switch_Misc_l44 = {
      _zz_IBusCachedPlugin_decompressor_decompressed[1 : 0],
      _zz_IBusCachedPlugin_decompressor_decompressed[15 : 13]
   };
   assign when_Misc_l47 = (_zz_IBusCachedPlugin_decompressor_decompressed[12 : 2] == 11'h000);
   assign _zz_IBusCachedPlugin_decompressor_decompressed_22 = (_zz_IBusCachedPlugin_decompressor_decompressed[11 : 10] != 2'b11);
   assign switch_Misc_l227 = _zz_IBusCachedPlugin_decompressor_decompressed[11 : 10];
   assign switch_Misc_l227_1 = _zz_IBusCachedPlugin_decompressor_decompressed[6 : 5];
   always @(*) begin
      case (switch_Misc_l227_1)
         2'b00: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_23 = 3'b000;
         end
         2'b01: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_23 = 3'b100;
         end
         2'b10: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_23 = 3'b110;
         end
         default: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_23 = 3'b111;
         end
      endcase
   end

   always @(*) begin
      case (switch_Misc_l227)
         2'b00: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_24 = 3'b101;
         end
         2'b01: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_24 = 3'b101;
         end
         2'b10: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_24 = 3'b111;
         end
         default: begin
            _zz_IBusCachedPlugin_decompressor_decompressed_24 = _zz_IBusCachedPlugin_decompressor_decompressed_23;
         end
      endcase
   end

   assign _zz_IBusCachedPlugin_decompressor_decompressed_25 = _zz_IBusCachedPlugin_decompressor_decompressed[12];
   always @(*) begin
      _zz_IBusCachedPlugin_decompressor_decompressed_26[6] = _zz_IBusCachedPlugin_decompressor_decompressed_25;
      _zz_IBusCachedPlugin_decompressor_decompressed_26[5] = _zz_IBusCachedPlugin_decompressor_decompressed_25;
      _zz_IBusCachedPlugin_decompressor_decompressed_26[4] = _zz_IBusCachedPlugin_decompressor_decompressed_25;
      _zz_IBusCachedPlugin_decompressor_decompressed_26[3] = _zz_IBusCachedPlugin_decompressor_decompressed_25;
      _zz_IBusCachedPlugin_decompressor_decompressed_26[2] = _zz_IBusCachedPlugin_decompressor_decompressed_25;
      _zz_IBusCachedPlugin_decompressor_decompressed_26[1] = _zz_IBusCachedPlugin_decompressor_decompressed_25;
      _zz_IBusCachedPlugin_decompressor_decompressed_26[0] = _zz_IBusCachedPlugin_decompressor_decompressed_25;
   end

   assign IBusCachedPlugin_decompressor_output_valid = (IBusCachedPlugin_decompressor_input_valid && (! ((IBusCachedPlugin_decompressor_throw2Bytes && (! IBusCachedPlugin_decompressor_bufferValid)) && (! IBusCachedPlugin_decompressor_isInputHighRvc))));
   assign IBusCachedPlugin_decompressor_output_payload_pc = IBusCachedPlugin_decompressor_input_payload_pc;
   assign IBusCachedPlugin_decompressor_output_payload_isRvc = IBusCachedPlugin_decompressor_isRvc;
   assign IBusCachedPlugin_decompressor_output_payload_rsp_inst = (IBusCachedPlugin_decompressor_isRvc ? IBusCachedPlugin_decompressor_decompressed : IBusCachedPlugin_decompressor_raw);
   assign IBusCachedPlugin_decompressor_input_ready = (IBusCachedPlugin_decompressor_output_ready && (((! IBusCachedPlugin_iBusRsp_stages_2_input_valid) || IBusCachedPlugin_decompressor_flushNext) || ((! (IBusCachedPlugin_decompressor_bufferValid && IBusCachedPlugin_decompressor_isInputHighRvc)) && (! (((! IBusCachedPlugin_decompressor_unaligned) && IBusCachedPlugin_decompressor_isInputLowRvc) && IBusCachedPlugin_decompressor_isInputHighRvc)))));
   assign IBusCachedPlugin_decompressor_output_fire = (IBusCachedPlugin_decompressor_output_valid && IBusCachedPlugin_decompressor_output_ready);
   assign IBusCachedPlugin_decompressor_bufferFill = (((((! IBusCachedPlugin_decompressor_unaligned) && IBusCachedPlugin_decompressor_isInputLowRvc) && (! IBusCachedPlugin_decompressor_isInputHighRvc)) || (IBusCachedPlugin_decompressor_bufferValid && (! IBusCachedPlugin_decompressor_isInputHighRvc))) || ((IBusCachedPlugin_decompressor_throw2Bytes && (! IBusCachedPlugin_decompressor_isRvc)) && (! IBusCachedPlugin_decompressor_isInputHighRvc)));
   assign when_Fetcher_l285 = (IBusCachedPlugin_decompressor_output_ready && IBusCachedPlugin_decompressor_input_valid);
   assign when_Fetcher_l288 = (IBusCachedPlugin_decompressor_output_ready && IBusCachedPlugin_decompressor_input_valid);
   assign when_Fetcher_l293 = (IBusCachedPlugin_externalFlush || IBusCachedPlugin_decompressor_consumeCurrent);
   assign IBusCachedPlugin_decompressor_output_ready = ((1'b0 && (! IBusCachedPlugin_injector_decodeInput_valid)) || IBusCachedPlugin_injector_decodeInput_ready);
   assign IBusCachedPlugin_injector_decodeInput_valid = _zz_IBusCachedPlugin_injector_decodeInput_valid;
   assign IBusCachedPlugin_injector_decodeInput_payload_pc = _zz_IBusCachedPlugin_injector_decodeInput_payload_pc;
   assign IBusCachedPlugin_injector_decodeInput_payload_rsp_error = _zz_IBusCachedPlugin_injector_decodeInput_payload_rsp_error;
   assign IBusCachedPlugin_injector_decodeInput_payload_rsp_inst = _zz_IBusCachedPlugin_injector_decodeInput_payload_rsp_inst;
   assign IBusCachedPlugin_injector_decodeInput_payload_isRvc = _zz_IBusCachedPlugin_injector_decodeInput_payload_isRvc;
   assign when_Fetcher_l331 = (!1'b0);
   assign when_Fetcher_l331_1 = (!execute_arbitration_isStuck);
   assign when_Fetcher_l331_2 = (!memory_arbitration_isStuck);
   assign when_Fetcher_l331_3 = (!writeBack_arbitration_isStuck);
   assign IBusCachedPlugin_pcValids_0 = IBusCachedPlugin_injector_nextPcCalc_valids_0;
   assign IBusCachedPlugin_pcValids_1 = IBusCachedPlugin_injector_nextPcCalc_valids_1;
   assign IBusCachedPlugin_pcValids_2 = IBusCachedPlugin_injector_nextPcCalc_valids_2;
   assign IBusCachedPlugin_pcValids_3 = IBusCachedPlugin_injector_nextPcCalc_valids_3;
   assign IBusCachedPlugin_injector_decodeInput_ready = (!decode_arbitration_isStuck);
   always @(*) begin
      decode_arbitration_isValid = IBusCachedPlugin_injector_decodeInput_valid;
      if (IBusCachedPlugin_forceNoDecodeCond) begin
         decode_arbitration_isValid = 1'b0;
      end
   end

   assign iBus_cmd_valid = IBusCachedPlugin_cache_io_mem_cmd_valid;
   always @(*) begin
      iBus_cmd_payload_address = IBusCachedPlugin_cache_io_mem_cmd_payload_address;
      iBus_cmd_payload_address = IBusCachedPlugin_cache_io_mem_cmd_payload_address;
   end

   assign iBus_cmd_payload_size = IBusCachedPlugin_cache_io_mem_cmd_payload_size;
   assign IBusCachedPlugin_s0_tightlyCoupledHit = 1'b0;
   assign IBusCachedPlugin_cache_io_cpu_prefetch_isValid = (IBusCachedPlugin_iBusRsp_stages_0_input_valid && (! IBusCachedPlugin_s0_tightlyCoupledHit));
   assign IBusCachedPlugin_mmuBus_cmd_0_isValid = IBusCachedPlugin_cache_io_cpu_prefetch_isValid;
   assign IBusCachedPlugin_mmuBus_cmd_0_isStuck = (!IBusCachedPlugin_iBusRsp_stages_0_input_ready);
   assign IBusCachedPlugin_mmuBus_cmd_0_virtualAddress = IBusCachedPlugin_iBusRsp_stages_0_input_payload;
   assign IBusCachedPlugin_mmuBus_cmd_0_bypassTranslation = 1'b0;
   assign IBusCachedPlugin_cache_io_cpu_fetch_isValid = (IBusCachedPlugin_iBusRsp_stages_1_input_valid && (! IBusCachedPlugin_s1_tightlyCoupledHit));
   assign IBusCachedPlugin_cache_io_cpu_fetch_isStuck = (! IBusCachedPlugin_iBusRsp_stages_1_input_ready);
   assign IBusCachedPlugin_mmuBus_cmd_1_isValid = IBusCachedPlugin_cache_io_cpu_fetch_isValid;
   assign IBusCachedPlugin_mmuBus_cmd_1_isStuck = (!IBusCachedPlugin_iBusRsp_stages_1_input_ready);
   assign IBusCachedPlugin_mmuBus_cmd_1_virtualAddress = IBusCachedPlugin_iBusRsp_stages_1_input_payload;
   assign IBusCachedPlugin_mmuBus_cmd_1_bypassTranslation = 1'b0;
   assign IBusCachedPlugin_mmuBus_end = (IBusCachedPlugin_iBusRsp_stages_1_input_ready || IBusCachedPlugin_externalFlush);
   assign IBusCachedPlugin_cache_io_cpu_decode_isValid = (IBusCachedPlugin_iBusRsp_stages_2_input_valid && (! IBusCachedPlugin_s2_tightlyCoupledHit));
   assign IBusCachedPlugin_cache_io_cpu_decode_isStuck = (! IBusCachedPlugin_iBusRsp_stages_2_input_ready);
   assign IBusCachedPlugin_cache_io_cpu_decode_isUser = (CsrPlugin_privilege == 2'b00);
   assign IBusCachedPlugin_rsp_iBusRspOutputHalt = 1'b0;
   assign IBusCachedPlugin_rsp_issueDetected = 1'b0;
   always @(*) begin
      IBusCachedPlugin_rsp_redoFetch = 1'b0;
      if (when_IBusCachedPlugin_l245) begin
         IBusCachedPlugin_rsp_redoFetch = 1'b1;
      end
      if (when_IBusCachedPlugin_l256) begin
         IBusCachedPlugin_rsp_redoFetch = 1'b1;
      end
   end

   always @(*) begin
      IBusCachedPlugin_cache_io_cpu_fill_valid = (IBusCachedPlugin_rsp_redoFetch && (! IBusCachedPlugin_cache_io_cpu_decode_mmuRefilling));
      if (when_IBusCachedPlugin_l256) begin
         IBusCachedPlugin_cache_io_cpu_fill_valid = 1'b1;
      end
   end

   always @(*) begin
      IBusCachedPlugin_decodeExceptionPort_valid = 1'b0;
      if (when_IBusCachedPlugin_l250) begin
         IBusCachedPlugin_decodeExceptionPort_valid = IBusCachedPlugin_iBusRsp_readyForError;
      end
      if (when_IBusCachedPlugin_l262) begin
         IBusCachedPlugin_decodeExceptionPort_valid = IBusCachedPlugin_iBusRsp_readyForError;
      end
   end

   always @(*) begin
      IBusCachedPlugin_decodeExceptionPort_payload_code = 4'bxxxx;
      if (when_IBusCachedPlugin_l250) begin
         IBusCachedPlugin_decodeExceptionPort_payload_code = 4'b1100;
      end
      if (when_IBusCachedPlugin_l262) begin
         IBusCachedPlugin_decodeExceptionPort_payload_code = 4'b0001;
      end
   end

   assign IBusCachedPlugin_decodeExceptionPort_payload_badAddr = {
      IBusCachedPlugin_iBusRsp_stages_2_input_payload[31 : 2], 2'b00
   };
   assign when_IBusCachedPlugin_l245 = ((IBusCachedPlugin_cache_io_cpu_decode_isValid && IBusCachedPlugin_cache_io_cpu_decode_mmuRefilling) && (! IBusCachedPlugin_rsp_issueDetected));
   assign when_IBusCachedPlugin_l250 = ((IBusCachedPlugin_cache_io_cpu_decode_isValid && IBusCachedPlugin_cache_io_cpu_decode_mmuException) && (! IBusCachedPlugin_rsp_issueDetected_1));
   assign when_IBusCachedPlugin_l256 = ((IBusCachedPlugin_cache_io_cpu_decode_isValid && IBusCachedPlugin_cache_io_cpu_decode_cacheMiss) && (! IBusCachedPlugin_rsp_issueDetected_2));
   assign when_IBusCachedPlugin_l262 = ((IBusCachedPlugin_cache_io_cpu_decode_isValid && IBusCachedPlugin_cache_io_cpu_decode_error) && (! IBusCachedPlugin_rsp_issueDetected_3));
   assign when_IBusCachedPlugin_l273 = (IBusCachedPlugin_rsp_issueDetected_4 || IBusCachedPlugin_rsp_iBusRspOutputHalt);
   assign IBusCachedPlugin_iBusRsp_output_valid = IBusCachedPlugin_iBusRsp_stages_2_output_valid;
   assign IBusCachedPlugin_iBusRsp_stages_2_output_ready = IBusCachedPlugin_iBusRsp_output_ready;
   assign IBusCachedPlugin_iBusRsp_output_payload_rsp_inst = IBusCachedPlugin_cache_io_cpu_decode_data;
   assign IBusCachedPlugin_iBusRsp_output_payload_pc = IBusCachedPlugin_iBusRsp_stages_2_output_payload;
   assign IBusCachedPlugin_cache_io_flush = (decode_arbitration_isValid && decode_FLUSH_ALL);
   assign dBus_cmd_valid = dataCache_1_io_mem_cmd_valid;
   assign dBus_cmd_payload_wr = dataCache_1_io_mem_cmd_payload_wr;
   assign dBus_cmd_payload_uncached = dataCache_1_io_mem_cmd_payload_uncached;
   assign dBus_cmd_payload_address = dataCache_1_io_mem_cmd_payload_address;
   assign dBus_cmd_payload_data = dataCache_1_io_mem_cmd_payload_data;
   assign dBus_cmd_payload_mask = dataCache_1_io_mem_cmd_payload_mask;
   assign dBus_cmd_payload_size = dataCache_1_io_mem_cmd_payload_size;
   assign dBus_cmd_payload_last = dataCache_1_io_mem_cmd_payload_last;
   assign when_DBusCachedPlugin_l343 = ((DBusCachedPlugin_mmuBus_busy && decode_arbitration_isValid) && decode_MEMORY_ENABLE);
   always @(*) begin
      _zz_decode_MEMORY_FORCE_CONSTISTENCY = 1'b0;
      if (when_DBusCachedPlugin_l351) begin
         if (decode_MEMORY_LRSC) begin
            _zz_decode_MEMORY_FORCE_CONSTISTENCY = 1'b1;
         end
         if (decode_MEMORY_AMO) begin
            _zz_decode_MEMORY_FORCE_CONSTISTENCY = 1'b1;
         end
      end
   end

   assign when_DBusCachedPlugin_l351    = decode_INSTRUCTION[25];
   assign execute_DBusCachedPlugin_size = execute_INSTRUCTION[13 : 12];
   always @(*) begin
      dataCache_1_io_cpu_execute_isValid = (execute_arbitration_isValid && execute_MEMORY_ENABLE);
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            if (when_DBusCachedPlugin_l596) begin
               dataCache_1_io_cpu_execute_isValid = 1'b1;
            end
         end
      end
   end

   always @(*) begin
      dataCache_1_io_cpu_execute_address = execute_SRC_ADD;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            dataCache_1_io_cpu_execute_address = MmuPlugin_dBusAccess_cmd_payload_address;
         end
      end
   end

   always @(*) begin
      dataCache_1_io_cpu_execute_args_wr = execute_MEMORY_WR;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            dataCache_1_io_cpu_execute_args_wr = 1'b0;
         end
      end
   end

   always @(*) begin
      case (execute_DBusCachedPlugin_size)
         2'b00: begin
            _zz_execute_MEMORY_STORE_DATA_RF = {
               {{execute_RS2[7 : 0], execute_RS2[7 : 0]}, execute_RS2[7 : 0]}, execute_RS2[7 : 0]
            };
         end
         2'b01: begin
            _zz_execute_MEMORY_STORE_DATA_RF = {execute_RS2[15 : 0], execute_RS2[15 : 0]};
         end
         default: begin
            _zz_execute_MEMORY_STORE_DATA_RF = execute_RS2[31 : 0];
         end
      endcase
   end

   always @(*) begin
      dataCache_1_io_cpu_execute_args_size = execute_DBusCachedPlugin_size;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            dataCache_1_io_cpu_execute_args_size = MmuPlugin_dBusAccess_cmd_payload_size;
         end
      end
   end

   assign DBusCachedPlugin_mmuBus_cmd_0_isValid        = dataCache_1_io_cpu_execute_isValid;
   assign DBusCachedPlugin_mmuBus_cmd_0_isStuck        = execute_arbitration_isStuck;
   assign DBusCachedPlugin_mmuBus_cmd_0_virtualAddress = execute_SRC_ADD;
   always @(*) begin
      DBusCachedPlugin_mmuBus_cmd_0_bypassTranslation = 1'b0;
      if (execute_IS_DBUS_SHARING) begin
         DBusCachedPlugin_mmuBus_cmd_0_bypassTranslation = 1'b1;
      end
   end

   assign dataCache_1_io_cpu_flush_valid = (execute_arbitration_isValid && execute_MEMORY_MANAGMENT);
   assign dataCache_1_io_cpu_flush_payload_singleLine = (execute_INSTRUCTION[19 : 15] != 5'h00);
   assign dataCache_1_io_cpu_flush_payload_lineId = _zz_io_cpu_flush_payload_lineId[5:0];
   assign toplevel_dataCache_1_io_cpu_flush_isStall = (dataCache_1_io_cpu_flush_valid && (! dataCache_1_io_cpu_flush_ready));
   assign when_DBusCachedPlugin_l385 = (toplevel_dataCache_1_io_cpu_flush_isStall || dataCache_1_io_cpu_execute_haltIt);
   always @(*) begin
      dataCache_1_io_cpu_execute_args_isLrsc = 1'b0;
      if (execute_MEMORY_LRSC) begin
         dataCache_1_io_cpu_execute_args_isLrsc = 1'b1;
      end
   end

   assign dataCache_1_io_cpu_execute_args_amoCtrl_alu = execute_INSTRUCTION[31 : 29];
   assign dataCache_1_io_cpu_execute_args_amoCtrl_swap = execute_INSTRUCTION[27];
   assign when_DBusCachedPlugin_l401 = (dataCache_1_io_cpu_execute_refilling && execute_arbitration_isValid);
   always @(*) begin
      dataCache_1_io_cpu_memory_isValid = (memory_arbitration_isValid && memory_MEMORY_ENABLE);
      if (memory_IS_DBUS_SHARING) begin
         dataCache_1_io_cpu_memory_isValid = 1'b1;
      end
   end

   assign dataCache_1_io_cpu_memory_address            = memory_REGFILE_WRITE_DATA;
   assign DBusCachedPlugin_mmuBus_cmd_1_isValid        = dataCache_1_io_cpu_memory_isValid;
   assign DBusCachedPlugin_mmuBus_cmd_1_isStuck        = memory_arbitration_isStuck;
   assign DBusCachedPlugin_mmuBus_cmd_1_virtualAddress = dataCache_1_io_cpu_memory_address;
   always @(*) begin
      DBusCachedPlugin_mmuBus_cmd_1_bypassTranslation = 1'b0;
      if (memory_IS_DBUS_SHARING) begin
         DBusCachedPlugin_mmuBus_cmd_1_bypassTranslation = 1'b1;
      end
   end

   assign DBusCachedPlugin_mmuBus_end = ((! memory_arbitration_isStuck) || memory_arbitration_removeIt);
   always @(*) begin
      dataCache_1_io_cpu_memory_mmuRsp_isIoAccess = DBusCachedPlugin_mmuBus_rsp_isIoAccess;
      if (when_DBusCachedPlugin_l463) begin
         dataCache_1_io_cpu_memory_mmuRsp_isIoAccess = 1'b1;
      end
   end

   assign when_DBusCachedPlugin_l463 = (1'b0 && (!dataCache_1_io_cpu_memory_isWrite));
   always @(*) begin
      dataCache_1_io_cpu_writeBack_isValid = (writeBack_arbitration_isValid && writeBack_MEMORY_ENABLE);
      if (writeBack_IS_DBUS_SHARING) begin
         dataCache_1_io_cpu_writeBack_isValid = 1'b1;
      end
      if (writeBack_arbitration_haltByOther) begin
         dataCache_1_io_cpu_writeBack_isValid = 1'b0;
      end
   end

   assign dataCache_1_io_cpu_writeBack_isUser            = (CsrPlugin_privilege == 2'b00);
   assign dataCache_1_io_cpu_writeBack_address           = writeBack_REGFILE_WRITE_DATA;
   assign dataCache_1_io_cpu_writeBack_storeData[31 : 0] = writeBack_MEMORY_STORE_DATA_RF;
   always @(*) begin
      DBusCachedPlugin_redoBranch_valid = 1'b0;
      if (when_DBusCachedPlugin_l524) begin
         if (dataCache_1_io_cpu_redo) begin
            DBusCachedPlugin_redoBranch_valid = 1'b1;
         end
      end
   end

   assign DBusCachedPlugin_redoBranch_payload = writeBack_PC;
   always @(*) begin
      DBusCachedPlugin_exceptionBus_valid = 1'b0;
      if (when_DBusCachedPlugin_l524) begin
         if (dataCache_1_io_cpu_writeBack_accessError) begin
            DBusCachedPlugin_exceptionBus_valid = 1'b1;
         end
         if (dataCache_1_io_cpu_writeBack_mmuException) begin
            DBusCachedPlugin_exceptionBus_valid = 1'b1;
         end
         if (dataCache_1_io_cpu_writeBack_unalignedAccess) begin
            DBusCachedPlugin_exceptionBus_valid = 1'b1;
         end
         if (dataCache_1_io_cpu_redo) begin
            DBusCachedPlugin_exceptionBus_valid = 1'b0;
         end
      end
   end

   assign DBusCachedPlugin_exceptionBus_payload_badAddr = writeBack_REGFILE_WRITE_DATA;
   always @(*) begin
      DBusCachedPlugin_exceptionBus_payload_code = 4'bxxxx;
      if (when_DBusCachedPlugin_l524) begin
         if (dataCache_1_io_cpu_writeBack_accessError) begin
            DBusCachedPlugin_exceptionBus_payload_code = {
               1'd0, _zz_DBusCachedPlugin_exceptionBus_payload_code
            };
         end
         if (dataCache_1_io_cpu_writeBack_mmuException) begin
            DBusCachedPlugin_exceptionBus_payload_code = (writeBack_MEMORY_WR ? 4'b1111 : 4'b1101);
         end
         if (dataCache_1_io_cpu_writeBack_unalignedAccess) begin
            DBusCachedPlugin_exceptionBus_payload_code = {
               1'd0, _zz_DBusCachedPlugin_exceptionBus_payload_code_1
            };
         end
      end
   end

   assign when_DBusCachedPlugin_l524 = (writeBack_arbitration_isValid && writeBack_MEMORY_ENABLE);
   assign when_DBusCachedPlugin_l544 = (dataCache_1_io_cpu_writeBack_isValid && dataCache_1_io_cpu_writeBack_haltIt);
   assign writeBack_DBusCachedPlugin_rspData = dataCache_1_io_cpu_writeBack_data;
   assign writeBack_DBusCachedPlugin_rspSplits_0 = writeBack_DBusCachedPlugin_rspData[7 : 0];
   assign writeBack_DBusCachedPlugin_rspSplits_1 = writeBack_DBusCachedPlugin_rspData[15 : 8];
   assign writeBack_DBusCachedPlugin_rspSplits_2 = writeBack_DBusCachedPlugin_rspData[23 : 16];
   assign writeBack_DBusCachedPlugin_rspSplits_3 = writeBack_DBusCachedPlugin_rspData[31 : 24];
   always @(*) begin
      writeBack_DBusCachedPlugin_rspShifted[7 : 0]   = _zz_writeBack_DBusCachedPlugin_rspShifted;
      writeBack_DBusCachedPlugin_rspShifted[15 : 8]  = _zz_writeBack_DBusCachedPlugin_rspShifted_2;
      writeBack_DBusCachedPlugin_rspShifted[23 : 16] = writeBack_DBusCachedPlugin_rspSplits_2;
      writeBack_DBusCachedPlugin_rspShifted[31 : 24] = writeBack_DBusCachedPlugin_rspSplits_3;
   end

   always @(*) begin
      writeBack_DBusCachedPlugin_rspRf = writeBack_DBusCachedPlugin_rspShifted[31 : 0];
      if (when_DBusCachedPlugin_l561) begin
         writeBack_DBusCachedPlugin_rspRf = {31'd0, _zz_writeBack_DBusCachedPlugin_rspRf};
      end
   end

   assign when_DBusCachedPlugin_l561 = (writeBack_MEMORY_LRSC && writeBack_MEMORY_WR);
   assign switch_Misc_l227_2 = writeBack_INSTRUCTION[13 : 12];
   assign _zz_writeBack_DBusCachedPlugin_rspFormated = (writeBack_DBusCachedPlugin_rspRf[7] && (! writeBack_INSTRUCTION[14]));
   always @(*) begin
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[31] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[30] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[29] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[28] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[27] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[26] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[25] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[24] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[23] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[22] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[21] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[20] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[19] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[18] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[17] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[16] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[15] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[14] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[13] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[12] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[11] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[10] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[9] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[8] = _zz_writeBack_DBusCachedPlugin_rspFormated;
      _zz_writeBack_DBusCachedPlugin_rspFormated_1[7 : 0] = writeBack_DBusCachedPlugin_rspRf[7 : 0];
   end

   assign _zz_writeBack_DBusCachedPlugin_rspFormated_2 = (writeBack_DBusCachedPlugin_rspRf[15] && (! writeBack_INSTRUCTION[14]));
   always @(*) begin
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[31] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[30] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[29] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[28] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[27] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[26] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[25] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[24] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[23] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[22] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[21] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[20] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[19] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[18] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[17] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[16] = _zz_writeBack_DBusCachedPlugin_rspFormated_2;
      _zz_writeBack_DBusCachedPlugin_rspFormated_3[15 : 0] = writeBack_DBusCachedPlugin_rspRf[15 : 0];
   end

   always @(*) begin
      case (switch_Misc_l227_2)
         2'b00: begin
            writeBack_DBusCachedPlugin_rspFormated = _zz_writeBack_DBusCachedPlugin_rspFormated_1;
         end
         2'b01: begin
            writeBack_DBusCachedPlugin_rspFormated = _zz_writeBack_DBusCachedPlugin_rspFormated_3;
         end
         default: begin
            writeBack_DBusCachedPlugin_rspFormated = writeBack_DBusCachedPlugin_rspRf;
         end
      endcase
   end

   assign when_DBusCachedPlugin_l571 = (writeBack_arbitration_isValid && writeBack_MEMORY_ENABLE);
   always @(*) begin
      MmuPlugin_dBusAccess_cmd_ready = 1'b0;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            if (when_DBusCachedPlugin_l596) begin
               MmuPlugin_dBusAccess_cmd_ready = (!execute_arbitration_isStuck);
            end
         end
      end
   end

   always @(*) begin
      DBusCachedPlugin_forceDatapath = 1'b0;
      if (MmuPlugin_dBusAccess_cmd_valid) begin
         if (when_DBusCachedPlugin_l595) begin
            DBusCachedPlugin_forceDatapath = 1'b1;
         end
      end
   end

   assign when_DBusCachedPlugin_l595 = (! ({(writeBack_arbitration_isValid || CsrPlugin_exceptionPendings_3),{(memory_arbitration_isValid || CsrPlugin_exceptionPendings_2),(execute_arbitration_isValid || CsrPlugin_exceptionPendings_1)}} != 3'b000));
   assign when_DBusCachedPlugin_l596 = (!dataCache_1_io_cpu_execute_refilling);
   assign MmuPlugin_dBusAccess_cmd_fire = (MmuPlugin_dBusAccess_cmd_valid && MmuPlugin_dBusAccess_cmd_ready);
   assign MmuPlugin_dBusAccess_rsp_valid = ((writeBack_IS_DBUS_SHARING && (! dataCache_1_io_cpu_writeBack_isWrite)) && (dataCache_1_io_cpu_redo || (! dataCache_1_io_cpu_writeBack_haltIt)));
   assign MmuPlugin_dBusAccess_rsp_payload_data = writeBack_DBusCachedPlugin_rspRf;
   assign MmuPlugin_dBusAccess_rsp_payload_error = (dataCache_1_io_cpu_writeBack_unalignedAccess || dataCache_1_io_cpu_writeBack_accessError);
   assign MmuPlugin_dBusAccess_rsp_payload_redo = dataCache_1_io_cpu_redo;
   assign when_MmuPlugin_l129 = (!IBusCachedPlugin_mmuBus_cmd_1_isStuck);
   always @(*) begin
      MmuPlugin_ports_0_requireMmuLockupCalc = ((1'b1 && (! IBusCachedPlugin_mmuBus_cmd_0_bypassTranslation)) && MmuPlugin_satp_mode);
      if (when_MmuPlugin_l143) begin
         MmuPlugin_ports_0_requireMmuLockupCalc = 1'b0;
      end
      if (when_MmuPlugin_l144) begin
         MmuPlugin_ports_0_requireMmuLockupCalc = 1'b0;
      end
   end

   assign when_MmuPlugin_l143 = ((!MmuPlugin_status_mprv) && (CsrPlugin_privilege == 2'b11));
   assign when_MmuPlugin_l144 = (CsrPlugin_privilege == 2'b11);
   assign MmuPlugin_ports_0_cacheHitsCalc = {
      ((MmuPlugin_ports_0_cache_3_valid && (MmuPlugin_ports_0_cache_3_virtualAddress_1 == IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22])) && (MmuPlugin_ports_0_cache_3_superPage || (MmuPlugin_ports_0_cache_3_virtualAddress_0 == IBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12]))),
      {
         ((MmuPlugin_ports_0_cache_2_valid && (MmuPlugin_ports_0_cache_2_virtualAddress_1 == _zz_MmuPlugin_ports_0_cacheHitsCalc)) && (MmuPlugin_ports_0_cache_2_superPage || (MmuPlugin_ports_0_cache_2_virtualAddress_0 == _zz_MmuPlugin_ports_0_cacheHitsCalc_1))),
         {
            ((MmuPlugin_ports_0_cache_1_valid && _zz_MmuPlugin_ports_0_cacheHitsCalc_2) && (MmuPlugin_ports_0_cache_1_superPage || _zz_MmuPlugin_ports_0_cacheHitsCalc_3)),
            ((MmuPlugin_ports_0_cache_0_valid && _zz_MmuPlugin_ports_0_cacheHitsCalc_4) && (MmuPlugin_ports_0_cache_0_superPage || _zz_MmuPlugin_ports_0_cacheHitsCalc_5))
         }
      }
   };
   assign when_MmuPlugin_l136 = (!IBusCachedPlugin_mmuBus_cmd_1_isStuck);
   assign when_MmuPlugin_l136_1 = (!IBusCachedPlugin_mmuBus_cmd_1_isStuck);
   assign MmuPlugin_ports_0_cacheHit = (|MmuPlugin_ports_0_cacheHits);
   assign _zz_MmuPlugin_ports_0_cacheLine_valid = MmuPlugin_ports_0_cacheHits[3];
   assign _zz_MmuPlugin_ports_0_cacheLine_valid_1 = (MmuPlugin_ports_0_cacheHits[1] || _zz_MmuPlugin_ports_0_cacheLine_valid);
   assign _zz_MmuPlugin_ports_0_cacheLine_valid_2 = (MmuPlugin_ports_0_cacheHits[2] || _zz_MmuPlugin_ports_0_cacheLine_valid);
   assign _zz_MmuPlugin_ports_0_cacheLine_valid_3 = {
      _zz_MmuPlugin_ports_0_cacheLine_valid_2, _zz_MmuPlugin_ports_0_cacheLine_valid_1
   };
   assign MmuPlugin_ports_0_cacheLine_valid = _zz_MmuPlugin_ports_0_cacheLine_valid_4;
   assign MmuPlugin_ports_0_cacheLine_exception = _zz_MmuPlugin_ports_0_cacheLine_exception;
   assign MmuPlugin_ports_0_cacheLine_superPage = _zz_MmuPlugin_ports_0_cacheLine_superPage;
   assign MmuPlugin_ports_0_cacheLine_virtualAddress_0 = _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_0;
   assign MmuPlugin_ports_0_cacheLine_virtualAddress_1 = _zz_MmuPlugin_ports_0_cacheLine_virtualAddress_1;
   assign MmuPlugin_ports_0_cacheLine_physicalAddress_0 = _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_0;
   assign MmuPlugin_ports_0_cacheLine_physicalAddress_1 = _zz_MmuPlugin_ports_0_cacheLine_physicalAddress_1;
   assign MmuPlugin_ports_0_cacheLine_allowRead = _zz_MmuPlugin_ports_0_cacheLine_allowRead;
   assign MmuPlugin_ports_0_cacheLine_allowWrite = _zz_MmuPlugin_ports_0_cacheLine_allowWrite;
   assign MmuPlugin_ports_0_cacheLine_allowExecute = _zz_MmuPlugin_ports_0_cacheLine_allowExecute;
   assign MmuPlugin_ports_0_cacheLine_allowUser = _zz_MmuPlugin_ports_0_cacheLine_allowUser;
   always @(*) begin
      MmuPlugin_ports_0_entryToReplace_willIncrement = 1'b0;
      if (when_MmuPlugin_l302) begin
         if (when_MmuPlugin_l304) begin
            MmuPlugin_ports_0_entryToReplace_willIncrement = 1'b1;
         end
      end
   end

   assign MmuPlugin_ports_0_entryToReplace_willClear = 1'b0;
   assign MmuPlugin_ports_0_entryToReplace_willOverflowIfInc = (MmuPlugin_ports_0_entryToReplace_value == 2'b11);
   assign MmuPlugin_ports_0_entryToReplace_willOverflow = (MmuPlugin_ports_0_entryToReplace_willOverflowIfInc && MmuPlugin_ports_0_entryToReplace_willIncrement);
   always @(*) begin
      MmuPlugin_ports_0_entryToReplace_valueNext = (MmuPlugin_ports_0_entryToReplace_value + _zz_MmuPlugin_ports_0_entryToReplace_valueNext);
      if (MmuPlugin_ports_0_entryToReplace_willClear) begin
         MmuPlugin_ports_0_entryToReplace_valueNext = 2'b00;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_0_requireMmuLockup) begin
         IBusCachedPlugin_mmuBus_rsp_physicalAddress = {
            {
               MmuPlugin_ports_0_cacheLine_physicalAddress_1,
               (MmuPlugin_ports_0_cacheLine_superPage ? IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_0_cacheLine_physicalAddress_0)
            },
            IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
         };
      end else begin
         IBusCachedPlugin_mmuBus_rsp_physicalAddress = IBusCachedPlugin_mmuBus_cmd_1_virtualAddress;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_0_requireMmuLockup) begin
         IBusCachedPlugin_mmuBus_rsp_allowRead = (MmuPlugin_ports_0_cacheLine_allowRead || (MmuPlugin_status_mxr && MmuPlugin_ports_0_cacheLine_allowExecute));
      end else begin
         IBusCachedPlugin_mmuBus_rsp_allowRead = 1'b1;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_0_requireMmuLockup) begin
         IBusCachedPlugin_mmuBus_rsp_allowWrite = MmuPlugin_ports_0_cacheLine_allowWrite;
      end else begin
         IBusCachedPlugin_mmuBus_rsp_allowWrite = 1'b1;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_0_requireMmuLockup) begin
         IBusCachedPlugin_mmuBus_rsp_allowExecute = MmuPlugin_ports_0_cacheLine_allowExecute;
      end else begin
         IBusCachedPlugin_mmuBus_rsp_allowExecute = 1'b1;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_0_requireMmuLockup) begin
         IBusCachedPlugin_mmuBus_rsp_exception = (((! MmuPlugin_ports_0_dirty) && MmuPlugin_ports_0_cacheHit) && ((MmuPlugin_ports_0_cacheLine_exception || ((MmuPlugin_ports_0_cacheLine_allowUser && (CsrPlugin_privilege == 2'b01)) && (! MmuPlugin_status_sum))) || ((! MmuPlugin_ports_0_cacheLine_allowUser) && (CsrPlugin_privilege == 2'b00))));
      end else begin
         IBusCachedPlugin_mmuBus_rsp_exception = 1'b0;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_0_requireMmuLockup) begin
         IBusCachedPlugin_mmuBus_rsp_refilling = (MmuPlugin_ports_0_dirty || (! MmuPlugin_ports_0_cacheHit));
      end else begin
         IBusCachedPlugin_mmuBus_rsp_refilling = 1'b0;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_0_requireMmuLockup) begin
         IBusCachedPlugin_mmuBus_rsp_isPaging = 1'b1;
      end else begin
         IBusCachedPlugin_mmuBus_rsp_isPaging = 1'b0;
      end
   end

   assign IBusCachedPlugin_mmuBus_rsp_isIoAccess = ((ioStartAddr <= IBusCachedPlugin_mmuBus_rsp_physicalAddress) && (IBusCachedPlugin_mmuBus_rsp_physicalAddress <= MmuPlugin_ioEndAddr));
   assign IBusCachedPlugin_mmuBus_rsp_bypassTranslation = (!MmuPlugin_ports_0_requireMmuLockup);
   assign IBusCachedPlugin_mmuBus_rsp_ways_0_sel = MmuPlugin_ports_0_cacheHits[0];
   assign IBusCachedPlugin_mmuBus_rsp_ways_0_physical = {
      {
         MmuPlugin_ports_0_cache_0_physicalAddress_1,
         (MmuPlugin_ports_0_cache_0_superPage ? IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_0_cache_0_physicalAddress_0)
      },
      IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign IBusCachedPlugin_mmuBus_rsp_ways_1_sel = MmuPlugin_ports_0_cacheHits[1];
   assign IBusCachedPlugin_mmuBus_rsp_ways_1_physical = {
      {
         MmuPlugin_ports_0_cache_1_physicalAddress_1,
         (MmuPlugin_ports_0_cache_1_superPage ? IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_0_cache_1_physicalAddress_0)
      },
      IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign IBusCachedPlugin_mmuBus_rsp_ways_2_sel = MmuPlugin_ports_0_cacheHits[2];
   assign IBusCachedPlugin_mmuBus_rsp_ways_2_physical = {
      {
         MmuPlugin_ports_0_cache_2_physicalAddress_1,
         (MmuPlugin_ports_0_cache_2_superPage ? IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_0_cache_2_physicalAddress_0)
      },
      IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign IBusCachedPlugin_mmuBus_rsp_ways_3_sel = MmuPlugin_ports_0_cacheHits[3];
   assign IBusCachedPlugin_mmuBus_rsp_ways_3_physical = {
      {
         MmuPlugin_ports_0_cache_3_physicalAddress_1,
         (MmuPlugin_ports_0_cache_3_superPage ? IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_0_cache_3_physicalAddress_0)
      },
      IBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign when_MmuPlugin_l129_1 = (!DBusCachedPlugin_mmuBus_cmd_1_isStuck);
   always @(*) begin
      MmuPlugin_ports_1_requireMmuLockupCalc = ((1'b1 && (! DBusCachedPlugin_mmuBus_cmd_0_bypassTranslation)) && MmuPlugin_satp_mode);
      if (when_MmuPlugin_l143_1) begin
         MmuPlugin_ports_1_requireMmuLockupCalc = 1'b0;
      end
      if (when_MmuPlugin_l144_1) begin
         if (when_MmuPlugin_l146) begin
            MmuPlugin_ports_1_requireMmuLockupCalc = 1'b0;
         end
      end
   end

   assign when_MmuPlugin_l143_1 = ((!MmuPlugin_status_mprv) && (CsrPlugin_privilege == 2'b11));
   assign when_MmuPlugin_l144_1 = (CsrPlugin_privilege == 2'b11);
   assign when_MmuPlugin_l146 = ((!MmuPlugin_status_mprv) || (CsrPlugin_mstatus_MPP == 2'b11));
   assign MmuPlugin_ports_1_cacheHitsCalc = {
      ((MmuPlugin_ports_1_cache_3_valid && (MmuPlugin_ports_1_cache_3_virtualAddress_1 == DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[31 : 22])) && (MmuPlugin_ports_1_cache_3_superPage || (MmuPlugin_ports_1_cache_3_virtualAddress_0 == DBusCachedPlugin_mmuBus_cmd_0_virtualAddress[21 : 12]))),
      {
         ((MmuPlugin_ports_1_cache_2_valid && (MmuPlugin_ports_1_cache_2_virtualAddress_1 == _zz_MmuPlugin_ports_1_cacheHitsCalc)) && (MmuPlugin_ports_1_cache_2_superPage || (MmuPlugin_ports_1_cache_2_virtualAddress_0 == _zz_MmuPlugin_ports_1_cacheHitsCalc_1))),
         {
            ((MmuPlugin_ports_1_cache_1_valid && _zz_MmuPlugin_ports_1_cacheHitsCalc_2) && (MmuPlugin_ports_1_cache_1_superPage || _zz_MmuPlugin_ports_1_cacheHitsCalc_3)),
            ((MmuPlugin_ports_1_cache_0_valid && _zz_MmuPlugin_ports_1_cacheHitsCalc_4) && (MmuPlugin_ports_1_cache_0_superPage || _zz_MmuPlugin_ports_1_cacheHitsCalc_5))
         }
      }
   };
   assign when_MmuPlugin_l136_2 = (!DBusCachedPlugin_mmuBus_cmd_1_isStuck);
   assign when_MmuPlugin_l136_3 = (!DBusCachedPlugin_mmuBus_cmd_1_isStuck);
   assign MmuPlugin_ports_1_cacheHit = (|MmuPlugin_ports_1_cacheHits);
   assign _zz_MmuPlugin_ports_1_cacheLine_valid = MmuPlugin_ports_1_cacheHits[3];
   assign _zz_MmuPlugin_ports_1_cacheLine_valid_1 = (MmuPlugin_ports_1_cacheHits[1] || _zz_MmuPlugin_ports_1_cacheLine_valid);
   assign _zz_MmuPlugin_ports_1_cacheLine_valid_2 = (MmuPlugin_ports_1_cacheHits[2] || _zz_MmuPlugin_ports_1_cacheLine_valid);
   assign _zz_MmuPlugin_ports_1_cacheLine_valid_3 = {
      _zz_MmuPlugin_ports_1_cacheLine_valid_2, _zz_MmuPlugin_ports_1_cacheLine_valid_1
   };
   assign MmuPlugin_ports_1_cacheLine_valid = _zz_MmuPlugin_ports_1_cacheLine_valid_4;
   assign MmuPlugin_ports_1_cacheLine_exception = _zz_MmuPlugin_ports_1_cacheLine_exception;
   assign MmuPlugin_ports_1_cacheLine_superPage = _zz_MmuPlugin_ports_1_cacheLine_superPage;
   assign MmuPlugin_ports_1_cacheLine_virtualAddress_0 = _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_0;
   assign MmuPlugin_ports_1_cacheLine_virtualAddress_1 = _zz_MmuPlugin_ports_1_cacheLine_virtualAddress_1;
   assign MmuPlugin_ports_1_cacheLine_physicalAddress_0 = _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_0;
   assign MmuPlugin_ports_1_cacheLine_physicalAddress_1 = _zz_MmuPlugin_ports_1_cacheLine_physicalAddress_1;
   assign MmuPlugin_ports_1_cacheLine_allowRead = _zz_MmuPlugin_ports_1_cacheLine_allowRead;
   assign MmuPlugin_ports_1_cacheLine_allowWrite = _zz_MmuPlugin_ports_1_cacheLine_allowWrite;
   assign MmuPlugin_ports_1_cacheLine_allowExecute = _zz_MmuPlugin_ports_1_cacheLine_allowExecute;
   assign MmuPlugin_ports_1_cacheLine_allowUser = _zz_MmuPlugin_ports_1_cacheLine_allowUser;
   always @(*) begin
      MmuPlugin_ports_1_entryToReplace_willIncrement = 1'b0;
      if (when_MmuPlugin_l302) begin
         if (when_MmuPlugin_l304_1) begin
            MmuPlugin_ports_1_entryToReplace_willIncrement = 1'b1;
         end
      end
   end

   assign MmuPlugin_ports_1_entryToReplace_willClear = 1'b0;
   assign MmuPlugin_ports_1_entryToReplace_willOverflowIfInc = (MmuPlugin_ports_1_entryToReplace_value == 2'b11);
   assign MmuPlugin_ports_1_entryToReplace_willOverflow = (MmuPlugin_ports_1_entryToReplace_willOverflowIfInc && MmuPlugin_ports_1_entryToReplace_willIncrement);
   always @(*) begin
      MmuPlugin_ports_1_entryToReplace_valueNext = (MmuPlugin_ports_1_entryToReplace_value + _zz_MmuPlugin_ports_1_entryToReplace_valueNext);
      if (MmuPlugin_ports_1_entryToReplace_willClear) begin
         MmuPlugin_ports_1_entryToReplace_valueNext = 2'b00;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_1_requireMmuLockup) begin
         DBusCachedPlugin_mmuBus_rsp_physicalAddress = {
            {
               MmuPlugin_ports_1_cacheLine_physicalAddress_1,
               (MmuPlugin_ports_1_cacheLine_superPage ? DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_1_cacheLine_physicalAddress_0)
            },
            DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
         };
      end else begin
         DBusCachedPlugin_mmuBus_rsp_physicalAddress = DBusCachedPlugin_mmuBus_cmd_1_virtualAddress;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_1_requireMmuLockup) begin
         DBusCachedPlugin_mmuBus_rsp_allowRead = (MmuPlugin_ports_1_cacheLine_allowRead || (MmuPlugin_status_mxr && MmuPlugin_ports_1_cacheLine_allowExecute));
      end else begin
         DBusCachedPlugin_mmuBus_rsp_allowRead = 1'b1;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_1_requireMmuLockup) begin
         DBusCachedPlugin_mmuBus_rsp_allowWrite = MmuPlugin_ports_1_cacheLine_allowWrite;
      end else begin
         DBusCachedPlugin_mmuBus_rsp_allowWrite = 1'b1;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_1_requireMmuLockup) begin
         DBusCachedPlugin_mmuBus_rsp_allowExecute = MmuPlugin_ports_1_cacheLine_allowExecute;
      end else begin
         DBusCachedPlugin_mmuBus_rsp_allowExecute = 1'b1;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_1_requireMmuLockup) begin
         DBusCachedPlugin_mmuBus_rsp_exception = (((! MmuPlugin_ports_1_dirty) && MmuPlugin_ports_1_cacheHit) && ((MmuPlugin_ports_1_cacheLine_exception || ((MmuPlugin_ports_1_cacheLine_allowUser && (CsrPlugin_privilege == 2'b01)) && (! MmuPlugin_status_sum))) || ((! MmuPlugin_ports_1_cacheLine_allowUser) && (CsrPlugin_privilege == 2'b00))));
      end else begin
         DBusCachedPlugin_mmuBus_rsp_exception = 1'b0;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_1_requireMmuLockup) begin
         DBusCachedPlugin_mmuBus_rsp_refilling = (MmuPlugin_ports_1_dirty || (! MmuPlugin_ports_1_cacheHit));
      end else begin
         DBusCachedPlugin_mmuBus_rsp_refilling = 1'b0;
      end
   end

   always @(*) begin
      if (MmuPlugin_ports_1_requireMmuLockup) begin
         DBusCachedPlugin_mmuBus_rsp_isPaging = 1'b1;
      end else begin
         DBusCachedPlugin_mmuBus_rsp_isPaging = 1'b0;
      end
   end

   assign DBusCachedPlugin_mmuBus_rsp_isIoAccess = ((ioStartAddr <= DBusCachedPlugin_mmuBus_rsp_physicalAddress) && (DBusCachedPlugin_mmuBus_rsp_physicalAddress <= MmuPlugin_ioEndAddr));
   assign DBusCachedPlugin_mmuBus_rsp_bypassTranslation = (!MmuPlugin_ports_1_requireMmuLockup);
   assign DBusCachedPlugin_mmuBus_rsp_ways_0_sel = MmuPlugin_ports_1_cacheHits[0];
   assign DBusCachedPlugin_mmuBus_rsp_ways_0_physical = {
      {
         MmuPlugin_ports_1_cache_0_physicalAddress_1,
         (MmuPlugin_ports_1_cache_0_superPage ? DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_1_cache_0_physicalAddress_0)
      },
      DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign DBusCachedPlugin_mmuBus_rsp_ways_1_sel = MmuPlugin_ports_1_cacheHits[1];
   assign DBusCachedPlugin_mmuBus_rsp_ways_1_physical = {
      {
         MmuPlugin_ports_1_cache_1_physicalAddress_1,
         (MmuPlugin_ports_1_cache_1_superPage ? DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_1_cache_1_physicalAddress_0)
      },
      DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign DBusCachedPlugin_mmuBus_rsp_ways_2_sel = MmuPlugin_ports_1_cacheHits[2];
   assign DBusCachedPlugin_mmuBus_rsp_ways_2_physical = {
      {
         MmuPlugin_ports_1_cache_2_physicalAddress_1,
         (MmuPlugin_ports_1_cache_2_superPage ? DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_1_cache_2_physicalAddress_0)
      },
      DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign DBusCachedPlugin_mmuBus_rsp_ways_3_sel = MmuPlugin_ports_1_cacheHits[3];
   assign DBusCachedPlugin_mmuBus_rsp_ways_3_physical = {
      {
         MmuPlugin_ports_1_cache_3_physicalAddress_1,
         (MmuPlugin_ports_1_cache_3_superPage ? DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[21 : 12] : MmuPlugin_ports_1_cache_3_physicalAddress_0)
      },
      DBusCachedPlugin_mmuBus_cmd_1_virtualAddress[11 : 0]
   };
   assign MmuPlugin_shared_dBusRsp_pte_V = MmuPlugin_shared_dBusRspStaged_payload_data[0];
   assign MmuPlugin_shared_dBusRsp_pte_R = MmuPlugin_shared_dBusRspStaged_payload_data[1];
   assign MmuPlugin_shared_dBusRsp_pte_W = MmuPlugin_shared_dBusRspStaged_payload_data[2];
   assign MmuPlugin_shared_dBusRsp_pte_X = MmuPlugin_shared_dBusRspStaged_payload_data[3];
   assign MmuPlugin_shared_dBusRsp_pte_U = MmuPlugin_shared_dBusRspStaged_payload_data[4];
   assign MmuPlugin_shared_dBusRsp_pte_G = MmuPlugin_shared_dBusRspStaged_payload_data[5];
   assign MmuPlugin_shared_dBusRsp_pte_A = MmuPlugin_shared_dBusRspStaged_payload_data[6];
   assign MmuPlugin_shared_dBusRsp_pte_D = MmuPlugin_shared_dBusRspStaged_payload_data[7];
   assign MmuPlugin_shared_dBusRsp_pte_RSW = MmuPlugin_shared_dBusRspStaged_payload_data[9 : 8];
   assign MmuPlugin_shared_dBusRsp_pte_PPN0 = MmuPlugin_shared_dBusRspStaged_payload_data[19 : 10];
   assign MmuPlugin_shared_dBusRsp_pte_PPN1 = MmuPlugin_shared_dBusRspStaged_payload_data[31 : 20];
   assign MmuPlugin_shared_dBusRsp_exception = (((! MmuPlugin_shared_dBusRsp_pte_V) || ((! MmuPlugin_shared_dBusRsp_pte_R) && MmuPlugin_shared_dBusRsp_pte_W)) || MmuPlugin_shared_dBusRspStaged_payload_error);
   assign MmuPlugin_shared_dBusRsp_leaf = (MmuPlugin_shared_dBusRsp_pte_R || MmuPlugin_shared_dBusRsp_pte_X);
   assign when_MmuPlugin_l234 = (MmuPlugin_shared_dBusRspStaged_valid && (! MmuPlugin_shared_dBusRspStaged_payload_redo));
   always @(*) begin
      MmuPlugin_dBusAccess_cmd_valid = 1'b0;
      case (MmuPlugin_shared_state_1)
         MmuPlugin_shared_State_IDLE: begin
         end
         MmuPlugin_shared_State_L1_CMD: begin
            MmuPlugin_dBusAccess_cmd_valid = 1'b1;
         end
         MmuPlugin_shared_State_L1_RSP: begin
         end
         MmuPlugin_shared_State_L0_CMD: begin
            MmuPlugin_dBusAccess_cmd_valid = 1'b1;
         end
         default: begin
         end
      endcase
   end

   assign MmuPlugin_dBusAccess_cmd_payload_write = 1'b0;
   assign MmuPlugin_dBusAccess_cmd_payload_size  = 2'b10;
   always @(*) begin
      MmuPlugin_dBusAccess_cmd_payload_address = 32'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
      case (MmuPlugin_shared_state_1)
         MmuPlugin_shared_State_IDLE: begin
         end
         MmuPlugin_shared_State_L1_CMD: begin
            MmuPlugin_dBusAccess_cmd_payload_address = {
               {MmuPlugin_satp_ppn[19 : 0], MmuPlugin_shared_vpn_1}, 2'b00
            };
         end
         MmuPlugin_shared_State_L1_RSP: begin
         end
         MmuPlugin_shared_State_L0_CMD: begin
            MmuPlugin_dBusAccess_cmd_payload_address = {
               {
                  {MmuPlugin_shared_pteBuffer_PPN1[9 : 0], MmuPlugin_shared_pteBuffer_PPN0},
                  MmuPlugin_shared_vpn_0
               },
               2'b00
            };
         end
         default: begin
         end
      endcase
   end

   assign MmuPlugin_dBusAccess_cmd_payload_data = 32'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
   assign MmuPlugin_dBusAccess_cmd_payload_writeMask = 4'bxxxx;
   assign _zz_MmuPlugin_shared_refills = {
      (((DBusCachedPlugin_mmuBus_cmd_1_isValid && MmuPlugin_ports_1_requireMmuLockup) && (! MmuPlugin_ports_1_dirty)) && (! MmuPlugin_ports_1_cacheHit)),
      (((IBusCachedPlugin_mmuBus_cmd_1_isValid && MmuPlugin_ports_0_requireMmuLockup) && (! MmuPlugin_ports_0_dirty)) && (! MmuPlugin_ports_0_cacheHit))
   };
   always @(*) begin
      _zz_MmuPlugin_shared_refills_1[0] = _zz_MmuPlugin_shared_refills[1];
      _zz_MmuPlugin_shared_refills_1[1] = _zz_MmuPlugin_shared_refills[0];
   end

   assign _zz_MmuPlugin_shared_refills_2 = (_zz_MmuPlugin_shared_refills_1 & (~ _zz__zz_MmuPlugin_shared_refills_2));
   always @(*) begin
      _zz_MmuPlugin_shared_refills_3[0] = _zz_MmuPlugin_shared_refills_2[1];
      _zz_MmuPlugin_shared_refills_3[1] = _zz_MmuPlugin_shared_refills_2[0];
   end

   assign MmuPlugin_shared_refills = _zz_MmuPlugin_shared_refills_3;
   assign when_MmuPlugin_l246 = (|MmuPlugin_shared_refills);
   assign _zz_MmuPlugin_shared_vpn_0 = (MmuPlugin_shared_refills[0] ? IBusCachedPlugin_mmuBus_cmd_1_virtualAddress : DBusCachedPlugin_mmuBus_cmd_1_virtualAddress);
   assign when_MmuPlugin_l273 = (MmuPlugin_shared_dBusRsp_leaf || MmuPlugin_shared_dBusRsp_exception);
   assign IBusCachedPlugin_mmuBus_busy = ((MmuPlugin_shared_state_1 != MmuPlugin_shared_State_IDLE) && MmuPlugin_shared_portSortedOh[0]);
   assign DBusCachedPlugin_mmuBus_busy = ((MmuPlugin_shared_state_1 != MmuPlugin_shared_State_IDLE) && MmuPlugin_shared_portSortedOh[1]);
   assign when_MmuPlugin_l302 = ((MmuPlugin_shared_dBusRspStaged_valid && (! MmuPlugin_shared_dBusRspStaged_payload_redo)) && (MmuPlugin_shared_dBusRsp_leaf || MmuPlugin_shared_dBusRsp_exception));
   assign when_MmuPlugin_l304 = MmuPlugin_shared_portSortedOh[0];
   assign when_MmuPlugin_l310 = (MmuPlugin_ports_0_entryToReplace_value == 2'b00);
   assign when_MmuPlugin_l310_1 = (MmuPlugin_ports_0_entryToReplace_value == 2'b01);
   assign when_MmuPlugin_l310_2 = (MmuPlugin_ports_0_entryToReplace_value == 2'b10);
   assign when_MmuPlugin_l310_3 = (MmuPlugin_ports_0_entryToReplace_value == 2'b11);
   assign when_MmuPlugin_l304_1 = MmuPlugin_shared_portSortedOh[1];
   assign when_MmuPlugin_l310_4 = (MmuPlugin_ports_1_entryToReplace_value == 2'b00);
   assign when_MmuPlugin_l310_5 = (MmuPlugin_ports_1_entryToReplace_value == 2'b01);
   assign when_MmuPlugin_l310_6 = (MmuPlugin_ports_1_entryToReplace_value == 2'b10);
   assign when_MmuPlugin_l310_7 = (MmuPlugin_ports_1_entryToReplace_value == 2'b11);
   assign when_MmuPlugin_l334 = ((execute_arbitration_isValid && execute_arbitration_isFiring) && execute_IS_SFENCE_VMA2);
   assign _zz_decode_IS_CSR_1 = ((decode_INSTRUCTION & 32'h00005048) == 32'h00001008);
   assign _zz_decode_IS_CSR_2 = ((decode_INSTRUCTION & 32'h02003050) == 32'h02000050);
   assign _zz_decode_IS_CSR_3 = ((decode_INSTRUCTION & 32'h00004050) == 32'h00004050);
   assign _zz_decode_IS_CSR_4 = ((decode_INSTRUCTION & 32'h00000048) == 32'h00000048);
   assign _zz_decode_IS_CSR_5 = ((decode_INSTRUCTION & 32'h00002050) == 32'h00002000);
   assign _zz_decode_IS_CSR_6 = ((decode_INSTRUCTION & 32'h00000018) == 32'h00000000);
   assign _zz_decode_IS_CSR_7 = ((decode_INSTRUCTION & 32'h00000004) == 32'h00000004);
   assign _zz_decode_IS_CSR_8 = ((decode_INSTRUCTION & 32'h0000000c) == 32'h00000004);
   assign _zz_decode_IS_CSR_9 = ((decode_INSTRUCTION & 32'h00002010) == 32'h00002000);
   assign _zz_decode_IS_CSR_10 = ((decode_INSTRUCTION & 32'h00001000) == 32'h00000000);
   assign _zz_decode_IS_CSR = {
      (|((decode_INSTRUCTION & 32'h10103050) == 32'h00100050)),
      {
         (|{(_zz__zz_decode_IS_CSR == _zz__zz_decode_IS_CSR_1),(_zz__zz_decode_IS_CSR_2 == _zz__zz_decode_IS_CSR_3)}),
         {
            (|(_zz__zz_decode_IS_CSR_4 == _zz__zz_decode_IS_CSR_5)),
            {
               (|{_zz__zz_decode_IS_CSR_6, _zz__zz_decode_IS_CSR_8}),
               {
                  (|_zz__zz_decode_IS_CSR_10),
                  {_zz__zz_decode_IS_CSR_13, {_zz__zz_decode_IS_CSR_16, _zz__zz_decode_IS_CSR_17}}
               }
            }
         }
      }
   };
   assign _zz_decode_SRC1_CTRL_2 = _zz_decode_IS_CSR[3 : 2];
   assign _zz_decode_SRC1_CTRL_1 = _zz_decode_SRC1_CTRL_2;
   assign _zz_decode_ALU_CTRL_2 = _zz_decode_IS_CSR[8 : 7];
   assign _zz_decode_ALU_CTRL_1 = _zz_decode_ALU_CTRL_2;
   assign _zz_decode_SRC2_CTRL_2 = _zz_decode_IS_CSR[10 : 9];
   assign _zz_decode_SRC2_CTRL_1 = _zz_decode_SRC2_CTRL_2;
   assign _zz_decode_ALU_BITWISE_CTRL_2 = _zz_decode_IS_CSR[24 : 23];
   assign _zz_decode_ALU_BITWISE_CTRL_1 = _zz_decode_ALU_BITWISE_CTRL_2;
   assign _zz_decode_SHIFT_CTRL_2 = _zz_decode_IS_CSR[26 : 25];
   assign _zz_decode_SHIFT_CTRL_1 = _zz_decode_SHIFT_CTRL_2;
   assign _zz_decode_BRANCH_CTRL_2 = _zz_decode_IS_CSR[32 : 31];
   assign _zz_decode_BRANCH_CTRL_1 = _zz_decode_BRANCH_CTRL_2;
   assign _zz_decode_ENV_CTRL_2 = _zz_decode_IS_CSR[36 : 34];
   assign _zz_decode_ENV_CTRL_1 = _zz_decode_ENV_CTRL_2;
   assign decodeExceptionPort_valid = (decode_arbitration_isValid && (!decode_LEGAL_INSTRUCTION));
   assign decodeExceptionPort_payload_code = 4'b0010;
   assign decodeExceptionPort_payload_badAddr = decode_INSTRUCTION;
   assign when_RegFilePlugin_l63 = (decode_INSTRUCTION[11 : 7] == 5'h00);
   assign decode_RegFilePlugin_regFileReadAddress1 = decode_INSTRUCTION_ANTICIPATED[19 : 15];
   assign decode_RegFilePlugin_regFileReadAddress2 = decode_INSTRUCTION_ANTICIPATED[24 : 20];
   assign decode_RegFilePlugin_rs1Data = _zz_RegFilePlugin_regFile_port0;
   assign decode_RegFilePlugin_rs2Data = _zz_RegFilePlugin_regFile_port1;
   always @(*) begin
      lastStageRegFileWrite_valid = (_zz_lastStageRegFileWrite_valid && writeBack_arbitration_isFiring);
      if (_zz_5) begin
         lastStageRegFileWrite_valid = 1'b1;
      end
   end

   always @(*) begin
      lastStageRegFileWrite_payload_address = _zz_lastStageRegFileWrite_payload_address[11 : 7];
      if (_zz_5) begin
         lastStageRegFileWrite_payload_address = 5'h00;
      end
   end

   always @(*) begin
      lastStageRegFileWrite_payload_data = _zz_decode_RS2_2;
      if (_zz_5) begin
         lastStageRegFileWrite_payload_data = 32'h00000000;
      end
   end

   always @(*) begin
      case (execute_ALU_BITWISE_CTRL)
         AluBitwiseCtrlEnum_AND_1: begin
            execute_IntAluPlugin_bitwise = (execute_SRC1 & execute_SRC2);
         end
         AluBitwiseCtrlEnum_OR_1: begin
            execute_IntAluPlugin_bitwise = (execute_SRC1 | execute_SRC2);
         end
         default: begin
            execute_IntAluPlugin_bitwise = (execute_SRC1 ^ execute_SRC2);
         end
      endcase
   end

   always @(*) begin
      case (execute_ALU_CTRL)
         AluCtrlEnum_BITWISE: begin
            _zz_execute_REGFILE_WRITE_DATA = execute_IntAluPlugin_bitwise;
         end
         AluCtrlEnum_SLT_SLTU: begin
            _zz_execute_REGFILE_WRITE_DATA = {31'd0, _zz__zz_execute_REGFILE_WRITE_DATA};
         end
         default: begin
            _zz_execute_REGFILE_WRITE_DATA = execute_SRC_ADD_SUB;
         end
      endcase
   end

   always @(*) begin
      case (execute_SRC1_CTRL)
         Src1CtrlEnum_RS: begin
            _zz_execute_SRC1 = execute_RS1;
         end
         Src1CtrlEnum_PC_INCREMENT: begin
            _zz_execute_SRC1 = {29'd0, _zz__zz_execute_SRC1};
         end
         Src1CtrlEnum_IMU: begin
            _zz_execute_SRC1 = {execute_INSTRUCTION[31 : 12], 12'h000};
         end
         default: begin
            _zz_execute_SRC1 = {27'd0, _zz__zz_execute_SRC1_1};
         end
      endcase
   end

   assign _zz_execute_SRC2 = execute_INSTRUCTION[31];
   always @(*) begin
      _zz_execute_SRC2_1[19] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[18] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[17] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[16] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[15] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[14] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[13] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[12] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[11] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[10] = _zz_execute_SRC2;
      _zz_execute_SRC2_1[9]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[8]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[7]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[6]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[5]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[4]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[3]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[2]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[1]  = _zz_execute_SRC2;
      _zz_execute_SRC2_1[0]  = _zz_execute_SRC2;
   end

   assign _zz_execute_SRC2_2 = _zz__zz_execute_SRC2_2[11];
   always @(*) begin
      _zz_execute_SRC2_3[19] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[18] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[17] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[16] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[15] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[14] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[13] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[12] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[11] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[10] = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[9]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[8]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[7]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[6]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[5]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[4]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[3]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[2]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[1]  = _zz_execute_SRC2_2;
      _zz_execute_SRC2_3[0]  = _zz_execute_SRC2_2;
   end

   always @(*) begin
      case (execute_SRC2_CTRL)
         Src2CtrlEnum_RS: begin
            _zz_execute_SRC2_4 = execute_RS2;
         end
         Src2CtrlEnum_IMI: begin
            _zz_execute_SRC2_4 = {_zz_execute_SRC2_1, execute_INSTRUCTION[31 : 20]};
         end
         Src2CtrlEnum_IMS: begin
            _zz_execute_SRC2_4 = {
               _zz_execute_SRC2_3, {execute_INSTRUCTION[31 : 25], execute_INSTRUCTION[11 : 7]}
            };
         end
         default: begin
            _zz_execute_SRC2_4 = _zz_execute_to_memory_PC;
         end
      endcase
   end

   always @(*) begin
      execute_SrcPlugin_addSub = _zz_execute_SrcPlugin_addSub;
      if (execute_SRC2_FORCE_ZERO) begin
         execute_SrcPlugin_addSub = execute_SRC1;
      end
   end

   assign execute_SrcPlugin_less = ((execute_SRC1[31] == execute_SRC2[31]) ? execute_SrcPlugin_addSub[31] : (execute_SRC_LESS_UNSIGNED ? execute_SRC2[31] : execute_SRC1[31]));
   assign execute_FullBarrelShifterPlugin_amplitude = execute_SRC2[4 : 0];
   always @(*) begin
      _zz_execute_FullBarrelShifterPlugin_reversed[0]  = execute_SRC1[31];
      _zz_execute_FullBarrelShifterPlugin_reversed[1]  = execute_SRC1[30];
      _zz_execute_FullBarrelShifterPlugin_reversed[2]  = execute_SRC1[29];
      _zz_execute_FullBarrelShifterPlugin_reversed[3]  = execute_SRC1[28];
      _zz_execute_FullBarrelShifterPlugin_reversed[4]  = execute_SRC1[27];
      _zz_execute_FullBarrelShifterPlugin_reversed[5]  = execute_SRC1[26];
      _zz_execute_FullBarrelShifterPlugin_reversed[6]  = execute_SRC1[25];
      _zz_execute_FullBarrelShifterPlugin_reversed[7]  = execute_SRC1[24];
      _zz_execute_FullBarrelShifterPlugin_reversed[8]  = execute_SRC1[23];
      _zz_execute_FullBarrelShifterPlugin_reversed[9]  = execute_SRC1[22];
      _zz_execute_FullBarrelShifterPlugin_reversed[10] = execute_SRC1[21];
      _zz_execute_FullBarrelShifterPlugin_reversed[11] = execute_SRC1[20];
      _zz_execute_FullBarrelShifterPlugin_reversed[12] = execute_SRC1[19];
      _zz_execute_FullBarrelShifterPlugin_reversed[13] = execute_SRC1[18];
      _zz_execute_FullBarrelShifterPlugin_reversed[14] = execute_SRC1[17];
      _zz_execute_FullBarrelShifterPlugin_reversed[15] = execute_SRC1[16];
      _zz_execute_FullBarrelShifterPlugin_reversed[16] = execute_SRC1[15];
      _zz_execute_FullBarrelShifterPlugin_reversed[17] = execute_SRC1[14];
      _zz_execute_FullBarrelShifterPlugin_reversed[18] = execute_SRC1[13];
      _zz_execute_FullBarrelShifterPlugin_reversed[19] = execute_SRC1[12];
      _zz_execute_FullBarrelShifterPlugin_reversed[20] = execute_SRC1[11];
      _zz_execute_FullBarrelShifterPlugin_reversed[21] = execute_SRC1[10];
      _zz_execute_FullBarrelShifterPlugin_reversed[22] = execute_SRC1[9];
      _zz_execute_FullBarrelShifterPlugin_reversed[23] = execute_SRC1[8];
      _zz_execute_FullBarrelShifterPlugin_reversed[24] = execute_SRC1[7];
      _zz_execute_FullBarrelShifterPlugin_reversed[25] = execute_SRC1[6];
      _zz_execute_FullBarrelShifterPlugin_reversed[26] = execute_SRC1[5];
      _zz_execute_FullBarrelShifterPlugin_reversed[27] = execute_SRC1[4];
      _zz_execute_FullBarrelShifterPlugin_reversed[28] = execute_SRC1[3];
      _zz_execute_FullBarrelShifterPlugin_reversed[29] = execute_SRC1[2];
      _zz_execute_FullBarrelShifterPlugin_reversed[30] = execute_SRC1[1];
      _zz_execute_FullBarrelShifterPlugin_reversed[31] = execute_SRC1[0];
   end

   assign execute_FullBarrelShifterPlugin_reversed = ((execute_SHIFT_CTRL == ShiftCtrlEnum_SLL_1) ? _zz_execute_FullBarrelShifterPlugin_reversed : execute_SRC1);
   always @(*) begin
      _zz_decode_RS2_3[0]  = memory_SHIFT_RIGHT[31];
      _zz_decode_RS2_3[1]  = memory_SHIFT_RIGHT[30];
      _zz_decode_RS2_3[2]  = memory_SHIFT_RIGHT[29];
      _zz_decode_RS2_3[3]  = memory_SHIFT_RIGHT[28];
      _zz_decode_RS2_3[4]  = memory_SHIFT_RIGHT[27];
      _zz_decode_RS2_3[5]  = memory_SHIFT_RIGHT[26];
      _zz_decode_RS2_3[6]  = memory_SHIFT_RIGHT[25];
      _zz_decode_RS2_3[7]  = memory_SHIFT_RIGHT[24];
      _zz_decode_RS2_3[8]  = memory_SHIFT_RIGHT[23];
      _zz_decode_RS2_3[9]  = memory_SHIFT_RIGHT[22];
      _zz_decode_RS2_3[10] = memory_SHIFT_RIGHT[21];
      _zz_decode_RS2_3[11] = memory_SHIFT_RIGHT[20];
      _zz_decode_RS2_3[12] = memory_SHIFT_RIGHT[19];
      _zz_decode_RS2_3[13] = memory_SHIFT_RIGHT[18];
      _zz_decode_RS2_3[14] = memory_SHIFT_RIGHT[17];
      _zz_decode_RS2_3[15] = memory_SHIFT_RIGHT[16];
      _zz_decode_RS2_3[16] = memory_SHIFT_RIGHT[15];
      _zz_decode_RS2_3[17] = memory_SHIFT_RIGHT[14];
      _zz_decode_RS2_3[18] = memory_SHIFT_RIGHT[13];
      _zz_decode_RS2_3[19] = memory_SHIFT_RIGHT[12];
      _zz_decode_RS2_3[20] = memory_SHIFT_RIGHT[11];
      _zz_decode_RS2_3[21] = memory_SHIFT_RIGHT[10];
      _zz_decode_RS2_3[22] = memory_SHIFT_RIGHT[9];
      _zz_decode_RS2_3[23] = memory_SHIFT_RIGHT[8];
      _zz_decode_RS2_3[24] = memory_SHIFT_RIGHT[7];
      _zz_decode_RS2_3[25] = memory_SHIFT_RIGHT[6];
      _zz_decode_RS2_3[26] = memory_SHIFT_RIGHT[5];
      _zz_decode_RS2_3[27] = memory_SHIFT_RIGHT[4];
      _zz_decode_RS2_3[28] = memory_SHIFT_RIGHT[3];
      _zz_decode_RS2_3[29] = memory_SHIFT_RIGHT[2];
      _zz_decode_RS2_3[30] = memory_SHIFT_RIGHT[1];
      _zz_decode_RS2_3[31] = memory_SHIFT_RIGHT[0];
   end

   assign execute_MulPlugin_a  = execute_RS1;
   assign execute_MulPlugin_b  = execute_RS2;
   assign switch_MulPlugin_l87 = execute_INSTRUCTION[13 : 12];
   always @(*) begin
      case (switch_MulPlugin_l87)
         2'b01: begin
            execute_MulPlugin_aSigned = 1'b1;
         end
         2'b10: begin
            execute_MulPlugin_aSigned = 1'b1;
         end
         default: begin
            execute_MulPlugin_aSigned = 1'b0;
         end
      endcase
   end

   always @(*) begin
      case (switch_MulPlugin_l87)
         2'b01: begin
            execute_MulPlugin_bSigned = 1'b1;
         end
         2'b10: begin
            execute_MulPlugin_bSigned = 1'b0;
         end
         default: begin
            execute_MulPlugin_bSigned = 1'b0;
         end
      endcase
   end

   assign execute_MulPlugin_aULow = execute_MulPlugin_a[15 : 0];
   assign execute_MulPlugin_bULow = execute_MulPlugin_b[15 : 0];
   assign execute_MulPlugin_aSLow = {1'b0, execute_MulPlugin_a[15 : 0]};
   assign execute_MulPlugin_bSLow = {1'b0, execute_MulPlugin_b[15 : 0]};
   assign execute_MulPlugin_aHigh = {
      (execute_MulPlugin_aSigned && execute_MulPlugin_a[31]), execute_MulPlugin_a[31 : 16]
   };
   assign execute_MulPlugin_bHigh = {
      (execute_MulPlugin_bSigned && execute_MulPlugin_b[31]), execute_MulPlugin_b[31 : 16]
   };
   assign writeBack_MulPlugin_result = ($signed(
       _zz_writeBack_MulPlugin_result
   ) + $signed(
       _zz_writeBack_MulPlugin_result_1
   ));
   assign when_MulPlugin_l147 = (writeBack_arbitration_isValid && writeBack_IS_MUL);
   assign switch_MulPlugin_l148 = writeBack_INSTRUCTION[13 : 12];
   assign memory_DivPlugin_frontendOk = 1'b1;
   always @(*) begin
      memory_DivPlugin_div_counter_willIncrement = 1'b0;
      if (when_MulDivIterativePlugin_l128) begin
         if (when_MulDivIterativePlugin_l132) begin
            memory_DivPlugin_div_counter_willIncrement = 1'b1;
         end
      end
   end

   always @(*) begin
      memory_DivPlugin_div_counter_willClear = 1'b0;
      if (when_MulDivIterativePlugin_l162) begin
         memory_DivPlugin_div_counter_willClear = 1'b1;
      end
   end

   assign memory_DivPlugin_div_counter_willOverflowIfInc = (memory_DivPlugin_div_counter_value == 6'h21);
   assign memory_DivPlugin_div_counter_willOverflow = (memory_DivPlugin_div_counter_willOverflowIfInc && memory_DivPlugin_div_counter_willIncrement);
   always @(*) begin
      if (memory_DivPlugin_div_counter_willOverflow) begin
         memory_DivPlugin_div_counter_valueNext = 6'h00;
      end else begin
         memory_DivPlugin_div_counter_valueNext = (memory_DivPlugin_div_counter_value + _zz_memory_DivPlugin_div_counter_valueNext);
      end
      if (memory_DivPlugin_div_counter_willClear) begin
         memory_DivPlugin_div_counter_valueNext = 6'h00;
      end
   end

   assign when_MulDivIterativePlugin_l126 = (memory_DivPlugin_div_counter_value == 6'h20);
   assign when_MulDivIterativePlugin_l126_1 = (!memory_arbitration_isStuck);
   assign when_MulDivIterativePlugin_l128 = (memory_arbitration_isValid && memory_IS_DIV);
   assign when_MulDivIterativePlugin_l129 = ((! memory_DivPlugin_frontendOk) || (! memory_DivPlugin_div_done));
   assign when_MulDivIterativePlugin_l132 = (memory_DivPlugin_frontendOk && (! memory_DivPlugin_div_done));
   assign _zz_memory_DivPlugin_div_stage_0_remainderShifted = memory_DivPlugin_rs1[31 : 0];
   assign memory_DivPlugin_div_stage_0_remainderShifted = {
      memory_DivPlugin_accumulator[31 : 0], _zz_memory_DivPlugin_div_stage_0_remainderShifted[31]
   };
   assign memory_DivPlugin_div_stage_0_remainderMinusDenominator = (memory_DivPlugin_div_stage_0_remainderShifted - _zz_memory_DivPlugin_div_stage_0_remainderMinusDenominator);
   assign memory_DivPlugin_div_stage_0_outRemainder = ((! memory_DivPlugin_div_stage_0_remainderMinusDenominator[32]) ? _zz_memory_DivPlugin_div_stage_0_outRemainder : _zz_memory_DivPlugin_div_stage_0_outRemainder_1);
   assign memory_DivPlugin_div_stage_0_outNumerator = _zz_memory_DivPlugin_div_stage_0_outNumerator[31:0];
   assign when_MulDivIterativePlugin_l151 = (memory_DivPlugin_div_counter_value == 6'h20);
   assign _zz_memory_DivPlugin_div_result = (memory_INSTRUCTION[13] ? memory_DivPlugin_accumulator[31 : 0] : memory_DivPlugin_rs1[31 : 0]);
   assign when_MulDivIterativePlugin_l162 = (!memory_arbitration_isStuck);
   assign _zz_memory_DivPlugin_rs2 = (execute_RS2[31] && execute_IS_RS2_SIGNED);
   assign _zz_memory_DivPlugin_rs1 = (1'b0 || ((execute_IS_DIV && execute_RS1[31]) && execute_IS_RS1_SIGNED));
   always @(*) begin
      _zz_memory_DivPlugin_rs1_1[32]     = (execute_IS_RS1_SIGNED && execute_RS1[31]);
      _zz_memory_DivPlugin_rs1_1[31 : 0] = execute_RS1;
   end

   always @(*) begin
      HazardSimplePlugin_src0Hazard = 1'b0;
      if (when_HazardSimplePlugin_l57) begin
         if (when_HazardSimplePlugin_l58) begin
            if (when_HazardSimplePlugin_l48) begin
               HazardSimplePlugin_src0Hazard = 1'b1;
            end
         end
      end
      if (when_HazardSimplePlugin_l57_1) begin
         if (when_HazardSimplePlugin_l58_1) begin
            if (when_HazardSimplePlugin_l48_1) begin
               HazardSimplePlugin_src0Hazard = 1'b1;
            end
         end
      end
      if (when_HazardSimplePlugin_l57_2) begin
         if (when_HazardSimplePlugin_l58_2) begin
            if (when_HazardSimplePlugin_l48_2) begin
               HazardSimplePlugin_src0Hazard = 1'b1;
            end
         end
      end
      if (when_HazardSimplePlugin_l105) begin
         HazardSimplePlugin_src0Hazard = 1'b0;
      end
   end

   always @(*) begin
      HazardSimplePlugin_src1Hazard = 1'b0;
      if (when_HazardSimplePlugin_l57) begin
         if (when_HazardSimplePlugin_l58) begin
            if (when_HazardSimplePlugin_l51) begin
               HazardSimplePlugin_src1Hazard = 1'b1;
            end
         end
      end
      if (when_HazardSimplePlugin_l57_1) begin
         if (when_HazardSimplePlugin_l58_1) begin
            if (when_HazardSimplePlugin_l51_1) begin
               HazardSimplePlugin_src1Hazard = 1'b1;
            end
         end
      end
      if (when_HazardSimplePlugin_l57_2) begin
         if (when_HazardSimplePlugin_l58_2) begin
            if (when_HazardSimplePlugin_l51_2) begin
               HazardSimplePlugin_src1Hazard = 1'b1;
            end
         end
      end
      if (when_HazardSimplePlugin_l108) begin
         HazardSimplePlugin_src1Hazard = 1'b0;
      end
   end

   assign HazardSimplePlugin_writeBackWrites_valid = (_zz_lastStageRegFileWrite_valid && writeBack_arbitration_isFiring);
   assign HazardSimplePlugin_writeBackWrites_payload_address = _zz_lastStageRegFileWrite_payload_address[11 : 7];
   assign HazardSimplePlugin_writeBackWrites_payload_data = _zz_decode_RS2_2;
   assign HazardSimplePlugin_addr0Match = (HazardSimplePlugin_writeBackBuffer_payload_address == decode_INSTRUCTION[19 : 15]);
   assign HazardSimplePlugin_addr1Match = (HazardSimplePlugin_writeBackBuffer_payload_address == decode_INSTRUCTION[24 : 20]);
   assign when_HazardSimplePlugin_l47 = 1'b1;
   assign when_HazardSimplePlugin_l48 = (writeBack_INSTRUCTION[11 : 7] == decode_INSTRUCTION[19 : 15]);
   assign when_HazardSimplePlugin_l51 = (writeBack_INSTRUCTION[11 : 7] == decode_INSTRUCTION[24 : 20]);
   assign when_HazardSimplePlugin_l45 = (writeBack_arbitration_isValid && writeBack_REGFILE_WRITE_VALID);
   assign when_HazardSimplePlugin_l57 = (writeBack_arbitration_isValid && writeBack_REGFILE_WRITE_VALID);
   assign when_HazardSimplePlugin_l58 = (1'b0 || (!when_HazardSimplePlugin_l47));
   assign when_HazardSimplePlugin_l48_1 = (memory_INSTRUCTION[11 : 7] == decode_INSTRUCTION[19 : 15]);
   assign when_HazardSimplePlugin_l51_1 = (memory_INSTRUCTION[11 : 7] == decode_INSTRUCTION[24 : 20]);
   assign when_HazardSimplePlugin_l45_1 = (memory_arbitration_isValid && memory_REGFILE_WRITE_VALID);
   assign when_HazardSimplePlugin_l57_1 = (memory_arbitration_isValid && memory_REGFILE_WRITE_VALID);
   assign when_HazardSimplePlugin_l58_1 = (1'b0 || (!memory_BYPASSABLE_MEMORY_STAGE));
   assign when_HazardSimplePlugin_l48_2 = (execute_INSTRUCTION[11 : 7] == decode_INSTRUCTION[19 : 15]);
   assign when_HazardSimplePlugin_l51_2 = (execute_INSTRUCTION[11 : 7] == decode_INSTRUCTION[24 : 20]);
   assign when_HazardSimplePlugin_l45_2 = (execute_arbitration_isValid && execute_REGFILE_WRITE_VALID);
   assign when_HazardSimplePlugin_l57_2 = (execute_arbitration_isValid && execute_REGFILE_WRITE_VALID);
   assign when_HazardSimplePlugin_l58_2 = (1'b0 || (!execute_BYPASSABLE_EXECUTE_STAGE));
   assign when_HazardSimplePlugin_l105 = (!decode_RS1_USE);
   assign when_HazardSimplePlugin_l108 = (!decode_RS2_USE);
   assign when_HazardSimplePlugin_l113 = (decode_arbitration_isValid && (HazardSimplePlugin_src0Hazard || HazardSimplePlugin_src1Hazard));
   assign execute_BranchPlugin_eq = (execute_SRC1 == execute_SRC2);
   assign switch_Misc_l227_3 = execute_INSTRUCTION[14 : 12];
   always @(*) begin
      case (switch_Misc_l227_3)
         3'b000: begin
            _zz_execute_BRANCH_DO = execute_BranchPlugin_eq;
         end
         3'b001: begin
            _zz_execute_BRANCH_DO = (!execute_BranchPlugin_eq);
         end
         3'b101: begin
            _zz_execute_BRANCH_DO = (!execute_SRC_LESS);
         end
         3'b111: begin
            _zz_execute_BRANCH_DO = (!execute_SRC_LESS);
         end
         default: begin
            _zz_execute_BRANCH_DO = execute_SRC_LESS;
         end
      endcase
   end

   always @(*) begin
      case (execute_BRANCH_CTRL)
         BranchCtrlEnum_INC: begin
            _zz_execute_BRANCH_DO_1 = 1'b0;
         end
         BranchCtrlEnum_JAL: begin
            _zz_execute_BRANCH_DO_1 = 1'b1;
         end
         BranchCtrlEnum_JALR: begin
            _zz_execute_BRANCH_DO_1 = 1'b1;
         end
         default: begin
            _zz_execute_BRANCH_DO_1 = _zz_execute_BRANCH_DO;
         end
      endcase
   end

   assign execute_BranchPlugin_branch_src1 = ((execute_BRANCH_CTRL == BranchCtrlEnum_JALR) ? execute_RS1 : execute_PC);
   assign _zz_execute_BranchPlugin_branch_src2 = _zz__zz_execute_BranchPlugin_branch_src2[19];
   always @(*) begin
      _zz_execute_BranchPlugin_branch_src2_1[10] = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[9]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[8]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[7]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[6]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[5]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[4]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[3]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[2]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[1]  = _zz_execute_BranchPlugin_branch_src2;
      _zz_execute_BranchPlugin_branch_src2_1[0]  = _zz_execute_BranchPlugin_branch_src2;
   end

   assign _zz_execute_BranchPlugin_branch_src2_2 = execute_INSTRUCTION[31];
   always @(*) begin
      _zz_execute_BranchPlugin_branch_src2_3[19] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[18] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[17] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[16] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[15] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[14] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[13] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[12] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[11] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[10] = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[9]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[8]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[7]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[6]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[5]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[4]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[3]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[2]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[1]  = _zz_execute_BranchPlugin_branch_src2_2;
      _zz_execute_BranchPlugin_branch_src2_3[0]  = _zz_execute_BranchPlugin_branch_src2_2;
   end

   assign _zz_execute_BranchPlugin_branch_src2_4 = _zz__zz_execute_BranchPlugin_branch_src2_4[11];
   always @(*) begin
      _zz_execute_BranchPlugin_branch_src2_5[18] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[17] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[16] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[15] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[14] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[13] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[12] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[11] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[10] = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[9]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[8]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[7]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[6]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[5]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[4]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[3]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[2]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[1]  = _zz_execute_BranchPlugin_branch_src2_4;
      _zz_execute_BranchPlugin_branch_src2_5[0]  = _zz_execute_BranchPlugin_branch_src2_4;
   end

   always @(*) begin
      case (execute_BRANCH_CTRL)
         BranchCtrlEnum_JAL: begin
            _zz_execute_BranchPlugin_branch_src2_6 = {
               {
                  _zz_execute_BranchPlugin_branch_src2_1,
                  {
                     {
                        {execute_INSTRUCTION[31], execute_INSTRUCTION[19 : 12]},
                        execute_INSTRUCTION[20]
                     },
                     execute_INSTRUCTION[30 : 21]
                  }
               },
               1'b0
            };
         end
         BranchCtrlEnum_JALR: begin
            _zz_execute_BranchPlugin_branch_src2_6 = {
               _zz_execute_BranchPlugin_branch_src2_3, execute_INSTRUCTION[31 : 20]
            };
         end
         default: begin
            _zz_execute_BranchPlugin_branch_src2_6 = {
               {
                  _zz_execute_BranchPlugin_branch_src2_5,
                  {
                     {
                        {execute_INSTRUCTION[31], execute_INSTRUCTION[7]},
                        execute_INSTRUCTION[30 : 25]
                     },
                     execute_INSTRUCTION[11 : 8]
                  }
               },
               1'b0
            };
         end
      endcase
   end

   assign execute_BranchPlugin_branch_src2 = _zz_execute_BranchPlugin_branch_src2_6;
   assign execute_BranchPlugin_branchAdder = (execute_BranchPlugin_branch_src1 + execute_BranchPlugin_branch_src2);
   assign BranchPlugin_jumpInterface_valid = ((memory_arbitration_isValid && memory_BRANCH_DO) && (! 1'b0));
   assign BranchPlugin_jumpInterface_payload = memory_BRANCH_CALC;
   always @(*) begin
      CsrPlugin_privilege = _zz_CsrPlugin_privilege;
      if (CsrPlugin_forceMachineWire) begin
         CsrPlugin_privilege = 2'b11;
      end
   end

   assign CsrPlugin_misa_base       = 2'b01;
   assign CsrPlugin_misa_extensions = 26'h0141105;
   assign CsrPlugin_mtvec_mode      = 2'b00;
   assign CsrPlugin_sip_SEIP_OR     = (CsrPlugin_sip_SEIP_SOFT || CsrPlugin_sip_SEIP_INPUT);
   always @(*) begin
      CsrPlugin_redoInterface_valid = 1'b0;
      if (CsrPlugin_rescheduleLogic_rescheduleNext) begin
         CsrPlugin_redoInterface_valid = 1'b1;
      end
   end

   assign CsrPlugin_redoInterface_payload = decode_PC;
   always @(*) begin
      CsrPlugin_rescheduleLogic_rescheduleNext = 1'b0;
      if (when_CsrPlugin_l1153) begin
         CsrPlugin_rescheduleLogic_rescheduleNext = 1'b1;
      end
      if (execute_CsrPlugin_csr_384) begin
         if (execute_CsrPlugin_writeInstruction) begin
            CsrPlugin_rescheduleLogic_rescheduleNext = 1'b1;
         end
      end
   end

   assign when_CsrPlugin_l1153       = (execute_arbitration_isValid && execute_RESCHEDULE_NEXT);
   assign _zz_when_CsrPlugin_l1302   = (CsrPlugin_sip_STIP && CsrPlugin_sie_STIE);
   assign _zz_when_CsrPlugin_l1302_1 = (CsrPlugin_sip_SSIP && CsrPlugin_sie_SSIE);
   assign _zz_when_CsrPlugin_l1302_2 = (CsrPlugin_sip_SEIP_OR && CsrPlugin_sie_SEIE);
   assign _zz_when_CsrPlugin_l1302_3 = (CsrPlugin_mip_MTIP && CsrPlugin_mie_MTIE);
   assign _zz_when_CsrPlugin_l1302_4 = (CsrPlugin_mip_MSIP && CsrPlugin_mie_MSIE);
   assign _zz_when_CsrPlugin_l1302_5 = (CsrPlugin_mip_MEIP && CsrPlugin_mie_MEIE);
   always @(*) begin
      CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b11;
      case (CsrPlugin_exceptionPortCtrl_exceptionContext_code)
         4'b0000: begin
            if (when_CsrPlugin_l1216) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b0001: begin
            if (when_CsrPlugin_l1216_1) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b0010: begin
            if (when_CsrPlugin_l1216_2) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b0011: begin
            if (when_CsrPlugin_l1216_3) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b0100: begin
            if (when_CsrPlugin_l1216_4) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b0101: begin
            if (when_CsrPlugin_l1216_5) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b0110: begin
            if (when_CsrPlugin_l1216_6) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b0111: begin
            if (when_CsrPlugin_l1216_7) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b1000: begin
            if (when_CsrPlugin_l1216_8) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b1001: begin
            if (when_CsrPlugin_l1216_9) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b1100: begin
            if (when_CsrPlugin_l1216_10) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b1101: begin
            if (when_CsrPlugin_l1216_11) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         4'b1111: begin
            if (when_CsrPlugin_l1216_12) begin
               CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped = 2'b01;
            end
         end
         default: begin
         end
      endcase
   end

   assign when_CsrPlugin_l1216 = ((1'b1 && CsrPlugin_medeleg_IAM) && (!1'b0));
   assign when_CsrPlugin_l1216_1 = ((1'b1 && CsrPlugin_medeleg_IAF) && (!1'b0));
   assign when_CsrPlugin_l1216_2 = ((1'b1 && CsrPlugin_medeleg_II) && (!1'b0));
   assign when_CsrPlugin_l1216_3 = ((1'b1 && CsrPlugin_medeleg_BP) && (!1'b0));
   assign when_CsrPlugin_l1216_4 = ((1'b1 && CsrPlugin_medeleg_LAM) && (!1'b0));
   assign when_CsrPlugin_l1216_5 = ((1'b1 && CsrPlugin_medeleg_LAF) && (!1'b0));
   assign when_CsrPlugin_l1216_6 = ((1'b1 && CsrPlugin_medeleg_SAM) && (!1'b0));
   assign when_CsrPlugin_l1216_7 = ((1'b1 && CsrPlugin_medeleg_SAF) && (!1'b0));
   assign when_CsrPlugin_l1216_8 = ((1'b1 && CsrPlugin_medeleg_EU) && (!1'b0));
   assign when_CsrPlugin_l1216_9 = ((1'b1 && CsrPlugin_medeleg_ES) && (!1'b0));
   assign when_CsrPlugin_l1216_10 = ((1'b1 && CsrPlugin_medeleg_IPF) && (!1'b0));
   assign when_CsrPlugin_l1216_11 = ((1'b1 && CsrPlugin_medeleg_LPF) && (!1'b0));
   assign when_CsrPlugin_l1216_12 = ((1'b1 && CsrPlugin_medeleg_SPF) && (!1'b0));
   assign CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilege = ((CsrPlugin_privilege < CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped) ? CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilegeUncapped : CsrPlugin_privilege);
   assign _zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code = {
      decodeExceptionPort_valid, IBusCachedPlugin_decodeExceptionPort_valid
   };
   assign _zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1 = _zz__zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1[0];
   always @(*) begin
      CsrPlugin_exceptionPortCtrl_exceptionValids_decode = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_decode;
      if (_zz_when) begin
         CsrPlugin_exceptionPortCtrl_exceptionValids_decode = 1'b1;
      end
      if (decode_arbitration_isFlushed) begin
         CsrPlugin_exceptionPortCtrl_exceptionValids_decode = 1'b0;
      end
   end

   always @(*) begin
      CsrPlugin_exceptionPortCtrl_exceptionValids_execute = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_execute;
      if (CsrPlugin_selfException_valid) begin
         CsrPlugin_exceptionPortCtrl_exceptionValids_execute = 1'b1;
      end
      if (execute_arbitration_isFlushed) begin
         CsrPlugin_exceptionPortCtrl_exceptionValids_execute = 1'b0;
      end
   end

   always @(*) begin
      CsrPlugin_exceptionPortCtrl_exceptionValids_memory = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_memory;
      if (memory_arbitration_isFlushed) begin
         CsrPlugin_exceptionPortCtrl_exceptionValids_memory = 1'b0;
      end
   end

   always @(*) begin
      CsrPlugin_exceptionPortCtrl_exceptionValids_writeBack = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_writeBack;
      if (DBusCachedPlugin_exceptionBus_valid) begin
         CsrPlugin_exceptionPortCtrl_exceptionValids_writeBack = 1'b1;
      end
      if (writeBack_arbitration_isFlushed) begin
         CsrPlugin_exceptionPortCtrl_exceptionValids_writeBack = 1'b0;
      end
   end

   assign when_CsrPlugin_l1259 = (!decode_arbitration_isStuck);
   assign when_CsrPlugin_l1259_1 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1259_2 = (!memory_arbitration_isStuck);
   assign when_CsrPlugin_l1259_3 = (!writeBack_arbitration_isStuck);
   assign when_CsrPlugin_l1272 = ({CsrPlugin_exceptionPortCtrl_exceptionValids_writeBack,{CsrPlugin_exceptionPortCtrl_exceptionValids_memory,{CsrPlugin_exceptionPortCtrl_exceptionValids_execute,CsrPlugin_exceptionPortCtrl_exceptionValids_decode}}} != 4'b0000);
   assign CsrPlugin_exceptionPendings_0 = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_decode;
   assign CsrPlugin_exceptionPendings_1 = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_execute;
   assign CsrPlugin_exceptionPendings_2 = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_memory;
   assign CsrPlugin_exceptionPendings_3 = CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_writeBack;
   assign when_CsrPlugin_l1296 = ((CsrPlugin_sstatus_SIE && (CsrPlugin_privilege == 2'b01)) || (CsrPlugin_privilege < 2'b01));
   assign when_CsrPlugin_l1296_1 = (CsrPlugin_mstatus_MIE || (CsrPlugin_privilege < 2'b11));
   assign when_CsrPlugin_l1302 = ((_zz_when_CsrPlugin_l1302 && (1'b1 && CsrPlugin_mideleg_ST)) && (! 1'b0));
   assign when_CsrPlugin_l1302_1 = ((_zz_when_CsrPlugin_l1302_1 && (1'b1 && CsrPlugin_mideleg_SS)) && (! 1'b0));
   assign when_CsrPlugin_l1302_2 = ((_zz_when_CsrPlugin_l1302_2 && (1'b1 && CsrPlugin_mideleg_SE)) && (! 1'b0));
   assign when_CsrPlugin_l1302_3 = ((_zz_when_CsrPlugin_l1302 && 1'b1) && (! (CsrPlugin_mideleg_ST != 1'b0)));
   assign when_CsrPlugin_l1302_4 = ((_zz_when_CsrPlugin_l1302_1 && 1'b1) && (! (CsrPlugin_mideleg_SS != 1'b0)));
   assign when_CsrPlugin_l1302_5 = ((_zz_when_CsrPlugin_l1302_2 && 1'b1) && (! (CsrPlugin_mideleg_SE != 1'b0)));
   assign when_CsrPlugin_l1302_6 = ((_zz_when_CsrPlugin_l1302_3 && 1'b1) && (!1'b0));
   assign when_CsrPlugin_l1302_7 = ((_zz_when_CsrPlugin_l1302_4 && 1'b1) && (!1'b0));
   assign when_CsrPlugin_l1302_8 = ((_zz_when_CsrPlugin_l1302_5 && 1'b1) && (!1'b0));
   assign CsrPlugin_exception = (CsrPlugin_exceptionPortCtrl_exceptionValids_writeBack && CsrPlugin_allowException);
   assign CsrPlugin_pipelineLiberator_active = ((CsrPlugin_interrupt_valid && CsrPlugin_allowInterrupts) && decode_arbitration_isValid);
   assign when_CsrPlugin_l1335 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1335_1 = (!memory_arbitration_isStuck);
   assign when_CsrPlugin_l1335_2 = (!writeBack_arbitration_isStuck);
   assign when_CsrPlugin_l1340 = ((! CsrPlugin_pipelineLiberator_active) || decode_arbitration_removeIt);
   always @(*) begin
      CsrPlugin_pipelineLiberator_done = CsrPlugin_pipelineLiberator_pcValids_2;
      if (when_CsrPlugin_l1346) begin
         CsrPlugin_pipelineLiberator_done = 1'b0;
      end
      if (CsrPlugin_hadException) begin
         CsrPlugin_pipelineLiberator_done = 1'b0;
      end
   end

   assign when_CsrPlugin_l1346 = ({CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_writeBack,{CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_memory,CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_execute}} != 3'b000);
   assign CsrPlugin_interruptJump = ((CsrPlugin_interrupt_valid && CsrPlugin_pipelineLiberator_done) && CsrPlugin_allowInterrupts);
   always @(*) begin
      CsrPlugin_targetPrivilege = CsrPlugin_interrupt_targetPrivilege;
      if (CsrPlugin_hadException) begin
         CsrPlugin_targetPrivilege = CsrPlugin_exceptionPortCtrl_exceptionTargetPrivilege;
      end
   end

   always @(*) begin
      CsrPlugin_trapCause = CsrPlugin_interrupt_code;
      if (CsrPlugin_hadException) begin
         CsrPlugin_trapCause = CsrPlugin_exceptionPortCtrl_exceptionContext_code;
      end
   end

   assign CsrPlugin_trapCauseEbreakDebug = 1'b0;
   always @(*) begin
      CsrPlugin_xtvec_mode = 2'bxx;
      case (CsrPlugin_targetPrivilege)
         2'b01: begin
            CsrPlugin_xtvec_mode = CsrPlugin_stvec_mode;
         end
         2'b11: begin
            CsrPlugin_xtvec_mode = CsrPlugin_mtvec_mode;
         end
         default: begin
         end
      endcase
   end

   always @(*) begin
      CsrPlugin_xtvec_base = 30'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
      case (CsrPlugin_targetPrivilege)
         2'b01: begin
            CsrPlugin_xtvec_base = CsrPlugin_stvec_base;
         end
         2'b11: begin
            CsrPlugin_xtvec_base = CsrPlugin_mtvec_base;
         end
         default: begin
         end
      endcase
   end

   assign CsrPlugin_trapEnterDebug = 1'b0;
   assign when_CsrPlugin_l1390 = (CsrPlugin_hadException || CsrPlugin_interruptJump);
   assign when_CsrPlugin_l1398 = (!CsrPlugin_trapEnterDebug);
   assign when_CsrPlugin_l1456 = (writeBack_arbitration_isValid && (writeBack_ENV_CTRL == EnvCtrlEnum_XRET));
   assign switch_CsrPlugin_l1460 = writeBack_INSTRUCTION[29 : 28];
   assign when_CsrPlugin_l1468 = (CsrPlugin_mstatus_MPP < 2'b11);
   assign contextSwitching = CsrPlugin_jumpInterface_valid;
   assign when_CsrPlugin_l1519 = (execute_arbitration_isValid && (execute_ENV_CTRL == EnvCtrlEnum_WFI));
   assign when_CsrPlugin_l1521 = (!execute_CsrPlugin_wfiWake);
   assign when_CsrPlugin_l1527 = (|{(writeBack_arbitration_isValid && (writeBack_ENV_CTRL == EnvCtrlEnum_XRET)),{
      (memory_arbitration_isValid && (memory_ENV_CTRL == EnvCtrlEnum_XRET)),
      (execute_arbitration_isValid && (execute_ENV_CTRL == EnvCtrlEnum_XRET))
   }});
   assign execute_CsrPlugin_blockedBySideEffects = ((|{writeBack_arbitration_isValid,memory_arbitration_isValid}) || 1'b0);
   always @(*) begin
      execute_CsrPlugin_illegalAccess = 1'b1;
      if (execute_CsrPlugin_csr_768) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_256) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_384) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_3857) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3858) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3859) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3860) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_769) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_836) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_772) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_773) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_833) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_832) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_834) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_835) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_2816) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_2944) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_2818) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_2946) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_770) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_771) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_3072) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3200) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3074) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3202) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3073) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_3201) begin
         if (execute_CSR_READ_OPCODE) begin
            execute_CsrPlugin_illegalAccess = 1'b0;
         end
      end
      if (execute_CsrPlugin_csr_774) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_262) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_324) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_260) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_261) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_321) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_320) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_322) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (execute_CsrPlugin_csr_323) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (CsrPlugin_csrMapping_allowCsrSignal) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
      if (when_CsrPlugin_l1719) begin
         execute_CsrPlugin_illegalAccess = 1'b1;
      end
      if (when_CsrPlugin_l1725) begin
         execute_CsrPlugin_illegalAccess = 1'b0;
      end
   end

   always @(*) begin
      execute_CsrPlugin_illegalInstruction = 1'b0;
      if (when_CsrPlugin_l1547) begin
         if (when_CsrPlugin_l1548) begin
            execute_CsrPlugin_illegalInstruction = 1'b1;
         end
      end
   end

   always @(*) begin
      CsrPlugin_selfException_valid = 1'b0;
      if (when_CsrPlugin_l1540) begin
         CsrPlugin_selfException_valid = 1'b1;
      end
      if (when_CsrPlugin_l1555) begin
         CsrPlugin_selfException_valid = 1'b1;
      end
      if (when_CsrPlugin_l1565) begin
         CsrPlugin_selfException_valid = 1'b1;
      end
   end

   always @(*) begin
      CsrPlugin_selfException_payload_code = 4'bxxxx;
      if (when_CsrPlugin_l1540) begin
         CsrPlugin_selfException_payload_code = 4'b0010;
      end
      if (when_CsrPlugin_l1555) begin
         case (CsrPlugin_privilege)
            2'b00: begin
               CsrPlugin_selfException_payload_code = 4'b1000;
            end
            2'b01: begin
               CsrPlugin_selfException_payload_code = 4'b1001;
            end
            default: begin
               CsrPlugin_selfException_payload_code = 4'b1011;
            end
         endcase
      end
      if (when_CsrPlugin_l1565) begin
         CsrPlugin_selfException_payload_code = 4'b0011;
      end
   end

   assign CsrPlugin_selfException_payload_badAddr = execute_INSTRUCTION;
   assign when_CsrPlugin_l1540 = (execute_CsrPlugin_illegalAccess || execute_CsrPlugin_illegalInstruction);
   assign when_CsrPlugin_l1547 = (execute_arbitration_isValid && (execute_ENV_CTRL == EnvCtrlEnum_XRET));
   assign when_CsrPlugin_l1548 = (CsrPlugin_privilege < execute_INSTRUCTION[29 : 28]);
   assign when_CsrPlugin_l1555 = (execute_arbitration_isValid && (execute_ENV_CTRL == EnvCtrlEnum_ECALL));
   assign when_CsrPlugin_l1565 = ((execute_arbitration_isValid && (execute_ENV_CTRL == EnvCtrlEnum_EBREAK)) && CsrPlugin_allowEbreakException);
   always @(*) begin
      execute_CsrPlugin_writeInstruction = ((execute_arbitration_isValid && execute_IS_CSR) && execute_CSR_WRITE_OPCODE);
      if (when_CsrPlugin_l1719) begin
         execute_CsrPlugin_writeInstruction = 1'b0;
      end
   end

   always @(*) begin
      execute_CsrPlugin_readInstruction = ((execute_arbitration_isValid && execute_IS_CSR) && execute_CSR_READ_OPCODE);
      if (when_CsrPlugin_l1719) begin
         execute_CsrPlugin_readInstruction = 1'b0;
      end
   end

   assign execute_CsrPlugin_writeEnable = (execute_CsrPlugin_writeInstruction && (! execute_arbitration_isStuck));
   assign execute_CsrPlugin_readEnable = (execute_CsrPlugin_readInstruction && (! execute_arbitration_isStuck));
   assign CsrPlugin_csrMapping_hazardFree = (!execute_CsrPlugin_blockedBySideEffects);
   always @(*) begin
      execute_CsrPlugin_readToWriteData = CsrPlugin_csrMapping_readDataSignal;
      if (execute_CsrPlugin_csr_836) begin
         execute_CsrPlugin_readToWriteData[9 : 9] = CsrPlugin_sip_SEIP_SOFT;
      end
      if (execute_CsrPlugin_csr_324) begin
         execute_CsrPlugin_readToWriteData[9 : 9] = CsrPlugin_sip_SEIP_SOFT;
      end
   end

   assign switch_Misc_l227_4 = execute_INSTRUCTION[13];
   always @(*) begin
      case (switch_Misc_l227_4)
         1'b0: begin
            _zz_CsrPlugin_csrMapping_writeDataSignal = execute_SRC1;
         end
         default: begin
            _zz_CsrPlugin_csrMapping_writeDataSignal = (execute_INSTRUCTION[12] ? (execute_CsrPlugin_readToWriteData & (~ execute_SRC1)) : (execute_CsrPlugin_readToWriteData | execute_SRC1));
         end
      endcase
   end

   assign CsrPlugin_csrMapping_writeDataSignal = _zz_CsrPlugin_csrMapping_writeDataSignal;
   assign when_CsrPlugin_l1587 = (execute_arbitration_isValid && execute_IS_CSR);
   assign when_CsrPlugin_l1591 = (execute_arbitration_isValid && (execute_IS_CSR || execute_RESCHEDULE_NEXT));
   assign execute_CsrPlugin_csrAddress = execute_INSTRUCTION[31 : 20];
   assign when_Pipeline_l124 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_1 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_2 = ((! writeBack_arbitration_isStuck) && (! CsrPlugin_exceptionPortCtrl_exceptionValids_writeBack));
   assign when_Pipeline_l124_3 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_4 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_5 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_6 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_7 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_8 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_9 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_10 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_11 = (!execute_arbitration_isStuck);
   assign _zz_decode_to_execute_SRC1_CTRL_1 = decode_SRC1_CTRL;
   assign _zz_decode_SRC1_CTRL = _zz_decode_SRC1_CTRL_1;
   assign when_Pipeline_l124_12 = (!execute_arbitration_isStuck);
   assign _zz_execute_SRC1_CTRL = decode_to_execute_SRC1_CTRL;
   assign when_Pipeline_l124_13 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_14 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_15 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_16 = (!writeBack_arbitration_isStuck);
   assign _zz_decode_to_execute_ALU_CTRL_1 = decode_ALU_CTRL;
   assign _zz_decode_ALU_CTRL = _zz_decode_ALU_CTRL_1;
   assign when_Pipeline_l124_17 = (!execute_arbitration_isStuck);
   assign _zz_execute_ALU_CTRL = decode_to_execute_ALU_CTRL;
   assign _zz_decode_to_execute_SRC2_CTRL_1 = decode_SRC2_CTRL;
   assign _zz_decode_SRC2_CTRL = _zz_decode_SRC2_CTRL_1;
   assign when_Pipeline_l124_18 = (!execute_arbitration_isStuck);
   assign _zz_execute_SRC2_CTRL = decode_to_execute_SRC2_CTRL;
   assign when_Pipeline_l124_19 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_20 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_21 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_22 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_23 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_24 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_25 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_26 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_27 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_28 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_29 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_30 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_31 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_32 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_33 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_34 = (!execute_arbitration_isStuck);
   assign _zz_decode_to_execute_ALU_BITWISE_CTRL_1 = decode_ALU_BITWISE_CTRL;
   assign _zz_decode_ALU_BITWISE_CTRL = _zz_decode_ALU_BITWISE_CTRL_1;
   assign when_Pipeline_l124_35 = (!execute_arbitration_isStuck);
   assign _zz_execute_ALU_BITWISE_CTRL = decode_to_execute_ALU_BITWISE_CTRL;
   assign _zz_decode_to_execute_SHIFT_CTRL_1 = decode_SHIFT_CTRL;
   assign _zz_execute_to_memory_SHIFT_CTRL_1 = execute_SHIFT_CTRL;
   assign _zz_decode_SHIFT_CTRL = _zz_decode_SHIFT_CTRL_1;
   assign when_Pipeline_l124_36 = (!execute_arbitration_isStuck);
   assign _zz_execute_SHIFT_CTRL = decode_to_execute_SHIFT_CTRL;
   assign when_Pipeline_l124_37 = (!memory_arbitration_isStuck);
   assign _zz_memory_SHIFT_CTRL = execute_to_memory_SHIFT_CTRL;
   assign when_Pipeline_l124_38 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_39 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_40 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_41 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_42 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_43 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_44 = (!execute_arbitration_isStuck);
   assign _zz_decode_to_execute_BRANCH_CTRL_1 = decode_BRANCH_CTRL;
   assign _zz_decode_BRANCH_CTRL = _zz_decode_BRANCH_CTRL_1;
   assign when_Pipeline_l124_45 = (!execute_arbitration_isStuck);
   assign _zz_execute_BRANCH_CTRL = decode_to_execute_BRANCH_CTRL;
   assign when_Pipeline_l124_46 = (!execute_arbitration_isStuck);
   assign _zz_decode_to_execute_ENV_CTRL_1 = decode_ENV_CTRL;
   assign _zz_execute_to_memory_ENV_CTRL_1 = execute_ENV_CTRL;
   assign _zz_memory_to_writeBack_ENV_CTRL_1 = memory_ENV_CTRL;
   assign _zz_decode_ENV_CTRL = _zz_decode_ENV_CTRL_1;
   assign when_Pipeline_l124_47 = (!execute_arbitration_isStuck);
   assign _zz_execute_ENV_CTRL = decode_to_execute_ENV_CTRL;
   assign when_Pipeline_l124_48 = (!memory_arbitration_isStuck);
   assign _zz_memory_ENV_CTRL = execute_to_memory_ENV_CTRL;
   assign when_Pipeline_l124_49 = (!writeBack_arbitration_isStuck);
   assign _zz_writeBack_ENV_CTRL = memory_to_writeBack_ENV_CTRL;
   assign when_Pipeline_l124_50 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_51 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_52 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_53 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_54 = (!execute_arbitration_isStuck);
   assign when_Pipeline_l124_55 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_56 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_57 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_58 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_59 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_60 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_61 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_62 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_63 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_64 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_65 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_66 = (!writeBack_arbitration_isStuck);
   assign when_Pipeline_l124_67 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_68 = (!memory_arbitration_isStuck);
   assign when_Pipeline_l124_69 = (!writeBack_arbitration_isStuck);
   assign decode_arbitration_isFlushed = (({writeBack_arbitration_flushNext,{memory_arbitration_flushNext,execute_arbitration_flushNext}} != 3'b000) || ({writeBack_arbitration_flushIt,{memory_arbitration_flushIt,{execute_arbitration_flushIt,decode_arbitration_flushIt}}} != 4'b0000));
   assign execute_arbitration_isFlushed = (({writeBack_arbitration_flushNext,memory_arbitration_flushNext} != 2'b00) || ({writeBack_arbitration_flushIt,{memory_arbitration_flushIt,execute_arbitration_flushIt}} != 3'b000));
   assign memory_arbitration_isFlushed = ((writeBack_arbitration_flushNext != 1'b0) || ({writeBack_arbitration_flushIt,memory_arbitration_flushIt} != 2'b00));
   assign writeBack_arbitration_isFlushed = (1'b0 || (writeBack_arbitration_flushIt != 1'b0));
   assign decode_arbitration_isStuckByOthers = (decode_arbitration_haltByOther || (((1'b0 || execute_arbitration_isStuck) || memory_arbitration_isStuck) || writeBack_arbitration_isStuck));
   assign decode_arbitration_isStuck = (decode_arbitration_haltItself || decode_arbitration_isStuckByOthers);
   assign decode_arbitration_isMoving = ((! decode_arbitration_isStuck) && (! decode_arbitration_removeIt));
   assign decode_arbitration_isFiring = ((decode_arbitration_isValid && (! decode_arbitration_isStuck)) && (! decode_arbitration_removeIt));
   assign execute_arbitration_isStuckByOthers = (execute_arbitration_haltByOther || ((1'b0 || memory_arbitration_isStuck) || writeBack_arbitration_isStuck));
   assign execute_arbitration_isStuck = (execute_arbitration_haltItself || execute_arbitration_isStuckByOthers);
   assign execute_arbitration_isMoving = ((! execute_arbitration_isStuck) && (! execute_arbitration_removeIt));
   assign execute_arbitration_isFiring = ((execute_arbitration_isValid && (! execute_arbitration_isStuck)) && (! execute_arbitration_removeIt));
   assign memory_arbitration_isStuckByOthers = (memory_arbitration_haltByOther || (1'b0 || writeBack_arbitration_isStuck));
   assign memory_arbitration_isStuck = (memory_arbitration_haltItself || memory_arbitration_isStuckByOthers);
   assign memory_arbitration_isMoving = ((! memory_arbitration_isStuck) && (! memory_arbitration_removeIt));
   assign memory_arbitration_isFiring = ((memory_arbitration_isValid && (! memory_arbitration_isStuck)) && (! memory_arbitration_removeIt));
   assign writeBack_arbitration_isStuckByOthers = (writeBack_arbitration_haltByOther || 1'b0);
   assign writeBack_arbitration_isStuck = (writeBack_arbitration_haltItself || writeBack_arbitration_isStuckByOthers);
   assign writeBack_arbitration_isMoving = ((! writeBack_arbitration_isStuck) && (! writeBack_arbitration_removeIt));
   assign writeBack_arbitration_isFiring = ((writeBack_arbitration_isValid && (! writeBack_arbitration_isStuck)) && (! writeBack_arbitration_removeIt));
   assign when_Pipeline_l151 = ((!execute_arbitration_isStuck) || execute_arbitration_removeIt);
   assign when_Pipeline_l154 = ((!decode_arbitration_isStuck) && (!decode_arbitration_removeIt));
   assign when_Pipeline_l151_1 = ((!memory_arbitration_isStuck) || memory_arbitration_removeIt);
   assign when_Pipeline_l154_1 = ((! execute_arbitration_isStuck) && (! execute_arbitration_removeIt));
   assign when_Pipeline_l151_2 = ((! writeBack_arbitration_isStuck) || writeBack_arbitration_removeIt);
   assign when_Pipeline_l154_2 = ((!memory_arbitration_isStuck) && (!memory_arbitration_removeIt));
   assign when_CsrPlugin_l1669 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_1 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_2 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_3 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_4 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_5 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_6 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_7 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_8 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_9 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_10 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_11 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_12 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_13 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_14 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_15 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_16 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_17 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_18 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_19 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_20 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_21 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_22 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_23 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_24 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_25 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_26 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_27 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_28 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_29 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_30 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_31 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_32 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_33 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_34 = (!execute_arbitration_isStuck);
   assign when_CsrPlugin_l1669_35 = (!execute_arbitration_isStuck);
   assign switch_CsrPlugin_l1031 = CsrPlugin_csrMapping_writeDataSignal[12 : 11];
   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit = 32'h00000000;
      if (execute_CsrPlugin_csr_768) begin
         _zz_CsrPlugin_csrMapping_readDataInit[19 : 19] = MmuPlugin_status_mxr;
         _zz_CsrPlugin_csrMapping_readDataInit[18 : 18] = MmuPlugin_status_sum;
         _zz_CsrPlugin_csrMapping_readDataInit[17 : 17] = MmuPlugin_status_mprv;
         _zz_CsrPlugin_csrMapping_readDataInit[7 : 7]   = CsrPlugin_mstatus_MPIE;
         _zz_CsrPlugin_csrMapping_readDataInit[3 : 3]   = CsrPlugin_mstatus_MIE;
         _zz_CsrPlugin_csrMapping_readDataInit[12 : 11] = CsrPlugin_mstatus_MPP;
         _zz_CsrPlugin_csrMapping_readDataInit[8 : 8]   = CsrPlugin_sstatus_SPP;
         _zz_CsrPlugin_csrMapping_readDataInit[5 : 5]   = CsrPlugin_sstatus_SPIE;
         _zz_CsrPlugin_csrMapping_readDataInit[1 : 1]   = CsrPlugin_sstatus_SIE;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_1 = 32'h00000000;
      if (execute_CsrPlugin_csr_256) begin
         _zz_CsrPlugin_csrMapping_readDataInit_1[19 : 19] = MmuPlugin_status_mxr;
         _zz_CsrPlugin_csrMapping_readDataInit_1[18 : 18] = MmuPlugin_status_sum;
         _zz_CsrPlugin_csrMapping_readDataInit_1[17 : 17] = MmuPlugin_status_mprv;
         _zz_CsrPlugin_csrMapping_readDataInit_1[8 : 8]   = CsrPlugin_sstatus_SPP;
         _zz_CsrPlugin_csrMapping_readDataInit_1[5 : 5]   = CsrPlugin_sstatus_SPIE;
         _zz_CsrPlugin_csrMapping_readDataInit_1[1 : 1]   = CsrPlugin_sstatus_SIE;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_2 = 32'h00000000;
      if (execute_CsrPlugin_csr_384) begin
         _zz_CsrPlugin_csrMapping_readDataInit_2[31 : 31] = MmuPlugin_satp_mode;
         _zz_CsrPlugin_csrMapping_readDataInit_2[30 : 22] = MmuPlugin_satp_asid;
         _zz_CsrPlugin_csrMapping_readDataInit_2[21 : 0]  = MmuPlugin_satp_ppn;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_3 = 32'h00000000;
      if (execute_CsrPlugin_csr_3857) begin
         _zz_CsrPlugin_csrMapping_readDataInit_3[0 : 0] = 1'b1;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_4 = 32'h00000000;
      if (execute_CsrPlugin_csr_3858) begin
         _zz_CsrPlugin_csrMapping_readDataInit_4[1 : 0] = 2'b10;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_5 = 32'h00000000;
      if (execute_CsrPlugin_csr_3859) begin
         _zz_CsrPlugin_csrMapping_readDataInit_5[1 : 0] = 2'b11;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_6 = 32'h00000000;
      if (execute_CsrPlugin_csr_769) begin
         _zz_CsrPlugin_csrMapping_readDataInit_6[31 : 30] = CsrPlugin_misa_base;
         _zz_CsrPlugin_csrMapping_readDataInit_6[25 : 0]  = CsrPlugin_misa_extensions;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_7 = 32'h00000000;
      if (execute_CsrPlugin_csr_836) begin
         _zz_CsrPlugin_csrMapping_readDataInit_7[11 : 11] = CsrPlugin_mip_MEIP;
         _zz_CsrPlugin_csrMapping_readDataInit_7[7 : 7]   = CsrPlugin_mip_MTIP;
         _zz_CsrPlugin_csrMapping_readDataInit_7[3 : 3]   = CsrPlugin_mip_MSIP;
         _zz_CsrPlugin_csrMapping_readDataInit_7[5 : 5]   = CsrPlugin_sip_STIP;
         _zz_CsrPlugin_csrMapping_readDataInit_7[1 : 1]   = CsrPlugin_sip_SSIP;
         _zz_CsrPlugin_csrMapping_readDataInit_7[9 : 9]   = CsrPlugin_sip_SEIP_OR;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_8 = 32'h00000000;
      if (execute_CsrPlugin_csr_772) begin
         _zz_CsrPlugin_csrMapping_readDataInit_8[11 : 11] = CsrPlugin_mie_MEIE;
         _zz_CsrPlugin_csrMapping_readDataInit_8[7 : 7]   = CsrPlugin_mie_MTIE;
         _zz_CsrPlugin_csrMapping_readDataInit_8[3 : 3]   = CsrPlugin_mie_MSIE;
         _zz_CsrPlugin_csrMapping_readDataInit_8[9 : 9]   = CsrPlugin_sie_SEIE;
         _zz_CsrPlugin_csrMapping_readDataInit_8[5 : 5]   = CsrPlugin_sie_STIE;
         _zz_CsrPlugin_csrMapping_readDataInit_8[1 : 1]   = CsrPlugin_sie_SSIE;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_9 = 32'h00000000;
      if (execute_CsrPlugin_csr_773) begin
         _zz_CsrPlugin_csrMapping_readDataInit_9[31 : 2] = CsrPlugin_mtvec_base;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_10 = 32'h00000000;
      if (execute_CsrPlugin_csr_833) begin
         _zz_CsrPlugin_csrMapping_readDataInit_10[31 : 0] = CsrPlugin_mepc;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_11 = 32'h00000000;
      if (execute_CsrPlugin_csr_832) begin
         _zz_CsrPlugin_csrMapping_readDataInit_11[31 : 0] = CsrPlugin_mscratch;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_12 = 32'h00000000;
      if (execute_CsrPlugin_csr_834) begin
         _zz_CsrPlugin_csrMapping_readDataInit_12[31 : 31] = CsrPlugin_mcause_interrupt;
         _zz_CsrPlugin_csrMapping_readDataInit_12[3 : 0]   = CsrPlugin_mcause_exceptionCode;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_13 = 32'h00000000;
      if (execute_CsrPlugin_csr_835) begin
         _zz_CsrPlugin_csrMapping_readDataInit_13[31 : 0] = CsrPlugin_mtval;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_14 = 32'h00000000;
      if (execute_CsrPlugin_csr_2816) begin
         _zz_CsrPlugin_csrMapping_readDataInit_14[31 : 0] = CsrPlugin_mcycle[31 : 0];
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_15 = 32'h00000000;
      if (execute_CsrPlugin_csr_2944) begin
         _zz_CsrPlugin_csrMapping_readDataInit_15[31 : 0] = CsrPlugin_mcycle[63 : 32];
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_16 = 32'h00000000;
      if (execute_CsrPlugin_csr_2818) begin
         _zz_CsrPlugin_csrMapping_readDataInit_16[31 : 0] = CsrPlugin_minstret[31 : 0];
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_17 = 32'h00000000;
      if (execute_CsrPlugin_csr_2946) begin
         _zz_CsrPlugin_csrMapping_readDataInit_17[31 : 0] = CsrPlugin_minstret[63 : 32];
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_18 = 32'h00000000;
      if (execute_CsrPlugin_csr_770) begin
         _zz_CsrPlugin_csrMapping_readDataInit_18[0 : 0]   = CsrPlugin_medeleg_IAM;
         _zz_CsrPlugin_csrMapping_readDataInit_18[1 : 1]   = CsrPlugin_medeleg_IAF;
         _zz_CsrPlugin_csrMapping_readDataInit_18[2 : 2]   = CsrPlugin_medeleg_II;
         _zz_CsrPlugin_csrMapping_readDataInit_18[3 : 3]   = CsrPlugin_medeleg_BP;
         _zz_CsrPlugin_csrMapping_readDataInit_18[4 : 4]   = CsrPlugin_medeleg_LAM;
         _zz_CsrPlugin_csrMapping_readDataInit_18[5 : 5]   = CsrPlugin_medeleg_LAF;
         _zz_CsrPlugin_csrMapping_readDataInit_18[6 : 6]   = CsrPlugin_medeleg_SAM;
         _zz_CsrPlugin_csrMapping_readDataInit_18[7 : 7]   = CsrPlugin_medeleg_SAF;
         _zz_CsrPlugin_csrMapping_readDataInit_18[8 : 8]   = CsrPlugin_medeleg_EU;
         _zz_CsrPlugin_csrMapping_readDataInit_18[9 : 9]   = CsrPlugin_medeleg_ES;
         _zz_CsrPlugin_csrMapping_readDataInit_18[12 : 12] = CsrPlugin_medeleg_IPF;
         _zz_CsrPlugin_csrMapping_readDataInit_18[13 : 13] = CsrPlugin_medeleg_LPF;
         _zz_CsrPlugin_csrMapping_readDataInit_18[15 : 15] = CsrPlugin_medeleg_SPF;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_19 = 32'h00000000;
      if (execute_CsrPlugin_csr_771) begin
         _zz_CsrPlugin_csrMapping_readDataInit_19[9 : 9] = CsrPlugin_mideleg_SE;
         _zz_CsrPlugin_csrMapping_readDataInit_19[5 : 5] = CsrPlugin_mideleg_ST;
         _zz_CsrPlugin_csrMapping_readDataInit_19[1 : 1] = CsrPlugin_mideleg_SS;
      end
   end

   assign when_CsrPlugin_l1076 = ((CsrPlugin_privilege < 2'b11) && (!CsrPlugin_mcounteren_CY));
   assign when_CsrPlugin_l1077 = ((CsrPlugin_privilege < 2'b01) && (!CsrPlugin_scounteren_CY));
   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_20 = 32'h00000000;
      if (execute_CsrPlugin_csr_3072) begin
         _zz_CsrPlugin_csrMapping_readDataInit_20[31 : 0] = CsrPlugin_mcycle[31 : 0];
      end
   end

   assign when_CsrPlugin_l1076_1 = ((CsrPlugin_privilege < 2'b11) && (!CsrPlugin_mcounteren_CY));
   assign when_CsrPlugin_l1077_1 = ((CsrPlugin_privilege < 2'b01) && (!CsrPlugin_scounteren_CY));
   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_21 = 32'h00000000;
      if (execute_CsrPlugin_csr_3200) begin
         _zz_CsrPlugin_csrMapping_readDataInit_21[31 : 0] = CsrPlugin_mcycle[63 : 32];
      end
   end

   assign when_CsrPlugin_l1076_2 = ((CsrPlugin_privilege < 2'b11) && (!CsrPlugin_mcounteren_IR));
   assign when_CsrPlugin_l1077_2 = ((CsrPlugin_privilege < 2'b01) && (!CsrPlugin_scounteren_IR));
   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_22 = 32'h00000000;
      if (execute_CsrPlugin_csr_3074) begin
         _zz_CsrPlugin_csrMapping_readDataInit_22[31 : 0] = CsrPlugin_minstret[31 : 0];
      end
   end

   assign when_CsrPlugin_l1076_3 = ((CsrPlugin_privilege < 2'b11) && (!CsrPlugin_mcounteren_IR));
   assign when_CsrPlugin_l1077_3 = ((CsrPlugin_privilege < 2'b01) && (!CsrPlugin_scounteren_IR));
   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_23 = 32'h00000000;
      if (execute_CsrPlugin_csr_3202) begin
         _zz_CsrPlugin_csrMapping_readDataInit_23[31 : 0] = CsrPlugin_minstret[63 : 32];
      end
   end

   assign when_CsrPlugin_l1076_4 = ((CsrPlugin_privilege < 2'b11) && (!CsrPlugin_mcounteren_TM));
   assign when_CsrPlugin_l1077_4 = ((CsrPlugin_privilege < 2'b01) && (!CsrPlugin_scounteren_TM));
   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_24 = 32'h00000000;
      if (execute_CsrPlugin_csr_3073) begin
         _zz_CsrPlugin_csrMapping_readDataInit_24[31 : 0] = utime[31 : 0];
      end
   end

   assign when_CsrPlugin_l1076_5 = ((CsrPlugin_privilege < 2'b11) && (!CsrPlugin_mcounteren_TM));
   assign when_CsrPlugin_l1077_5 = ((CsrPlugin_privilege < 2'b01) && (!CsrPlugin_scounteren_TM));
   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_25 = 32'h00000000;
      if (execute_CsrPlugin_csr_3201) begin
         _zz_CsrPlugin_csrMapping_readDataInit_25[31 : 0] = utime[63 : 32];
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_26 = 32'h00000000;
      if (execute_CsrPlugin_csr_774) begin
         _zz_CsrPlugin_csrMapping_readDataInit_26[0 : 0] = CsrPlugin_mcounteren_CY;
         _zz_CsrPlugin_csrMapping_readDataInit_26[1 : 1] = CsrPlugin_mcounteren_TM;
         _zz_CsrPlugin_csrMapping_readDataInit_26[2 : 2] = CsrPlugin_mcounteren_IR;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_27 = 32'h00000000;
      if (execute_CsrPlugin_csr_262) begin
         _zz_CsrPlugin_csrMapping_readDataInit_27[0 : 0] = CsrPlugin_scounteren_CY;
         _zz_CsrPlugin_csrMapping_readDataInit_27[1 : 1] = CsrPlugin_scounteren_TM;
         _zz_CsrPlugin_csrMapping_readDataInit_27[2 : 2] = CsrPlugin_scounteren_IR;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_28 = 32'h00000000;
      if (execute_CsrPlugin_csr_324) begin
         _zz_CsrPlugin_csrMapping_readDataInit_28[5 : 5] = CsrPlugin_sip_STIP;
         _zz_CsrPlugin_csrMapping_readDataInit_28[1 : 1] = CsrPlugin_sip_SSIP;
         _zz_CsrPlugin_csrMapping_readDataInit_28[9 : 9] = CsrPlugin_sip_SEIP_OR;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_29 = 32'h00000000;
      if (execute_CsrPlugin_csr_260) begin
         _zz_CsrPlugin_csrMapping_readDataInit_29[9 : 9] = CsrPlugin_sie_SEIE;
         _zz_CsrPlugin_csrMapping_readDataInit_29[5 : 5] = CsrPlugin_sie_STIE;
         _zz_CsrPlugin_csrMapping_readDataInit_29[1 : 1] = CsrPlugin_sie_SSIE;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_30 = 32'h00000000;
      if (execute_CsrPlugin_csr_261) begin
         _zz_CsrPlugin_csrMapping_readDataInit_30[31 : 2] = CsrPlugin_stvec_base;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_31 = 32'h00000000;
      if (execute_CsrPlugin_csr_321) begin
         _zz_CsrPlugin_csrMapping_readDataInit_31[31 : 0] = CsrPlugin_sepc;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_32 = 32'h00000000;
      if (execute_CsrPlugin_csr_320) begin
         _zz_CsrPlugin_csrMapping_readDataInit_32[31 : 0] = CsrPlugin_sscratch;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_33 = 32'h00000000;
      if (execute_CsrPlugin_csr_322) begin
         _zz_CsrPlugin_csrMapping_readDataInit_33[31 : 31] = CsrPlugin_scause_interrupt;
         _zz_CsrPlugin_csrMapping_readDataInit_33[3 : 0]   = CsrPlugin_scause_exceptionCode;
      end
   end

   always @(*) begin
      _zz_CsrPlugin_csrMapping_readDataInit_34 = 32'h00000000;
      if (execute_CsrPlugin_csr_323) begin
         _zz_CsrPlugin_csrMapping_readDataInit_34[31 : 0] = CsrPlugin_stval;
      end
   end

   assign CsrPlugin_csrMapping_readDataInit = (((((_zz_CsrPlugin_csrMapping_readDataInit_35 | _zz_CsrPlugin_csrMapping_readDataInit_36) | (_zz_CsrPlugin_csrMapping_readDataInit_37 | _zz_CsrPlugin_csrMapping_readDataInit_38)) | ((_zz_CsrPlugin_csrMapping_readDataInit_40 | _zz_CsrPlugin_csrMapping_readDataInit_41) | (_zz_CsrPlugin_csrMapping_readDataInit_42 | _zz_CsrPlugin_csrMapping_readDataInit_43))) | (((_zz_CsrPlugin_csrMapping_readDataInit_44 | _zz_CsrPlugin_csrMapping_readDataInit_45) | (_zz_CsrPlugin_csrMapping_readDataInit_46 | _zz_CsrPlugin_csrMapping_readDataInit_47)) | ((_zz_CsrPlugin_csrMapping_readDataInit_48 | _zz_CsrPlugin_csrMapping_readDataInit_49) | (_zz_CsrPlugin_csrMapping_readDataInit_50 | _zz_CsrPlugin_csrMapping_readDataInit_51)))) | ((_zz_CsrPlugin_csrMapping_readDataInit_31 | _zz_CsrPlugin_csrMapping_readDataInit_32) | (_zz_CsrPlugin_csrMapping_readDataInit_33 | _zz_CsrPlugin_csrMapping_readDataInit_34)));
   assign when_CsrPlugin_l1702 = ((execute_arbitration_isValid && execute_IS_CSR) && (({execute_CsrPlugin_csrAddress[11 : 2],2'b00} == 12'h3a0) || ({execute_CsrPlugin_csrAddress[11 : 4],4'b0000} == 12'h3b0)));
   assign _zz_when_CsrPlugin_l1709 = (execute_CsrPlugin_csrAddress & 12'hf60);
   assign when_CsrPlugin_l1709 = (((execute_arbitration_isValid && execute_IS_CSR) && (5'h03 <= execute_CsrPlugin_csrAddress[4 : 0])) && (((_zz_when_CsrPlugin_l1709 == 12'hb00) || (((_zz_when_CsrPlugin_l1709 == 12'hc00) && (! execute_CsrPlugin_writeInstruction)) && (CsrPlugin_privilege == 2'b11))) || ((execute_CsrPlugin_csrAddress & 12'hfe0) == 12'h320)));
   always @(*) begin
      when_CsrPlugin_l1719 = CsrPlugin_csrMapping_doForceFailCsr;
      if (when_CsrPlugin_l1717) begin
         when_CsrPlugin_l1719 = 1'b1;
      end
   end

   assign when_CsrPlugin_l1717        = (CsrPlugin_privilege < execute_CsrPlugin_csrAddress[9 : 8]);
   assign when_CsrPlugin_l1725        = ((!execute_arbitration_isValid) || (!execute_IS_CSR));
   assign iBus_cmd_ready              = iBusAxi_arready;
   assign iBus_rsp_valid              = iBusAxi_rvalid;
   assign iBus_rsp_payload_data       = iBusAxi_rdata;
   assign iBus_rsp_payload_error      = (!(iBusAxi_rresp == 2'b00));
   assign iBusAxi_arvalid             = iBus_cmd_valid;
   assign iBusAxi_araddr              = iBus_cmd_payload_address;
   assign _zz_iBusAxi_arid[0 : 0]     = 1'b0;
   assign iBusAxi_arid                = _zz_iBusAxi_arid;
   assign _zz_iBusAxi_arregion[3 : 0] = 4'b0000;
   assign iBusAxi_arregion            = _zz_iBusAxi_arregion;
   assign iBusAxi_arlen               = 8'h0f;
   assign iBusAxi_arsize              = 3'b010;
   assign iBusAxi_arburst             = 2'b01;
   assign iBusAxi_arlock              = 1'b0;
   assign iBusAxi_arcache             = 4'b1111;
   assign iBusAxi_arqos               = 4'b0000;
   assign iBusAxi_arprot              = 3'b110;
   assign iBusAxi_rready              = 1'b1;
   assign dBus_cmd_fire               = (dBus_cmd_valid && dBus_cmd_ready);
   assign when_Utils_l659             = (dBus_cmd_fire && dBus_cmd_payload_wr);
   assign dbus_axi_b_fire             = (dbus_axi_b_valid && dbus_axi_b_ready);
   always @(*) begin
      _zz_when_Utils_l687 = 1'b0;
      if (when_Utils_l659) begin
         _zz_when_Utils_l687 = 1'b1;
      end
   end

   always @(*) begin
      _zz_when_Utils_l687_1 = 1'b0;
      if (dbus_axi_b_fire) begin
         _zz_when_Utils_l687_1 = 1'b1;
      end
   end

   assign when_Utils_l687 = (_zz_when_Utils_l687 && (!_zz_when_Utils_l687_1));
   always @(*) begin
      if (when_Utils_l687) begin
         _zz_dBus_cmd_ready_1 = 3'b001;
      end else begin
         if (when_Utils_l689) begin
            _zz_dBus_cmd_ready_1 = 3'b111;
         end else begin
            _zz_dBus_cmd_ready_1 = 3'b000;
         end
      end
   end

   assign when_Utils_l689 = ((!_zz_when_Utils_l687) && _zz_when_Utils_l687_1);
   assign _zz_dBus_cmd_ready_2 = (! (((_zz_dBus_cmd_ready != 3'b000) && (! dBus_cmd_payload_wr)) || (_zz_dBus_cmd_ready == 3'b111)));
   assign _zz_dbus_axi_arw_valid = (dBus_cmd_valid && _zz_dBus_cmd_ready_2);
   assign dBus_cmd_ready = (_zz_dBus_cmd_ready_3 && _zz_dBus_cmd_ready_2);
   assign _zz_dbus_axi_arw_payload_write = dBus_cmd_payload_wr;
   assign _zz_dbus_axi_w_payload_last = dBus_cmd_payload_last;
   always @(*) begin
      _zz_dBus_cmd_ready_3 = 1'b1;
      if (when_Stream_l998) begin
         _zz_dBus_cmd_ready_3 = 1'b0;
      end
      if (when_Stream_l998_1) begin
         _zz_dBus_cmd_ready_3 = 1'b0;
      end
   end

   assign when_Stream_l998         = ((!_zz_when_Stream_l998) && _zz_when_Stream_l998_2);
   assign when_Stream_l998_1       = ((!_zz_when_Stream_l998_1) && _zz_when_Stream_l998_3);
   assign _zz_dbus_axi_arw_valid_1 = (_zz_dbus_axi_arw_valid && _zz_when_Stream_l998_2);
   assign _zz_6                    = (_zz_dbus_axi_arw_valid_1 && _zz_when_Stream_l998);
   assign _zz_dbus_axi_w_valid     = (_zz_dbus_axi_arw_valid && _zz_when_Stream_l998_3);
   always @(*) begin
      _zz_dbus_axi_arw_valid_2 = _zz_dbus_axi_arw_valid_1;
      if (_zz_7) begin
         _zz_dbus_axi_arw_valid_2 = 1'b0;
      end
   end

   always @(*) begin
      _zz_when_Stream_l998 = dbus_axi_arw_ready;
      if (_zz_7) begin
         _zz_when_Stream_l998 = 1'b1;
      end
   end

   assign when_Stream_l439 = (!_zz_dbus_axi_arw_payload_write);
   always @(*) begin
      _zz_dbus_axi_w_valid_1 = _zz_dbus_axi_w_valid;
      if (when_Stream_l439) begin
         _zz_dbus_axi_w_valid_1 = 1'b0;
      end
   end

   always @(*) begin
      _zz_when_Stream_l998_1 = dbus_axi_w_ready;
      if (when_Stream_l439) begin
         _zz_when_Stream_l998_1 = 1'b1;
      end
   end

   assign dbus_axi_arw_valid = _zz_dbus_axi_arw_valid_2;
   assign dbus_axi_arw_payload_write = _zz_dbus_axi_arw_payload_write;
   assign dbus_axi_arw_payload_prot = 3'b010;
   assign dbus_axi_arw_payload_cache = 4'b1111;
   assign dbus_axi_arw_payload_size = 3'b010;
   assign dbus_axi_arw_payload_addr = dBus_cmd_payload_address;
   assign dbus_axi_arw_payload_len = {4'd0, _zz_dbus_axi_arw_payload_len};
   assign dbus_axi_w_valid = _zz_dbus_axi_w_valid_1;
   assign dbus_axi_w_payload_data = dBus_cmd_payload_data;
   assign dbus_axi_w_payload_strb = dBus_cmd_payload_mask;
   assign dbus_axi_w_payload_last = _zz_dbus_axi_w_payload_last;
   assign dBus_rsp_valid = dbus_axi_r_valid;
   assign dBus_rsp_payload_error = (!(dbus_axi_r_payload_resp == 2'b00));
   assign dBus_rsp_payload_data = dbus_axi_r_payload_data;
   assign dbus_axi_r_ready = 1'b1;
   assign dbus_axi_b_ready = 1'b1;
   assign dbus_axi_arw_ready = (dbus_axi_arw_payload_write ? dBusAxi_awready : dBusAxi_arready);
   assign dbus_axi_w_ready = dBusAxi_wready;
   assign dbus_axi_r_valid = dBusAxi_rvalid;
   assign dbus_axi_r_payload_data = dBusAxi_rdata;
   assign dbus_axi_r_payload_resp = dBusAxi_rresp;
   assign dbus_axi_r_payload_last = dBusAxi_rlast;
   assign dbus_axi_b_valid = dBusAxi_bvalid;
   assign dbus_axi_b_payload_resp = dBusAxi_bresp;
   assign dBusAxi_arvalid = (dbus_axi_arw_valid && (!dbus_axi_arw_payload_write));
   assign dBusAxi_araddr = dbus_axi_arw_payload_addr;
   assign _zz_dBusAxi_arid[0 : 0] = 1'b0;
   assign dBusAxi_arid = _zz_dBusAxi_arid;
   assign _zz_dBusAxi_arregion[3 : 0] = 4'b0000;
   assign dBusAxi_arregion = _zz_dBusAxi_arregion;
   assign dBusAxi_arlen = dbus_axi_arw_payload_len;
   assign dBusAxi_arsize = dbus_axi_arw_payload_size;
   assign dBusAxi_arburst = 2'b01;
   assign dBusAxi_arlock = 1'b0;
   assign dBusAxi_arcache = dbus_axi_arw_payload_cache;
   assign dBusAxi_arqos = 4'b0000;
   assign dBusAxi_arprot = dbus_axi_arw_payload_prot;
   assign dBusAxi_awvalid = (dbus_axi_arw_valid && dbus_axi_arw_payload_write);
   assign dBusAxi_awaddr = dbus_axi_arw_payload_addr;
   assign _zz_dBusAxi_awid[0 : 0] = 1'b0;
   assign dBusAxi_awid = _zz_dBusAxi_awid;
   assign _zz_dBusAxi_awregion[3 : 0] = 4'b0000;
   assign dBusAxi_awregion = _zz_dBusAxi_awregion;
   assign dBusAxi_awlen = dbus_axi_arw_payload_len;
   assign dBusAxi_awsize = dbus_axi_arw_payload_size;
   assign dBusAxi_awburst = 2'b01;
   assign dBusAxi_awlock = 1'b0;
   assign dBusAxi_awcache = dbus_axi_arw_payload_cache;
   assign dBusAxi_awqos = 4'b0000;
   assign dBusAxi_awprot = dbus_axi_arw_payload_prot;
   assign dBusAxi_wvalid = dbus_axi_w_valid;
   assign dBusAxi_wdata = dbus_axi_w_payload_data;
   assign dBusAxi_wstrb = dbus_axi_w_payload_strb;
   assign dBusAxi_wlast = dbus_axi_w_payload_last;
   assign dBusAxi_rready = dbus_axi_r_ready;
   assign dBusAxi_bready = dbus_axi_b_ready;
   assign timerInterrupt = clintCtrl_io_timerInterrupt[0];
   assign softwareInterrupt = clintCtrl_io_softwareInterrupt[0];
   assign externalInterrupt = plicCtrl_io_targets[0];
   assign externalInterruptS = plicCtrl_io_targets[1];
   assign utime = clintCtrl_io_time;
   always @(posedge clk or posedge reset) begin
      if (reset) begin
         IBusCachedPlugin_fetchPc_pcReg                             <= externalResetVector;
         IBusCachedPlugin_fetchPc_correctionReg                     <= 1'b0;
         IBusCachedPlugin_fetchPc_booted                            <= 1'b0;
         IBusCachedPlugin_fetchPc_inc                               <= 1'b0;
         IBusCachedPlugin_decodePc_pcReg                            <= externalResetVector;
         _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid_1        <= 1'b0;
         _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid <= 1'b0;
         IBusCachedPlugin_decompressor_bufferValid                  <= 1'b0;
         IBusCachedPlugin_decompressor_throw2BytesReg               <= 1'b0;
         _zz_IBusCachedPlugin_injector_decodeInput_valid            <= 1'b0;
         IBusCachedPlugin_injector_nextPcCalc_valids_0              <= 1'b0;
         IBusCachedPlugin_injector_nextPcCalc_valids_1              <= 1'b0;
         IBusCachedPlugin_injector_nextPcCalc_valids_2              <= 1'b0;
         IBusCachedPlugin_injector_nextPcCalc_valids_3              <= 1'b0;
         IBusCachedPlugin_rspCounter                                <= 32'h00000000;
         DBusCachedPlugin_rspCounter                                <= 32'h00000000;
         MmuPlugin_status_sum                                       <= 1'b0;
         MmuPlugin_status_mxr                                       <= 1'b0;
         MmuPlugin_status_mprv                                      <= 1'b0;
         MmuPlugin_satp_mode                                        <= 1'b0;
         MmuPlugin_ports_0_cache_0_valid                            <= 1'b0;
         MmuPlugin_ports_0_cache_1_valid                            <= 1'b0;
         MmuPlugin_ports_0_cache_2_valid                            <= 1'b0;
         MmuPlugin_ports_0_cache_3_valid                            <= 1'b0;
         MmuPlugin_ports_0_dirty                                    <= 1'b0;
         MmuPlugin_ports_0_entryToReplace_value                     <= 2'b00;
         MmuPlugin_ports_1_cache_0_valid                            <= 1'b0;
         MmuPlugin_ports_1_cache_1_valid                            <= 1'b0;
         MmuPlugin_ports_1_cache_2_valid                            <= 1'b0;
         MmuPlugin_ports_1_cache_3_valid                            <= 1'b0;
         MmuPlugin_ports_1_dirty                                    <= 1'b0;
         MmuPlugin_ports_1_entryToReplace_value                     <= 2'b00;
         MmuPlugin_shared_state_1                                   <= MmuPlugin_shared_State_IDLE;
         MmuPlugin_shared_dBusRspStaged_valid                       <= 1'b0;
         _zz_5                                                      <= 1'b1;
         memory_DivPlugin_div_counter_value                         <= 6'h00;
         HazardSimplePlugin_writeBackBuffer_valid                   <= 1'b0;
         _zz_CsrPlugin_privilege                                    <= 2'b11;
         CsrPlugin_mtvec_base                                       <= 30'h20000008;
         CsrPlugin_mstatus_MIE                                      <= 1'b0;
         CsrPlugin_mstatus_MPIE                                     <= 1'b0;
         CsrPlugin_mstatus_MPP                                      <= 2'b11;
         CsrPlugin_mie_MEIE                                         <= 1'b0;
         CsrPlugin_mie_MTIE                                         <= 1'b0;
         CsrPlugin_mie_MSIE                                         <= 1'b0;
         CsrPlugin_mcycle                                           <= 64'h0000000000000000;
         CsrPlugin_minstret                                         <= 64'h0000000000000000;
         CsrPlugin_medeleg_IAM                                      <= 1'b0;
         CsrPlugin_medeleg_IAF                                      <= 1'b0;
         CsrPlugin_medeleg_II                                       <= 1'b0;
         CsrPlugin_medeleg_BP                                       <= 1'b0;
         CsrPlugin_medeleg_LAM                                      <= 1'b0;
         CsrPlugin_medeleg_LAF                                      <= 1'b0;
         CsrPlugin_medeleg_SAM                                      <= 1'b0;
         CsrPlugin_medeleg_SAF                                      <= 1'b0;
         CsrPlugin_medeleg_EU                                       <= 1'b0;
         CsrPlugin_medeleg_ES                                       <= 1'b0;
         CsrPlugin_medeleg_IPF                                      <= 1'b0;
         CsrPlugin_medeleg_LPF                                      <= 1'b0;
         CsrPlugin_medeleg_SPF                                      <= 1'b0;
         CsrPlugin_mideleg_ST                                       <= 1'b0;
         CsrPlugin_mideleg_SE                                       <= 1'b0;
         CsrPlugin_mideleg_SS                                       <= 1'b0;
         CsrPlugin_mcounteren_IR                                    <= 1'b1;
         CsrPlugin_mcounteren_TM                                    <= 1'b1;
         CsrPlugin_mcounteren_CY                                    <= 1'b1;
         CsrPlugin_scounteren_IR                                    <= 1'b1;
         CsrPlugin_scounteren_TM                                    <= 1'b1;
         CsrPlugin_scounteren_CY                                    <= 1'b1;
         CsrPlugin_sstatus_SIE                                      <= 1'b0;
         CsrPlugin_sstatus_SPIE                                     <= 1'b0;
         CsrPlugin_sstatus_SPP                                      <= 1'b1;
         CsrPlugin_sip_SEIP_SOFT                                    <= 1'b0;
         CsrPlugin_sip_STIP                                         <= 1'b0;
         CsrPlugin_sip_SSIP                                         <= 1'b0;
         CsrPlugin_sie_SEIE                                         <= 1'b0;
         CsrPlugin_sie_STIE                                         <= 1'b0;
         CsrPlugin_sie_SSIE                                         <= 1'b0;
         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_decode     <= 1'b0;
         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_execute    <= 1'b0;
         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_memory     <= 1'b0;
         CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_writeBack  <= 1'b0;
         CsrPlugin_interrupt_valid                                  <= 1'b0;
         CsrPlugin_lastStageWasWfi                                  <= 1'b0;
         CsrPlugin_pipelineLiberator_pcValids_0                     <= 1'b0;
         CsrPlugin_pipelineLiberator_pcValids_1                     <= 1'b0;
         CsrPlugin_pipelineLiberator_pcValids_2                     <= 1'b0;
         CsrPlugin_hadException                                     <= 1'b0;
         execute_CsrPlugin_wfiWake                                  <= 1'b0;
         execute_arbitration_isValid                                <= 1'b0;
         memory_arbitration_isValid                                 <= 1'b0;
         writeBack_arbitration_isValid                              <= 1'b0;
         execute_to_memory_IS_DBUS_SHARING                          <= 1'b0;
         memory_to_writeBack_IS_DBUS_SHARING                        <= 1'b0;
         _zz_dBus_cmd_ready                                         <= 3'b000;
         _zz_when_Stream_l998_2                                     <= 1'b1;
         _zz_when_Stream_l998_3                                     <= 1'b1;
         _zz_7                                                      <= 1'b0;
      end else begin
         if (IBusCachedPlugin_fetchPc_correction) begin
            IBusCachedPlugin_fetchPc_correctionReg <= 1'b1;
         end
         if (IBusCachedPlugin_fetchPc_output_fire) begin
            IBusCachedPlugin_fetchPc_correctionReg <= 1'b0;
         end
         IBusCachedPlugin_fetchPc_booted <= 1'b1;
         if (when_Fetcher_l133) begin
            IBusCachedPlugin_fetchPc_inc <= 1'b0;
         end
         if (IBusCachedPlugin_fetchPc_output_fire) begin
            IBusCachedPlugin_fetchPc_inc <= 1'b1;
         end
         if (when_Fetcher_l133_1) begin
            IBusCachedPlugin_fetchPc_inc <= 1'b0;
         end
         if (when_Fetcher_l160) begin
            IBusCachedPlugin_fetchPc_pcReg <= IBusCachedPlugin_fetchPc_pc;
         end
         if (when_Fetcher_l182) begin
            IBusCachedPlugin_decodePc_pcReg <= IBusCachedPlugin_decodePc_pcPlus;
         end
         if (when_Fetcher_l194) begin
            IBusCachedPlugin_decodePc_pcReg <= IBusCachedPlugin_jump_pcLoad_payload;
         end
         if (IBusCachedPlugin_iBusRsp_flush) begin
            _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid_1 <= 1'b0;
         end
         if (_zz_IBusCachedPlugin_iBusRsp_stages_0_output_ready) begin
            _zz_IBusCachedPlugin_iBusRsp_stages_1_input_valid_1 <= (IBusCachedPlugin_iBusRsp_stages_0_output_valid && (! 1'b0));
         end
         if (IBusCachedPlugin_iBusRsp_flush) begin
            _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid <= 1'b0;
         end
         if (IBusCachedPlugin_iBusRsp_stages_1_output_ready) begin
            _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_valid <= (IBusCachedPlugin_iBusRsp_stages_1_output_valid && (! IBusCachedPlugin_iBusRsp_flush));
         end
         if (IBusCachedPlugin_decompressor_output_fire) begin
            IBusCachedPlugin_decompressor_throw2BytesReg <= ((((! IBusCachedPlugin_decompressor_unaligned) && IBusCachedPlugin_decompressor_isInputLowRvc) && IBusCachedPlugin_decompressor_isInputHighRvc) || (IBusCachedPlugin_decompressor_bufferValid && IBusCachedPlugin_decompressor_isInputHighRvc));
         end
         if (when_Fetcher_l285) begin
            IBusCachedPlugin_decompressor_bufferValid <= 1'b0;
         end
         if (when_Fetcher_l288) begin
            if (IBusCachedPlugin_decompressor_bufferFill) begin
               IBusCachedPlugin_decompressor_bufferValid <= 1'b1;
            end
         end
         if (when_Fetcher_l293) begin
            IBusCachedPlugin_decompressor_throw2BytesReg <= 1'b0;
            IBusCachedPlugin_decompressor_bufferValid    <= 1'b0;
         end
         if (decode_arbitration_removeIt) begin
            _zz_IBusCachedPlugin_injector_decodeInput_valid <= 1'b0;
         end
         if (IBusCachedPlugin_decompressor_output_ready) begin
            _zz_IBusCachedPlugin_injector_decodeInput_valid <= (IBusCachedPlugin_decompressor_output_valid && (! IBusCachedPlugin_externalFlush));
         end
         if (when_Fetcher_l331) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_0 <= 1'b1;
         end
         if (IBusCachedPlugin_decodePc_flushed) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_0 <= 1'b0;
         end
         if (when_Fetcher_l331_1) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_1 <= IBusCachedPlugin_injector_nextPcCalc_valids_0;
         end
         if (IBusCachedPlugin_decodePc_flushed) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_1 <= 1'b0;
         end
         if (when_Fetcher_l331_2) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_2 <= IBusCachedPlugin_injector_nextPcCalc_valids_1;
         end
         if (IBusCachedPlugin_decodePc_flushed) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_2 <= 1'b0;
         end
         if (when_Fetcher_l331_3) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_3 <= IBusCachedPlugin_injector_nextPcCalc_valids_2;
         end
         if (IBusCachedPlugin_decodePc_flushed) begin
            IBusCachedPlugin_injector_nextPcCalc_valids_3 <= 1'b0;
         end
         if (iBus_rsp_valid) begin
            IBusCachedPlugin_rspCounter <= (IBusCachedPlugin_rspCounter + 32'h00000001);
         end
         if (dBus_rsp_valid) begin
            DBusCachedPlugin_rspCounter <= (DBusCachedPlugin_rspCounter + 32'h00000001);
         end
         if (CsrPlugin_xretAwayFromMachine) begin
            MmuPlugin_status_mprv <= 1'b0;
         end
         if (when_MmuPlugin_l129) begin
            MmuPlugin_ports_0_dirty <= 1'b0;
         end
         MmuPlugin_ports_0_entryToReplace_value <= MmuPlugin_ports_0_entryToReplace_valueNext;
         if (contextSwitching) begin
            if (MmuPlugin_ports_0_cache_0_exception) begin
               MmuPlugin_ports_0_cache_0_valid <= 1'b0;
            end
            if (MmuPlugin_ports_0_cache_1_exception) begin
               MmuPlugin_ports_0_cache_1_valid <= 1'b0;
            end
            if (MmuPlugin_ports_0_cache_2_exception) begin
               MmuPlugin_ports_0_cache_2_valid <= 1'b0;
            end
            if (MmuPlugin_ports_0_cache_3_exception) begin
               MmuPlugin_ports_0_cache_3_valid <= 1'b0;
            end
         end
         if (when_MmuPlugin_l129_1) begin
            MmuPlugin_ports_1_dirty <= 1'b0;
         end
         MmuPlugin_ports_1_entryToReplace_value <= MmuPlugin_ports_1_entryToReplace_valueNext;
         if (contextSwitching) begin
            if (MmuPlugin_ports_1_cache_0_exception) begin
               MmuPlugin_ports_1_cache_0_valid <= 1'b0;
            end
            if (MmuPlugin_ports_1_cache_1_exception) begin
               MmuPlugin_ports_1_cache_1_valid <= 1'b0;
            end
            if (MmuPlugin_ports_1_cache_2_exception) begin
               MmuPlugin_ports_1_cache_2_valid <= 1'b0;
            end
            if (MmuPlugin_ports_1_cache_3_exception) begin
               MmuPlugin_ports_1_cache_3_valid <= 1'b0;
            end
         end
         MmuPlugin_shared_dBusRspStaged_valid <= MmuPlugin_dBusAccess_rsp_valid;
         case (MmuPlugin_shared_state_1)
            MmuPlugin_shared_State_IDLE: begin
               if (when_MmuPlugin_l246) begin
                  MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_L1_CMD;
               end
            end
            MmuPlugin_shared_State_L1_CMD: begin
               if (MmuPlugin_dBusAccess_cmd_ready) begin
                  MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_L1_RSP;
               end
            end
            MmuPlugin_shared_State_L1_RSP: begin
               if (MmuPlugin_shared_dBusRspStaged_valid) begin
                  MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_L0_CMD;
                  if (when_MmuPlugin_l273) begin
                     MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_IDLE;
                  end
                  if (MmuPlugin_shared_dBusRspStaged_payload_redo) begin
                     MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_L1_CMD;
                  end
               end
            end
            MmuPlugin_shared_State_L0_CMD: begin
               if (MmuPlugin_dBusAccess_cmd_ready) begin
                  MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_L0_RSP;
               end
            end
            default: begin
               if (MmuPlugin_shared_dBusRspStaged_valid) begin
                  MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_IDLE;
                  if (MmuPlugin_shared_dBusRspStaged_payload_redo) begin
                     MmuPlugin_shared_state_1 <= MmuPlugin_shared_State_L0_CMD;
                  end
               end
            end
         endcase
         if (when_MmuPlugin_l302) begin
            if (when_MmuPlugin_l304) begin
               MmuPlugin_ports_0_dirty <= 1'b1;
               if (when_MmuPlugin_l310) begin
                  MmuPlugin_ports_0_cache_0_valid <= 1'b1;
               end
               if (when_MmuPlugin_l310_1) begin
                  MmuPlugin_ports_0_cache_1_valid <= 1'b1;
               end
               if (when_MmuPlugin_l310_2) begin
                  MmuPlugin_ports_0_cache_2_valid <= 1'b1;
               end
               if (when_MmuPlugin_l310_3) begin
                  MmuPlugin_ports_0_cache_3_valid <= 1'b1;
               end
            end
            if (when_MmuPlugin_l304_1) begin
               MmuPlugin_ports_1_dirty <= 1'b1;
               if (when_MmuPlugin_l310_4) begin
                  MmuPlugin_ports_1_cache_0_valid <= 1'b1;
               end
               if (when_MmuPlugin_l310_5) begin
                  MmuPlugin_ports_1_cache_1_valid <= 1'b1;
               end
               if (when_MmuPlugin_l310_6) begin
                  MmuPlugin_ports_1_cache_2_valid <= 1'b1;
               end
               if (when_MmuPlugin_l310_7) begin
                  MmuPlugin_ports_1_cache_3_valid <= 1'b1;
               end
            end
         end
         if (when_MmuPlugin_l334) begin
            MmuPlugin_ports_0_cache_0_valid <= 1'b0;
            MmuPlugin_ports_0_cache_1_valid <= 1'b0;
            MmuPlugin_ports_0_cache_2_valid <= 1'b0;
            MmuPlugin_ports_0_cache_3_valid <= 1'b0;
            MmuPlugin_ports_1_cache_0_valid <= 1'b0;
            MmuPlugin_ports_1_cache_1_valid <= 1'b0;
            MmuPlugin_ports_1_cache_2_valid <= 1'b0;
            MmuPlugin_ports_1_cache_3_valid <= 1'b0;
         end
         _zz_5                                    <= 1'b0;
         memory_DivPlugin_div_counter_value       <= memory_DivPlugin_div_counter_valueNext;
         HazardSimplePlugin_writeBackBuffer_valid <= HazardSimplePlugin_writeBackWrites_valid;
         CsrPlugin_mcycle                         <= (CsrPlugin_mcycle + 64'h0000000000000001);
         if (writeBack_arbitration_isFiring) begin
            CsrPlugin_minstret <= (CsrPlugin_minstret + 64'h0000000000000001);
         end
         if (when_CsrPlugin_l1259) begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_decode <= 1'b0;
         end else begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_decode <= CsrPlugin_exceptionPortCtrl_exceptionValids_decode;
         end
         if (when_CsrPlugin_l1259_1) begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_execute <= (CsrPlugin_exceptionPortCtrl_exceptionValids_decode && (! decode_arbitration_isStuck));
         end else begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_execute <= CsrPlugin_exceptionPortCtrl_exceptionValids_execute;
         end
         if (when_CsrPlugin_l1259_2) begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_memory <= (CsrPlugin_exceptionPortCtrl_exceptionValids_execute && (! execute_arbitration_isStuck));
         end else begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_memory <= CsrPlugin_exceptionPortCtrl_exceptionValids_memory;
         end
         if (when_CsrPlugin_l1259_3) begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_writeBack <= (CsrPlugin_exceptionPortCtrl_exceptionValids_memory && (! memory_arbitration_isStuck));
         end else begin
            CsrPlugin_exceptionPortCtrl_exceptionValidsRegs_writeBack <= 1'b0;
         end
         CsrPlugin_interrupt_valid <= 1'b0;
         if (when_CsrPlugin_l1296) begin
            if (when_CsrPlugin_l1302) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
            if (when_CsrPlugin_l1302_1) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
            if (when_CsrPlugin_l1302_2) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
         end
         if (when_CsrPlugin_l1296_1) begin
            if (when_CsrPlugin_l1302_3) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
            if (when_CsrPlugin_l1302_4) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
            if (when_CsrPlugin_l1302_5) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
            if (when_CsrPlugin_l1302_6) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
            if (when_CsrPlugin_l1302_7) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
            if (when_CsrPlugin_l1302_8) begin
               CsrPlugin_interrupt_valid <= 1'b1;
            end
         end
         CsrPlugin_lastStageWasWfi <= (writeBack_arbitration_isFiring && (writeBack_ENV_CTRL == EnvCtrlEnum_WFI));
         if (CsrPlugin_pipelineLiberator_active) begin
            if (when_CsrPlugin_l1335) begin
               CsrPlugin_pipelineLiberator_pcValids_0 <= 1'b1;
            end
            if (when_CsrPlugin_l1335_1) begin
               CsrPlugin_pipelineLiberator_pcValids_1 <= CsrPlugin_pipelineLiberator_pcValids_0;
            end
            if (when_CsrPlugin_l1335_2) begin
               CsrPlugin_pipelineLiberator_pcValids_2 <= CsrPlugin_pipelineLiberator_pcValids_1;
            end
         end
         if (when_CsrPlugin_l1340) begin
            CsrPlugin_pipelineLiberator_pcValids_0 <= 1'b0;
            CsrPlugin_pipelineLiberator_pcValids_1 <= 1'b0;
            CsrPlugin_pipelineLiberator_pcValids_2 <= 1'b0;
         end
         if (CsrPlugin_interruptJump) begin
            CsrPlugin_interrupt_valid <= 1'b0;
         end
         CsrPlugin_hadException <= CsrPlugin_exception;
         if (when_CsrPlugin_l1390) begin
            if (when_CsrPlugin_l1398) begin
               _zz_CsrPlugin_privilege <= CsrPlugin_targetPrivilege;
               case (CsrPlugin_targetPrivilege)
                  2'b01: begin
                     CsrPlugin_sstatus_SIE  <= 1'b0;
                     CsrPlugin_sstatus_SPIE <= CsrPlugin_sstatus_SIE;
                     CsrPlugin_sstatus_SPP  <= CsrPlugin_privilege[0 : 0];
                  end
                  2'b11: begin
                     CsrPlugin_mstatus_MIE  <= 1'b0;
                     CsrPlugin_mstatus_MPIE <= CsrPlugin_mstatus_MIE;
                     CsrPlugin_mstatus_MPP  <= CsrPlugin_privilege;
                  end
                  default: begin
                  end
               endcase
            end
         end
         if (when_CsrPlugin_l1456) begin
            case (switch_CsrPlugin_l1460)
               2'b11: begin
                  CsrPlugin_mstatus_MPP   <= 2'b00;
                  CsrPlugin_mstatus_MIE   <= CsrPlugin_mstatus_MPIE;
                  CsrPlugin_mstatus_MPIE  <= 1'b1;
                  _zz_CsrPlugin_privilege <= CsrPlugin_mstatus_MPP;
               end
               2'b01: begin
                  CsrPlugin_sstatus_SPP   <= 1'b0;
                  CsrPlugin_sstatus_SIE   <= CsrPlugin_sstatus_SPIE;
                  CsrPlugin_sstatus_SPIE  <= 1'b1;
                  _zz_CsrPlugin_privilege <= {1'b0, CsrPlugin_sstatus_SPP};
               end
               default: begin
               end
            endcase
         end
         execute_CsrPlugin_wfiWake <= (({_zz_when_CsrPlugin_l1302_5,{_zz_when_CsrPlugin_l1302_4,{_zz_when_CsrPlugin_l1302_3,{_zz_when_CsrPlugin_l1302_2,{_zz_when_CsrPlugin_l1302_1,_zz_when_CsrPlugin_l1302}}}}} != 6'h00) || CsrPlugin_thirdPartyWake);
         if (when_Pipeline_l124_57) begin
            execute_to_memory_IS_DBUS_SHARING <= execute_IS_DBUS_SHARING;
         end
         if (when_Pipeline_l124_58) begin
            memory_to_writeBack_IS_DBUS_SHARING <= memory_IS_DBUS_SHARING;
         end
         if (when_Pipeline_l151) begin
            execute_arbitration_isValid <= 1'b0;
         end
         if (when_Pipeline_l154) begin
            execute_arbitration_isValid <= decode_arbitration_isValid;
         end
         if (when_Pipeline_l151_1) begin
            memory_arbitration_isValid <= 1'b0;
         end
         if (when_Pipeline_l154_1) begin
            memory_arbitration_isValid <= execute_arbitration_isValid;
         end
         if (when_Pipeline_l151_2) begin
            writeBack_arbitration_isValid <= 1'b0;
         end
         if (when_Pipeline_l154_2) begin
            writeBack_arbitration_isValid <= memory_arbitration_isValid;
         end
         if (MmuPlugin_dBusAccess_rsp_valid) begin
            memory_to_writeBack_IS_DBUS_SHARING <= 1'b0;
         end
         if (MmuPlugin_dBusAccess_rsp_valid) begin
            memory_to_writeBack_IS_DBUS_SHARING <= 1'b0;
         end
         if (execute_CsrPlugin_csr_768) begin
            if (execute_CsrPlugin_writeEnable) begin
               MmuPlugin_status_mxr   <= CsrPlugin_csrMapping_writeDataSignal[19];
               MmuPlugin_status_sum   <= CsrPlugin_csrMapping_writeDataSignal[18];
               MmuPlugin_status_mprv  <= CsrPlugin_csrMapping_writeDataSignal[17];
               CsrPlugin_mstatus_MPIE <= CsrPlugin_csrMapping_writeDataSignal[7];
               CsrPlugin_mstatus_MIE  <= CsrPlugin_csrMapping_writeDataSignal[3];
               case (switch_CsrPlugin_l1031)
                  2'b11: begin
                     CsrPlugin_mstatus_MPP <= 2'b11;
                  end
                  2'b01: begin
                     CsrPlugin_mstatus_MPP <= 2'b01;
                  end
                  2'b00: begin
                     CsrPlugin_mstatus_MPP <= 2'b00;
                  end
                  default: begin
                  end
               endcase
               CsrPlugin_sstatus_SPP  <= CsrPlugin_csrMapping_writeDataSignal[8 : 8];
               CsrPlugin_sstatus_SPIE <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_sstatus_SIE  <= CsrPlugin_csrMapping_writeDataSignal[1];
            end
         end
         if (execute_CsrPlugin_csr_256) begin
            if (execute_CsrPlugin_writeEnable) begin
               MmuPlugin_status_mxr   <= CsrPlugin_csrMapping_writeDataSignal[19];
               MmuPlugin_status_sum   <= CsrPlugin_csrMapping_writeDataSignal[18];
               MmuPlugin_status_mprv  <= CsrPlugin_csrMapping_writeDataSignal[17];
               CsrPlugin_sstatus_SPP  <= CsrPlugin_csrMapping_writeDataSignal[8 : 8];
               CsrPlugin_sstatus_SPIE <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_sstatus_SIE  <= CsrPlugin_csrMapping_writeDataSignal[1];
            end
         end
         if (execute_CsrPlugin_csr_384) begin
            if (execute_CsrPlugin_writeEnable) begin
               MmuPlugin_satp_mode             <= CsrPlugin_csrMapping_writeDataSignal[31];
               MmuPlugin_ports_0_cache_0_valid <= 1'b0;
               MmuPlugin_ports_0_cache_1_valid <= 1'b0;
               MmuPlugin_ports_0_cache_2_valid <= 1'b0;
               MmuPlugin_ports_0_cache_3_valid <= 1'b0;
               MmuPlugin_ports_1_cache_0_valid <= 1'b0;
               MmuPlugin_ports_1_cache_1_valid <= 1'b0;
               MmuPlugin_ports_1_cache_2_valid <= 1'b0;
               MmuPlugin_ports_1_cache_3_valid <= 1'b0;
            end
         end
         if (execute_CsrPlugin_csr_836) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_sip_STIP      <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_sip_SSIP      <= CsrPlugin_csrMapping_writeDataSignal[1];
               CsrPlugin_sip_SEIP_SOFT <= CsrPlugin_csrMapping_writeDataSignal[9];
            end
         end
         if (execute_CsrPlugin_csr_772) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_mie_MEIE <= CsrPlugin_csrMapping_writeDataSignal[11];
               CsrPlugin_mie_MTIE <= CsrPlugin_csrMapping_writeDataSignal[7];
               CsrPlugin_mie_MSIE <= CsrPlugin_csrMapping_writeDataSignal[3];
               CsrPlugin_sie_SEIE <= CsrPlugin_csrMapping_writeDataSignal[9];
               CsrPlugin_sie_STIE <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_sie_SSIE <= CsrPlugin_csrMapping_writeDataSignal[1];
            end
         end
         if (execute_CsrPlugin_csr_773) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_mtvec_base <= CsrPlugin_csrMapping_writeDataSignal[31 : 2];
            end
         end
         if (execute_CsrPlugin_csr_2816) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_mcycle[31 : 0] <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
            end
         end
         if (execute_CsrPlugin_csr_2944) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_mcycle[63 : 32] <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
            end
         end
         if (execute_CsrPlugin_csr_2818) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_minstret[31 : 0] <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
            end
         end
         if (execute_CsrPlugin_csr_2946) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_minstret[63 : 32] <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
            end
         end
         if (execute_CsrPlugin_csr_770) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_medeleg_IAM <= CsrPlugin_csrMapping_writeDataSignal[0];
               CsrPlugin_medeleg_IAF <= CsrPlugin_csrMapping_writeDataSignal[1];
               CsrPlugin_medeleg_II  <= CsrPlugin_csrMapping_writeDataSignal[2];
               CsrPlugin_medeleg_BP  <= CsrPlugin_csrMapping_writeDataSignal[3];
               CsrPlugin_medeleg_LAM <= CsrPlugin_csrMapping_writeDataSignal[4];
               CsrPlugin_medeleg_LAF <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_medeleg_SAM <= CsrPlugin_csrMapping_writeDataSignal[6];
               CsrPlugin_medeleg_SAF <= CsrPlugin_csrMapping_writeDataSignal[7];
               CsrPlugin_medeleg_EU  <= CsrPlugin_csrMapping_writeDataSignal[8];
               CsrPlugin_medeleg_ES  <= CsrPlugin_csrMapping_writeDataSignal[9];
               CsrPlugin_medeleg_IPF <= CsrPlugin_csrMapping_writeDataSignal[12];
               CsrPlugin_medeleg_LPF <= CsrPlugin_csrMapping_writeDataSignal[13];
               CsrPlugin_medeleg_SPF <= CsrPlugin_csrMapping_writeDataSignal[15];
            end
         end
         if (execute_CsrPlugin_csr_771) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_mideleg_SE <= CsrPlugin_csrMapping_writeDataSignal[9];
               CsrPlugin_mideleg_ST <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_mideleg_SS <= CsrPlugin_csrMapping_writeDataSignal[1];
            end
         end
         if (execute_CsrPlugin_csr_774) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_mcounteren_CY <= CsrPlugin_csrMapping_writeDataSignal[0];
               CsrPlugin_mcounteren_TM <= CsrPlugin_csrMapping_writeDataSignal[1];
               CsrPlugin_mcounteren_IR <= CsrPlugin_csrMapping_writeDataSignal[2];
            end
         end
         if (execute_CsrPlugin_csr_262) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_scounteren_CY <= CsrPlugin_csrMapping_writeDataSignal[0];
               CsrPlugin_scounteren_TM <= CsrPlugin_csrMapping_writeDataSignal[1];
               CsrPlugin_scounteren_IR <= CsrPlugin_csrMapping_writeDataSignal[2];
            end
         end
         if (execute_CsrPlugin_csr_324) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_sip_STIP      <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_sip_SSIP      <= CsrPlugin_csrMapping_writeDataSignal[1];
               CsrPlugin_sip_SEIP_SOFT <= CsrPlugin_csrMapping_writeDataSignal[9];
            end
         end
         if (execute_CsrPlugin_csr_260) begin
            if (execute_CsrPlugin_writeEnable) begin
               CsrPlugin_sie_SEIE <= CsrPlugin_csrMapping_writeDataSignal[9];
               CsrPlugin_sie_STIE <= CsrPlugin_csrMapping_writeDataSignal[5];
               CsrPlugin_sie_SSIE <= CsrPlugin_csrMapping_writeDataSignal[1];
            end
         end
         _zz_dBus_cmd_ready <= (_zz_dBus_cmd_ready + _zz_dBus_cmd_ready_1);
         if (_zz_6) begin
            _zz_when_Stream_l998_2 <= 1'b0;
         end
         if ((_zz_dbus_axi_w_valid && _zz_when_Stream_l998_1)) begin
            _zz_when_Stream_l998_3 <= 1'b0;
         end
         if (_zz_dBus_cmd_ready_3) begin
            _zz_when_Stream_l998_2 <= 1'b1;
            _zz_when_Stream_l998_3 <= 1'b1;
         end
         if (_zz_6) begin
            _zz_7 <= (!_zz_dbus_axi_w_payload_last);
         end
      end
   end

   always @(posedge clk) begin
      if (IBusCachedPlugin_iBusRsp_stages_1_output_ready) begin
         _zz_IBusCachedPlugin_iBusRsp_stages_1_output_m2sPipe_payload <= IBusCachedPlugin_iBusRsp_stages_1_output_payload;
      end
      if (IBusCachedPlugin_decompressor_input_valid) begin
         IBusCachedPlugin_decompressor_bufferValidLatch <= IBusCachedPlugin_decompressor_bufferValid;
      end
      if (IBusCachedPlugin_decompressor_input_valid) begin
         IBusCachedPlugin_decompressor_throw2BytesLatch <= IBusCachedPlugin_decompressor_throw2Bytes;
      end
      if (when_Fetcher_l288) begin
         IBusCachedPlugin_decompressor_bufferData <= IBusCachedPlugin_decompressor_input_payload_rsp_inst[31 : 16];
      end
      if (IBusCachedPlugin_decompressor_output_ready) begin
         _zz_IBusCachedPlugin_injector_decodeInput_payload_pc <= IBusCachedPlugin_decompressor_output_payload_pc;
         _zz_IBusCachedPlugin_injector_decodeInput_payload_rsp_error <= IBusCachedPlugin_decompressor_output_payload_rsp_error;
         _zz_IBusCachedPlugin_injector_decodeInput_payload_rsp_inst <= IBusCachedPlugin_decompressor_output_payload_rsp_inst;
         _zz_IBusCachedPlugin_injector_decodeInput_payload_isRvc <= IBusCachedPlugin_decompressor_output_payload_isRvc;
      end
      if (IBusCachedPlugin_injector_decodeInput_ready) begin
         IBusCachedPlugin_injector_formal_rawInDecode <= IBusCachedPlugin_decompressor_raw;
      end
      if (IBusCachedPlugin_iBusRsp_stages_1_input_ready) begin
         IBusCachedPlugin_s1_tightlyCoupledHit <= IBusCachedPlugin_s0_tightlyCoupledHit;
      end
      if (IBusCachedPlugin_iBusRsp_stages_2_input_ready) begin
         IBusCachedPlugin_s2_tightlyCoupledHit <= IBusCachedPlugin_s1_tightlyCoupledHit;
      end
      if (when_MmuPlugin_l136) begin
         MmuPlugin_ports_0_requireMmuLockup <= MmuPlugin_ports_0_requireMmuLockupCalc;
      end
      if (when_MmuPlugin_l136_1) begin
         MmuPlugin_ports_0_cacheHits <= MmuPlugin_ports_0_cacheHitsCalc;
      end
      if (when_MmuPlugin_l136_2) begin
         MmuPlugin_ports_1_requireMmuLockup <= MmuPlugin_ports_1_requireMmuLockupCalc;
      end
      if (when_MmuPlugin_l136_3) begin
         MmuPlugin_ports_1_cacheHits <= MmuPlugin_ports_1_cacheHitsCalc;
      end
      MmuPlugin_shared_dBusRspStaged_payload_data  <= MmuPlugin_dBusAccess_rsp_payload_data;
      MmuPlugin_shared_dBusRspStaged_payload_error <= MmuPlugin_dBusAccess_rsp_payload_error;
      MmuPlugin_shared_dBusRspStaged_payload_redo  <= MmuPlugin_dBusAccess_rsp_payload_redo;
      if (when_MmuPlugin_l234) begin
         MmuPlugin_shared_pteBuffer_V    <= MmuPlugin_shared_dBusRsp_pte_V;
         MmuPlugin_shared_pteBuffer_R    <= MmuPlugin_shared_dBusRsp_pte_R;
         MmuPlugin_shared_pteBuffer_W    <= MmuPlugin_shared_dBusRsp_pte_W;
         MmuPlugin_shared_pteBuffer_X    <= MmuPlugin_shared_dBusRsp_pte_X;
         MmuPlugin_shared_pteBuffer_U    <= MmuPlugin_shared_dBusRsp_pte_U;
         MmuPlugin_shared_pteBuffer_G    <= MmuPlugin_shared_dBusRsp_pte_G;
         MmuPlugin_shared_pteBuffer_A    <= MmuPlugin_shared_dBusRsp_pte_A;
         MmuPlugin_shared_pteBuffer_D    <= MmuPlugin_shared_dBusRsp_pte_D;
         MmuPlugin_shared_pteBuffer_RSW  <= MmuPlugin_shared_dBusRsp_pte_RSW;
         MmuPlugin_shared_pteBuffer_PPN0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
         MmuPlugin_shared_pteBuffer_PPN1 <= MmuPlugin_shared_dBusRsp_pte_PPN1;
      end
      case (MmuPlugin_shared_state_1)
         MmuPlugin_shared_State_IDLE: begin
            if (when_MmuPlugin_l246) begin
               MmuPlugin_shared_portSortedOh <= MmuPlugin_shared_refills;
               MmuPlugin_shared_vpn_1        <= _zz_MmuPlugin_shared_vpn_0[31 : 22];
               MmuPlugin_shared_vpn_0        <= _zz_MmuPlugin_shared_vpn_0[21 : 12];
            end
         end
         MmuPlugin_shared_State_L1_CMD: begin
         end
         MmuPlugin_shared_State_L1_RSP: begin
         end
         MmuPlugin_shared_State_L0_CMD: begin
         end
         default: begin
         end
      endcase
      if (when_MmuPlugin_l302) begin
         if (when_MmuPlugin_l304) begin
            if (when_MmuPlugin_l310) begin
               MmuPlugin_ports_0_cache_0_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_0_cache_0_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_0_cache_0_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_0_cache_0_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_0_cache_0_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_0_cache_0_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_0_cache_0_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_0_cache_0_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_0_cache_0_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_0_cache_0_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
            if (when_MmuPlugin_l310_1) begin
               MmuPlugin_ports_0_cache_1_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_0_cache_1_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_0_cache_1_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_0_cache_1_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_0_cache_1_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_0_cache_1_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_0_cache_1_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_0_cache_1_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_0_cache_1_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_0_cache_1_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
            if (when_MmuPlugin_l310_2) begin
               MmuPlugin_ports_0_cache_2_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_0_cache_2_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_0_cache_2_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_0_cache_2_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_0_cache_2_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_0_cache_2_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_0_cache_2_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_0_cache_2_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_0_cache_2_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_0_cache_2_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
            if (when_MmuPlugin_l310_3) begin
               MmuPlugin_ports_0_cache_3_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_0_cache_3_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_0_cache_3_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_0_cache_3_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_0_cache_3_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_0_cache_3_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_0_cache_3_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_0_cache_3_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_0_cache_3_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_0_cache_3_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
         end
         if (when_MmuPlugin_l304_1) begin
            if (when_MmuPlugin_l310_4) begin
               MmuPlugin_ports_1_cache_0_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_1_cache_0_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_1_cache_0_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_1_cache_0_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_1_cache_0_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_1_cache_0_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_1_cache_0_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_1_cache_0_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_1_cache_0_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_1_cache_0_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
            if (when_MmuPlugin_l310_5) begin
               MmuPlugin_ports_1_cache_1_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_1_cache_1_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_1_cache_1_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_1_cache_1_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_1_cache_1_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_1_cache_1_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_1_cache_1_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_1_cache_1_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_1_cache_1_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_1_cache_1_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
            if (when_MmuPlugin_l310_6) begin
               MmuPlugin_ports_1_cache_2_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_1_cache_2_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_1_cache_2_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_1_cache_2_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_1_cache_2_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_1_cache_2_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_1_cache_2_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_1_cache_2_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_1_cache_2_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_1_cache_2_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
            if (when_MmuPlugin_l310_7) begin
               MmuPlugin_ports_1_cache_3_exception <= ((MmuPlugin_shared_dBusRsp_exception || ((MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP) && (MmuPlugin_shared_dBusRsp_pte_PPN0 != 10'h000))) || (! MmuPlugin_shared_dBusRsp_pte_A));
               MmuPlugin_ports_1_cache_3_virtualAddress_0 <= MmuPlugin_shared_vpn_0;
               MmuPlugin_ports_1_cache_3_virtualAddress_1 <= MmuPlugin_shared_vpn_1;
               MmuPlugin_ports_1_cache_3_physicalAddress_0 <= MmuPlugin_shared_dBusRsp_pte_PPN0;
               MmuPlugin_ports_1_cache_3_physicalAddress_1 <= MmuPlugin_shared_dBusRsp_pte_PPN1[9 : 0];
               MmuPlugin_ports_1_cache_3_allowRead <= MmuPlugin_shared_dBusRsp_pte_R;
               MmuPlugin_ports_1_cache_3_allowWrite <= (MmuPlugin_shared_dBusRsp_pte_W && MmuPlugin_shared_dBusRsp_pte_D);
               MmuPlugin_ports_1_cache_3_allowExecute <= MmuPlugin_shared_dBusRsp_pte_X;
               MmuPlugin_ports_1_cache_3_allowUser <= MmuPlugin_shared_dBusRsp_pte_U;
               MmuPlugin_ports_1_cache_3_superPage <= (MmuPlugin_shared_state_1 == MmuPlugin_shared_State_L1_RSP);
            end
         end
      end
      if (when_MulDivIterativePlugin_l126) begin
         memory_DivPlugin_div_done <= 1'b1;
      end
      if (when_MulDivIterativePlugin_l126_1) begin
         memory_DivPlugin_div_done <= 1'b0;
      end
      if (when_MulDivIterativePlugin_l128) begin
         if (when_MulDivIterativePlugin_l132) begin
            memory_DivPlugin_rs1[31 : 0]         <= memory_DivPlugin_div_stage_0_outNumerator;
            memory_DivPlugin_accumulator[31 : 0] <= memory_DivPlugin_div_stage_0_outRemainder;
            if (when_MulDivIterativePlugin_l151) begin
               memory_DivPlugin_div_result <= _zz_memory_DivPlugin_div_result_1[31:0];
            end
         end
      end
      if (when_MulDivIterativePlugin_l162) begin
         memory_DivPlugin_accumulator <= 65'h00000000000000000;
         memory_DivPlugin_rs1 <= ((_zz_memory_DivPlugin_rs1 ? (~ _zz_memory_DivPlugin_rs1_1) : _zz_memory_DivPlugin_rs1_1) + _zz_memory_DivPlugin_rs1_2);
         memory_DivPlugin_rs2 <= ((_zz_memory_DivPlugin_rs2 ? (~ execute_RS2) : execute_RS2) + _zz_memory_DivPlugin_rs2_1);
         memory_DivPlugin_div_needRevert <= ((_zz_memory_DivPlugin_rs1 ^ (_zz_memory_DivPlugin_rs2 && (! execute_INSTRUCTION[13]))) && (! (((execute_RS2 == 32'h00000000) && execute_IS_RS2_SIGNED) && (! execute_INSTRUCTION[13]))));
      end
      HazardSimplePlugin_writeBackBuffer_payload_address <= HazardSimplePlugin_writeBackWrites_payload_address;
      HazardSimplePlugin_writeBackBuffer_payload_data <= HazardSimplePlugin_writeBackWrites_payload_data;
      CsrPlugin_mip_MEIP <= externalInterrupt;
      CsrPlugin_mip_MTIP <= timerInterrupt;
      CsrPlugin_mip_MSIP <= softwareInterrupt;
      CsrPlugin_sip_SEIP_INPUT <= externalInterruptS;
      if (_zz_when) begin
         CsrPlugin_exceptionPortCtrl_exceptionContext_code <= (_zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1 ? IBusCachedPlugin_decodeExceptionPort_payload_code : decodeExceptionPort_payload_code);
         CsrPlugin_exceptionPortCtrl_exceptionContext_badAddr <= (_zz_CsrPlugin_exceptionPortCtrl_exceptionContext_code_1 ? IBusCachedPlugin_decodeExceptionPort_payload_badAddr : decodeExceptionPort_payload_badAddr);
      end
      if (CsrPlugin_selfException_valid) begin
         CsrPlugin_exceptionPortCtrl_exceptionContext_code <= CsrPlugin_selfException_payload_code;
         CsrPlugin_exceptionPortCtrl_exceptionContext_badAddr <= CsrPlugin_selfException_payload_badAddr;
      end
      if (DBusCachedPlugin_exceptionBus_valid) begin
         CsrPlugin_exceptionPortCtrl_exceptionContext_code <= DBusCachedPlugin_exceptionBus_payload_code;
         CsrPlugin_exceptionPortCtrl_exceptionContext_badAddr <= DBusCachedPlugin_exceptionBus_payload_badAddr;
      end
      if (when_CsrPlugin_l1296) begin
         if (when_CsrPlugin_l1302) begin
            CsrPlugin_interrupt_code            <= 4'b0101;
            CsrPlugin_interrupt_targetPrivilege <= 2'b01;
         end
         if (when_CsrPlugin_l1302_1) begin
            CsrPlugin_interrupt_code            <= 4'b0001;
            CsrPlugin_interrupt_targetPrivilege <= 2'b01;
         end
         if (when_CsrPlugin_l1302_2) begin
            CsrPlugin_interrupt_code            <= 4'b1001;
            CsrPlugin_interrupt_targetPrivilege <= 2'b01;
         end
      end
      if (when_CsrPlugin_l1296_1) begin
         if (when_CsrPlugin_l1302_3) begin
            CsrPlugin_interrupt_code            <= 4'b0101;
            CsrPlugin_interrupt_targetPrivilege <= 2'b11;
         end
         if (when_CsrPlugin_l1302_4) begin
            CsrPlugin_interrupt_code            <= 4'b0001;
            CsrPlugin_interrupt_targetPrivilege <= 2'b11;
         end
         if (when_CsrPlugin_l1302_5) begin
            CsrPlugin_interrupt_code            <= 4'b1001;
            CsrPlugin_interrupt_targetPrivilege <= 2'b11;
         end
         if (when_CsrPlugin_l1302_6) begin
            CsrPlugin_interrupt_code            <= 4'b0111;
            CsrPlugin_interrupt_targetPrivilege <= 2'b11;
         end
         if (when_CsrPlugin_l1302_7) begin
            CsrPlugin_interrupt_code            <= 4'b0011;
            CsrPlugin_interrupt_targetPrivilege <= 2'b11;
         end
         if (when_CsrPlugin_l1302_8) begin
            CsrPlugin_interrupt_code            <= 4'b1011;
            CsrPlugin_interrupt_targetPrivilege <= 2'b11;
         end
      end
      if (when_CsrPlugin_l1390) begin
         if (when_CsrPlugin_l1398) begin
            case (CsrPlugin_targetPrivilege)
               2'b01: begin
                  CsrPlugin_scause_interrupt     <= (!CsrPlugin_hadException);
                  CsrPlugin_scause_exceptionCode <= CsrPlugin_trapCause;
                  CsrPlugin_sepc                 <= writeBack_PC;
                  if (CsrPlugin_hadException) begin
                     CsrPlugin_stval <= CsrPlugin_exceptionPortCtrl_exceptionContext_badAddr;
                  end
               end
               2'b11: begin
                  CsrPlugin_mcause_interrupt     <= (!CsrPlugin_hadException);
                  CsrPlugin_mcause_exceptionCode <= CsrPlugin_trapCause;
                  CsrPlugin_mepc                 <= writeBack_PC;
                  if (CsrPlugin_hadException) begin
                     CsrPlugin_mtval <= CsrPlugin_exceptionPortCtrl_exceptionContext_badAddr;
                  end
               end
               default: begin
               end
            endcase
         end
      end
      if (when_Pipeline_l124) begin
         decode_to_execute_PC <= decode_PC;
      end
      if (when_Pipeline_l124_1) begin
         execute_to_memory_PC <= _zz_execute_to_memory_PC;
      end
      if (when_Pipeline_l124_2) begin
         memory_to_writeBack_PC <= memory_PC;
      end
      if (when_Pipeline_l124_3) begin
         decode_to_execute_INSTRUCTION <= decode_INSTRUCTION;
      end
      if (when_Pipeline_l124_4) begin
         execute_to_memory_INSTRUCTION <= execute_INSTRUCTION;
      end
      if (when_Pipeline_l124_5) begin
         memory_to_writeBack_INSTRUCTION <= memory_INSTRUCTION;
      end
      if (when_Pipeline_l124_6) begin
         decode_to_execute_IS_RVC <= decode_IS_RVC;
      end
      if (when_Pipeline_l124_7) begin
         decode_to_execute_FORMAL_PC_NEXT <= decode_FORMAL_PC_NEXT;
      end
      if (when_Pipeline_l124_8) begin
         execute_to_memory_FORMAL_PC_NEXT <= _zz_execute_to_memory_FORMAL_PC_NEXT;
      end
      if (when_Pipeline_l124_9) begin
         memory_to_writeBack_FORMAL_PC_NEXT <= _zz_memory_to_writeBack_FORMAL_PC_NEXT;
      end
      if (when_Pipeline_l124_10) begin
         decode_to_execute_MEMORY_FORCE_CONSTISTENCY <= decode_MEMORY_FORCE_CONSTISTENCY;
      end
      if (when_Pipeline_l124_11) begin
         decode_to_execute_RESCHEDULE_NEXT <= decode_RESCHEDULE_NEXT;
      end
      if (when_Pipeline_l124_12) begin
         decode_to_execute_SRC1_CTRL <= _zz_decode_to_execute_SRC1_CTRL;
      end
      if (when_Pipeline_l124_13) begin
         decode_to_execute_SRC_USE_SUB_LESS <= decode_SRC_USE_SUB_LESS;
      end
      if (when_Pipeline_l124_14) begin
         decode_to_execute_MEMORY_ENABLE <= decode_MEMORY_ENABLE;
      end
      if (when_Pipeline_l124_15) begin
         execute_to_memory_MEMORY_ENABLE <= execute_MEMORY_ENABLE;
      end
      if (when_Pipeline_l124_16) begin
         memory_to_writeBack_MEMORY_ENABLE <= memory_MEMORY_ENABLE;
      end
      if (when_Pipeline_l124_17) begin
         decode_to_execute_ALU_CTRL <= _zz_decode_to_execute_ALU_CTRL;
      end
      if (when_Pipeline_l124_18) begin
         decode_to_execute_SRC2_CTRL <= _zz_decode_to_execute_SRC2_CTRL;
      end
      if (when_Pipeline_l124_19) begin
         decode_to_execute_REGFILE_WRITE_VALID <= decode_REGFILE_WRITE_VALID;
      end
      if (when_Pipeline_l124_20) begin
         execute_to_memory_REGFILE_WRITE_VALID <= execute_REGFILE_WRITE_VALID;
      end
      if (when_Pipeline_l124_21) begin
         memory_to_writeBack_REGFILE_WRITE_VALID <= memory_REGFILE_WRITE_VALID;
      end
      if (when_Pipeline_l124_22) begin
         decode_to_execute_BYPASSABLE_EXECUTE_STAGE <= decode_BYPASSABLE_EXECUTE_STAGE;
      end
      if (when_Pipeline_l124_23) begin
         decode_to_execute_BYPASSABLE_MEMORY_STAGE <= decode_BYPASSABLE_MEMORY_STAGE;
      end
      if (when_Pipeline_l124_24) begin
         execute_to_memory_BYPASSABLE_MEMORY_STAGE <= execute_BYPASSABLE_MEMORY_STAGE;
      end
      if (when_Pipeline_l124_25) begin
         decode_to_execute_MEMORY_WR <= decode_MEMORY_WR;
      end
      if (when_Pipeline_l124_26) begin
         execute_to_memory_MEMORY_WR <= execute_MEMORY_WR;
      end
      if (when_Pipeline_l124_27) begin
         memory_to_writeBack_MEMORY_WR <= memory_MEMORY_WR;
      end
      if (when_Pipeline_l124_28) begin
         decode_to_execute_MEMORY_LRSC <= decode_MEMORY_LRSC;
      end
      if (when_Pipeline_l124_29) begin
         execute_to_memory_MEMORY_LRSC <= execute_MEMORY_LRSC;
      end
      if (when_Pipeline_l124_30) begin
         memory_to_writeBack_MEMORY_LRSC <= memory_MEMORY_LRSC;
      end
      if (when_Pipeline_l124_31) begin
         decode_to_execute_MEMORY_AMO <= decode_MEMORY_AMO;
      end
      if (when_Pipeline_l124_32) begin
         decode_to_execute_MEMORY_MANAGMENT <= decode_MEMORY_MANAGMENT;
      end
      if (when_Pipeline_l124_33) begin
         decode_to_execute_IS_SFENCE_VMA2 <= decode_IS_SFENCE_VMA2;
      end
      if (when_Pipeline_l124_34) begin
         decode_to_execute_SRC_LESS_UNSIGNED <= decode_SRC_LESS_UNSIGNED;
      end
      if (when_Pipeline_l124_35) begin
         decode_to_execute_ALU_BITWISE_CTRL <= _zz_decode_to_execute_ALU_BITWISE_CTRL;
      end
      if (when_Pipeline_l124_36) begin
         decode_to_execute_SHIFT_CTRL <= _zz_decode_to_execute_SHIFT_CTRL;
      end
      if (when_Pipeline_l124_37) begin
         execute_to_memory_SHIFT_CTRL <= _zz_execute_to_memory_SHIFT_CTRL;
      end
      if (when_Pipeline_l124_38) begin
         decode_to_execute_IS_MUL <= decode_IS_MUL;
      end
      if (when_Pipeline_l124_39) begin
         execute_to_memory_IS_MUL <= execute_IS_MUL;
      end
      if (when_Pipeline_l124_40) begin
         memory_to_writeBack_IS_MUL <= memory_IS_MUL;
      end
      if (when_Pipeline_l124_41) begin
         decode_to_execute_IS_DIV <= decode_IS_DIV;
      end
      if (when_Pipeline_l124_42) begin
         execute_to_memory_IS_DIV <= execute_IS_DIV;
      end
      if (when_Pipeline_l124_43) begin
         decode_to_execute_IS_RS1_SIGNED <= decode_IS_RS1_SIGNED;
      end
      if (when_Pipeline_l124_44) begin
         decode_to_execute_IS_RS2_SIGNED <= decode_IS_RS2_SIGNED;
      end
      if (when_Pipeline_l124_45) begin
         decode_to_execute_BRANCH_CTRL <= _zz_decode_to_execute_BRANCH_CTRL;
      end
      if (when_Pipeline_l124_46) begin
         decode_to_execute_IS_CSR <= decode_IS_CSR;
      end
      if (when_Pipeline_l124_47) begin
         decode_to_execute_ENV_CTRL <= _zz_decode_to_execute_ENV_CTRL;
      end
      if (when_Pipeline_l124_48) begin
         execute_to_memory_ENV_CTRL <= _zz_execute_to_memory_ENV_CTRL;
      end
      if (when_Pipeline_l124_49) begin
         memory_to_writeBack_ENV_CTRL <= _zz_memory_to_writeBack_ENV_CTRL;
      end
      if (when_Pipeline_l124_50) begin
         decode_to_execute_RS1 <= decode_RS1;
      end
      if (when_Pipeline_l124_51) begin
         decode_to_execute_RS2 <= decode_RS2;
      end
      if (when_Pipeline_l124_52) begin
         decode_to_execute_SRC2_FORCE_ZERO <= decode_SRC2_FORCE_ZERO;
      end
      if (when_Pipeline_l124_53) begin
         decode_to_execute_CSR_WRITE_OPCODE <= decode_CSR_WRITE_OPCODE;
      end
      if (when_Pipeline_l124_54) begin
         decode_to_execute_CSR_READ_OPCODE <= decode_CSR_READ_OPCODE;
      end
      if (when_Pipeline_l124_55) begin
         execute_to_memory_MEMORY_STORE_DATA_RF <= execute_MEMORY_STORE_DATA_RF;
      end
      if (when_Pipeline_l124_56) begin
         memory_to_writeBack_MEMORY_STORE_DATA_RF <= memory_MEMORY_STORE_DATA_RF;
      end
      if (when_Pipeline_l124_59) begin
         execute_to_memory_REGFILE_WRITE_DATA <= _zz_decode_RS2;
      end
      if (when_Pipeline_l124_60) begin
         memory_to_writeBack_REGFILE_WRITE_DATA <= _zz_decode_RS2_1;
      end
      if (when_Pipeline_l124_61) begin
         execute_to_memory_SHIFT_RIGHT <= execute_SHIFT_RIGHT;
      end
      if (when_Pipeline_l124_62) begin
         execute_to_memory_MUL_LL <= execute_MUL_LL;
      end
      if (when_Pipeline_l124_63) begin
         execute_to_memory_MUL_LH <= execute_MUL_LH;
      end
      if (when_Pipeline_l124_64) begin
         execute_to_memory_MUL_HL <= execute_MUL_HL;
      end
      if (when_Pipeline_l124_65) begin
         execute_to_memory_MUL_HH <= execute_MUL_HH;
      end
      if (when_Pipeline_l124_66) begin
         memory_to_writeBack_MUL_HH <= memory_MUL_HH;
      end
      if (when_Pipeline_l124_67) begin
         execute_to_memory_BRANCH_DO <= execute_BRANCH_DO;
      end
      if (when_Pipeline_l124_68) begin
         execute_to_memory_BRANCH_CALC <= execute_BRANCH_CALC;
      end
      if (when_Pipeline_l124_69) begin
         memory_to_writeBack_MUL_LOW <= memory_MUL_LOW;
      end
      if (when_CsrPlugin_l1669) begin
         execute_CsrPlugin_csr_768 <= (decode_INSTRUCTION[31 : 20] == 12'h300);
      end
      if (when_CsrPlugin_l1669_1) begin
         execute_CsrPlugin_csr_256 <= (decode_INSTRUCTION[31 : 20] == 12'h100);
      end
      if (when_CsrPlugin_l1669_2) begin
         execute_CsrPlugin_csr_384 <= (decode_INSTRUCTION[31 : 20] == 12'h180);
      end
      if (when_CsrPlugin_l1669_3) begin
         execute_CsrPlugin_csr_3857 <= (decode_INSTRUCTION[31 : 20] == 12'hf11);
      end
      if (when_CsrPlugin_l1669_4) begin
         execute_CsrPlugin_csr_3858 <= (decode_INSTRUCTION[31 : 20] == 12'hf12);
      end
      if (when_CsrPlugin_l1669_5) begin
         execute_CsrPlugin_csr_3859 <= (decode_INSTRUCTION[31 : 20] == 12'hf13);
      end
      if (when_CsrPlugin_l1669_6) begin
         execute_CsrPlugin_csr_3860 <= (decode_INSTRUCTION[31 : 20] == 12'hf14);
      end
      if (when_CsrPlugin_l1669_7) begin
         execute_CsrPlugin_csr_769 <= (decode_INSTRUCTION[31 : 20] == 12'h301);
      end
      if (when_CsrPlugin_l1669_8) begin
         execute_CsrPlugin_csr_836 <= (decode_INSTRUCTION[31 : 20] == 12'h344);
      end
      if (when_CsrPlugin_l1669_9) begin
         execute_CsrPlugin_csr_772 <= (decode_INSTRUCTION[31 : 20] == 12'h304);
      end
      if (when_CsrPlugin_l1669_10) begin
         execute_CsrPlugin_csr_773 <= (decode_INSTRUCTION[31 : 20] == 12'h305);
      end
      if (when_CsrPlugin_l1669_11) begin
         execute_CsrPlugin_csr_833 <= (decode_INSTRUCTION[31 : 20] == 12'h341);
      end
      if (when_CsrPlugin_l1669_12) begin
         execute_CsrPlugin_csr_832 <= (decode_INSTRUCTION[31 : 20] == 12'h340);
      end
      if (when_CsrPlugin_l1669_13) begin
         execute_CsrPlugin_csr_834 <= (decode_INSTRUCTION[31 : 20] == 12'h342);
      end
      if (when_CsrPlugin_l1669_14) begin
         execute_CsrPlugin_csr_835 <= (decode_INSTRUCTION[31 : 20] == 12'h343);
      end
      if (when_CsrPlugin_l1669_15) begin
         execute_CsrPlugin_csr_2816 <= (decode_INSTRUCTION[31 : 20] == 12'hb00);
      end
      if (when_CsrPlugin_l1669_16) begin
         execute_CsrPlugin_csr_2944 <= (decode_INSTRUCTION[31 : 20] == 12'hb80);
      end
      if (when_CsrPlugin_l1669_17) begin
         execute_CsrPlugin_csr_2818 <= (decode_INSTRUCTION[31 : 20] == 12'hb02);
      end
      if (when_CsrPlugin_l1669_18) begin
         execute_CsrPlugin_csr_2946 <= (decode_INSTRUCTION[31 : 20] == 12'hb82);
      end
      if (when_CsrPlugin_l1669_19) begin
         execute_CsrPlugin_csr_770 <= (decode_INSTRUCTION[31 : 20] == 12'h302);
      end
      if (when_CsrPlugin_l1669_20) begin
         execute_CsrPlugin_csr_771 <= (decode_INSTRUCTION[31 : 20] == 12'h303);
      end
      if (when_CsrPlugin_l1669_21) begin
         execute_CsrPlugin_csr_3072 <= (decode_INSTRUCTION[31 : 20] == 12'hc00);
      end
      if (when_CsrPlugin_l1669_22) begin
         execute_CsrPlugin_csr_3200 <= (decode_INSTRUCTION[31 : 20] == 12'hc80);
      end
      if (when_CsrPlugin_l1669_23) begin
         execute_CsrPlugin_csr_3074 <= (decode_INSTRUCTION[31 : 20] == 12'hc02);
      end
      if (when_CsrPlugin_l1669_24) begin
         execute_CsrPlugin_csr_3202 <= (decode_INSTRUCTION[31 : 20] == 12'hc82);
      end
      if (when_CsrPlugin_l1669_25) begin
         execute_CsrPlugin_csr_3073 <= (decode_INSTRUCTION[31 : 20] == 12'hc01);
      end
      if (when_CsrPlugin_l1669_26) begin
         execute_CsrPlugin_csr_3201 <= (decode_INSTRUCTION[31 : 20] == 12'hc81);
      end
      if (when_CsrPlugin_l1669_27) begin
         execute_CsrPlugin_csr_774 <= (decode_INSTRUCTION[31 : 20] == 12'h306);
      end
      if (when_CsrPlugin_l1669_28) begin
         execute_CsrPlugin_csr_262 <= (decode_INSTRUCTION[31 : 20] == 12'h106);
      end
      if (when_CsrPlugin_l1669_29) begin
         execute_CsrPlugin_csr_324 <= (decode_INSTRUCTION[31 : 20] == 12'h144);
      end
      if (when_CsrPlugin_l1669_30) begin
         execute_CsrPlugin_csr_260 <= (decode_INSTRUCTION[31 : 20] == 12'h104);
      end
      if (when_CsrPlugin_l1669_31) begin
         execute_CsrPlugin_csr_261 <= (decode_INSTRUCTION[31 : 20] == 12'h105);
      end
      if (when_CsrPlugin_l1669_32) begin
         execute_CsrPlugin_csr_321 <= (decode_INSTRUCTION[31 : 20] == 12'h141);
      end
      if (when_CsrPlugin_l1669_33) begin
         execute_CsrPlugin_csr_320 <= (decode_INSTRUCTION[31 : 20] == 12'h140);
      end
      if (when_CsrPlugin_l1669_34) begin
         execute_CsrPlugin_csr_322 <= (decode_INSTRUCTION[31 : 20] == 12'h142);
      end
      if (when_CsrPlugin_l1669_35) begin
         execute_CsrPlugin_csr_323 <= (decode_INSTRUCTION[31 : 20] == 12'h143);
      end
      if (execute_CsrPlugin_csr_384) begin
         if (execute_CsrPlugin_writeEnable) begin
            MmuPlugin_satp_asid <= CsrPlugin_csrMapping_writeDataSignal[30 : 22];
            MmuPlugin_satp_ppn  <= CsrPlugin_csrMapping_writeDataSignal[21 : 0];
         end
      end
      if (execute_CsrPlugin_csr_836) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_mip_MSIP <= CsrPlugin_csrMapping_writeDataSignal[3];
         end
      end
      if (execute_CsrPlugin_csr_833) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_mepc <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
         end
      end
      if (execute_CsrPlugin_csr_832) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_mscratch <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
         end
      end
      if (execute_CsrPlugin_csr_834) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_mcause_interrupt     <= CsrPlugin_csrMapping_writeDataSignal[31];
            CsrPlugin_mcause_exceptionCode <= CsrPlugin_csrMapping_writeDataSignal[3 : 0];
         end
      end
      if (execute_CsrPlugin_csr_835) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_mtval <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
         end
      end
      if (execute_CsrPlugin_csr_261) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_stvec_base <= CsrPlugin_csrMapping_writeDataSignal[31 : 2];
         end
      end
      if (execute_CsrPlugin_csr_321) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_sepc <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
         end
      end
      if (execute_CsrPlugin_csr_320) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_sscratch <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
         end
      end
      if (execute_CsrPlugin_csr_322) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_scause_interrupt     <= CsrPlugin_csrMapping_writeDataSignal[31];
            CsrPlugin_scause_exceptionCode <= CsrPlugin_csrMapping_writeDataSignal[3 : 0];
         end
      end
      if (execute_CsrPlugin_csr_323) begin
         if (execute_CsrPlugin_writeEnable) begin
            CsrPlugin_stval <= CsrPlugin_csrMapping_writeDataSignal[31 : 0];
         end
      end
   end


endmodule

module DataCache (
   input             io_cpu_execute_isValid,
   input      [31:0] io_cpu_execute_address,
   output reg        io_cpu_execute_haltIt,
   input             io_cpu_execute_args_wr,
   input      [ 1:0] io_cpu_execute_args_size,
   input             io_cpu_execute_args_isLrsc,
   input             io_cpu_execute_args_isAmo,
   input             io_cpu_execute_args_amoCtrl_swap,
   input      [ 2:0] io_cpu_execute_args_amoCtrl_alu,
   input             io_cpu_execute_args_totalyConsistent,
   output            io_cpu_execute_refilling,
   input             io_cpu_memory_isValid,
   input             io_cpu_memory_isStuck,
   output            io_cpu_memory_isWrite,
   input      [31:0] io_cpu_memory_address,
   input      [31:0] io_cpu_memory_mmuRsp_physicalAddress,
   input             io_cpu_memory_mmuRsp_isIoAccess,
   input             io_cpu_memory_mmuRsp_isPaging,
   input             io_cpu_memory_mmuRsp_allowRead,
   input             io_cpu_memory_mmuRsp_allowWrite,
   input             io_cpu_memory_mmuRsp_allowExecute,
   input             io_cpu_memory_mmuRsp_exception,
   input             io_cpu_memory_mmuRsp_refilling,
   input             io_cpu_memory_mmuRsp_bypassTranslation,
   input             io_cpu_memory_mmuRsp_ways_0_sel,
   input      [31:0] io_cpu_memory_mmuRsp_ways_0_physical,
   input             io_cpu_memory_mmuRsp_ways_1_sel,
   input      [31:0] io_cpu_memory_mmuRsp_ways_1_physical,
   input             io_cpu_memory_mmuRsp_ways_2_sel,
   input      [31:0] io_cpu_memory_mmuRsp_ways_2_physical,
   input             io_cpu_memory_mmuRsp_ways_3_sel,
   input      [31:0] io_cpu_memory_mmuRsp_ways_3_physical,
   input             io_cpu_writeBack_isValid,
   input             io_cpu_writeBack_isStuck,
   input             io_cpu_writeBack_isFiring,
   input             io_cpu_writeBack_isUser,
   output reg        io_cpu_writeBack_haltIt,
   output            io_cpu_writeBack_isWrite,
   input      [31:0] io_cpu_writeBack_storeData,
   output reg [31:0] io_cpu_writeBack_data,
   input      [31:0] io_cpu_writeBack_address,
   output            io_cpu_writeBack_mmuException,
   output            io_cpu_writeBack_unalignedAccess,
   output reg        io_cpu_writeBack_accessError,
   output            io_cpu_writeBack_keepMemRspData,
   input             io_cpu_writeBack_fence_SW,
   input             io_cpu_writeBack_fence_SR,
   input             io_cpu_writeBack_fence_SO,
   input             io_cpu_writeBack_fence_SI,
   input             io_cpu_writeBack_fence_PW,
   input             io_cpu_writeBack_fence_PR,
   input             io_cpu_writeBack_fence_PO,
   input             io_cpu_writeBack_fence_PI,
   input      [ 3:0] io_cpu_writeBack_fence_FM,
   output            io_cpu_writeBack_exclusiveOk,
   output reg        io_cpu_redo,
   input             io_cpu_flush_valid,
   output            io_cpu_flush_ready,
   input             io_cpu_flush_payload_singleLine,
   input      [ 5:0] io_cpu_flush_payload_lineId,
   output            io_cpu_writesPending,
   output reg        io_mem_cmd_valid,
   input             io_mem_cmd_ready,
   output reg        io_mem_cmd_payload_wr,
   output            io_mem_cmd_payload_uncached,
   output reg [31:0] io_mem_cmd_payload_address,
   output     [31:0] io_mem_cmd_payload_data,
   output     [ 3:0] io_mem_cmd_payload_mask,
   output reg [ 2:0] io_mem_cmd_payload_size,
   output            io_mem_cmd_payload_last,
   input             io_mem_rsp_valid,
   input             io_mem_rsp_payload_last,
   input      [31:0] io_mem_rsp_payload_data,
   input             io_mem_rsp_payload_error,
   input             clk,
   input             reset
);

   reg  [21:0] _zz_ways_0_tags_port0;
   reg  [31:0] _zz_ways_0_data_port0;
   wire [21:0] _zz_ways_0_tags_port;
   wire [31:0] _zz_stageB_amo_addSub;
   wire [31:0] _zz_stageB_amo_addSub_1;
   wire [31:0] _zz_stageB_amo_addSub_2;
   wire [31:0] _zz_stageB_amo_addSub_3;
   wire [31:0] _zz_stageB_amo_addSub_4;
   wire [ 1:0] _zz_stageB_amo_addSub_5;
   wire [ 0:0] _zz_when;
   wire [ 3:0] _zz_loader_counter_valueNext;
   wire [ 0:0] _zz_loader_counter_valueNext_1;
   wire [ 1:0] _zz_loader_waysAllocator;
   reg         _zz_1;
   reg         _zz_2;
   wire        haltCpu;
   reg         tagsReadCmd_valid;
   reg  [ 5:0] tagsReadCmd_payload;
   reg         tagsWriteCmd_valid;
   reg  [ 0:0] tagsWriteCmd_payload_way;
   reg  [ 5:0] tagsWriteCmd_payload_address;
   reg         tagsWriteCmd_payload_data_valid;
   reg         tagsWriteCmd_payload_data_error;
   reg  [19:0] tagsWriteCmd_payload_data_address;
   reg         tagsWriteLastCmd_valid;
   reg  [ 0:0] tagsWriteLastCmd_payload_way;
   reg  [ 5:0] tagsWriteLastCmd_payload_address;
   reg         tagsWriteLastCmd_payload_data_valid;
   reg         tagsWriteLastCmd_payload_data_error;
   reg  [19:0] tagsWriteLastCmd_payload_data_address;
   reg         dataReadCmd_valid;
   reg  [ 9:0] dataReadCmd_payload;
   reg         dataWriteCmd_valid;
   reg  [ 0:0] dataWriteCmd_payload_way;
   reg  [ 9:0] dataWriteCmd_payload_address;
   reg  [31:0] dataWriteCmd_payload_data;
   reg  [ 3:0] dataWriteCmd_payload_mask;
   wire        _zz_ways_0_tagsReadRsp_valid;
   wire        ways_0_tagsReadRsp_valid;
   wire        ways_0_tagsReadRsp_error;
   wire [19:0] ways_0_tagsReadRsp_address;
   wire [21:0] _zz_ways_0_tagsReadRsp_valid_1;
   wire        _zz_ways_0_dataReadRspMem;
   wire [31:0] ways_0_dataReadRspMem;
   wire [31:0] ways_0_dataReadRsp;
   wire        when_DataCache_l645;
   wire        when_DataCache_l648;
   wire        when_DataCache_l667;
   wire        rspSync;
   wire        rspLast;
   reg         memCmdSent;
   wire        io_mem_cmd_fire;
   wire        when_DataCache_l689;
   reg  [ 3:0] _zz_stage0_mask;
   wire [ 3:0] stage0_mask;
   wire [ 0:0] stage0_dataColisions;
   wire [ 0:0] stage0_wayInvalidate;
   wire        when_DataCache_l776;
   reg         stageA_request_wr;
   reg  [ 1:0] stageA_request_size;
   reg         stageA_request_isLrsc;
   reg         stageA_request_isAmo;
   reg         stageA_request_amoCtrl_swap;
   reg  [ 2:0] stageA_request_amoCtrl_alu;
   reg         stageA_request_totalyConsistent;
   wire        when_DataCache_l776_1;
   reg  [ 3:0] stageA_mask;
   wire [ 0:0] stageA_wayHits;
   wire        when_DataCache_l776_2;
   reg  [ 0:0] stageA_wayInvalidate;
   wire        when_DataCache_l776_3;
   reg  [ 0:0] stage0_dataColisions_regNextWhen;
   wire [ 0:0] _zz_stageA_dataColisions;
   wire [ 0:0] stageA_dataColisions;
   wire        when_DataCache_l827;
   reg         stageB_request_wr;
   reg  [ 1:0] stageB_request_size;
   reg         stageB_request_isLrsc;
   reg         stageB_request_isAmo;
   reg         stageB_request_amoCtrl_swap;
   reg  [ 2:0] stageB_request_amoCtrl_alu;
   reg         stageB_request_totalyConsistent;
   reg         stageB_mmuRspFreeze;
   wire        when_DataCache_l829;
   reg  [31:0] stageB_mmuRsp_physicalAddress;
   reg         stageB_mmuRsp_isIoAccess;
   reg         stageB_mmuRsp_isPaging;
   reg         stageB_mmuRsp_allowRead;
   reg         stageB_mmuRsp_allowWrite;
   reg         stageB_mmuRsp_allowExecute;
   reg         stageB_mmuRsp_exception;
   reg         stageB_mmuRsp_refilling;
   reg         stageB_mmuRsp_bypassTranslation;
   reg         stageB_mmuRsp_ways_0_sel;
   reg  [31:0] stageB_mmuRsp_ways_0_physical;
   reg         stageB_mmuRsp_ways_1_sel;
   reg  [31:0] stageB_mmuRsp_ways_1_physical;
   reg         stageB_mmuRsp_ways_2_sel;
   reg  [31:0] stageB_mmuRsp_ways_2_physical;
   reg         stageB_mmuRsp_ways_3_sel;
   reg  [31:0] stageB_mmuRsp_ways_3_physical;
   wire        when_DataCache_l826;
   reg         stageB_tagsReadRsp_0_valid;
   reg         stageB_tagsReadRsp_0_error;
   reg  [19:0] stageB_tagsReadRsp_0_address;
   wire        when_DataCache_l826_1;
   reg  [31:0] stageB_dataReadRsp_0;
   wire        when_DataCache_l825;
   reg  [ 0:0] stageB_wayInvalidate;
   wire        stageB_consistancyHazard;
   wire        when_DataCache_l825_1;
   reg  [ 0:0] stageB_dataColisions;
   wire        when_DataCache_l825_2;
   reg         stageB_unaligned;
   wire        when_DataCache_l825_3;
   reg  [ 0:0] stageB_waysHitsBeforeInvalidate;
   wire [ 0:0] stageB_waysHits;
   wire        stageB_waysHit;
   wire [31:0] stageB_dataMux;
   wire        when_DataCache_l825_4;
   reg  [ 3:0] stageB_mask;
   reg         stageB_loaderValid;
   wire [31:0] stageB_ioMemRspMuxed;
   reg         stageB_flusher_waitDone;
   wire        stageB_flusher_hold;
   reg  [ 6:0] stageB_flusher_counter;
   wire        when_DataCache_l855;
   wire        when_DataCache_l861;
   wire        when_DataCache_l863;
   reg         stageB_flusher_start;
   wire        when_DataCache_l877;
   reg         stageB_lrSc_reserved;
   wire        when_DataCache_l885;
   wire        stageB_isExternalLsrc;
   wire        stageB_isExternalAmo;
   reg  [31:0] stageB_requestDataBypass;
   wire        stageB_amo_compare;
   wire        stageB_amo_unsigned;
   wire [31:0] stageB_amo_addSub;
   wire        stageB_amo_less;
   wire        stageB_amo_selectRf;
   wire [ 2:0] switch_Misc_l227;
   reg  [31:0] stageB_amo_result;
   reg  [31:0] stageB_amo_resultReg;
   reg         stageB_amo_internal_resultRegValid;
   reg         stageB_cpuWriteToCache;
   wire        when_DataCache_l931;
   wire        stageB_badPermissions;
   wire        stageB_loadStoreFault;
   wire        stageB_bypassCache;
   wire        when_DataCache_l1000;
   wire        when_DataCache_l1004;
   wire        when_DataCache_l1009;
   wire        when_DataCache_l1014;
   wire        when_DataCache_l1017;
   wire        when_DataCache_l1025;
   wire        when_DataCache_l1030;
   wire        when_DataCache_l1037;
   wire        when_DataCache_l996;
   wire        when_DataCache_l1072;
   wire        when_DataCache_l1081;
   reg         loader_valid;
   reg         loader_counter_willIncrement;
   wire        loader_counter_willClear;
   reg  [ 3:0] loader_counter_valueNext;
   reg  [ 3:0] loader_counter_value;
   wire        loader_counter_willOverflowIfInc;
   wire        loader_counter_willOverflow;
   reg  [ 0:0] loader_waysAllocator;
   reg         loader_error;
   wire        loader_kill;
   reg         loader_killReg;
   wire        when_DataCache_l1097;
   wire        loader_done;
   wire        when_DataCache_l1125;
   reg         loader_valid_regNext;
   wire        when_DataCache_l1129;
   wire        when_DataCache_l1132;
   reg  [21:0] ways_0_tags                           [  0:63];
   reg  [ 7:0] ways_0_data_symbol0                   [0:1023];
   reg  [ 7:0] ways_0_data_symbol1                   [0:1023];
   reg  [ 7:0] ways_0_data_symbol2                   [0:1023];
   reg  [ 7:0] ways_0_data_symbol3                   [0:1023];
   reg  [ 7:0] _zz_ways_0_datasymbol_read;
   reg  [ 7:0] _zz_ways_0_datasymbol_read_1;
   reg  [ 7:0] _zz_ways_0_datasymbol_read_2;
   reg  [ 7:0] _zz_ways_0_datasymbol_read_3;

   assign _zz_stageB_amo_addSub = ($signed(
       _zz_stageB_amo_addSub_1
   ) + $signed(
       _zz_stageB_amo_addSub_4
   ));
   assign _zz_stageB_amo_addSub_1 = ($signed(
       _zz_stageB_amo_addSub_2
   ) + $signed(
       _zz_stageB_amo_addSub_3
   ));
   assign _zz_stageB_amo_addSub_2 = io_cpu_writeBack_storeData[31 : 0];
   assign _zz_stageB_amo_addSub_3 = (stageB_amo_compare ? (~ stageB_dataMux[31 : 0]) : stageB_dataMux[31 : 0]);
   assign _zz_stageB_amo_addSub_5 = (stageB_amo_compare ? 2'b01 : 2'b00);
   assign _zz_stageB_amo_addSub_4 = {{30{_zz_stageB_amo_addSub_5[1]}}, _zz_stageB_amo_addSub_5};
   assign _zz_when = 1'b1;
   assign _zz_loader_counter_valueNext_1 = loader_counter_willIncrement;
   assign _zz_loader_counter_valueNext = {3'd0, _zz_loader_counter_valueNext_1};
   assign _zz_loader_waysAllocator = {loader_waysAllocator, loader_waysAllocator[0]};
   assign _zz_ways_0_tags_port = {
      tagsWriteCmd_payload_data_address,
      {tagsWriteCmd_payload_data_error, tagsWriteCmd_payload_data_valid}
   };
   always @(posedge clk) begin
      if (_zz_ways_0_tagsReadRsp_valid) begin
         _zz_ways_0_tags_port0 <= ways_0_tags[tagsReadCmd_payload];
      end
   end

   always @(posedge clk) begin
      if (_zz_2) begin
         ways_0_tags[tagsWriteCmd_payload_address] <= _zz_ways_0_tags_port;
      end
   end

   always @(*) begin
      _zz_ways_0_data_port0 = {
         _zz_ways_0_datasymbol_read_3,
         _zz_ways_0_datasymbol_read_2,
         _zz_ways_0_datasymbol_read_1,
         _zz_ways_0_datasymbol_read
      };
   end
   always @(posedge clk) begin
      if (_zz_ways_0_dataReadRspMem) begin
         _zz_ways_0_datasymbol_read   <= ways_0_data_symbol0[dataReadCmd_payload];
         _zz_ways_0_datasymbol_read_1 <= ways_0_data_symbol1[dataReadCmd_payload];
         _zz_ways_0_datasymbol_read_2 <= ways_0_data_symbol2[dataReadCmd_payload];
         _zz_ways_0_datasymbol_read_3 <= ways_0_data_symbol3[dataReadCmd_payload];
      end
   end

   always @(posedge clk) begin
      if (dataWriteCmd_payload_mask[0] && _zz_1) begin
         ways_0_data_symbol0[dataWriteCmd_payload_address] <= dataWriteCmd_payload_data[7 : 0];
      end
      if (dataWriteCmd_payload_mask[1] && _zz_1) begin
         ways_0_data_symbol1[dataWriteCmd_payload_address] <= dataWriteCmd_payload_data[15 : 8];
      end
      if (dataWriteCmd_payload_mask[2] && _zz_1) begin
         ways_0_data_symbol2[dataWriteCmd_payload_address] <= dataWriteCmd_payload_data[23 : 16];
      end
      if (dataWriteCmd_payload_mask[3] && _zz_1) begin
         ways_0_data_symbol3[dataWriteCmd_payload_address] <= dataWriteCmd_payload_data[31 : 24];
      end
   end

   always @(*) begin
      _zz_1 = 1'b0;
      if (when_DataCache_l648) begin
         _zz_1 = 1'b1;
      end
   end

   always @(*) begin
      _zz_2 = 1'b0;
      if (when_DataCache_l645) begin
         _zz_2 = 1'b1;
      end
   end

   assign haltCpu                        = 1'b0;
   assign _zz_ways_0_tagsReadRsp_valid   = (tagsReadCmd_valid && (!io_cpu_memory_isStuck));
   assign _zz_ways_0_tagsReadRsp_valid_1 = _zz_ways_0_tags_port0;
   assign ways_0_tagsReadRsp_valid       = _zz_ways_0_tagsReadRsp_valid_1[0];
   assign ways_0_tagsReadRsp_error       = _zz_ways_0_tagsReadRsp_valid_1[1];
   assign ways_0_tagsReadRsp_address     = _zz_ways_0_tagsReadRsp_valid_1[21 : 2];
   assign _zz_ways_0_dataReadRspMem      = (dataReadCmd_valid && (!io_cpu_memory_isStuck));
   assign ways_0_dataReadRspMem          = _zz_ways_0_data_port0;
   assign ways_0_dataReadRsp             = ways_0_dataReadRspMem[31 : 0];
   assign when_DataCache_l645            = (tagsWriteCmd_valid && tagsWriteCmd_payload_way[0]);
   assign when_DataCache_l648            = (dataWriteCmd_valid && dataWriteCmd_payload_way[0]);
   always @(*) begin
      tagsReadCmd_valid = 1'b0;
      if (when_DataCache_l667) begin
         tagsReadCmd_valid = 1'b1;
      end
   end

   always @(*) begin
      tagsReadCmd_payload = 6'bxxxxxx;
      if (when_DataCache_l667) begin
         tagsReadCmd_payload = io_cpu_execute_address[11 : 6];
      end
   end

   always @(*) begin
      dataReadCmd_valid = 1'b0;
      if (when_DataCache_l667) begin
         dataReadCmd_valid = 1'b1;
      end
   end

   always @(*) begin
      dataReadCmd_payload = 10'bxxxxxxxxxx;
      if (when_DataCache_l667) begin
         dataReadCmd_payload = io_cpu_execute_address[11 : 2];
      end
   end

   always @(*) begin
      tagsWriteCmd_valid = 1'b0;
      if (when_DataCache_l855) begin
         tagsWriteCmd_valid = 1'b1;
      end
      if (io_cpu_writeBack_isValid) begin
         if (when_DataCache_l1072) begin
            tagsWriteCmd_valid = 1'b0;
         end
      end
      if (loader_done) begin
         tagsWriteCmd_valid = 1'b1;
      end
   end

   always @(*) begin
      tagsWriteCmd_payload_way = 1'bx;
      if (when_DataCache_l855) begin
         tagsWriteCmd_payload_way = 1'b1;
      end
      if (loader_done) begin
         tagsWriteCmd_payload_way = loader_waysAllocator;
      end
   end

   always @(*) begin
      tagsWriteCmd_payload_address = 6'bxxxxxx;
      if (when_DataCache_l855) begin
         tagsWriteCmd_payload_address = stageB_flusher_counter[5:0];
      end
      if (loader_done) begin
         tagsWriteCmd_payload_address = stageB_mmuRsp_physicalAddress[11 : 6];
      end
   end

   always @(*) begin
      tagsWriteCmd_payload_data_valid = 1'bx;
      if (when_DataCache_l855) begin
         tagsWriteCmd_payload_data_valid = 1'b0;
      end
      if (loader_done) begin
         tagsWriteCmd_payload_data_valid = (!(loader_kill || loader_killReg));
      end
   end

   always @(*) begin
      tagsWriteCmd_payload_data_error = 1'bx;
      if (loader_done) begin
         tagsWriteCmd_payload_data_error = (loader_error || (io_mem_rsp_valid && io_mem_rsp_payload_error));
      end
   end

   always @(*) begin
      tagsWriteCmd_payload_data_address = 20'bxxxxxxxxxxxxxxxxxxxx;
      if (loader_done) begin
         tagsWriteCmd_payload_data_address = stageB_mmuRsp_physicalAddress[31 : 12];
      end
   end

   always @(*) begin
      dataWriteCmd_valid = 1'b0;
      if (stageB_cpuWriteToCache) begin
         if (when_DataCache_l931) begin
            dataWriteCmd_valid = 1'b1;
         end
      end
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (!when_DataCache_l996) begin
               if (when_DataCache_l1009) begin
                  if (stageB_request_isAmo) begin
                     if (when_DataCache_l1017) begin
                        dataWriteCmd_valid = 1'b0;
                     end
                  end
                  if (when_DataCache_l1030) begin
                     dataWriteCmd_valid = 1'b0;
                  end
               end
            end
         end
      end
      if (io_cpu_writeBack_isValid) begin
         if (when_DataCache_l1072) begin
            dataWriteCmd_valid = 1'b0;
         end
      end
      if (when_DataCache_l1097) begin
         dataWriteCmd_valid = 1'b1;
      end
   end

   always @(*) begin
      dataWriteCmd_payload_way = 1'bx;
      if (stageB_cpuWriteToCache) begin
         dataWriteCmd_payload_way = stageB_waysHits;
      end
      if (when_DataCache_l1097) begin
         dataWriteCmd_payload_way = loader_waysAllocator;
      end
   end

   always @(*) begin
      dataWriteCmd_payload_address = 10'bxxxxxxxxxx;
      if (stageB_cpuWriteToCache) begin
         dataWriteCmd_payload_address = stageB_mmuRsp_physicalAddress[11 : 2];
      end
      if (when_DataCache_l1097) begin
         dataWriteCmd_payload_address = {
            stageB_mmuRsp_physicalAddress[11 : 6], loader_counter_value
         };
      end
   end

   always @(*) begin
      dataWriteCmd_payload_data = 32'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
      if (stageB_cpuWriteToCache) begin
         dataWriteCmd_payload_data[31 : 0] = stageB_requestDataBypass;
      end
      if (when_DataCache_l1097) begin
         dataWriteCmd_payload_data = io_mem_rsp_payload_data;
      end
   end

   always @(*) begin
      dataWriteCmd_payload_mask = 4'bxxxx;
      if (stageB_cpuWriteToCache) begin
         dataWriteCmd_payload_mask = 4'b0000;
         if (_zz_when[0]) begin
            dataWriteCmd_payload_mask[3 : 0] = stageB_mask;
         end
      end
      if (when_DataCache_l1097) begin
         dataWriteCmd_payload_mask = 4'b1111;
      end
   end

   assign when_DataCache_l667 = (io_cpu_execute_isValid && (!io_cpu_memory_isStuck));
   always @(*) begin
      io_cpu_execute_haltIt = 1'b0;
      if (when_DataCache_l855) begin
         io_cpu_execute_haltIt = 1'b1;
      end
   end

   assign rspSync             = 1'b1;
   assign rspLast             = 1'b1;
   assign io_mem_cmd_fire     = (io_mem_cmd_valid && io_mem_cmd_ready);
   assign when_DataCache_l689 = (!io_cpu_writeBack_isStuck);
   always @(*) begin
      _zz_stage0_mask = 4'bxxxx;
      case (io_cpu_execute_args_size)
         2'b00: begin
            _zz_stage0_mask = 4'b0001;
         end
         2'b01: begin
            _zz_stage0_mask = 4'b0011;
         end
         2'b10: begin
            _zz_stage0_mask = 4'b1111;
         end
         default: begin
         end
      endcase
   end

   assign stage0_mask = (_zz_stage0_mask <<< io_cpu_execute_address[1 : 0]);
   assign stage0_dataColisions[0] = (((dataWriteCmd_valid && dataWriteCmd_payload_way[0]) && (dataWriteCmd_payload_address == io_cpu_execute_address[11 : 2])) && ((stage0_mask & dataWriteCmd_payload_mask[3 : 0]) != 4'b0000));
   assign stage0_wayInvalidate = 1'b0;
   assign when_DataCache_l776 = (!io_cpu_memory_isStuck);
   assign when_DataCache_l776_1 = (!io_cpu_memory_isStuck);
   assign io_cpu_memory_isWrite = stageA_request_wr;
   assign stageA_wayHits = ((io_cpu_memory_mmuRsp_physicalAddress[31 : 12] == ways_0_tagsReadRsp_address) && ways_0_tagsReadRsp_valid);
   assign when_DataCache_l776_2 = (!io_cpu_memory_isStuck);
   assign when_DataCache_l776_3 = (!io_cpu_memory_isStuck);
   assign _zz_stageA_dataColisions[0] = (((dataWriteCmd_valid && dataWriteCmd_payload_way[0]) && (dataWriteCmd_payload_address == io_cpu_memory_address[11 : 2])) && ((stageA_mask & dataWriteCmd_payload_mask[3 : 0]) != 4'b0000));
   assign stageA_dataColisions = (stage0_dataColisions_regNextWhen | _zz_stageA_dataColisions);
   assign when_DataCache_l827 = (!io_cpu_writeBack_isStuck);
   always @(*) begin
      stageB_mmuRspFreeze = 1'b0;
      if (when_DataCache_l1132) begin
         stageB_mmuRspFreeze = 1'b1;
      end
   end

   assign when_DataCache_l829      = ((!io_cpu_writeBack_isStuck) && (!stageB_mmuRspFreeze));
   assign when_DataCache_l826      = (!io_cpu_writeBack_isStuck);
   assign when_DataCache_l826_1    = (!io_cpu_writeBack_isStuck);
   assign when_DataCache_l825      = (!io_cpu_writeBack_isStuck);
   assign stageB_consistancyHazard = 1'b0;
   assign when_DataCache_l825_1    = (!io_cpu_writeBack_isStuck);
   assign when_DataCache_l825_2    = (!io_cpu_writeBack_isStuck);
   assign when_DataCache_l825_3    = (!io_cpu_writeBack_isStuck);
   assign stageB_waysHits          = (stageB_waysHitsBeforeInvalidate & (~stageB_wayInvalidate));
   assign stageB_waysHit           = (|stageB_waysHits);
   assign stageB_dataMux           = stageB_dataReadRsp_0;
   assign when_DataCache_l825_4    = (!io_cpu_writeBack_isStuck);
   always @(*) begin
      stageB_loaderValid = 1'b0;
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (!when_DataCache_l996) begin
               if (!when_DataCache_l1009) begin
                  if (io_mem_cmd_ready) begin
                     stageB_loaderValid = 1'b1;
                  end
               end
            end
         end
      end
      if (io_cpu_writeBack_isValid) begin
         if (when_DataCache_l1072) begin
            stageB_loaderValid = 1'b0;
         end
      end
   end

   assign stageB_ioMemRspMuxed = io_mem_rsp_payload_data[31 : 0];
   always @(*) begin
      io_cpu_writeBack_haltIt = 1'b1;
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (when_DataCache_l996) begin
               if (when_DataCache_l1000) begin
                  io_cpu_writeBack_haltIt = 1'b0;
               end
               if (when_DataCache_l1004) begin
                  io_cpu_writeBack_haltIt = 1'b0;
               end
            end else begin
               if (when_DataCache_l1009) begin
                  if (when_DataCache_l1014) begin
                     io_cpu_writeBack_haltIt = 1'b0;
                  end
                  if (stageB_request_isAmo) begin
                     if (when_DataCache_l1017) begin
                        io_cpu_writeBack_haltIt = 1'b1;
                     end
                  end
                  if (when_DataCache_l1030) begin
                     io_cpu_writeBack_haltIt = 1'b0;
                  end
               end
            end
         end
      end
      if (io_cpu_writeBack_isValid) begin
         if (when_DataCache_l1072) begin
            io_cpu_writeBack_haltIt = 1'b0;
         end
      end
   end

   assign stageB_flusher_hold   = 1'b0;
   assign when_DataCache_l855   = (!stageB_flusher_counter[6]);
   assign when_DataCache_l861   = (!stageB_flusher_hold);
   assign when_DataCache_l863   = (io_cpu_flush_valid && io_cpu_flush_payload_singleLine);
   assign io_cpu_flush_ready    = (stageB_flusher_waitDone && stageB_flusher_counter[6]);
   assign when_DataCache_l877   = (io_cpu_flush_valid && io_cpu_flush_payload_singleLine);
   assign when_DataCache_l885   = (io_cpu_writeBack_isValid && io_cpu_writeBack_isFiring);
   assign stageB_isExternalLsrc = 1'b0;
   assign stageB_isExternalAmo  = 1'b0;
   always @(*) begin
      stageB_requestDataBypass = io_cpu_writeBack_storeData;
      if (stageB_request_isAmo) begin
         stageB_requestDataBypass[31 : 0] = stageB_amo_resultReg;
      end
   end

   assign stageB_amo_compare = stageB_request_amoCtrl_alu[2];
   assign stageB_amo_unsigned = (stageB_request_amoCtrl_alu[2 : 1] == 2'b11);
   assign stageB_amo_addSub = _zz_stageB_amo_addSub;
   assign stageB_amo_less = ((io_cpu_writeBack_storeData[31] == stageB_dataMux[31]) ? stageB_amo_addSub[31] : (stageB_amo_unsigned ? stageB_dataMux[31] : io_cpu_writeBack_storeData[31]));
   assign stageB_amo_selectRf = (stageB_request_amoCtrl_swap ? 1'b1 : (stageB_request_amoCtrl_alu[0] ^ stageB_amo_less));
   assign switch_Misc_l227 = (stageB_request_amoCtrl_alu | {stageB_request_amoCtrl_swap, 2'b00});
   always @(*) begin
      case (switch_Misc_l227)
         3'b000: begin
            stageB_amo_result = stageB_amo_addSub;
         end
         3'b001: begin
            stageB_amo_result = (io_cpu_writeBack_storeData[31 : 0] ^ stageB_dataMux[31 : 0]);
         end
         3'b010: begin
            stageB_amo_result = (io_cpu_writeBack_storeData[31 : 0] | stageB_dataMux[31 : 0]);
         end
         3'b011: begin
            stageB_amo_result = (io_cpu_writeBack_storeData[31 : 0] & stageB_dataMux[31 : 0]);
         end
         default: begin
            stageB_amo_result = (stageB_amo_selectRf ? io_cpu_writeBack_storeData[31 : 0] : stageB_dataMux[31 : 0]);
         end
      endcase
   end

   always @(*) begin
      stageB_cpuWriteToCache = 1'b0;
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (!when_DataCache_l996) begin
               if (when_DataCache_l1009) begin
                  stageB_cpuWriteToCache = 1'b1;
               end
            end
         end
      end
   end

   assign when_DataCache_l931 = (stageB_request_wr && stageB_waysHit);
   assign stageB_badPermissions = (((! stageB_mmuRsp_allowWrite) && stageB_request_wr) || ((! stageB_mmuRsp_allowRead) && ((! stageB_request_wr) || stageB_request_isAmo)));
   assign stageB_loadStoreFault = (io_cpu_writeBack_isValid && (stageB_mmuRsp_exception || stageB_badPermissions));
   always @(*) begin
      io_cpu_redo = 1'b0;
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (!when_DataCache_l996) begin
               if (when_DataCache_l1009) begin
                  if (when_DataCache_l1025) begin
                     io_cpu_redo = 1'b1;
                  end
               end
            end
         end
      end
      if (io_cpu_writeBack_isValid) begin
         if (when_DataCache_l1081) begin
            io_cpu_redo = 1'b1;
         end
      end
      if (when_DataCache_l1129) begin
         io_cpu_redo = 1'b1;
      end
   end

   always @(*) begin
      io_cpu_writeBack_accessError = 1'b0;
      if (stageB_bypassCache) begin
         io_cpu_writeBack_accessError = ((((! stageB_request_wr) && 1'b1) && io_mem_rsp_valid) && io_mem_rsp_payload_error);
      end else begin
         io_cpu_writeBack_accessError = (((stageB_waysHits & stageB_tagsReadRsp_0_error) != 1'b0) || (stageB_loadStoreFault && (! stageB_mmuRsp_isPaging)));
      end
   end

   assign io_cpu_writeBack_mmuException    = (stageB_loadStoreFault && stageB_mmuRsp_isPaging);
   assign io_cpu_writeBack_unalignedAccess = (io_cpu_writeBack_isValid && stageB_unaligned);
   assign io_cpu_writeBack_isWrite         = stageB_request_wr;
   always @(*) begin
      io_mem_cmd_valid = 1'b0;
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (when_DataCache_l996) begin
               io_mem_cmd_valid = (!memCmdSent);
               if (when_DataCache_l1004) begin
                  io_mem_cmd_valid = 1'b0;
               end
            end else begin
               if (when_DataCache_l1009) begin
                  if (stageB_request_wr) begin
                     io_mem_cmd_valid = 1'b1;
                  end
                  if (stageB_request_isAmo) begin
                     if (when_DataCache_l1017) begin
                        io_mem_cmd_valid = 1'b0;
                     end
                  end
                  if (when_DataCache_l1025) begin
                     io_mem_cmd_valid = 1'b0;
                  end
                  if (when_DataCache_l1030) begin
                     io_mem_cmd_valid = 1'b0;
                  end
               end else begin
                  if (when_DataCache_l1037) begin
                     io_mem_cmd_valid = 1'b1;
                  end
               end
            end
         end
      end
      if (io_cpu_writeBack_isValid) begin
         if (when_DataCache_l1072) begin
            io_mem_cmd_valid = 1'b0;
         end
      end
   end

   always @(*) begin
      io_mem_cmd_payload_address = stageB_mmuRsp_physicalAddress;
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (!when_DataCache_l996) begin
               if (!when_DataCache_l1009) begin
                  io_mem_cmd_payload_address[5 : 0] = 6'h00;
               end
            end
         end
      end
   end

   assign io_mem_cmd_payload_last = 1'b1;
   always @(*) begin
      io_mem_cmd_payload_wr = stageB_request_wr;
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (!when_DataCache_l996) begin
               if (!when_DataCache_l1009) begin
                  io_mem_cmd_payload_wr = 1'b0;
               end
            end
         end
      end
   end

   assign io_mem_cmd_payload_mask     = stageB_mask;
   assign io_mem_cmd_payload_data     = stageB_requestDataBypass;
   assign io_mem_cmd_payload_uncached = stageB_mmuRsp_isIoAccess;
   always @(*) begin
      io_mem_cmd_payload_size = {1'd0, stageB_request_size};
      if (io_cpu_writeBack_isValid) begin
         if (!stageB_isExternalAmo) begin
            if (!when_DataCache_l996) begin
               if (!when_DataCache_l1009) begin
                  io_mem_cmd_payload_size = 3'b110;
               end
            end
         end
      end
   end

   assign stageB_bypassCache = ((stageB_mmuRsp_isIoAccess || stageB_isExternalLsrc) || stageB_isExternalAmo);
   assign io_cpu_writeBack_keepMemRspData = 1'b0;
   assign when_DataCache_l1000 = ((! stageB_request_wr) ? (io_mem_rsp_valid && rspSync) : io_mem_cmd_ready);
   assign when_DataCache_l1004 = (stageB_request_isLrsc && (!stageB_lrSc_reserved));
   assign when_DataCache_l1009 = (stageB_waysHit || (stageB_request_wr && (!stageB_request_isAmo)));
   assign when_DataCache_l1014 = ((!stageB_request_wr) || io_mem_cmd_ready);
   assign when_DataCache_l1017 = (!stageB_amo_internal_resultRegValid);
   assign when_DataCache_l1025 = (((! stageB_request_wr) || stageB_request_isAmo) && ((stageB_dataColisions & stageB_waysHits) != 1'b0));
   assign when_DataCache_l1030 = (stageB_request_isLrsc && (!stageB_lrSc_reserved));
   assign when_DataCache_l1037 = (!memCmdSent);
   assign when_DataCache_l996 = (stageB_mmuRsp_isIoAccess || stageB_isExternalLsrc);
   always @(*) begin
      if (stageB_bypassCache) begin
         io_cpu_writeBack_data = stageB_ioMemRspMuxed;
      end else begin
         io_cpu_writeBack_data = stageB_dataMux;
      end
   end

   assign io_cpu_writeBack_exclusiveOk = stageB_lrSc_reserved;
   assign when_DataCache_l1072 = ((((stageB_consistancyHazard || stageB_mmuRsp_refilling) || io_cpu_writeBack_accessError) || io_cpu_writeBack_mmuException) || io_cpu_writeBack_unalignedAccess);
   assign when_DataCache_l1081 = (stageB_mmuRsp_refilling || stageB_consistancyHazard);
   always @(*) begin
      loader_counter_willIncrement = 1'b0;
      if (when_DataCache_l1097) begin
         loader_counter_willIncrement = 1'b1;
      end
   end

   assign loader_counter_willClear = 1'b0;
   assign loader_counter_willOverflowIfInc = (loader_counter_value == 4'b1111);
   assign loader_counter_willOverflow = (loader_counter_willOverflowIfInc && loader_counter_willIncrement);
   always @(*) begin
      loader_counter_valueNext = (loader_counter_value + _zz_loader_counter_valueNext);
      if (loader_counter_willClear) begin
         loader_counter_valueNext = 4'b0000;
      end
   end

   assign loader_kill              = 1'b0;
   assign when_DataCache_l1097     = ((loader_valid && io_mem_rsp_valid) && rspLast);
   assign loader_done              = loader_counter_willOverflow;
   assign when_DataCache_l1125     = (!loader_valid);
   assign when_DataCache_l1129     = (loader_valid && (!loader_valid_regNext));
   assign io_cpu_execute_refilling = loader_valid;
   assign when_DataCache_l1132     = (stageB_loaderValid || loader_valid);
   always @(posedge clk) begin
      tagsWriteLastCmd_valid                <= tagsWriteCmd_valid;
      tagsWriteLastCmd_payload_way          <= tagsWriteCmd_payload_way;
      tagsWriteLastCmd_payload_address      <= tagsWriteCmd_payload_address;
      tagsWriteLastCmd_payload_data_valid   <= tagsWriteCmd_payload_data_valid;
      tagsWriteLastCmd_payload_data_error   <= tagsWriteCmd_payload_data_error;
      tagsWriteLastCmd_payload_data_address <= tagsWriteCmd_payload_data_address;
      if (when_DataCache_l776) begin
         stageA_request_wr               <= io_cpu_execute_args_wr;
         stageA_request_size             <= io_cpu_execute_args_size;
         stageA_request_isLrsc           <= io_cpu_execute_args_isLrsc;
         stageA_request_isAmo            <= io_cpu_execute_args_isAmo;
         stageA_request_amoCtrl_swap     <= io_cpu_execute_args_amoCtrl_swap;
         stageA_request_amoCtrl_alu      <= io_cpu_execute_args_amoCtrl_alu;
         stageA_request_totalyConsistent <= io_cpu_execute_args_totalyConsistent;
      end
      if (when_DataCache_l776_1) begin
         stageA_mask <= stage0_mask;
      end
      if (when_DataCache_l776_2) begin
         stageA_wayInvalidate <= stage0_wayInvalidate;
      end
      if (when_DataCache_l776_3) begin
         stage0_dataColisions_regNextWhen <= stage0_dataColisions;
      end
      if (when_DataCache_l827) begin
         stageB_request_wr               <= stageA_request_wr;
         stageB_request_size             <= stageA_request_size;
         stageB_request_isLrsc           <= stageA_request_isLrsc;
         stageB_request_isAmo            <= stageA_request_isAmo;
         stageB_request_amoCtrl_swap     <= stageA_request_amoCtrl_swap;
         stageB_request_amoCtrl_alu      <= stageA_request_amoCtrl_alu;
         stageB_request_totalyConsistent <= stageA_request_totalyConsistent;
      end
      if (when_DataCache_l829) begin
         stageB_mmuRsp_physicalAddress   <= io_cpu_memory_mmuRsp_physicalAddress;
         stageB_mmuRsp_isIoAccess        <= io_cpu_memory_mmuRsp_isIoAccess;
         stageB_mmuRsp_isPaging          <= io_cpu_memory_mmuRsp_isPaging;
         stageB_mmuRsp_allowRead         <= io_cpu_memory_mmuRsp_allowRead;
         stageB_mmuRsp_allowWrite        <= io_cpu_memory_mmuRsp_allowWrite;
         stageB_mmuRsp_allowExecute      <= io_cpu_memory_mmuRsp_allowExecute;
         stageB_mmuRsp_exception         <= io_cpu_memory_mmuRsp_exception;
         stageB_mmuRsp_refilling         <= io_cpu_memory_mmuRsp_refilling;
         stageB_mmuRsp_bypassTranslation <= io_cpu_memory_mmuRsp_bypassTranslation;
         stageB_mmuRsp_ways_0_sel        <= io_cpu_memory_mmuRsp_ways_0_sel;
         stageB_mmuRsp_ways_0_physical   <= io_cpu_memory_mmuRsp_ways_0_physical;
         stageB_mmuRsp_ways_1_sel        <= io_cpu_memory_mmuRsp_ways_1_sel;
         stageB_mmuRsp_ways_1_physical   <= io_cpu_memory_mmuRsp_ways_1_physical;
         stageB_mmuRsp_ways_2_sel        <= io_cpu_memory_mmuRsp_ways_2_sel;
         stageB_mmuRsp_ways_2_physical   <= io_cpu_memory_mmuRsp_ways_2_physical;
         stageB_mmuRsp_ways_3_sel        <= io_cpu_memory_mmuRsp_ways_3_sel;
         stageB_mmuRsp_ways_3_physical   <= io_cpu_memory_mmuRsp_ways_3_physical;
      end
      if (when_DataCache_l826) begin
         stageB_tagsReadRsp_0_valid   <= ways_0_tagsReadRsp_valid;
         stageB_tagsReadRsp_0_error   <= ways_0_tagsReadRsp_error;
         stageB_tagsReadRsp_0_address <= ways_0_tagsReadRsp_address;
      end
      if (when_DataCache_l826_1) begin
         stageB_dataReadRsp_0 <= ways_0_dataReadRsp;
      end
      if (when_DataCache_l825) begin
         stageB_wayInvalidate <= stageA_wayInvalidate;
      end
      if (when_DataCache_l825_1) begin
         stageB_dataColisions <= stageA_dataColisions;
      end
      if (when_DataCache_l825_2) begin
         stageB_unaligned <= ({((stageA_request_size == 2'b10) && (io_cpu_memory_address[1 : 0] != 2'b00)),((stageA_request_size == 2'b01) && (io_cpu_memory_address[0 : 0] != 1'b0))} != 2'b00);
      end
      if (when_DataCache_l825_3) begin
         stageB_waysHitsBeforeInvalidate <= stageA_wayHits;
      end
      if (when_DataCache_l825_4) begin
         stageB_mask <= stageA_mask;
      end
      stageB_amo_internal_resultRegValid <= io_cpu_writeBack_isStuck;
      stageB_amo_resultReg               <= stageB_amo_result;
      loader_valid_regNext               <= loader_valid;
   end

   always @(posedge clk or posedge reset) begin
      if (reset) begin
         memCmdSent              <= 1'b0;
         stageB_flusher_waitDone <= 1'b0;
         stageB_flusher_counter  <= 7'h00;
         stageB_flusher_start    <= 1'b1;
         stageB_lrSc_reserved    <= 1'b0;
         loader_valid            <= 1'b0;
         loader_counter_value    <= 4'b0000;
         loader_waysAllocator    <= 1'b1;
         loader_error            <= 1'b0;
         loader_killReg          <= 1'b0;
      end else begin
         if (io_mem_cmd_fire) begin
            memCmdSent <= 1'b1;
         end
         if (when_DataCache_l689) begin
            memCmdSent <= 1'b0;
         end
         if (io_cpu_flush_ready) begin
            stageB_flusher_waitDone <= 1'b0;
         end
         if (when_DataCache_l855) begin
            if (when_DataCache_l861) begin
               stageB_flusher_counter <= (stageB_flusher_counter + 7'h01);
               if (when_DataCache_l863) begin
                  stageB_flusher_counter[6] <= 1'b1;
               end
            end
         end
         stageB_flusher_start <= (((((((! stageB_flusher_waitDone) && (! stageB_flusher_start)) && io_cpu_flush_valid) && (! io_cpu_execute_isValid)) && (! io_cpu_memory_isValid)) && (! io_cpu_writeBack_isValid)) && (! io_cpu_redo));
         if (stageB_flusher_start) begin
            stageB_flusher_waitDone <= 1'b1;
            stageB_flusher_counter  <= 7'h00;
            if (when_DataCache_l877) begin
               stageB_flusher_counter <= {1'b0, io_cpu_flush_payload_lineId};
            end
         end
         if (when_DataCache_l885) begin
            if (stageB_request_isLrsc) begin
               stageB_lrSc_reserved <= 1'b1;
            end
            if (stageB_request_wr) begin
               stageB_lrSc_reserved <= 1'b0;
            end
         end
         if (io_cpu_writeBack_isValid) begin
            if (when_DataCache_l1072) begin
               stageB_lrSc_reserved <= stageB_lrSc_reserved;
            end
         end
`ifndef SYNTHESIS
`ifdef FORMAL
         assert((! ((io_cpu_writeBack_isValid && (! io_cpu_writeBack_haltIt)) && io_cpu_writeBack_isStuck))); // DataCache.scala:L1084
`else
         if(!(! ((io_cpu_writeBack_isValid && (! io_cpu_writeBack_haltIt)) && io_cpu_writeBack_isStuck))) begin
            $display(
                "ERROR writeBack stuck by another plugin is not allowed");  // DataCache.scala:L1084
         end
`endif
`endif
         if (stageB_loaderValid) begin
            loader_valid <= 1'b1;
         end
         loader_counter_value <= loader_counter_valueNext;
         if (loader_kill) begin
            loader_killReg <= 1'b1;
         end
         if (when_DataCache_l1097) begin
            loader_error <= (loader_error || io_mem_rsp_payload_error);
         end
         if (loader_done) begin
            loader_valid   <= 1'b0;
            loader_error   <= 1'b0;
            loader_killReg <= 1'b0;
         end
         if (when_DataCache_l1125) begin
            loader_waysAllocator <= _zz_loader_waysAllocator[0:0];
         end
      end
   end


endmodule

module InstructionCache (
   input             io_flush,
   input             io_cpu_prefetch_isValid,
   output reg        io_cpu_prefetch_haltIt,
   input      [31:0] io_cpu_prefetch_pc,
   input             io_cpu_fetch_isValid,
   input             io_cpu_fetch_isStuck,
   input             io_cpu_fetch_isRemoved,
   input      [31:0] io_cpu_fetch_pc,
   output     [31:0] io_cpu_fetch_data,
   input      [31:0] io_cpu_fetch_mmuRsp_physicalAddress,
   input             io_cpu_fetch_mmuRsp_isIoAccess,
   input             io_cpu_fetch_mmuRsp_isPaging,
   input             io_cpu_fetch_mmuRsp_allowRead,
   input             io_cpu_fetch_mmuRsp_allowWrite,
   input             io_cpu_fetch_mmuRsp_allowExecute,
   input             io_cpu_fetch_mmuRsp_exception,
   input             io_cpu_fetch_mmuRsp_refilling,
   input             io_cpu_fetch_mmuRsp_bypassTranslation,
   input             io_cpu_fetch_mmuRsp_ways_0_sel,
   input      [31:0] io_cpu_fetch_mmuRsp_ways_0_physical,
   input             io_cpu_fetch_mmuRsp_ways_1_sel,
   input      [31:0] io_cpu_fetch_mmuRsp_ways_1_physical,
   input             io_cpu_fetch_mmuRsp_ways_2_sel,
   input      [31:0] io_cpu_fetch_mmuRsp_ways_2_physical,
   input             io_cpu_fetch_mmuRsp_ways_3_sel,
   input      [31:0] io_cpu_fetch_mmuRsp_ways_3_physical,
   output     [31:0] io_cpu_fetch_physicalAddress,
   input             io_cpu_decode_isValid,
   input             io_cpu_decode_isStuck,
   input      [31:0] io_cpu_decode_pc,
   output     [31:0] io_cpu_decode_physicalAddress,
   output     [31:0] io_cpu_decode_data,
   output            io_cpu_decode_cacheMiss,
   output            io_cpu_decode_error,
   output            io_cpu_decode_mmuRefilling,
   output            io_cpu_decode_mmuException,
   input             io_cpu_decode_isUser,
   input             io_cpu_fill_valid,
   input      [31:0] io_cpu_fill_payload,
   output            io_mem_cmd_valid,
   input             io_mem_cmd_ready,
   output     [31:0] io_mem_cmd_payload_address,
   output     [ 2:0] io_mem_cmd_payload_size,
   input             io_mem_rsp_valid,
   input      [31:0] io_mem_rsp_payload_data,
   input             io_mem_rsp_payload_error,
   input             clk,
   input             reset
);

   reg  [31:0] _zz_banks_0_port1;
   reg  [21:0] _zz_ways_0_tags_port1;
   wire [21:0] _zz_ways_0_tags_port;
   reg         _zz_1;
   reg         _zz_2;
   reg         lineLoader_fire;
   reg         lineLoader_valid;
   (* keep , syn_keep *)reg  [31:0] lineLoader_address  /* synthesis syn_keep = 1 */;
   reg         lineLoader_hadError;
   reg         lineLoader_flushPending;
   reg  [ 6:0] lineLoader_flushCounter;
   wire        when_InstructionCache_l338;
   reg         _zz_when_InstructionCache_l342;
   wire        when_InstructionCache_l342;
   wire        when_InstructionCache_l351;
   reg         lineLoader_cmdSent;
   wire        io_mem_cmd_fire;
   wire        when_Utils_l538;
   reg         lineLoader_wayToAllocate_willIncrement;
   wire        lineLoader_wayToAllocate_willClear;
   wire        lineLoader_wayToAllocate_willOverflowIfInc;
   wire        lineLoader_wayToAllocate_willOverflow;
   (* keep , syn_keep *)reg  [ 3:0] lineLoader_wordIndex  /* synthesis syn_keep = 1 */;
   wire        lineLoader_write_tag_0_valid;
   wire [ 5:0] lineLoader_write_tag_0_payload_address;
   wire        lineLoader_write_tag_0_payload_data_valid;
   wire        lineLoader_write_tag_0_payload_data_error;
   wire [19:0] lineLoader_write_tag_0_payload_data_address;
   wire        lineLoader_write_data_0_valid;
   wire [ 9:0] lineLoader_write_data_0_payload_address;
   wire [31:0] lineLoader_write_data_0_payload_data;
   wire        when_InstructionCache_l401;
   wire [ 9:0] _zz_fetchStage_read_banksValue_0_dataMem;
   wire        _zz_fetchStage_read_banksValue_0_dataMem_1;
   wire [31:0] fetchStage_read_banksValue_0_dataMem;
   wire [31:0] fetchStage_read_banksValue_0_data;
   wire [ 5:0] _zz_fetchStage_read_waysValues_0_tag_valid;
   wire        _zz_fetchStage_read_waysValues_0_tag_valid_1;
   wire        fetchStage_read_waysValues_0_tag_valid;
   wire        fetchStage_read_waysValues_0_tag_error;
   wire [19:0] fetchStage_read_waysValues_0_tag_address;
   wire [21:0] _zz_fetchStage_read_waysValues_0_tag_valid_2;
   wire        when_InstructionCache_l459;
   reg  [31:0] decodeStage_mmuRsp_physicalAddress;
   reg         decodeStage_mmuRsp_isIoAccess;
   reg         decodeStage_mmuRsp_isPaging;
   reg         decodeStage_mmuRsp_allowRead;
   reg         decodeStage_mmuRsp_allowWrite;
   reg         decodeStage_mmuRsp_allowExecute;
   reg         decodeStage_mmuRsp_exception;
   reg         decodeStage_mmuRsp_refilling;
   reg         decodeStage_mmuRsp_bypassTranslation;
   reg         decodeStage_mmuRsp_ways_0_sel;
   reg  [31:0] decodeStage_mmuRsp_ways_0_physical;
   reg         decodeStage_mmuRsp_ways_1_sel;
   reg  [31:0] decodeStage_mmuRsp_ways_1_physical;
   reg         decodeStage_mmuRsp_ways_2_sel;
   reg  [31:0] decodeStage_mmuRsp_ways_2_physical;
   reg         decodeStage_mmuRsp_ways_3_sel;
   reg  [31:0] decodeStage_mmuRsp_ways_3_physical;
   wire        when_InstructionCache_l459_1;
   reg         decodeStage_hit_tags_0_valid;
   reg         decodeStage_hit_tags_0_error;
   reg  [19:0] decodeStage_hit_tags_0_address;
   wire        decodeStage_hit_hits_0;
   wire        decodeStage_hit_valid;
   wire        when_InstructionCache_l459_2;
   reg  [31:0] _zz_decodeStage_hit_data;
   wire [31:0] decodeStage_hit_data;
   reg  [31:0] banks_0                                            [0:1023];
   reg  [21:0] ways_0_tags                                        [  0:63];

   assign _zz_ways_0_tags_port = {
      lineLoader_write_tag_0_payload_data_address,
      {lineLoader_write_tag_0_payload_data_error, lineLoader_write_tag_0_payload_data_valid}
   };
   always @(posedge clk) begin
      if (_zz_1) begin
         banks_0[lineLoader_write_data_0_payload_address] <= lineLoader_write_data_0_payload_data;
      end
   end

   always @(posedge clk) begin
      if (_zz_fetchStage_read_banksValue_0_dataMem_1) begin
         _zz_banks_0_port1 <= banks_0[_zz_fetchStage_read_banksValue_0_dataMem];
      end
   end

   always @(posedge clk) begin
      if (_zz_2) begin
         ways_0_tags[lineLoader_write_tag_0_payload_address] <= _zz_ways_0_tags_port;
      end
   end

   always @(posedge clk) begin
      if (_zz_fetchStage_read_waysValues_0_tag_valid_1) begin
         _zz_ways_0_tags_port1 <= ways_0_tags[_zz_fetchStage_read_waysValues_0_tag_valid];
      end
   end

   always @(*) begin
      _zz_1 = 1'b0;
      if (lineLoader_write_data_0_valid) begin
         _zz_1 = 1'b1;
      end
   end

   always @(*) begin
      _zz_2 = 1'b0;
      if (lineLoader_write_tag_0_valid) begin
         _zz_2 = 1'b1;
      end
   end

   always @(*) begin
      lineLoader_fire = 1'b0;
      if (io_mem_rsp_valid) begin
         if (when_InstructionCache_l401) begin
            lineLoader_fire = 1'b1;
         end
      end
   end

   always @(*) begin
      io_cpu_prefetch_haltIt = (lineLoader_valid || lineLoader_flushPending);
      if (when_InstructionCache_l338) begin
         io_cpu_prefetch_haltIt = 1'b1;
      end
      if (when_InstructionCache_l342) begin
         io_cpu_prefetch_haltIt = 1'b1;
      end
      if (io_flush) begin
         io_cpu_prefetch_haltIt = 1'b1;
      end
   end

   assign when_InstructionCache_l338 = (!lineLoader_flushCounter[6]);
   assign when_InstructionCache_l342 = (!_zz_when_InstructionCache_l342);
   assign when_InstructionCache_l351 = (lineLoader_flushPending && (! (lineLoader_valid || io_cpu_fetch_isValid)));
   assign io_mem_cmd_fire = (io_mem_cmd_valid && io_mem_cmd_ready);
   assign io_mem_cmd_valid = (lineLoader_valid && (!lineLoader_cmdSent));
   assign io_mem_cmd_payload_address = {lineLoader_address[31 : 6], 6'h00};
   assign io_mem_cmd_payload_size = 3'b110;
   assign when_Utils_l538 = (!lineLoader_valid);
   always @(*) begin
      lineLoader_wayToAllocate_willIncrement = 1'b0;
      if (when_Utils_l538) begin
         lineLoader_wayToAllocate_willIncrement = 1'b1;
      end
   end

   assign lineLoader_wayToAllocate_willClear = 1'b0;
   assign lineLoader_wayToAllocate_willOverflowIfInc = 1'b1;
   assign lineLoader_wayToAllocate_willOverflow = (lineLoader_wayToAllocate_willOverflowIfInc && lineLoader_wayToAllocate_willIncrement);
   assign lineLoader_write_tag_0_valid = ((1'b1 && lineLoader_fire) || (! lineLoader_flushCounter[6]));
   assign lineLoader_write_tag_0_payload_address = (lineLoader_flushCounter[6] ? lineLoader_address[11 : 6] : lineLoader_flushCounter[5 : 0]);
   assign lineLoader_write_tag_0_payload_data_valid = lineLoader_flushCounter[6];
   assign lineLoader_write_tag_0_payload_data_error = (lineLoader_hadError || io_mem_rsp_payload_error);
   assign lineLoader_write_tag_0_payload_data_address = lineLoader_address[31 : 12];
   assign lineLoader_write_data_0_valid = (io_mem_rsp_valid && 1'b1);
   assign lineLoader_write_data_0_payload_address = {
      lineLoader_address[11 : 6], lineLoader_wordIndex
   };
   assign lineLoader_write_data_0_payload_data = io_mem_rsp_payload_data;
   assign when_InstructionCache_l401 = (lineLoader_wordIndex == 4'b1111);
   assign _zz_fetchStage_read_banksValue_0_dataMem = io_cpu_prefetch_pc[11 : 2];
   assign _zz_fetchStage_read_banksValue_0_dataMem_1 = (!io_cpu_fetch_isStuck);
   assign fetchStage_read_banksValue_0_dataMem = _zz_banks_0_port1;
   assign fetchStage_read_banksValue_0_data = fetchStage_read_banksValue_0_dataMem[31 : 0];
   assign _zz_fetchStage_read_waysValues_0_tag_valid = io_cpu_prefetch_pc[11 : 6];
   assign _zz_fetchStage_read_waysValues_0_tag_valid_1 = (!io_cpu_fetch_isStuck);
   assign _zz_fetchStage_read_waysValues_0_tag_valid_2 = _zz_ways_0_tags_port1;
   assign fetchStage_read_waysValues_0_tag_valid = _zz_fetchStage_read_waysValues_0_tag_valid_2[0];
   assign fetchStage_read_waysValues_0_tag_error = _zz_fetchStage_read_waysValues_0_tag_valid_2[1];
   assign fetchStage_read_waysValues_0_tag_address = _zz_fetchStage_read_waysValues_0_tag_valid_2[21 : 2];
   assign io_cpu_fetch_data = fetchStage_read_banksValue_0_data;
   assign io_cpu_fetch_physicalAddress = io_cpu_fetch_mmuRsp_physicalAddress;
   assign when_InstructionCache_l459 = (!io_cpu_decode_isStuck);
   assign when_InstructionCache_l459_1 = (!io_cpu_decode_isStuck);
   assign decodeStage_hit_hits_0 = (decodeStage_hit_tags_0_valid && (decodeStage_hit_tags_0_address == decodeStage_mmuRsp_physicalAddress[31 : 12]));
   assign decodeStage_hit_valid = (|decodeStage_hit_hits_0);
   assign when_InstructionCache_l459_2 = (!io_cpu_decode_isStuck);
   assign decodeStage_hit_data = _zz_decodeStage_hit_data;
   assign io_cpu_decode_data = decodeStage_hit_data;
   assign io_cpu_decode_cacheMiss = (!decodeStage_hit_valid);
   assign io_cpu_decode_error = (decodeStage_hit_tags_0_error || ((! decodeStage_mmuRsp_isPaging) && (decodeStage_mmuRsp_exception || (! decodeStage_mmuRsp_allowExecute))));
   assign io_cpu_decode_mmuRefilling = decodeStage_mmuRsp_refilling;
   assign io_cpu_decode_mmuException = (((! decodeStage_mmuRsp_refilling) && decodeStage_mmuRsp_isPaging) && (decodeStage_mmuRsp_exception || (! decodeStage_mmuRsp_allowExecute)));
   assign io_cpu_decode_physicalAddress = decodeStage_mmuRsp_physicalAddress;
   always @(posedge clk or posedge reset) begin
      if (reset) begin
         lineLoader_valid        <= 1'b0;
         lineLoader_hadError     <= 1'b0;
         lineLoader_flushPending <= 1'b1;
         lineLoader_cmdSent      <= 1'b0;
         lineLoader_wordIndex    <= 4'b0000;
      end else begin
         if (lineLoader_fire) begin
            lineLoader_valid <= 1'b0;
         end
         if (lineLoader_fire) begin
            lineLoader_hadError <= 1'b0;
         end
         if (io_cpu_fill_valid) begin
            lineLoader_valid <= 1'b1;
         end
         if (io_flush) begin
            lineLoader_flushPending <= 1'b1;
         end
         if (when_InstructionCache_l351) begin
            lineLoader_flushPending <= 1'b0;
         end
         if (io_mem_cmd_fire) begin
            lineLoader_cmdSent <= 1'b1;
         end
         if (lineLoader_fire) begin
            lineLoader_cmdSent <= 1'b0;
         end
         if (io_mem_rsp_valid) begin
            lineLoader_wordIndex <= (lineLoader_wordIndex + 4'b0001);
            if (io_mem_rsp_payload_error) begin
               lineLoader_hadError <= 1'b1;
            end
         end
      end
   end

   always @(posedge clk) begin
      if (io_cpu_fill_valid) begin
         lineLoader_address <= io_cpu_fill_payload;
      end
      if (when_InstructionCache_l338) begin
         lineLoader_flushCounter <= (lineLoader_flushCounter + 7'h01);
      end
      _zz_when_InstructionCache_l342 <= lineLoader_flushCounter[6];
      if (when_InstructionCache_l351) begin
         lineLoader_flushCounter <= 7'h00;
      end
      if (when_InstructionCache_l459) begin
         decodeStage_mmuRsp_physicalAddress   <= io_cpu_fetch_mmuRsp_physicalAddress;
         decodeStage_mmuRsp_isIoAccess        <= io_cpu_fetch_mmuRsp_isIoAccess;
         decodeStage_mmuRsp_isPaging          <= io_cpu_fetch_mmuRsp_isPaging;
         decodeStage_mmuRsp_allowRead         <= io_cpu_fetch_mmuRsp_allowRead;
         decodeStage_mmuRsp_allowWrite        <= io_cpu_fetch_mmuRsp_allowWrite;
         decodeStage_mmuRsp_allowExecute      <= io_cpu_fetch_mmuRsp_allowExecute;
         decodeStage_mmuRsp_exception         <= io_cpu_fetch_mmuRsp_exception;
         decodeStage_mmuRsp_refilling         <= io_cpu_fetch_mmuRsp_refilling;
         decodeStage_mmuRsp_bypassTranslation <= io_cpu_fetch_mmuRsp_bypassTranslation;
         decodeStage_mmuRsp_ways_0_sel        <= io_cpu_fetch_mmuRsp_ways_0_sel;
         decodeStage_mmuRsp_ways_0_physical   <= io_cpu_fetch_mmuRsp_ways_0_physical;
         decodeStage_mmuRsp_ways_1_sel        <= io_cpu_fetch_mmuRsp_ways_1_sel;
         decodeStage_mmuRsp_ways_1_physical   <= io_cpu_fetch_mmuRsp_ways_1_physical;
         decodeStage_mmuRsp_ways_2_sel        <= io_cpu_fetch_mmuRsp_ways_2_sel;
         decodeStage_mmuRsp_ways_2_physical   <= io_cpu_fetch_mmuRsp_ways_2_physical;
         decodeStage_mmuRsp_ways_3_sel        <= io_cpu_fetch_mmuRsp_ways_3_sel;
         decodeStage_mmuRsp_ways_3_physical   <= io_cpu_fetch_mmuRsp_ways_3_physical;
      end
      if (when_InstructionCache_l459_1) begin
         decodeStage_hit_tags_0_valid   <= fetchStage_read_waysValues_0_tag_valid;
         decodeStage_hit_tags_0_error   <= fetchStage_read_waysValues_0_tag_error;
         decodeStage_hit_tags_0_address <= fetchStage_read_waysValues_0_tag_address;
      end
      if (when_InstructionCache_l459_2) begin
         _zz_decodeStage_hit_data <= fetchStage_read_banksValue_0_data;
      end
   end


endmodule

module AxiLite4Plic (
   input             io_bus_aw_valid,
   output            io_bus_aw_ready,
   input      [21:0] io_bus_aw_payload_addr,
   input      [ 2:0] io_bus_aw_payload_prot,
   input             io_bus_w_valid,
   output            io_bus_w_ready,
   input      [31:0] io_bus_w_payload_data,
   input      [ 3:0] io_bus_w_payload_strb,
   output            io_bus_b_valid,
   input             io_bus_b_ready,
   output     [ 1:0] io_bus_b_payload_resp,
   input             io_bus_ar_valid,
   output reg        io_bus_ar_ready,
   input      [21:0] io_bus_ar_payload_addr,
   input      [ 2:0] io_bus_ar_payload_prot,
   output            io_bus_r_valid,
   input             io_bus_r_ready,
   output     [31:0] io_bus_r_payload_data,
   output     [ 1:0] io_bus_r_payload_resp,
   input      [30:0] io_sources,
   output     [ 1:0] io_targets,
   input             clk,
   input             reset
);

   wire [ 4:0] _zz_targets_0_bestRequest_id_82;
   wire [ 4:0] _zz_targets_0_bestRequest_id_83;
   wire [ 4:0] _zz_targets_0_bestRequest_id_84;
   wire [ 4:0] _zz_targets_0_bestRequest_id_85;
   wire [ 4:0] _zz_targets_0_bestRequest_id_86;
   wire [ 4:0] _zz_targets_0_bestRequest_id_87;
   wire [ 4:0] _zz_targets_0_bestRequest_id_88;
   wire [ 4:0] _zz_targets_0_bestRequest_id_89;
   wire [ 4:0] _zz_targets_0_bestRequest_id_90;
   wire [ 4:0] _zz_targets_0_bestRequest_id_91;
   wire [ 4:0] _zz_targets_0_bestRequest_id_92;
   wire [ 4:0] _zz_targets_0_bestRequest_id_93;
   wire [ 4:0] _zz_targets_0_bestRequest_id_94;
   wire [ 4:0] _zz_targets_0_bestRequest_id_95;
   wire [ 4:0] _zz_targets_0_bestRequest_id_96;
   wire [ 4:0] _zz_targets_0_bestRequest_id_97;
   wire [ 4:0] _zz_targets_1_bestRequest_id_82;
   wire [ 4:0] _zz_targets_1_bestRequest_id_83;
   wire [ 4:0] _zz_targets_1_bestRequest_id_84;
   wire [ 4:0] _zz_targets_1_bestRequest_id_85;
   wire [ 4:0] _zz_targets_1_bestRequest_id_86;
   wire [ 4:0] _zz_targets_1_bestRequest_id_87;
   wire [ 4:0] _zz_targets_1_bestRequest_id_88;
   wire [ 4:0] _zz_targets_1_bestRequest_id_89;
   wire [ 4:0] _zz_targets_1_bestRequest_id_90;
   wire [ 4:0] _zz_targets_1_bestRequest_id_91;
   wire [ 4:0] _zz_targets_1_bestRequest_id_92;
   wire [ 4:0] _zz_targets_1_bestRequest_id_93;
   wire [ 4:0] _zz_targets_1_bestRequest_id_94;
   wire [ 4:0] _zz_targets_1_bestRequest_id_95;
   wire [ 4:0] _zz_targets_1_bestRequest_id_96;
   wire [ 4:0] _zz_targets_1_bestRequest_id_97;
   wire        _zz_gateways_0_ip;
   wire        _zz_gateways_1_ip;
   wire        _zz_gateways_2_ip;
   wire        _zz_gateways_3_ip;
   wire        _zz_gateways_4_ip;
   wire        _zz_gateways_5_ip;
   wire        _zz_gateways_6_ip;
   wire        _zz_gateways_7_ip;
   wire        _zz_gateways_8_ip;
   wire        _zz_gateways_9_ip;
   wire        _zz_gateways_10_ip;
   wire        _zz_gateways_11_ip;
   wire        _zz_gateways_12_ip;
   wire        _zz_gateways_13_ip;
   wire        _zz_gateways_14_ip;
   wire        _zz_gateways_15_ip;
   wire        _zz_gateways_16_ip;
   wire        _zz_gateways_17_ip;
   wire        _zz_gateways_18_ip;
   wire        _zz_gateways_19_ip;
   wire        _zz_gateways_20_ip;
   wire        _zz_gateways_21_ip;
   wire        _zz_gateways_22_ip;
   wire        _zz_gateways_23_ip;
   wire        _zz_gateways_24_ip;
   wire        _zz_gateways_25_ip;
   wire        _zz_gateways_26_ip;
   wire        _zz_gateways_27_ip;
   wire        _zz_gateways_28_ip;
   wire        _zz_gateways_29_ip;
   wire        _zz_gateways_30_ip;
   wire [ 1:0] gateways_0_priority;
   reg         gateways_0_ip;
   reg         gateways_0_waitCompletion;
   wire        when_PlicGateway_l21;
   wire [ 1:0] gateways_1_priority;
   reg         gateways_1_ip;
   reg         gateways_1_waitCompletion;
   wire        when_PlicGateway_l21_1;
   wire [ 1:0] gateways_2_priority;
   reg         gateways_2_ip;
   reg         gateways_2_waitCompletion;
   wire        when_PlicGateway_l21_2;
   wire [ 1:0] gateways_3_priority;
   reg         gateways_3_ip;
   reg         gateways_3_waitCompletion;
   wire        when_PlicGateway_l21_3;
   wire [ 1:0] gateways_4_priority;
   reg         gateways_4_ip;
   reg         gateways_4_waitCompletion;
   wire        when_PlicGateway_l21_4;
   wire [ 1:0] gateways_5_priority;
   reg         gateways_5_ip;
   reg         gateways_5_waitCompletion;
   wire        when_PlicGateway_l21_5;
   wire [ 1:0] gateways_6_priority;
   reg         gateways_6_ip;
   reg         gateways_6_waitCompletion;
   wire        when_PlicGateway_l21_6;
   wire [ 1:0] gateways_7_priority;
   reg         gateways_7_ip;
   reg         gateways_7_waitCompletion;
   wire        when_PlicGateway_l21_7;
   wire [ 1:0] gateways_8_priority;
   reg         gateways_8_ip;
   reg         gateways_8_waitCompletion;
   wire        when_PlicGateway_l21_8;
   wire [ 1:0] gateways_9_priority;
   reg         gateways_9_ip;
   reg         gateways_9_waitCompletion;
   wire        when_PlicGateway_l21_9;
   wire [ 1:0] gateways_10_priority;
   reg         gateways_10_ip;
   reg         gateways_10_waitCompletion;
   wire        when_PlicGateway_l21_10;
   wire [ 1:0] gateways_11_priority;
   reg         gateways_11_ip;
   reg         gateways_11_waitCompletion;
   wire        when_PlicGateway_l21_11;
   wire [ 1:0] gateways_12_priority;
   reg         gateways_12_ip;
   reg         gateways_12_waitCompletion;
   wire        when_PlicGateway_l21_12;
   wire [ 1:0] gateways_13_priority;
   reg         gateways_13_ip;
   reg         gateways_13_waitCompletion;
   wire        when_PlicGateway_l21_13;
   wire [ 1:0] gateways_14_priority;
   reg         gateways_14_ip;
   reg         gateways_14_waitCompletion;
   wire        when_PlicGateway_l21_14;
   wire [ 1:0] gateways_15_priority;
   reg         gateways_15_ip;
   reg         gateways_15_waitCompletion;
   wire        when_PlicGateway_l21_15;
   wire [ 1:0] gateways_16_priority;
   reg         gateways_16_ip;
   reg         gateways_16_waitCompletion;
   wire        when_PlicGateway_l21_16;
   wire [ 1:0] gateways_17_priority;
   reg         gateways_17_ip;
   reg         gateways_17_waitCompletion;
   wire        when_PlicGateway_l21_17;
   wire [ 1:0] gateways_18_priority;
   reg         gateways_18_ip;
   reg         gateways_18_waitCompletion;
   wire        when_PlicGateway_l21_18;
   wire [ 1:0] gateways_19_priority;
   reg         gateways_19_ip;
   reg         gateways_19_waitCompletion;
   wire        when_PlicGateway_l21_19;
   wire [ 1:0] gateways_20_priority;
   reg         gateways_20_ip;
   reg         gateways_20_waitCompletion;
   wire        when_PlicGateway_l21_20;
   wire [ 1:0] gateways_21_priority;
   reg         gateways_21_ip;
   reg         gateways_21_waitCompletion;
   wire        when_PlicGateway_l21_21;
   wire [ 1:0] gateways_22_priority;
   reg         gateways_22_ip;
   reg         gateways_22_waitCompletion;
   wire        when_PlicGateway_l21_22;
   wire [ 1:0] gateways_23_priority;
   reg         gateways_23_ip;
   reg         gateways_23_waitCompletion;
   wire        when_PlicGateway_l21_23;
   wire [ 1:0] gateways_24_priority;
   reg         gateways_24_ip;
   reg         gateways_24_waitCompletion;
   wire        when_PlicGateway_l21_24;
   wire [ 1:0] gateways_25_priority;
   reg         gateways_25_ip;
   reg         gateways_25_waitCompletion;
   wire        when_PlicGateway_l21_25;
   wire [ 1:0] gateways_26_priority;
   reg         gateways_26_ip;
   reg         gateways_26_waitCompletion;
   wire        when_PlicGateway_l21_26;
   wire [ 1:0] gateways_27_priority;
   reg         gateways_27_ip;
   reg         gateways_27_waitCompletion;
   wire        when_PlicGateway_l21_27;
   wire [ 1:0] gateways_28_priority;
   reg         gateways_28_ip;
   reg         gateways_28_waitCompletion;
   wire        when_PlicGateway_l21_28;
   wire [ 1:0] gateways_29_priority;
   reg         gateways_29_ip;
   reg         gateways_29_waitCompletion;
   wire        when_PlicGateway_l21_29;
   wire [ 1:0] gateways_30_priority;
   reg         gateways_30_ip;
   reg         gateways_30_waitCompletion;
   wire        when_PlicGateway_l21_30;
   wire        targets_0_ie_0;
   wire        targets_0_ie_1;
   wire        targets_0_ie_2;
   wire        targets_0_ie_3;
   wire        targets_0_ie_4;
   wire        targets_0_ie_5;
   wire        targets_0_ie_6;
   wire        targets_0_ie_7;
   wire        targets_0_ie_8;
   wire        targets_0_ie_9;
   wire        targets_0_ie_10;
   wire        targets_0_ie_11;
   wire        targets_0_ie_12;
   wire        targets_0_ie_13;
   wire        targets_0_ie_14;
   wire        targets_0_ie_15;
   wire        targets_0_ie_16;
   wire        targets_0_ie_17;
   wire        targets_0_ie_18;
   wire        targets_0_ie_19;
   wire        targets_0_ie_20;
   wire        targets_0_ie_21;
   wire        targets_0_ie_22;
   wire        targets_0_ie_23;
   wire        targets_0_ie_24;
   wire        targets_0_ie_25;
   wire        targets_0_ie_26;
   wire        targets_0_ie_27;
   wire        targets_0_ie_28;
   wire        targets_0_ie_29;
   wire        targets_0_ie_30;
   wire [ 1:0] targets_0_threshold;
   wire [ 1:0] targets_0_requests_0_priority;
   wire [ 4:0] targets_0_requests_0_id;
   wire        targets_0_requests_0_valid;
   wire [ 1:0] targets_0_requests_1_priority;
   wire [ 4:0] targets_0_requests_1_id;
   wire        targets_0_requests_1_valid;
   wire [ 1:0] targets_0_requests_2_priority;
   wire [ 4:0] targets_0_requests_2_id;
   wire        targets_0_requests_2_valid;
   wire [ 1:0] targets_0_requests_3_priority;
   wire [ 4:0] targets_0_requests_3_id;
   wire        targets_0_requests_3_valid;
   wire [ 1:0] targets_0_requests_4_priority;
   wire [ 4:0] targets_0_requests_4_id;
   wire        targets_0_requests_4_valid;
   wire [ 1:0] targets_0_requests_5_priority;
   wire [ 4:0] targets_0_requests_5_id;
   wire        targets_0_requests_5_valid;
   wire [ 1:0] targets_0_requests_6_priority;
   wire [ 4:0] targets_0_requests_6_id;
   wire        targets_0_requests_6_valid;
   wire [ 1:0] targets_0_requests_7_priority;
   wire [ 4:0] targets_0_requests_7_id;
   wire        targets_0_requests_7_valid;
   wire [ 1:0] targets_0_requests_8_priority;
   wire [ 4:0] targets_0_requests_8_id;
   wire        targets_0_requests_8_valid;
   wire [ 1:0] targets_0_requests_9_priority;
   wire [ 4:0] targets_0_requests_9_id;
   wire        targets_0_requests_9_valid;
   wire [ 1:0] targets_0_requests_10_priority;
   wire [ 4:0] targets_0_requests_10_id;
   wire        targets_0_requests_10_valid;
   wire [ 1:0] targets_0_requests_11_priority;
   wire [ 4:0] targets_0_requests_11_id;
   wire        targets_0_requests_11_valid;
   wire [ 1:0] targets_0_requests_12_priority;
   wire [ 4:0] targets_0_requests_12_id;
   wire        targets_0_requests_12_valid;
   wire [ 1:0] targets_0_requests_13_priority;
   wire [ 4:0] targets_0_requests_13_id;
   wire        targets_0_requests_13_valid;
   wire [ 1:0] targets_0_requests_14_priority;
   wire [ 4:0] targets_0_requests_14_id;
   wire        targets_0_requests_14_valid;
   wire [ 1:0] targets_0_requests_15_priority;
   wire [ 4:0] targets_0_requests_15_id;
   wire        targets_0_requests_15_valid;
   wire [ 1:0] targets_0_requests_16_priority;
   wire [ 4:0] targets_0_requests_16_id;
   wire        targets_0_requests_16_valid;
   wire [ 1:0] targets_0_requests_17_priority;
   wire [ 4:0] targets_0_requests_17_id;
   wire        targets_0_requests_17_valid;
   wire [ 1:0] targets_0_requests_18_priority;
   wire [ 4:0] targets_0_requests_18_id;
   wire        targets_0_requests_18_valid;
   wire [ 1:0] targets_0_requests_19_priority;
   wire [ 4:0] targets_0_requests_19_id;
   wire        targets_0_requests_19_valid;
   wire [ 1:0] targets_0_requests_20_priority;
   wire [ 4:0] targets_0_requests_20_id;
   wire        targets_0_requests_20_valid;
   wire [ 1:0] targets_0_requests_21_priority;
   wire [ 4:0] targets_0_requests_21_id;
   wire        targets_0_requests_21_valid;
   wire [ 1:0] targets_0_requests_22_priority;
   wire [ 4:0] targets_0_requests_22_id;
   wire        targets_0_requests_22_valid;
   wire [ 1:0] targets_0_requests_23_priority;
   wire [ 4:0] targets_0_requests_23_id;
   wire        targets_0_requests_23_valid;
   wire [ 1:0] targets_0_requests_24_priority;
   wire [ 4:0] targets_0_requests_24_id;
   wire        targets_0_requests_24_valid;
   wire [ 1:0] targets_0_requests_25_priority;
   wire [ 4:0] targets_0_requests_25_id;
   wire        targets_0_requests_25_valid;
   wire [ 1:0] targets_0_requests_26_priority;
   wire [ 4:0] targets_0_requests_26_id;
   wire        targets_0_requests_26_valid;
   wire [ 1:0] targets_0_requests_27_priority;
   wire [ 4:0] targets_0_requests_27_id;
   wire        targets_0_requests_27_valid;
   wire [ 1:0] targets_0_requests_28_priority;
   wire [ 4:0] targets_0_requests_28_id;
   wire        targets_0_requests_28_valid;
   wire [ 1:0] targets_0_requests_29_priority;
   wire [ 4:0] targets_0_requests_29_id;
   wire        targets_0_requests_29_valid;
   wire [ 1:0] targets_0_requests_30_priority;
   wire [ 4:0] targets_0_requests_30_id;
   wire        targets_0_requests_30_valid;
   wire [ 1:0] targets_0_requests_31_priority;
   wire [ 4:0] targets_0_requests_31_id;
   wire        targets_0_requests_31_valid;
   wire        _zz_targets_0_bestRequest_id;
   wire [ 1:0] _zz_targets_0_bestRequest_id_1;
   wire        _zz_targets_0_bestRequest_id_2;
   wire        _zz_targets_0_bestRequest_id_3;
   wire [ 1:0] _zz_targets_0_bestRequest_id_4;
   wire        _zz_targets_0_bestRequest_id_5;
   wire        _zz_targets_0_bestRequest_id_6;
   wire [ 1:0] _zz_targets_0_bestRequest_id_7;
   wire        _zz_targets_0_bestRequest_id_8;
   wire        _zz_targets_0_bestRequest_id_9;
   wire [ 1:0] _zz_targets_0_bestRequest_id_10;
   wire        _zz_targets_0_bestRequest_id_11;
   wire        _zz_targets_0_bestRequest_id_12;
   wire [ 1:0] _zz_targets_0_bestRequest_id_13;
   wire        _zz_targets_0_bestRequest_id_14;
   wire        _zz_targets_0_bestRequest_id_15;
   wire [ 1:0] _zz_targets_0_bestRequest_id_16;
   wire        _zz_targets_0_bestRequest_id_17;
   wire        _zz_targets_0_bestRequest_id_18;
   wire [ 1:0] _zz_targets_0_bestRequest_id_19;
   wire        _zz_targets_0_bestRequest_id_20;
   wire        _zz_targets_0_bestRequest_id_21;
   wire [ 1:0] _zz_targets_0_bestRequest_id_22;
   wire        _zz_targets_0_bestRequest_id_23;
   wire        _zz_targets_0_bestRequest_id_24;
   wire [ 1:0] _zz_targets_0_bestRequest_id_25;
   wire        _zz_targets_0_bestRequest_id_26;
   wire        _zz_targets_0_bestRequest_id_27;
   wire [ 1:0] _zz_targets_0_bestRequest_id_28;
   wire        _zz_targets_0_bestRequest_id_29;
   wire        _zz_targets_0_bestRequest_id_30;
   wire [ 1:0] _zz_targets_0_bestRequest_id_31;
   wire        _zz_targets_0_bestRequest_id_32;
   wire        _zz_targets_0_bestRequest_id_33;
   wire [ 1:0] _zz_targets_0_bestRequest_id_34;
   wire        _zz_targets_0_bestRequest_id_35;
   wire        _zz_targets_0_bestRequest_id_36;
   wire [ 1:0] _zz_targets_0_bestRequest_id_37;
   wire        _zz_targets_0_bestRequest_id_38;
   wire        _zz_targets_0_bestRequest_id_39;
   wire [ 1:0] _zz_targets_0_bestRequest_id_40;
   wire        _zz_targets_0_bestRequest_id_41;
   wire        _zz_targets_0_bestRequest_id_42;
   wire [ 1:0] _zz_targets_0_bestRequest_id_43;
   wire        _zz_targets_0_bestRequest_id_44;
   wire        _zz_targets_0_bestRequest_id_45;
   wire [ 1:0] _zz_targets_0_bestRequest_id_46;
   wire        _zz_targets_0_bestRequest_id_47;
   wire        _zz_targets_0_bestRequest_id_48;
   wire [ 1:0] _zz_targets_0_bestRequest_id_49;
   wire        _zz_targets_0_bestRequest_id_50;
   wire        _zz_targets_0_bestRequest_id_51;
   wire [ 1:0] _zz_targets_0_bestRequest_id_52;
   wire        _zz_targets_0_bestRequest_id_53;
   wire        _zz_targets_0_bestRequest_id_54;
   wire [ 1:0] _zz_targets_0_bestRequest_id_55;
   wire        _zz_targets_0_bestRequest_id_56;
   wire        _zz_targets_0_bestRequest_id_57;
   wire [ 1:0] _zz_targets_0_bestRequest_id_58;
   wire        _zz_targets_0_bestRequest_id_59;
   wire        _zz_targets_0_bestRequest_id_60;
   wire [ 1:0] _zz_targets_0_bestRequest_id_61;
   wire        _zz_targets_0_bestRequest_id_62;
   wire        _zz_targets_0_bestRequest_id_63;
   wire [ 1:0] _zz_targets_0_bestRequest_id_64;
   wire        _zz_targets_0_bestRequest_id_65;
   wire        _zz_targets_0_bestRequest_id_66;
   wire [ 1:0] _zz_targets_0_bestRequest_id_67;
   wire        _zz_targets_0_bestRequest_id_68;
   wire        _zz_targets_0_bestRequest_id_69;
   wire [ 1:0] _zz_targets_0_bestRequest_id_70;
   wire        _zz_targets_0_bestRequest_id_71;
   wire        _zz_targets_0_bestRequest_id_72;
   wire [ 1:0] _zz_targets_0_bestRequest_priority;
   wire        _zz_targets_0_bestRequest_id_73;
   wire        _zz_targets_0_bestRequest_id_74;
   wire [ 1:0] _zz_targets_0_bestRequest_priority_1;
   wire        _zz_targets_0_bestRequest_id_75;
   wire        _zz_targets_0_bestRequest_id_76;
   wire [ 1:0] _zz_targets_0_bestRequest_priority_2;
   wire        _zz_targets_0_bestRequest_id_77;
   wire        _zz_targets_0_bestRequest_id_78;
   wire [ 1:0] _zz_targets_0_bestRequest_priority_3;
   wire        _zz_targets_0_bestRequest_id_79;
   wire        _zz_targets_0_bestRequest_id_80;
   wire [ 1:0] _zz_targets_0_bestRequest_priority_4;
   wire        _zz_targets_0_bestRequest_valid;
   wire        _zz_targets_0_bestRequest_id_81;
   wire [ 1:0] _zz_targets_0_bestRequest_priority_5;
   wire        _zz_targets_0_bestRequest_valid_1;
   wire        _zz_targets_0_bestRequest_priority_6;
   reg  [ 1:0] targets_0_bestRequest_priority;
   reg  [ 4:0] targets_0_bestRequest_id;
   reg         targets_0_bestRequest_valid;
   wire        targets_0_iep;
   wire [ 4:0] targets_0_claim;
   wire        targets_1_ie_0;
   wire        targets_1_ie_1;
   wire        targets_1_ie_2;
   wire        targets_1_ie_3;
   wire        targets_1_ie_4;
   wire        targets_1_ie_5;
   wire        targets_1_ie_6;
   wire        targets_1_ie_7;
   wire        targets_1_ie_8;
   wire        targets_1_ie_9;
   wire        targets_1_ie_10;
   wire        targets_1_ie_11;
   wire        targets_1_ie_12;
   wire        targets_1_ie_13;
   wire        targets_1_ie_14;
   wire        targets_1_ie_15;
   wire        targets_1_ie_16;
   wire        targets_1_ie_17;
   wire        targets_1_ie_18;
   wire        targets_1_ie_19;
   wire        targets_1_ie_20;
   wire        targets_1_ie_21;
   wire        targets_1_ie_22;
   wire        targets_1_ie_23;
   wire        targets_1_ie_24;
   wire        targets_1_ie_25;
   wire        targets_1_ie_26;
   wire        targets_1_ie_27;
   wire        targets_1_ie_28;
   wire        targets_1_ie_29;
   wire        targets_1_ie_30;
   wire [ 1:0] targets_1_threshold;
   wire [ 1:0] targets_1_requests_0_priority;
   wire [ 4:0] targets_1_requests_0_id;
   wire        targets_1_requests_0_valid;
   wire [ 1:0] targets_1_requests_1_priority;
   wire [ 4:0] targets_1_requests_1_id;
   wire        targets_1_requests_1_valid;
   wire [ 1:0] targets_1_requests_2_priority;
   wire [ 4:0] targets_1_requests_2_id;
   wire        targets_1_requests_2_valid;
   wire [ 1:0] targets_1_requests_3_priority;
   wire [ 4:0] targets_1_requests_3_id;
   wire        targets_1_requests_3_valid;
   wire [ 1:0] targets_1_requests_4_priority;
   wire [ 4:0] targets_1_requests_4_id;
   wire        targets_1_requests_4_valid;
   wire [ 1:0] targets_1_requests_5_priority;
   wire [ 4:0] targets_1_requests_5_id;
   wire        targets_1_requests_5_valid;
   wire [ 1:0] targets_1_requests_6_priority;
   wire [ 4:0] targets_1_requests_6_id;
   wire        targets_1_requests_6_valid;
   wire [ 1:0] targets_1_requests_7_priority;
   wire [ 4:0] targets_1_requests_7_id;
   wire        targets_1_requests_7_valid;
   wire [ 1:0] targets_1_requests_8_priority;
   wire [ 4:0] targets_1_requests_8_id;
   wire        targets_1_requests_8_valid;
   wire [ 1:0] targets_1_requests_9_priority;
   wire [ 4:0] targets_1_requests_9_id;
   wire        targets_1_requests_9_valid;
   wire [ 1:0] targets_1_requests_10_priority;
   wire [ 4:0] targets_1_requests_10_id;
   wire        targets_1_requests_10_valid;
   wire [ 1:0] targets_1_requests_11_priority;
   wire [ 4:0] targets_1_requests_11_id;
   wire        targets_1_requests_11_valid;
   wire [ 1:0] targets_1_requests_12_priority;
   wire [ 4:0] targets_1_requests_12_id;
   wire        targets_1_requests_12_valid;
   wire [ 1:0] targets_1_requests_13_priority;
   wire [ 4:0] targets_1_requests_13_id;
   wire        targets_1_requests_13_valid;
   wire [ 1:0] targets_1_requests_14_priority;
   wire [ 4:0] targets_1_requests_14_id;
   wire        targets_1_requests_14_valid;
   wire [ 1:0] targets_1_requests_15_priority;
   wire [ 4:0] targets_1_requests_15_id;
   wire        targets_1_requests_15_valid;
   wire [ 1:0] targets_1_requests_16_priority;
   wire [ 4:0] targets_1_requests_16_id;
   wire        targets_1_requests_16_valid;
   wire [ 1:0] targets_1_requests_17_priority;
   wire [ 4:0] targets_1_requests_17_id;
   wire        targets_1_requests_17_valid;
   wire [ 1:0] targets_1_requests_18_priority;
   wire [ 4:0] targets_1_requests_18_id;
   wire        targets_1_requests_18_valid;
   wire [ 1:0] targets_1_requests_19_priority;
   wire [ 4:0] targets_1_requests_19_id;
   wire        targets_1_requests_19_valid;
   wire [ 1:0] targets_1_requests_20_priority;
   wire [ 4:0] targets_1_requests_20_id;
   wire        targets_1_requests_20_valid;
   wire [ 1:0] targets_1_requests_21_priority;
   wire [ 4:0] targets_1_requests_21_id;
   wire        targets_1_requests_21_valid;
   wire [ 1:0] targets_1_requests_22_priority;
   wire [ 4:0] targets_1_requests_22_id;
   wire        targets_1_requests_22_valid;
   wire [ 1:0] targets_1_requests_23_priority;
   wire [ 4:0] targets_1_requests_23_id;
   wire        targets_1_requests_23_valid;
   wire [ 1:0] targets_1_requests_24_priority;
   wire [ 4:0] targets_1_requests_24_id;
   wire        targets_1_requests_24_valid;
   wire [ 1:0] targets_1_requests_25_priority;
   wire [ 4:0] targets_1_requests_25_id;
   wire        targets_1_requests_25_valid;
   wire [ 1:0] targets_1_requests_26_priority;
   wire [ 4:0] targets_1_requests_26_id;
   wire        targets_1_requests_26_valid;
   wire [ 1:0] targets_1_requests_27_priority;
   wire [ 4:0] targets_1_requests_27_id;
   wire        targets_1_requests_27_valid;
   wire [ 1:0] targets_1_requests_28_priority;
   wire [ 4:0] targets_1_requests_28_id;
   wire        targets_1_requests_28_valid;
   wire [ 1:0] targets_1_requests_29_priority;
   wire [ 4:0] targets_1_requests_29_id;
   wire        targets_1_requests_29_valid;
   wire [ 1:0] targets_1_requests_30_priority;
   wire [ 4:0] targets_1_requests_30_id;
   wire        targets_1_requests_30_valid;
   wire [ 1:0] targets_1_requests_31_priority;
   wire [ 4:0] targets_1_requests_31_id;
   wire        targets_1_requests_31_valid;
   wire        _zz_targets_1_bestRequest_id;
   wire [ 1:0] _zz_targets_1_bestRequest_id_1;
   wire        _zz_targets_1_bestRequest_id_2;
   wire        _zz_targets_1_bestRequest_id_3;
   wire [ 1:0] _zz_targets_1_bestRequest_id_4;
   wire        _zz_targets_1_bestRequest_id_5;
   wire        _zz_targets_1_bestRequest_id_6;
   wire [ 1:0] _zz_targets_1_bestRequest_id_7;
   wire        _zz_targets_1_bestRequest_id_8;
   wire        _zz_targets_1_bestRequest_id_9;
   wire [ 1:0] _zz_targets_1_bestRequest_id_10;
   wire        _zz_targets_1_bestRequest_id_11;
   wire        _zz_targets_1_bestRequest_id_12;
   wire [ 1:0] _zz_targets_1_bestRequest_id_13;
   wire        _zz_targets_1_bestRequest_id_14;
   wire        _zz_targets_1_bestRequest_id_15;
   wire [ 1:0] _zz_targets_1_bestRequest_id_16;
   wire        _zz_targets_1_bestRequest_id_17;
   wire        _zz_targets_1_bestRequest_id_18;
   wire [ 1:0] _zz_targets_1_bestRequest_id_19;
   wire        _zz_targets_1_bestRequest_id_20;
   wire        _zz_targets_1_bestRequest_id_21;
   wire [ 1:0] _zz_targets_1_bestRequest_id_22;
   wire        _zz_targets_1_bestRequest_id_23;
   wire        _zz_targets_1_bestRequest_id_24;
   wire [ 1:0] _zz_targets_1_bestRequest_id_25;
   wire        _zz_targets_1_bestRequest_id_26;
   wire        _zz_targets_1_bestRequest_id_27;
   wire [ 1:0] _zz_targets_1_bestRequest_id_28;
   wire        _zz_targets_1_bestRequest_id_29;
   wire        _zz_targets_1_bestRequest_id_30;
   wire [ 1:0] _zz_targets_1_bestRequest_id_31;
   wire        _zz_targets_1_bestRequest_id_32;
   wire        _zz_targets_1_bestRequest_id_33;
   wire [ 1:0] _zz_targets_1_bestRequest_id_34;
   wire        _zz_targets_1_bestRequest_id_35;
   wire        _zz_targets_1_bestRequest_id_36;
   wire [ 1:0] _zz_targets_1_bestRequest_id_37;
   wire        _zz_targets_1_bestRequest_id_38;
   wire        _zz_targets_1_bestRequest_id_39;
   wire [ 1:0] _zz_targets_1_bestRequest_id_40;
   wire        _zz_targets_1_bestRequest_id_41;
   wire        _zz_targets_1_bestRequest_id_42;
   wire [ 1:0] _zz_targets_1_bestRequest_id_43;
   wire        _zz_targets_1_bestRequest_id_44;
   wire        _zz_targets_1_bestRequest_id_45;
   wire [ 1:0] _zz_targets_1_bestRequest_id_46;
   wire        _zz_targets_1_bestRequest_id_47;
   wire        _zz_targets_1_bestRequest_id_48;
   wire [ 1:0] _zz_targets_1_bestRequest_id_49;
   wire        _zz_targets_1_bestRequest_id_50;
   wire        _zz_targets_1_bestRequest_id_51;
   wire [ 1:0] _zz_targets_1_bestRequest_id_52;
   wire        _zz_targets_1_bestRequest_id_53;
   wire        _zz_targets_1_bestRequest_id_54;
   wire [ 1:0] _zz_targets_1_bestRequest_id_55;
   wire        _zz_targets_1_bestRequest_id_56;
   wire        _zz_targets_1_bestRequest_id_57;
   wire [ 1:0] _zz_targets_1_bestRequest_id_58;
   wire        _zz_targets_1_bestRequest_id_59;
   wire        _zz_targets_1_bestRequest_id_60;
   wire [ 1:0] _zz_targets_1_bestRequest_id_61;
   wire        _zz_targets_1_bestRequest_id_62;
   wire        _zz_targets_1_bestRequest_id_63;
   wire [ 1:0] _zz_targets_1_bestRequest_id_64;
   wire        _zz_targets_1_bestRequest_id_65;
   wire        _zz_targets_1_bestRequest_id_66;
   wire [ 1:0] _zz_targets_1_bestRequest_id_67;
   wire        _zz_targets_1_bestRequest_id_68;
   wire        _zz_targets_1_bestRequest_id_69;
   wire [ 1:0] _zz_targets_1_bestRequest_id_70;
   wire        _zz_targets_1_bestRequest_id_71;
   wire        _zz_targets_1_bestRequest_id_72;
   wire [ 1:0] _zz_targets_1_bestRequest_priority;
   wire        _zz_targets_1_bestRequest_id_73;
   wire        _zz_targets_1_bestRequest_id_74;
   wire [ 1:0] _zz_targets_1_bestRequest_priority_1;
   wire        _zz_targets_1_bestRequest_id_75;
   wire        _zz_targets_1_bestRequest_id_76;
   wire [ 1:0] _zz_targets_1_bestRequest_priority_2;
   wire        _zz_targets_1_bestRequest_id_77;
   wire        _zz_targets_1_bestRequest_id_78;
   wire [ 1:0] _zz_targets_1_bestRequest_priority_3;
   wire        _zz_targets_1_bestRequest_id_79;
   wire        _zz_targets_1_bestRequest_id_80;
   wire [ 1:0] _zz_targets_1_bestRequest_priority_4;
   wire        _zz_targets_1_bestRequest_valid;
   wire        _zz_targets_1_bestRequest_id_81;
   wire [ 1:0] _zz_targets_1_bestRequest_priority_5;
   wire        _zz_targets_1_bestRequest_valid_1;
   wire        _zz_targets_1_bestRequest_priority_6;
   reg  [ 1:0] targets_1_bestRequest_priority;
   reg  [ 4:0] targets_1_bestRequest_id;
   reg         targets_1_bestRequest_valid;
   wire        targets_1_iep;
   wire [ 4:0] targets_1_claim;
   wire        bus_readErrorFlag;
   wire        bus_writeErrorFlag;
   reg         bus_readHaltRequest;
   wire        bus_writeHaltRequest;
   wire        bus_writeJoinEvent_valid;
   wire        bus_writeJoinEvent_ready;
   wire        bus_writeOccur;
   reg  [ 1:0] bus_writeRsp_resp;
   wire        bus_writeJoinEvent_translated_valid;
   wire        bus_writeJoinEvent_translated_ready;
   wire [ 1:0] bus_writeJoinEvent_translated_payload_resp;
   wire        _zz_bus_writeJoinEvent_translated_ready;
   reg         _zz_bus_writeJoinEvent_translated_ready_1;
   wire        _zz_io_bus_b_valid;
   reg         _zz_io_bus_b_valid_1;
   reg  [ 1:0] _zz_io_bus_b_payload_resp;
   wire        when_Stream_l369;
   wire        bus_readDataStage_valid;
   wire        bus_readDataStage_ready;
   wire [21:0] bus_readDataStage_payload_addr;
   wire [ 2:0] bus_readDataStage_payload_prot;
   reg         io_bus_ar_rValid;
   reg  [21:0] io_bus_ar_rData_addr;
   reg  [ 2:0] io_bus_ar_rData_prot;
   wire        when_Stream_l369_1;
   reg  [31:0] bus_readRsp_data;
   reg  [ 1:0] bus_readRsp_resp;
   wire        _zz_io_bus_r_valid;
   wire [21:0] bus_readAddressMasked;
   wire [21:0] bus_writeAddressMasked;
   wire        bus_readOccur;
   reg  [ 1:0] _zz_gateways_0_priority;
   reg  [ 1:0] _zz_gateways_1_priority;
   reg  [ 1:0] _zz_gateways_2_priority;
   reg  [ 1:0] _zz_gateways_3_priority;
   reg  [ 1:0] _zz_gateways_4_priority;
   reg  [ 1:0] _zz_gateways_5_priority;
   reg  [ 1:0] _zz_gateways_6_priority;
   reg  [ 1:0] _zz_gateways_7_priority;
   reg  [ 1:0] _zz_gateways_8_priority;
   reg  [ 1:0] _zz_gateways_9_priority;
   reg  [ 1:0] _zz_gateways_10_priority;
   reg  [ 1:0] _zz_gateways_11_priority;
   reg  [ 1:0] _zz_gateways_12_priority;
   reg  [ 1:0] _zz_gateways_13_priority;
   reg  [ 1:0] _zz_gateways_14_priority;
   reg  [ 1:0] _zz_gateways_15_priority;
   reg  [ 1:0] _zz_gateways_16_priority;
   reg  [ 1:0] _zz_gateways_17_priority;
   reg  [ 1:0] _zz_gateways_18_priority;
   reg  [ 1:0] _zz_gateways_19_priority;
   reg  [ 1:0] _zz_gateways_20_priority;
   reg  [ 1:0] _zz_gateways_21_priority;
   reg  [ 1:0] _zz_gateways_22_priority;
   reg  [ 1:0] _zz_gateways_23_priority;
   reg  [ 1:0] _zz_gateways_24_priority;
   reg  [ 1:0] _zz_gateways_25_priority;
   reg  [ 1:0] _zz_gateways_26_priority;
   reg  [ 1:0] _zz_gateways_27_priority;
   reg  [ 1:0] _zz_gateways_28_priority;
   reg  [ 1:0] _zz_gateways_29_priority;
   reg  [ 1:0] _zz_gateways_30_priority;
   reg         mapping_claim_valid;
   reg  [ 4:0] mapping_claim_payload;
   reg         mapping_completion_valid;
   reg  [ 4:0] mapping_completion_payload;
   reg         mapping_coherencyStall_willIncrement;
   wire        mapping_coherencyStall_willClear;
   reg  [ 0:0] mapping_coherencyStall_valueNext;
   reg  [ 0:0] mapping_coherencyStall_value;
   wire        mapping_coherencyStall_willOverflowIfInc;
   wire        mapping_coherencyStall_willOverflow;
   wire        when_PlicMapper_l122;
   reg  [ 1:0] _zz_targets_0_threshold;
   reg         mapping_targetMapping_0_targetCompletion_valid;
   wire [ 4:0] mapping_targetMapping_0_targetCompletion_payload;
   reg         _zz_targets_0_ie_0;
   reg         _zz_targets_0_ie_1;
   reg         _zz_targets_0_ie_2;
   reg         _zz_targets_0_ie_3;
   reg         _zz_targets_0_ie_4;
   reg         _zz_targets_0_ie_5;
   reg         _zz_targets_0_ie_6;
   reg         _zz_targets_0_ie_7;
   reg         _zz_targets_0_ie_8;
   reg         _zz_targets_0_ie_9;
   reg         _zz_targets_0_ie_10;
   reg         _zz_targets_0_ie_11;
   reg         _zz_targets_0_ie_12;
   reg         _zz_targets_0_ie_13;
   reg         _zz_targets_0_ie_14;
   reg         _zz_targets_0_ie_15;
   reg         _zz_targets_0_ie_16;
   reg         _zz_targets_0_ie_17;
   reg         _zz_targets_0_ie_18;
   reg         _zz_targets_0_ie_19;
   reg         _zz_targets_0_ie_20;
   reg         _zz_targets_0_ie_21;
   reg         _zz_targets_0_ie_22;
   reg         _zz_targets_0_ie_23;
   reg         _zz_targets_0_ie_24;
   reg         _zz_targets_0_ie_25;
   reg         _zz_targets_0_ie_26;
   reg         _zz_targets_0_ie_27;
   reg         _zz_targets_0_ie_28;
   reg         _zz_targets_0_ie_29;
   reg         _zz_targets_0_ie_30;
   reg  [ 1:0] _zz_targets_1_threshold;
   reg         mapping_targetMapping_1_targetCompletion_valid;
   wire [ 4:0] mapping_targetMapping_1_targetCompletion_payload;
   reg         _zz_targets_1_ie_0;
   reg         _zz_targets_1_ie_1;
   reg         _zz_targets_1_ie_2;
   reg         _zz_targets_1_ie_3;
   reg         _zz_targets_1_ie_4;
   reg         _zz_targets_1_ie_5;
   reg         _zz_targets_1_ie_6;
   reg         _zz_targets_1_ie_7;
   reg         _zz_targets_1_ie_8;
   reg         _zz_targets_1_ie_9;
   reg         _zz_targets_1_ie_10;
   reg         _zz_targets_1_ie_11;
   reg         _zz_targets_1_ie_12;
   reg         _zz_targets_1_ie_13;
   reg         _zz_targets_1_ie_14;
   reg         _zz_targets_1_ie_15;
   reg         _zz_targets_1_ie_16;
   reg         _zz_targets_1_ie_17;
   reg         _zz_targets_1_ie_18;
   reg         _zz_targets_1_ie_19;
   reg         _zz_targets_1_ie_20;
   reg         _zz_targets_1_ie_21;
   reg         _zz_targets_1_ie_22;
   reg         _zz_targets_1_ie_23;
   reg         _zz_targets_1_ie_24;
   reg         _zz_targets_1_ie_25;
   reg         _zz_targets_1_ie_26;
   reg         _zz_targets_1_ie_27;
   reg         _zz_targets_1_ie_28;
   reg         _zz_targets_1_ie_29;
   reg         _zz_targets_1_ie_30;
   wire        when_AxiLite4SlaveFactory_l68;
   wire        when_AxiLite4SlaveFactory_l86;

   assign _zz_targets_0_bestRequest_id_82 = (_zz_targets_0_bestRequest_id ? targets_0_requests_0_id : targets_0_requests_1_id);
   assign _zz_targets_0_bestRequest_id_83 = (_zz_targets_0_bestRequest_id_3 ? targets_0_requests_2_id : targets_0_requests_3_id);
   assign _zz_targets_0_bestRequest_id_84 = (_zz_targets_0_bestRequest_id_6 ? targets_0_requests_4_id : targets_0_requests_5_id);
   assign _zz_targets_0_bestRequest_id_85 = (_zz_targets_0_bestRequest_id_9 ? targets_0_requests_6_id : targets_0_requests_7_id);
   assign _zz_targets_0_bestRequest_id_86 = (_zz_targets_0_bestRequest_id_12 ? targets_0_requests_8_id : targets_0_requests_9_id);
   assign _zz_targets_0_bestRequest_id_87 = (_zz_targets_0_bestRequest_id_15 ? targets_0_requests_10_id : targets_0_requests_11_id);
   assign _zz_targets_0_bestRequest_id_88 = (_zz_targets_0_bestRequest_id_18 ? targets_0_requests_12_id : targets_0_requests_13_id);
   assign _zz_targets_0_bestRequest_id_89 = (_zz_targets_0_bestRequest_id_21 ? targets_0_requests_14_id : targets_0_requests_15_id);
   assign _zz_targets_0_bestRequest_id_90 = (_zz_targets_0_bestRequest_id_24 ? targets_0_requests_16_id : targets_0_requests_17_id);
   assign _zz_targets_0_bestRequest_id_91 = (_zz_targets_0_bestRequest_id_27 ? targets_0_requests_18_id : targets_0_requests_19_id);
   assign _zz_targets_0_bestRequest_id_92 = (_zz_targets_0_bestRequest_id_30 ? targets_0_requests_20_id : targets_0_requests_21_id);
   assign _zz_targets_0_bestRequest_id_93 = (_zz_targets_0_bestRequest_id_33 ? targets_0_requests_22_id : targets_0_requests_23_id);
   assign _zz_targets_0_bestRequest_id_94 = (_zz_targets_0_bestRequest_id_36 ? targets_0_requests_24_id : targets_0_requests_25_id);
   assign _zz_targets_0_bestRequest_id_95 = (_zz_targets_0_bestRequest_id_39 ? targets_0_requests_26_id : targets_0_requests_27_id);
   assign _zz_targets_0_bestRequest_id_96 = (_zz_targets_0_bestRequest_id_42 ? targets_0_requests_28_id : targets_0_requests_29_id);
   assign _zz_targets_0_bestRequest_id_97 = (_zz_targets_0_bestRequest_id_45 ? targets_0_requests_30_id : targets_0_requests_31_id);
   assign _zz_targets_1_bestRequest_id_82 = (_zz_targets_1_bestRequest_id ? targets_1_requests_0_id : targets_1_requests_1_id);
   assign _zz_targets_1_bestRequest_id_83 = (_zz_targets_1_bestRequest_id_3 ? targets_1_requests_2_id : targets_1_requests_3_id);
   assign _zz_targets_1_bestRequest_id_84 = (_zz_targets_1_bestRequest_id_6 ? targets_1_requests_4_id : targets_1_requests_5_id);
   assign _zz_targets_1_bestRequest_id_85 = (_zz_targets_1_bestRequest_id_9 ? targets_1_requests_6_id : targets_1_requests_7_id);
   assign _zz_targets_1_bestRequest_id_86 = (_zz_targets_1_bestRequest_id_12 ? targets_1_requests_8_id : targets_1_requests_9_id);
   assign _zz_targets_1_bestRequest_id_87 = (_zz_targets_1_bestRequest_id_15 ? targets_1_requests_10_id : targets_1_requests_11_id);
   assign _zz_targets_1_bestRequest_id_88 = (_zz_targets_1_bestRequest_id_18 ? targets_1_requests_12_id : targets_1_requests_13_id);
   assign _zz_targets_1_bestRequest_id_89 = (_zz_targets_1_bestRequest_id_21 ? targets_1_requests_14_id : targets_1_requests_15_id);
   assign _zz_targets_1_bestRequest_id_90 = (_zz_targets_1_bestRequest_id_24 ? targets_1_requests_16_id : targets_1_requests_17_id);
   assign _zz_targets_1_bestRequest_id_91 = (_zz_targets_1_bestRequest_id_27 ? targets_1_requests_18_id : targets_1_requests_19_id);
   assign _zz_targets_1_bestRequest_id_92 = (_zz_targets_1_bestRequest_id_30 ? targets_1_requests_20_id : targets_1_requests_21_id);
   assign _zz_targets_1_bestRequest_id_93 = (_zz_targets_1_bestRequest_id_33 ? targets_1_requests_22_id : targets_1_requests_23_id);
   assign _zz_targets_1_bestRequest_id_94 = (_zz_targets_1_bestRequest_id_36 ? targets_1_requests_24_id : targets_1_requests_25_id);
   assign _zz_targets_1_bestRequest_id_95 = (_zz_targets_1_bestRequest_id_39 ? targets_1_requests_26_id : targets_1_requests_27_id);
   assign _zz_targets_1_bestRequest_id_96 = (_zz_targets_1_bestRequest_id_42 ? targets_1_requests_28_id : targets_1_requests_29_id);
   assign _zz_targets_1_bestRequest_id_97 = (_zz_targets_1_bestRequest_id_45 ? targets_1_requests_30_id : targets_1_requests_31_id);
   assign _zz_gateways_0_ip = io_sources[0];
   assign _zz_gateways_1_ip = io_sources[1];
   assign _zz_gateways_2_ip = io_sources[2];
   assign _zz_gateways_3_ip = io_sources[3];
   assign _zz_gateways_4_ip = io_sources[4];
   assign _zz_gateways_5_ip = io_sources[5];
   assign _zz_gateways_6_ip = io_sources[6];
   assign _zz_gateways_7_ip = io_sources[7];
   assign _zz_gateways_8_ip = io_sources[8];
   assign _zz_gateways_9_ip = io_sources[9];
   assign _zz_gateways_10_ip = io_sources[10];
   assign _zz_gateways_11_ip = io_sources[11];
   assign _zz_gateways_12_ip = io_sources[12];
   assign _zz_gateways_13_ip = io_sources[13];
   assign _zz_gateways_14_ip = io_sources[14];
   assign _zz_gateways_15_ip = io_sources[15];
   assign _zz_gateways_16_ip = io_sources[16];
   assign _zz_gateways_17_ip = io_sources[17];
   assign _zz_gateways_18_ip = io_sources[18];
   assign _zz_gateways_19_ip = io_sources[19];
   assign _zz_gateways_20_ip = io_sources[20];
   assign _zz_gateways_21_ip = io_sources[21];
   assign _zz_gateways_22_ip = io_sources[22];
   assign _zz_gateways_23_ip = io_sources[23];
   assign _zz_gateways_24_ip = io_sources[24];
   assign _zz_gateways_25_ip = io_sources[25];
   assign _zz_gateways_26_ip = io_sources[26];
   assign _zz_gateways_27_ip = io_sources[27];
   assign _zz_gateways_28_ip = io_sources[28];
   assign _zz_gateways_29_ip = io_sources[29];
   assign _zz_gateways_30_ip = io_sources[30];
   assign when_PlicGateway_l21 = (!gateways_0_waitCompletion);
   assign when_PlicGateway_l21_1 = (!gateways_1_waitCompletion);
   assign when_PlicGateway_l21_2 = (!gateways_2_waitCompletion);
   assign when_PlicGateway_l21_3 = (!gateways_3_waitCompletion);
   assign when_PlicGateway_l21_4 = (!gateways_4_waitCompletion);
   assign when_PlicGateway_l21_5 = (!gateways_5_waitCompletion);
   assign when_PlicGateway_l21_6 = (!gateways_6_waitCompletion);
   assign when_PlicGateway_l21_7 = (!gateways_7_waitCompletion);
   assign when_PlicGateway_l21_8 = (!gateways_8_waitCompletion);
   assign when_PlicGateway_l21_9 = (!gateways_9_waitCompletion);
   assign when_PlicGateway_l21_10 = (!gateways_10_waitCompletion);
   assign when_PlicGateway_l21_11 = (!gateways_11_waitCompletion);
   assign when_PlicGateway_l21_12 = (!gateways_12_waitCompletion);
   assign when_PlicGateway_l21_13 = (!gateways_13_waitCompletion);
   assign when_PlicGateway_l21_14 = (!gateways_14_waitCompletion);
   assign when_PlicGateway_l21_15 = (!gateways_15_waitCompletion);
   assign when_PlicGateway_l21_16 = (!gateways_16_waitCompletion);
   assign when_PlicGateway_l21_17 = (!gateways_17_waitCompletion);
   assign when_PlicGateway_l21_18 = (!gateways_18_waitCompletion);
   assign when_PlicGateway_l21_19 = (!gateways_19_waitCompletion);
   assign when_PlicGateway_l21_20 = (!gateways_20_waitCompletion);
   assign when_PlicGateway_l21_21 = (!gateways_21_waitCompletion);
   assign when_PlicGateway_l21_22 = (!gateways_22_waitCompletion);
   assign when_PlicGateway_l21_23 = (!gateways_23_waitCompletion);
   assign when_PlicGateway_l21_24 = (!gateways_24_waitCompletion);
   assign when_PlicGateway_l21_25 = (!gateways_25_waitCompletion);
   assign when_PlicGateway_l21_26 = (!gateways_26_waitCompletion);
   assign when_PlicGateway_l21_27 = (!gateways_27_waitCompletion);
   assign when_PlicGateway_l21_28 = (!gateways_28_waitCompletion);
   assign when_PlicGateway_l21_29 = (!gateways_29_waitCompletion);
   assign when_PlicGateway_l21_30 = (!gateways_30_waitCompletion);
   assign targets_0_requests_0_priority = 2'b00;
   assign targets_0_requests_0_id = 5'h00;
   assign targets_0_requests_0_valid = 1'b1;
   assign targets_0_requests_1_priority = gateways_0_priority;
   assign targets_0_requests_1_id = 5'h01;
   assign targets_0_requests_1_valid = (gateways_0_ip && targets_0_ie_0);
   assign targets_0_requests_2_priority = gateways_1_priority;
   assign targets_0_requests_2_id = 5'h02;
   assign targets_0_requests_2_valid = (gateways_1_ip && targets_0_ie_1);
   assign targets_0_requests_3_priority = gateways_2_priority;
   assign targets_0_requests_3_id = 5'h03;
   assign targets_0_requests_3_valid = (gateways_2_ip && targets_0_ie_2);
   assign targets_0_requests_4_priority = gateways_3_priority;
   assign targets_0_requests_4_id = 5'h04;
   assign targets_0_requests_4_valid = (gateways_3_ip && targets_0_ie_3);
   assign targets_0_requests_5_priority = gateways_4_priority;
   assign targets_0_requests_5_id = 5'h05;
   assign targets_0_requests_5_valid = (gateways_4_ip && targets_0_ie_4);
   assign targets_0_requests_6_priority = gateways_5_priority;
   assign targets_0_requests_6_id = 5'h06;
   assign targets_0_requests_6_valid = (gateways_5_ip && targets_0_ie_5);
   assign targets_0_requests_7_priority = gateways_6_priority;
   assign targets_0_requests_7_id = 5'h07;
   assign targets_0_requests_7_valid = (gateways_6_ip && targets_0_ie_6);
   assign targets_0_requests_8_priority = gateways_7_priority;
   assign targets_0_requests_8_id = 5'h08;
   assign targets_0_requests_8_valid = (gateways_7_ip && targets_0_ie_7);
   assign targets_0_requests_9_priority = gateways_8_priority;
   assign targets_0_requests_9_id = 5'h09;
   assign targets_0_requests_9_valid = (gateways_8_ip && targets_0_ie_8);
   assign targets_0_requests_10_priority = gateways_9_priority;
   assign targets_0_requests_10_id = 5'h0a;
   assign targets_0_requests_10_valid = (gateways_9_ip && targets_0_ie_9);
   assign targets_0_requests_11_priority = gateways_10_priority;
   assign targets_0_requests_11_id = 5'h0b;
   assign targets_0_requests_11_valid = (gateways_10_ip && targets_0_ie_10);
   assign targets_0_requests_12_priority = gateways_11_priority;
   assign targets_0_requests_12_id = 5'h0c;
   assign targets_0_requests_12_valid = (gateways_11_ip && targets_0_ie_11);
   assign targets_0_requests_13_priority = gateways_12_priority;
   assign targets_0_requests_13_id = 5'h0d;
   assign targets_0_requests_13_valid = (gateways_12_ip && targets_0_ie_12);
   assign targets_0_requests_14_priority = gateways_13_priority;
   assign targets_0_requests_14_id = 5'h0e;
   assign targets_0_requests_14_valid = (gateways_13_ip && targets_0_ie_13);
   assign targets_0_requests_15_priority = gateways_14_priority;
   assign targets_0_requests_15_id = 5'h0f;
   assign targets_0_requests_15_valid = (gateways_14_ip && targets_0_ie_14);
   assign targets_0_requests_16_priority = gateways_15_priority;
   assign targets_0_requests_16_id = 5'h10;
   assign targets_0_requests_16_valid = (gateways_15_ip && targets_0_ie_15);
   assign targets_0_requests_17_priority = gateways_16_priority;
   assign targets_0_requests_17_id = 5'h11;
   assign targets_0_requests_17_valid = (gateways_16_ip && targets_0_ie_16);
   assign targets_0_requests_18_priority = gateways_17_priority;
   assign targets_0_requests_18_id = 5'h12;
   assign targets_0_requests_18_valid = (gateways_17_ip && targets_0_ie_17);
   assign targets_0_requests_19_priority = gateways_18_priority;
   assign targets_0_requests_19_id = 5'h13;
   assign targets_0_requests_19_valid = (gateways_18_ip && targets_0_ie_18);
   assign targets_0_requests_20_priority = gateways_19_priority;
   assign targets_0_requests_20_id = 5'h14;
   assign targets_0_requests_20_valid = (gateways_19_ip && targets_0_ie_19);
   assign targets_0_requests_21_priority = gateways_20_priority;
   assign targets_0_requests_21_id = 5'h15;
   assign targets_0_requests_21_valid = (gateways_20_ip && targets_0_ie_20);
   assign targets_0_requests_22_priority = gateways_21_priority;
   assign targets_0_requests_22_id = 5'h16;
   assign targets_0_requests_22_valid = (gateways_21_ip && targets_0_ie_21);
   assign targets_0_requests_23_priority = gateways_22_priority;
   assign targets_0_requests_23_id = 5'h17;
   assign targets_0_requests_23_valid = (gateways_22_ip && targets_0_ie_22);
   assign targets_0_requests_24_priority = gateways_23_priority;
   assign targets_0_requests_24_id = 5'h18;
   assign targets_0_requests_24_valid = (gateways_23_ip && targets_0_ie_23);
   assign targets_0_requests_25_priority = gateways_24_priority;
   assign targets_0_requests_25_id = 5'h19;
   assign targets_0_requests_25_valid = (gateways_24_ip && targets_0_ie_24);
   assign targets_0_requests_26_priority = gateways_25_priority;
   assign targets_0_requests_26_id = 5'h1a;
   assign targets_0_requests_26_valid = (gateways_25_ip && targets_0_ie_25);
   assign targets_0_requests_27_priority = gateways_26_priority;
   assign targets_0_requests_27_id = 5'h1b;
   assign targets_0_requests_27_valid = (gateways_26_ip && targets_0_ie_26);
   assign targets_0_requests_28_priority = gateways_27_priority;
   assign targets_0_requests_28_id = 5'h1c;
   assign targets_0_requests_28_valid = (gateways_27_ip && targets_0_ie_27);
   assign targets_0_requests_29_priority = gateways_28_priority;
   assign targets_0_requests_29_id = 5'h1d;
   assign targets_0_requests_29_valid = (gateways_28_ip && targets_0_ie_28);
   assign targets_0_requests_30_priority = gateways_29_priority;
   assign targets_0_requests_30_id = 5'h1e;
   assign targets_0_requests_30_valid = (gateways_29_ip && targets_0_ie_29);
   assign targets_0_requests_31_priority = gateways_30_priority;
   assign targets_0_requests_31_id = 5'h1f;
   assign targets_0_requests_31_valid = (gateways_30_ip && targets_0_ie_30);
   assign _zz_targets_0_bestRequest_id = ((! targets_0_requests_1_valid) || (targets_0_requests_0_valid && (targets_0_requests_1_priority <= targets_0_requests_0_priority)));
   assign _zz_targets_0_bestRequest_id_1 = (_zz_targets_0_bestRequest_id ? targets_0_requests_0_priority : targets_0_requests_1_priority);
   assign _zz_targets_0_bestRequest_id_2 = (_zz_targets_0_bestRequest_id ? targets_0_requests_0_valid : targets_0_requests_1_valid);
   assign _zz_targets_0_bestRequest_id_3 = ((! targets_0_requests_3_valid) || (targets_0_requests_2_valid && (targets_0_requests_3_priority <= targets_0_requests_2_priority)));
   assign _zz_targets_0_bestRequest_id_4 = (_zz_targets_0_bestRequest_id_3 ? targets_0_requests_2_priority : targets_0_requests_3_priority);
   assign _zz_targets_0_bestRequest_id_5 = (_zz_targets_0_bestRequest_id_3 ? targets_0_requests_2_valid : targets_0_requests_3_valid);
   assign _zz_targets_0_bestRequest_id_6 = ((! targets_0_requests_5_valid) || (targets_0_requests_4_valid && (targets_0_requests_5_priority <= targets_0_requests_4_priority)));
   assign _zz_targets_0_bestRequest_id_7 = (_zz_targets_0_bestRequest_id_6 ? targets_0_requests_4_priority : targets_0_requests_5_priority);
   assign _zz_targets_0_bestRequest_id_8 = (_zz_targets_0_bestRequest_id_6 ? targets_0_requests_4_valid : targets_0_requests_5_valid);
   assign _zz_targets_0_bestRequest_id_9 = ((! targets_0_requests_7_valid) || (targets_0_requests_6_valid && (targets_0_requests_7_priority <= targets_0_requests_6_priority)));
   assign _zz_targets_0_bestRequest_id_10 = (_zz_targets_0_bestRequest_id_9 ? targets_0_requests_6_priority : targets_0_requests_7_priority);
   assign _zz_targets_0_bestRequest_id_11 = (_zz_targets_0_bestRequest_id_9 ? targets_0_requests_6_valid : targets_0_requests_7_valid);
   assign _zz_targets_0_bestRequest_id_12 = ((! targets_0_requests_9_valid) || (targets_0_requests_8_valid && (targets_0_requests_9_priority <= targets_0_requests_8_priority)));
   assign _zz_targets_0_bestRequest_id_13 = (_zz_targets_0_bestRequest_id_12 ? targets_0_requests_8_priority : targets_0_requests_9_priority);
   assign _zz_targets_0_bestRequest_id_14 = (_zz_targets_0_bestRequest_id_12 ? targets_0_requests_8_valid : targets_0_requests_9_valid);
   assign _zz_targets_0_bestRequest_id_15 = ((! targets_0_requests_11_valid) || (targets_0_requests_10_valid && (targets_0_requests_11_priority <= targets_0_requests_10_priority)));
   assign _zz_targets_0_bestRequest_id_16 = (_zz_targets_0_bestRequest_id_15 ? targets_0_requests_10_priority : targets_0_requests_11_priority);
   assign _zz_targets_0_bestRequest_id_17 = (_zz_targets_0_bestRequest_id_15 ? targets_0_requests_10_valid : targets_0_requests_11_valid);
   assign _zz_targets_0_bestRequest_id_18 = ((! targets_0_requests_13_valid) || (targets_0_requests_12_valid && (targets_0_requests_13_priority <= targets_0_requests_12_priority)));
   assign _zz_targets_0_bestRequest_id_19 = (_zz_targets_0_bestRequest_id_18 ? targets_0_requests_12_priority : targets_0_requests_13_priority);
   assign _zz_targets_0_bestRequest_id_20 = (_zz_targets_0_bestRequest_id_18 ? targets_0_requests_12_valid : targets_0_requests_13_valid);
   assign _zz_targets_0_bestRequest_id_21 = ((! targets_0_requests_15_valid) || (targets_0_requests_14_valid && (targets_0_requests_15_priority <= targets_0_requests_14_priority)));
   assign _zz_targets_0_bestRequest_id_22 = (_zz_targets_0_bestRequest_id_21 ? targets_0_requests_14_priority : targets_0_requests_15_priority);
   assign _zz_targets_0_bestRequest_id_23 = (_zz_targets_0_bestRequest_id_21 ? targets_0_requests_14_valid : targets_0_requests_15_valid);
   assign _zz_targets_0_bestRequest_id_24 = ((! targets_0_requests_17_valid) || (targets_0_requests_16_valid && (targets_0_requests_17_priority <= targets_0_requests_16_priority)));
   assign _zz_targets_0_bestRequest_id_25 = (_zz_targets_0_bestRequest_id_24 ? targets_0_requests_16_priority : targets_0_requests_17_priority);
   assign _zz_targets_0_bestRequest_id_26 = (_zz_targets_0_bestRequest_id_24 ? targets_0_requests_16_valid : targets_0_requests_17_valid);
   assign _zz_targets_0_bestRequest_id_27 = ((! targets_0_requests_19_valid) || (targets_0_requests_18_valid && (targets_0_requests_19_priority <= targets_0_requests_18_priority)));
   assign _zz_targets_0_bestRequest_id_28 = (_zz_targets_0_bestRequest_id_27 ? targets_0_requests_18_priority : targets_0_requests_19_priority);
   assign _zz_targets_0_bestRequest_id_29 = (_zz_targets_0_bestRequest_id_27 ? targets_0_requests_18_valid : targets_0_requests_19_valid);
   assign _zz_targets_0_bestRequest_id_30 = ((! targets_0_requests_21_valid) || (targets_0_requests_20_valid && (targets_0_requests_21_priority <= targets_0_requests_20_priority)));
   assign _zz_targets_0_bestRequest_id_31 = (_zz_targets_0_bestRequest_id_30 ? targets_0_requests_20_priority : targets_0_requests_21_priority);
   assign _zz_targets_0_bestRequest_id_32 = (_zz_targets_0_bestRequest_id_30 ? targets_0_requests_20_valid : targets_0_requests_21_valid);
   assign _zz_targets_0_bestRequest_id_33 = ((! targets_0_requests_23_valid) || (targets_0_requests_22_valid && (targets_0_requests_23_priority <= targets_0_requests_22_priority)));
   assign _zz_targets_0_bestRequest_id_34 = (_zz_targets_0_bestRequest_id_33 ? targets_0_requests_22_priority : targets_0_requests_23_priority);
   assign _zz_targets_0_bestRequest_id_35 = (_zz_targets_0_bestRequest_id_33 ? targets_0_requests_22_valid : targets_0_requests_23_valid);
   assign _zz_targets_0_bestRequest_id_36 = ((! targets_0_requests_25_valid) || (targets_0_requests_24_valid && (targets_0_requests_25_priority <= targets_0_requests_24_priority)));
   assign _zz_targets_0_bestRequest_id_37 = (_zz_targets_0_bestRequest_id_36 ? targets_0_requests_24_priority : targets_0_requests_25_priority);
   assign _zz_targets_0_bestRequest_id_38 = (_zz_targets_0_bestRequest_id_36 ? targets_0_requests_24_valid : targets_0_requests_25_valid);
   assign _zz_targets_0_bestRequest_id_39 = ((! targets_0_requests_27_valid) || (targets_0_requests_26_valid && (targets_0_requests_27_priority <= targets_0_requests_26_priority)));
   assign _zz_targets_0_bestRequest_id_40 = (_zz_targets_0_bestRequest_id_39 ? targets_0_requests_26_priority : targets_0_requests_27_priority);
   assign _zz_targets_0_bestRequest_id_41 = (_zz_targets_0_bestRequest_id_39 ? targets_0_requests_26_valid : targets_0_requests_27_valid);
   assign _zz_targets_0_bestRequest_id_42 = ((! targets_0_requests_29_valid) || (targets_0_requests_28_valid && (targets_0_requests_29_priority <= targets_0_requests_28_priority)));
   assign _zz_targets_0_bestRequest_id_43 = (_zz_targets_0_bestRequest_id_42 ? targets_0_requests_28_priority : targets_0_requests_29_priority);
   assign _zz_targets_0_bestRequest_id_44 = (_zz_targets_0_bestRequest_id_42 ? targets_0_requests_28_valid : targets_0_requests_29_valid);
   assign _zz_targets_0_bestRequest_id_45 = ((! targets_0_requests_31_valid) || (targets_0_requests_30_valid && (targets_0_requests_31_priority <= targets_0_requests_30_priority)));
   assign _zz_targets_0_bestRequest_id_46 = (_zz_targets_0_bestRequest_id_45 ? targets_0_requests_30_priority : targets_0_requests_31_priority);
   assign _zz_targets_0_bestRequest_id_47 = (_zz_targets_0_bestRequest_id_45 ? targets_0_requests_30_valid : targets_0_requests_31_valid);
   assign _zz_targets_0_bestRequest_id_48 = ((! _zz_targets_0_bestRequest_id_5) || (_zz_targets_0_bestRequest_id_2 && (_zz_targets_0_bestRequest_id_4 <= _zz_targets_0_bestRequest_id_1)));
   assign _zz_targets_0_bestRequest_id_49 = (_zz_targets_0_bestRequest_id_48 ? _zz_targets_0_bestRequest_id_1 : _zz_targets_0_bestRequest_id_4);
   assign _zz_targets_0_bestRequest_id_50 = (_zz_targets_0_bestRequest_id_48 ? _zz_targets_0_bestRequest_id_2 : _zz_targets_0_bestRequest_id_5);
   assign _zz_targets_0_bestRequest_id_51 = ((! _zz_targets_0_bestRequest_id_11) || (_zz_targets_0_bestRequest_id_8 && (_zz_targets_0_bestRequest_id_10 <= _zz_targets_0_bestRequest_id_7)));
   assign _zz_targets_0_bestRequest_id_52 = (_zz_targets_0_bestRequest_id_51 ? _zz_targets_0_bestRequest_id_7 : _zz_targets_0_bestRequest_id_10);
   assign _zz_targets_0_bestRequest_id_53 = (_zz_targets_0_bestRequest_id_51 ? _zz_targets_0_bestRequest_id_8 : _zz_targets_0_bestRequest_id_11);
   assign _zz_targets_0_bestRequest_id_54 = ((! _zz_targets_0_bestRequest_id_17) || (_zz_targets_0_bestRequest_id_14 && (_zz_targets_0_bestRequest_id_16 <= _zz_targets_0_bestRequest_id_13)));
   assign _zz_targets_0_bestRequest_id_55 = (_zz_targets_0_bestRequest_id_54 ? _zz_targets_0_bestRequest_id_13 : _zz_targets_0_bestRequest_id_16);
   assign _zz_targets_0_bestRequest_id_56 = (_zz_targets_0_bestRequest_id_54 ? _zz_targets_0_bestRequest_id_14 : _zz_targets_0_bestRequest_id_17);
   assign _zz_targets_0_bestRequest_id_57 = ((! _zz_targets_0_bestRequest_id_23) || (_zz_targets_0_bestRequest_id_20 && (_zz_targets_0_bestRequest_id_22 <= _zz_targets_0_bestRequest_id_19)));
   assign _zz_targets_0_bestRequest_id_58 = (_zz_targets_0_bestRequest_id_57 ? _zz_targets_0_bestRequest_id_19 : _zz_targets_0_bestRequest_id_22);
   assign _zz_targets_0_bestRequest_id_59 = (_zz_targets_0_bestRequest_id_57 ? _zz_targets_0_bestRequest_id_20 : _zz_targets_0_bestRequest_id_23);
   assign _zz_targets_0_bestRequest_id_60 = ((! _zz_targets_0_bestRequest_id_29) || (_zz_targets_0_bestRequest_id_26 && (_zz_targets_0_bestRequest_id_28 <= _zz_targets_0_bestRequest_id_25)));
   assign _zz_targets_0_bestRequest_id_61 = (_zz_targets_0_bestRequest_id_60 ? _zz_targets_0_bestRequest_id_25 : _zz_targets_0_bestRequest_id_28);
   assign _zz_targets_0_bestRequest_id_62 = (_zz_targets_0_bestRequest_id_60 ? _zz_targets_0_bestRequest_id_26 : _zz_targets_0_bestRequest_id_29);
   assign _zz_targets_0_bestRequest_id_63 = ((! _zz_targets_0_bestRequest_id_35) || (_zz_targets_0_bestRequest_id_32 && (_zz_targets_0_bestRequest_id_34 <= _zz_targets_0_bestRequest_id_31)));
   assign _zz_targets_0_bestRequest_id_64 = (_zz_targets_0_bestRequest_id_63 ? _zz_targets_0_bestRequest_id_31 : _zz_targets_0_bestRequest_id_34);
   assign _zz_targets_0_bestRequest_id_65 = (_zz_targets_0_bestRequest_id_63 ? _zz_targets_0_bestRequest_id_32 : _zz_targets_0_bestRequest_id_35);
   assign _zz_targets_0_bestRequest_id_66 = ((! _zz_targets_0_bestRequest_id_41) || (_zz_targets_0_bestRequest_id_38 && (_zz_targets_0_bestRequest_id_40 <= _zz_targets_0_bestRequest_id_37)));
   assign _zz_targets_0_bestRequest_id_67 = (_zz_targets_0_bestRequest_id_66 ? _zz_targets_0_bestRequest_id_37 : _zz_targets_0_bestRequest_id_40);
   assign _zz_targets_0_bestRequest_id_68 = (_zz_targets_0_bestRequest_id_66 ? _zz_targets_0_bestRequest_id_38 : _zz_targets_0_bestRequest_id_41);
   assign _zz_targets_0_bestRequest_id_69 = ((! _zz_targets_0_bestRequest_id_47) || (_zz_targets_0_bestRequest_id_44 && (_zz_targets_0_bestRequest_id_46 <= _zz_targets_0_bestRequest_id_43)));
   assign _zz_targets_0_bestRequest_id_70 = (_zz_targets_0_bestRequest_id_69 ? _zz_targets_0_bestRequest_id_43 : _zz_targets_0_bestRequest_id_46);
   assign _zz_targets_0_bestRequest_id_71 = (_zz_targets_0_bestRequest_id_69 ? _zz_targets_0_bestRequest_id_44 : _zz_targets_0_bestRequest_id_47);
   assign _zz_targets_0_bestRequest_id_72 = ((! _zz_targets_0_bestRequest_id_53) || (_zz_targets_0_bestRequest_id_50 && (_zz_targets_0_bestRequest_id_52 <= _zz_targets_0_bestRequest_id_49)));
   assign _zz_targets_0_bestRequest_priority = (_zz_targets_0_bestRequest_id_72 ? _zz_targets_0_bestRequest_id_49 : _zz_targets_0_bestRequest_id_52);
   assign _zz_targets_0_bestRequest_id_73 = (_zz_targets_0_bestRequest_id_72 ? _zz_targets_0_bestRequest_id_50 : _zz_targets_0_bestRequest_id_53);
   assign _zz_targets_0_bestRequest_id_74 = ((! _zz_targets_0_bestRequest_id_59) || (_zz_targets_0_bestRequest_id_56 && (_zz_targets_0_bestRequest_id_58 <= _zz_targets_0_bestRequest_id_55)));
   assign _zz_targets_0_bestRequest_priority_1 = (_zz_targets_0_bestRequest_id_74 ? _zz_targets_0_bestRequest_id_55 : _zz_targets_0_bestRequest_id_58);
   assign _zz_targets_0_bestRequest_id_75 = (_zz_targets_0_bestRequest_id_74 ? _zz_targets_0_bestRequest_id_56 : _zz_targets_0_bestRequest_id_59);
   assign _zz_targets_0_bestRequest_id_76 = ((! _zz_targets_0_bestRequest_id_65) || (_zz_targets_0_bestRequest_id_62 && (_zz_targets_0_bestRequest_id_64 <= _zz_targets_0_bestRequest_id_61)));
   assign _zz_targets_0_bestRequest_priority_2 = (_zz_targets_0_bestRequest_id_76 ? _zz_targets_0_bestRequest_id_61 : _zz_targets_0_bestRequest_id_64);
   assign _zz_targets_0_bestRequest_id_77 = (_zz_targets_0_bestRequest_id_76 ? _zz_targets_0_bestRequest_id_62 : _zz_targets_0_bestRequest_id_65);
   assign _zz_targets_0_bestRequest_id_78 = ((! _zz_targets_0_bestRequest_id_71) || (_zz_targets_0_bestRequest_id_68 && (_zz_targets_0_bestRequest_id_70 <= _zz_targets_0_bestRequest_id_67)));
   assign _zz_targets_0_bestRequest_priority_3 = (_zz_targets_0_bestRequest_id_78 ? _zz_targets_0_bestRequest_id_67 : _zz_targets_0_bestRequest_id_70);
   assign _zz_targets_0_bestRequest_id_79 = (_zz_targets_0_bestRequest_id_78 ? _zz_targets_0_bestRequest_id_68 : _zz_targets_0_bestRequest_id_71);
   assign _zz_targets_0_bestRequest_id_80 = ((! _zz_targets_0_bestRequest_id_75) || (_zz_targets_0_bestRequest_id_73 && (_zz_targets_0_bestRequest_priority_1 <= _zz_targets_0_bestRequest_priority)));
   assign _zz_targets_0_bestRequest_priority_4 = (_zz_targets_0_bestRequest_id_80 ? _zz_targets_0_bestRequest_priority : _zz_targets_0_bestRequest_priority_1);
   assign _zz_targets_0_bestRequest_valid = (_zz_targets_0_bestRequest_id_80 ? _zz_targets_0_bestRequest_id_73 : _zz_targets_0_bestRequest_id_75);
   assign _zz_targets_0_bestRequest_id_81 = ((! _zz_targets_0_bestRequest_id_79) || (_zz_targets_0_bestRequest_id_77 && (_zz_targets_0_bestRequest_priority_3 <= _zz_targets_0_bestRequest_priority_2)));
   assign _zz_targets_0_bestRequest_priority_5 = (_zz_targets_0_bestRequest_id_81 ? _zz_targets_0_bestRequest_priority_2 : _zz_targets_0_bestRequest_priority_3);
   assign _zz_targets_0_bestRequest_valid_1 = (_zz_targets_0_bestRequest_id_81 ? _zz_targets_0_bestRequest_id_77 : _zz_targets_0_bestRequest_id_79);
   assign _zz_targets_0_bestRequest_priority_6 = ((! _zz_targets_0_bestRequest_valid_1) || (_zz_targets_0_bestRequest_valid && (_zz_targets_0_bestRequest_priority_5 <= _zz_targets_0_bestRequest_priority_4)));
   assign targets_0_iep = (targets_0_threshold < targets_0_bestRequest_priority);
   assign targets_0_claim = (targets_0_iep ? targets_0_bestRequest_id : 5'h00);
   assign targets_1_requests_0_priority = 2'b00;
   assign targets_1_requests_0_id = 5'h00;
   assign targets_1_requests_0_valid = 1'b1;
   assign targets_1_requests_1_priority = gateways_0_priority;
   assign targets_1_requests_1_id = 5'h01;
   assign targets_1_requests_1_valid = (gateways_0_ip && targets_1_ie_0);
   assign targets_1_requests_2_priority = gateways_1_priority;
   assign targets_1_requests_2_id = 5'h02;
   assign targets_1_requests_2_valid = (gateways_1_ip && targets_1_ie_1);
   assign targets_1_requests_3_priority = gateways_2_priority;
   assign targets_1_requests_3_id = 5'h03;
   assign targets_1_requests_3_valid = (gateways_2_ip && targets_1_ie_2);
   assign targets_1_requests_4_priority = gateways_3_priority;
   assign targets_1_requests_4_id = 5'h04;
   assign targets_1_requests_4_valid = (gateways_3_ip && targets_1_ie_3);
   assign targets_1_requests_5_priority = gateways_4_priority;
   assign targets_1_requests_5_id = 5'h05;
   assign targets_1_requests_5_valid = (gateways_4_ip && targets_1_ie_4);
   assign targets_1_requests_6_priority = gateways_5_priority;
   assign targets_1_requests_6_id = 5'h06;
   assign targets_1_requests_6_valid = (gateways_5_ip && targets_1_ie_5);
   assign targets_1_requests_7_priority = gateways_6_priority;
   assign targets_1_requests_7_id = 5'h07;
   assign targets_1_requests_7_valid = (gateways_6_ip && targets_1_ie_6);
   assign targets_1_requests_8_priority = gateways_7_priority;
   assign targets_1_requests_8_id = 5'h08;
   assign targets_1_requests_8_valid = (gateways_7_ip && targets_1_ie_7);
   assign targets_1_requests_9_priority = gateways_8_priority;
   assign targets_1_requests_9_id = 5'h09;
   assign targets_1_requests_9_valid = (gateways_8_ip && targets_1_ie_8);
   assign targets_1_requests_10_priority = gateways_9_priority;
   assign targets_1_requests_10_id = 5'h0a;
   assign targets_1_requests_10_valid = (gateways_9_ip && targets_1_ie_9);
   assign targets_1_requests_11_priority = gateways_10_priority;
   assign targets_1_requests_11_id = 5'h0b;
   assign targets_1_requests_11_valid = (gateways_10_ip && targets_1_ie_10);
   assign targets_1_requests_12_priority = gateways_11_priority;
   assign targets_1_requests_12_id = 5'h0c;
   assign targets_1_requests_12_valid = (gateways_11_ip && targets_1_ie_11);
   assign targets_1_requests_13_priority = gateways_12_priority;
   assign targets_1_requests_13_id = 5'h0d;
   assign targets_1_requests_13_valid = (gateways_12_ip && targets_1_ie_12);
   assign targets_1_requests_14_priority = gateways_13_priority;
   assign targets_1_requests_14_id = 5'h0e;
   assign targets_1_requests_14_valid = (gateways_13_ip && targets_1_ie_13);
   assign targets_1_requests_15_priority = gateways_14_priority;
   assign targets_1_requests_15_id = 5'h0f;
   assign targets_1_requests_15_valid = (gateways_14_ip && targets_1_ie_14);
   assign targets_1_requests_16_priority = gateways_15_priority;
   assign targets_1_requests_16_id = 5'h10;
   assign targets_1_requests_16_valid = (gateways_15_ip && targets_1_ie_15);
   assign targets_1_requests_17_priority = gateways_16_priority;
   assign targets_1_requests_17_id = 5'h11;
   assign targets_1_requests_17_valid = (gateways_16_ip && targets_1_ie_16);
   assign targets_1_requests_18_priority = gateways_17_priority;
   assign targets_1_requests_18_id = 5'h12;
   assign targets_1_requests_18_valid = (gateways_17_ip && targets_1_ie_17);
   assign targets_1_requests_19_priority = gateways_18_priority;
   assign targets_1_requests_19_id = 5'h13;
   assign targets_1_requests_19_valid = (gateways_18_ip && targets_1_ie_18);
   assign targets_1_requests_20_priority = gateways_19_priority;
   assign targets_1_requests_20_id = 5'h14;
   assign targets_1_requests_20_valid = (gateways_19_ip && targets_1_ie_19);
   assign targets_1_requests_21_priority = gateways_20_priority;
   assign targets_1_requests_21_id = 5'h15;
   assign targets_1_requests_21_valid = (gateways_20_ip && targets_1_ie_20);
   assign targets_1_requests_22_priority = gateways_21_priority;
   assign targets_1_requests_22_id = 5'h16;
   assign targets_1_requests_22_valid = (gateways_21_ip && targets_1_ie_21);
   assign targets_1_requests_23_priority = gateways_22_priority;
   assign targets_1_requests_23_id = 5'h17;
   assign targets_1_requests_23_valid = (gateways_22_ip && targets_1_ie_22);
   assign targets_1_requests_24_priority = gateways_23_priority;
   assign targets_1_requests_24_id = 5'h18;
   assign targets_1_requests_24_valid = (gateways_23_ip && targets_1_ie_23);
   assign targets_1_requests_25_priority = gateways_24_priority;
   assign targets_1_requests_25_id = 5'h19;
   assign targets_1_requests_25_valid = (gateways_24_ip && targets_1_ie_24);
   assign targets_1_requests_26_priority = gateways_25_priority;
   assign targets_1_requests_26_id = 5'h1a;
   assign targets_1_requests_26_valid = (gateways_25_ip && targets_1_ie_25);
   assign targets_1_requests_27_priority = gateways_26_priority;
   assign targets_1_requests_27_id = 5'h1b;
   assign targets_1_requests_27_valid = (gateways_26_ip && targets_1_ie_26);
   assign targets_1_requests_28_priority = gateways_27_priority;
   assign targets_1_requests_28_id = 5'h1c;
   assign targets_1_requests_28_valid = (gateways_27_ip && targets_1_ie_27);
   assign targets_1_requests_29_priority = gateways_28_priority;
   assign targets_1_requests_29_id = 5'h1d;
   assign targets_1_requests_29_valid = (gateways_28_ip && targets_1_ie_28);
   assign targets_1_requests_30_priority = gateways_29_priority;
   assign targets_1_requests_30_id = 5'h1e;
   assign targets_1_requests_30_valid = (gateways_29_ip && targets_1_ie_29);
   assign targets_1_requests_31_priority = gateways_30_priority;
   assign targets_1_requests_31_id = 5'h1f;
   assign targets_1_requests_31_valid = (gateways_30_ip && targets_1_ie_30);
   assign _zz_targets_1_bestRequest_id = ((! targets_1_requests_1_valid) || (targets_1_requests_0_valid && (targets_1_requests_1_priority <= targets_1_requests_0_priority)));
   assign _zz_targets_1_bestRequest_id_1 = (_zz_targets_1_bestRequest_id ? targets_1_requests_0_priority : targets_1_requests_1_priority);
   assign _zz_targets_1_bestRequest_id_2 = (_zz_targets_1_bestRequest_id ? targets_1_requests_0_valid : targets_1_requests_1_valid);
   assign _zz_targets_1_bestRequest_id_3 = ((! targets_1_requests_3_valid) || (targets_1_requests_2_valid && (targets_1_requests_3_priority <= targets_1_requests_2_priority)));
   assign _zz_targets_1_bestRequest_id_4 = (_zz_targets_1_bestRequest_id_3 ? targets_1_requests_2_priority : targets_1_requests_3_priority);
   assign _zz_targets_1_bestRequest_id_5 = (_zz_targets_1_bestRequest_id_3 ? targets_1_requests_2_valid : targets_1_requests_3_valid);
   assign _zz_targets_1_bestRequest_id_6 = ((! targets_1_requests_5_valid) || (targets_1_requests_4_valid && (targets_1_requests_5_priority <= targets_1_requests_4_priority)));
   assign _zz_targets_1_bestRequest_id_7 = (_zz_targets_1_bestRequest_id_6 ? targets_1_requests_4_priority : targets_1_requests_5_priority);
   assign _zz_targets_1_bestRequest_id_8 = (_zz_targets_1_bestRequest_id_6 ? targets_1_requests_4_valid : targets_1_requests_5_valid);
   assign _zz_targets_1_bestRequest_id_9 = ((! targets_1_requests_7_valid) || (targets_1_requests_6_valid && (targets_1_requests_7_priority <= targets_1_requests_6_priority)));
   assign _zz_targets_1_bestRequest_id_10 = (_zz_targets_1_bestRequest_id_9 ? targets_1_requests_6_priority : targets_1_requests_7_priority);
   assign _zz_targets_1_bestRequest_id_11 = (_zz_targets_1_bestRequest_id_9 ? targets_1_requests_6_valid : targets_1_requests_7_valid);
   assign _zz_targets_1_bestRequest_id_12 = ((! targets_1_requests_9_valid) || (targets_1_requests_8_valid && (targets_1_requests_9_priority <= targets_1_requests_8_priority)));
   assign _zz_targets_1_bestRequest_id_13 = (_zz_targets_1_bestRequest_id_12 ? targets_1_requests_8_priority : targets_1_requests_9_priority);
   assign _zz_targets_1_bestRequest_id_14 = (_zz_targets_1_bestRequest_id_12 ? targets_1_requests_8_valid : targets_1_requests_9_valid);
   assign _zz_targets_1_bestRequest_id_15 = ((! targets_1_requests_11_valid) || (targets_1_requests_10_valid && (targets_1_requests_11_priority <= targets_1_requests_10_priority)));
   assign _zz_targets_1_bestRequest_id_16 = (_zz_targets_1_bestRequest_id_15 ? targets_1_requests_10_priority : targets_1_requests_11_priority);
   assign _zz_targets_1_bestRequest_id_17 = (_zz_targets_1_bestRequest_id_15 ? targets_1_requests_10_valid : targets_1_requests_11_valid);
   assign _zz_targets_1_bestRequest_id_18 = ((! targets_1_requests_13_valid) || (targets_1_requests_12_valid && (targets_1_requests_13_priority <= targets_1_requests_12_priority)));
   assign _zz_targets_1_bestRequest_id_19 = (_zz_targets_1_bestRequest_id_18 ? targets_1_requests_12_priority : targets_1_requests_13_priority);
   assign _zz_targets_1_bestRequest_id_20 = (_zz_targets_1_bestRequest_id_18 ? targets_1_requests_12_valid : targets_1_requests_13_valid);
   assign _zz_targets_1_bestRequest_id_21 = ((! targets_1_requests_15_valid) || (targets_1_requests_14_valid && (targets_1_requests_15_priority <= targets_1_requests_14_priority)));
   assign _zz_targets_1_bestRequest_id_22 = (_zz_targets_1_bestRequest_id_21 ? targets_1_requests_14_priority : targets_1_requests_15_priority);
   assign _zz_targets_1_bestRequest_id_23 = (_zz_targets_1_bestRequest_id_21 ? targets_1_requests_14_valid : targets_1_requests_15_valid);
   assign _zz_targets_1_bestRequest_id_24 = ((! targets_1_requests_17_valid) || (targets_1_requests_16_valid && (targets_1_requests_17_priority <= targets_1_requests_16_priority)));
   assign _zz_targets_1_bestRequest_id_25 = (_zz_targets_1_bestRequest_id_24 ? targets_1_requests_16_priority : targets_1_requests_17_priority);
   assign _zz_targets_1_bestRequest_id_26 = (_zz_targets_1_bestRequest_id_24 ? targets_1_requests_16_valid : targets_1_requests_17_valid);
   assign _zz_targets_1_bestRequest_id_27 = ((! targets_1_requests_19_valid) || (targets_1_requests_18_valid && (targets_1_requests_19_priority <= targets_1_requests_18_priority)));
   assign _zz_targets_1_bestRequest_id_28 = (_zz_targets_1_bestRequest_id_27 ? targets_1_requests_18_priority : targets_1_requests_19_priority);
   assign _zz_targets_1_bestRequest_id_29 = (_zz_targets_1_bestRequest_id_27 ? targets_1_requests_18_valid : targets_1_requests_19_valid);
   assign _zz_targets_1_bestRequest_id_30 = ((! targets_1_requests_21_valid) || (targets_1_requests_20_valid && (targets_1_requests_21_priority <= targets_1_requests_20_priority)));
   assign _zz_targets_1_bestRequest_id_31 = (_zz_targets_1_bestRequest_id_30 ? targets_1_requests_20_priority : targets_1_requests_21_priority);
   assign _zz_targets_1_bestRequest_id_32 = (_zz_targets_1_bestRequest_id_30 ? targets_1_requests_20_valid : targets_1_requests_21_valid);
   assign _zz_targets_1_bestRequest_id_33 = ((! targets_1_requests_23_valid) || (targets_1_requests_22_valid && (targets_1_requests_23_priority <= targets_1_requests_22_priority)));
   assign _zz_targets_1_bestRequest_id_34 = (_zz_targets_1_bestRequest_id_33 ? targets_1_requests_22_priority : targets_1_requests_23_priority);
   assign _zz_targets_1_bestRequest_id_35 = (_zz_targets_1_bestRequest_id_33 ? targets_1_requests_22_valid : targets_1_requests_23_valid);
   assign _zz_targets_1_bestRequest_id_36 = ((! targets_1_requests_25_valid) || (targets_1_requests_24_valid && (targets_1_requests_25_priority <= targets_1_requests_24_priority)));
   assign _zz_targets_1_bestRequest_id_37 = (_zz_targets_1_bestRequest_id_36 ? targets_1_requests_24_priority : targets_1_requests_25_priority);
   assign _zz_targets_1_bestRequest_id_38 = (_zz_targets_1_bestRequest_id_36 ? targets_1_requests_24_valid : targets_1_requests_25_valid);
   assign _zz_targets_1_bestRequest_id_39 = ((! targets_1_requests_27_valid) || (targets_1_requests_26_valid && (targets_1_requests_27_priority <= targets_1_requests_26_priority)));
   assign _zz_targets_1_bestRequest_id_40 = (_zz_targets_1_bestRequest_id_39 ? targets_1_requests_26_priority : targets_1_requests_27_priority);
   assign _zz_targets_1_bestRequest_id_41 = (_zz_targets_1_bestRequest_id_39 ? targets_1_requests_26_valid : targets_1_requests_27_valid);
   assign _zz_targets_1_bestRequest_id_42 = ((! targets_1_requests_29_valid) || (targets_1_requests_28_valid && (targets_1_requests_29_priority <= targets_1_requests_28_priority)));
   assign _zz_targets_1_bestRequest_id_43 = (_zz_targets_1_bestRequest_id_42 ? targets_1_requests_28_priority : targets_1_requests_29_priority);
   assign _zz_targets_1_bestRequest_id_44 = (_zz_targets_1_bestRequest_id_42 ? targets_1_requests_28_valid : targets_1_requests_29_valid);
   assign _zz_targets_1_bestRequest_id_45 = ((! targets_1_requests_31_valid) || (targets_1_requests_30_valid && (targets_1_requests_31_priority <= targets_1_requests_30_priority)));
   assign _zz_targets_1_bestRequest_id_46 = (_zz_targets_1_bestRequest_id_45 ? targets_1_requests_30_priority : targets_1_requests_31_priority);
   assign _zz_targets_1_bestRequest_id_47 = (_zz_targets_1_bestRequest_id_45 ? targets_1_requests_30_valid : targets_1_requests_31_valid);
   assign _zz_targets_1_bestRequest_id_48 = ((! _zz_targets_1_bestRequest_id_5) || (_zz_targets_1_bestRequest_id_2 && (_zz_targets_1_bestRequest_id_4 <= _zz_targets_1_bestRequest_id_1)));
   assign _zz_targets_1_bestRequest_id_49 = (_zz_targets_1_bestRequest_id_48 ? _zz_targets_1_bestRequest_id_1 : _zz_targets_1_bestRequest_id_4);
   assign _zz_targets_1_bestRequest_id_50 = (_zz_targets_1_bestRequest_id_48 ? _zz_targets_1_bestRequest_id_2 : _zz_targets_1_bestRequest_id_5);
   assign _zz_targets_1_bestRequest_id_51 = ((! _zz_targets_1_bestRequest_id_11) || (_zz_targets_1_bestRequest_id_8 && (_zz_targets_1_bestRequest_id_10 <= _zz_targets_1_bestRequest_id_7)));
   assign _zz_targets_1_bestRequest_id_52 = (_zz_targets_1_bestRequest_id_51 ? _zz_targets_1_bestRequest_id_7 : _zz_targets_1_bestRequest_id_10);
   assign _zz_targets_1_bestRequest_id_53 = (_zz_targets_1_bestRequest_id_51 ? _zz_targets_1_bestRequest_id_8 : _zz_targets_1_bestRequest_id_11);
   assign _zz_targets_1_bestRequest_id_54 = ((! _zz_targets_1_bestRequest_id_17) || (_zz_targets_1_bestRequest_id_14 && (_zz_targets_1_bestRequest_id_16 <= _zz_targets_1_bestRequest_id_13)));
   assign _zz_targets_1_bestRequest_id_55 = (_zz_targets_1_bestRequest_id_54 ? _zz_targets_1_bestRequest_id_13 : _zz_targets_1_bestRequest_id_16);
   assign _zz_targets_1_bestRequest_id_56 = (_zz_targets_1_bestRequest_id_54 ? _zz_targets_1_bestRequest_id_14 : _zz_targets_1_bestRequest_id_17);
   assign _zz_targets_1_bestRequest_id_57 = ((! _zz_targets_1_bestRequest_id_23) || (_zz_targets_1_bestRequest_id_20 && (_zz_targets_1_bestRequest_id_22 <= _zz_targets_1_bestRequest_id_19)));
   assign _zz_targets_1_bestRequest_id_58 = (_zz_targets_1_bestRequest_id_57 ? _zz_targets_1_bestRequest_id_19 : _zz_targets_1_bestRequest_id_22);
   assign _zz_targets_1_bestRequest_id_59 = (_zz_targets_1_bestRequest_id_57 ? _zz_targets_1_bestRequest_id_20 : _zz_targets_1_bestRequest_id_23);
   assign _zz_targets_1_bestRequest_id_60 = ((! _zz_targets_1_bestRequest_id_29) || (_zz_targets_1_bestRequest_id_26 && (_zz_targets_1_bestRequest_id_28 <= _zz_targets_1_bestRequest_id_25)));
   assign _zz_targets_1_bestRequest_id_61 = (_zz_targets_1_bestRequest_id_60 ? _zz_targets_1_bestRequest_id_25 : _zz_targets_1_bestRequest_id_28);
   assign _zz_targets_1_bestRequest_id_62 = (_zz_targets_1_bestRequest_id_60 ? _zz_targets_1_bestRequest_id_26 : _zz_targets_1_bestRequest_id_29);
   assign _zz_targets_1_bestRequest_id_63 = ((! _zz_targets_1_bestRequest_id_35) || (_zz_targets_1_bestRequest_id_32 && (_zz_targets_1_bestRequest_id_34 <= _zz_targets_1_bestRequest_id_31)));
   assign _zz_targets_1_bestRequest_id_64 = (_zz_targets_1_bestRequest_id_63 ? _zz_targets_1_bestRequest_id_31 : _zz_targets_1_bestRequest_id_34);
   assign _zz_targets_1_bestRequest_id_65 = (_zz_targets_1_bestRequest_id_63 ? _zz_targets_1_bestRequest_id_32 : _zz_targets_1_bestRequest_id_35);
   assign _zz_targets_1_bestRequest_id_66 = ((! _zz_targets_1_bestRequest_id_41) || (_zz_targets_1_bestRequest_id_38 && (_zz_targets_1_bestRequest_id_40 <= _zz_targets_1_bestRequest_id_37)));
   assign _zz_targets_1_bestRequest_id_67 = (_zz_targets_1_bestRequest_id_66 ? _zz_targets_1_bestRequest_id_37 : _zz_targets_1_bestRequest_id_40);
   assign _zz_targets_1_bestRequest_id_68 = (_zz_targets_1_bestRequest_id_66 ? _zz_targets_1_bestRequest_id_38 : _zz_targets_1_bestRequest_id_41);
   assign _zz_targets_1_bestRequest_id_69 = ((! _zz_targets_1_bestRequest_id_47) || (_zz_targets_1_bestRequest_id_44 && (_zz_targets_1_bestRequest_id_46 <= _zz_targets_1_bestRequest_id_43)));
   assign _zz_targets_1_bestRequest_id_70 = (_zz_targets_1_bestRequest_id_69 ? _zz_targets_1_bestRequest_id_43 : _zz_targets_1_bestRequest_id_46);
   assign _zz_targets_1_bestRequest_id_71 = (_zz_targets_1_bestRequest_id_69 ? _zz_targets_1_bestRequest_id_44 : _zz_targets_1_bestRequest_id_47);
   assign _zz_targets_1_bestRequest_id_72 = ((! _zz_targets_1_bestRequest_id_53) || (_zz_targets_1_bestRequest_id_50 && (_zz_targets_1_bestRequest_id_52 <= _zz_targets_1_bestRequest_id_49)));
   assign _zz_targets_1_bestRequest_priority = (_zz_targets_1_bestRequest_id_72 ? _zz_targets_1_bestRequest_id_49 : _zz_targets_1_bestRequest_id_52);
   assign _zz_targets_1_bestRequest_id_73 = (_zz_targets_1_bestRequest_id_72 ? _zz_targets_1_bestRequest_id_50 : _zz_targets_1_bestRequest_id_53);
   assign _zz_targets_1_bestRequest_id_74 = ((! _zz_targets_1_bestRequest_id_59) || (_zz_targets_1_bestRequest_id_56 && (_zz_targets_1_bestRequest_id_58 <= _zz_targets_1_bestRequest_id_55)));
   assign _zz_targets_1_bestRequest_priority_1 = (_zz_targets_1_bestRequest_id_74 ? _zz_targets_1_bestRequest_id_55 : _zz_targets_1_bestRequest_id_58);
   assign _zz_targets_1_bestRequest_id_75 = (_zz_targets_1_bestRequest_id_74 ? _zz_targets_1_bestRequest_id_56 : _zz_targets_1_bestRequest_id_59);
   assign _zz_targets_1_bestRequest_id_76 = ((! _zz_targets_1_bestRequest_id_65) || (_zz_targets_1_bestRequest_id_62 && (_zz_targets_1_bestRequest_id_64 <= _zz_targets_1_bestRequest_id_61)));
   assign _zz_targets_1_bestRequest_priority_2 = (_zz_targets_1_bestRequest_id_76 ? _zz_targets_1_bestRequest_id_61 : _zz_targets_1_bestRequest_id_64);
   assign _zz_targets_1_bestRequest_id_77 = (_zz_targets_1_bestRequest_id_76 ? _zz_targets_1_bestRequest_id_62 : _zz_targets_1_bestRequest_id_65);
   assign _zz_targets_1_bestRequest_id_78 = ((! _zz_targets_1_bestRequest_id_71) || (_zz_targets_1_bestRequest_id_68 && (_zz_targets_1_bestRequest_id_70 <= _zz_targets_1_bestRequest_id_67)));
   assign _zz_targets_1_bestRequest_priority_3 = (_zz_targets_1_bestRequest_id_78 ? _zz_targets_1_bestRequest_id_67 : _zz_targets_1_bestRequest_id_70);
   assign _zz_targets_1_bestRequest_id_79 = (_zz_targets_1_bestRequest_id_78 ? _zz_targets_1_bestRequest_id_68 : _zz_targets_1_bestRequest_id_71);
   assign _zz_targets_1_bestRequest_id_80 = ((! _zz_targets_1_bestRequest_id_75) || (_zz_targets_1_bestRequest_id_73 && (_zz_targets_1_bestRequest_priority_1 <= _zz_targets_1_bestRequest_priority)));
   assign _zz_targets_1_bestRequest_priority_4 = (_zz_targets_1_bestRequest_id_80 ? _zz_targets_1_bestRequest_priority : _zz_targets_1_bestRequest_priority_1);
   assign _zz_targets_1_bestRequest_valid = (_zz_targets_1_bestRequest_id_80 ? _zz_targets_1_bestRequest_id_73 : _zz_targets_1_bestRequest_id_75);
   assign _zz_targets_1_bestRequest_id_81 = ((! _zz_targets_1_bestRequest_id_79) || (_zz_targets_1_bestRequest_id_77 && (_zz_targets_1_bestRequest_priority_3 <= _zz_targets_1_bestRequest_priority_2)));
   assign _zz_targets_1_bestRequest_priority_5 = (_zz_targets_1_bestRequest_id_81 ? _zz_targets_1_bestRequest_priority_2 : _zz_targets_1_bestRequest_priority_3);
   assign _zz_targets_1_bestRequest_valid_1 = (_zz_targets_1_bestRequest_id_81 ? _zz_targets_1_bestRequest_id_77 : _zz_targets_1_bestRequest_id_79);
   assign _zz_targets_1_bestRequest_priority_6 = ((! _zz_targets_1_bestRequest_valid_1) || (_zz_targets_1_bestRequest_valid && (_zz_targets_1_bestRequest_priority_5 <= _zz_targets_1_bestRequest_priority_4)));
   assign targets_1_iep = (targets_1_threshold < targets_1_bestRequest_priority);
   assign targets_1_claim = (targets_1_iep ? targets_1_bestRequest_id : 5'h00);
   assign io_targets = {targets_1_iep, targets_0_iep};
   assign bus_readErrorFlag = 1'b0;
   assign bus_writeErrorFlag = 1'b0;
   always @(*) begin
      bus_readHaltRequest = 1'b0;
      if (when_PlicMapper_l122) begin
         bus_readHaltRequest = 1'b1;
      end
   end

   assign bus_writeHaltRequest = 1'b0;
   assign bus_writeOccur = (bus_writeJoinEvent_valid && bus_writeJoinEvent_ready);
   assign bus_writeJoinEvent_valid = (io_bus_aw_valid && io_bus_w_valid);
   assign io_bus_aw_ready = bus_writeOccur;
   assign io_bus_w_ready = bus_writeOccur;
   assign bus_writeJoinEvent_translated_valid = bus_writeJoinEvent_valid;
   assign bus_writeJoinEvent_ready = bus_writeJoinEvent_translated_ready;
   assign bus_writeJoinEvent_translated_payload_resp = bus_writeRsp_resp;
   assign _zz_bus_writeJoinEvent_translated_ready = (!bus_writeHaltRequest);
   assign bus_writeJoinEvent_translated_ready = (_zz_bus_writeJoinEvent_translated_ready_1 && _zz_bus_writeJoinEvent_translated_ready);
   always @(*) begin
      _zz_bus_writeJoinEvent_translated_ready_1 = io_bus_b_ready;
      if (when_Stream_l369) begin
         _zz_bus_writeJoinEvent_translated_ready_1 = 1'b1;
      end
   end

   assign when_Stream_l369      = (!_zz_io_bus_b_valid);
   assign _zz_io_bus_b_valid    = _zz_io_bus_b_valid_1;
   assign io_bus_b_valid        = _zz_io_bus_b_valid;
   assign io_bus_b_payload_resp = _zz_io_bus_b_payload_resp;
   always @(*) begin
      io_bus_ar_ready = bus_readDataStage_ready;
      if (when_Stream_l369_1) begin
         io_bus_ar_ready = 1'b1;
      end
   end

   assign when_Stream_l369_1             = (!bus_readDataStage_valid);
   assign bus_readDataStage_valid        = io_bus_ar_rValid;
   assign bus_readDataStage_payload_addr = io_bus_ar_rData_addr;
   assign bus_readDataStage_payload_prot = io_bus_ar_rData_prot;
   assign _zz_io_bus_r_valid             = (!bus_readHaltRequest);
   assign bus_readDataStage_ready        = (io_bus_r_ready && _zz_io_bus_r_valid);
   assign io_bus_r_valid                 = (bus_readDataStage_valid && _zz_io_bus_r_valid);
   assign io_bus_r_payload_data          = bus_readRsp_data;
   assign io_bus_r_payload_resp          = bus_readRsp_resp;
   always @(*) begin
      if (bus_writeErrorFlag) begin
         bus_writeRsp_resp = 2'b10;
      end else begin
         bus_writeRsp_resp = 2'b00;
      end
   end

   always @(*) begin
      if (bus_readErrorFlag) begin
         bus_readRsp_resp = 2'b10;
      end else begin
         bus_readRsp_resp = 2'b00;
      end
   end

   always @(*) begin
      bus_readRsp_data = 32'h00000000;
      case (bus_readAddressMasked)
         22'h000004: begin
            bus_readRsp_data[1 : 0] = gateways_0_priority;
         end
         22'h001000: begin
            bus_readRsp_data[1 : 1]   = gateways_0_ip;
            bus_readRsp_data[2 : 2]   = gateways_1_ip;
            bus_readRsp_data[3 : 3]   = gateways_2_ip;
            bus_readRsp_data[4 : 4]   = gateways_3_ip;
            bus_readRsp_data[5 : 5]   = gateways_4_ip;
            bus_readRsp_data[6 : 6]   = gateways_5_ip;
            bus_readRsp_data[7 : 7]   = gateways_6_ip;
            bus_readRsp_data[8 : 8]   = gateways_7_ip;
            bus_readRsp_data[9 : 9]   = gateways_8_ip;
            bus_readRsp_data[10 : 10] = gateways_9_ip;
            bus_readRsp_data[11 : 11] = gateways_10_ip;
            bus_readRsp_data[12 : 12] = gateways_11_ip;
            bus_readRsp_data[13 : 13] = gateways_12_ip;
            bus_readRsp_data[14 : 14] = gateways_13_ip;
            bus_readRsp_data[15 : 15] = gateways_14_ip;
            bus_readRsp_data[16 : 16] = gateways_15_ip;
            bus_readRsp_data[17 : 17] = gateways_16_ip;
            bus_readRsp_data[18 : 18] = gateways_17_ip;
            bus_readRsp_data[19 : 19] = gateways_18_ip;
            bus_readRsp_data[20 : 20] = gateways_19_ip;
            bus_readRsp_data[21 : 21] = gateways_20_ip;
            bus_readRsp_data[22 : 22] = gateways_21_ip;
            bus_readRsp_data[23 : 23] = gateways_22_ip;
            bus_readRsp_data[24 : 24] = gateways_23_ip;
            bus_readRsp_data[25 : 25] = gateways_24_ip;
            bus_readRsp_data[26 : 26] = gateways_25_ip;
            bus_readRsp_data[27 : 27] = gateways_26_ip;
            bus_readRsp_data[28 : 28] = gateways_27_ip;
            bus_readRsp_data[29 : 29] = gateways_28_ip;
            bus_readRsp_data[30 : 30] = gateways_29_ip;
            bus_readRsp_data[31 : 31] = gateways_30_ip;
         end
         22'h000008: begin
            bus_readRsp_data[1 : 0] = gateways_1_priority;
         end
         22'h00000c: begin
            bus_readRsp_data[1 : 0] = gateways_2_priority;
         end
         22'h000010: begin
            bus_readRsp_data[1 : 0] = gateways_3_priority;
         end
         22'h000014: begin
            bus_readRsp_data[1 : 0] = gateways_4_priority;
         end
         22'h000018: begin
            bus_readRsp_data[1 : 0] = gateways_5_priority;
         end
         22'h00001c: begin
            bus_readRsp_data[1 : 0] = gateways_6_priority;
         end
         22'h000020: begin
            bus_readRsp_data[1 : 0] = gateways_7_priority;
         end
         22'h000024: begin
            bus_readRsp_data[1 : 0] = gateways_8_priority;
         end
         22'h000028: begin
            bus_readRsp_data[1 : 0] = gateways_9_priority;
         end
         22'h00002c: begin
            bus_readRsp_data[1 : 0] = gateways_10_priority;
         end
         22'h000030: begin
            bus_readRsp_data[1 : 0] = gateways_11_priority;
         end
         22'h000034: begin
            bus_readRsp_data[1 : 0] = gateways_12_priority;
         end
         22'h000038: begin
            bus_readRsp_data[1 : 0] = gateways_13_priority;
         end
         22'h00003c: begin
            bus_readRsp_data[1 : 0] = gateways_14_priority;
         end
         22'h000040: begin
            bus_readRsp_data[1 : 0] = gateways_15_priority;
         end
         22'h000044: begin
            bus_readRsp_data[1 : 0] = gateways_16_priority;
         end
         22'h000048: begin
            bus_readRsp_data[1 : 0] = gateways_17_priority;
         end
         22'h00004c: begin
            bus_readRsp_data[1 : 0] = gateways_18_priority;
         end
         22'h000050: begin
            bus_readRsp_data[1 : 0] = gateways_19_priority;
         end
         22'h000054: begin
            bus_readRsp_data[1 : 0] = gateways_20_priority;
         end
         22'h000058: begin
            bus_readRsp_data[1 : 0] = gateways_21_priority;
         end
         22'h00005c: begin
            bus_readRsp_data[1 : 0] = gateways_22_priority;
         end
         22'h000060: begin
            bus_readRsp_data[1 : 0] = gateways_23_priority;
         end
         22'h000064: begin
            bus_readRsp_data[1 : 0] = gateways_24_priority;
         end
         22'h000068: begin
            bus_readRsp_data[1 : 0] = gateways_25_priority;
         end
         22'h00006c: begin
            bus_readRsp_data[1 : 0] = gateways_26_priority;
         end
         22'h000070: begin
            bus_readRsp_data[1 : 0] = gateways_27_priority;
         end
         22'h000074: begin
            bus_readRsp_data[1 : 0] = gateways_28_priority;
         end
         22'h000078: begin
            bus_readRsp_data[1 : 0] = gateways_29_priority;
         end
         22'h00007c: begin
            bus_readRsp_data[1 : 0] = gateways_30_priority;
         end
         22'h200000: begin
            bus_readRsp_data[1 : 0] = targets_0_threshold;
         end
         22'h200004: begin
            bus_readRsp_data[4 : 0] = targets_0_claim;
         end
         22'h002000: begin
            bus_readRsp_data[1 : 1]   = targets_0_ie_0;
            bus_readRsp_data[2 : 2]   = targets_0_ie_1;
            bus_readRsp_data[3 : 3]   = targets_0_ie_2;
            bus_readRsp_data[4 : 4]   = targets_0_ie_3;
            bus_readRsp_data[5 : 5]   = targets_0_ie_4;
            bus_readRsp_data[6 : 6]   = targets_0_ie_5;
            bus_readRsp_data[7 : 7]   = targets_0_ie_6;
            bus_readRsp_data[8 : 8]   = targets_0_ie_7;
            bus_readRsp_data[9 : 9]   = targets_0_ie_8;
            bus_readRsp_data[10 : 10] = targets_0_ie_9;
            bus_readRsp_data[11 : 11] = targets_0_ie_10;
            bus_readRsp_data[12 : 12] = targets_0_ie_11;
            bus_readRsp_data[13 : 13] = targets_0_ie_12;
            bus_readRsp_data[14 : 14] = targets_0_ie_13;
            bus_readRsp_data[15 : 15] = targets_0_ie_14;
            bus_readRsp_data[16 : 16] = targets_0_ie_15;
            bus_readRsp_data[17 : 17] = targets_0_ie_16;
            bus_readRsp_data[18 : 18] = targets_0_ie_17;
            bus_readRsp_data[19 : 19] = targets_0_ie_18;
            bus_readRsp_data[20 : 20] = targets_0_ie_19;
            bus_readRsp_data[21 : 21] = targets_0_ie_20;
            bus_readRsp_data[22 : 22] = targets_0_ie_21;
            bus_readRsp_data[23 : 23] = targets_0_ie_22;
            bus_readRsp_data[24 : 24] = targets_0_ie_23;
            bus_readRsp_data[25 : 25] = targets_0_ie_24;
            bus_readRsp_data[26 : 26] = targets_0_ie_25;
            bus_readRsp_data[27 : 27] = targets_0_ie_26;
            bus_readRsp_data[28 : 28] = targets_0_ie_27;
            bus_readRsp_data[29 : 29] = targets_0_ie_28;
            bus_readRsp_data[30 : 30] = targets_0_ie_29;
            bus_readRsp_data[31 : 31] = targets_0_ie_30;
         end
         22'h201000: begin
            bus_readRsp_data[1 : 0] = targets_1_threshold;
         end
         22'h201004: begin
            bus_readRsp_data[4 : 0] = targets_1_claim;
         end
         22'h002080: begin
            bus_readRsp_data[1 : 1]   = targets_1_ie_0;
            bus_readRsp_data[2 : 2]   = targets_1_ie_1;
            bus_readRsp_data[3 : 3]   = targets_1_ie_2;
            bus_readRsp_data[4 : 4]   = targets_1_ie_3;
            bus_readRsp_data[5 : 5]   = targets_1_ie_4;
            bus_readRsp_data[6 : 6]   = targets_1_ie_5;
            bus_readRsp_data[7 : 7]   = targets_1_ie_6;
            bus_readRsp_data[8 : 8]   = targets_1_ie_7;
            bus_readRsp_data[9 : 9]   = targets_1_ie_8;
            bus_readRsp_data[10 : 10] = targets_1_ie_9;
            bus_readRsp_data[11 : 11] = targets_1_ie_10;
            bus_readRsp_data[12 : 12] = targets_1_ie_11;
            bus_readRsp_data[13 : 13] = targets_1_ie_12;
            bus_readRsp_data[14 : 14] = targets_1_ie_13;
            bus_readRsp_data[15 : 15] = targets_1_ie_14;
            bus_readRsp_data[16 : 16] = targets_1_ie_15;
            bus_readRsp_data[17 : 17] = targets_1_ie_16;
            bus_readRsp_data[18 : 18] = targets_1_ie_17;
            bus_readRsp_data[19 : 19] = targets_1_ie_18;
            bus_readRsp_data[20 : 20] = targets_1_ie_19;
            bus_readRsp_data[21 : 21] = targets_1_ie_20;
            bus_readRsp_data[22 : 22] = targets_1_ie_21;
            bus_readRsp_data[23 : 23] = targets_1_ie_22;
            bus_readRsp_data[24 : 24] = targets_1_ie_23;
            bus_readRsp_data[25 : 25] = targets_1_ie_24;
            bus_readRsp_data[26 : 26] = targets_1_ie_25;
            bus_readRsp_data[27 : 27] = targets_1_ie_26;
            bus_readRsp_data[28 : 28] = targets_1_ie_27;
            bus_readRsp_data[29 : 29] = targets_1_ie_28;
            bus_readRsp_data[30 : 30] = targets_1_ie_29;
            bus_readRsp_data[31 : 31] = targets_1_ie_30;
         end
         default: begin
         end
      endcase
   end

   assign bus_readAddressMasked  = (bus_readDataStage_payload_addr & (~22'h000003));
   assign bus_writeAddressMasked = (io_bus_aw_payload_addr & (~22'h000003));
   assign bus_readOccur          = (io_bus_r_valid && io_bus_r_ready);
   assign gateways_0_priority    = _zz_gateways_0_priority;
   assign gateways_1_priority    = _zz_gateways_1_priority;
   assign gateways_2_priority    = _zz_gateways_2_priority;
   assign gateways_3_priority    = _zz_gateways_3_priority;
   assign gateways_4_priority    = _zz_gateways_4_priority;
   assign gateways_5_priority    = _zz_gateways_5_priority;
   assign gateways_6_priority    = _zz_gateways_6_priority;
   assign gateways_7_priority    = _zz_gateways_7_priority;
   assign gateways_8_priority    = _zz_gateways_8_priority;
   assign gateways_9_priority    = _zz_gateways_9_priority;
   assign gateways_10_priority   = _zz_gateways_10_priority;
   assign gateways_11_priority   = _zz_gateways_11_priority;
   assign gateways_12_priority   = _zz_gateways_12_priority;
   assign gateways_13_priority   = _zz_gateways_13_priority;
   assign gateways_14_priority   = _zz_gateways_14_priority;
   assign gateways_15_priority   = _zz_gateways_15_priority;
   assign gateways_16_priority   = _zz_gateways_16_priority;
   assign gateways_17_priority   = _zz_gateways_17_priority;
   assign gateways_18_priority   = _zz_gateways_18_priority;
   assign gateways_19_priority   = _zz_gateways_19_priority;
   assign gateways_20_priority   = _zz_gateways_20_priority;
   assign gateways_21_priority   = _zz_gateways_21_priority;
   assign gateways_22_priority   = _zz_gateways_22_priority;
   assign gateways_23_priority   = _zz_gateways_23_priority;
   assign gateways_24_priority   = _zz_gateways_24_priority;
   assign gateways_25_priority   = _zz_gateways_25_priority;
   assign gateways_26_priority   = _zz_gateways_26_priority;
   assign gateways_27_priority   = _zz_gateways_27_priority;
   assign gateways_28_priority   = _zz_gateways_28_priority;
   assign gateways_29_priority   = _zz_gateways_29_priority;
   assign gateways_30_priority   = _zz_gateways_30_priority;
   always @(*) begin
      mapping_claim_valid = 1'b0;
      case (bus_readAddressMasked)
         22'h200004: begin
            if (bus_readOccur) begin
               mapping_claim_valid = 1'b1;
            end
         end
         22'h201004: begin
            if (bus_readOccur) begin
               mapping_claim_valid = 1'b1;
            end
         end
         default: begin
         end
      endcase
   end

   always @(*) begin
      mapping_claim_payload = 5'bxxxxx;
      case (bus_readAddressMasked)
         22'h200004: begin
            if (bus_readOccur) begin
               mapping_claim_payload = targets_0_claim;
            end
         end
         22'h201004: begin
            if (bus_readOccur) begin
               mapping_claim_payload = targets_1_claim;
            end
         end
         default: begin
         end
      endcase
   end

   always @(*) begin
      mapping_completion_valid = 1'b0;
      if (mapping_targetMapping_0_targetCompletion_valid) begin
         mapping_completion_valid = 1'b1;
      end
      if (mapping_targetMapping_1_targetCompletion_valid) begin
         mapping_completion_valid = 1'b1;
      end
   end

   always @(*) begin
      mapping_completion_payload = 5'bxxxxx;
      if (mapping_targetMapping_0_targetCompletion_valid) begin
         mapping_completion_payload = mapping_targetMapping_0_targetCompletion_payload;
      end
      if (mapping_targetMapping_1_targetCompletion_valid) begin
         mapping_completion_payload = mapping_targetMapping_1_targetCompletion_payload;
      end
   end

   always @(*) begin
      mapping_coherencyStall_willIncrement = 1'b0;
      if (when_PlicMapper_l122) begin
         mapping_coherencyStall_willIncrement = 1'b1;
      end
      if (when_AxiLite4SlaveFactory_l68) begin
         if (bus_writeJoinEvent_valid) begin
            mapping_coherencyStall_willIncrement = 1'b1;
         end
      end
      if (when_AxiLite4SlaveFactory_l86) begin
         if (bus_readDataStage_valid) begin
            mapping_coherencyStall_willIncrement = 1'b1;
         end
      end
   end

   assign mapping_coherencyStall_willClear = 1'b0;
   assign mapping_coherencyStall_willOverflowIfInc = (mapping_coherencyStall_value == 1'b1);
   assign mapping_coherencyStall_willOverflow = (mapping_coherencyStall_willOverflowIfInc && mapping_coherencyStall_willIncrement);
   always @(*) begin
      mapping_coherencyStall_valueNext = (mapping_coherencyStall_value + mapping_coherencyStall_willIncrement);
      if (mapping_coherencyStall_willClear) begin
         mapping_coherencyStall_valueNext = 1'b0;
      end
   end

   assign when_PlicMapper_l122 = (mapping_coherencyStall_value != 1'b0);
   assign targets_0_threshold  = _zz_targets_0_threshold;
   always @(*) begin
      mapping_targetMapping_0_targetCompletion_valid = 1'b0;
      case (bus_writeAddressMasked)
         22'h200004: begin
            if (bus_writeOccur) begin
               mapping_targetMapping_0_targetCompletion_valid = 1'b1;
            end
         end
         default: begin
         end
      endcase
   end

   assign targets_0_ie_0      = _zz_targets_0_ie_0;
   assign targets_0_ie_1      = _zz_targets_0_ie_1;
   assign targets_0_ie_2      = _zz_targets_0_ie_2;
   assign targets_0_ie_3      = _zz_targets_0_ie_3;
   assign targets_0_ie_4      = _zz_targets_0_ie_4;
   assign targets_0_ie_5      = _zz_targets_0_ie_5;
   assign targets_0_ie_6      = _zz_targets_0_ie_6;
   assign targets_0_ie_7      = _zz_targets_0_ie_7;
   assign targets_0_ie_8      = _zz_targets_0_ie_8;
   assign targets_0_ie_9      = _zz_targets_0_ie_9;
   assign targets_0_ie_10     = _zz_targets_0_ie_10;
   assign targets_0_ie_11     = _zz_targets_0_ie_11;
   assign targets_0_ie_12     = _zz_targets_0_ie_12;
   assign targets_0_ie_13     = _zz_targets_0_ie_13;
   assign targets_0_ie_14     = _zz_targets_0_ie_14;
   assign targets_0_ie_15     = _zz_targets_0_ie_15;
   assign targets_0_ie_16     = _zz_targets_0_ie_16;
   assign targets_0_ie_17     = _zz_targets_0_ie_17;
   assign targets_0_ie_18     = _zz_targets_0_ie_18;
   assign targets_0_ie_19     = _zz_targets_0_ie_19;
   assign targets_0_ie_20     = _zz_targets_0_ie_20;
   assign targets_0_ie_21     = _zz_targets_0_ie_21;
   assign targets_0_ie_22     = _zz_targets_0_ie_22;
   assign targets_0_ie_23     = _zz_targets_0_ie_23;
   assign targets_0_ie_24     = _zz_targets_0_ie_24;
   assign targets_0_ie_25     = _zz_targets_0_ie_25;
   assign targets_0_ie_26     = _zz_targets_0_ie_26;
   assign targets_0_ie_27     = _zz_targets_0_ie_27;
   assign targets_0_ie_28     = _zz_targets_0_ie_28;
   assign targets_0_ie_29     = _zz_targets_0_ie_29;
   assign targets_0_ie_30     = _zz_targets_0_ie_30;
   assign targets_1_threshold = _zz_targets_1_threshold;
   always @(*) begin
      mapping_targetMapping_1_targetCompletion_valid = 1'b0;
      case (bus_writeAddressMasked)
         22'h201004: begin
            if (bus_writeOccur) begin
               mapping_targetMapping_1_targetCompletion_valid = 1'b1;
            end
         end
         default: begin
         end
      endcase
   end

   assign targets_1_ie_0                                   = _zz_targets_1_ie_0;
   assign targets_1_ie_1                                   = _zz_targets_1_ie_1;
   assign targets_1_ie_2                                   = _zz_targets_1_ie_2;
   assign targets_1_ie_3                                   = _zz_targets_1_ie_3;
   assign targets_1_ie_4                                   = _zz_targets_1_ie_4;
   assign targets_1_ie_5                                   = _zz_targets_1_ie_5;
   assign targets_1_ie_6                                   = _zz_targets_1_ie_6;
   assign targets_1_ie_7                                   = _zz_targets_1_ie_7;
   assign targets_1_ie_8                                   = _zz_targets_1_ie_8;
   assign targets_1_ie_9                                   = _zz_targets_1_ie_9;
   assign targets_1_ie_10                                  = _zz_targets_1_ie_10;
   assign targets_1_ie_11                                  = _zz_targets_1_ie_11;
   assign targets_1_ie_12                                  = _zz_targets_1_ie_12;
   assign targets_1_ie_13                                  = _zz_targets_1_ie_13;
   assign targets_1_ie_14                                  = _zz_targets_1_ie_14;
   assign targets_1_ie_15                                  = _zz_targets_1_ie_15;
   assign targets_1_ie_16                                  = _zz_targets_1_ie_16;
   assign targets_1_ie_17                                  = _zz_targets_1_ie_17;
   assign targets_1_ie_18                                  = _zz_targets_1_ie_18;
   assign targets_1_ie_19                                  = _zz_targets_1_ie_19;
   assign targets_1_ie_20                                  = _zz_targets_1_ie_20;
   assign targets_1_ie_21                                  = _zz_targets_1_ie_21;
   assign targets_1_ie_22                                  = _zz_targets_1_ie_22;
   assign targets_1_ie_23                                  = _zz_targets_1_ie_23;
   assign targets_1_ie_24                                  = _zz_targets_1_ie_24;
   assign targets_1_ie_25                                  = _zz_targets_1_ie_25;
   assign targets_1_ie_26                                  = _zz_targets_1_ie_26;
   assign targets_1_ie_27                                  = _zz_targets_1_ie_27;
   assign targets_1_ie_28                                  = _zz_targets_1_ie_28;
   assign targets_1_ie_29                                  = _zz_targets_1_ie_29;
   assign targets_1_ie_30                                  = _zz_targets_1_ie_30;
   assign mapping_targetMapping_0_targetCompletion_payload = io_bus_w_payload_data[4 : 0];
   assign mapping_targetMapping_1_targetCompletion_payload = io_bus_w_payload_data[4 : 0];
   assign when_AxiLite4SlaveFactory_l68                    = 1'b1;
   assign when_AxiLite4SlaveFactory_l86                    = 1'b1;
   always @(posedge clk or posedge reset) begin
      if (reset) begin
         gateways_0_ip                <= 1'b0;
         gateways_0_waitCompletion    <= 1'b0;
         gateways_1_ip                <= 1'b0;
         gateways_1_waitCompletion    <= 1'b0;
         gateways_2_ip                <= 1'b0;
         gateways_2_waitCompletion    <= 1'b0;
         gateways_3_ip                <= 1'b0;
         gateways_3_waitCompletion    <= 1'b0;
         gateways_4_ip                <= 1'b0;
         gateways_4_waitCompletion    <= 1'b0;
         gateways_5_ip                <= 1'b0;
         gateways_5_waitCompletion    <= 1'b0;
         gateways_6_ip                <= 1'b0;
         gateways_6_waitCompletion    <= 1'b0;
         gateways_7_ip                <= 1'b0;
         gateways_7_waitCompletion    <= 1'b0;
         gateways_8_ip                <= 1'b0;
         gateways_8_waitCompletion    <= 1'b0;
         gateways_9_ip                <= 1'b0;
         gateways_9_waitCompletion    <= 1'b0;
         gateways_10_ip               <= 1'b0;
         gateways_10_waitCompletion   <= 1'b0;
         gateways_11_ip               <= 1'b0;
         gateways_11_waitCompletion   <= 1'b0;
         gateways_12_ip               <= 1'b0;
         gateways_12_waitCompletion   <= 1'b0;
         gateways_13_ip               <= 1'b0;
         gateways_13_waitCompletion   <= 1'b0;
         gateways_14_ip               <= 1'b0;
         gateways_14_waitCompletion   <= 1'b0;
         gateways_15_ip               <= 1'b0;
         gateways_15_waitCompletion   <= 1'b0;
         gateways_16_ip               <= 1'b0;
         gateways_16_waitCompletion   <= 1'b0;
         gateways_17_ip               <= 1'b0;
         gateways_17_waitCompletion   <= 1'b0;
         gateways_18_ip               <= 1'b0;
         gateways_18_waitCompletion   <= 1'b0;
         gateways_19_ip               <= 1'b0;
         gateways_19_waitCompletion   <= 1'b0;
         gateways_20_ip               <= 1'b0;
         gateways_20_waitCompletion   <= 1'b0;
         gateways_21_ip               <= 1'b0;
         gateways_21_waitCompletion   <= 1'b0;
         gateways_22_ip               <= 1'b0;
         gateways_22_waitCompletion   <= 1'b0;
         gateways_23_ip               <= 1'b0;
         gateways_23_waitCompletion   <= 1'b0;
         gateways_24_ip               <= 1'b0;
         gateways_24_waitCompletion   <= 1'b0;
         gateways_25_ip               <= 1'b0;
         gateways_25_waitCompletion   <= 1'b0;
         gateways_26_ip               <= 1'b0;
         gateways_26_waitCompletion   <= 1'b0;
         gateways_27_ip               <= 1'b0;
         gateways_27_waitCompletion   <= 1'b0;
         gateways_28_ip               <= 1'b0;
         gateways_28_waitCompletion   <= 1'b0;
         gateways_29_ip               <= 1'b0;
         gateways_29_waitCompletion   <= 1'b0;
         gateways_30_ip               <= 1'b0;
         gateways_30_waitCompletion   <= 1'b0;
         _zz_io_bus_b_valid_1         <= 1'b0;
         io_bus_ar_rValid             <= 1'b0;
         _zz_gateways_0_priority      <= 2'b00;
         _zz_gateways_1_priority      <= 2'b00;
         _zz_gateways_2_priority      <= 2'b00;
         _zz_gateways_3_priority      <= 2'b00;
         _zz_gateways_4_priority      <= 2'b00;
         _zz_gateways_5_priority      <= 2'b00;
         _zz_gateways_6_priority      <= 2'b00;
         _zz_gateways_7_priority      <= 2'b00;
         _zz_gateways_8_priority      <= 2'b00;
         _zz_gateways_9_priority      <= 2'b00;
         _zz_gateways_10_priority     <= 2'b00;
         _zz_gateways_11_priority     <= 2'b00;
         _zz_gateways_12_priority     <= 2'b00;
         _zz_gateways_13_priority     <= 2'b00;
         _zz_gateways_14_priority     <= 2'b00;
         _zz_gateways_15_priority     <= 2'b00;
         _zz_gateways_16_priority     <= 2'b00;
         _zz_gateways_17_priority     <= 2'b00;
         _zz_gateways_18_priority     <= 2'b00;
         _zz_gateways_19_priority     <= 2'b00;
         _zz_gateways_20_priority     <= 2'b00;
         _zz_gateways_21_priority     <= 2'b00;
         _zz_gateways_22_priority     <= 2'b00;
         _zz_gateways_23_priority     <= 2'b00;
         _zz_gateways_24_priority     <= 2'b00;
         _zz_gateways_25_priority     <= 2'b00;
         _zz_gateways_26_priority     <= 2'b00;
         _zz_gateways_27_priority     <= 2'b00;
         _zz_gateways_28_priority     <= 2'b00;
         _zz_gateways_29_priority     <= 2'b00;
         _zz_gateways_30_priority     <= 2'b00;
         mapping_coherencyStall_value <= 1'b0;
         _zz_targets_0_threshold      <= 2'b00;
         _zz_targets_0_ie_0           <= 1'b0;
         _zz_targets_0_ie_1           <= 1'b0;
         _zz_targets_0_ie_2           <= 1'b0;
         _zz_targets_0_ie_3           <= 1'b0;
         _zz_targets_0_ie_4           <= 1'b0;
         _zz_targets_0_ie_5           <= 1'b0;
         _zz_targets_0_ie_6           <= 1'b0;
         _zz_targets_0_ie_7           <= 1'b0;
         _zz_targets_0_ie_8           <= 1'b0;
         _zz_targets_0_ie_9           <= 1'b0;
         _zz_targets_0_ie_10          <= 1'b0;
         _zz_targets_0_ie_11          <= 1'b0;
         _zz_targets_0_ie_12          <= 1'b0;
         _zz_targets_0_ie_13          <= 1'b0;
         _zz_targets_0_ie_14          <= 1'b0;
         _zz_targets_0_ie_15          <= 1'b0;
         _zz_targets_0_ie_16          <= 1'b0;
         _zz_targets_0_ie_17          <= 1'b0;
         _zz_targets_0_ie_18          <= 1'b0;
         _zz_targets_0_ie_19          <= 1'b0;
         _zz_targets_0_ie_20          <= 1'b0;
         _zz_targets_0_ie_21          <= 1'b0;
         _zz_targets_0_ie_22          <= 1'b0;
         _zz_targets_0_ie_23          <= 1'b0;
         _zz_targets_0_ie_24          <= 1'b0;
         _zz_targets_0_ie_25          <= 1'b0;
         _zz_targets_0_ie_26          <= 1'b0;
         _zz_targets_0_ie_27          <= 1'b0;
         _zz_targets_0_ie_28          <= 1'b0;
         _zz_targets_0_ie_29          <= 1'b0;
         _zz_targets_0_ie_30          <= 1'b0;
         _zz_targets_1_threshold      <= 2'b00;
         _zz_targets_1_ie_0           <= 1'b0;
         _zz_targets_1_ie_1           <= 1'b0;
         _zz_targets_1_ie_2           <= 1'b0;
         _zz_targets_1_ie_3           <= 1'b0;
         _zz_targets_1_ie_4           <= 1'b0;
         _zz_targets_1_ie_5           <= 1'b0;
         _zz_targets_1_ie_6           <= 1'b0;
         _zz_targets_1_ie_7           <= 1'b0;
         _zz_targets_1_ie_8           <= 1'b0;
         _zz_targets_1_ie_9           <= 1'b0;
         _zz_targets_1_ie_10          <= 1'b0;
         _zz_targets_1_ie_11          <= 1'b0;
         _zz_targets_1_ie_12          <= 1'b0;
         _zz_targets_1_ie_13          <= 1'b0;
         _zz_targets_1_ie_14          <= 1'b0;
         _zz_targets_1_ie_15          <= 1'b0;
         _zz_targets_1_ie_16          <= 1'b0;
         _zz_targets_1_ie_17          <= 1'b0;
         _zz_targets_1_ie_18          <= 1'b0;
         _zz_targets_1_ie_19          <= 1'b0;
         _zz_targets_1_ie_20          <= 1'b0;
         _zz_targets_1_ie_21          <= 1'b0;
         _zz_targets_1_ie_22          <= 1'b0;
         _zz_targets_1_ie_23          <= 1'b0;
         _zz_targets_1_ie_24          <= 1'b0;
         _zz_targets_1_ie_25          <= 1'b0;
         _zz_targets_1_ie_26          <= 1'b0;
         _zz_targets_1_ie_27          <= 1'b0;
         _zz_targets_1_ie_28          <= 1'b0;
         _zz_targets_1_ie_29          <= 1'b0;
         _zz_targets_1_ie_30          <= 1'b0;
      end else begin
         if (when_PlicGateway_l21) begin
            gateways_0_ip             <= _zz_gateways_0_ip;
            gateways_0_waitCompletion <= _zz_gateways_0_ip;
         end
         if (when_PlicGateway_l21_1) begin
            gateways_1_ip             <= _zz_gateways_1_ip;
            gateways_1_waitCompletion <= _zz_gateways_1_ip;
         end
         if (when_PlicGateway_l21_2) begin
            gateways_2_ip             <= _zz_gateways_2_ip;
            gateways_2_waitCompletion <= _zz_gateways_2_ip;
         end
         if (when_PlicGateway_l21_3) begin
            gateways_3_ip             <= _zz_gateways_3_ip;
            gateways_3_waitCompletion <= _zz_gateways_3_ip;
         end
         if (when_PlicGateway_l21_4) begin
            gateways_4_ip             <= _zz_gateways_4_ip;
            gateways_4_waitCompletion <= _zz_gateways_4_ip;
         end
         if (when_PlicGateway_l21_5) begin
            gateways_5_ip             <= _zz_gateways_5_ip;
            gateways_5_waitCompletion <= _zz_gateways_5_ip;
         end
         if (when_PlicGateway_l21_6) begin
            gateways_6_ip             <= _zz_gateways_6_ip;
            gateways_6_waitCompletion <= _zz_gateways_6_ip;
         end
         if (when_PlicGateway_l21_7) begin
            gateways_7_ip             <= _zz_gateways_7_ip;
            gateways_7_waitCompletion <= _zz_gateways_7_ip;
         end
         if (when_PlicGateway_l21_8) begin
            gateways_8_ip             <= _zz_gateways_8_ip;
            gateways_8_waitCompletion <= _zz_gateways_8_ip;
         end
         if (when_PlicGateway_l21_9) begin
            gateways_9_ip             <= _zz_gateways_9_ip;
            gateways_9_waitCompletion <= _zz_gateways_9_ip;
         end
         if (when_PlicGateway_l21_10) begin
            gateways_10_ip             <= _zz_gateways_10_ip;
            gateways_10_waitCompletion <= _zz_gateways_10_ip;
         end
         if (when_PlicGateway_l21_11) begin
            gateways_11_ip             <= _zz_gateways_11_ip;
            gateways_11_waitCompletion <= _zz_gateways_11_ip;
         end
         if (when_PlicGateway_l21_12) begin
            gateways_12_ip             <= _zz_gateways_12_ip;
            gateways_12_waitCompletion <= _zz_gateways_12_ip;
         end
         if (when_PlicGateway_l21_13) begin
            gateways_13_ip             <= _zz_gateways_13_ip;
            gateways_13_waitCompletion <= _zz_gateways_13_ip;
         end
         if (when_PlicGateway_l21_14) begin
            gateways_14_ip             <= _zz_gateways_14_ip;
            gateways_14_waitCompletion <= _zz_gateways_14_ip;
         end
         if (when_PlicGateway_l21_15) begin
            gateways_15_ip             <= _zz_gateways_15_ip;
            gateways_15_waitCompletion <= _zz_gateways_15_ip;
         end
         if (when_PlicGateway_l21_16) begin
            gateways_16_ip             <= _zz_gateways_16_ip;
            gateways_16_waitCompletion <= _zz_gateways_16_ip;
         end
         if (when_PlicGateway_l21_17) begin
            gateways_17_ip             <= _zz_gateways_17_ip;
            gateways_17_waitCompletion <= _zz_gateways_17_ip;
         end
         if (when_PlicGateway_l21_18) begin
            gateways_18_ip             <= _zz_gateways_18_ip;
            gateways_18_waitCompletion <= _zz_gateways_18_ip;
         end
         if (when_PlicGateway_l21_19) begin
            gateways_19_ip             <= _zz_gateways_19_ip;
            gateways_19_waitCompletion <= _zz_gateways_19_ip;
         end
         if (when_PlicGateway_l21_20) begin
            gateways_20_ip             <= _zz_gateways_20_ip;
            gateways_20_waitCompletion <= _zz_gateways_20_ip;
         end
         if (when_PlicGateway_l21_21) begin
            gateways_21_ip             <= _zz_gateways_21_ip;
            gateways_21_waitCompletion <= _zz_gateways_21_ip;
         end
         if (when_PlicGateway_l21_22) begin
            gateways_22_ip             <= _zz_gateways_22_ip;
            gateways_22_waitCompletion <= _zz_gateways_22_ip;
         end
         if (when_PlicGateway_l21_23) begin
            gateways_23_ip             <= _zz_gateways_23_ip;
            gateways_23_waitCompletion <= _zz_gateways_23_ip;
         end
         if (when_PlicGateway_l21_24) begin
            gateways_24_ip             <= _zz_gateways_24_ip;
            gateways_24_waitCompletion <= _zz_gateways_24_ip;
         end
         if (when_PlicGateway_l21_25) begin
            gateways_25_ip             <= _zz_gateways_25_ip;
            gateways_25_waitCompletion <= _zz_gateways_25_ip;
         end
         if (when_PlicGateway_l21_26) begin
            gateways_26_ip             <= _zz_gateways_26_ip;
            gateways_26_waitCompletion <= _zz_gateways_26_ip;
         end
         if (when_PlicGateway_l21_27) begin
            gateways_27_ip             <= _zz_gateways_27_ip;
            gateways_27_waitCompletion <= _zz_gateways_27_ip;
         end
         if (when_PlicGateway_l21_28) begin
            gateways_28_ip             <= _zz_gateways_28_ip;
            gateways_28_waitCompletion <= _zz_gateways_28_ip;
         end
         if (when_PlicGateway_l21_29) begin
            gateways_29_ip             <= _zz_gateways_29_ip;
            gateways_29_waitCompletion <= _zz_gateways_29_ip;
         end
         if (when_PlicGateway_l21_30) begin
            gateways_30_ip             <= _zz_gateways_30_ip;
            gateways_30_waitCompletion <= _zz_gateways_30_ip;
         end
         if (_zz_bus_writeJoinEvent_translated_ready_1) begin
            _zz_io_bus_b_valid_1 <= (bus_writeJoinEvent_translated_valid && _zz_bus_writeJoinEvent_translated_ready);
         end
         if (io_bus_ar_ready) begin
            io_bus_ar_rValid <= io_bus_ar_valid;
         end
         if (mapping_claim_valid) begin
            case (mapping_claim_payload)
               5'h01: begin
                  gateways_0_ip <= 1'b0;
               end
               5'h02: begin
                  gateways_1_ip <= 1'b0;
               end
               5'h03: begin
                  gateways_2_ip <= 1'b0;
               end
               5'h04: begin
                  gateways_3_ip <= 1'b0;
               end
               5'h05: begin
                  gateways_4_ip <= 1'b0;
               end
               5'h06: begin
                  gateways_5_ip <= 1'b0;
               end
               5'h07: begin
                  gateways_6_ip <= 1'b0;
               end
               5'h08: begin
                  gateways_7_ip <= 1'b0;
               end
               5'h09: begin
                  gateways_8_ip <= 1'b0;
               end
               5'h0a: begin
                  gateways_9_ip <= 1'b0;
               end
               5'h0b: begin
                  gateways_10_ip <= 1'b0;
               end
               5'h0c: begin
                  gateways_11_ip <= 1'b0;
               end
               5'h0d: begin
                  gateways_12_ip <= 1'b0;
               end
               5'h0e: begin
                  gateways_13_ip <= 1'b0;
               end
               5'h0f: begin
                  gateways_14_ip <= 1'b0;
               end
               5'h10: begin
                  gateways_15_ip <= 1'b0;
               end
               5'h11: begin
                  gateways_16_ip <= 1'b0;
               end
               5'h12: begin
                  gateways_17_ip <= 1'b0;
               end
               5'h13: begin
                  gateways_18_ip <= 1'b0;
               end
               5'h14: begin
                  gateways_19_ip <= 1'b0;
               end
               5'h15: begin
                  gateways_20_ip <= 1'b0;
               end
               5'h16: begin
                  gateways_21_ip <= 1'b0;
               end
               5'h17: begin
                  gateways_22_ip <= 1'b0;
               end
               5'h18: begin
                  gateways_23_ip <= 1'b0;
               end
               5'h19: begin
                  gateways_24_ip <= 1'b0;
               end
               5'h1a: begin
                  gateways_25_ip <= 1'b0;
               end
               5'h1b: begin
                  gateways_26_ip <= 1'b0;
               end
               5'h1c: begin
                  gateways_27_ip <= 1'b0;
               end
               5'h1d: begin
                  gateways_28_ip <= 1'b0;
               end
               5'h1e: begin
                  gateways_29_ip <= 1'b0;
               end
               5'h1f: begin
                  gateways_30_ip <= 1'b0;
               end
               default: begin
               end
            endcase
         end
         if (mapping_completion_valid) begin
            case (mapping_completion_payload)
               5'h01: begin
                  gateways_0_waitCompletion <= 1'b0;
               end
               5'h02: begin
                  gateways_1_waitCompletion <= 1'b0;
               end
               5'h03: begin
                  gateways_2_waitCompletion <= 1'b0;
               end
               5'h04: begin
                  gateways_3_waitCompletion <= 1'b0;
               end
               5'h05: begin
                  gateways_4_waitCompletion <= 1'b0;
               end
               5'h06: begin
                  gateways_5_waitCompletion <= 1'b0;
               end
               5'h07: begin
                  gateways_6_waitCompletion <= 1'b0;
               end
               5'h08: begin
                  gateways_7_waitCompletion <= 1'b0;
               end
               5'h09: begin
                  gateways_8_waitCompletion <= 1'b0;
               end
               5'h0a: begin
                  gateways_9_waitCompletion <= 1'b0;
               end
               5'h0b: begin
                  gateways_10_waitCompletion <= 1'b0;
               end
               5'h0c: begin
                  gateways_11_waitCompletion <= 1'b0;
               end
               5'h0d: begin
                  gateways_12_waitCompletion <= 1'b0;
               end
               5'h0e: begin
                  gateways_13_waitCompletion <= 1'b0;
               end
               5'h0f: begin
                  gateways_14_waitCompletion <= 1'b0;
               end
               5'h10: begin
                  gateways_15_waitCompletion <= 1'b0;
               end
               5'h11: begin
                  gateways_16_waitCompletion <= 1'b0;
               end
               5'h12: begin
                  gateways_17_waitCompletion <= 1'b0;
               end
               5'h13: begin
                  gateways_18_waitCompletion <= 1'b0;
               end
               5'h14: begin
                  gateways_19_waitCompletion <= 1'b0;
               end
               5'h15: begin
                  gateways_20_waitCompletion <= 1'b0;
               end
               5'h16: begin
                  gateways_21_waitCompletion <= 1'b0;
               end
               5'h17: begin
                  gateways_22_waitCompletion <= 1'b0;
               end
               5'h18: begin
                  gateways_23_waitCompletion <= 1'b0;
               end
               5'h19: begin
                  gateways_24_waitCompletion <= 1'b0;
               end
               5'h1a: begin
                  gateways_25_waitCompletion <= 1'b0;
               end
               5'h1b: begin
                  gateways_26_waitCompletion <= 1'b0;
               end
               5'h1c: begin
                  gateways_27_waitCompletion <= 1'b0;
               end
               5'h1d: begin
                  gateways_28_waitCompletion <= 1'b0;
               end
               5'h1e: begin
                  gateways_29_waitCompletion <= 1'b0;
               end
               5'h1f: begin
                  gateways_30_waitCompletion <= 1'b0;
               end
               default: begin
               end
            endcase
         end
         mapping_coherencyStall_value <= mapping_coherencyStall_valueNext;
         case (bus_writeAddressMasked)
            22'h000004: begin
               if (bus_writeOccur) begin
                  _zz_gateways_0_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000008: begin
               if (bus_writeOccur) begin
                  _zz_gateways_1_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00000c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_2_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000010: begin
               if (bus_writeOccur) begin
                  _zz_gateways_3_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000014: begin
               if (bus_writeOccur) begin
                  _zz_gateways_4_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000018: begin
               if (bus_writeOccur) begin
                  _zz_gateways_5_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00001c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_6_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000020: begin
               if (bus_writeOccur) begin
                  _zz_gateways_7_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000024: begin
               if (bus_writeOccur) begin
                  _zz_gateways_8_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000028: begin
               if (bus_writeOccur) begin
                  _zz_gateways_9_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00002c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_10_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000030: begin
               if (bus_writeOccur) begin
                  _zz_gateways_11_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000034: begin
               if (bus_writeOccur) begin
                  _zz_gateways_12_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000038: begin
               if (bus_writeOccur) begin
                  _zz_gateways_13_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00003c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_14_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000040: begin
               if (bus_writeOccur) begin
                  _zz_gateways_15_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000044: begin
               if (bus_writeOccur) begin
                  _zz_gateways_16_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000048: begin
               if (bus_writeOccur) begin
                  _zz_gateways_17_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00004c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_18_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000050: begin
               if (bus_writeOccur) begin
                  _zz_gateways_19_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000054: begin
               if (bus_writeOccur) begin
                  _zz_gateways_20_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000058: begin
               if (bus_writeOccur) begin
                  _zz_gateways_21_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00005c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_22_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000060: begin
               if (bus_writeOccur) begin
                  _zz_gateways_23_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000064: begin
               if (bus_writeOccur) begin
                  _zz_gateways_24_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000068: begin
               if (bus_writeOccur) begin
                  _zz_gateways_25_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00006c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_26_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000070: begin
               if (bus_writeOccur) begin
                  _zz_gateways_27_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000074: begin
               if (bus_writeOccur) begin
                  _zz_gateways_28_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h000078: begin
               if (bus_writeOccur) begin
                  _zz_gateways_29_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h00007c: begin
               if (bus_writeOccur) begin
                  _zz_gateways_30_priority <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h200000: begin
               if (bus_writeOccur) begin
                  _zz_targets_0_threshold <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h002000: begin
               if (bus_writeOccur) begin
                  _zz_targets_0_ie_0  <= io_bus_w_payload_data[1];
                  _zz_targets_0_ie_1  <= io_bus_w_payload_data[2];
                  _zz_targets_0_ie_2  <= io_bus_w_payload_data[3];
                  _zz_targets_0_ie_3  <= io_bus_w_payload_data[4];
                  _zz_targets_0_ie_4  <= io_bus_w_payload_data[5];
                  _zz_targets_0_ie_5  <= io_bus_w_payload_data[6];
                  _zz_targets_0_ie_6  <= io_bus_w_payload_data[7];
                  _zz_targets_0_ie_7  <= io_bus_w_payload_data[8];
                  _zz_targets_0_ie_8  <= io_bus_w_payload_data[9];
                  _zz_targets_0_ie_9  <= io_bus_w_payload_data[10];
                  _zz_targets_0_ie_10 <= io_bus_w_payload_data[11];
                  _zz_targets_0_ie_11 <= io_bus_w_payload_data[12];
                  _zz_targets_0_ie_12 <= io_bus_w_payload_data[13];
                  _zz_targets_0_ie_13 <= io_bus_w_payload_data[14];
                  _zz_targets_0_ie_14 <= io_bus_w_payload_data[15];
                  _zz_targets_0_ie_15 <= io_bus_w_payload_data[16];
                  _zz_targets_0_ie_16 <= io_bus_w_payload_data[17];
                  _zz_targets_0_ie_17 <= io_bus_w_payload_data[18];
                  _zz_targets_0_ie_18 <= io_bus_w_payload_data[19];
                  _zz_targets_0_ie_19 <= io_bus_w_payload_data[20];
                  _zz_targets_0_ie_20 <= io_bus_w_payload_data[21];
                  _zz_targets_0_ie_21 <= io_bus_w_payload_data[22];
                  _zz_targets_0_ie_22 <= io_bus_w_payload_data[23];
                  _zz_targets_0_ie_23 <= io_bus_w_payload_data[24];
                  _zz_targets_0_ie_24 <= io_bus_w_payload_data[25];
                  _zz_targets_0_ie_25 <= io_bus_w_payload_data[26];
                  _zz_targets_0_ie_26 <= io_bus_w_payload_data[27];
                  _zz_targets_0_ie_27 <= io_bus_w_payload_data[28];
                  _zz_targets_0_ie_28 <= io_bus_w_payload_data[29];
                  _zz_targets_0_ie_29 <= io_bus_w_payload_data[30];
                  _zz_targets_0_ie_30 <= io_bus_w_payload_data[31];
               end
            end
            22'h201000: begin
               if (bus_writeOccur) begin
                  _zz_targets_1_threshold <= io_bus_w_payload_data[1 : 0];
               end
            end
            22'h002080: begin
               if (bus_writeOccur) begin
                  _zz_targets_1_ie_0  <= io_bus_w_payload_data[1];
                  _zz_targets_1_ie_1  <= io_bus_w_payload_data[2];
                  _zz_targets_1_ie_2  <= io_bus_w_payload_data[3];
                  _zz_targets_1_ie_3  <= io_bus_w_payload_data[4];
                  _zz_targets_1_ie_4  <= io_bus_w_payload_data[5];
                  _zz_targets_1_ie_5  <= io_bus_w_payload_data[6];
                  _zz_targets_1_ie_6  <= io_bus_w_payload_data[7];
                  _zz_targets_1_ie_7  <= io_bus_w_payload_data[8];
                  _zz_targets_1_ie_8  <= io_bus_w_payload_data[9];
                  _zz_targets_1_ie_9  <= io_bus_w_payload_data[10];
                  _zz_targets_1_ie_10 <= io_bus_w_payload_data[11];
                  _zz_targets_1_ie_11 <= io_bus_w_payload_data[12];
                  _zz_targets_1_ie_12 <= io_bus_w_payload_data[13];
                  _zz_targets_1_ie_13 <= io_bus_w_payload_data[14];
                  _zz_targets_1_ie_14 <= io_bus_w_payload_data[15];
                  _zz_targets_1_ie_15 <= io_bus_w_payload_data[16];
                  _zz_targets_1_ie_16 <= io_bus_w_payload_data[17];
                  _zz_targets_1_ie_17 <= io_bus_w_payload_data[18];
                  _zz_targets_1_ie_18 <= io_bus_w_payload_data[19];
                  _zz_targets_1_ie_19 <= io_bus_w_payload_data[20];
                  _zz_targets_1_ie_20 <= io_bus_w_payload_data[21];
                  _zz_targets_1_ie_21 <= io_bus_w_payload_data[22];
                  _zz_targets_1_ie_22 <= io_bus_w_payload_data[23];
                  _zz_targets_1_ie_23 <= io_bus_w_payload_data[24];
                  _zz_targets_1_ie_24 <= io_bus_w_payload_data[25];
                  _zz_targets_1_ie_25 <= io_bus_w_payload_data[26];
                  _zz_targets_1_ie_26 <= io_bus_w_payload_data[27];
                  _zz_targets_1_ie_27 <= io_bus_w_payload_data[28];
                  _zz_targets_1_ie_28 <= io_bus_w_payload_data[29];
                  _zz_targets_1_ie_29 <= io_bus_w_payload_data[30];
                  _zz_targets_1_ie_30 <= io_bus_w_payload_data[31];
               end
            end
            default: begin
            end
         endcase
      end
   end

   always @(posedge clk) begin
      targets_0_bestRequest_priority <= (_zz_targets_0_bestRequest_priority_6 ? _zz_targets_0_bestRequest_priority_4 : _zz_targets_0_bestRequest_priority_5);
      targets_0_bestRequest_id <= (_zz_targets_0_bestRequest_priority_6 ? (_zz_targets_0_bestRequest_id_80 ? (_zz_targets_0_bestRequest_id_72 ? (_zz_targets_0_bestRequest_id_48 ? _zz_targets_0_bestRequest_id_82 : _zz_targets_0_bestRequest_id_83) : (_zz_targets_0_bestRequest_id_51 ? _zz_targets_0_bestRequest_id_84 : _zz_targets_0_bestRequest_id_85)) : (_zz_targets_0_bestRequest_id_74 ? (_zz_targets_0_bestRequest_id_54 ? _zz_targets_0_bestRequest_id_86 : _zz_targets_0_bestRequest_id_87) : (_zz_targets_0_bestRequest_id_57 ? _zz_targets_0_bestRequest_id_88 : _zz_targets_0_bestRequest_id_89))) : (_zz_targets_0_bestRequest_id_81 ? (_zz_targets_0_bestRequest_id_76 ? (_zz_targets_0_bestRequest_id_60 ? _zz_targets_0_bestRequest_id_90 : _zz_targets_0_bestRequest_id_91) : (_zz_targets_0_bestRequest_id_63 ? _zz_targets_0_bestRequest_id_92 : _zz_targets_0_bestRequest_id_93)) : (_zz_targets_0_bestRequest_id_78 ? (_zz_targets_0_bestRequest_id_66 ? _zz_targets_0_bestRequest_id_94 : _zz_targets_0_bestRequest_id_95) : (_zz_targets_0_bestRequest_id_69 ? _zz_targets_0_bestRequest_id_96 : _zz_targets_0_bestRequest_id_97))));
      targets_0_bestRequest_valid <= (_zz_targets_0_bestRequest_priority_6 ? _zz_targets_0_bestRequest_valid : _zz_targets_0_bestRequest_valid_1);
      targets_1_bestRequest_priority <= (_zz_targets_1_bestRequest_priority_6 ? _zz_targets_1_bestRequest_priority_4 : _zz_targets_1_bestRequest_priority_5);
      targets_1_bestRequest_id <= (_zz_targets_1_bestRequest_priority_6 ? (_zz_targets_1_bestRequest_id_80 ? (_zz_targets_1_bestRequest_id_72 ? (_zz_targets_1_bestRequest_id_48 ? _zz_targets_1_bestRequest_id_82 : _zz_targets_1_bestRequest_id_83) : (_zz_targets_1_bestRequest_id_51 ? _zz_targets_1_bestRequest_id_84 : _zz_targets_1_bestRequest_id_85)) : (_zz_targets_1_bestRequest_id_74 ? (_zz_targets_1_bestRequest_id_54 ? _zz_targets_1_bestRequest_id_86 : _zz_targets_1_bestRequest_id_87) : (_zz_targets_1_bestRequest_id_57 ? _zz_targets_1_bestRequest_id_88 : _zz_targets_1_bestRequest_id_89))) : (_zz_targets_1_bestRequest_id_81 ? (_zz_targets_1_bestRequest_id_76 ? (_zz_targets_1_bestRequest_id_60 ? _zz_targets_1_bestRequest_id_90 : _zz_targets_1_bestRequest_id_91) : (_zz_targets_1_bestRequest_id_63 ? _zz_targets_1_bestRequest_id_92 : _zz_targets_1_bestRequest_id_93)) : (_zz_targets_1_bestRequest_id_78 ? (_zz_targets_1_bestRequest_id_66 ? _zz_targets_1_bestRequest_id_94 : _zz_targets_1_bestRequest_id_95) : (_zz_targets_1_bestRequest_id_69 ? _zz_targets_1_bestRequest_id_96 : _zz_targets_1_bestRequest_id_97))));
      targets_1_bestRequest_valid <= (_zz_targets_1_bestRequest_priority_6 ? _zz_targets_1_bestRequest_valid : _zz_targets_1_bestRequest_valid_1);
      if (_zz_bus_writeJoinEvent_translated_ready_1) begin
         _zz_io_bus_b_payload_resp <= bus_writeJoinEvent_translated_payload_resp;
      end
      if (io_bus_ar_ready) begin
         io_bus_ar_rData_addr <= io_bus_ar_payload_addr;
         io_bus_ar_rData_prot <= io_bus_ar_payload_prot;
      end
   end


endmodule

module AxiLite4Clint (
   input             io_bus_aw_valid,
   output            io_bus_aw_ready,
   input      [15:0] io_bus_aw_payload_addr,
   input      [ 2:0] io_bus_aw_payload_prot,
   input             io_bus_w_valid,
   output            io_bus_w_ready,
   input      [31:0] io_bus_w_payload_data,
   input      [ 3:0] io_bus_w_payload_strb,
   output            io_bus_b_valid,
   input             io_bus_b_ready,
   output     [ 1:0] io_bus_b_payload_resp,
   input             io_bus_ar_valid,
   output reg        io_bus_ar_ready,
   input      [15:0] io_bus_ar_payload_addr,
   input      [ 2:0] io_bus_ar_payload_prot,
   output            io_bus_r_valid,
   input             io_bus_r_ready,
   output     [31:0] io_bus_r_payload_data,
   output     [ 1:0] io_bus_r_payload_resp,
   output     [ 0:0] io_timerInterrupt,
   output     [ 0:0] io_softwareInterrupt,
   output     [63:0] io_time,
   input             clk,
   input             reset
);

   wire [31:0] _zz_logic_harts_0_cmp;
   wire [31:0] _zz_logic_harts_0_cmp_1;
   wire [31:0] _zz_logic_harts_0_cmp_2;
   wire [31:0] _zz_logic_harts_0_cmp_3;
   wire        factory_readErrorFlag;
   wire        factory_writeErrorFlag;
   wire        factory_readHaltRequest;
   wire        factory_writeHaltRequest;
   wire        factory_writeJoinEvent_valid;
   wire        factory_writeJoinEvent_ready;
   wire        factory_writeOccur;
   reg  [ 1:0] factory_writeRsp_resp;
   wire        factory_writeJoinEvent_translated_valid;
   wire        factory_writeJoinEvent_translated_ready;
   wire [ 1:0] factory_writeJoinEvent_translated_payload_resp;
   wire        _zz_factory_writeJoinEvent_translated_ready;
   reg         _zz_factory_writeJoinEvent_translated_ready_1;
   wire        _zz_io_bus_b_valid;
   reg         _zz_io_bus_b_valid_1;
   reg  [ 1:0] _zz_io_bus_b_payload_resp;
   wire        when_Stream_l369;
   wire        factory_readDataStage_valid;
   wire        factory_readDataStage_ready;
   wire [15:0] factory_readDataStage_payload_addr;
   wire [ 2:0] factory_readDataStage_payload_prot;
   reg         io_bus_ar_rValid;
   reg  [15:0] io_bus_ar_rData_addr;
   reg  [ 2:0] io_bus_ar_rData_prot;
   wire        when_Stream_l369_1;
   reg  [31:0] factory_readRsp_data;
   reg  [ 1:0] factory_readRsp_resp;
   wire        _zz_io_bus_r_valid;
   wire [15:0] factory_readAddressMasked;
   wire [15:0] factory_writeAddressMasked;
   wire        factory_readOccur;
   wire        logic_stop;
   reg  [63:0] logic_time;
   wire        when_Clint_l36;
   reg  [63:0] logic_harts_0_cmp;
   reg         logic_harts_0_timerInterrupt;
   reg         logic_harts_0_softwareInterrupt;
   wire [63:0] _zz_factory_readRsp_data;
   wire        when_AxiLite4SlaveFactory_l68;
   wire        when_AxiLite4SlaveFactory_l68_1;
   wire        when_AxiLite4SlaveFactory_l86;
   wire        when_AxiLite4SlaveFactory_l86_1;

   assign _zz_logic_harts_0_cmp_1 = io_bus_w_payload_data[31 : 0];
   assign _zz_logic_harts_0_cmp = _zz_logic_harts_0_cmp_1;
   assign _zz_logic_harts_0_cmp_3 = io_bus_w_payload_data[31 : 0];
   assign _zz_logic_harts_0_cmp_2 = _zz_logic_harts_0_cmp_3;
   assign factory_readErrorFlag = 1'b0;
   assign factory_writeErrorFlag = 1'b0;
   assign factory_readHaltRequest = 1'b0;
   assign factory_writeHaltRequest = 1'b0;
   assign factory_writeOccur = (factory_writeJoinEvent_valid && factory_writeJoinEvent_ready);
   assign factory_writeJoinEvent_valid = (io_bus_aw_valid && io_bus_w_valid);
   assign io_bus_aw_ready = factory_writeOccur;
   assign io_bus_w_ready = factory_writeOccur;
   assign factory_writeJoinEvent_translated_valid = factory_writeJoinEvent_valid;
   assign factory_writeJoinEvent_ready = factory_writeJoinEvent_translated_ready;
   assign factory_writeJoinEvent_translated_payload_resp = factory_writeRsp_resp;
   assign _zz_factory_writeJoinEvent_translated_ready = (!factory_writeHaltRequest);
   assign factory_writeJoinEvent_translated_ready = (_zz_factory_writeJoinEvent_translated_ready_1 && _zz_factory_writeJoinEvent_translated_ready);
   always @(*) begin
      _zz_factory_writeJoinEvent_translated_ready_1 = io_bus_b_ready;
      if (when_Stream_l369) begin
         _zz_factory_writeJoinEvent_translated_ready_1 = 1'b1;
      end
   end

   assign when_Stream_l369      = (!_zz_io_bus_b_valid);
   assign _zz_io_bus_b_valid    = _zz_io_bus_b_valid_1;
   assign io_bus_b_valid        = _zz_io_bus_b_valid;
   assign io_bus_b_payload_resp = _zz_io_bus_b_payload_resp;
   always @(*) begin
      io_bus_ar_ready = factory_readDataStage_ready;
      if (when_Stream_l369_1) begin
         io_bus_ar_ready = 1'b1;
      end
   end

   assign when_Stream_l369_1                 = (!factory_readDataStage_valid);
   assign factory_readDataStage_valid        = io_bus_ar_rValid;
   assign factory_readDataStage_payload_addr = io_bus_ar_rData_addr;
   assign factory_readDataStage_payload_prot = io_bus_ar_rData_prot;
   assign _zz_io_bus_r_valid                 = (!factory_readHaltRequest);
   assign factory_readDataStage_ready        = (io_bus_r_ready && _zz_io_bus_r_valid);
   assign io_bus_r_valid                     = (factory_readDataStage_valid && _zz_io_bus_r_valid);
   assign io_bus_r_payload_data              = factory_readRsp_data;
   assign io_bus_r_payload_resp              = factory_readRsp_resp;
   always @(*) begin
      if (factory_writeErrorFlag) begin
         factory_writeRsp_resp = 2'b10;
      end else begin
         factory_writeRsp_resp = 2'b00;
      end
   end

   always @(*) begin
      if (factory_readErrorFlag) begin
         factory_readRsp_resp = 2'b10;
      end else begin
         factory_readRsp_resp = 2'b00;
      end
   end

   always @(*) begin
      factory_readRsp_data = 32'h00000000;
      case (factory_readAddressMasked)
         16'h0000: begin
            factory_readRsp_data[0 : 0] = logic_harts_0_softwareInterrupt;
         end
         default: begin
         end
      endcase
      if (when_AxiLite4SlaveFactory_l86) begin
         factory_readRsp_data[31 : 0] = _zz_factory_readRsp_data[31 : 0];
      end
      if (when_AxiLite4SlaveFactory_l86_1) begin
         factory_readRsp_data[31 : 0] = _zz_factory_readRsp_data[63 : 32];
      end
   end

   assign factory_readAddressMasked = (factory_readDataStage_payload_addr & (~16'h0003));
   assign factory_writeAddressMasked = (io_bus_aw_payload_addr & (~16'h0003));
   assign factory_readOccur = (io_bus_r_valid && io_bus_r_ready);
   assign logic_stop = 1'b0;
   assign when_Clint_l36 = (!logic_stop);
   assign _zz_factory_readRsp_data = logic_time;
   assign io_timerInterrupt[0] = logic_harts_0_timerInterrupt;
   assign io_softwareInterrupt[0] = logic_harts_0_softwareInterrupt;
   assign io_time = logic_time;
   assign when_AxiLite4SlaveFactory_l68 = ((factory_writeAddressMasked & (~16'h0003)) == 16'h4000);
   assign when_AxiLite4SlaveFactory_l68_1 = ((factory_writeAddressMasked & (~ 16'h0003)) == 16'h4004);
   assign when_AxiLite4SlaveFactory_l86 = ((factory_readAddressMasked & (~16'h0003)) == 16'hbff8);
   assign when_AxiLite4SlaveFactory_l86_1 = ((factory_readAddressMasked & (~16'h0003)) == 16'hbffc);
   always @(posedge clk or posedge reset) begin
      if (reset) begin
         _zz_io_bus_b_valid_1            <= 1'b0;
         io_bus_ar_rValid                <= 1'b0;
         logic_time                      <= 64'h0000000000000000;
         logic_harts_0_softwareInterrupt <= 1'b0;
      end else begin
         if (_zz_factory_writeJoinEvent_translated_ready_1) begin
            _zz_io_bus_b_valid_1 <= (factory_writeJoinEvent_translated_valid && _zz_factory_writeJoinEvent_translated_ready);
         end
         if (io_bus_ar_ready) begin
            io_bus_ar_rValid <= io_bus_ar_valid;
         end
         if (when_Clint_l36) begin
            logic_time <= (logic_time + 64'h0000000000000001);
         end
         case (factory_writeAddressMasked)
            16'h0000: begin
               if (factory_writeOccur) begin
                  logic_harts_0_softwareInterrupt <= io_bus_w_payload_data[0];
               end
            end
            default: begin
            end
         endcase
      end
   end

   always @(posedge clk) begin
      if (_zz_factory_writeJoinEvent_translated_ready_1) begin
         _zz_io_bus_b_payload_resp <= factory_writeJoinEvent_translated_payload_resp;
      end
      if (io_bus_ar_ready) begin
         io_bus_ar_rData_addr <= io_bus_ar_payload_addr;
         io_bus_ar_rData_prot <= io_bus_ar_payload_prot;
      end
      logic_harts_0_timerInterrupt <= (logic_harts_0_cmp <= logic_time);
      if (when_AxiLite4SlaveFactory_l68) begin
         if (factory_writeOccur) begin
            logic_harts_0_cmp[31 : 0] <= _zz_logic_harts_0_cmp;
         end
      end
      if (when_AxiLite4SlaveFactory_l68_1) begin
         if (factory_writeOccur) begin
            logic_harts_0_cmp[63 : 32] <= _zz_logic_harts_0_cmp_2;
         end
      end
   end


endmodule
