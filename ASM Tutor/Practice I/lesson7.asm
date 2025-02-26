; LineFeed

%include "functions.asm"

SECTION .data
    msg1 db "Hello, brave new world!", 0h
    msg2 db "This is how we recycle in NASM", 0h

SECTION .text
global _start

_start:
    mov eax, msg1
    call sprintLF

    mov eax, msg2
    call sprintLF
    
    call quit