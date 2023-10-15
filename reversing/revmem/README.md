# revmem

The binary generates a flag that is compared with the user input using `strcmp`.

## Easy way

```bash
ltrace ./revmem whatever
```

Will print the strcmp arguments, so we can just copy the flag.

## "Hard" way

Very similar to the last part of [keycheck_baby](../keycheck_baby/README.md).

This solution is in [flag_cracker.c](flag_cracker.c).

## Alternative solution

Using Ghidra we can see that the function strncmp in the main is called at the offset `0x22d` within the code segment. Using gdb we can set a breakpoint at the address `0x55555555522d` and see the parameters passed to the function.
