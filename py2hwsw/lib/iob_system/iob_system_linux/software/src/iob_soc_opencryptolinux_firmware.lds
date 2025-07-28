SECTIONS {
  __stack_size = DEFINED(__stack_size) ? __stack_size : 2K;
  /* Program code */
  . = 0x00000000;
  .init : { *(.init) }
  .text : { *(.text) }

  .memory : { 
    /* Read-only data */
    *(.rodata);

    /* Initialized data */
    *(.data);

    . = ALIGN(8);
    PROVIDE( __global_pointer$ = . + 0x7F0 );

    . = ALIGN(4);
    /* Uninitialized data */
    *(.bss);

    /* Any symbols not explicitly mentioned in previous sections are included in this section */
    *(*);
  }

  . = ALIGN(8);
  PROVIDE( _end = . );
  PROVIDE( end = . );

  . = ALIGN(16);
  .stack : {
    PROVIDE( _heap_end = . );
    . += __stack_size;
    PROVIDE( _sp = . );
  } 
}