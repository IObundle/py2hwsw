#include "versatCrypto.h"

#include <errno.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "arena.h"
#include "unitConfiguration.h"
#include "versat.h"
#include "versat_accel.h"

#undef ARRAY_SIZE
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof(arr[0]))

void clear_cache();

typedef struct {
  int fd;
} PhysicalAllocator;

PhysicalAllocator OpenPhysicalAllocator() {
  PhysicalAllocator res = {};
  res.fd = open("/dev/versat", O_RDWR | O_SYNC);
  if (res.fd < 0) {
    printf("Failed to open /dev/versat");
    exit(-1);
  }
  return res;
}

bool PhysicalAllocatorError(PhysicalAllocator allocator) {
  bool res = allocator.fd == 0;
  return res;
}

bool ClosePhysicalAllocator(PhysicalAllocator alloc) {
  int result = close(alloc.fd);
  bool res = (result == -1);
  return res;
}

typedef struct {
  uint8_t *virtualMemBase;
  uint8_t *physicalAddressBase;
  int size;
} PhysicalBuffer;

bool PhysicalBufferError(PhysicalBuffer buffer) {
  bool res = (buffer.virtualMemBase == NULL);
  return res;
}

PhysicalBuffer AllocatePhysicalBuffer(PhysicalAllocator allocator, int size) {
  PhysicalBuffer res = {};
  int fd = allocator.fd;
  void *virtual = mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

  if (virtual == MAP_FAILED) {
    printf("MMap failed\n");
    return res;
  }

  void *physicalAddress;
  int result = ioctl(fd, 0, &physicalAddress);

  if (result == -1) {
    printf("IO failed\n");
    return res;
  }

  res.virtualMemBase = (uint8_t *)virtual;
  res.physicalAddressBase = (uint8_t *)physicalAddress;
  res.size = size;

  return res;
}

void *ConvertVirtToPhys(PhysicalBuffer buffer, const void *virtual) {
  const uint8_t *viewVirt = virtual;
  uint8_t *viewVirtBase = buffer.virtualMemBase;
  uint8_t *viewPhys = buffer.physicalAddressBase;

  int offset = viewVirt - viewVirtBase;
  // Somehow virtual is outside allocated buffer. Program should probably give
  // some error before reaching here, but we double check it anyway.
  if (offset > buffer.size) {
    return NULL;
  }

  void *res = (void *)(viewPhys + offset);
  return res;
}

typedef enum {
  BUFFER_FREE = 0,
  BUFFER_RESERVED,  // Not being used by Versat but user copy data to it.
  BUFFER_BEING_USED // Being used by Versat. Only one buffer is allowed to be in
                    // this state at any time
} Buffer_State;

typedef enum {
  VersatType_UNITIALIZED,
  VersatType_SHA,
  VersatType_AES,
  VersatType_InvAES,
  VersatType_McEliece
} VersatType;

#define MAX_VERSAT_BUFFERS 2

typedef enum { AESType_ECB, AESType_CBC, AESType_CTR } AESType;

typedef struct {
  PhysicalAllocator alloc;
  PhysicalBuffer buffers[MAX_VERSAT_BUFFERS];
  Buffer_State bufferState[MAX_VERSAT_BUFFERS];
  VersatBuffer interface[MAX_VERSAT_BUFFERS];
  VersatType lastTypeActivated;
  bool currentlyInside;

  int bytesProcessed;
  union {
    struct {
      bool initialStateValuesLoaded;
    } SHA;

    struct {
      AESType type;
      uint8_t counter[16];
      uint8_t lastByteProcessed; // Needed to fix padding after decryption
      bool is256;
    } AES;
  };
} VersatCrypto;

static VersatCrypto versat = {};

int GetNextPowerOf2(int start) {
  int begin = 1;
  while (begin < start &&
         begin > 0) { // Overflow can occur. Make sure we do not infinite loop
    begin *= 2;
  }

  assert(begin > 0);

  return begin;
}

static PhysicalBuffer AllocateBuffer(PhysicalAllocator alloc, int attempSize) {
  PhysicalBuffer buffer = {};

  int val = 0;
  if (attempSize < 4096) {
    val = 4096;
  } else {
    val = GetNextPowerOf2(attempSize);
  }

  while (val >= 4096) {
    buffer = AllocatePhysicalBuffer(alloc, val);

    if (PhysicalBufferError(buffer)) {
      val /= 2;
    } else {
      break;
    }
  }

  if (val < 4096) {
    buffer = (PhysicalBuffer){};
    printf("Error at allocating buffer\n");
  } else {
    buffer.size =
        attempSize; // We allocate power of 2 but we reduce the persived size in
                    // order to properly test the algorithms
  }

  return buffer;
}

static uint32_t initialStateValues[] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372,
                                        0xa54ff53a, 0x510e527f, 0x9b05688c,
                                        0x1f83d9ab, 0x5be0cd19};
static uint32_t kConstants0[] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174};
static uint32_t kConstants1[] = {
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa,
    0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967};
static uint32_t kConstants2[] = {
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb,
    0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070};
static uint32_t kConstants3[] = {
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};

static uint32_t *kConstants[4] = {kConstants0, kConstants1, kConstants2,
                                  kConstants3};

void InitVersatSHA() {
  if (versat.lastTypeActivated == VersatType_SHA) {
    return;
  }

  versat.lastTypeActivated = VersatType_SHA;

  CryptoAlgosConfig *config = (CryptoAlgosConfig *)accelConfig;
  SHAConfig *sha = &config->sha;

  *sha = (SHAConfig){0};
  // ActivateMergedAccelerator(MergeType_SHA);
  ConfigureSimpleVRead(&sha->MemRead, 16, NULL);

  ACCEL_Constants_mem_iterA = 1;
  ACCEL_Constants_mem_incrA = 1;
  ACCEL_Constants_mem_perA = 16;
  ACCEL_Constants_mem_dutyA = 16;
  ACCEL_Constants_mem_startA = 0;
  ACCEL_Constants_mem_shiftA = 0;

  for (int ii = 0; ii < 16; ii++) {
    VersatUnitWrite(TOP_sha_cMem0_mem_addr, ii, kConstants[0][ii]);
  }
  for (int ii = 0; ii < 16; ii++) {
    VersatUnitWrite(TOP_sha_cMem1_mem_addr, ii, kConstants[1][ii]);
  }
  for (int ii = 0; ii < 16; ii++) {
    VersatUnitWrite(TOP_sha_cMem2_mem_addr, ii, kConstants[2][ii]);
  }
  for (int ii = 0; ii < 16; ii++) {
    VersatUnitWrite(TOP_sha_cMem3_mem_addr, ii, kConstants[3][ii]);
  }

  ACCEL_TOP_sha_Swap_enabled = 1;
}

bool InitVersat(int maxBlockSize) {
  assert(maxBlockSize >= 64);

  int mem = open("/dev/mem", O_RDWR | O_SYNC);
  if (mem == -1) {
    puts("Open mem failed\n");
    return false;
  }
  void *res = mmap(0, versatAddressSpace, PROT_READ | PROT_WRITE, MAP_SHARED,
                   mem, VERSAT_ADDRESS);

  if (res == MAP_FAILED) {
    puts("Mmap failed\n");
    printf("%d", errno);
    close(mem);
    return false;
  }

  versat_init((iptr)res);
  close(mem);

  versat = (VersatCrypto){};
  versat.alloc = OpenPhysicalAllocator();
  if (PhysicalAllocatorError(versat.alloc)) {
    puts("Physical allocator failed\n");
    return false;
  }

  versat.buffers[0] = AllocateBuffer(versat.alloc, maxBlockSize);
  if (PhysicalBufferError(versat.buffers[0])) {
    puts("Physical buffer failed\n");
    return false;
  }

  versat.buffers[1] = AllocateBuffer(versat.alloc, maxBlockSize);
  if (PhysicalBufferError(versat.buffers[1])) {
    puts("Physical buffer failed\n");
    return false;
  }

  versat.interface[0].mem = versat.buffers[0].virtualMemBase;
  versat.interface[0].maxSize = versat.buffers[0].size;
  versat.interface[1].mem = versat.buffers[1].virtualMemBase;
  versat.interface[1].maxSize = versat.buffers[1].size;

  // Start off in the SHA state
  // InitVersatSHA();

  return true;
}

static int GetVersatValidBuffer() {
  for (int i = 0; i < MAX_VERSAT_BUFFERS; i++) {
    if (versat.bufferState[i] == BUFFER_FREE) {
      return i;
    }
  }

  printf("GetVersatValidBuffer error\n");
  fflush(stdout);
  return -1;
}

static int GetIndex(VersatBuffer *input) {
  int index = input - &versat.interface[0];
  if (index < 0 || index >= MAX_VERSAT_BUFFERS) {
    printf("GetIndex error:%d\n", index);
    fflush(stdout);
  }
  return index;
}

static void FreeVersatBuffer(VersatBuffer *input) {
  int bufferIndex = GetIndex(input);
  versat.bufferState[bufferIndex] = BUFFER_FREE;
}

VersatBuffer *ReserveVersatBuffer() {
  int bufferIndex = GetVersatValidBuffer();

  versat.bufferState[bufferIndex] = BUFFER_RESERVED;

  // Always reset buffers because code is free to change these
  VersatBuffer *buffer = &versat.interface[bufferIndex];
  *buffer = (VersatBuffer){};
  buffer->mem = versat.buffers[bufferIndex].virtualMemBase;
  buffer->maxSize = versat.buffers[bufferIndex].size;

  return buffer;
}

void PrintBuffer(VersatBuffer *input) {
  printf("B:%p\n", input);
  fflush(stdout);

  if (input) {
    int index = GetIndex(input);
    printf("VB:%p %d %d %d\n", input->mem, index, input->size, input->maxSize);
    fflush(stdout);
  }
}

void HideDataVersatBuffer(VersatBuffer *input) {
  int size = input->size;
  input->mem += size;
  input->maxSize -= size;
  input->size = 0;
}

// Because our code might hide data inside the buffers, need to unhide it again
// afterwards
void NormalizeVersatBuffer(VersatBuffer *input) {
#if 0
  printf("V:%p\n",&versat);
  fflush(stdout);

  PrintBuffer(input);
#endif

  int bufferIndex = GetIndex(input);

  int delta = input->mem - versat.buffers[bufferIndex].virtualMemBase;

#if 0
  printf("D:%d %d\n",delta,bufferIndex);
  fflush(stdout);
#endif

  input->mem = versat.buffers[bufferIndex].virtualMemBase;
  input->size += delta;
  input->maxSize = versat.buffers[bufferIndex].size;

#if 0
  PrintBuffer(input);
#endif
}

bool CheckBegin() {
  if (versat.currentlyInside) {
    printf("Already called a Begin, call End beforehand");
    return true;
  }

  versat.currentlyInside = true;
  return false;
}

VersatBuffer *BeginSHA() {
  if (CheckBegin()) {
    return NULL;
  }

  InitVersatSHA();

  versat.SHA.initialStateValuesLoaded = false;
  versat.bytesProcessed = 0;

  return ReserveVersatBuffer();
}

#if 0
static char GetHexadecimalChar(unsigned char value){
  if(value < 10){
    return '0' + value;
  } else{
    return 'A' + (value - 10);
  }
}

static char* GetHexadecimal(const char* text,char* buffer,int str_size){
  int i = 0;
  unsigned char* view = (unsigned char*) text;
  for(; i< str_size; i++){
    buffer[i*2] = GetHexadecimalChar(view[i] / 16);
    buffer[i*2+1] = GetHexadecimalChar(view[i] % 16);
  }

  buffer[i*2] = '\0';

  return buffer;
}
#endif

static size_t versat_crypto_hashblocks_sha256(PhysicalBuffer *physBuffer,
                                              const uint8_t *in, size_t inlen) {
  while (inlen >= 64) {
    char buffer[128];
    ACCEL_TOP_sha_MemRead_ext_addr = (iptr)ConvertVirtToPhys(*physBuffer, in);

    // Loads data + performs work
    clear_cache();
    RunAccelerator(1);
    clear_cache();

    if (!versat.SHA.initialStateValuesLoaded) {
      VersatUnitWrite(TOP_sha_State_s_0_reg_addr, 0, initialStateValues[0]);
      VersatUnitWrite(TOP_sha_State_s_1_reg_addr, 0, initialStateValues[1]);
      VersatUnitWrite(TOP_sha_State_s_2_reg_addr, 0, initialStateValues[2]);
      VersatUnitWrite(TOP_sha_State_s_3_reg_addr, 0, initialStateValues[3]);
      VersatUnitWrite(TOP_sha_State_s_4_reg_addr, 0, initialStateValues[4]);
      VersatUnitWrite(TOP_sha_State_s_5_reg_addr, 0, initialStateValues[5]);
      VersatUnitWrite(TOP_sha_State_s_6_reg_addr, 0, initialStateValues[6]);
      VersatUnitWrite(TOP_sha_State_s_7_reg_addr, 0, initialStateValues[7]);
      versat.SHA.initialStateValuesLoaded = true;
    }

    in += 64;
    inlen -= 64;
  }

  return inlen;
}

VersatBuffer *ProcessSHA(VersatBuffer *input) {
  int bufferIndex = GetIndex(input);

  PhysicalBuffer *buffer = &versat.buffers[bufferIndex];

  NormalizeVersatBuffer(input);
  int numberBlocks = input->size / 64;

  versat_crypto_hashblocks_sha256(buffer, input->mem, numberBlocks * 64);

  int amountProcessed = numberBlocks * 64;
  int amountLeft = input->size - amountProcessed;

  input->size = amountLeft;
  // Copy what's left to the start so that we can reuse the buffer
  if (amountLeft != 0) {
    memcpy(input->mem, input->mem + amountProcessed, amountLeft * sizeof(char));
    HideDataVersatBuffer(input);
  }

  versat.bytesProcessed += amountProcessed;

  HideDataVersatBuffer(input);

  return input;
}

static void store_bigendian_32(uint8_t *x, uint32_t u) {
  x[3] = (uint8_t)u;
  u >>= 8;
  x[2] = (uint8_t)u;
  u >>= 8;
  x[1] = (uint8_t)u;
  u >>= 8;
  x[0] = (uint8_t)u;
}

void EndSHA(VersatBuffer *input, uint8_t digest[32]) {
  VersatBuffer *lastBuffer = ProcessSHA(input);

  int index = GetIndex(lastBuffer);
  PhysicalBuffer *buffer = &versat.buffers[index];

  NormalizeVersatBuffer(lastBuffer);

  uint8_t *in = (uint8_t *)lastBuffer->mem;
  size_t inlen = lastBuffer->size;

  uint64_t bytes = (uint64_t)versat.bytesProcessed + (uint64_t)inlen;

  versat_crypto_hashblocks_sha256(buffer, in, inlen);
  in += inlen;
  inlen &= 63;
  in -= inlen;

  in[inlen] = 0x80;

  if (inlen < 56) {
    for (size_t i = inlen + 1; i < 56; ++i) {
      in[i] = 0;
    }
    in[56] = (uint8_t)(bytes >> 53);
    in[57] = (uint8_t)(bytes >> 45);
    in[58] = (uint8_t)(bytes >> 37);
    in[59] = (uint8_t)(bytes >> 29);
    in[60] = (uint8_t)(bytes >> 21);
    in[61] = (uint8_t)(bytes >> 13);
    in[62] = (uint8_t)(bytes >> 5);
    in[63] = (uint8_t)(bytes << 3);
    versat_crypto_hashblocks_sha256(buffer, in, 64);
  } else {
    for (size_t i = inlen + 1; i < 120; ++i) {
      in[i] = 0;
    }
    in[120] = (uint8_t)(bytes >> 53);
    in[121] = (uint8_t)(bytes >> 45);
    in[122] = (uint8_t)(bytes >> 37);
    in[123] = (uint8_t)(bytes >> 29);
    in[124] = (uint8_t)(bytes >> 21);
    in[125] = (uint8_t)(bytes >> 13);
    in[126] = (uint8_t)(bytes >> 5);
    in[127] = (uint8_t)(bytes << 3);
    versat_crypto_hashblocks_sha256(buffer, in, 128);
  }

  // Flush last valid data
  clear_cache();
  RunAccelerator(1);

  clear_cache();

  store_bigendian_32(&digest[0 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_0_reg_addr, 0));
  store_bigendian_32(&digest[1 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_1_reg_addr, 0));
  store_bigendian_32(&digest[2 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_2_reg_addr, 0));
  store_bigendian_32(&digest[3 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_3_reg_addr, 0));
  store_bigendian_32(&digest[4 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_4_reg_addr, 0));
  store_bigendian_32(&digest[5 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_5_reg_addr, 0));
  store_bigendian_32(&digest[6 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_6_reg_addr, 0));
  store_bigendian_32(&digest[7 * 4],
                     (uint32_t)VersatUnitRead(TOP_sha_State_s_7_reg_addr, 0));

  versat.currentlyInside = false;
}

const uint8_t sbox[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b,
    0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26,
    0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2,
    0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed,
    0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f,
    0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
    0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14,
    0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d,
    0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f,
    0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11,
    0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f,
    0xb0, 0x54, 0xbb, 0x16};

const uint8_t mul2[] = {
    0x00, 0x02, 0x04, 0x06, 0x08, 0x0a, 0x0c, 0x0e, 0x10, 0x12, 0x14, 0x16,
    0x18, 0x1a, 0x1c, 0x1e, 0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e,
    0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e, 0x40, 0x42, 0x44, 0x46,
    0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e,
    0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76,
    0x78, 0x7a, 0x7c, 0x7e, 0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e,
    0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e, 0xa0, 0xa2, 0xa4, 0xa6,
    0xa8, 0xaa, 0xac, 0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe,
    0xc0, 0xc2, 0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0xd4, 0xd6,
    0xd8, 0xda, 0xdc, 0xde, 0xe0, 0xe2, 0xe4, 0xe6, 0xe8, 0xea, 0xec, 0xee,
    0xf0, 0xf2, 0xf4, 0xf6, 0xf8, 0xfa, 0xfc, 0xfe, 0x1b, 0x19, 0x1f, 0x1d,
    0x13, 0x11, 0x17, 0x15, 0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05,
    0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35, 0x2b, 0x29, 0x2f, 0x2d,
    0x23, 0x21, 0x27, 0x25, 0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55,
    0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45, 0x7b, 0x79, 0x7f, 0x7d,
    0x73, 0x71, 0x77, 0x75, 0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65,
    0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95, 0x8b, 0x89, 0x8f, 0x8d,
    0x83, 0x81, 0x87, 0x85, 0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5,
    0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5, 0xdb, 0xd9, 0xdf, 0xdd,
    0xd3, 0xd1, 0xd7, 0xd5, 0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5,
    0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5, 0xeb, 0xe9, 0xef, 0xed,
    0xe3, 0xe1, 0xe7, 0xe5};

const uint8_t mul3[] = {
    0x00, 0x03, 0x06, 0x05, 0x0c, 0x0f, 0x0a, 0x09, 0x18, 0x1b, 0x1e, 0x1d,
    0x14, 0x17, 0x12, 0x11, 0x30, 0x33, 0x36, 0x35, 0x3c, 0x3f, 0x3a, 0x39,
    0x28, 0x2b, 0x2e, 0x2d, 0x24, 0x27, 0x22, 0x21, 0x60, 0x63, 0x66, 0x65,
    0x6c, 0x6f, 0x6a, 0x69, 0x78, 0x7b, 0x7e, 0x7d, 0x74, 0x77, 0x72, 0x71,
    0x50, 0x53, 0x56, 0x55, 0x5c, 0x5f, 0x5a, 0x59, 0x48, 0x4b, 0x4e, 0x4d,
    0x44, 0x47, 0x42, 0x41, 0xc0, 0xc3, 0xc6, 0xc5, 0xcc, 0xcf, 0xca, 0xc9,
    0xd8, 0xdb, 0xde, 0xdd, 0xd4, 0xd7, 0xd2, 0xd1, 0xf0, 0xf3, 0xf6, 0xf5,
    0xfc, 0xff, 0xfa, 0xf9, 0xe8, 0xeb, 0xee, 0xed, 0xe4, 0xe7, 0xe2, 0xe1,
    0xa0, 0xa3, 0xa6, 0xa5, 0xac, 0xaf, 0xaa, 0xa9, 0xb8, 0xbb, 0xbe, 0xbd,
    0xb4, 0xb7, 0xb2, 0xb1, 0x90, 0x93, 0x96, 0x95, 0x9c, 0x9f, 0x9a, 0x99,
    0x88, 0x8b, 0x8e, 0x8d, 0x84, 0x87, 0x82, 0x81, 0x9b, 0x98, 0x9d, 0x9e,
    0x97, 0x94, 0x91, 0x92, 0x83, 0x80, 0x85, 0x86, 0x8f, 0x8c, 0x89, 0x8a,
    0xab, 0xa8, 0xad, 0xae, 0xa7, 0xa4, 0xa1, 0xa2, 0xb3, 0xb0, 0xb5, 0xb6,
    0xbf, 0xbc, 0xb9, 0xba, 0xfb, 0xf8, 0xfd, 0xfe, 0xf7, 0xf4, 0xf1, 0xf2,
    0xe3, 0xe0, 0xe5, 0xe6, 0xef, 0xec, 0xe9, 0xea, 0xcb, 0xc8, 0xcd, 0xce,
    0xc7, 0xc4, 0xc1, 0xc2, 0xd3, 0xd0, 0xd5, 0xd6, 0xdf, 0xdc, 0xd9, 0xda,
    0x5b, 0x58, 0x5d, 0x5e, 0x57, 0x54, 0x51, 0x52, 0x43, 0x40, 0x45, 0x46,
    0x4f, 0x4c, 0x49, 0x4a, 0x6b, 0x68, 0x6d, 0x6e, 0x67, 0x64, 0x61, 0x62,
    0x73, 0x70, 0x75, 0x76, 0x7f, 0x7c, 0x79, 0x7a, 0x3b, 0x38, 0x3d, 0x3e,
    0x37, 0x34, 0x31, 0x32, 0x23, 0x20, 0x25, 0x26, 0x2f, 0x2c, 0x29, 0x2a,
    0x0b, 0x08, 0x0d, 0x0e, 0x07, 0x04, 0x01, 0x02, 0x13, 0x10, 0x15, 0x16,
    0x1f, 0x1c, 0x19, 0x1a};

const uint8_t mul9[] = {
    0x00, 0x09, 0x12, 0x1b, 0x24, 0x2d, 0x36, 0x3f, 0x48, 0x41, 0x5a, 0x53,
    0x6c, 0x65, 0x7e, 0x77, 0x90, 0x99, 0x82, 0x8b, 0xb4, 0xbd, 0xa6, 0xaf,
    0xd8, 0xd1, 0xca, 0xc3, 0xfc, 0xf5, 0xee, 0xe7, 0x3b, 0x32, 0x29, 0x20,
    0x1f, 0x16, 0x0d, 0x04, 0x73, 0x7a, 0x61, 0x68, 0x57, 0x5e, 0x45, 0x4c,
    0xab, 0xa2, 0xb9, 0xb0, 0x8f, 0x86, 0x9d, 0x94, 0xe3, 0xea, 0xf1, 0xf8,
    0xc7, 0xce, 0xd5, 0xdc, 0x76, 0x7f, 0x64, 0x6d, 0x52, 0x5b, 0x40, 0x49,
    0x3e, 0x37, 0x2c, 0x25, 0x1a, 0x13, 0x08, 0x01, 0xe6, 0xef, 0xf4, 0xfd,
    0xc2, 0xcb, 0xd0, 0xd9, 0xae, 0xa7, 0xbc, 0xb5, 0x8a, 0x83, 0x98, 0x91,
    0x4d, 0x44, 0x5f, 0x56, 0x69, 0x60, 0x7b, 0x72, 0x05, 0x0c, 0x17, 0x1e,
    0x21, 0x28, 0x33, 0x3a, 0xdd, 0xd4, 0xcf, 0xc6, 0xf9, 0xf0, 0xeb, 0xe2,
    0x95, 0x9c, 0x87, 0x8e, 0xb1, 0xb8, 0xa3, 0xaa, 0xec, 0xe5, 0xfe, 0xf7,
    0xc8, 0xc1, 0xda, 0xd3, 0xa4, 0xad, 0xb6, 0xbf, 0x80, 0x89, 0x92, 0x9b,
    0x7c, 0x75, 0x6e, 0x67, 0x58, 0x51, 0x4a, 0x43, 0x34, 0x3d, 0x26, 0x2f,
    0x10, 0x19, 0x02, 0x0b, 0xd7, 0xde, 0xc5, 0xcc, 0xf3, 0xfa, 0xe1, 0xe8,
    0x9f, 0x96, 0x8d, 0x84, 0xbb, 0xb2, 0xa9, 0xa0, 0x47, 0x4e, 0x55, 0x5c,
    0x63, 0x6a, 0x71, 0x78, 0x0f, 0x06, 0x1d, 0x14, 0x2b, 0x22, 0x39, 0x30,
    0x9a, 0x93, 0x88, 0x81, 0xbe, 0xb7, 0xac, 0xa5, 0xd2, 0xdb, 0xc0, 0xc9,
    0xf6, 0xff, 0xe4, 0xed, 0x0a, 0x03, 0x18, 0x11, 0x2e, 0x27, 0x3c, 0x35,
    0x42, 0x4b, 0x50, 0x59, 0x66, 0x6f, 0x74, 0x7d, 0xa1, 0xa8, 0xb3, 0xba,
    0x85, 0x8c, 0x97, 0x9e, 0xe9, 0xe0, 0xfb, 0xf2, 0xcd, 0xc4, 0xdf, 0xd6,
    0x31, 0x38, 0x23, 0x2a, 0x15, 0x1c, 0x07, 0x0e, 0x79, 0x70, 0x6b, 0x62,
    0x5d, 0x54, 0x4f, 0x46};

const uint8_t mul11[] = {
    0x00, 0x0b, 0x16, 0x1d, 0x2c, 0x27, 0x3a, 0x31, 0x58, 0x53, 0x4e, 0x45,
    0x74, 0x7f, 0x62, 0x69, 0xb0, 0xbb, 0xa6, 0xad, 0x9c, 0x97, 0x8a, 0x81,
    0xe8, 0xe3, 0xfe, 0xf5, 0xc4, 0xcf, 0xd2, 0xd9, 0x7b, 0x70, 0x6d, 0x66,
    0x57, 0x5c, 0x41, 0x4a, 0x23, 0x28, 0x35, 0x3e, 0x0f, 0x04, 0x19, 0x12,
    0xcb, 0xc0, 0xdd, 0xd6, 0xe7, 0xec, 0xf1, 0xfa, 0x93, 0x98, 0x85, 0x8e,
    0xbf, 0xb4, 0xa9, 0xa2, 0xf6, 0xfd, 0xe0, 0xeb, 0xda, 0xd1, 0xcc, 0xc7,
    0xae, 0xa5, 0xb8, 0xb3, 0x82, 0x89, 0x94, 0x9f, 0x46, 0x4d, 0x50, 0x5b,
    0x6a, 0x61, 0x7c, 0x77, 0x1e, 0x15, 0x08, 0x03, 0x32, 0x39, 0x24, 0x2f,
    0x8d, 0x86, 0x9b, 0x90, 0xa1, 0xaa, 0xb7, 0xbc, 0xd5, 0xde, 0xc3, 0xc8,
    0xf9, 0xf2, 0xef, 0xe4, 0x3d, 0x36, 0x2b, 0x20, 0x11, 0x1a, 0x07, 0x0c,
    0x65, 0x6e, 0x73, 0x78, 0x49, 0x42, 0x5f, 0x54, 0xf7, 0xfc, 0xe1, 0xea,
    0xdb, 0xd0, 0xcd, 0xc6, 0xaf, 0xa4, 0xb9, 0xb2, 0x83, 0x88, 0x95, 0x9e,
    0x47, 0x4c, 0x51, 0x5a, 0x6b, 0x60, 0x7d, 0x76, 0x1f, 0x14, 0x09, 0x02,
    0x33, 0x38, 0x25, 0x2e, 0x8c, 0x87, 0x9a, 0x91, 0xa0, 0xab, 0xb6, 0xbd,
    0xd4, 0xdf, 0xc2, 0xc9, 0xf8, 0xf3, 0xee, 0xe5, 0x3c, 0x37, 0x2a, 0x21,
    0x10, 0x1b, 0x06, 0x0d, 0x64, 0x6f, 0x72, 0x79, 0x48, 0x43, 0x5e, 0x55,
    0x01, 0x0a, 0x17, 0x1c, 0x2d, 0x26, 0x3b, 0x30, 0x59, 0x52, 0x4f, 0x44,
    0x75, 0x7e, 0x63, 0x68, 0xb1, 0xba, 0xa7, 0xac, 0x9d, 0x96, 0x8b, 0x80,
    0xe9, 0xe2, 0xff, 0xf4, 0xc5, 0xce, 0xd3, 0xd8, 0x7a, 0x71, 0x6c, 0x67,
    0x56, 0x5d, 0x40, 0x4b, 0x22, 0x29, 0x34, 0x3f, 0x0e, 0x05, 0x18, 0x13,
    0xca, 0xc1, 0xdc, 0xd7, 0xe6, 0xed, 0xf0, 0xfb, 0x92, 0x99, 0x84, 0x8f,
    0xbe, 0xb5, 0xa8, 0xa3};

const uint8_t mul13[] = {
    0x00, 0x0d, 0x1a, 0x17, 0x34, 0x39, 0x2e, 0x23, 0x68, 0x65, 0x72, 0x7f,
    0x5c, 0x51, 0x46, 0x4b, 0xd0, 0xdd, 0xca, 0xc7, 0xe4, 0xe9, 0xfe, 0xf3,
    0xb8, 0xb5, 0xa2, 0xaf, 0x8c, 0x81, 0x96, 0x9b, 0xbb, 0xb6, 0xa1, 0xac,
    0x8f, 0x82, 0x95, 0x98, 0xd3, 0xde, 0xc9, 0xc4, 0xe7, 0xea, 0xfd, 0xf0,
    0x6b, 0x66, 0x71, 0x7c, 0x5f, 0x52, 0x45, 0x48, 0x03, 0x0e, 0x19, 0x14,
    0x37, 0x3a, 0x2d, 0x20, 0x6d, 0x60, 0x77, 0x7a, 0x59, 0x54, 0x43, 0x4e,
    0x05, 0x08, 0x1f, 0x12, 0x31, 0x3c, 0x2b, 0x26, 0xbd, 0xb0, 0xa7, 0xaa,
    0x89, 0x84, 0x93, 0x9e, 0xd5, 0xd8, 0xcf, 0xc2, 0xe1, 0xec, 0xfb, 0xf6,
    0xd6, 0xdb, 0xcc, 0xc1, 0xe2, 0xef, 0xf8, 0xf5, 0xbe, 0xb3, 0xa4, 0xa9,
    0x8a, 0x87, 0x90, 0x9d, 0x06, 0x0b, 0x1c, 0x11, 0x32, 0x3f, 0x28, 0x25,
    0x6e, 0x63, 0x74, 0x79, 0x5a, 0x57, 0x40, 0x4d, 0xda, 0xd7, 0xc0, 0xcd,
    0xee, 0xe3, 0xf4, 0xf9, 0xb2, 0xbf, 0xa8, 0xa5, 0x86, 0x8b, 0x9c, 0x91,
    0x0a, 0x07, 0x10, 0x1d, 0x3e, 0x33, 0x24, 0x29, 0x62, 0x6f, 0x78, 0x75,
    0x56, 0x5b, 0x4c, 0x41, 0x61, 0x6c, 0x7b, 0x76, 0x55, 0x58, 0x4f, 0x42,
    0x09, 0x04, 0x13, 0x1e, 0x3d, 0x30, 0x27, 0x2a, 0xb1, 0xbc, 0xab, 0xa6,
    0x85, 0x88, 0x9f, 0x92, 0xd9, 0xd4, 0xc3, 0xce, 0xed, 0xe0, 0xf7, 0xfa,
    0xb7, 0xba, 0xad, 0xa0, 0x83, 0x8e, 0x99, 0x94, 0xdf, 0xd2, 0xc5, 0xc8,
    0xeb, 0xe6, 0xf1, 0xfc, 0x67, 0x6a, 0x7d, 0x70, 0x53, 0x5e, 0x49, 0x44,
    0x0f, 0x02, 0x15, 0x18, 0x3b, 0x36, 0x21, 0x2c, 0x0c, 0x01, 0x16, 0x1b,
    0x38, 0x35, 0x22, 0x2f, 0x64, 0x69, 0x7e, 0x73, 0x50, 0x5d, 0x4a, 0x47,
    0xdc, 0xd1, 0xc6, 0xcb, 0xe8, 0xe5, 0xf2, 0xff, 0xb4, 0xb9, 0xae, 0xa3,
    0x80, 0x8d, 0x9a, 0x97};

const uint8_t mul14[] = {
    0x00, 0x0e, 0x1c, 0x12, 0x38, 0x36, 0x24, 0x2a, 0x70, 0x7e, 0x6c, 0x62,
    0x48, 0x46, 0x54, 0x5a, 0xe0, 0xee, 0xfc, 0xf2, 0xd8, 0xd6, 0xc4, 0xca,
    0x90, 0x9e, 0x8c, 0x82, 0xa8, 0xa6, 0xb4, 0xba, 0xdb, 0xd5, 0xc7, 0xc9,
    0xe3, 0xed, 0xff, 0xf1, 0xab, 0xa5, 0xb7, 0xb9, 0x93, 0x9d, 0x8f, 0x81,
    0x3b, 0x35, 0x27, 0x29, 0x03, 0x0d, 0x1f, 0x11, 0x4b, 0x45, 0x57, 0x59,
    0x73, 0x7d, 0x6f, 0x61, 0xad, 0xa3, 0xb1, 0xbf, 0x95, 0x9b, 0x89, 0x87,
    0xdd, 0xd3, 0xc1, 0xcf, 0xe5, 0xeb, 0xf9, 0xf7, 0x4d, 0x43, 0x51, 0x5f,
    0x75, 0x7b, 0x69, 0x67, 0x3d, 0x33, 0x21, 0x2f, 0x05, 0x0b, 0x19, 0x17,
    0x76, 0x78, 0x6a, 0x64, 0x4e, 0x40, 0x52, 0x5c, 0x06, 0x08, 0x1a, 0x14,
    0x3e, 0x30, 0x22, 0x2c, 0x96, 0x98, 0x8a, 0x84, 0xae, 0xa0, 0xb2, 0xbc,
    0xe6, 0xe8, 0xfa, 0xf4, 0xde, 0xd0, 0xc2, 0xcc, 0x41, 0x4f, 0x5d, 0x53,
    0x79, 0x77, 0x65, 0x6b, 0x31, 0x3f, 0x2d, 0x23, 0x09, 0x07, 0x15, 0x1b,
    0xa1, 0xaf, 0xbd, 0xb3, 0x99, 0x97, 0x85, 0x8b, 0xd1, 0xdf, 0xcd, 0xc3,
    0xe9, 0xe7, 0xf5, 0xfb, 0x9a, 0x94, 0x86, 0x88, 0xa2, 0xac, 0xbe, 0xb0,
    0xea, 0xe4, 0xf6, 0xf8, 0xd2, 0xdc, 0xce, 0xc0, 0x7a, 0x74, 0x66, 0x68,
    0x42, 0x4c, 0x5e, 0x50, 0x0a, 0x04, 0x16, 0x18, 0x32, 0x3c, 0x2e, 0x20,
    0xec, 0xe2, 0xf0, 0xfe, 0xd4, 0xda, 0xc8, 0xc6, 0x9c, 0x92, 0x80, 0x8e,
    0xa4, 0xaa, 0xb8, 0xb6, 0x0c, 0x02, 0x10, 0x1e, 0x34, 0x3a, 0x28, 0x26,
    0x7c, 0x72, 0x60, 0x6e, 0x44, 0x4a, 0x58, 0x56, 0x37, 0x39, 0x2b, 0x25,
    0x0f, 0x01, 0x13, 0x1d, 0x47, 0x49, 0x5b, 0x55, 0x7f, 0x71, 0x63, 0x6d,
    0xd7, 0xd9, 0xcb, 0xc5, 0xef, 0xe1, 0xf3, 0xfd, 0xa7, 0xa9, 0xbb, 0xb5,
    0x9f, 0x91, 0x83, 0x8d};

static const uint8_t rsbox[256] = {
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e,
    0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87,
    0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32,
    0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49,
    0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16,
    0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50,
    0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05,
    0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02,
    0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41,
    0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8,
    0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89,
    0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b,
    0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59,
    0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d,
    0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d,
    0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63,
    0x55, 0x21, 0x0c, 0x7d};

void FillLookupTable(LookupTableAddr addr, const uint8_t *mem, int size) {
  VersatMemoryCopy(addr.addr, mem, size * sizeof(uint8_t));
}

void FillKeySchedule(GenericKeySchedule256Addr addr) {
  FillLookupTable(addr.s.b_0, sbox, ARRAY_SIZE(sbox));
  FillLookupTable(addr.s.b_1, sbox, ARRAY_SIZE(sbox));
}

void FillRow(DoRowAddr addr) {
  FillLookupTable(addr.mul2_0, mul2, ARRAY_SIZE(mul2));
  FillLookupTable(addr.mul2_1, mul2, ARRAY_SIZE(mul2));
  FillLookupTable(addr.mul3_0, mul3, ARRAY_SIZE(mul3));
  FillLookupTable(addr.mul3_1, mul3, ARRAY_SIZE(mul3));
}

void FillMixColumns(MixColumnsAddr addr) {
  FillRow(addr.d_0);
  FillRow(addr.d_1);
  FillRow(addr.d_2);
  FillRow(addr.d_3);
}

void FillMainRound(FullAESRoundsAddr addr) { FillMixColumns(addr.mixColumns); }

void FillInvDoRowAddr(InvDoRowAddr addr) {
  FillLookupTable(addr.mul9_0, mul9, ARRAY_SIZE(mul9));
  FillLookupTable(addr.mul9_1, mul9, ARRAY_SIZE(mul9));
  FillLookupTable(addr.mul11_0, mul11, ARRAY_SIZE(mul11));
  FillLookupTable(addr.mul11_1, mul11, ARRAY_SIZE(mul11));
  FillLookupTable(addr.mul13_0, mul13, ARRAY_SIZE(mul13));
  FillLookupTable(addr.mul13_1, mul13, ARRAY_SIZE(mul13));
  FillLookupTable(addr.mul14_0, mul14, ARRAY_SIZE(mul14));
  FillLookupTable(addr.mul14_1, mul14, ARRAY_SIZE(mul14));
}

void FillInvMixColumns(InvMixColumnsAddr addr) {
  FillInvDoRowAddr(addr.d_0);
  FillInvDoRowAddr(addr.d_1);
  FillInvDoRowAddr(addr.d_2);
  FillInvDoRowAddr(addr.d_3);
}

void FillInvMainRound(FullAESRoundsAddr addr) {
  FillInvMixColumns(addr.invMixColumns);
}

static CryptoAlgosAddr aesAddr;

void ExpandKey(uint8_t *key) {
  static const int rcon[] = {0x01, 0x02, 0x04, 0x08, 0x10,
                             0x20, 0x40, 0x80, 0x1b, 0x36};

  CryptoAlgosConfig *config = (CryptoAlgosConfig *)accelConfig;

  RegFileAddr *view = &aesAddr.aes.key_0;
  for (int i = 0; i < 16; i++) {
    VersatUnitWrite(view[i].addr, 0, key[i]);
  }

  if (versat.AES.is256) {
    for (int i = 0; i < 16; i++) {
      VersatUnitWrite(view[i].addr, 1, key[i + 16]);
    }
  }

  config->aes.key_0.disabled = 0;

  if (versat.AES.is256) {
    for (int i = 0; i < 13; i++) {
      if (i % 2 == 1) {
        config->aes.rcon.constant = 0;
      } else {
        config->aes.rcon.constant = rcon[i / 2];
      }
      config->aes.key_0.selectedOutput0 = i;
      config->aes.key_0.selectedOutput1 = i + 1;
      config->aes.key_0.selectedInput = i + 2;
      config->aes.schedule.s.mux_0.sel = (i + 1) % 2;
      config->aes.schedule.s.mux_1.sel = (i + 1) % 2;
      config->aes.schedule.s.mux_2.sel = (i + 1) % 2;
      config->aes.schedule.s.mux_3.sel = (i + 1) % 2;

      EndAccelerator();
      StartAccelerator();
    }
  } else {
    config->aes.schedule.s.mux_0.sel = 1;
    config->aes.schedule.s.mux_1.sel = 1;
    config->aes.schedule.s.mux_2.sel = 1;
    config->aes.schedule.s.mux_3.sel = 1;
    for (int i = 0; i < 10; i++) {
      config->aes.rcon.constant = rcon[i];
      config->aes.key_0.selectedOutput0 = i;
      config->aes.key_0.selectedOutput1 = i;
      config->aes.key_0.selectedInput = i + 1;

      EndAccelerator();
      StartAccelerator();
    }
  }

  EndAccelerator();
  config->aes.key_0.disabled = 1;
}

void LoadIV(uint8_t *iv) {
  CryptoAlgosConfig *config = (CryptoAlgosConfig *)accelConfig;

  RegAddr *view = &aesAddr.aes.lastResult_0;
  for (int i = 0; i < 16; i++) {
    VersatUnitWrite(view[i].addr, 0, iv[i]);
  }

  config->aes.lastResult_0.disabled = 1;
}

void Encrypt(uint8_t *data, uint8_t *result, uint8_t *lastAddition) {
  int numberRounds = 10;
  if (versat.AES.is256) {
    numberRounds = 14;
  }

  CryptoAlgosConfig *config = (CryptoAlgosConfig *)accelConfig;

  RegAddr *view = &aesAddr.aes.state_0;
  for (int i = 0; i < 16; i++) {
    VersatUnitWrite(view[i].addr, 0, data[i]);
  }

  ActivateMergedAccelerator(MergeType_AESFirstAdd);
  config->aes.key_0.selectedOutput0 = 0;

  StartAccelerator();

  ActivateMergedAccelerator(MergeType_AESRound);

  for (int i = 0; i < (numberRounds - 1); i++) {
    config->aes.key_0.selectedOutput0 = i + 1;
    EndAccelerator();
    StartAccelerator();
  }

  ActivateMergedAccelerator(MergeType_AESLastRound);
  config->aes.key_0.selectedOutput0 = numberRounds;

  if (versat.AES.type == AESType_CBC) {
    config->aes.lastResult_0.disabled = 0;
  }

  EndAccelerator();

  if (lastAddition) {
    RegAddr *view = &aesAddr.aes.lastValToAdd_0;
    for (int i = 0; i < 16; i++) {
      VersatUnitWrite(view[i].addr, 0, lastAddition[i]);
    }
  }

  StartAccelerator();

  config->aes.lastResult_0.disabled = 1;

  EndAccelerator();

  for (int ii = 0; ii < 16; ii++) {
    result[ii] = VersatUnitRead(view[ii].addr, 0);
  }
}

void Decrypt(uint8_t *data, uint8_t *result, uint8_t *lastAddition) {
  int numberRounds = 10;
  if (versat.AES.is256) {
    numberRounds = 14;
  }

  CryptoAlgosConfig *config = (CryptoAlgosConfig *)accelConfig;

  RegAddr *view = &aesAddr.aes.state_0;
  for (int i = 0; i < 16; i++) {
    VersatUnitWrite(view[i].addr, 0, data[i]);
  }

  ActivateMergedAccelerator(MergeType_AESInvFirstAdd);
  config->aes.key_0.selectedOutput0 = numberRounds;

  StartAccelerator();

  ActivateMergedAccelerator(MergeType_AESInvRound);

  for (int i = (numberRounds - 1); i > 0; i--) {
    config->aes.key_0.selectedOutput0 = i;
    EndAccelerator();
    StartAccelerator();
  }

  ActivateMergedAccelerator(MergeType_AESInvLastRound);
  config->aes.key_0.selectedOutput0 = 0;

  EndAccelerator();

  if (lastAddition) {
    RegAddr *view = &aesAddr.aes.lastValToAdd_0;
    for (int i = 0; i < 16; i++) {
      VersatUnitWrite(view[i].addr, 0, lastAddition[i]);
    }
  }

  StartAccelerator();

  EndAccelerator();

  for (int ii = 0; ii < 16; ii++) {
    result[ii] = VersatUnitRead(view[ii].addr, 0);
  }
}

static void InitVersatAESCommon() {
  CryptoAlgosConfig *config = (CryptoAlgosConfig *)accelConfig;
  aesAddr = (CryptoAlgosAddr)ACCELERATOR_TOP_ADDR_INIT;
  FillKeySchedule(aesAddr.aes.schedule);

  {
    RegAddr *view = &aesAddr.aes.lastResult_0;
    for (int i = 0; i < 16; i++) {
      VersatUnitWrite(view[i].addr, 0, 0);
    }
  }
  {
    RegAddr *view = &aesAddr.aes.lastValToAdd_0;
    for (int i = 0; i < 16; i++) {
      VersatUnitWrite(view[i].addr, 0, 0);
    }
  }

  config->aes.lastResult_0.disabled = 1;
}

void InitVersatAES() {
  if (versat.lastTypeActivated == VersatType_AES) {
    return;
  }

  versat.lastTypeActivated = VersatType_AES;

  InitVersatAESCommon();
  FillMainRound(aesAddr.aes.round);
}

void InitVersatInvAES() {
  if (versat.lastTypeActivated == VersatType_InvAES) {
    return;
  }

  versat.lastTypeActivated = VersatType_InvAES;

  InitVersatAESCommon();
  FillInvMainRound(aesAddr.aes.round);
}

static VersatBuffer *BeginAES(uint8_t *key, uint8_t *iv, uint8_t *counter,
                              bool is256, bool isDecryption) {
  if (CheckBegin()) {
    return NULL;
  }

  versat.bytesProcessed = 0;
  versat.AES.is256 = is256;

  if (isDecryption) {
    InitVersatInvAES();
  } else {
    InitVersatAES();
  }

  ExpandKey(key);

  if (versat.AES.type == AESType_CBC) {
    if (isDecryption) {
      memcpy(versat.AES.counter, iv, 16);
    } else {
      LoadIV(iv);
    }
  }

  if (counter) {
    memcpy(versat.AES.counter, counter, sizeof(uint8_t) * 16);
  }

  return ReserveVersatBuffer();
}

VersatBuffer *BeginAES_ECB(uint8_t *key, bool is256, bool isDecryption) {
  versat.AES.type = AESType_ECB;
  return BeginAES(key, NULL, NULL, is256, isDecryption);
}

VersatBuffer *BeginAES_CBC(uint8_t *key, uint8_t *iv, bool is256,
                           bool isDecryption) {
  versat.AES.type = AESType_CBC;
  return BeginAES(key, iv, NULL, is256, isDecryption);
}

VersatBuffer *BeginAES_CTR(uint8_t *key, uint8_t *initialCounter, bool is256) {
  versat.AES.type = AESType_CTR;
  return BeginAES(key, NULL, initialCounter, is256, false);
}

VersatBuffer *ProcessAES(VersatBuffer *input, uint8_t *output,
                         int *outputOffset) {
  if (versat.lastTypeActivated != VersatType_AES &&
      versat.lastTypeActivated != VersatType_InvAES) {
    printf("Must call BeginAES_XXX before ProcessAES\n");
    return NULL;
  }

  NormalizeVersatBuffer(input);

  int size = input->size;
  int counter = 0;
  while (size >= 16) {
    if (versat.AES.type == AESType_CTR) {
      Encrypt(versat.AES.counter, output + counter, input->mem + counter);
      // TODO: Increment counter
    } else if (versat.lastTypeActivated == VersatType_AES) {
      Encrypt(input->mem + counter, output + counter, NULL);
    } else if (versat.AES.type == AESType_CBC) { // CBC
      Decrypt(input->mem + counter, output + counter, versat.AES.counter);
      memcpy(versat.AES.counter, input->mem + counter, 16);
    } else {
      Decrypt(input->mem + counter, output + counter, NULL);
    }

    counter += 16;
    size -= 16;
  }

  versat.bytesProcessed += counter;

  int amountLeft = input->size - counter;

  input->size = size;
  // Copy what's left to the start so that we can reuse the buffer
  if (amountLeft != 0) {
    memcpy(input->mem, input->mem + counter, amountLeft * sizeof(char));
    HideDataVersatBuffer(input);
  }

  if (counter > 0) {
    versat.AES.lastByteProcessed = output[counter - 1];
  }

  *outputOffset = counter;
  return input;
}

int EndAES(VersatBuffer *input, uint8_t *output, /* out */ int *outputOffset) {
  int insideOutputOffset = 0;
  VersatBuffer *lastBuffer = ProcessAES(input, output, &insideOutputOffset);

  uint8_t *ajustedOutput = output + insideOutputOffset;

  NormalizeVersatBuffer(lastBuffer);

  bool isDecryption = (versat.lastTypeActivated == VersatType_InvAES);

  if (isDecryption) {
    if (lastBuffer->size != 0) {
      printf("EndAES size different from zero when decrypting: %d\n",
             lastBuffer->size);
    }
    // lastBuffer should have zero size. Only need to fix offsets
    int paddingSize = versat.AES.lastByteProcessed;
    versat.bytesProcessed -= paddingSize;
    if (*outputOffset >= paddingSize) {
      *outputOffset -= paddingSize;
    }
  } else {
    int finalSize = lastBuffer->size;
    bool processTwoBlocks =
        (finalSize == 16); // Must always add padding, so if last block is
                           // perfect, need to add an entire dummy block
    int totalPaddingSize = (processTwoBlocks ? 32 : 16);
    uint8_t paddingToAdd = totalPaddingSize - finalSize;

    // PKCS#7 padding
    for (; lastBuffer->size < totalPaddingSize;) {
      lastBuffer->mem[lastBuffer->size++] = paddingToAdd;
    }

    if (versat.AES.type == AESType_CTR) {
      Encrypt(versat.AES.counter, ajustedOutput, lastBuffer->mem);
      // TODO: Increment counter
      if (processTwoBlocks)
        Encrypt(versat.AES.counter, ajustedOutput + 16, lastBuffer->mem + 16);
    } else if (versat.lastTypeActivated == VersatType_AES) {
      Encrypt(lastBuffer->mem, ajustedOutput, NULL);
      if (processTwoBlocks)
        Encrypt(lastBuffer->mem + 16, ajustedOutput + 16, NULL);
    }

    FreeVersatBuffer(lastBuffer);

    versat.bytesProcessed += totalPaddingSize;
    *outputOffset = insideOutputOffset + totalPaddingSize;
  }

  versat.currentlyInside = false;
  return versat.bytesProcessed;
}

// McEliece

#include "benes.h"
#include "controlbits.h"
#include "crypto_declassify.h"
#include "crypto_hash.h"
#include "crypto_uint64.h"
#include "decrypt.h"
#include "params.h"
#include "pk_gen.h"
#include "randombytes.h"
#include "root.h"
#include "sk_gen.h"
#include "uint64_sort.h"
#include "util.h"

// Prevents "cast increases required alignment" warnings by gcc
// When mat is allocated in such a way that rows are guaranteed to be aligned
#define CAST_PTR(TYPE, PTR) ((TYPE)((void *)(PTR)))

static McElieceConfig *vec;
static void *matAddr;

#define SBYTE (SYS_N / 8)
#define SINT (SBYTE / 4)

void ReadRow(uint32_t *row) {
  for (int i = 0; i < SINT; i++) {
    row[i] = VersatUnitRead(matAddr, i);
  }
}

void VersatLoadRow(uint32_t *row) {
  VersatMemoryCopy(matAddr, CAST_PTR(int *, row), SINT * sizeof(int));
}

#if 0
void PrintRow(unsigned char* view){
#if 0
  for(int i = 0; i < SBYTE; i++){
    printf("%02x",view[i]);
    if(i % 16 == 0 && i != 0){
      printf("\n");
    }
  }
#else
  for(int i = 0; i < 16; i++){
    printf("%02x",view[i]);
  }
  printf("\n");
  for(int i = SBYTE - 16; i < SBYTE; i++){
    printf("%02x",view[i]);
  }
  printf("\n");
#endif
}

void PrintFullRow(unsigned char* view){
  for(int i = 0; i < SBYTE; i++){
    printf("%02x",view[i]);
    if(i % 16 == 0 && i != 0){
      printf("\n");
    }
  }
}

void VersatPrintRow(){
  uint32_t values[SINT];
  ReadRow(values);
  PrintRow(CAST_PTR(uint8_t*,values));
}

uint8_t* GetVersatRowForTests(){  
  static uint8_t buffer[SBYTE];
  ReadRow(CAST_PTR(uint32_t*,buffer));
  return buffer;
}

void PrintSimpleMat(unsigned char** mat,int centerRow){
  PrintRow(mat[0]);
  PrintRow(mat[centerRow - 1]);
  PrintRow(mat[centerRow]);
  PrintRow(mat[centerRow + 1]);
  PrintRow(mat[PK_NROWS - 1]);
}

void PrintFullMat(unsigned char** mat){
  printf("Printing full mat:\n");
  for(int i = 0; i < PK_NROWS; i++){
    PrintFullRow(mat[i]);
  }
}
#endif

static void VersatMcElieceLoop1(PhysicalBuffer *physical, uint8_t *row,
                                uint8_t mask, bool first) {
  static uint8_t savedMask = 0;

  ConfigureSimpleVReadShallow(&vec->row, SINT,
                              ConvertVirtToPhys(*physical, row));
  if (first) {
    vec->mat.in0_wr = 0;
  } else {
    uint32_t mask_int = (savedMask) | (savedMask << 8) | (savedMask << 8 * 2) |
                        (savedMask << 8 * 3);
    vec->mask.constant = mask_int;
    vec->mat.in0_wr = 1;
  }

  EndAccelerator();
  StartAccelerator();

  savedMask = mask;
}

// Can only be called if k != row. Care
static void VersatMcElieceLoop2(PhysicalBuffer *physical, unsigned char **mat,
                                int timesCalled, int k, int row, uint8_t mask) {
  static uint8_t savedMask = 0;

  int toRead = k;
  int toCompute = ((toRead - 1 == row) ? toRead - 2 : toRead - 1);
  int toWrite = ((toCompute - 1 == row) ? toCompute - 2 : toCompute - 1);

  if (toRead < PK_NROWS) {
    vec->mat.in0_wr = 0;

    ConfigureSimpleVReadShallow(&vec->row, SINT,
                                ConvertVirtToPhys(*physical, mat[toRead]));
  } else {
    vec->row.enableRead = 0;
    toRead = -9;
  }

  if (timesCalled >= 1 && toCompute >= 0 && toCompute < PK_NROWS) {
    uint32_t mask_int = (savedMask) | (savedMask << 8) | (savedMask << 8 * 2) |
                        (savedMask << 8 * 3);

    vec->mask.constant = mask_int;
  } else {
    ConfigureSimpleVWrite(&vec->writer, SINT, (int *)NULL);
    vec->writer.enableWrite = 0;
    toCompute = -9;
  }

  if (timesCalled >= 2 && toWrite >= 0) {
    ConfigureSimpleVWrite(&vec->writer, SINT,
                          ConvertVirtToPhys(*physical, mat[toWrite]));
  } else {
    toWrite = -9;
    vec->writer.enableWrite = 0;
  }

  EndAccelerator();
  StartAccelerator();

  savedMask = mask;
}

static crypto_uint64 uint64_is_equal_declassify(uint64_t t, uint64_t u) {
  crypto_uint64 mask = crypto_uint64_equal_mask(t, u);
  crypto_declassify(&mask, sizeof mask);
  return mask;
}

static crypto_uint64 uint64_is_zero_declassify(uint64_t t) {
  crypto_uint64 mask = crypto_uint64_zero_mask(t);
  crypto_declassify(&mask, sizeof mask);
  return mask;
}

/* input: secret key sk */
/* output: public key pk */
int Versat_pk_gen(unsigned char *pk, unsigned char *sk, const uint32_t *perm,
                  int16_t *pi, Arena *temp) {
  int i, j, k;
  int row, c;

  int mark = MarkArena(temp);

  // Init needed values for versat later on.
  CryptoAlgosConfig *topConfig = (CryptoAlgosConfig *)accelConfig;
  vec = (McElieceConfig *)&topConfig->eliece;
  matAddr = (void *)TOP_eliece_mat_addr;

  int index = GetVersatValidBuffer();
  PhysicalBuffer *physical = &versat.buffers[index];

  Arena matArenaInst = {};
  Arena *matArena = &matArenaInst;
  matArena->ptr = physical->virtualMemBase;
  matArena->allocated = physical->size;

  // TODO: Error check size

  ConfigureSimpleVReadBare(&vec->row);

  vec->mat.iterA = 1;
  vec->mat.incrA = 1;
  vec->mat.iterB = 1;
  vec->mat.incrB = 1;
  vec->mat.perA = SINT + 1;
  vec->mat.dutyA = SINT + 1;
  vec->mat.perB = SINT + 1;
  vec->mat.dutyB = SINT + 1;

  uint64_t buf[1 << GFBITS];

  // SYS_N = 3488 / 8 = 436
  // PK_NROWS = 768
  // 768 * 436 = 334848 bytes which is 327 Kb

  unsigned char **mat =
      PushArray(temp, PK_NROWS, unsigned char *); // PK_NROWS = 768.
  for (int i = 0; i < PK_NROWS; i++) {
    mat[i] = PushArray(matArena, SYS_N / 8,
                       unsigned char); // This guarantees that each row is
                                       // properly aligned to a 32 bit boundary.
  }

  unsigned char mask;
  unsigned char b;

  gf *g = PushArray(temp, SYS_T + 1, gf);
  gf *L = PushArray(temp, SYS_N, gf); // support
  gf *inv = PushArray(temp, SYS_N, gf);

  g[SYS_T] = 1;

  for (i = 0; i < SYS_T; i++) {
    g[i] = load_gf(sk);
    sk += 2;
  }

  for (i = 0; i < (1 << GFBITS); i++) {
    buf[i] = perm[i];
    buf[i] <<= 31;
    buf[i] |= i;
  }

  uint64_sort(buf, 1 << GFBITS);

  for (i = 1; i < (1 << GFBITS); i++) {
    if (uint64_is_equal_declassify(buf[i - 1] >> 31, buf[i] >> 31)) {
      PopArena(temp, mark);
      return -1;
    }
  }

  for (i = 0; i < (1 << GFBITS); i++) {
    pi[i] = buf[i] & GFMASK;
  }
  for (i = 0; i < SYS_N; i++) {
    L[i] = bitrev(pi[i]);
  }

  // filling the matrix

  root(inv, g, L);

  for (i = 0; i < SYS_N; i++) {
    inv[i] = gf_inv(inv[i]);
  }

  for (i = 0; i < PK_NROWS; i++) {
    for (j = 0; j < SYS_N / 8; j++) {
      mat[i][j] = 0;
    }
  }

  for (i = 0; i < SYS_T; i++) {
    for (j = 0; j < SYS_N; j += 8) {
      for (k = 0; k < GFBITS; k++) {
        b = (inv[j + 7] >> k) & 1;
        b <<= 1;
        b |= (inv[j + 6] >> k) & 1;
        b <<= 1;
        b |= (inv[j + 5] >> k) & 1;
        b <<= 1;
        b |= (inv[j + 4] >> k) & 1;
        b <<= 1;
        b |= (inv[j + 3] >> k) & 1;
        b <<= 1;
        b |= (inv[j + 2] >> k) & 1;
        b <<= 1;
        b |= (inv[j + 1] >> k) & 1;
        b <<= 1;
        b |= (inv[j + 0] >> k) & 1;

        mat[i * GFBITS + k][j / 8] = b;
      }
    }

    for (j = 0; j < SYS_N; j++) {
      inv[j] = gf_mul(inv[j], L[j]);
    }
  }

  // gaussian elimination
  for (i = 0; i < (PK_NROWS + 7) / 8; i++) {
    for (j = 0; j < 8; j++) {
      row = i * 8 + j;

      if (row >= PK_NROWS) {
        break;
      }

      uint32_t *out_int = CAST_PTR(uint32_t *, mat[row]);
      EndAccelerator();

      VersatLoadRow(out_int);
      bool first = true;
      for (k = row + 1; k < PK_NROWS; k++) {
        mask = mat[row][i] ^ mat[k][i];
        mask >>= j;
        mask &= 1;
        mask = -mask;

        VersatMcElieceLoop1(physical, mat[k], mask, first);

        // We could fetch the value from Versat, but it's easier to calculate it
        // CPU side.
        mat[row][i] ^= mat[k][i] & mask;
        first = false;
      }

      // Last run, use valid data to compute last operation
      VersatMcElieceLoop1(physical, mat[PK_NROWS - 1], 0,
                          false); // TODO: Have a proper function instead of
                                  // sending a "fake" adress

      EndAccelerator();

      if (uint64_is_zero_declassify((mat[row][i] >> j) &
                                    1)) { // return if not systematic
        PopArena(temp, mark);
        return -1;
      }

      ReadRow(out_int);

      int index = 0;
      for (k = 0; k < PK_NROWS; k++) {
        if (k != row) {
          mask = mat[k][i] >> j;
          mask &= 1;
          mask = -mask;

          VersatMcElieceLoop2(physical, mat, index, k, row, mask);
          index += 1;
        }
      }

      VersatMcElieceLoop2(physical, mat, index++, PK_NROWS, row, 0);
      VersatMcElieceLoop2(physical, mat, index++, PK_NROWS + 1, row, 0);
      vec->writer.enableWrite = 0;

      clear_cache();
    }
  }

  for (i = 0; i < PK_NROWS; i++) {
    memcpy(pk + i * PK_ROW_BYTES, mat[i] + PK_NROWS / 8, PK_ROW_BYTES);
  }

  PopArena(temp, mark);
  return 0;
}

int VersatMcEliece(unsigned char *pk, unsigned char *sk, Arena *temp) {
  int i;
  unsigned char seed[33] = {64};
  unsigned char
      r[SYS_N / 8 + (1 << GFBITS) * sizeof(uint32_t) + SYS_T * 2 + 32];
  unsigned char *rp, *skp;

  gf f[SYS_T];                // element in GF(2^mt)
  gf irr[SYS_T];              // Goppa polynomial
  uint32_t perm[1 << GFBITS]; // random permutation as 32-bit integers
  int16_t pi[1 << GFBITS];    // random permutation

  randombytes(seed + 1, 32);

  while (1) {
    rp = &r[sizeof(r) - 32];
    skp = sk;

    // expanding and updating the seed
    shake(r, sizeof(r), seed, 33);
    memcpy(skp, seed + 1, 32);
    skp += 32 + 8;
    memcpy(seed + 1, &r[sizeof(r) - 32], 32);

    // generating irreducible polynomial
    rp -= sizeof(f);

    for (i = 0; i < SYS_T; i++) {
      f[i] = load_gf(rp + i * 2);
    }

    if (genpoly_gen(irr, f)) {
      continue;
    }

    for (i = 0; i < SYS_T; i++) {
      store_gf(skp + i * 2, irr[i]);
    }

    skp += IRR_BYTES;

    // generating permutation
    rp -= sizeof(perm);

    for (i = 0; i < (1 << GFBITS); i++) {
      perm[i] = load4(rp + i * 4);
    }

    if (Versat_pk_gen(pk, skp - IRR_BYTES, perm, pi, temp)) {
      continue;
    }

    controlbitsfrompermutation(skp, pi, GFBITS, 1 << GFBITS);
    skp += COND_BYTES;

    // storing the random string s
    rp -= SYS_N / 8;
    memcpy(skp, rp, SYS_N / 8);

    // storing positions of the 32 pivots

    store8(sk + 32, 0xFFFFFFFF);

    break;
  }

  return 0;
}
