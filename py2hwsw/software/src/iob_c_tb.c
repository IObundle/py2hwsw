/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>   // For memset
#include <sys/stat.h> // For mkfifo
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

  uint32_t ack = -100, mode = -100, addr = -100, dat_w = -100, dat = -100;
  int fscanf_ret, fread_ret;
  char buf[45];

  // send request
  fpw = fopen(C2V_FILE, "wb");
  if (fpw == NULL) {
    printf("C: Error opening file %s\n", C2V_FILE);
    exit(1);
  }
  fprintf(fpw, "%08x %08x %08x %08x %08x\n", req, W, address, data_w, data);
  fflush(fpw);
  fclose(fpw);
  // printf("C: New Write request %d: %08x %08x\n", req, address, data);
  my_usleep(100);

  // wait for ack
  fread_ret = fread(buf, sizeof(char), 45, fpr);
  if (fread_ret != 45)
    exit(1);
  fscanf_ret = sscanf(buf, "%08x %08x %08x %08x %08x\n", &ack, &mode, &addr,
                      &dat_w, &dat);
  if (fscanf_ret != 5)
    exit(1);
  if (ack != req || mode != W || addr != address || dat != data) {
    printf("C: Error: These values should be equal: ack/req:%d==%d mode:%d==%d "
           "addr:%d==%d dat:%d==%d\n",
           ack, req, mode, W, addr, address, dat, data);
    exit(1);
  }

  // printf("C: Written %d: %08x to %08x\n", req, data, address);
  req++;
}

// Function to read from the v2c file
uint32_t iob_read(uint32_t address, uint32_t data_w) {

  uint32_t ack = -100, mode = -100, addr = -100, dat_w = -100, dat = -100;
  int fscanf_ret, fread_ret;
  char buf[45];

  // send request
  fpw = fopen(C2V_FILE, "wb");
  if (fpw == NULL) {
    printf("C: Error opening file %s\n", C2V_FILE);
    exit(1);
  }
  fprintf(fpw, "%08x %08x %08x %08x %08x\n", req, R, address, data_w, 0);
  fflush(fpw);
  fclose(fpw);
  // printf("C: New Read requested %d: %08x\n", req, address);
  my_usleep(100);

  // wait for ack
  fread_ret = fread(buf, sizeof(char), 45, fpr);
  if (fread_ret != 45)
    exit(1);
  fscanf_ret = sscanf(buf, "%08x %08x %08x %08x %08x\n", &ack, &mode, &addr,
                      &dat_w, &dat);
  if (fscanf_ret != 5)
    exit(1);
  if (ack != req || mode != R || addr != address) {
    printf("C: Error: These values should be equal: ack/req:%d==%d mode:%d==%d "
           "addr:%d==%d\n",
           ack, req, mode, R, addr, address);
    exit(1);
  }

  // printf("C: Read %d: %08x from %08x\n", req, dat, address);
  req++;
  return dat;
}

void iob_start() {
  // Open IPC files
  fpw = fopen(C2V_FILE, "wb");
  if (fpw == NULL) {
    printf("C: Error opening file %s\n", C2V_FILE);
    exit(1);
  }
  fclose(fpw);
  // Create named pipe for responses (no need for polling)
  int result = mkfifo(V2C_FILE, 0666);
  if (result < 0) {
    printf("C: Error opening file %s\n", V2C_FILE);
    exit(1);
  }
  fpr = fopen(V2C_FILE, "rb");
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
  fclose(fpr);
  my_usleep(1000);
}

// User-supplied testbench function (must be defined by the user)
int iob_core_tb(); // Declaration

int main() {

  iob_start();

  int failed = iob_core_tb();

  // create test log file
  FILE *log = fopen("test.log", "w");
  if (failed != 0) {
    fprintf(log, "Test failed!");
  } else {
    fprintf(log, "Test passed!");
  }
  fclose(log);

  iob_finish();
}
