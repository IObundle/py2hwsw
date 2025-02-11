#include <stdio.h>
#include <stdint.h>

void iob_write(uint32_t address, uint32_t data);
uint32_t iob_read(uint32_t address);
void iob_finish();

int iob_core_tb() {
    uint32_t data_to_send = 0x12345678;
    uint32_t expected_data = 0xABCDEF01;  // Example value coming back from Verilog
    uint32_t received_data;

    iob_write(0x1000, data_to_send); // Write data to address 0x1000
    received_data = iob_read(0x1000); // Read back from the same address

    if (received_data != expected_data) {
        fprintf(stderr, "Error: Expected 0x%08X, received 0x%08X\n", expected_data, received_data);
        return 1; // Test failed
    }
    iob_finish();
}
