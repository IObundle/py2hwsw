# Reset timer
devmem 0x88000000 8 1
devmem 0x88000000 8 0
# Enable timer
devmem 0x88000001 8 1
# Enable sampling
devmem 0x88000002 8 1
# Trigger interrupt threshold
devmem 0x8800000c 32 05000000
devmem 0x88000010 32 0
devmem 0x88000004 32
devmem 0x90001000 32
# Print current count
devmem 0x88000004 32
devmem 0x88000008 32
