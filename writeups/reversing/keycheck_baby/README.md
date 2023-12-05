# keycheck_baby

## Disassembly and decompilation

This is the simplified version of the function that is checking the flag:

```c
void check(char[32] flag) {
    unsigned char magic0[] = { ... };
    unsigned char magic1[] = { ... };

    if(flag[0...4] != "flag{") {
        return 0;
    }

    if(flag[30] != '}') {
        return 0;
    }

    for(int i = 0; i < 0xd; i++) {
        if("babuzz"[i%6] ^ flag[i+5] != magic0[i]) {
            return 0;
        }
    }

    char acc = -0x45;
    for(i = 0; i < 0xc; i++) {
        acc = acc + str[i];
        if(acc!= magic1[i]) return -1;
    }

    return 1;
}
```

## Solution

We have three(+1) checks to pass:

1) The flag must start with `flag{`
2) The flag must end with `}`
3) The flag must satisfy the equation `babuzz[i%6] ^ flag[i+5] == magic0[i]` for `i` from `0` to `0xd`, then we have that `flag[i+5] == babuzz[i%6] ^ magic0[i]` for `i` from `0` to `0xd`.

The last check is a bit trickier since there is accumulation involved.
The idea is the following:

- Find the first: flag[0] = magic1[0] - (-0x45);
- Update j: j = j + flag[0];
- Find the second: flag[1] = magic1[1] - j;
- ...

This last step can be translated in the following cracking snippet:

```c
char j = -0x45;
for(int i = 0xd; i < 0xc + 0xd; i++) {
    flag[i+5] = magic1[i-0xd] - j;
    j = j + flag[i+5];
}
```

The complete cracking program is in [flag_cracker.c](flag_cracker.c).
