#ifndef INCLUDED_UNIT_CONFIGURATION
#define INCLUDED_UNIT_CONFIGURATION

#include "printf.h" 

static void IntSet(volatile void* buffer,int value,int byteSize){
   volatile int* asInt = (int*) buffer;

   int nInts = byteSize / 4;

   for(int i = 0; i < nInts; i++){
      asInt[i] = value;
   }
}

#ifdef VERSAT_DEFINED_VRead
static void ConfigureSimpleVReadBare(VReadConfig* inst){
   IntSet(inst,0,sizeof(VReadConfig));

   // Memory side
   inst->incrA = 1;
   inst->pingPong = 1;

   // B - versat side
   inst->iterB = 1;
   inst->incrB = 1;
   inst->dutyB = 1;
}

static void ConfigureSimpleVReadShallow(VReadConfig* inst, int numberItems,int* memory){
   inst->enableRead = 1;

   // Memory side
   inst->perA = numberItems;
   inst->ext_addr = (iptr) memory;
   inst->length = numberItems * sizeof(int);

   // B - versat side
   inst->perB = numberItems;
}

static void ConfigureSimpleVRead(VReadConfig* inst, int numberItems,int* memory){
   ConfigureSimpleVReadBare(inst);
   ConfigureSimpleVReadShallow(inst,numberItems,memory);
}
#endif

#ifdef VERSAT_DEFINED_VWrite
static void ConfigureSimpleVWriteBare(VWriteConfig* inst){
   IntSet(inst,0,sizeof(VWriteConfig));

   // Write side
   inst->incrA = 1;
   inst->pingPong = 1;

   // Memory side
   inst->iterB = 1;
   inst->dutyB = 1;
   inst->incrB = 1;
}

static void ConfigureSimpleVWriteShallow(VWriteConfig* inst, int numberItems,int* memory){
   inst->enableWrite = 1;

   // Write side
   inst->perA = numberItems;
   inst->length = numberItems * sizeof(int);
   inst->ext_addr = (iptr) memory;

   // Memory side
   inst->perB = numberItems;
}

static void ConfigureSimpleVWrite(VWriteConfig* inst, int numberItems,int* memory){
   ConfigureSimpleVWriteBare(inst);
   ConfigureSimpleVWriteShallow(inst,numberItems,memory);
}
#endif

#ifdef VERSAT_DEFINED_Mem
static void ConfigureMemoryOutputAndStart(MemConfig* inst, int amountOfData, int start){
   IntSet(inst,0,sizeof(MemConfig));

   inst->iterA = 1;
   inst->perA = amountOfData;
   inst->dutyA = amountOfData;
   inst->incrA = 1;
   inst->startA = start;
}

static void ConfigureMemoryOutputAndLoad(MemConfig* inst, int amountOfData, int start,MemAddr addr,int* data){
   ConfigureMemoryOutputAndStart(inst,amountOfData,start);
   VersatMemoryCopy(addr.addr,data,amountOfData * sizeof(int));
}

static void ConfigureMemoryOutput(MemConfig* inst, int amountOfData){
   IntSet(inst,0,sizeof(MemConfig));

   inst->iterA = 1;
   inst->perA = amountOfData;
   inst->dutyA = amountOfData;
   inst->incrA = 1;
}

static void ConfigureMemoryReceive(MemConfig* inst, int amountOfData){
   IntSet(inst,0,sizeof(MemConfig));

   inst->iterA = 1;
   inst->perA = amountOfData;
   inst->dutyA = amountOfData;
   inst->incrA = 1;
   inst->in0_wr = 1;
}
#endif

#endif // INCLUDED_UNIT_CONFIGURATION