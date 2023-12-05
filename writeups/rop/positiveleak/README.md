# positiveleak

## Setup

We are provided with a binary and the libc. Using `file` we can see that the binary is a 64-bit ELF.

With `checksec` we get:

```bash
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
```

Since NX is enabled we can't execute shellcode from the stack, so we have to use ROP.

With `patchelf` we can replace the libc with the one provided.

`patchelf --set-interpreter ./ld-2.35.so --replace-needed libc.so.6 ./libc-2.35.so positiveleak`

## Reversing the binary

Using IDA we can see that the binary lets us choice between 2 options:

1. Add Numbers
2. Print Numbers

### Add Numbers

```c
printf("How many would you add?");
printf("> ");
length = get_int();
stack = alloca(16 * (4 * length + 23) / 16);
printf("#> ");
num = get_int();
for (i = 0; i < length && num >= 0; ++i) {
    stack[i] = num;
    printf("[%d]#> ", i);
    num = get_int();
}
for (j = 0; j <= i; ++j)
    numbers[j] += stack[j];
```

This function asks for how many numbers we want to add, and then asks for each number. The numbers are stored in a global array of size 200.

The global array `numbers` stores `long long` values (8 bytes).

The vulnerability is in the fact that this function use alloca() to make space for the temporary numbers to store, but the space is allocated for integers (4 bytes) instead of long long (8 bytes). In fact is called `alloca(16 * (4*num + 23) / 16)`.
The multiplication and the division are there to round up the number to the nearest multiple of 16 (stack alignment).

Please note that this function ask for an extra number before the loop.

### Print Numbers

Just prints the 200 numbers stored in the global array (1600 bytes).

## Exploitation

We need to leak the libc base address and then we can, for example, use a one_gadget to get a shell.

### Leak libc

We can use the vulnerability in the `Add Numbers` function to leak the libc base address.
In fact if we add for example 6 numbers, the 5th number will be placed in the stack where the iteration counter is stored, then if we put for example `0x10ffffffff`, the counter will be set to 0x10, then in the global array will be placed 16 long longs from the stack, among which there will be the canary and a libc address.

We choose to add 6 numbers, when we add the first 5 numbers the situation will be:

```c
pwndbg> x/30gx 0x7ffc9fb3cf00 // Stack Dump
0x7ffc9fb3cf00: 0x0000000000000001  0x0000000000000002 // The first 2 numbers (1 and 2)
0x7ffc9fb3cf10: 0x0000000000000003  0x0000000000000004 // The second 2 numbers (3 and 4)
0x7ffc9fb3cf20: 0x0000000000000005  0x000000049fb3cf50 // The 5th number (5) and the counter (0x00000004)
```

When the next number is added, the counter will be overwritten, if the next number is 0x10ffffffff, the situation will be:

```c
pwndbg> x/30gx 0x7ffc9fb3cf00
0x7ffc9fb3cf00: 0x0000000000000001  0x0000000000000002
0x7ffc9fb3cf10: 0x0000000000000003  0x0000000000000004
0x7ffc9fb3cf20: 0x0000000000000005  0x00000010ffffffff // <- The core of is here
0x7ffc9fb3cf30: 0x0000000600000012      [something]    // The first 6 is the size that we choose.
```

As we can see the counter `i` is set to 0x10. Since 0x10 > 0x6 the loop will end and the 16 long longs will be copied from the stack to the global array, then we can print the array and we will get the canary and a libc address.

### Get-a-shell

[[TODO]]
