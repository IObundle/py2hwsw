#pragma once

#include <stdbool.h>
#include <stdint.h>

// These buffers are needed to load data into and from the versat accelerator.
// In order to avoid unneaded copies, we expose their interface to the
// programmer. Each time a buffer is returned by a function, that buffer is the
// next valid buffer that the programmer is allowed to use while the previous
// buffer is invalid.

typedef struct {
  uint8_t
      *mem; // Not guaranteed to be byte aligned. It's intended to store bytes
  int size;
  int maxSize;
} VersatBuffer;

// Each Begin/End represents a pair of functions that need to be called before
// calling other functions related to the crypto algorithm being used. Must call
// End before calling another Begin, unless calling Begin for the first time.

// SHA
bool InitVersat(int maxBlockSize); // There is a minimum size of 64 bytes

// To optimize performance try to send multiple buffers instead of a single
// buffer even if data fits into a single buffer. Versat can process data while
// CPU is filling the next buffer.

VersatBuffer *BeginSHA(); // Returns one buffer that can be used to load data.

// If buffer is not disivible by 64 bytes, prints an error.
VersatBuffer *
ProcessSHA(VersatBuffer *input); // Returns a valid buffer that can be used by
                                 // program to load more data
void EndSHA(VersatBuffer *input, uint8_t digest[32]); // Fills digest

#define AES_KEY_SIZE 16
#define AES_256_KEY_SIZE 32
#define AES_MAX_KEY_SIZE 32

#define AES_BLK_SIZE 16
#define AES_256_BLK_SIZE 16
#define AES_MAX_BLK_SIZE 16

#define AES_IV_SIZE 16
#define AES_256_IV_SIZE 16
#define AES_MAX_IV_SIZE 16

VersatBuffer *BeginAES_ECB(uint8_t *key, bool is256, bool isDecryption);
VersatBuffer *BeginAES_CBC(uint8_t *key, uint8_t *iv, bool is256,
                           bool isDecryption);
VersatBuffer *
BeginAES_CTR(uint8_t *key, uint8_t *initialCounter,
             bool is256); // Encryption and decryption are the same

VersatBuffer *
ProcessAES(VersatBuffer *input, uint8_t *output,
           /* out */ int *outputOffset); // Must make sure that output is
                                         // capable of storing data

// Returns total size of processed file. Important for decryption.
// For decryption outputOffset returns the actual amount of data removing the
// padding.
int EndAES(VersatBuffer *input, uint8_t *output,
           /* out */ int *outputOffset); // Must make sure that output is
                                         // capable of storing data
