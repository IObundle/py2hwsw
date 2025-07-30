#include <fcntl.h>
#include <unistd.h>

#include <argp.h>
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "arena.h"
#include "versatCrypto.h"
#include "versat_accel.h"

#include "api.h"

#include "aes.h"
#include "sha2.h"

#undef ARRAY_SIZE
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof(arr[0]))

typedef struct {
  char *str;
  int size;
} String;

#define STRING(str)                                                            \
  (String) { str, strlen(str) }

void nist_kat_init(unsigned char *entropy_input,
                   unsigned char *personalization_string,
                   int security_strength);

void clear_cache() {
  // Delay to ensure all data is written to memory
  for (unsigned int i = 0; i < 10; i++)
    asm volatile("nop");
  // Flush VexRiscv CPU internal cache
  asm volatile(".word 0x500F" ::: "memory");
}

static char HexToInt(char ch) {
  if ('0' <= ch && ch <= '9') {
    return (ch - '0');
  } else if ('a' <= ch && ch <= 'f') {
    return ch - 'a' + 10;
  } else if ('A' <= ch && ch <= 'F') {
    return ch - 'A' + 10;
  } else {
    return 0x7f;
  }
}

// Make sure that buffer is capable of storing the whole thing. Returns number
// of bytes inserted
int HexStringToHex(char *buffer, const char *str) {
  int inserted = 0;
  for (int i = 0;; i += 2) {
    char upper = HexToInt(str[i]);
    char lower = HexToInt(str[i + 1]);

    if (upper >= 16 || lower >= 16) {
      if (upper < 16) { // Upper is good but lower is not
        printf("Warning: HexString was not divisible by 2\n");
      }
      break;
    }

    buffer[inserted++] = upper * 16 + lower;
  }

  return inserted;
}

char GetHexadecimalChar(unsigned char value) {
  if (value < 10) {
    return '0' + value;
  } else {
    return 'A' + (value - 10);
  }
}

char *GetHexadecimal(const char *text, char *buffer, int str_size) {
  int i = 0;
  unsigned char *view = (unsigned char *)text;
  for (; i < str_size; i++) {
    buffer[i * 2] = GetHexadecimalChar(view[i] / 16);
    buffer[i * 2 + 1] = GetHexadecimalChar(view[i] % 16);
  }

  buffer[i * 2] = '\0';

  return buffer;
}

int VersatMcEliece(unsigned char *pk, unsigned char *sk, Arena *temp);

typedef struct {
  const char *algorithm;
  int maxBlockSize;

  const char *key;
  const char *iv;
  const char *inputFile;
  const char *outputFile;
  const char *privateFile;
  const char *publicFile;
  const char *seed;

  bool encrypt;
  bool decrypt;
  bool software;
} Options;

error_t parse(int key, char *arg, struct argp_state *state) {
  Options *options = (Options *)state->input;

  switch (key) {
  case ARGP_KEY_INIT:
    break;
  case ARGP_KEY_SUCCESS:
    break;
  case ARGP_KEY_ERROR:
    break;
  case ARGP_KEY_ARGS:
    break;
  case ARGP_KEY_END:
    break;
  case ARGP_KEY_NO_ARGS:
    break;
  case ARGP_KEY_FINI:
    break;

  case ARGP_KEY_ARG:
    options->algorithm = arg;
    break;
  case 'e':
    options->encrypt = true;
    break;
  case 'd':
    options->decrypt = true;
    break;
  case 't':
    options->software = true;
    break;
  case 'b':
    options->maxBlockSize = atoi(arg);
    break; // Not safe but this is more of a test program
  case 'k':
    options->key = arg;
    break;
  case 'v':
    options->iv = arg;
    break;
  case 'i':
    options->inputFile = arg;
    break;
  case 'o':
    options->outputFile = arg;
    break;
  case 'P':
    options->privateFile = arg;
    break;
  case 'p':
    options->publicFile = arg;
    break;
  case 's':
    options->seed = arg;
    break;
  default:
    return ARGP_ERR_UNKNOWN;
  }

  return 0;
}

typedef enum {
  AlgorithmType_SHA,
  AlgorithmType_AES,
  AlgorithmType_McEliece
} AlgorithmType;

typedef enum { AESType_CBC, AESType_ECB, AESType_CTR } AESType;

typedef enum {
  McElieceType_GEN,
  McElieceType_ENC,
  McElieceType_DEC
} McElieceType;

bool CheckCorrectHex(const char *str, int expectedLength) {
  for (int i = 0; i < expectedLength; i++) {
    if (str[i] == '\0') {
      return false;
    }
    bool check =
        ((str[i] >= '0' && str[i] <= '9') || (str[i] >= 'a' && str[i] <= 'f') ||
         (str[i] >= 'A' && str[i] <= 'F'));

    if (!check) {
      return false;
    }
  }

  return (str[expectedLength] == '\0');
}

bool FillBufferFromFile(VersatBuffer *buffer, int fileFd) {
  while (1) {
    ssize_t bytesRead = read(fileFd, buffer->mem + buffer->size,
                             buffer->maxSize - buffer->size);

    if (bytesRead == -1) {
      printf("There was an error reading the file\n");
      exit(-1);
    }

    if (bytesRead == 0) {
      return true;
    }

    buffer->size += bytesRead;

    if (bytesRead >= buffer->size) {
      return false;
    }
  }
}

// Returns -1 if read exactly memSize, otherwise returns the actual amount of
// mem read (signaling end of file)
int FillMemFromFile(void *mem, int memSize, int fileFd) {
  int amountRead = 0;
  while (1) {
    ssize_t bytesRead = read(fileFd, mem + amountRead, memSize - amountRead);

    if (bytesRead == -1) {
      printf("There was an error reading the file\n");
      exit(-1);
    }

    if (bytesRead == 0) {
      return amountRead;
    }

    amountRead += bytesRead;

    if (bytesRead >= memSize) {
      return -1;
    }
  }
}

int OpenReadFile(const char *filepath) {
  int fd = open(filepath, O_RDONLY, 0);

  if (fd == -1) {
    printf("Problem opening file: %s\n", filepath);
    exit(-1);
  }

  return fd;
}

int OpenWriteFile(const char *filepath) {
  int fd =
      open(filepath, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);

  if (fd == -1) {
    printf("Problem opening file: %s\n", filepath);
    exit(-1);
  }

  return fd;
}

int main(int argc, char **argv) {
  const struct argp_option options[] = {
      {.name = NULL,
       .key = 0,
       .arg = NULL,
       .flags = 0,
       .doc = "AES:",
       .group = 0},
      {.name = "Encrypt",
       .key = 'e',
       .arg = NULL,
       .flags = 0,
       .doc = "",
       .group = 0},
      {.name = "Decrypt",
       .key = 'd',
       .arg = NULL,
       .flags = 0,
       .doc = "",
       .group = 0},
      {.name = "Key",
       .key = 'k',
       .arg = "hex",
       .flags = 0,
       .doc = "Key used for AES in Hex (32 chars for 128, 64 chars for 256)",
       .group = 0},
      {.name = "IV",
       .key = 'v',
       .arg = "hex",
       .flags = 0,
       .doc = "IV or initial counter for AES in Hex (32 chars)",
       .group = 0},
      {.name = NULL,
       .key = 0,
       .arg = NULL,
       .flags = 0,
       .doc = "McEliece:",
       .group = 0},
      {.name = "PrivateFile",
       .key = 'P',
       .arg = "name",
       .flags = 0,
       .doc = "File to output private key or to input private key",
       .group = 0},
      {.name = "PublicFile",
       .key = 'p',
       .arg = "name",
       .flags = 0,
       .doc = "File to output public key or to input public key",
       .group = 0},
      {.name = "Seed",
       .key = 's',
       .arg = "hex",
       .flags = 0,
       .doc = "Seed for McEliece in Hex (96 chars)",
       .group = 0},
      {.name = NULL,
       .key = 0,
       .arg = NULL,
       .flags = 0,
       .doc = "Input/Output:",
       .group = 0},
      {.name = "InputFile",
       .key = 'i',
       .arg = "name",
       .flags = 0,
       .doc = "",
       .group = 0},
      {.name = "OutputFile",
       .key = 'o',
       .arg = "name",
       .flags = 0,
       .doc = "",
       .group = 0},
      {.name = "NoVersat",
       .key = 't',
       .arg = NULL,
       .flags = 0,
       .doc = "",
       .group = 0},
      {.name = "MaxBlockSize",
       .key = 'b',
       .arg = "int",
       .flags = 0,
       .doc = "",
       .group = 0},
      {0}};

  const struct argp parser = {
      .options = options,
      .parser = parse,
      .args_doc = "ALGORITHM",
      .doc =
          "\nSupported algorithms: SHA256 AES-128-CBC AES-128-ECB AES-128-CTR "
          "AES-256-CBC AES-256-ECB AES-256-CTR McEliece\n\nSHA outputs digest "
          "on terminal, no output file used\n\nFor McEliece the session key is "
          "outputted on the terminal while output file stores the chipertext",
      .children = NULL,
      .help_filter = NULL,
      .argp_domain = NULL};

  Options OPT = {};
  OPT.maxBlockSize = 1024 * 1024;

  int index = 0;
  error_t result = argp_parse(&parser, argc, argv, 0, &index, &OPT);

  if (!OPT.algorithm) {
    printf("Need to specify an algorithm\n");
    return -1;
  }

  AlgorithmType algorithm;
  AESType type;
  bool is256 = false;
  if (strcmp(OPT.algorithm, "SHA256") == 0) {
    algorithm = AlgorithmType_SHA;
  } else if (strcmp(OPT.algorithm, "AES-128-CBC") == 0) {
    algorithm = AlgorithmType_AES;
    type = AESType_CBC;
  } else if (strcmp(OPT.algorithm, "AES-256-CBC") == 0) {
    algorithm = AlgorithmType_AES;
    type = AESType_CBC;
    is256 = true;
  } else if (strcmp(OPT.algorithm, "AES-128-CTR") == 0) {
    algorithm = AlgorithmType_AES;
    type = AESType_CTR;
  } else if (strcmp(OPT.algorithm, "AES-256-CTR") == 0) {
    algorithm = AlgorithmType_AES;
    type = AESType_CTR;
    is256 = true;
  } else if (strcmp(OPT.algorithm, "AES-128-ECB") == 0) {
    algorithm = AlgorithmType_AES;
    type = AESType_ECB;
  } else if (strcmp(OPT.algorithm, "AES-256-ECB") == 0) {
    algorithm = AlgorithmType_AES;
    type = AESType_ECB;
    is256 = true;
  } else if (strcmp(OPT.algorithm, "McEliece") == 0) {
    algorithm = AlgorithmType_McEliece;
  } else {
    printf("Algorithm '%s' not supported\n", OPT.algorithm);
    return -1;
  }

  McElieceType mcType;
  switch (algorithm) {
  case AlgorithmType_SHA: {
    if (OPT.inputFile == NULL) {
      printf("Need input file for SHA\n");
      return -1;
    }
  } break;
  case AlgorithmType_McEliece: {
    if (OPT.privateFile == NULL && OPT.publicFile == NULL) {
      printf("Need either privateFile, publicFile or both for McEliece\n");
      return -1;
    }

    if (OPT.privateFile && OPT.publicFile) {
      mcType = McElieceType_GEN;
    } else if (OPT.publicFile) {
      mcType = McElieceType_ENC;
    } else if (OPT.privateFile) {
      mcType = McElieceType_DEC;
    }

    if (mcType == McElieceType_ENC && OPT.outputFile == NULL) {
      printf("McEliece needs an output file when performing encapsulation\n");
      return -1;
    }

    if (mcType == McElieceType_DEC && OPT.inputFile == NULL) {
      printf("McEliece needs an input file when performing decapsulation\n");
      return -1;
    }

    if (OPT.seed == NULL) {
      printf("Need seed for McEliece\n");
      return -1;
    }

    if (!CheckCorrectHex(OPT.seed, 96)) {
      printf("McEliece seed needs to be 96 hexadecimal characters\n");
      return -1;
    }
  } break;
  case AlgorithmType_AES: {
    if (OPT.inputFile == NULL || OPT.outputFile == NULL) {
      printf("Need both input file and output file for AES\n");
      return -1;
    }

    if (OPT.key == NULL) {
      printf("Need key for AES\n");
      return -1;
    }

    if (is256) {
      if (!CheckCorrectHex(OPT.key, 64)) {
        printf("AES key needs to be 64 hexadecimal characters\n");
        return -1;
      }
    } else if (!CheckCorrectHex(OPT.key, 32)) {
      printf("AES key needs to be 32 hexadecimal characters\n");
      return -1;
    }

    if (type == AESType_CTR || type == AESType_CBC) {
      if (OPT.iv == NULL) {
        printf("Need IV for selected AES algorithm\n");
        return -1;
      }

      if (!CheckCorrectHex(OPT.iv, 32)) {
        printf("IV needs to be an hexadecimal number with 32 characters\n");
        return -1;
      }
    }

    if (OPT.encrypt == false && OPT.decrypt == false) {
      printf("Need either a encrypt or a decrypt option set for AES\n");
      return -1;
    }
    if (OPT.encrypt == true && OPT.decrypt == true) {
      printf("Cannot have both encrypt and decrypt options set\n");
      return -1;
    }
  } break;
  }

  if (!InitVersat(OPT.maxBlockSize)) {
    return -1;
  }
  ConfigEnableDMA(false);

  Arena testInst = InitArena(4 * 1024 * 1024); // 4 Megabytes
  Arena *test = &testInst;

  globalArena = test; // Global arena is only used for allocations that are 100%
                      // stack based. There should not be any conflict having
                      // test and global acting the same

  int inputFd = -1;
  int outputFd = -1;

  int privateFd = -1;
  int publicFd = -1;

  if (algorithm == AlgorithmType_AES || algorithm == AlgorithmType_SHA ||
      (algorithm == AlgorithmType_McEliece && mcType == McElieceType_DEC)) {
    inputFd = OpenReadFile(OPT.inputFile);
  }

  if (algorithm == AlgorithmType_AES ||
      (algorithm == AlgorithmType_McEliece && mcType == McElieceType_ENC)) {
    outputFd = OpenWriteFile(OPT.outputFile);
  }

  if (algorithm == AlgorithmType_McEliece) {
    switch (mcType) {
    case McElieceType_GEN: {
      privateFd = OpenWriteFile(OPT.privateFile);
      publicFd = OpenWriteFile(OPT.publicFile);
    } break;
    case McElieceType_ENC: {
      publicFd = OpenReadFile(OPT.publicFile);
    } break;
    case McElieceType_DEC: {
      privateFd = OpenReadFile(OPT.privateFile);
    } break;
    }
  }

  switch (algorithm) {
  case AlgorithmType_SHA: {
    uint8_t *digest = PushArray(test, 32 + 1, uint8_t);
    uint8_t *digestBuffer = PushArray(test, 64 + 1, uint8_t);

    if (OPT.software) {
      sha256ctx context;
      sha256_inc_init(&context);

      assert(OPT.maxBlockSize % 64 == 0);

      uint8_t *buffer = PushArray(test, OPT.maxBlockSize + 1, uint8_t);

      while (1) {
        int amount = FillMemFromFile(buffer, OPT.maxBlockSize, inputFd);
        if (amount >= 0) {
          sha256_inc_finalize(digest, &context, buffer, amount);
          break;
        } else {
          sha256_inc_blocks(&context, buffer, OPT.maxBlockSize);
        }
      }
    } else {
      VersatBuffer *buffer = BeginSHA();

      while (1) {
        if (FillBufferFromFile(buffer, inputFd)) {
          EndSHA(buffer, digest);
          break;
        } else {
          buffer = ProcessSHA(buffer);
        }
      }
    }

    char *res = GetHexadecimal(digest, digestBuffer, 32);

    digestBuffer[64] = '\0';

    printf("%s\n", res);
  } break;
  case AlgorithmType_AES: {
    uint8_t key[AES_MAX_KEY_SIZE] = {};
    uint8_t ivOrCounter[AES_MAX_BLK_SIZE] = {};
    HexStringToHex(key, OPT.key);

    if (OPT.software) {
      // Only implement the 256 version of ECB. Baremetal tests correctness, we
      // want to test performance.
      aes256ctx ctx;

      aes256_ecb_keyexp(&ctx, key);

      uint8_t *input = PushArray(test, OPT.maxBlockSize + 1, uint8_t);
      uint8_t *output = PushArray(test, OPT.maxBlockSize + 1, uint8_t);
      while (1) {
        int amount = FillMemFromFile(input, OPT.maxBlockSize, inputFd);

        bool end = false;
        if (amount >= 0) {
          assert(amount % 16 == 0);
          end = true;
        }

        aes256_ecb(output, input, OPT.maxBlockSize / 16, &ctx);
        ssize_t res = write(outputFd, output, OPT.maxBlockSize);

        if (res < 0) {
          printf("There was an error writing to the file\n");
          return -1;
        }

        if (end) {
          break;
        }
      }
    } else {
      VersatBuffer *buffer = NULL;

      switch (type) {
      case AESType_ECB: {
        buffer = BeginAES_ECB(key, is256, OPT.decrypt);
      } break;
      case AESType_CTR: {
        HexStringToHex(ivOrCounter, OPT.iv);
        buffer = BeginAES_CTR(key, ivOrCounter, is256);
      } break;
      case AESType_CBC: {
        HexStringToHex(ivOrCounter, OPT.iv);
        buffer = BeginAES_CBC(key, ivOrCounter, is256, OPT.decrypt);
      } break;
      }

      int mark = MarkArena(test);
      while (1) {
        PopArena(test, mark);

        uint8_t *outputSpace = PushBytes(test, buffer->maxSize);
        bool end = false;
        if (FillBufferFromFile(buffer, inputFd)) {
          end = true;
        }

        int outputOffset = 0;
        int totalFileSize = 0;

        if (end) {
          totalFileSize = EndAES(buffer, outputSpace, &outputOffset);
        } else {
          buffer = ProcessAES(buffer, outputSpace, &outputOffset);
        }

        ssize_t res = write(outputFd, outputSpace, outputOffset);

        if (res < 0) {
          printf("There was an error writing to the file\n");
          return -1;
        }

        if (end) {
          ftruncate(outputFd, totalFileSize);
          break;
        }
      }
    }
  } break;
  case AlgorithmType_McEliece: {
    switch (mcType) {
    case McElieceType_GEN: {
      uint8_t seed[49];
      HexStringToHex(seed, OPT.seed);

      nist_kat_init(seed, NULL, 256);

      uint8_t *public_key = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_PUBLICKEYBYTES, uint8_t);
      uint8_t *secret_key = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_SECRETKEYBYTES, uint8_t);

      if (OPT.software) {
        PQCLEAN_MCELIECE348864_CLEAN_crypto_kem_keypair(public_key, secret_key);
      } else {
        VersatMcEliece(public_key, secret_key, test);
      }

      ssize_t res = write(publicFd, public_key,
                          PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_PUBLICKEYBYTES);
      res |= write(privateFd, secret_key,
                   PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_SECRETKEYBYTES);

      if (res < 0) {
        printf("There was an error writing to the file\n");
        return -1;
      }
    } break;
    case McElieceType_ENC: {
      uint8_t *chiperText = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_CIPHERTEXTBYTES, uint8_t);
      uint8_t *publicKey = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_PUBLICKEYBYTES, uint8_t);
      uint8_t *sharedKey =
          PushArray(test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES, uint8_t);

      ssize_t readAmount =
          read(publicFd, publicKey,
               PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_PUBLICKEYBYTES);
      if (readAmount != PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_PUBLICKEYBYTES) {
        printf("McEliece public key was not correct size\n");
        return -1;
      }
      PQCLEAN_MCELIECE348864_CLEAN_crypto_kem_enc(chiperText, sharedKey,
                                                  publicKey);

      {
        ssize_t res =
            write(outputFd, chiperText,
                  PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_CIPHERTEXTBYTES);
        if (res < 0) {
          printf("There was an error writing to the file\n");
          return -1;
        }
      }

      char *sharedKeyBuffer = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES * 2 + 1, char);
      char *res = GetHexadecimal(sharedKey, sharedKeyBuffer,
                                 PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES);
      sharedKeyBuffer[PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES * 2] = '\0';

      printf("%s", res);
    } break;
    case McElieceType_DEC: {
      uint8_t *chiperText = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_CIPHERTEXTBYTES, uint8_t);
      uint8_t *privateKey = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_SECRETKEYBYTES, uint8_t);
      uint8_t *sharedKey =
          PushArray(test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES, uint8_t);

      {
        ssize_t readAmount =
            read(privateFd, privateKey,
                 PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_SECRETKEYBYTES);
        if (readAmount != PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_SECRETKEYBYTES) {
          printf("McEliece private key was not correct size\n");
          return -1;
        }
      }
      {
        ssize_t readAmount =
            read(inputFd, chiperText,
                 PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_CIPHERTEXTBYTES);
        if (readAmount != PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_CIPHERTEXTBYTES) {
          printf("McEliece cipherText was not correct size\n");
          return -1;
        }
      }

      PQCLEAN_MCELIECE348864_CLEAN_crypto_kem_dec(sharedKey, chiperText,
                                                  privateKey);

      char *sharedKeyBuffer = PushArray(
          test, PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES * 2 + 1, char);
      char *res = GetHexadecimal(sharedKey, sharedKeyBuffer,
                                 PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES);
      sharedKeyBuffer[PQCLEAN_MCELIECE348864_CLEAN_CRYPTO_BYTES * 2] = '\0';

      printf("%s", res);
    } break;
    }
  } break;
  }

  return 0;
}
