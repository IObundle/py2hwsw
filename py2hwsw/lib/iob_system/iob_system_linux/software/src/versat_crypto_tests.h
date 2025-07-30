#pragma once

#include <stdint.h>
#include <string.h>

typedef struct {
  char *str;
  int size;
} String;

#define STRING(str)                                                            \
  (String) { str, strlen(str) }

typedef struct {
  int initTime;
  int tests;
  int goodTests;
  int versatTimeAccum;
  int softwareTimeAccum;
  int earlyExit;
} TestState;

// Functions needed by crypto side but implemented elsewhere
// Somewhere someone must implement such functions so that we can time the
// algorithms relative performance and receive the testcases by ethernet
int GetTime();
uint32_t uart_recvfile_ethernet(const char *file_name);

// Misc Functions used by tests to parse KAT file
char *SearchAndAdvance(char *ptr, String str);
int ParseNumber(char *ptr);

void InitializeCryptoSide(int versatAddress);

// Returns zero if pass, nonzero otherwise
int VersatSimpleSHATests();
int VersatSimpleAESTests();

int VersatSHATests();
int VersatAESTests();
int VersatMcElieceTests();

TestState VersatCommonSHATests(String content);
TestState VersatCommonAESTests(String content);
