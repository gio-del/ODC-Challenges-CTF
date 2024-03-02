from z3 import *
import time
from pwn import *

strlen = 45

key = [0xc, 0x11, 0x13, 0x1b, 0x1f, 1, 0x30, 0x20, 0x2c, 0x3c, 0x3c, 0x37, 0x3d, 0x3e, 4, 4, 0x12, 1, 0, 0x2d, 0x3f, 5, 2, 0x28, 0x3a, 0x11, 0x1d, 5, 0x29, 0x34, 0x35, 0x2c, 0x16, 0xd, 0x13, 0x15, 0x15, 0x13, 6, 6, 0x42, 0x4b, 0x48, 0x56, 0x16]

s = Solver()

flag = [BitVec("flag%d" % i, 32) for i in range(strlen)]

# Constratints on the string
for i in flag:
	s.add(i >= 0x20, i <= 0x7f) # Only Printable Characters

s.add(flag[0] == ord("f"))
s.add(flag[1] == ord("l"))
s.add(flag[2] == ord("a"))
s.add(flag[3] == ord("g"))
s.add(flag[4] == ord("{"))
s.add(flag[strlen-1] == ord("}"))

for i in range(strlen):
    if(i < strlen - 3):
        s.add((flag[i] ^ flag[i+1] ^ flag[i+2] ^ flag[i+3]) == key[i])
    elif(i < strlen - 2):
        s.add((flag[i] ^ flag[i+1] ^ flag[i+2] ^ flag[0]) == key[i])
    elif(i < strlen - 1):
        s.add((flag[i] ^ flag[i+1] ^ flag[1] ^ flag[0]) == key[i])
    else: # i == strlen - 1
        s.add((flag[i] ^ flag[2] ^ flag[1] ^ flag[0]) == key[i])

print(s.check())
m = s.model()

# print(m)

flag_str = ''
for i in range(strlen):
	flag_str += chr(m[flag[i]].as_long())

print('Flag', flag_str)

