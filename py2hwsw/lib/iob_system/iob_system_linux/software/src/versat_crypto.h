#ifndef INCLUDED_SHA_AES
#define INCLUDED_SHA_AES

#include "stddef.h"
#include "stdint.h"

// Must call versat_init before calling any function from here

// Each Init... function must be called before calling the corresponding Versat*
// function. This function prepares the accelerator for the specific algorithm
// Only need to call init once per multiple calls of Versat*.
// When changing algorithms, need to call the init function again even if called
// previously.

void InitVersatSHA();
void VersatSHA(uint8_t *out, const uint8_t *in, size_t inlen);

// AES Sizes (bytes)
#define AES_BLK_SIZE (16)
#define AES_KEY_SIZE (32)

void InitVersatAES();
void VersatAES();
void InitAES();

// McEliece
int VersatMcEliece(unsigned char *pk, unsigned char *sk);

// Simple function to convert result into plain text hexadecimal number and vice
// versa. Useful for testing
char *GetHexadecimal(const char *text, char *buffer, int str_size);
int HexStringToHex(char *buffer, const char *str);

#endif // INCLUDED_SHA_AES