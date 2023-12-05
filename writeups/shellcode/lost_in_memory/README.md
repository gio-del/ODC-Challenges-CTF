# Lost In Memory

```c
lea rax, [rip]
sub rax, 0x6e
mov rdi, 1
mov rsi, rax
mov rdx, 47
mov rax, 1
syscall
```

- RAX: 1 (SYS_WRITE)
- RDI: 1 (fd = STDOUT)
- RSI: address of the flag
- RDX: 47 (length of the flag in bytes)

The idea is to use the address of the shellcode as the address of the string to print. The RIP contains the next instruction address. The flag is placed before the shellcode, so the address of the shellcode is the address of the flag minus 0x6e. Where 0x6e is the length of the flag.

The flag is 48 (0x30) bytes long. The stub is 55 (0x37) bytes long. The first instruction of the shellcode is 7 bytes long. Then 0x30 + 0x37 + 0x7 = 0x6e, that we have to subtract from the RIP.
We are using the first instruction of the shellcode because the RIP points to the next instruction.

The complete exploit is in [script.py](script.py).
