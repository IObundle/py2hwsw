/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h> // For memset
#include <time.h>
#include <unistd.h>

// File names (adjust as needed)
#define C2V_FILE "c2v.txt"
#define V2C_FILE "v2c.txt"

#define R 0
#define W 1
#define F 2

static FILE *fpw;
static FILE *fpr;

static uint32_t req = 0;

void my_usleep(int microseconds) {
    struct timespec req = {0};
    req.tv_sec = microseconds / 1000000;
    req.tv_nsec = (microseconds % 1000000) * 1000;
    nanosleep(&req, NULL);
}

// Function to write to the c2v file
void iob_write(uint32_t address, uint32_t data_w, uint32_t data) {

  uint32_t ack=-100, mode=-100, addr=-100, dat_w=-100, dat=-100;
  uint32_t fscanf_ret;

  //send request
  fpw = fopen(C2V_FILE, "wb");
  if (fpw == NULL) {
    printf("C: Error opening file %s\n", C2V_FILE);
    exit(1);
  }
  fprintf(fpw, "%08x %08x %08x %08x %08x\n", req, W, address, data_w, data);
  fflush(fpw);
  fclose(fpw);
  my_usleep(100);

  int fscan_ret = -1;
  
  //wait for ack
  do {
    fpr = fopen(V2C_FILE, "rb");
    if (fpr != NULL) {
      my_usleep(100);
      fscan_ret = fscanf(fpr, "%08x %08x %08x %08x %08x\n", &ack, &mode, &addr, &dat_w, &dat);
      if (fscan_ret == 4) {
        if (ack == req && mode == W && addr == address && dat == data) {
          fclose(fpr);
          break;
        }
      }
      fclose(fpr);
    }
  } while (ack != req);

  //printf("C: Written %08x to %08x\n", data, address);
  req++;
}

// Function to read from the v2c file
uint32_t iob_read(uint32_t address, uint32_t data_w) {

  uint32_t ack=-100, mode=-100, addr=-100, dat_w=-100, dat=-100;
  uint32_t fscanf_ret;

  //send request
  fpw = fopen(C2V_FILE, "wb");
  if (fpw == NULL) {
    printf("C: Error opening file %s\n", C2V_FILE);
    exit(1);
  }
  fprintf(fpw, "%08x %08x %08x %08x %08x\n", req, R, address, data_w, 0);
  fflush(fpw);
  fclose(fpw);
  my_usleep(100);
  
  int fscan_ret = -1;

  //wait for ack
  do {
    fpr = fopen(V2C_FILE, "rb");
    if (fpr != NULL) {
      my_usleep(100);
      fscanf_ret = (fscanf (fpr, "%08x %08x %08x %08x %08x\n", &ack, &mode, &addr, &dat_w, &dat) != 0);
      if (fscan_ret == 4) {
        if (ack == req && mode == R && addr == address) {
          fclose(fpr);
          break;
        }
      }
      fclose(fpr);
    }
  } while (ack != req);

  //printf("C: Read %08x from %08x\n", dat, address);
  req++;
  return dat;
}



void iob_finish() {
  fpw = fopen(C2V_FILE, "wb");
  if (fpw == NULL) {
    printf("C: Error opening file %s\n", C2V_FILE);
    exit(1);
  }
  fprintf(fpw, "%08x %08x %08x %08x %08x\n", req, F, 0, 0, 0);
  fflush(fpw);
  fclose(fpw);
  my_usleep(1000);
}

// User-supplied testbench function (must be defined by the user)
int iob_core_tb(); // Declaration

int main() {

  int failed = iob_core_tb();
  
  iob_finish();

  // create test log file
  FILE *log = fopen("test.log", "w");
  if (failed != 0) {
    fprintf(log, "Test failed!");
  } else {
    fprintf(log, "Test passed!");
  }
  fclose(log);
 
}
