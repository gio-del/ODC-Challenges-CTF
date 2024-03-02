# gonna_leak

## Description

- checksec output:

```c
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX unknown - GNU_STACK missing
    PIE:      No PIE (0x400000)
    Stack:    Executable
    RWX:      Has RWX segments
```

The binary reads a string from stdin into a stack buffer, then it loops reading in a stack buffer and printing it out.

The stack buffer is 100 bytes long, but 200 bytes are read in. Good old buffer overflow :)

We can leak the canary and a stack address by overflowing by a single byte and then reading the stack buffer.

Then, we can overflow the buffer writing our shellcode, the correct canary and the address of the stack where we put our shellcode (this is possible because the stack is executable).

The complete exploit is in [script.py](script.py).
