# Reset timer
devmem 0x88000000 8 1
devmem 0x88000000 8 0
# Enable timer
devmem 0x88000001 8 1
# Enable sampling
devmem 0x88000002 8 1
# Trigger interrupt threshold
devmem 0x8800000c 32 0x05000000
devmem 0x88000010 32 0x0
# Print current count
devmem 0x88000008 32
devmem 0x88000004 32

# Verify timer interrupt count increases
cat /proc/interrupts
