#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h> // For memset
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

// Function to write to the c2v file
void iob_write(uint32_t address, uint32_t data) {

  uint32_t ack, mode;

  //open the c2v file for writing and seend write request
  fpw = fopen(C2V_FILE, "wb");
  fprintf(fpw, "%08x %08x %08x %08x\n", req, W, address, data);
  fclose(fpw);
  usleep(100);

  //wait for ack
  do {
    fpr = fopen(V2C_FILE, "rb"); // Open for reading in binary mode
    if (fpr == NULL) {
      continue;
    }
    while (fscanf(fpr, "%08x %08x %08x %08x\n", &ack, &mode, &address, &data) == EOF)
      usleep(100);
    fclose(fpr);
  } while (ack != req  || mode != W);

  printf("C: Written %08x to %08x\n", data, address);
  req++;
}

// Function to read from the v2c file
uint32_t iob_read(uint32_t address) {

  uint32_t ack, mode, data;

  //open the c2v file for writing and send read request
  fpw = fopen(C2V_FILE, "wb"); // Open for reading and writing in binary mode
  fprintf(fpw, "%08x %08x %08x %08x\n", req, R, address, 0);
  fclose(fpw);
  usleep(100);
  
  //wait for ack
  do {
    fpr = fopen(V2C_FILE, "rb"); // Open for reading and writing in binary mode
    if (fpr == NULL) {
      continue;
    }
    while (fscanf(fpr, "%08x %08x %08x %08x\n", &ack, &mode, &address, &data) == EOF)
      usleep(100);
    fclose(fpr);
  } while (ack != req  || mode != R );

  req++;
  
  return data;

}

void iob_finish() {
  fprintf(fpw, "%08x %08x %08x %08x\n", req, F, 0, 0); // Write finish
}

// User-supplied testbench function (must be defined by the user)
int iob_core_tb(); // Declaration

int main() {

  //create the c2v file for writing
  fpw = fopen(C2V_FILE, "wb"); // Open for reading and writing in binary mode
  if (fpw == NULL) {
    perror("C: Error opening c2v.txt for writing");
    exit(1);
  }
  fprintf(fpw, "%08x %08x %08x %08x\n", -2, W, 0, 0);
  printf("C: file fpw create for writing\n");
  fclose(fpw);

  //wait for the v2c file to be created and opened for reading
  fpr = NULL;
  while (fpr == NULL) {
    fpr = fopen(V2C_FILE, "rb"); // Open for reading and writing in binary mode
  }
  printf("C: file fpr opened for reading\n");
  fclose(fpr);

   // Write a dummy value to the file
  iob_write(1, 2);
  iob_finish();

  exit(0);

  // Call the user's testbench function
  //int failed = iob_core_tb();

  //return failed;
}
