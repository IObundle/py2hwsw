#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h> // For memset

// File names (adjust as needed)
#define C2V_FILE "c2v.txt"
#define V2C_FILE "v2c.txt"

#define R 0
#define W 1
#define F 2

static FILE *fpw;
static FILE *fpr;

// Function to write to the c2v file
void iob_write(uint32_t address, uint32_t data) {
  fprintf(fpw, "%d %d %d\n", W, address, data); // Write address and data in hex
  fflush(fpw); // Flush to make data immediately available
}

// Function to read from the v2c file
uint32_t iob_read(uint32_t address) {

  uint32_t read_address, read_data;

  fprintf(fpw, "%d %d %d\n", R, address, 0); // Write read address
  fflush(fpw); // Flush to make data immediately available

  //wait for the data to be available
  while (!feof(fpr));

  //read the data
  int n = fscanf(fpr, "%d %d\n", &read_address, &read_data);

  if (n != 2) {
    printf("Error reading from file\n");
    exit(1);
  }

  //check if the read address is the same as the requested address
  if (read_address == address) {
    return read_data;
  } else {
    perror("Address mismatch");
    exit(1);
  }
}

void iob_finish() {
  fprintf(fpw, "%d %d %d\n", F, 0, 0); // Write finish
}

// User-supplied testbench function (must be defined by the user)
int iob_core_tb(); // Declaration

int main() {

  //open the files
  fpw = fopen(C2V_FILE, "a"); // Append mode
  if (fpw == NULL) {
    perror("Error opening c2v.txt for writing");
    exit(1); // Or handle the error as needed
  }
  
  fpr = fopen(V2C_FILE, "r");
  if (fpr == NULL) {
    perror("Error opening v2c.txt for reading");
    exit(1); // Or handle the error as needed
  }

  // Call the user's testbench function
  int failed = iob_core_tb();

  //close the files
  fclose(fpw);
  fclose(fpr);

  return failed;
}
