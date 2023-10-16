# ropasaurusrex

## Setup

In this challenge we are provided a binary, the libc and the loader so we have to use patchelf.

`patchelf --set-interpreter ./ld-2.35.so --replace-needed libc.so.6 ./libc-2.35.so ropasaurusrex`

Using `file` we can see that the binary is a 32-bit ELF.

Using `checksec` we get:

```bash
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8047000)
```

Since NX is enabled we can't execute shellcode from the stack, so we have to use ROP. In particular since the binary is 32-bit we have to use a different ROP strategy w.r.t. [easyrop](../easyrop/) or [emptyspaces](../emptyspaces/).
Also, even if the binary is not PIE, we have to leak the address of a function in libc to calculate the base address of libc (if we need it) because of ASLR.

## Solution

The idea is to rejump to the main to restart the binary (we do not have a loop and we need it to leak the address of a libc function).

We use cyclic to find the offset of the return address on the stack.

`cyclic -n 4 300`

Then we send that as a payload to the binary and we get a segfault.

It crashes on 0x626161b ('kaab'). With `cyclic -n 4 -l 0x626161b` we get the offset of the return address on the stack: 140.

We can chain parameters to call a write to call write(got.read) now that we have a loop.

Since the binary is not PIE we know the address of the GOT.
We can find the address of GOT using Ghidra PTR_read for example using Show References.
