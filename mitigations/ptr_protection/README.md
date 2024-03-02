# ptr_protection

## Description

- checksec output:

```c
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Basically the binary lets us write integers in whatever index we want in an array, but the index is not checked, so we have arbitrary write in the stack.

The challenge is that the return address is xor'd with the canary, so we can't just overwrite the return address with the address of the win function. But we know that the canary has 0x00 as the last byte, so we can do a probabilistic attack to get to the win function by changing the last byte of the saved return address to the one of the win function and then the last but one byte of the saved return address to a random value. This random value will be xor'd with the canary, so we have a 1/256 chance of getting the right value.

The complete exploit is in [script.py](script.py).
