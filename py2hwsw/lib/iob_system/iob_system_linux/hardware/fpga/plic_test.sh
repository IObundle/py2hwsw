# Set PLIC threshold for context 0 to 0 so *all* non‑zero‑priority interrupts are allowed
devmem 0x90200000 32 0x00000000

# Read PLIC pending register for first 32 sources
devmem 0x90001000 32
