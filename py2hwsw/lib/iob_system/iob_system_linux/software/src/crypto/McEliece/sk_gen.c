/*
  This file is for secret-key generation
*/

#include "sk_gen.h"

#include "controlbits.h"
#include "crypto_declassify.h"
#include "crypto_uint16.h"
#include "gf.h"
#include "params.h"
#include "randombytes.h"
#include "util.h"

#include "arena.h"
#include "printf.h"

static inline crypto_uint16 gf_is_zero_declassify(gf t) {
  crypto_uint16 mask = crypto_uint16_zero_mask(t);
  crypto_declassify(&mask, sizeof mask);
  return mask;
}

// Matrix Allocate
#define MA(Y, X, TYPE) PushBytes(globalArena, sizeof(TYPE) * (X) * (Y))
// Matrix Index

#define MI(Y, X, ROWSIZE) ((Y) * (ROWSIZE) + (X))
//#define MI(Y,X,ROWSIZE) Y ][ X

/* input: f, element in GF((2^m)^t) */
/* output: out, minimal polynomial of f */
/* return: 0 for success and -1 for failure */
int genpoly_gen(gf *out, gf *f) {
  int i, j, k, c;

  int mark = MarkArena(globalArena);

  gf *mat = MA(SYS_T + 1, SYS_T, gf);
  // gf mat[ SYS_T + 1 ][ SYS_T ];

  gf mask, inv, t;

  // fill matrix
  mat[MI(0, 0, SYS_T)] = 1;

  for (i = 1; i < SYS_T; i++) {
    mat[MI(0, i, SYS_T)] = 0;
  }

  for (i = 0; i < SYS_T; i++) {
    mat[MI(1, i, SYS_T)] = f[i];
  }

  for (j = 2; j <= SYS_T; j++) {
    // GF_mul(mat[j], mat[(j - 1)], f);
    GF_mul(&mat[j * SYS_T], &mat[(j - 1) * SYS_T], f);
  }

  // TODO: Potential place to accelerate using Versat
  for (j = 0; j < SYS_T; j++) {
    for (k = j + 1; k < SYS_T; k++) {
      mask = gf_iszero(mat[MI(j, j, SYS_T)]);

      for (c = j; c < SYS_T + 1; c++) {
        mat[MI(c, j, SYS_T)] ^= mat[MI(c, k, SYS_T)] & mask;
      }
    }

    if (gf_is_zero_declassify(
            mat[MI(j, j, SYS_T)])) { // return if not systematic
      PopArena(globalArena, mark);
      return -1;
    }

    inv = gf_inv(mat[MI(j, j, SYS_T)]);

    for (c = j; c < SYS_T + 1; c++) {
      mat[MI(c, j, SYS_T)] = gf_mul(mat[MI(c, j, SYS_T)], inv);
    }

    for (k = 0; k < SYS_T; k++) {
      if (k != j) {
        t = mat[MI(j, k, SYS_T)];

        for (c = j; c < SYS_T + 1; c++) {
          mat[MI(c, k, SYS_T)] ^= gf_mul(mat[MI(c, j, SYS_T)], t);
        }
      }
    }
  }

  for (i = 0; i < SYS_T; i++) {
    out[i] = mat[MI(SYS_T, i, SYS_T)];
  }

  PopArena(globalArena, mark);

  return 0;
}
