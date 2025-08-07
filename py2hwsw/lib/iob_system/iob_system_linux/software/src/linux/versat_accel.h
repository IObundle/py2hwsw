/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

// This file has been auto-generated

#ifndef INCLUDED_VERSAT_ACCELERATOR_HEADER
#define INCLUDED_VERSAT_ACCELERATOR_HEADER

#ifdef __cplusplus
#include <cstdint>
#else
#include "stdbool.h"
#include "stdint.h"
#endif

typedef intptr_t iptr;

// Config

#define VERSAT_DEFINED_RegFile
typedef struct {
  iptr selectedInput;
  iptr selectedOutput0;
  iptr selectedOutput1;
  iptr disabled;
} RegFileConfig;

#define VERSAT_DEFINED_Reg
typedef struct {
  iptr disabled;
} RegConfig;

#define VERSAT_DEFINED_Mux2
typedef struct {
  iptr sel;
} Mux2Config;

#define VERSAT_DEFINED_Const
typedef struct {
  iptr constant;
} ConstConfig;

#define VERSAT_DEFINED_CombMux8
typedef struct {
  iptr sel;
} CombMux8Config;

#define VERSAT_DEFINED_Buffer
typedef struct {
  iptr amount;
} BufferConfig;

#define VERSAT_DEFINED_VRead
typedef struct {
  iptr ext_addr;
  iptr perA;
  iptr incrA;
  iptr length;
  iptr pingPong;
  iptr iterB;
  iptr perB;
  iptr dutyB;
  iptr startB;
  iptr shiftB;
  iptr incrB;
  iptr reverseB;
  iptr extB;
  iptr iter2B;
  iptr per2B;
  iptr shift2B;
  iptr incr2B;
  iptr enableRead;
} VReadConfig;

#define VERSAT_DEFINED_SwapEndian
typedef struct {
  iptr enabled;
} SwapEndianConfig;

#define VERSAT_DEFINED_OnlyOutputMem
typedef struct {
  iptr disabled;
  iptr iterA;
  iptr perA;
  iptr dutyA;
  iptr startA;
  iptr shiftA;
  iptr incrA;
  iptr reverseA;
  iptr extA;
  iptr iter2A;
  iptr per2A;
  iptr shift2A;
  iptr incr2A;
} OnlyOutputMemConfig;

#define VERSAT_DEFINED_ShaSingleState
typedef struct {
  RegConfig reg;
} ShaSingleStateConfig;

#define VERSAT_DEFINED_ReadWriteMem
typedef struct {
  iptr disabled;
  iptr iterA;
  iptr perA;
  iptr dutyA;
  iptr startA;
  iptr shiftA;
  iptr incrA;
  iptr reverseA;
  iptr extA;
  iptr in0_wr;
  iptr iterB;
  iptr perB;
  iptr dutyB;
  iptr startB;
  iptr shiftB;
  iptr incrB;
  iptr reverseB;
} ReadWriteMemConfig;

#define VERSAT_DEFINED_VWrite
typedef struct {
  iptr ext_addr;
  iptr perA;
  iptr incrA;
  iptr length;
  iptr pingPong;
  iptr iterB;
  iptr perB;
  iptr dutyB;
  iptr startB;
  iptr shiftB;
  iptr incrB;
  iptr reverseB;
  iptr extB;
  iptr iter2B;
  iptr per2B;
  iptr shift2B;
  iptr incr2B;
  iptr enableWrite;
} VWriteConfig;

#define VERSAT_DEFINED_GenericLineKey
typedef struct {
  Mux2Config mux_0;
  Mux2Config mux_1;
  Mux2Config mux_2;
  Mux2Config mux_3;
} GenericLineKeyConfig;

#define VERSAT_DEFINED_AESFirstAdd
typedef struct {
  CombMux8Config versat_merge_mux_0;
} AESFirstAddConfig;

#define VERSAT_DEFINED_AESRound
typedef struct {
  CombMux8Config versat_merge_mux_0;
} AESRoundConfig;

#define VERSAT_DEFINED_AESLastRound
typedef struct {
  CombMux8Config versat_merge_mux_0;
} AESLastRoundConfig;

#define VERSAT_DEFINED_AESInvFirstAdd
typedef struct {
  CombMux8Config versat_merge_mux_0;
} AESInvFirstAddConfig;

#define VERSAT_DEFINED_AESInvRound
typedef struct {
  CombMux8Config versat_merge_mux_0;
} AESInvRoundConfig;

#define VERSAT_DEFINED_AESInvLastRound
typedef struct {
  CombMux8Config versat_merge_mux_0;
} AESInvLastRoundConfig;

#define VERSAT_DEFINED_FullAESRounds
typedef struct {
  union {
    AESFirstAddConfig AESFirstAdd;
    AESRoundConfig AESRound;
    AESLastRoundConfig AESLastRound;
    AESInvFirstAddConfig AESInvFirstAdd;
    AESInvRoundConfig AESInvRound;
    AESInvLastRoundConfig AESInvLastRound;
  };
} FullAESRoundsConfig;

#define VERSAT_DEFINED_ShaState
typedef struct {
  ShaSingleStateConfig s_0;
  ShaSingleStateConfig s_1;
  ShaSingleStateConfig s_2;
  ShaSingleStateConfig s_3;
  ShaSingleStateConfig s_4;
  ShaSingleStateConfig s_5;
  ShaSingleStateConfig s_6;
  ShaSingleStateConfig s_7;
} ShaStateConfig;

#define VERSAT_DEFINED_McEliece
typedef struct {
  ReadWriteMemConfig mat;
  VReadConfig row;
  VWriteConfig writer;
  ConstConfig mask;
} McElieceConfig;

#define VERSAT_DEFINED_GenericKeySchedule256
typedef struct {
  GenericLineKeyConfig s;
} GenericKeySchedule256Config;

#define VERSAT_DEFINED_SHA
typedef struct {
  VReadConfig MemRead;
  SwapEndianConfig Swap;
  ShaStateConfig State;
} SHAConfig;

#define VERSAT_DEFINED_FullAES
typedef struct {
  union {
    RegFileConfig key_0;
    RegFileConfig key_1;
    RegFileConfig key_2;
    RegFileConfig key_3;
    RegFileConfig key_4;
    RegFileConfig key_5;
    RegFileConfig key_6;
    RegFileConfig key_7;
    RegFileConfig key_8;
    RegFileConfig key_9;
    RegFileConfig key_10;
    RegFileConfig key_11;
    RegFileConfig key_12;
    RegFileConfig key_13;
    RegFileConfig key_14;
    RegFileConfig key_15;
  };
  union {
    RegConfig state_0;
    RegConfig state_1;
    RegConfig state_2;
    RegConfig state_3;
    RegConfig state_4;
    RegConfig state_5;
    RegConfig state_6;
    RegConfig state_7;
    RegConfig state_8;
    RegConfig state_9;
    RegConfig state_10;
    RegConfig state_11;
    RegConfig state_12;
    RegConfig state_13;
    RegConfig state_14;
    RegConfig state_15;
  };
  union {
    RegConfig lastResult_0;
    RegConfig lastResult_1;
    RegConfig lastResult_2;
    RegConfig lastResult_3;
    RegConfig lastResult_4;
    RegConfig lastResult_5;
    RegConfig lastResult_6;
    RegConfig lastResult_7;
    RegConfig lastResult_8;
    RegConfig lastResult_9;
    RegConfig lastResult_10;
    RegConfig lastResult_11;
    RegConfig lastResult_12;
    RegConfig lastResult_13;
    RegConfig lastResult_14;
    RegConfig lastResult_15;
  };
  union {
    RegConfig lastValToAdd_0;
    RegConfig lastValToAdd_1;
    RegConfig lastValToAdd_2;
    RegConfig lastValToAdd_3;
    RegConfig lastValToAdd_4;
    RegConfig lastValToAdd_5;
    RegConfig lastValToAdd_6;
    RegConfig lastValToAdd_7;
    RegConfig lastValToAdd_8;
    RegConfig lastValToAdd_9;
    RegConfig lastValToAdd_10;
    RegConfig lastValToAdd_11;
    RegConfig lastValToAdd_12;
    RegConfig lastValToAdd_13;
    RegConfig lastValToAdd_14;
    RegConfig lastValToAdd_15;
  };
  GenericKeySchedule256Config schedule;
  ConstConfig rcon;
  FullAESRoundsConfig round;
} FullAESConfig;

#define VERSAT_DEFINED_CryptoAlgos
typedef struct {
  FullAESConfig aes;
  SHAConfig sha;
  McElieceConfig eliece;
} CryptoAlgosConfig;

// Address

#define VERSAT_DEFINED_RegFileAddr
typedef struct {
  void *addr;
} RegFileAddr;

#define VERSAT_DEFINED_RegAddr
typedef struct {
  void *addr;
} RegAddr;

#define VERSAT_DEFINED_LookupTableAddr
typedef struct {
  void *addr;
} LookupTableAddr;

#define VERSAT_DEFINED_DoRowAddr
typedef struct {
  LookupTableAddr mul2_0;
  LookupTableAddr mul2_1;
  LookupTableAddr mul3_0;
  LookupTableAddr mul3_1;
} DoRowAddr;

#define VERSAT_DEFINED_InvDoRowAddr
typedef struct {
  LookupTableAddr mul9_0;
  LookupTableAddr mul9_1;
  LookupTableAddr mul11_0;
  LookupTableAddr mul11_1;
  LookupTableAddr mul13_0;
  LookupTableAddr mul13_1;
  LookupTableAddr mul14_0;
  LookupTableAddr mul14_1;
} InvDoRowAddr;

#define VERSAT_DEFINED_OnlyOutputMemAddr
typedef struct {
  void *addr;
} OnlyOutputMemAddr;

#define VERSAT_DEFINED_ShaSingleStateAddr
typedef struct {
  RegAddr reg;
} ShaSingleStateAddr;

#define VERSAT_DEFINED_ReadWriteMemAddr
typedef struct {
  void *addr;
} ReadWriteMemAddr;

#define VERSAT_DEFINED_GenericLineKeyAddr
typedef struct {
  LookupTableAddr b_0;
  LookupTableAddr b_1;
} GenericLineKeyAddr;

#define VERSAT_DEFINED_MixColumnsAddr
typedef struct {
  DoRowAddr d_0;
  DoRowAddr d_1;
  DoRowAddr d_2;
  DoRowAddr d_3;
} MixColumnsAddr;

#define VERSAT_DEFINED_InvMixColumnsAddr
typedef struct {
  InvDoRowAddr d_0;
  InvDoRowAddr d_1;
  InvDoRowAddr d_2;
  InvDoRowAddr d_3;
} InvMixColumnsAddr;

#define VERSAT_DEFINED_ConstantsAddr
typedef struct {
  OnlyOutputMemAddr mem;
} ConstantsAddr;

#define VERSAT_DEFINED_ShaStateAddr
typedef struct {
  ShaSingleStateAddr s_0;
  ShaSingleStateAddr s_1;
  ShaSingleStateAddr s_2;
  ShaSingleStateAddr s_3;
  ShaSingleStateAddr s_4;
  ShaSingleStateAddr s_5;
  ShaSingleStateAddr s_6;
  ShaSingleStateAddr s_7;
} ShaStateAddr;

#define VERSAT_DEFINED_McElieceAddr
typedef struct {
  ReadWriteMemAddr mat;
} McElieceAddr;

#define VERSAT_DEFINED_GenericKeySchedule256Addr
typedef struct {
  GenericLineKeyAddr s;
} GenericKeySchedule256Addr;

#define VERSAT_DEFINED_FullAESRoundsAddr
typedef struct {
  MixColumnsAddr mixColumns;
  InvMixColumnsAddr invMixColumns;
} FullAESRoundsAddr;

#define VERSAT_DEFINED_SHAAddr
typedef struct {
  ConstantsAddr cMem0;
  ConstantsAddr cMem1;
  ConstantsAddr cMem2;
  ConstantsAddr cMem3;
  ShaStateAddr State;
} SHAAddr;

#define VERSAT_DEFINED_FullAESAddr
typedef struct {
  RegFileAddr key_0;
  RegFileAddr key_1;
  RegFileAddr key_2;
  RegFileAddr key_3;
  RegFileAddr key_4;
  RegFileAddr key_5;
  RegFileAddr key_6;
  RegFileAddr key_7;
  RegFileAddr key_8;
  RegFileAddr key_9;
  RegFileAddr key_10;
  RegFileAddr key_11;
  RegFileAddr key_12;
  RegFileAddr key_13;
  RegFileAddr key_14;
  RegFileAddr key_15;
  RegAddr state_0;
  RegAddr state_1;
  RegAddr state_2;
  RegAddr state_3;
  RegAddr state_4;
  RegAddr state_5;
  RegAddr state_6;
  RegAddr state_7;
  RegAddr state_8;
  RegAddr state_9;
  RegAddr state_10;
  RegAddr state_11;
  RegAddr state_12;
  RegAddr state_13;
  RegAddr state_14;
  RegAddr state_15;
  RegAddr lastResult_0;
  RegAddr lastResult_1;
  RegAddr lastResult_2;
  RegAddr lastResult_3;
  RegAddr lastResult_4;
  RegAddr lastResult_5;
  RegAddr lastResult_6;
  RegAddr lastResult_7;
  RegAddr lastResult_8;
  RegAddr lastResult_9;
  RegAddr lastResult_10;
  RegAddr lastResult_11;
  RegAddr lastResult_12;
  RegAddr lastResult_13;
  RegAddr lastResult_14;
  RegAddr lastResult_15;
  RegAddr lastValToAdd_0;
  RegAddr lastValToAdd_1;
  RegAddr lastValToAdd_2;
  RegAddr lastValToAdd_3;
  RegAddr lastValToAdd_4;
  RegAddr lastValToAdd_5;
  RegAddr lastValToAdd_6;
  RegAddr lastValToAdd_7;
  RegAddr lastValToAdd_8;
  RegAddr lastValToAdd_9;
  RegAddr lastValToAdd_10;
  RegAddr lastValToAdd_11;
  RegAddr lastValToAdd_12;
  RegAddr lastValToAdd_13;
  RegAddr lastValToAdd_14;
  RegAddr lastValToAdd_15;
  GenericKeySchedule256Addr schedule;
  FullAESRoundsAddr round;
} FullAESAddr;

#define VERSAT_DEFINED_CryptoAlgosAddr
typedef struct {
  FullAESAddr aes;
  SHAAddr sha;
  McElieceAddr eliece;
} CryptoAlgosAddr;

typedef struct {
  union {
    iptr TOP_aes_key_0_selectedInput;
    iptr TOP_aes_key_1_selectedInput;
    iptr TOP_aes_key_2_selectedInput;
    iptr TOP_aes_key_3_selectedInput;
    iptr TOP_aes_key_4_selectedInput;
    iptr TOP_aes_key_5_selectedInput;
    iptr TOP_aes_key_6_selectedInput;
    iptr TOP_aes_key_7_selectedInput;
    iptr TOP_aes_key_8_selectedInput;
    iptr TOP_aes_key_9_selectedInput;
    iptr TOP_aes_key_10_selectedInput;
    iptr TOP_aes_key_11_selectedInput;
    iptr TOP_aes_key_12_selectedInput;
    iptr TOP_aes_key_13_selectedInput;
    iptr TOP_aes_key_14_selectedInput;
    iptr TOP_aes_key_15_selectedInput;
  };
  union {
    iptr TOP_aes_key_0_selectedOutput0;
    iptr TOP_aes_key_1_selectedOutput0;
    iptr TOP_aes_key_2_selectedOutput0;
    iptr TOP_aes_key_3_selectedOutput0;
    iptr TOP_aes_key_4_selectedOutput0;
    iptr TOP_aes_key_5_selectedOutput0;
    iptr TOP_aes_key_6_selectedOutput0;
    iptr TOP_aes_key_7_selectedOutput0;
    iptr TOP_aes_key_8_selectedOutput0;
    iptr TOP_aes_key_9_selectedOutput0;
    iptr TOP_aes_key_10_selectedOutput0;
    iptr TOP_aes_key_11_selectedOutput0;
    iptr TOP_aes_key_12_selectedOutput0;
    iptr TOP_aes_key_13_selectedOutput0;
    iptr TOP_aes_key_14_selectedOutput0;
    iptr TOP_aes_key_15_selectedOutput0;
  };
  union {
    iptr TOP_aes_key_0_selectedOutput1;
    iptr TOP_aes_key_1_selectedOutput1;
    iptr TOP_aes_key_2_selectedOutput1;
    iptr TOP_aes_key_3_selectedOutput1;
    iptr TOP_aes_key_4_selectedOutput1;
    iptr TOP_aes_key_5_selectedOutput1;
    iptr TOP_aes_key_6_selectedOutput1;
    iptr TOP_aes_key_7_selectedOutput1;
    iptr TOP_aes_key_8_selectedOutput1;
    iptr TOP_aes_key_9_selectedOutput1;
    iptr TOP_aes_key_10_selectedOutput1;
    iptr TOP_aes_key_11_selectedOutput1;
    iptr TOP_aes_key_12_selectedOutput1;
    iptr TOP_aes_key_13_selectedOutput1;
    iptr TOP_aes_key_14_selectedOutput1;
    iptr TOP_aes_key_15_selectedOutput1;
  };
  union {
    iptr TOP_aes_key_0_disabled;
    iptr TOP_aes_key_1_disabled;
    iptr TOP_aes_key_2_disabled;
    iptr TOP_aes_key_3_disabled;
    iptr TOP_aes_key_4_disabled;
    iptr TOP_aes_key_5_disabled;
    iptr TOP_aes_key_6_disabled;
    iptr TOP_aes_key_7_disabled;
    iptr TOP_aes_key_8_disabled;
    iptr TOP_aes_key_9_disabled;
    iptr TOP_aes_key_10_disabled;
    iptr TOP_aes_key_11_disabled;
    iptr TOP_aes_key_12_disabled;
    iptr TOP_aes_key_13_disabled;
    iptr TOP_aes_key_14_disabled;
    iptr TOP_aes_key_15_disabled;
  };
  union {
    iptr TOP_aes_state_0_disabled;
    iptr TOP_aes_state_1_disabled;
    iptr TOP_aes_state_2_disabled;
    iptr TOP_aes_state_3_disabled;
    iptr TOP_aes_state_4_disabled;
    iptr TOP_aes_state_5_disabled;
    iptr TOP_aes_state_6_disabled;
    iptr TOP_aes_state_7_disabled;
    iptr TOP_aes_state_8_disabled;
    iptr TOP_aes_state_9_disabled;
    iptr TOP_aes_state_10_disabled;
    iptr TOP_aes_state_11_disabled;
    iptr TOP_aes_state_12_disabled;
    iptr TOP_aes_state_13_disabled;
    iptr TOP_aes_state_14_disabled;
    iptr TOP_aes_state_15_disabled;
  };
  union {
    iptr TOP_aes_lastResult_0_disabled;
    iptr TOP_aes_lastResult_1_disabled;
    iptr TOP_aes_lastResult_2_disabled;
    iptr TOP_aes_lastResult_3_disabled;
    iptr TOP_aes_lastResult_4_disabled;
    iptr TOP_aes_lastResult_5_disabled;
    iptr TOP_aes_lastResult_6_disabled;
    iptr TOP_aes_lastResult_7_disabled;
    iptr TOP_aes_lastResult_8_disabled;
    iptr TOP_aes_lastResult_9_disabled;
    iptr TOP_aes_lastResult_10_disabled;
    iptr TOP_aes_lastResult_11_disabled;
    iptr TOP_aes_lastResult_12_disabled;
    iptr TOP_aes_lastResult_13_disabled;
    iptr TOP_aes_lastResult_14_disabled;
    iptr TOP_aes_lastResult_15_disabled;
  };
  union {
    iptr TOP_aes_lastValToAdd_0_disabled;
    iptr TOP_aes_lastValToAdd_1_disabled;
    iptr TOP_aes_lastValToAdd_2_disabled;
    iptr TOP_aes_lastValToAdd_3_disabled;
    iptr TOP_aes_lastValToAdd_4_disabled;
    iptr TOP_aes_lastValToAdd_5_disabled;
    iptr TOP_aes_lastValToAdd_6_disabled;
    iptr TOP_aes_lastValToAdd_7_disabled;
    iptr TOP_aes_lastValToAdd_8_disabled;
    iptr TOP_aes_lastValToAdd_9_disabled;
    iptr TOP_aes_lastValToAdd_10_disabled;
    iptr TOP_aes_lastValToAdd_11_disabled;
    iptr TOP_aes_lastValToAdd_12_disabled;
    iptr TOP_aes_lastValToAdd_13_disabled;
    iptr TOP_aes_lastValToAdd_14_disabled;
    iptr TOP_aes_lastValToAdd_15_disabled;
  };
  iptr TOP_aes_schedule_s_mux_0_sel;
  iptr TOP_aes_schedule_s_mux_1_sel;
  iptr TOP_aes_schedule_s_mux_2_sel;
  iptr TOP_aes_schedule_s_mux_3_sel;
  iptr TOP_aes_rcon_constant;
  union {
    iptr TOP_aes_round_versat_merge_mux_0_sel;
    iptr TOP_aes_round_versat_merge_mux_1_sel;
    iptr TOP_aes_round_versat_merge_mux_2_sel;
    iptr TOP_aes_round_versat_merge_mux_3_sel;
    iptr TOP_aes_round_versat_merge_mux_4_sel;
    iptr TOP_aes_round_versat_merge_mux_5_sel;
    iptr TOP_aes_round_versat_merge_mux_6_sel;
    iptr TOP_aes_round_versat_merge_mux_7_sel;
    iptr TOP_aes_round_versat_merge_mux_8_sel;
    iptr TOP_aes_round_versat_merge_mux_9_sel;
    iptr TOP_aes_round_versat_merge_mux_10_sel;
    iptr TOP_aes_round_versat_merge_mux_11_sel;
    iptr TOP_aes_round_versat_merge_mux_12_sel;
    iptr TOP_aes_round_versat_merge_mux_13_sel;
    iptr TOP_aes_round_versat_merge_mux_14_sel;
    iptr TOP_aes_round_versat_merge_mux_15_sel;
    iptr TOP_aes_round_versat_merge_mux_16_sel;
    iptr TOP_aes_round_versat_merge_mux_17_sel;
    iptr TOP_aes_round_versat_merge_mux_18_sel;
    iptr TOP_aes_round_versat_merge_mux_19_sel;
    iptr TOP_aes_round_versat_merge_mux_20_sel;
    iptr TOP_aes_round_versat_merge_mux_21_sel;
    iptr TOP_aes_round_versat_merge_mux_22_sel;
    iptr TOP_aes_round_versat_merge_mux_23_sel;
    iptr TOP_aes_round_versat_merge_mux_24_sel;
    iptr TOP_aes_round_versat_merge_mux_25_sel;
    iptr TOP_aes_round_versat_merge_mux_26_sel;
    iptr TOP_aes_round_versat_merge_mux_27_sel;
    iptr TOP_aes_round_versat_merge_mux_28_sel;
    iptr TOP_aes_round_versat_merge_mux_29_sel;
    iptr TOP_aes_round_versat_merge_mux_30_sel;
    iptr TOP_aes_round_versat_merge_mux_31_sel;
    iptr TOP_aes_round_versat_merge_mux_32_sel;
    iptr TOP_aes_round_versat_merge_mux_33_sel;
    iptr TOP_aes_round_versat_merge_mux_34_sel;
    iptr TOP_aes_round_versat_merge_mux_35_sel;
    iptr TOP_aes_round_versat_merge_mux_36_sel;
    iptr TOP_aes_round_versat_merge_mux_37_sel;
    iptr TOP_aes_round_versat_merge_mux_38_sel;
    iptr TOP_aes_round_versat_merge_mux_39_sel;
    iptr TOP_aes_round_versat_merge_mux_40_sel;
    iptr TOP_aes_round_versat_merge_mux_41_sel;
    iptr TOP_aes_round_versat_merge_mux_42_sel;
    iptr TOP_aes_round_versat_merge_mux_43_sel;
    iptr TOP_aes_round_versat_merge_mux_44_sel;
    iptr TOP_aes_round_versat_merge_mux_45_sel;
    iptr TOP_aes_round_versat_merge_mux_46_sel;
    iptr TOP_aes_round_versat_merge_mux_47_sel;
    iptr TOP_aes_round_versat_merge_mux_48_sel;
    iptr TOP_aes_round_versat_merge_mux_49_sel;
    iptr TOP_aes_round_versat_merge_mux_50_sel;
    iptr TOP_aes_round_versat_merge_mux_51_sel;
    iptr TOP_aes_round_versat_merge_mux_52_sel;
    iptr TOP_aes_round_versat_merge_mux_53_sel;
    iptr TOP_aes_round_versat_merge_mux_54_sel;
    iptr TOP_aes_round_versat_merge_mux_55_sel;
    iptr TOP_aes_round_versat_merge_mux_56_sel;
    iptr TOP_aes_round_versat_merge_mux_57_sel;
    iptr TOP_aes_round_versat_merge_mux_58_sel;
    iptr TOP_aes_round_versat_merge_mux_59_sel;
    iptr TOP_aes_round_versat_merge_mux_60_sel;
    iptr TOP_aes_round_versat_merge_mux_61_sel;
    iptr TOP_aes_round_versat_merge_mux_62_sel;
    iptr TOP_aes_round_versat_merge_mux_63_sel;
  };
  iptr TOP_sha_MemRead_ext_addr;
  iptr TOP_sha_MemRead_perA;
  iptr TOP_sha_MemRead_incrA;
  iptr TOP_sha_MemRead_length;
  iptr TOP_sha_MemRead_pingPong;
  iptr TOP_sha_MemRead_iterB;
  iptr TOP_sha_MemRead_perB;
  iptr TOP_sha_MemRead_dutyB;
  iptr TOP_sha_MemRead_startB;
  iptr TOP_sha_MemRead_shiftB;
  iptr TOP_sha_MemRead_incrB;
  iptr TOP_sha_MemRead_reverseB;
  iptr TOP_sha_MemRead_extB;
  iptr TOP_sha_MemRead_iter2B;
  iptr TOP_sha_MemRead_per2B;
  iptr TOP_sha_MemRead_shift2B;
  iptr TOP_sha_MemRead_incr2B;
  iptr TOP_sha_MemRead_enableRead;
  iptr TOP_sha_Swap_enabled;
  iptr TOP_sha_State_s_0_reg_disabled;
  iptr TOP_sha_State_s_1_reg_disabled;
  iptr TOP_sha_State_s_2_reg_disabled;
  iptr TOP_sha_State_s_3_reg_disabled;
  iptr TOP_sha_State_s_4_reg_disabled;
  iptr TOP_sha_State_s_5_reg_disabled;
  iptr TOP_sha_State_s_6_reg_disabled;
  iptr TOP_sha_State_s_7_reg_disabled;
  iptr TOP_eliece_mat_disabled;
  iptr TOP_eliece_mat_iterA;
  iptr TOP_eliece_mat_perA;
  iptr TOP_eliece_mat_dutyA;
  iptr TOP_eliece_mat_startA;
  iptr TOP_eliece_mat_shiftA;
  iptr TOP_eliece_mat_incrA;
  iptr TOP_eliece_mat_reverseA;
  iptr TOP_eliece_mat_extA;
  iptr TOP_eliece_mat_in0_wr;
  iptr TOP_eliece_mat_iterB;
  iptr TOP_eliece_mat_perB;
  iptr TOP_eliece_mat_dutyB;
  iptr TOP_eliece_mat_startB;
  iptr TOP_eliece_mat_shiftB;
  iptr TOP_eliece_mat_incrB;
  iptr TOP_eliece_mat_reverseB;
  iptr TOP_eliece_row_ext_addr;
  iptr TOP_eliece_row_perA;
  iptr TOP_eliece_row_incrA;
  iptr TOP_eliece_row_length;
  iptr TOP_eliece_row_pingPong;
  iptr TOP_eliece_row_iterB;
  iptr TOP_eliece_row_perB;
  iptr TOP_eliece_row_dutyB;
  iptr TOP_eliece_row_startB;
  iptr TOP_eliece_row_shiftB;
  iptr TOP_eliece_row_incrB;
  iptr TOP_eliece_row_reverseB;
  iptr TOP_eliece_row_extB;
  iptr TOP_eliece_row_iter2B;
  iptr TOP_eliece_row_per2B;
  iptr TOP_eliece_row_shift2B;
  iptr TOP_eliece_row_incr2B;
  iptr TOP_eliece_row_enableRead;
  iptr TOP_eliece_writer_ext_addr;
  iptr TOP_eliece_writer_perA;
  iptr TOP_eliece_writer_incrA;
  iptr TOP_eliece_writer_length;
  iptr TOP_eliece_writer_pingPong;
  iptr TOP_eliece_writer_iterB;
  iptr TOP_eliece_writer_perB;
  iptr TOP_eliece_writer_dutyB;
  iptr TOP_eliece_writer_startB;
  iptr TOP_eliece_writer_shiftB;
  iptr TOP_eliece_writer_incrB;
  iptr TOP_eliece_writer_reverseB;
  iptr TOP_eliece_writer_extB;
  iptr TOP_eliece_writer_iter2B;
  iptr TOP_eliece_writer_per2B;
  iptr TOP_eliece_writer_shift2B;
  iptr TOP_eliece_writer_incr2B;
  iptr TOP_eliece_writer_enableWrite;
  iptr TOP_eliece_mask_constant;
} AcceleratorConfig;

typedef struct {
  iptr FullAESRounds_buffer0_1_1_amount;
  iptr FullAESRounds_buffer1_1_1_amount;
  iptr FullAESRounds_buffer2_1_1_amount;
  iptr FullAESRounds_buffer3_1_1_amount;
  iptr FullAESRounds_buffer4_1_1_amount;
  iptr FullAESRounds_buffer5_1_1_amount;
  iptr FullAESRounds_buffer6_1_1_amount;
  iptr FullAESRounds_buffer7_1_1_amount;
  iptr FullAESRounds_buffer8_1_1_amount;
  iptr FullAESRounds_buffer9_1_1_amount;
  iptr FullAESRounds_buffer10_1_1_amount;
  iptr FullAESRounds_buffer11_1_1_amount;
  iptr FullAESRounds_buffer12_1_1_amount;
  iptr FullAESRounds_buffer13_1_1_amount;
  iptr FullAESRounds_buffer14_1_1_amount;
  iptr FullAESRounds_buffer15_1_1_amount;
  iptr Constants_mem_disabled;
  iptr Constants_mem_iterA;
  iptr Constants_mem_perA;
  iptr Constants_mem_dutyA;
  iptr Constants_mem_startA;
  iptr Constants_mem_shiftA;
  iptr Constants_mem_incrA;
  iptr Constants_mem_reverseA;
  iptr Constants_mem_extA;
  iptr Constants_mem_iter2A;
  iptr Constants_mem_per2A;
  iptr Constants_mem_shift2A;
  iptr Constants_mem_incr2A;
} AcceleratorStatic;

typedef struct {
  union {
    struct {
      iptr TOP_Delay0;
      iptr TOP_Delay1;
      iptr TOP_Delay2;
      iptr TOP_Delay3;
      iptr TOP_Delay4;
      iptr TOP_Delay5;
      iptr TOP_Delay6;
      iptr TOP_Delay7;
      iptr TOP_Delay8;
      iptr TOP_Delay9;
      iptr TOP_Delay10;
      iptr TOP_Delay11;
      iptr TOP_Delay12;
      iptr TOP_Delay13;
      iptr TOP_Delay14;
      iptr TOP_Delay15;
      iptr TOP_Delay16;
      iptr TOP_Delay17;
      iptr TOP_Delay18;
      iptr TOP_Delay19;
      iptr TOP_Delay20;
      iptr TOP_Delay21;
      iptr TOP_Delay22;
      iptr TOP_Delay23;
      iptr TOP_Delay24;
      iptr TOP_Delay25;
      iptr TOP_Delay26;
      iptr TOP_Delay27;
      iptr TOP_Delay28;
      iptr TOP_Delay29;
      iptr TOP_Delay30;
      iptr TOP_Delay31;
      iptr TOP_Delay32;
      iptr TOP_Delay33;
      iptr TOP_Delay34;
      iptr TOP_Delay35;
      iptr TOP_Delay36;
      iptr TOP_Delay37;
      iptr TOP_Delay38;
      iptr TOP_Delay39;
      iptr TOP_Delay40;
      iptr TOP_Delay41;
      iptr TOP_Delay42;
      iptr TOP_Delay43;
      iptr TOP_Delay44;
      iptr TOP_Delay45;
      iptr TOP_Delay46;
      iptr TOP_Delay47;
      iptr TOP_Delay48;
      iptr TOP_Delay49;
      iptr TOP_Delay50;
      iptr TOP_Delay51;
      iptr TOP_Delay52;
      iptr TOP_Delay53;
      iptr TOP_Delay54;
      iptr TOP_Delay55;
      iptr TOP_Delay56;
      iptr TOP_Delay57;
      iptr TOP_Delay58;
      iptr TOP_Delay59;
      iptr TOP_Delay60;
      iptr TOP_Delay61;
      iptr TOP_Delay62;
      iptr TOP_Delay63;
      iptr TOP_Delay64;
      iptr TOP_Delay65;
      iptr TOP_Delay66;
      iptr TOP_Delay67;
      iptr TOP_Delay68;
      iptr TOP_Delay69;
      iptr TOP_Delay70;
      iptr TOP_Delay71;
      iptr TOP_Delay72;
      iptr TOP_Delay73;
      iptr TOP_Delay74;
      iptr TOP_Delay75;
      iptr TOP_Delay76;
      iptr TOP_Delay77;
      iptr TOP_Delay78;
      iptr TOP_Delay79;
      iptr TOP_Delay80;
      iptr TOP_Delay81;
      iptr TOP_Delay82;
      iptr TOP_Delay83;
      iptr TOP_Delay84;
      iptr TOP_Delay85;
      iptr TOP_Delay86;
    };
    iptr delays[87];
  };
} AcceleratorDelay;

typedef struct {
  int TOP_aes_state_0_currentValue;
  int TOP_aes_state_1_currentValue;
  int TOP_aes_state_2_currentValue;
  int TOP_aes_state_3_currentValue;
  int TOP_aes_state_4_currentValue;
  int TOP_aes_state_5_currentValue;
  int TOP_aes_state_6_currentValue;
  int TOP_aes_state_7_currentValue;
  int TOP_aes_state_8_currentValue;
  int TOP_aes_state_9_currentValue;
  int TOP_aes_state_10_currentValue;
  int TOP_aes_state_11_currentValue;
  int TOP_aes_state_12_currentValue;
  int TOP_aes_state_13_currentValue;
  int TOP_aes_state_14_currentValue;
  int TOP_aes_state_15_currentValue;
  int TOP_aes_lastResult_0_currentValue;
  int TOP_aes_lastResult_1_currentValue;
  int TOP_aes_lastResult_2_currentValue;
  int TOP_aes_lastResult_3_currentValue;
  int TOP_aes_lastResult_4_currentValue;
  int TOP_aes_lastResult_5_currentValue;
  int TOP_aes_lastResult_6_currentValue;
  int TOP_aes_lastResult_7_currentValue;
  int TOP_aes_lastResult_8_currentValue;
  int TOP_aes_lastResult_9_currentValue;
  int TOP_aes_lastResult_10_currentValue;
  int TOP_aes_lastResult_11_currentValue;
  int TOP_aes_lastResult_12_currentValue;
  int TOP_aes_lastResult_13_currentValue;
  int TOP_aes_lastResult_14_currentValue;
  int TOP_aes_lastResult_15_currentValue;
  int TOP_aes_lastValToAdd_0_currentValue;
  int TOP_aes_lastValToAdd_1_currentValue;
  int TOP_aes_lastValToAdd_2_currentValue;
  int TOP_aes_lastValToAdd_3_currentValue;
  int TOP_aes_lastValToAdd_4_currentValue;
  int TOP_aes_lastValToAdd_5_currentValue;
  int TOP_aes_lastValToAdd_6_currentValue;
  int TOP_aes_lastValToAdd_7_currentValue;
  int TOP_aes_lastValToAdd_8_currentValue;
  int TOP_aes_lastValToAdd_9_currentValue;
  int TOP_aes_lastValToAdd_10_currentValue;
  int TOP_aes_lastValToAdd_11_currentValue;
  int TOP_aes_lastValToAdd_12_currentValue;
  int TOP_aes_lastValToAdd_13_currentValue;
  int TOP_aes_lastValToAdd_14_currentValue;
  int TOP_aes_lastValToAdd_15_currentValue;
  int TOP_sha_State_s_0_reg_currentValue;
  int TOP_sha_State_s_1_reg_currentValue;
  int TOP_sha_State_s_2_reg_currentValue;
  int TOP_sha_State_s_3_reg_currentValue;
  int TOP_sha_State_s_4_reg_currentValue;
  int TOP_sha_State_s_5_reg_currentValue;
  int TOP_sha_State_s_6_reg_currentValue;
  int TOP_sha_State_s_7_reg_currentValue;
} AcceleratorState;

static const int memMappedStart = 0x80000;
static const int versatAddressSpace = 2 * 0x80000;

extern iptr versat_base;

// NOTE: The address for memory mapped units depends on the address of
//       the accelerator.  Because of this, the full address can only
//       be calculated after calling versat_init(iptr), which is the
//       function that sets the versat_base variable.  It is for this
//       reason that the address info for every unit is a define. Addr
//       variables must be instantiated only after calling
//       versat_base.

// Base address for each memory mapped unit
#define TOP_aes_key_0_addr ((void *)(versat_base + memMappedStart + 0x0))
#define TOP_aes_key_1_addr ((void *)(versat_base + memMappedStart + 0x40))
#define TOP_aes_key_2_addr ((void *)(versat_base + memMappedStart + 0x80))
#define TOP_aes_key_3_addr ((void *)(versat_base + memMappedStart + 0xc0))
#define TOP_aes_key_4_addr ((void *)(versat_base + memMappedStart + 0x100))
#define TOP_aes_key_5_addr ((void *)(versat_base + memMappedStart + 0x140))
#define TOP_aes_key_6_addr ((void *)(versat_base + memMappedStart + 0x180))
#define TOP_aes_key_7_addr ((void *)(versat_base + memMappedStart + 0x1c0))
#define TOP_aes_key_8_addr ((void *)(versat_base + memMappedStart + 0x200))
#define TOP_aes_key_9_addr ((void *)(versat_base + memMappedStart + 0x240))
#define TOP_aes_key_10_addr ((void *)(versat_base + memMappedStart + 0x280))
#define TOP_aes_key_11_addr ((void *)(versat_base + memMappedStart + 0x2c0))
#define TOP_aes_key_12_addr ((void *)(versat_base + memMappedStart + 0x300))
#define TOP_aes_key_13_addr ((void *)(versat_base + memMappedStart + 0x340))
#define TOP_aes_key_14_addr ((void *)(versat_base + memMappedStart + 0x380))
#define TOP_aes_key_15_addr ((void *)(versat_base + memMappedStart + 0x3c0))
#define TOP_aes_state_0_addr ((void *)(versat_base + memMappedStart + 0x400))
#define TOP_aes_state_1_addr ((void *)(versat_base + memMappedStart + 0x404))
#define TOP_aes_state_2_addr ((void *)(versat_base + memMappedStart + 0x408))
#define TOP_aes_state_3_addr ((void *)(versat_base + memMappedStart + 0x40c))
#define TOP_aes_state_4_addr ((void *)(versat_base + memMappedStart + 0x410))
#define TOP_aes_state_5_addr ((void *)(versat_base + memMappedStart + 0x414))
#define TOP_aes_state_6_addr ((void *)(versat_base + memMappedStart + 0x418))
#define TOP_aes_state_7_addr ((void *)(versat_base + memMappedStart + 0x41c))
#define TOP_aes_state_8_addr ((void *)(versat_base + memMappedStart + 0x420))
#define TOP_aes_state_9_addr ((void *)(versat_base + memMappedStart + 0x424))
#define TOP_aes_state_10_addr ((void *)(versat_base + memMappedStart + 0x428))
#define TOP_aes_state_11_addr ((void *)(versat_base + memMappedStart + 0x42c))
#define TOP_aes_state_12_addr ((void *)(versat_base + memMappedStart + 0x430))
#define TOP_aes_state_13_addr ((void *)(versat_base + memMappedStart + 0x434))
#define TOP_aes_state_14_addr ((void *)(versat_base + memMappedStart + 0x438))
#define TOP_aes_state_15_addr ((void *)(versat_base + memMappedStart + 0x43c))
#define TOP_aes_lastResult_0_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x440))
#define TOP_aes_lastResult_1_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x444))
#define TOP_aes_lastResult_2_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x448))
#define TOP_aes_lastResult_3_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x44c))
#define TOP_aes_lastResult_4_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x450))
#define TOP_aes_lastResult_5_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x454))
#define TOP_aes_lastResult_6_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x458))
#define TOP_aes_lastResult_7_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x45c))
#define TOP_aes_lastResult_8_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x460))
#define TOP_aes_lastResult_9_addr                                              \
  ((void *)(versat_base + memMappedStart + 0x464))
#define TOP_aes_lastResult_10_addr                                             \
  ((void *)(versat_base + memMappedStart + 0x468))
#define TOP_aes_lastResult_11_addr                                             \
  ((void *)(versat_base + memMappedStart + 0x46c))
#define TOP_aes_lastResult_12_addr                                             \
  ((void *)(versat_base + memMappedStart + 0x470))
#define TOP_aes_lastResult_13_addr                                             \
  ((void *)(versat_base + memMappedStart + 0x474))
#define TOP_aes_lastResult_14_addr                                             \
  ((void *)(versat_base + memMappedStart + 0x478))
#define TOP_aes_lastResult_15_addr                                             \
  ((void *)(versat_base + memMappedStart + 0x47c))
#define TOP_aes_lastValToAdd_0_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x480))
#define TOP_aes_lastValToAdd_1_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x484))
#define TOP_aes_lastValToAdd_2_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x488))
#define TOP_aes_lastValToAdd_3_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x48c))
#define TOP_aes_lastValToAdd_4_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x490))
#define TOP_aes_lastValToAdd_5_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x494))
#define TOP_aes_lastValToAdd_6_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x498))
#define TOP_aes_lastValToAdd_7_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x49c))
#define TOP_aes_lastValToAdd_8_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x4a0))
#define TOP_aes_lastValToAdd_9_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x4a4))
#define TOP_aes_lastValToAdd_10_addr                                           \
  ((void *)(versat_base + memMappedStart + 0x4a8))
#define TOP_aes_lastValToAdd_11_addr                                           \
  ((void *)(versat_base + memMappedStart + 0x4ac))
#define TOP_aes_lastValToAdd_12_addr                                           \
  ((void *)(versat_base + memMappedStart + 0x4b0))
#define TOP_aes_lastValToAdd_13_addr                                           \
  ((void *)(versat_base + memMappedStart + 0x4b4))
#define TOP_aes_lastValToAdd_14_addr                                           \
  ((void *)(versat_base + memMappedStart + 0x4b8))
#define TOP_aes_lastValToAdd_15_addr                                           \
  ((void *)(versat_base + memMappedStart + 0x4bc))
#define TOP_aes_schedule_s_b_0_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x600))
#define TOP_aes_schedule_s_b_1_addr                                            \
  ((void *)(versat_base + memMappedStart + 0x700))
#define TOP_aes_round_mixColumns_d_0_mul2_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4000))
#define TOP_aes_round_mixColumns_d_0_mul2_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4100))
#define TOP_aes_round_mixColumns_d_0_mul3_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4200))
#define TOP_aes_round_mixColumns_d_0_mul3_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4300))
#define TOP_aes_round_mixColumns_d_1_mul2_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4400))
#define TOP_aes_round_mixColumns_d_1_mul2_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4500))
#define TOP_aes_round_mixColumns_d_1_mul3_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4600))
#define TOP_aes_round_mixColumns_d_1_mul3_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4700))
#define TOP_aes_round_mixColumns_d_2_mul2_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4800))
#define TOP_aes_round_mixColumns_d_2_mul2_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4900))
#define TOP_aes_round_mixColumns_d_2_mul3_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4a00))
#define TOP_aes_round_mixColumns_d_2_mul3_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4b00))
#define TOP_aes_round_mixColumns_d_3_mul2_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4c00))
#define TOP_aes_round_mixColumns_d_3_mul2_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4d00))
#define TOP_aes_round_mixColumns_d_3_mul3_0_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4e00))
#define TOP_aes_round_mixColumns_d_3_mul3_1_addr                               \
  ((void *)(versat_base + memMappedStart + 0x4f00))
#define TOP_aes_round_invMixColumns_d_0_mul9_0_addr                            \
  ((void *)(versat_base + memMappedStart + 0x6000))
#define TOP_aes_round_invMixColumns_d_0_mul9_1_addr                            \
  ((void *)(versat_base + memMappedStart + 0x6100))
#define TOP_aes_round_invMixColumns_d_0_mul11_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6200))
#define TOP_aes_round_invMixColumns_d_0_mul11_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6300))
#define TOP_aes_round_invMixColumns_d_0_mul13_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6400))
#define TOP_aes_round_invMixColumns_d_0_mul13_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6500))
#define TOP_aes_round_invMixColumns_d_0_mul14_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6600))
#define TOP_aes_round_invMixColumns_d_0_mul14_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6700))
#define TOP_aes_round_invMixColumns_d_1_mul9_0_addr                            \
  ((void *)(versat_base + memMappedStart + 0x6800))
#define TOP_aes_round_invMixColumns_d_1_mul9_1_addr                            \
  ((void *)(versat_base + memMappedStart + 0x6900))
#define TOP_aes_round_invMixColumns_d_1_mul11_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6a00))
#define TOP_aes_round_invMixColumns_d_1_mul11_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6b00))
#define TOP_aes_round_invMixColumns_d_1_mul13_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6c00))
#define TOP_aes_round_invMixColumns_d_1_mul13_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6d00))
#define TOP_aes_round_invMixColumns_d_1_mul14_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6e00))
#define TOP_aes_round_invMixColumns_d_1_mul14_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x6f00))
#define TOP_aes_round_invMixColumns_d_2_mul9_0_addr                            \
  ((void *)(versat_base + memMappedStart + 0x7000))
#define TOP_aes_round_invMixColumns_d_2_mul9_1_addr                            \
  ((void *)(versat_base + memMappedStart + 0x7100))
#define TOP_aes_round_invMixColumns_d_2_mul11_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7200))
#define TOP_aes_round_invMixColumns_d_2_mul11_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7300))
#define TOP_aes_round_invMixColumns_d_2_mul13_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7400))
#define TOP_aes_round_invMixColumns_d_2_mul13_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7500))
#define TOP_aes_round_invMixColumns_d_2_mul14_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7600))
#define TOP_aes_round_invMixColumns_d_2_mul14_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7700))
#define TOP_aes_round_invMixColumns_d_3_mul9_0_addr                            \
  ((void *)(versat_base + memMappedStart + 0x7800))
#define TOP_aes_round_invMixColumns_d_3_mul9_1_addr                            \
  ((void *)(versat_base + memMappedStart + 0x7900))
#define TOP_aes_round_invMixColumns_d_3_mul11_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7a00))
#define TOP_aes_round_invMixColumns_d_3_mul11_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7b00))
#define TOP_aes_round_invMixColumns_d_3_mul13_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7c00))
#define TOP_aes_round_invMixColumns_d_3_mul13_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7d00))
#define TOP_aes_round_invMixColumns_d_3_mul14_0_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7e00))
#define TOP_aes_round_invMixColumns_d_3_mul14_1_addr                           \
  ((void *)(versat_base + memMappedStart + 0x7f00))
#define TOP_sha_cMem0_mem_addr ((void *)(versat_base + memMappedStart + 0x8000))
#define TOP_sha_cMem1_mem_addr ((void *)(versat_base + memMappedStart + 0x9000))
#define TOP_sha_cMem2_mem_addr ((void *)(versat_base + memMappedStart + 0xa000))
#define TOP_sha_cMem3_mem_addr ((void *)(versat_base + memMappedStart + 0xb000))
#define TOP_sha_State_s_0_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc000))
#define TOP_sha_State_s_1_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc004))
#define TOP_sha_State_s_2_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc008))
#define TOP_sha_State_s_3_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc00c))
#define TOP_sha_State_s_4_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc010))
#define TOP_sha_State_s_5_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc014))
#define TOP_sha_State_s_6_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc018))
#define TOP_sha_State_s_7_reg_addr                                             \
  ((void *)(versat_base + memMappedStart + 0xc01c))
#define TOP_eliece_mat_addr ((void *)(versat_base + memMappedStart + 0x10000))

#define ACCELERATOR_TOP_ADDR_INIT                                              \
  {                                                                            \
    TOP_aes_key_0_addr, TOP_aes_key_1_addr, TOP_aes_key_2_addr,                \
        TOP_aes_key_3_addr, TOP_aes_key_4_addr, TOP_aes_key_5_addr,            \
        TOP_aes_key_6_addr, TOP_aes_key_7_addr, TOP_aes_key_8_addr,            \
        TOP_aes_key_9_addr, TOP_aes_key_10_addr, TOP_aes_key_11_addr,          \
        TOP_aes_key_12_addr, TOP_aes_key_13_addr, TOP_aes_key_14_addr,         \
        TOP_aes_key_15_addr, TOP_aes_state_0_addr, TOP_aes_state_1_addr,       \
        TOP_aes_state_2_addr, TOP_aes_state_3_addr, TOP_aes_state_4_addr,      \
        TOP_aes_state_5_addr, TOP_aes_state_6_addr, TOP_aes_state_7_addr,      \
        TOP_aes_state_8_addr, TOP_aes_state_9_addr, TOP_aes_state_10_addr,     \
        TOP_aes_state_11_addr, TOP_aes_state_12_addr, TOP_aes_state_13_addr,   \
        TOP_aes_state_14_addr, TOP_aes_state_15_addr,                          \
        TOP_aes_lastResult_0_addr, TOP_aes_lastResult_1_addr,                  \
        TOP_aes_lastResult_2_addr, TOP_aes_lastResult_3_addr,                  \
        TOP_aes_lastResult_4_addr, TOP_aes_lastResult_5_addr,                  \
        TOP_aes_lastResult_6_addr, TOP_aes_lastResult_7_addr,                  \
        TOP_aes_lastResult_8_addr, TOP_aes_lastResult_9_addr,                  \
        TOP_aes_lastResult_10_addr, TOP_aes_lastResult_11_addr,                \
        TOP_aes_lastResult_12_addr, TOP_aes_lastResult_13_addr,                \
        TOP_aes_lastResult_14_addr, TOP_aes_lastResult_15_addr,                \
        TOP_aes_lastValToAdd_0_addr, TOP_aes_lastValToAdd_1_addr,              \
        TOP_aes_lastValToAdd_2_addr, TOP_aes_lastValToAdd_3_addr,              \
        TOP_aes_lastValToAdd_4_addr, TOP_aes_lastValToAdd_5_addr,              \
        TOP_aes_lastValToAdd_6_addr, TOP_aes_lastValToAdd_7_addr,              \
        TOP_aes_lastValToAdd_8_addr, TOP_aes_lastValToAdd_9_addr,              \
        TOP_aes_lastValToAdd_10_addr, TOP_aes_lastValToAdd_11_addr,            \
        TOP_aes_lastValToAdd_12_addr, TOP_aes_lastValToAdd_13_addr,            \
        TOP_aes_lastValToAdd_14_addr, TOP_aes_lastValToAdd_15_addr,            \
        TOP_aes_schedule_s_b_0_addr, TOP_aes_schedule_s_b_1_addr,              \
        TOP_aes_round_mixColumns_d_0_mul2_0_addr,                              \
        TOP_aes_round_mixColumns_d_0_mul2_1_addr,                              \
        TOP_aes_round_mixColumns_d_0_mul3_0_addr,                              \
        TOP_aes_round_mixColumns_d_0_mul3_1_addr,                              \
        TOP_aes_round_mixColumns_d_1_mul2_0_addr,                              \
        TOP_aes_round_mixColumns_d_1_mul2_1_addr,                              \
        TOP_aes_round_mixColumns_d_1_mul3_0_addr,                              \
        TOP_aes_round_mixColumns_d_1_mul3_1_addr,                              \
        TOP_aes_round_mixColumns_d_2_mul2_0_addr,                              \
        TOP_aes_round_mixColumns_d_2_mul2_1_addr,                              \
        TOP_aes_round_mixColumns_d_2_mul3_0_addr,                              \
        TOP_aes_round_mixColumns_d_2_mul3_1_addr,                              \
        TOP_aes_round_mixColumns_d_3_mul2_0_addr,                              \
        TOP_aes_round_mixColumns_d_3_mul2_1_addr,                              \
        TOP_aes_round_mixColumns_d_3_mul3_0_addr,                              \
        TOP_aes_round_mixColumns_d_3_mul3_1_addr,                              \
        TOP_aes_round_invMixColumns_d_0_mul9_0_addr,                           \
        TOP_aes_round_invMixColumns_d_0_mul9_1_addr,                           \
        TOP_aes_round_invMixColumns_d_0_mul11_0_addr,                          \
        TOP_aes_round_invMixColumns_d_0_mul11_1_addr,                          \
        TOP_aes_round_invMixColumns_d_0_mul13_0_addr,                          \
        TOP_aes_round_invMixColumns_d_0_mul13_1_addr,                          \
        TOP_aes_round_invMixColumns_d_0_mul14_0_addr,                          \
        TOP_aes_round_invMixColumns_d_0_mul14_1_addr,                          \
        TOP_aes_round_invMixColumns_d_1_mul9_0_addr,                           \
        TOP_aes_round_invMixColumns_d_1_mul9_1_addr,                           \
        TOP_aes_round_invMixColumns_d_1_mul11_0_addr,                          \
        TOP_aes_round_invMixColumns_d_1_mul11_1_addr,                          \
        TOP_aes_round_invMixColumns_d_1_mul13_0_addr,                          \
        TOP_aes_round_invMixColumns_d_1_mul13_1_addr,                          \
        TOP_aes_round_invMixColumns_d_1_mul14_0_addr,                          \
        TOP_aes_round_invMixColumns_d_1_mul14_1_addr,                          \
        TOP_aes_round_invMixColumns_d_2_mul9_0_addr,                           \
        TOP_aes_round_invMixColumns_d_2_mul9_1_addr,                           \
        TOP_aes_round_invMixColumns_d_2_mul11_0_addr,                          \
        TOP_aes_round_invMixColumns_d_2_mul11_1_addr,                          \
        TOP_aes_round_invMixColumns_d_2_mul13_0_addr,                          \
        TOP_aes_round_invMixColumns_d_2_mul13_1_addr,                          \
        TOP_aes_round_invMixColumns_d_2_mul14_0_addr,                          \
        TOP_aes_round_invMixColumns_d_2_mul14_1_addr,                          \
        TOP_aes_round_invMixColumns_d_3_mul9_0_addr,                           \
        TOP_aes_round_invMixColumns_d_3_mul9_1_addr,                           \
        TOP_aes_round_invMixColumns_d_3_mul11_0_addr,                          \
        TOP_aes_round_invMixColumns_d_3_mul11_1_addr,                          \
        TOP_aes_round_invMixColumns_d_3_mul13_0_addr,                          \
        TOP_aes_round_invMixColumns_d_3_mul13_1_addr,                          \
        TOP_aes_round_invMixColumns_d_3_mul14_0_addr,                          \
        TOP_aes_round_invMixColumns_d_3_mul14_1_addr, TOP_sha_cMem0_mem_addr,  \
        TOP_sha_cMem1_mem_addr, TOP_sha_cMem2_mem_addr,                        \
        TOP_sha_cMem3_mem_addr, TOP_sha_State_s_0_reg_addr,                    \
        TOP_sha_State_s_1_reg_addr, TOP_sha_State_s_2_reg_addr,                \
        TOP_sha_State_s_3_reg_addr, TOP_sha_State_s_4_reg_addr,                \
        TOP_sha_State_s_5_reg_addr, TOP_sha_State_s_6_reg_addr,                \
        TOP_sha_State_s_7_reg_addr, TOP_eliece_mat_addr                        \
  }

static unsigned int delayBuffer[] = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};
static AcceleratorDelay accelDelay = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};

#ifdef __cplusplus
extern "C" {
#endif

// Always call first before calling any other function.
void versat_init(int base);

// In pc-emul provides a low bound on performance.
// In sim-run refines the lower bound but still likely to be smaller than
// reality due to memory delays that are only present in real circuits.
int GetAcceleratorCyclesElapsed();

void RunAccelerator(int times);
void StartAccelerator();
void EndAccelerator();
void VersatMemoryCopy(void *dest, const void *data, int size);
void VersatUnitWrite(const void *baseaddr, int index, int val);
int VersatUnitRead(const void *baseaddr, int index);
float VersatUnitReadFloat(const void *baseaddr, int index);
void SignalLoop();
void VersatLoadDelay(const unsigned int *delayBuffer);

// PC-Emul side functions that allow to enable or disable certain portions of
// the emulation Their embedded counterparts simply do nothing
void ConfigEnableDMA(bool value);
void ConfigCreateVCD(bool value);
void ConfigSimulateDatabus(bool value);

#ifdef __cplusplus
} // extern "C"
#endif

// Needed by PC-EMUL to correctly simulate the design, embedded compiler should
// remove these symbols from firmware because not used by them
static const char *acceleratorTypeName = "CryptoAlgos";
static bool isSimpleAccelerator = true;
static bool acceleratorSupportsDMA = true;

static const int staticStart = 0x63 * sizeof(iptr);
static const int delayStart = 0x80 * sizeof(iptr);
static const int configStart = 0x5 * sizeof(iptr);
static const int stateStart = 0x5 * sizeof(int);

extern volatile AcceleratorConfig *accelConfig;
extern volatile AcceleratorState *accelState;
extern volatile AcceleratorStatic *accelStatics;

// Simple input and output connection for simple accelerators
#define NumberSimpleInputs 0
#define NumberSimpleOutputs 0
#define SimpleInputStart ((iptr *)accelConfig)
#define SimpleOutputStart ((int *)accelState)

#define ACCEL_TOP_aes_key_0_selectedInput                                      \
  accelConfig->TOP_aes_key_0_selectedInput
#define ACCEL_TOP_aes_key_1_selectedInput                                      \
  accelConfig->TOP_aes_key_1_selectedInput
#define ACCEL_TOP_aes_key_2_selectedInput                                      \
  accelConfig->TOP_aes_key_2_selectedInput
#define ACCEL_TOP_aes_key_3_selectedInput                                      \
  accelConfig->TOP_aes_key_3_selectedInput
#define ACCEL_TOP_aes_key_4_selectedInput                                      \
  accelConfig->TOP_aes_key_4_selectedInput
#define ACCEL_TOP_aes_key_5_selectedInput                                      \
  accelConfig->TOP_aes_key_5_selectedInput
#define ACCEL_TOP_aes_key_6_selectedInput                                      \
  accelConfig->TOP_aes_key_6_selectedInput
#define ACCEL_TOP_aes_key_7_selectedInput                                      \
  accelConfig->TOP_aes_key_7_selectedInput
#define ACCEL_TOP_aes_key_8_selectedInput                                      \
  accelConfig->TOP_aes_key_8_selectedInput
#define ACCEL_TOP_aes_key_9_selectedInput                                      \
  accelConfig->TOP_aes_key_9_selectedInput
#define ACCEL_TOP_aes_key_10_selectedInput                                     \
  accelConfig->TOP_aes_key_10_selectedInput
#define ACCEL_TOP_aes_key_11_selectedInput                                     \
  accelConfig->TOP_aes_key_11_selectedInput
#define ACCEL_TOP_aes_key_12_selectedInput                                     \
  accelConfig->TOP_aes_key_12_selectedInput
#define ACCEL_TOP_aes_key_13_selectedInput                                     \
  accelConfig->TOP_aes_key_13_selectedInput
#define ACCEL_TOP_aes_key_14_selectedInput                                     \
  accelConfig->TOP_aes_key_14_selectedInput
#define ACCEL_TOP_aes_key_15_selectedInput                                     \
  accelConfig->TOP_aes_key_15_selectedInput
#define ACCEL_TOP_aes_key_0_selectedOutput0                                    \
  accelConfig->TOP_aes_key_0_selectedOutput0
#define ACCEL_TOP_aes_key_1_selectedOutput0                                    \
  accelConfig->TOP_aes_key_1_selectedOutput0
#define ACCEL_TOP_aes_key_2_selectedOutput0                                    \
  accelConfig->TOP_aes_key_2_selectedOutput0
#define ACCEL_TOP_aes_key_3_selectedOutput0                                    \
  accelConfig->TOP_aes_key_3_selectedOutput0
#define ACCEL_TOP_aes_key_4_selectedOutput0                                    \
  accelConfig->TOP_aes_key_4_selectedOutput0
#define ACCEL_TOP_aes_key_5_selectedOutput0                                    \
  accelConfig->TOP_aes_key_5_selectedOutput0
#define ACCEL_TOP_aes_key_6_selectedOutput0                                    \
  accelConfig->TOP_aes_key_6_selectedOutput0
#define ACCEL_TOP_aes_key_7_selectedOutput0                                    \
  accelConfig->TOP_aes_key_7_selectedOutput0
#define ACCEL_TOP_aes_key_8_selectedOutput0                                    \
  accelConfig->TOP_aes_key_8_selectedOutput0
#define ACCEL_TOP_aes_key_9_selectedOutput0                                    \
  accelConfig->TOP_aes_key_9_selectedOutput0
#define ACCEL_TOP_aes_key_10_selectedOutput0                                   \
  accelConfig->TOP_aes_key_10_selectedOutput0
#define ACCEL_TOP_aes_key_11_selectedOutput0                                   \
  accelConfig->TOP_aes_key_11_selectedOutput0
#define ACCEL_TOP_aes_key_12_selectedOutput0                                   \
  accelConfig->TOP_aes_key_12_selectedOutput0
#define ACCEL_TOP_aes_key_13_selectedOutput0                                   \
  accelConfig->TOP_aes_key_13_selectedOutput0
#define ACCEL_TOP_aes_key_14_selectedOutput0                                   \
  accelConfig->TOP_aes_key_14_selectedOutput0
#define ACCEL_TOP_aes_key_15_selectedOutput0                                   \
  accelConfig->TOP_aes_key_15_selectedOutput0
#define ACCEL_TOP_aes_key_0_selectedOutput1                                    \
  accelConfig->TOP_aes_key_0_selectedOutput1
#define ACCEL_TOP_aes_key_1_selectedOutput1                                    \
  accelConfig->TOP_aes_key_1_selectedOutput1
#define ACCEL_TOP_aes_key_2_selectedOutput1                                    \
  accelConfig->TOP_aes_key_2_selectedOutput1
#define ACCEL_TOP_aes_key_3_selectedOutput1                                    \
  accelConfig->TOP_aes_key_3_selectedOutput1
#define ACCEL_TOP_aes_key_4_selectedOutput1                                    \
  accelConfig->TOP_aes_key_4_selectedOutput1
#define ACCEL_TOP_aes_key_5_selectedOutput1                                    \
  accelConfig->TOP_aes_key_5_selectedOutput1
#define ACCEL_TOP_aes_key_6_selectedOutput1                                    \
  accelConfig->TOP_aes_key_6_selectedOutput1
#define ACCEL_TOP_aes_key_7_selectedOutput1                                    \
  accelConfig->TOP_aes_key_7_selectedOutput1
#define ACCEL_TOP_aes_key_8_selectedOutput1                                    \
  accelConfig->TOP_aes_key_8_selectedOutput1
#define ACCEL_TOP_aes_key_9_selectedOutput1                                    \
  accelConfig->TOP_aes_key_9_selectedOutput1
#define ACCEL_TOP_aes_key_10_selectedOutput1                                   \
  accelConfig->TOP_aes_key_10_selectedOutput1
#define ACCEL_TOP_aes_key_11_selectedOutput1                                   \
  accelConfig->TOP_aes_key_11_selectedOutput1
#define ACCEL_TOP_aes_key_12_selectedOutput1                                   \
  accelConfig->TOP_aes_key_12_selectedOutput1
#define ACCEL_TOP_aes_key_13_selectedOutput1                                   \
  accelConfig->TOP_aes_key_13_selectedOutput1
#define ACCEL_TOP_aes_key_14_selectedOutput1                                   \
  accelConfig->TOP_aes_key_14_selectedOutput1
#define ACCEL_TOP_aes_key_15_selectedOutput1                                   \
  accelConfig->TOP_aes_key_15_selectedOutput1
#define ACCEL_TOP_aes_key_0_disabled accelConfig->TOP_aes_key_0_disabled
#define ACCEL_TOP_aes_key_1_disabled accelConfig->TOP_aes_key_1_disabled
#define ACCEL_TOP_aes_key_2_disabled accelConfig->TOP_aes_key_2_disabled
#define ACCEL_TOP_aes_key_3_disabled accelConfig->TOP_aes_key_3_disabled
#define ACCEL_TOP_aes_key_4_disabled accelConfig->TOP_aes_key_4_disabled
#define ACCEL_TOP_aes_key_5_disabled accelConfig->TOP_aes_key_5_disabled
#define ACCEL_TOP_aes_key_6_disabled accelConfig->TOP_aes_key_6_disabled
#define ACCEL_TOP_aes_key_7_disabled accelConfig->TOP_aes_key_7_disabled
#define ACCEL_TOP_aes_key_8_disabled accelConfig->TOP_aes_key_8_disabled
#define ACCEL_TOP_aes_key_9_disabled accelConfig->TOP_aes_key_9_disabled
#define ACCEL_TOP_aes_key_10_disabled accelConfig->TOP_aes_key_10_disabled
#define ACCEL_TOP_aes_key_11_disabled accelConfig->TOP_aes_key_11_disabled
#define ACCEL_TOP_aes_key_12_disabled accelConfig->TOP_aes_key_12_disabled
#define ACCEL_TOP_aes_key_13_disabled accelConfig->TOP_aes_key_13_disabled
#define ACCEL_TOP_aes_key_14_disabled accelConfig->TOP_aes_key_14_disabled
#define ACCEL_TOP_aes_key_15_disabled accelConfig->TOP_aes_key_15_disabled
#define ACCEL_TOP_aes_state_0_disabled accelConfig->TOP_aes_state_0_disabled
#define ACCEL_TOP_aes_state_1_disabled accelConfig->TOP_aes_state_1_disabled
#define ACCEL_TOP_aes_state_2_disabled accelConfig->TOP_aes_state_2_disabled
#define ACCEL_TOP_aes_state_3_disabled accelConfig->TOP_aes_state_3_disabled
#define ACCEL_TOP_aes_state_4_disabled accelConfig->TOP_aes_state_4_disabled
#define ACCEL_TOP_aes_state_5_disabled accelConfig->TOP_aes_state_5_disabled
#define ACCEL_TOP_aes_state_6_disabled accelConfig->TOP_aes_state_6_disabled
#define ACCEL_TOP_aes_state_7_disabled accelConfig->TOP_aes_state_7_disabled
#define ACCEL_TOP_aes_state_8_disabled accelConfig->TOP_aes_state_8_disabled
#define ACCEL_TOP_aes_state_9_disabled accelConfig->TOP_aes_state_9_disabled
#define ACCEL_TOP_aes_state_10_disabled accelConfig->TOP_aes_state_10_disabled
#define ACCEL_TOP_aes_state_11_disabled accelConfig->TOP_aes_state_11_disabled
#define ACCEL_TOP_aes_state_12_disabled accelConfig->TOP_aes_state_12_disabled
#define ACCEL_TOP_aes_state_13_disabled accelConfig->TOP_aes_state_13_disabled
#define ACCEL_TOP_aes_state_14_disabled accelConfig->TOP_aes_state_14_disabled
#define ACCEL_TOP_aes_state_15_disabled accelConfig->TOP_aes_state_15_disabled
#define ACCEL_TOP_aes_lastResult_0_disabled                                    \
  accelConfig->TOP_aes_lastResult_0_disabled
#define ACCEL_TOP_aes_lastResult_1_disabled                                    \
  accelConfig->TOP_aes_lastResult_1_disabled
#define ACCEL_TOP_aes_lastResult_2_disabled                                    \
  accelConfig->TOP_aes_lastResult_2_disabled
#define ACCEL_TOP_aes_lastResult_3_disabled                                    \
  accelConfig->TOP_aes_lastResult_3_disabled
#define ACCEL_TOP_aes_lastResult_4_disabled                                    \
  accelConfig->TOP_aes_lastResult_4_disabled
#define ACCEL_TOP_aes_lastResult_5_disabled                                    \
  accelConfig->TOP_aes_lastResult_5_disabled
#define ACCEL_TOP_aes_lastResult_6_disabled                                    \
  accelConfig->TOP_aes_lastResult_6_disabled
#define ACCEL_TOP_aes_lastResult_7_disabled                                    \
  accelConfig->TOP_aes_lastResult_7_disabled
#define ACCEL_TOP_aes_lastResult_8_disabled                                    \
  accelConfig->TOP_aes_lastResult_8_disabled
#define ACCEL_TOP_aes_lastResult_9_disabled                                    \
  accelConfig->TOP_aes_lastResult_9_disabled
#define ACCEL_TOP_aes_lastResult_10_disabled                                   \
  accelConfig->TOP_aes_lastResult_10_disabled
#define ACCEL_TOP_aes_lastResult_11_disabled                                   \
  accelConfig->TOP_aes_lastResult_11_disabled
#define ACCEL_TOP_aes_lastResult_12_disabled                                   \
  accelConfig->TOP_aes_lastResult_12_disabled
#define ACCEL_TOP_aes_lastResult_13_disabled                                   \
  accelConfig->TOP_aes_lastResult_13_disabled
#define ACCEL_TOP_aes_lastResult_14_disabled                                   \
  accelConfig->TOP_aes_lastResult_14_disabled
#define ACCEL_TOP_aes_lastResult_15_disabled                                   \
  accelConfig->TOP_aes_lastResult_15_disabled
#define ACCEL_TOP_aes_lastValToAdd_0_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_0_disabled
#define ACCEL_TOP_aes_lastValToAdd_1_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_1_disabled
#define ACCEL_TOP_aes_lastValToAdd_2_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_2_disabled
#define ACCEL_TOP_aes_lastValToAdd_3_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_3_disabled
#define ACCEL_TOP_aes_lastValToAdd_4_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_4_disabled
#define ACCEL_TOP_aes_lastValToAdd_5_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_5_disabled
#define ACCEL_TOP_aes_lastValToAdd_6_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_6_disabled
#define ACCEL_TOP_aes_lastValToAdd_7_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_7_disabled
#define ACCEL_TOP_aes_lastValToAdd_8_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_8_disabled
#define ACCEL_TOP_aes_lastValToAdd_9_disabled                                  \
  accelConfig->TOP_aes_lastValToAdd_9_disabled
#define ACCEL_TOP_aes_lastValToAdd_10_disabled                                 \
  accelConfig->TOP_aes_lastValToAdd_10_disabled
#define ACCEL_TOP_aes_lastValToAdd_11_disabled                                 \
  accelConfig->TOP_aes_lastValToAdd_11_disabled
#define ACCEL_TOP_aes_lastValToAdd_12_disabled                                 \
  accelConfig->TOP_aes_lastValToAdd_12_disabled
#define ACCEL_TOP_aes_lastValToAdd_13_disabled                                 \
  accelConfig->TOP_aes_lastValToAdd_13_disabled
#define ACCEL_TOP_aes_lastValToAdd_14_disabled                                 \
  accelConfig->TOP_aes_lastValToAdd_14_disabled
#define ACCEL_TOP_aes_lastValToAdd_15_disabled                                 \
  accelConfig->TOP_aes_lastValToAdd_15_disabled
#define ACCEL_TOP_aes_schedule_s_mux_0_sel                                     \
  accelConfig->TOP_aes_schedule_s_mux_0_sel
#define ACCEL_TOP_aes_schedule_s_mux_1_sel                                     \
  accelConfig->TOP_aes_schedule_s_mux_1_sel
#define ACCEL_TOP_aes_schedule_s_mux_2_sel                                     \
  accelConfig->TOP_aes_schedule_s_mux_2_sel
#define ACCEL_TOP_aes_schedule_s_mux_3_sel                                     \
  accelConfig->TOP_aes_schedule_s_mux_3_sel
#define ACCEL_TOP_aes_rcon_constant accelConfig->TOP_aes_rcon_constant
#define ACCEL_TOP_aes_round_versat_merge_mux_0_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_0_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_1_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_1_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_2_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_2_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_3_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_3_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_4_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_4_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_5_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_5_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_6_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_6_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_7_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_7_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_8_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_8_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_9_sel                             \
  accelConfig->TOP_aes_round_versat_merge_mux_9_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_10_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_10_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_11_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_11_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_12_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_12_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_13_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_13_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_14_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_14_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_15_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_15_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_16_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_16_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_17_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_17_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_18_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_18_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_19_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_19_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_20_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_20_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_21_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_21_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_22_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_22_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_23_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_23_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_24_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_24_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_25_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_25_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_26_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_26_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_27_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_27_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_28_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_28_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_29_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_29_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_30_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_30_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_31_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_31_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_32_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_32_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_33_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_33_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_34_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_34_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_35_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_35_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_36_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_36_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_37_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_37_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_38_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_38_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_39_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_39_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_40_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_40_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_41_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_41_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_42_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_42_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_43_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_43_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_44_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_44_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_45_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_45_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_46_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_46_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_47_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_47_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_48_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_48_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_49_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_49_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_50_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_50_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_51_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_51_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_52_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_52_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_53_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_53_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_54_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_54_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_55_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_55_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_56_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_56_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_57_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_57_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_58_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_58_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_59_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_59_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_60_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_60_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_61_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_61_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_62_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_62_sel
#define ACCEL_TOP_aes_round_versat_merge_mux_63_sel                            \
  accelConfig->TOP_aes_round_versat_merge_mux_63_sel
#define ACCEL_TOP_sha_MemRead_ext_addr accelConfig->TOP_sha_MemRead_ext_addr
#define ACCEL_TOP_sha_MemRead_perA accelConfig->TOP_sha_MemRead_perA
#define ACCEL_TOP_sha_MemRead_incrA accelConfig->TOP_sha_MemRead_incrA
#define ACCEL_TOP_sha_MemRead_length accelConfig->TOP_sha_MemRead_length
#define ACCEL_TOP_sha_MemRead_pingPong accelConfig->TOP_sha_MemRead_pingPong
#define ACCEL_TOP_sha_MemRead_iterB accelConfig->TOP_sha_MemRead_iterB
#define ACCEL_TOP_sha_MemRead_perB accelConfig->TOP_sha_MemRead_perB
#define ACCEL_TOP_sha_MemRead_dutyB accelConfig->TOP_sha_MemRead_dutyB
#define ACCEL_TOP_sha_MemRead_startB accelConfig->TOP_sha_MemRead_startB
#define ACCEL_TOP_sha_MemRead_shiftB accelConfig->TOP_sha_MemRead_shiftB
#define ACCEL_TOP_sha_MemRead_incrB accelConfig->TOP_sha_MemRead_incrB
#define ACCEL_TOP_sha_MemRead_reverseB accelConfig->TOP_sha_MemRead_reverseB
#define ACCEL_TOP_sha_MemRead_extB accelConfig->TOP_sha_MemRead_extB
#define ACCEL_TOP_sha_MemRead_iter2B accelConfig->TOP_sha_MemRead_iter2B
#define ACCEL_TOP_sha_MemRead_per2B accelConfig->TOP_sha_MemRead_per2B
#define ACCEL_TOP_sha_MemRead_shift2B accelConfig->TOP_sha_MemRead_shift2B
#define ACCEL_TOP_sha_MemRead_incr2B accelConfig->TOP_sha_MemRead_incr2B
#define ACCEL_TOP_sha_MemRead_enableRead accelConfig->TOP_sha_MemRead_enableRead
#define ACCEL_TOP_sha_Swap_enabled accelConfig->TOP_sha_Swap_enabled
#define ACCEL_TOP_sha_State_s_0_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_0_reg_disabled
#define ACCEL_TOP_sha_State_s_1_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_1_reg_disabled
#define ACCEL_TOP_sha_State_s_2_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_2_reg_disabled
#define ACCEL_TOP_sha_State_s_3_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_3_reg_disabled
#define ACCEL_TOP_sha_State_s_4_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_4_reg_disabled
#define ACCEL_TOP_sha_State_s_5_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_5_reg_disabled
#define ACCEL_TOP_sha_State_s_6_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_6_reg_disabled
#define ACCEL_TOP_sha_State_s_7_reg_disabled                                   \
  accelConfig->TOP_sha_State_s_7_reg_disabled
#define ACCEL_TOP_eliece_mat_disabled accelConfig->TOP_eliece_mat_disabled
#define ACCEL_TOP_eliece_mat_iterA accelConfig->TOP_eliece_mat_iterA
#define ACCEL_TOP_eliece_mat_perA accelConfig->TOP_eliece_mat_perA
#define ACCEL_TOP_eliece_mat_dutyA accelConfig->TOP_eliece_mat_dutyA
#define ACCEL_TOP_eliece_mat_startA accelConfig->TOP_eliece_mat_startA
#define ACCEL_TOP_eliece_mat_shiftA accelConfig->TOP_eliece_mat_shiftA
#define ACCEL_TOP_eliece_mat_incrA accelConfig->TOP_eliece_mat_incrA
#define ACCEL_TOP_eliece_mat_reverseA accelConfig->TOP_eliece_mat_reverseA
#define ACCEL_TOP_eliece_mat_extA accelConfig->TOP_eliece_mat_extA
#define ACCEL_TOP_eliece_mat_in0_wr accelConfig->TOP_eliece_mat_in0_wr
#define ACCEL_TOP_eliece_mat_iterB accelConfig->TOP_eliece_mat_iterB
#define ACCEL_TOP_eliece_mat_perB accelConfig->TOP_eliece_mat_perB
#define ACCEL_TOP_eliece_mat_dutyB accelConfig->TOP_eliece_mat_dutyB
#define ACCEL_TOP_eliece_mat_startB accelConfig->TOP_eliece_mat_startB
#define ACCEL_TOP_eliece_mat_shiftB accelConfig->TOP_eliece_mat_shiftB
#define ACCEL_TOP_eliece_mat_incrB accelConfig->TOP_eliece_mat_incrB
#define ACCEL_TOP_eliece_mat_reverseB accelConfig->TOP_eliece_mat_reverseB
#define ACCEL_TOP_eliece_row_ext_addr accelConfig->TOP_eliece_row_ext_addr
#define ACCEL_TOP_eliece_row_perA accelConfig->TOP_eliece_row_perA
#define ACCEL_TOP_eliece_row_incrA accelConfig->TOP_eliece_row_incrA
#define ACCEL_TOP_eliece_row_length accelConfig->TOP_eliece_row_length
#define ACCEL_TOP_eliece_row_pingPong accelConfig->TOP_eliece_row_pingPong
#define ACCEL_TOP_eliece_row_iterB accelConfig->TOP_eliece_row_iterB
#define ACCEL_TOP_eliece_row_perB accelConfig->TOP_eliece_row_perB
#define ACCEL_TOP_eliece_row_dutyB accelConfig->TOP_eliece_row_dutyB
#define ACCEL_TOP_eliece_row_startB accelConfig->TOP_eliece_row_startB
#define ACCEL_TOP_eliece_row_shiftB accelConfig->TOP_eliece_row_shiftB
#define ACCEL_TOP_eliece_row_incrB accelConfig->TOP_eliece_row_incrB
#define ACCEL_TOP_eliece_row_reverseB accelConfig->TOP_eliece_row_reverseB
#define ACCEL_TOP_eliece_row_extB accelConfig->TOP_eliece_row_extB
#define ACCEL_TOP_eliece_row_iter2B accelConfig->TOP_eliece_row_iter2B
#define ACCEL_TOP_eliece_row_per2B accelConfig->TOP_eliece_row_per2B
#define ACCEL_TOP_eliece_row_shift2B accelConfig->TOP_eliece_row_shift2B
#define ACCEL_TOP_eliece_row_incr2B accelConfig->TOP_eliece_row_incr2B
#define ACCEL_TOP_eliece_row_enableRead accelConfig->TOP_eliece_row_enableRead
#define ACCEL_TOP_eliece_writer_ext_addr accelConfig->TOP_eliece_writer_ext_addr
#define ACCEL_TOP_eliece_writer_perA accelConfig->TOP_eliece_writer_perA
#define ACCEL_TOP_eliece_writer_incrA accelConfig->TOP_eliece_writer_incrA
#define ACCEL_TOP_eliece_writer_length accelConfig->TOP_eliece_writer_length
#define ACCEL_TOP_eliece_writer_pingPong accelConfig->TOP_eliece_writer_pingPong
#define ACCEL_TOP_eliece_writer_iterB accelConfig->TOP_eliece_writer_iterB
#define ACCEL_TOP_eliece_writer_perB accelConfig->TOP_eliece_writer_perB
#define ACCEL_TOP_eliece_writer_dutyB accelConfig->TOP_eliece_writer_dutyB
#define ACCEL_TOP_eliece_writer_startB accelConfig->TOP_eliece_writer_startB
#define ACCEL_TOP_eliece_writer_shiftB accelConfig->TOP_eliece_writer_shiftB
#define ACCEL_TOP_eliece_writer_incrB accelConfig->TOP_eliece_writer_incrB
#define ACCEL_TOP_eliece_writer_reverseB accelConfig->TOP_eliece_writer_reverseB
#define ACCEL_TOP_eliece_writer_extB accelConfig->TOP_eliece_writer_extB
#define ACCEL_TOP_eliece_writer_iter2B accelConfig->TOP_eliece_writer_iter2B
#define ACCEL_TOP_eliece_writer_per2B accelConfig->TOP_eliece_writer_per2B
#define ACCEL_TOP_eliece_writer_shift2B accelConfig->TOP_eliece_writer_shift2B
#define ACCEL_TOP_eliece_writer_incr2B accelConfig->TOP_eliece_writer_incr2B
#define ACCEL_TOP_eliece_writer_enableWrite                                    \
  accelConfig->TOP_eliece_writer_enableWrite
#define ACCEL_TOP_eliece_mask_constant accelConfig->TOP_eliece_mask_constant

#define ACCEL_FullAESRounds_buffer0_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer0_1_1_amount
#define ACCEL_FullAESRounds_buffer1_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer1_1_1_amount
#define ACCEL_FullAESRounds_buffer2_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer2_1_1_amount
#define ACCEL_FullAESRounds_buffer3_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer3_1_1_amount
#define ACCEL_FullAESRounds_buffer4_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer4_1_1_amount
#define ACCEL_FullAESRounds_buffer5_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer5_1_1_amount
#define ACCEL_FullAESRounds_buffer6_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer6_1_1_amount
#define ACCEL_FullAESRounds_buffer7_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer7_1_1_amount
#define ACCEL_FullAESRounds_buffer8_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer8_1_1_amount
#define ACCEL_FullAESRounds_buffer9_1_1_amount                                 \
  accelStatics->FullAESRounds_buffer9_1_1_amount
#define ACCEL_FullAESRounds_buffer10_1_1_amount                                \
  accelStatics->FullAESRounds_buffer10_1_1_amount
#define ACCEL_FullAESRounds_buffer11_1_1_amount                                \
  accelStatics->FullAESRounds_buffer11_1_1_amount
#define ACCEL_FullAESRounds_buffer12_1_1_amount                                \
  accelStatics->FullAESRounds_buffer12_1_1_amount
#define ACCEL_FullAESRounds_buffer13_1_1_amount                                \
  accelStatics->FullAESRounds_buffer13_1_1_amount
#define ACCEL_FullAESRounds_buffer14_1_1_amount                                \
  accelStatics->FullAESRounds_buffer14_1_1_amount
#define ACCEL_FullAESRounds_buffer15_1_1_amount                                \
  accelStatics->FullAESRounds_buffer15_1_1_amount
#define ACCEL_Constants_mem_disabled accelStatics->Constants_mem_disabled
#define ACCEL_Constants_mem_iterA accelStatics->Constants_mem_iterA
#define ACCEL_Constants_mem_perA accelStatics->Constants_mem_perA
#define ACCEL_Constants_mem_dutyA accelStatics->Constants_mem_dutyA
#define ACCEL_Constants_mem_startA accelStatics->Constants_mem_startA
#define ACCEL_Constants_mem_shiftA accelStatics->Constants_mem_shiftA
#define ACCEL_Constants_mem_incrA accelStatics->Constants_mem_incrA
#define ACCEL_Constants_mem_reverseA accelStatics->Constants_mem_reverseA
#define ACCEL_Constants_mem_extA accelStatics->Constants_mem_extA
#define ACCEL_Constants_mem_iter2A accelStatics->Constants_mem_iter2A
#define ACCEL_Constants_mem_per2A accelStatics->Constants_mem_per2A
#define ACCEL_Constants_mem_shift2A accelStatics->Constants_mem_shift2A
#define ACCEL_Constants_mem_incr2A accelStatics->Constants_mem_incr2A

#define ACCEL_TOP_Delay0 accelConfig->TOP_Delay0
#define ACCEL_TOP_Delay1 accelConfig->TOP_Delay1
#define ACCEL_TOP_Delay2 accelConfig->TOP_Delay2
#define ACCEL_TOP_Delay3 accelConfig->TOP_Delay3
#define ACCEL_TOP_Delay4 accelConfig->TOP_Delay4
#define ACCEL_TOP_Delay5 accelConfig->TOP_Delay5
#define ACCEL_TOP_Delay6 accelConfig->TOP_Delay6
#define ACCEL_TOP_Delay7 accelConfig->TOP_Delay7
#define ACCEL_TOP_Delay8 accelConfig->TOP_Delay8
#define ACCEL_TOP_Delay9 accelConfig->TOP_Delay9
#define ACCEL_TOP_Delay10 accelConfig->TOP_Delay10
#define ACCEL_TOP_Delay11 accelConfig->TOP_Delay11
#define ACCEL_TOP_Delay12 accelConfig->TOP_Delay12
#define ACCEL_TOP_Delay13 accelConfig->TOP_Delay13
#define ACCEL_TOP_Delay14 accelConfig->TOP_Delay14
#define ACCEL_TOP_Delay15 accelConfig->TOP_Delay15
#define ACCEL_TOP_Delay16 accelConfig->TOP_Delay16
#define ACCEL_TOP_Delay17 accelConfig->TOP_Delay17
#define ACCEL_TOP_Delay18 accelConfig->TOP_Delay18
#define ACCEL_TOP_Delay19 accelConfig->TOP_Delay19
#define ACCEL_TOP_Delay20 accelConfig->TOP_Delay20
#define ACCEL_TOP_Delay21 accelConfig->TOP_Delay21
#define ACCEL_TOP_Delay22 accelConfig->TOP_Delay22
#define ACCEL_TOP_Delay23 accelConfig->TOP_Delay23
#define ACCEL_TOP_Delay24 accelConfig->TOP_Delay24
#define ACCEL_TOP_Delay25 accelConfig->TOP_Delay25
#define ACCEL_TOP_Delay26 accelConfig->TOP_Delay26
#define ACCEL_TOP_Delay27 accelConfig->TOP_Delay27
#define ACCEL_TOP_Delay28 accelConfig->TOP_Delay28
#define ACCEL_TOP_Delay29 accelConfig->TOP_Delay29
#define ACCEL_TOP_Delay30 accelConfig->TOP_Delay30
#define ACCEL_TOP_Delay31 accelConfig->TOP_Delay31
#define ACCEL_TOP_Delay32 accelConfig->TOP_Delay32
#define ACCEL_TOP_Delay33 accelConfig->TOP_Delay33
#define ACCEL_TOP_Delay34 accelConfig->TOP_Delay34
#define ACCEL_TOP_Delay35 accelConfig->TOP_Delay35
#define ACCEL_TOP_Delay36 accelConfig->TOP_Delay36
#define ACCEL_TOP_Delay37 accelConfig->TOP_Delay37
#define ACCEL_TOP_Delay38 accelConfig->TOP_Delay38
#define ACCEL_TOP_Delay39 accelConfig->TOP_Delay39
#define ACCEL_TOP_Delay40 accelConfig->TOP_Delay40
#define ACCEL_TOP_Delay41 accelConfig->TOP_Delay41
#define ACCEL_TOP_Delay42 accelConfig->TOP_Delay42
#define ACCEL_TOP_Delay43 accelConfig->TOP_Delay43
#define ACCEL_TOP_Delay44 accelConfig->TOP_Delay44
#define ACCEL_TOP_Delay45 accelConfig->TOP_Delay45
#define ACCEL_TOP_Delay46 accelConfig->TOP_Delay46
#define ACCEL_TOP_Delay47 accelConfig->TOP_Delay47
#define ACCEL_TOP_Delay48 accelConfig->TOP_Delay48
#define ACCEL_TOP_Delay49 accelConfig->TOP_Delay49
#define ACCEL_TOP_Delay50 accelConfig->TOP_Delay50
#define ACCEL_TOP_Delay51 accelConfig->TOP_Delay51
#define ACCEL_TOP_Delay52 accelConfig->TOP_Delay52
#define ACCEL_TOP_Delay53 accelConfig->TOP_Delay53
#define ACCEL_TOP_Delay54 accelConfig->TOP_Delay54
#define ACCEL_TOP_Delay55 accelConfig->TOP_Delay55
#define ACCEL_TOP_Delay56 accelConfig->TOP_Delay56
#define ACCEL_TOP_Delay57 accelConfig->TOP_Delay57
#define ACCEL_TOP_Delay58 accelConfig->TOP_Delay58
#define ACCEL_TOP_Delay59 accelConfig->TOP_Delay59
#define ACCEL_TOP_Delay60 accelConfig->TOP_Delay60
#define ACCEL_TOP_Delay61 accelConfig->TOP_Delay61
#define ACCEL_TOP_Delay62 accelConfig->TOP_Delay62
#define ACCEL_TOP_Delay63 accelConfig->TOP_Delay63
#define ACCEL_TOP_Delay64 accelConfig->TOP_Delay64
#define ACCEL_TOP_Delay65 accelConfig->TOP_Delay65
#define ACCEL_TOP_Delay66 accelConfig->TOP_Delay66
#define ACCEL_TOP_Delay67 accelConfig->TOP_Delay67
#define ACCEL_TOP_Delay68 accelConfig->TOP_Delay68
#define ACCEL_TOP_Delay69 accelConfig->TOP_Delay69
#define ACCEL_TOP_Delay70 accelConfig->TOP_Delay70
#define ACCEL_TOP_Delay71 accelConfig->TOP_Delay71
#define ACCEL_TOP_Delay72 accelConfig->TOP_Delay72
#define ACCEL_TOP_Delay73 accelConfig->TOP_Delay73
#define ACCEL_TOP_Delay74 accelConfig->TOP_Delay74
#define ACCEL_TOP_Delay75 accelConfig->TOP_Delay75
#define ACCEL_TOP_Delay76 accelConfig->TOP_Delay76
#define ACCEL_TOP_Delay77 accelConfig->TOP_Delay77
#define ACCEL_TOP_Delay78 accelConfig->TOP_Delay78
#define ACCEL_TOP_Delay79 accelConfig->TOP_Delay79
#define ACCEL_TOP_Delay80 accelConfig->TOP_Delay80
#define ACCEL_TOP_Delay81 accelConfig->TOP_Delay81
#define ACCEL_TOP_Delay82 accelConfig->TOP_Delay82
#define ACCEL_TOP_Delay83 accelConfig->TOP_Delay83
#define ACCEL_TOP_Delay84 accelConfig->TOP_Delay84
#define ACCEL_TOP_Delay85 accelConfig->TOP_Delay85
#define ACCEL_TOP_Delay86 accelConfig->TOP_Delay86

#define ACCEL_TOP_aes_state_0_currentValue                                     \
  accelState->TOP_aes_state_0_currentValue
#define ACCEL_TOP_aes_state_1_currentValue                                     \
  accelState->TOP_aes_state_1_currentValue
#define ACCEL_TOP_aes_state_2_currentValue                                     \
  accelState->TOP_aes_state_2_currentValue
#define ACCEL_TOP_aes_state_3_currentValue                                     \
  accelState->TOP_aes_state_3_currentValue
#define ACCEL_TOP_aes_state_4_currentValue                                     \
  accelState->TOP_aes_state_4_currentValue
#define ACCEL_TOP_aes_state_5_currentValue                                     \
  accelState->TOP_aes_state_5_currentValue
#define ACCEL_TOP_aes_state_6_currentValue                                     \
  accelState->TOP_aes_state_6_currentValue
#define ACCEL_TOP_aes_state_7_currentValue                                     \
  accelState->TOP_aes_state_7_currentValue
#define ACCEL_TOP_aes_state_8_currentValue                                     \
  accelState->TOP_aes_state_8_currentValue
#define ACCEL_TOP_aes_state_9_currentValue                                     \
  accelState->TOP_aes_state_9_currentValue
#define ACCEL_TOP_aes_state_10_currentValue                                    \
  accelState->TOP_aes_state_10_currentValue
#define ACCEL_TOP_aes_state_11_currentValue                                    \
  accelState->TOP_aes_state_11_currentValue
#define ACCEL_TOP_aes_state_12_currentValue                                    \
  accelState->TOP_aes_state_12_currentValue
#define ACCEL_TOP_aes_state_13_currentValue                                    \
  accelState->TOP_aes_state_13_currentValue
#define ACCEL_TOP_aes_state_14_currentValue                                    \
  accelState->TOP_aes_state_14_currentValue
#define ACCEL_TOP_aes_state_15_currentValue                                    \
  accelState->TOP_aes_state_15_currentValue
#define ACCEL_TOP_aes_lastResult_0_currentValue                                \
  accelState->TOP_aes_lastResult_0_currentValue
#define ACCEL_TOP_aes_lastResult_1_currentValue                                \
  accelState->TOP_aes_lastResult_1_currentValue
#define ACCEL_TOP_aes_lastResult_2_currentValue                                \
  accelState->TOP_aes_lastResult_2_currentValue
#define ACCEL_TOP_aes_lastResult_3_currentValue                                \
  accelState->TOP_aes_lastResult_3_currentValue
#define ACCEL_TOP_aes_lastResult_4_currentValue                                \
  accelState->TOP_aes_lastResult_4_currentValue
#define ACCEL_TOP_aes_lastResult_5_currentValue                                \
  accelState->TOP_aes_lastResult_5_currentValue
#define ACCEL_TOP_aes_lastResult_6_currentValue                                \
  accelState->TOP_aes_lastResult_6_currentValue
#define ACCEL_TOP_aes_lastResult_7_currentValue                                \
  accelState->TOP_aes_lastResult_7_currentValue
#define ACCEL_TOP_aes_lastResult_8_currentValue                                \
  accelState->TOP_aes_lastResult_8_currentValue
#define ACCEL_TOP_aes_lastResult_9_currentValue                                \
  accelState->TOP_aes_lastResult_9_currentValue
#define ACCEL_TOP_aes_lastResult_10_currentValue                               \
  accelState->TOP_aes_lastResult_10_currentValue
#define ACCEL_TOP_aes_lastResult_11_currentValue                               \
  accelState->TOP_aes_lastResult_11_currentValue
#define ACCEL_TOP_aes_lastResult_12_currentValue                               \
  accelState->TOP_aes_lastResult_12_currentValue
#define ACCEL_TOP_aes_lastResult_13_currentValue                               \
  accelState->TOP_aes_lastResult_13_currentValue
#define ACCEL_TOP_aes_lastResult_14_currentValue                               \
  accelState->TOP_aes_lastResult_14_currentValue
#define ACCEL_TOP_aes_lastResult_15_currentValue                               \
  accelState->TOP_aes_lastResult_15_currentValue
#define ACCEL_TOP_aes_lastValToAdd_0_currentValue                              \
  accelState->TOP_aes_lastValToAdd_0_currentValue
#define ACCEL_TOP_aes_lastValToAdd_1_currentValue                              \
  accelState->TOP_aes_lastValToAdd_1_currentValue
#define ACCEL_TOP_aes_lastValToAdd_2_currentValue                              \
  accelState->TOP_aes_lastValToAdd_2_currentValue
#define ACCEL_TOP_aes_lastValToAdd_3_currentValue                              \
  accelState->TOP_aes_lastValToAdd_3_currentValue
#define ACCEL_TOP_aes_lastValToAdd_4_currentValue                              \
  accelState->TOP_aes_lastValToAdd_4_currentValue
#define ACCEL_TOP_aes_lastValToAdd_5_currentValue                              \
  accelState->TOP_aes_lastValToAdd_5_currentValue
#define ACCEL_TOP_aes_lastValToAdd_6_currentValue                              \
  accelState->TOP_aes_lastValToAdd_6_currentValue
#define ACCEL_TOP_aes_lastValToAdd_7_currentValue                              \
  accelState->TOP_aes_lastValToAdd_7_currentValue
#define ACCEL_TOP_aes_lastValToAdd_8_currentValue                              \
  accelState->TOP_aes_lastValToAdd_8_currentValue
#define ACCEL_TOP_aes_lastValToAdd_9_currentValue                              \
  accelState->TOP_aes_lastValToAdd_9_currentValue
#define ACCEL_TOP_aes_lastValToAdd_10_currentValue                             \
  accelState->TOP_aes_lastValToAdd_10_currentValue
#define ACCEL_TOP_aes_lastValToAdd_11_currentValue                             \
  accelState->TOP_aes_lastValToAdd_11_currentValue
#define ACCEL_TOP_aes_lastValToAdd_12_currentValue                             \
  accelState->TOP_aes_lastValToAdd_12_currentValue
#define ACCEL_TOP_aes_lastValToAdd_13_currentValue                             \
  accelState->TOP_aes_lastValToAdd_13_currentValue
#define ACCEL_TOP_aes_lastValToAdd_14_currentValue                             \
  accelState->TOP_aes_lastValToAdd_14_currentValue
#define ACCEL_TOP_aes_lastValToAdd_15_currentValue                             \
  accelState->TOP_aes_lastValToAdd_15_currentValue
#define ACCEL_TOP_sha_State_s_0_reg_currentValue                               \
  accelState->TOP_sha_State_s_0_reg_currentValue
#define ACCEL_TOP_sha_State_s_1_reg_currentValue                               \
  accelState->TOP_sha_State_s_1_reg_currentValue
#define ACCEL_TOP_sha_State_s_2_reg_currentValue                               \
  accelState->TOP_sha_State_s_2_reg_currentValue
#define ACCEL_TOP_sha_State_s_3_reg_currentValue                               \
  accelState->TOP_sha_State_s_3_reg_currentValue
#define ACCEL_TOP_sha_State_s_4_reg_currentValue                               \
  accelState->TOP_sha_State_s_4_reg_currentValue
#define ACCEL_TOP_sha_State_s_5_reg_currentValue                               \
  accelState->TOP_sha_State_s_5_reg_currentValue
#define ACCEL_TOP_sha_State_s_6_reg_currentValue                               \
  accelState->TOP_sha_State_s_6_reg_currentValue
#define ACCEL_TOP_sha_State_s_7_reg_currentValue                               \
  accelState->TOP_sha_State_s_7_reg_currentValue

static unsigned int delayBuffer_0[] = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};
static unsigned int delayBuffer_1[] = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x5,  0x5,  0x5,  0x5,  0x5, 0x5, 0x5, 0x5, 0x5,  0x5,
    0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5, 0x5, 0x5, 0x5, 0x5,  0x5,
    0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5, 0x5, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};
static unsigned int delayBuffer_2[] = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};
static unsigned int delayBuffer_3[] = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};
static unsigned int delayBuffer_4[] = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x5,  0x5,  0x5,  0x5,  0x5, 0x5, 0x5, 0x5, 0x5,  0x5,
    0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5, 0x5, 0x5, 0x5, 0x5,  0x5,
    0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5,  0x5, 0x5, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};
static unsigned int delayBuffer_5[] = {
    0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6,  0x6, 0x6, 0x6, 0x6, 0x6,  0x6,
    0x6,  0x6,  0x6,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x2, 0x2, 0x2,  0x2,
    0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2,  0x2, 0x2, 0x0, 0x0, 0x0,  0x0,
    0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0x0, 0x0,  0x0,
    0x2,  0x12, 0x23, 0x34, 0x1,  0x12, 0x23, 0x0, 0x0, 0x0, 0x0, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x3,  0x0, 0x3};

static unsigned int *delayBuffers[] = {delayBuffer_0, delayBuffer_1,
                                       delayBuffer_2, delayBuffer_3,
                                       delayBuffer_4, delayBuffer_5};

typedef enum {
  MergeType_AESFirstAdd = 0,
  MergeType_AESRound = 1,
  MergeType_AESLastRound = 2,
  MergeType_AESInvFirstAdd = 3,
  MergeType_AESInvRound = 4,
  MergeType_AESInvLastRound = 5
} MergeType;

#ifdef __cplusplus
extern "C" {
#endif

static inline void OnlyActivateMergedAccelerator(MergeType type) {
  static int lastLoaded = -1;
  int asInt = (int)type;

  if (lastLoaded == asInt) {
    return;
  }
  lastLoaded = asInt;

  ACCEL_TOP_aes_round_versat_merge_mux_63_sel = asInt;
}

static inline void ActivateMergedAccelerator(MergeType type) {
  static int lastLoaded = -1;
  int asInt = (int)type;

  if (lastLoaded == asInt) {
    return;
  }
  lastLoaded = asInt;

  ACCEL_TOP_aes_round_versat_merge_mux_63_sel = asInt;
  VersatLoadDelay(delayBuffers[asInt]);
}

#ifdef __cplusplus
}
#endif

#endif // INCLUDED_VERSAT_ACCELERATOR_HEADER
