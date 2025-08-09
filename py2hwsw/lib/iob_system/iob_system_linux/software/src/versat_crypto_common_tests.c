/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "versat_crypto_tests.h"

#include "stdbool.h"

#include "iob-eth.h"
#include "iob-uart16550.h"
#include "printf.h"

#include "crypto/aes.h"
#include "crypto/sha2.h"
#include "versat_accel.h"
#include "versat_crypto.h"

#include "arena.h"

#include "string.h"

void versat_init(int);
void AES_ECB256(uint8_t *key, uint8_t *data, uint8_t *encrypted);

static Arena globalArenaInst = {};

void InitializeCryptoSide(int versatAddress) {
  versat_init(versatAddress);
  ConfigEnableDMA(true);

  globalArenaInst = InitArena(
      16 * 1024 * 1024); // 16 megabytes should suffice. Arena memory used by
                         // crypto algorithms, both by software and Versat impl.
  globalArena = &globalArenaInst;
}

char *SearchAndAdvance(char *ptr, String str) {
  char *firstChar = strstr(ptr, str.str);
  if (firstChar == NULL) {
    return NULL;
  }

  char *advance = firstChar + str.size;
  return advance;
}

int ParseNumber(char *ptr) {
  int count = 0;

  while (ptr != NULL) {
    char ch = *ptr;

    if (ch >= '0' && ch <= '9') {
      count *= 10;
      count += ch - '0';
      ptr += 1;
      continue;
    }

    break;
  }

  return count;
}

TestState VersatCommonSHATests(String content) {
  TestState result = {};

  int mark = MarkArena(globalArena);

  int start = GetTime();
  InitVersatSHA();
  int end = GetTime();

  result.initTime = end - start;

  static const int HASH_SIZE = (256 / 8);

  char *ptr = content.str;
  while (1) {
    int testMark = MarkArena(globalArena);

    ptr = SearchAndAdvance(ptr, STRING("LEN = "));
    if (ptr == NULL) {
      break;
    }

    int len = ParseNumber(ptr);

    ptr = SearchAndAdvance(ptr, STRING("MSG = "));
    if (ptr ==
        NULL) { // Note: It's only a error if any check after the first one
                // fails, because we are assuming that if the first passes then
                // that must mean that the rest should pass as well.
      result.earlyExit = 1;
      break;
    }

    unsigned char *message = PushArray(globalArena, len, unsigned char);
    int bytes = HexStringToHex(message, ptr);

    ptr = SearchAndAdvance(ptr, STRING("MD = "));
    if (ptr == NULL) {
      result.earlyExit = 1;
      break;
    }

    char *expected = ptr;

    unsigned char versat_digest[256];
    unsigned char software_digest[256];
    for (int i = 0; i < 256; i++) {
      versat_digest[i] = 0;
      software_digest[i] = 0;
    }

    int start = GetTime();
    VersatSHA(versat_digest, message, len / 8);
    int middle = GetTime();
    sha256(software_digest, message, len / 8);
    int end = GetTime();

    bool good = true;
    for (int i = 0; i < 256; i++) {
      if (versat_digest[i] != software_digest[i]) {
        good = false;
        break;
      }
    }

    if (good) {
      result.versatTimeAccum += middle - start;
      result.softwareTimeAccum += end - middle;
      result.goodTests += 1;
    } else {
      char versat_buffer[2048];
      char software_buffer[2048];
      GetHexadecimal((char *)versat_digest, versat_buffer, HASH_SIZE);
      GetHexadecimal((char *)software_digest, software_buffer, HASH_SIZE);

      printf("SHA Test %02d: Error\n", result.tests);
      printf("  Expected: %.64s\n", expected);
      printf("  Software: %s\n", software_buffer);
      printf("  Versat:   %s\n", versat_buffer);
    }

    result.tests += 1;
    PopArena(globalArena, testMark);
  }

  PopArena(globalArena, mark);

  return result;
}

TestState VersatCommonAESTests(String content) {
  TestState result = {};

  int mark = MarkArena(globalArena);

  InitVersatAES();
  InitAES();

  char *ptr = content.str;
  while (1) {
    int testMark = MarkArena(globalArena);

    ptr = SearchAndAdvance(ptr, STRING("COUNT = "));
    if (ptr == NULL) {
      break;
    }

    int count = ParseNumber(ptr);

    ptr = SearchAndAdvance(ptr, STRING("KEY = "));
    if (ptr == NULL) {
      result.earlyExit = 1;
      break;
    }

    unsigned char *key = PushArray(globalArena, 32 + 1, unsigned char);
    HexStringToHex(key, ptr);

    ptr = SearchAndAdvance(ptr, STRING("PLAINTEXT = "));
    if (ptr == NULL) {
      result.earlyExit = 1;
      break;
    }

    unsigned char *plain = PushArray(globalArena, 16 + 1, unsigned char);
    HexStringToHex(plain, ptr);

    ptr = SearchAndAdvance(ptr, STRING("CIPHERTEXT = "));
    if (ptr == NULL) {
      result.earlyExit = 1;
      break;
    }

    char *cypher = ptr;

    uint8_t versat_result[AES_BLK_SIZE] = {};
    uint8_t software_result[AES_BLK_SIZE] = {};

    int start = GetTime();
    AES_ECB256(key, plain, versat_result);
    int middle = GetTime();

    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);
    memcpy(software_result, plain, AES_BLK_SIZE);
    AES_ECB_encrypt(&ctx, software_result);
    int end = GetTime();

    bool good = true;
    for (int i = 0; i < AES_BLK_SIZE; i++) {
      if (versat_result[i] != software_result[i]) {
        good = false;
        break;
      }
    }

    if (good) {
      result.versatTimeAccum += middle - start;
      result.softwareTimeAccum += end - middle;
      result.goodTests += 1;
    } else {
      char versat_buffer[2048];
      char software_buffer[2048];
      GetHexadecimal((char *)versat_result, versat_buffer, AES_BLK_SIZE);
      GetHexadecimal((char *)software_result, software_buffer, AES_BLK_SIZE);

      printf("AES Test %02d: Error\n", result.tests);
      printf("  Expected: %.32s\n", cypher);
      printf("  Software: %s\n", software_buffer);
      printf("  Versat:   %s\n", versat_buffer);
    }

    result.tests += 1;
    PopArena(globalArena, testMark);
  }

  PopArena(globalArena, mark);

  return result;
}
