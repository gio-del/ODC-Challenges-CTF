# revmemp

The program generates a flag with this function:

```c
char * generate_flag(void) {
  int random_idx;
  char *flag;
  int i;

  flag = (char *)malloc(0x21);
  srand(0x1337);
  for (i = 0; i < 0x21; i = i + 1) {
    check_something();
    random_idx = rand();
    flag[i] = PTR_DAT_00104060[random_idx % 0x539];
  }
  return flag;
}
```

As we can see, the flag is generated with a random number generator seeded with `0x1337` and the random number is used to select a character from a table of `0x539` characters.

The issue of this function is that the random number generator is seeded with a constant value, so the flag is always the same and we can easily find it by just executing the snippet above and printing the flag.

This is what the [flag_cracker.c](flag_cracker.c) file does.
