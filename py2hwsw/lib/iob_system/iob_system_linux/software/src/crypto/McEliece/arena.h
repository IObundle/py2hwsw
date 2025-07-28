#ifndef H_ARENA_H
#define H_ARENA_H
#include <stdint.h>

typedef struct{
  char* ptr;
  int used;
  int allocated;
} Arena;

extern Arena* globalArena;

Arena InitArena(int size);
void* PushBytes(Arena* arena,int size);
void* PushAndZeroBytes(Arena* arena,int size);
int MarkArena(Arena* arena);
void PopArena(Arena* arena,int mark);

#define PushArray(ARENA,N_ELEM,TYPE) (TYPE*) PushBytes(ARENA,(N_ELEM) * sizeof(TYPE))

#endif // H_MEMORY_POOL_H
