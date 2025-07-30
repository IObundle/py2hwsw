#include "arena.h"

#include <stdlib.h>

#include <stdio.h>

// Arena globalArenaInst = {};
Arena *globalArena = NULL;

Arena InitArena(int size) {
  Arena arena = {};
  arena.ptr = (char *)malloc(size * sizeof(char));
  arena.allocated = size;

  return arena;
}

void *PushBytes(Arena *arena, int size) {
  char *ptr = &arena->ptr[arena->used];

  size = (size + 3) & (~3); // Align to 4 byte boundary
  arena->used += size;

  if (arena->used > arena->allocated) {
    printf("Arena overflow\n");
    printf("Size: %d,Used: %d, Allocated: %d\n", size, arena->used,
           arena->allocated);
  }

  return ptr;
}

void *PushAndZeroBytes(Arena *arena, int size) {
  char *ptr = PushBytes(arena, size);

  for (int i = 0; i < size; i++) {
    ptr[i] = 0;
  }

  return ptr;
}

int MarkArena(Arena *arena) { return arena->used; }

void PopArena(Arena *arena, int mark) { arena->used = mark; }
