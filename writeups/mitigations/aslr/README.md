# aslr

## Description

- checksec output:

```c
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Similar to [leakers](../leakers/README.md), but this time the binary is PIE and NX is enabled.
The binary reads a string from stdin into a global buffer, then it loops reading in a stack buffer and printing it out.

The stack buffer is 100 bytes long, but 200 bytes are read in. Yet another bof :D

Since there is a canary, we can first leak it by overflowing by a single byte and then reading the stack buffer.

Then, we can overflow the buffer writing the correct canary and the address of the global buffer in which we put our shellcode. But we don't know the address of the global buffer, since the binary is PIE then we need to leak an address near it and compute the offset.

The complete exploit is in [script.py](script.py).
