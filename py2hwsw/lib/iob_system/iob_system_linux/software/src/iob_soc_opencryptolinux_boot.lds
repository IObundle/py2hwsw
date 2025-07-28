SECTIONS {
  /* Program code */
  . = 0x00000000;
  .memory : {
    *(.init);
    *(.text);
    *(*);
  }
  . = ALIGN(4);
  _heap_start = .; 
  end = .;
}
