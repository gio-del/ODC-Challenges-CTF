from z3 import *
import time
from pwn import *

strlen = 29

s = Solver()

key = [BitVec("key%d" % i, 32) for i in range(strlen)]

# Constratints on the string
for i in key:
	s.add(i >= 0x20, i <= 0x7f) # Only Printable Characters

# Constraints from Ghidra

s.add(And(
    And(((key[5] == 45), (key[0xb] == 45))), (key[0x11] == 45), (key[0x17] == 45)
    ))
s.add(And(
    key[1] - 48 < 10, key[4] - 48 < 10, key[6] - 0x30 < 10, key[9] - 48 < 10, key[0xf] - 0x30 < 10, key[0x12] - 0x30 < 10, key[0x16] - 0x30 < 10, key[0x1b] - 0x30 < 10, key[0x1c] - 0x30 < 10
    ))
s.add(And(
    key[4] + -0x30 == (key[1] + -0x30) * 2 + 1, 7 < key[4] + -0x30, key[9] == (key[4] - (key[1] + -0x30)) + 2
    ))
s.add((key[0x1b] + key[0x1c]) % 0xd == 8)
s.add((key[0x1b] + key[0x16]) % 0x16 == 0x12)
s.add((key[0x12] + key[0x16]) % 0xb == 5)
s.add((key[0x1c] + key[0x16] + key[0x12]) % 0x1a == 4)
s.add((key[1] + key[6] * key[4]) % 0x29 == 5)
s.add((key[0xf] - key[0x1c]) % 4 == 1)
s.add((key[4] + key[0x16]) % 4 == 3)
s.add(And((key[0x14] == 66), (key[0x15] == 66)))
s.add((key[6] + key[9] * key[0xf]) % 10 == 1)
s.add((key[0x1b] + key[4] + key[0xf] + -0x12) % 0x10 == 8)
s.add((key[0x1c] - key[9]) % 2 == 1)
s.add(key[0] == 77)

p = remote("bin.training.offdef.it", 2021)
input('Enter to CRACK')

print(s.check())
m = s.model()
print(m)

key_str = ''
for i in range(strlen):
	key_str += chr(m[key[i]].as_long())

print('Key', key_str)

p.recvuntil(b'\nPlease Enter a product key to continue: \n')
p.sendline(key_str)

print('Flag:', str(p.recv(),'utf-8'))

