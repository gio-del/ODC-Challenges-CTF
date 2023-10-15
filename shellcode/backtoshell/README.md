# backtoshell

Very simple challenge. It basically reads the shellcode from stdin and executes it. We only need to pass the correct shellcode.

```asm
mov rdi, rax
add rdi, 16
mov rax, 0x3b
syscall
.string "/bin/sh"
```

RAX register contains the address of the shellcode (returned by the read syscall). We need to add 16 to it to get the address of the string "/bin/sh" (which is the first argument of the execve syscall). Then we can call execve.

Note that RSI and RDX are already set to 0, so we don't need to set them.

The complete exploit is in [script.py](script.py).
