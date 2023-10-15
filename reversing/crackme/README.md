# crackme

This challenge is a simple crackme that asks for a flag and checks if it is correct.

## Disassembling and reversing with Ghidra

```c
int main(int argc,char **argv) {
  code *pcVar1;
  int iVar2;

  signal(5,catch_function);
  if (argc < 2) {
    puts("USAGE: ./crackme FLAG!");
    return 1;
  }
  input = argv[1];
  pcVar1 = (code *)swi(3);
  iVar2 = (*pcVar1)();
  return iVar2;
}
```

The swi(3) is doing an int3 to trigger a SIGTRAP signal. This is used to prevent the program from being debugged. We can patch this out with a hex editor or gdb. Or we can just reverse engineer the catch_function and see what it does. This is what the `flag_cracker.c` program does. In fact, it is a very simple function: the input is xored with a key and the result is compared with another array of bytes. So we need just to xor the key array with the result bytes array to get the flag.
