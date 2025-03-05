%include 'functions.asm'

SECTION .text
global _start

_start:
    mov eax, 90
    mov ebx, 9
    mul ebx ; mul use eax by default and only accepts one parameter (which would be multiplied by eax)
    call iprintLF
    
    call quit